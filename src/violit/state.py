import json
import time
from typing import Any, Dict, Optional, Set, Tuple, cast
from cachetools import TTLCache
from .context import action_ctx, pending_shared_views_ctx, session_ctx, view_ctx, rendering_ctx, app_instance_ref
from .theme import Theme

STATE_SCOPE_VIEW = 'view'
STATE_SCOPE_SESSION = 'session'
STATE_SCOPE_APP = 'app'
STATE_SCOPE_SHARED = 'shared'
VALID_STATE_SCOPES = {
    STATE_SCOPE_VIEW,
    STATE_SCOPE_SESSION,
    STATE_SCOPE_APP,
    STATE_SCOPE_SHARED,
}

_SESSION_STATE_BUCKET_KEY = '__violit_session_state_bucket__'
SHARED_STATE_NAMESPACE_TTL_SECONDS = 21600
MAX_SHARED_STATE_NAMESPACES = 256
MAX_SCOPED_STATE_VALUE_BYTES = 262144

class DependencyTracker:
    def __init__(self):
        self.subscribers: Dict[str, Set[str]] = {}
    
    def register_dependency(self, state_name: str, component_id: str):
        if state_name not in self.subscribers:
            self.subscribers[state_name] = set()
        self.subscribers[state_name].add(component_id)

    def get_dirty_components(self, state_name: str) -> Set[str]:
        return self.subscribers.get(state_name, set())

    def unregister_component(self, component_id: str):
        """Remove a component from all subscriber sets.

        Call this before re-rendering a component (so stale deps are cleared
        and fresh ones are registered by the upcoming builder() call), or when
        a component is permanently gone (builder lookup returned None).
        Empty subscriber sets are pruned to prevent dict bloat.
        """
        empty_keys = []
        for state_name, cids in self.subscribers.items():
            cids.discard(component_id)
            if not cids:
                empty_keys.append(state_name)
        for k in empty_keys:
            del self.subscribers[k]


class SharedDependencyTracker:
    def __init__(self):
        self.subscribers: Dict[str, Set[Tuple[str, str, str]]] = {}

    def register_dependency(self, state_name: str, session_id: str, current_view_id: str, component_id: str):
        if state_name not in self.subscribers:
            self.subscribers[state_name] = set()
        self.subscribers[state_name].add((session_id, current_view_id, component_id))

    def get_dirty_targets(self, state_name: str) -> Set[Tuple[str, str, str]]:
        return set(self.subscribers.get(state_name, set()))

    def unregister_component(self, session_id: str, current_view_id: str, component_id: str):
        empty_keys = []
        target = (session_id, current_view_id, component_id)
        for state_name, subscribers in self.subscribers.items():
            subscribers.discard(target)
            if not subscribers:
                empty_keys.append(state_name)
        for key in empty_keys:
            del self.subscribers[key]

    def unregister_view(self, session_id: str, current_view_id: str):
        empty_keys = []
        for state_name, subscribers in self.subscribers.items():
            kept = {
                entry for entry in subscribers
                if not (entry[0] == session_id and entry[1] == current_view_id)
            }
            if kept:
                self.subscribers[state_name] = kept
            else:
                empty_keys.append(state_name)
        for key in empty_keys:
            del self.subscribers[key]

# Persistent store for static components (created during app initialization)
STATIC_STORE = {}

# TTL-cached store for per-view runtime state (expires after 6 hours [21600s] to survive mobile/PC long suspensions)
VIEW_STORE = TTLCache(maxsize=4000, ttl=21600)

# TTL-cached store for per-browser-session state (expires after 6 hours [21600s] to survive mobile/PC long suspensions)
SESSION_STORE = TTLCache(maxsize=1000, ttl=21600)

# Process-local shared state across all users in the current app instance.
APP_STATE_STORE: Dict[str, Any] = {
    'states': {},
    'tracker': SharedDependencyTracker(),
}

# Process-local namespace stores for room/board/workspace-style shared state.
SHARED_STATE_STORES: Dict[str, Dict[str, Any]] = {}
SHARED_STATE_LAST_TOUCH: Dict[str, float] = {}


def _initial_theme_name() -> str:
    if app_instance_ref[0]:
        return app_instance_ref[0].theme_manager.preset_name
    return 'light'


def _create_runtime_store(base_count: int = 0) -> Dict[str, Any]:
    return {
        'states': {},
        'tracker': DependencyTracker(),
        'builders': {},
        'actions': {},
        'submitted_values': {},
        'component_count': base_count,
        'fragment_components': {},
        'order': [],
        'sidebar_order': [],
        'theme': Theme(_initial_theme_name()),
        'dirty_states': set(),
        'forced_dirty': set(),
        'eval_queue': [],
        '_vl_chart_requested': set(),
        'toasts': [],
        'effects': [],
        'interval_callbacks': {},
        '_interval_count': 0,
    }


def _create_scoped_state_store() -> Dict[str, Any]:
    return {
        'states': {},
        'tracker': SharedDependencyTracker(),
    }


def _get_static_store() -> Dict[str, Any]:
    if not STATIC_STORE:
        STATIC_STORE.update(_create_runtime_store(base_count=0))
    return STATIC_STORE


def _refresh_ttl_entry(cache: TTLCache, key: Any):
    try:
        value = cache[key]
    except KeyError:
        return None

    cache[key] = value
    return value


def _estimate_state_value_size_bytes(value: Any) -> int:
    try:
        serialized = json.dumps(value, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        serialized = repr(value)
    return len(serialized.encode('utf-8'))


def _prune_expired_shared_state_stores(now: Optional[float] = None) -> None:
    current_time = time.monotonic() if now is None else now
    cutoff = current_time - SHARED_STATE_NAMESPACE_TTL_SECONDS
    expired_namespaces = [
        namespace
        for namespace, last_touch in SHARED_STATE_LAST_TOUCH.items()
        if last_touch < cutoff
    ]
    for namespace in expired_namespaces:
        SHARED_STATE_LAST_TOUCH.pop(namespace, None)
        SHARED_STATE_STORES.pop(namespace, None)


def _touch_shared_state_store(namespace: str, now: Optional[float] = None) -> None:
    SHARED_STATE_LAST_TOUCH[namespace] = time.monotonic() if now is None else now


def _validate_scoped_state_value(scope: str, state_name: str, new_value: Any, namespace: str | None = None) -> None:
    if scope not in {STATE_SCOPE_APP, STATE_SCOPE_SHARED}:
        return

    size_bytes = _estimate_state_value_size_bytes(new_value)
    if size_bytes <= MAX_SCOPED_STATE_VALUE_BYTES:
        return

    location = f"{scope} state '{state_name}'"
    if scope == STATE_SCOPE_SHARED and namespace:
        location = f"shared state '{state_name}' in namespace '{namespace}'"
    raise ValueError(
        f"{location} exceeds the {MAX_SCOPED_STATE_VALUE_BYTES}-byte safety limit. "
        "Store large shared data in a database or external cache instead."
    )


def get_browser_session_store() -> Dict[str, Any]:
    sid = session_ctx.get()
    if sid is None:
        return {}

    store = _refresh_ttl_entry(SESSION_STORE, sid)
    if store is None:
        store = {}
        SESSION_STORE[sid] = store
    return store


def _get_browser_session_state_store_for(
    session_id: Optional[str],
    *,
    create: bool,
) -> Optional[Dict[str, Any]]:
    if session_id is None:
        return _create_scoped_state_store() if create else None

    store = _refresh_ttl_entry(SESSION_STORE, session_id)
    if store is None:
        if not create:
            return None
        store = {}
        SESSION_STORE[session_id] = store

    bucket = store.get(_SESSION_STATE_BUCKET_KEY)
    if bucket is None:
        if not create:
            return None
        bucket = _create_scoped_state_store()
        store[_SESSION_STATE_BUCKET_KEY] = bucket
    return bucket


def get_browser_session_state_store() -> Dict[str, Any]:
    bucket = _get_browser_session_state_store_for(session_ctx.get(), create=True)
    if bucket is None:
        return _create_scoped_state_store()
    return bucket


def get_view_store(
    session_id: Optional[str] = None,
    current_view_id: Optional[str] = None,
    *,
    create: bool = True,
) -> Optional[Dict[str, Any]]:
    sid = session_id if session_id is not None else session_ctx.get()
    view_id = current_view_id if current_view_id is not None else view_ctx.get()

    if sid is None or view_id is None:
        return _get_static_store() if create else None

    key: Tuple[str, str] = (sid, view_id)
    store = _refresh_ttl_entry(VIEW_STORE, key)
    if store is None and create:
        static_store = _get_static_store()
        base_count = static_store.get('component_count', 0)
        runtime_store = _create_runtime_store(base_count=base_count)
        runtime_store['interval_callbacks'] = dict(static_store.get('interval_callbacks', {}))
        runtime_store['_interval_count'] = static_store.get('_interval_count', 0)
        VIEW_STORE[key] = runtime_store
        store = runtime_store
    return store


def get_session_store():
    store = get_view_store(create=True)
    if store is None:
        return _get_static_store()
    return store


def get_app_state_store() -> Dict[str, Any]:
    return APP_STATE_STORE


def get_shared_state_store(namespace: str) -> Dict[str, Any]:
    if not namespace:
        raise ValueError("scope='shared' requires a namespace")

    _prune_expired_shared_state_stores()

    store = SHARED_STATE_STORES.get(namespace)
    if store is not None:
        _touch_shared_state_store(namespace)
        return store

    if len(SHARED_STATE_STORES) >= MAX_SHARED_STATE_NAMESPACES:
        raise ValueError(
            f"Cannot create shared namespace '{namespace}': reached the "
            f"{MAX_SHARED_STATE_NAMESPACES}-namespace safety limit."
        )

    store = _create_scoped_state_store()
    SHARED_STATE_STORES[namespace] = store
    _touch_shared_state_store(namespace)
    return store


def get_state_store(scope: str = STATE_SCOPE_VIEW, namespace: str | None = None) -> Dict[str, Any]:
    if scope == STATE_SCOPE_VIEW:
        return get_session_store()
    if scope == STATE_SCOPE_SESSION:
        return get_browser_session_state_store()
    if scope == STATE_SCOPE_APP:
        return get_app_state_store()
    if scope == STATE_SCOPE_SHARED:
        return get_shared_state_store(namespace or '')
    raise ValueError(f"Unknown state scope: {scope}")


def get_scoped_dependency_targets(scope: str, state_name: str, namespace: str | None = None) -> Set[Tuple[str, str, str]]:
    if scope == STATE_SCOPE_VIEW:
        return set()
    store = get_state_store(scope, namespace)
    tracker = store.get('tracker')
    if tracker is None:
        return set()
    return tracker.get_dirty_targets(state_name)


def mark_scoped_views_dirty(scope: str, state_name: str, namespace: str | None = None) -> Set[Tuple[str, str]]:
    targets = get_scoped_dependency_targets(scope, state_name, namespace)
    affected_views: Set[Tuple[str, str]] = set()
    stale_targets: list[Tuple[str, str, str]] = []

    for session_id, current_view_id, component_id in targets:
        store = get_view_store(session_id, current_view_id, create=False)
        if store is None:
            stale_targets.append((session_id, current_view_id, component_id))
            continue
        store.setdefault('forced_dirty', set()).add(component_id)
        affected_views.add((session_id, current_view_id))

    if stale_targets:
        unregister_scoped_targets(scope, stale_targets, namespace)

    return affected_views


def unregister_scoped_targets(
    scope: str,
    targets: list[Tuple[str, str, str]],
    namespace: str | None = None,
) -> None:
    if scope == STATE_SCOPE_VIEW or not targets:
        return

    tracker = get_state_store(scope, namespace).get('tracker')
    if tracker is None:
        return

    for session_id, current_view_id, component_id in targets:
        tracker.unregister_component(session_id, current_view_id, component_id)


def unregister_component_from_scoped_trackers(session_id: str | None, current_view_id: str | None, component_id: str) -> None:
    if not session_id or not current_view_id:
        return

    session_store = _get_browser_session_state_store_for(session_id, create=False)
    if session_store is not None:
        session_tracker = cast(SharedDependencyTracker, session_store['tracker'])
        session_tracker.unregister_component(session_id, current_view_id, component_id)
    APP_STATE_STORE['tracker'].unregister_component(session_id, current_view_id, component_id)
    for store in SHARED_STATE_STORES.values():
        store['tracker'].unregister_component(session_id, current_view_id, component_id)


def clear_view_scoped_dependencies(session_id: str | None, current_view_id: str | None) -> None:
    if not session_id or not current_view_id:
        return

    session_store = _get_browser_session_state_store_for(session_id, create=False)
    if session_store is not None:
        session_tracker = cast(SharedDependencyTracker, session_store['tracker'])
        session_tracker.unregister_view(session_id, current_view_id)
    APP_STATE_STORE['tracker'].unregister_view(session_id, current_view_id)
    for store in SHARED_STATE_STORES.values():
        store['tracker'].unregister_view(session_id, current_view_id)


def touch_runtime_stores(session_id: str | None = None, view_id: str | None = None) -> None:
    _prune_expired_shared_state_stores()

    sid = session_id if session_id is not None else session_ctx.get()
    current_view_id = view_id if view_id is not None else view_ctx.get()

    if sid is None:
        return

    _refresh_ttl_entry(SESSION_STORE, sid)

    if current_view_id is None:
        return

    _refresh_ttl_entry(VIEW_STORE, (sid, current_view_id))


class Subscription:
    """Handle returned by State.subscribe(). Call .cancel() to unsubscribe."""

    def __init__(self, subscribers_list, entry):
        self._list = subscribers_list
        self._entry = entry
        self._active = True

    @property
    def is_active(self) -> bool:
        return self._active

    def cancel(self):
        """Remove this callback from the subscriber list."""
        if self._active:
            try:
                self._list.remove(self._entry)
            except ValueError:
                pass
            self._active = False


class State:
    name: str
    default_value: Any
    scope: str
    namespace: str | None
    _subscribers: list

    def __init__(self, name: str, default_value: Any, scope: str = STATE_SCOPE_VIEW, namespace: str | None = None):
        if scope not in VALID_STATE_SCOPES:
            raise ValueError(f"Unknown state scope: {scope}")
        if scope == STATE_SCOPE_SHARED and not namespace:
            raise ValueError("scope='shared' requires a namespace")
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'default_value', default_value)
        object.__setattr__(self, 'scope', scope)
        object.__setattr__(self, 'namespace', namespace)
        object.__setattr__(self, '_subscribers', [])  # list of (callback, wants_old_val)

    @property
    def value(self):
        store = get_state_store(self.scope, self.namespace)
        current_comp_id = rendering_ctx.get()
        if current_comp_id:
            if self.scope == STATE_SCOPE_VIEW:
                store['tracker'].register_dependency(self.name, current_comp_id)
            else:
                session_id = session_ctx.get()
                current_view_id = view_ctx.get()
                if session_id and current_view_id:
                    store['tracker'].register_dependency(self.name, session_id, current_view_id, current_comp_id)
        return store['states'].get(self.name, self.default_value)
    
    @value.setter
    def value(self, new_value: Any):
        self.set(new_value)

    def set(self, new_value: Any):
        store = get_state_store(self.scope, self.namespace)
        old_value = store['states'].get(self.name, self.default_value)
        _validate_scoped_state_value(self.scope, self.name, new_value, self.namespace)
        store['states'][self.name] = new_value
        if self.scope == STATE_SCOPE_VIEW:
            if 'dirty_states' not in store: store['dirty_states'] = set()
            store['dirty_states'].add(self.name)
        else:
            affected_views = mark_scoped_views_dirty(self.scope, self.name, self.namespace)
            pending_views = pending_shared_views_ctx.get()
            if pending_views is not None:
                pending_views.update(affected_views)
            elif affected_views:
                app = app_instance_ref[0]
                if app is not None:
                    app._schedule_scoped_state_flush(affected_views, exclude_current=action_ctx.get(False))
        # Fire side-effect subscribers
        for cb, wants_old in list(self._subscribers):
            try:
                cb(new_value, old_value) if wants_old else cb(new_value)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(
                    f"[state] subscriber error on '{self.name}': {e}"
                )

    def subscribe(self, callback) -> 'Subscription':
        """Register a side-effect callback fired on every set().

        Callback signature options:
            callback(new_val)            - receives new value only
            callback(new_val, old_val)   - receives new and previous value

        Returns a Subscription object. Call .cancel() to unsubscribe.
        """
        import inspect
        try:
            wants_old = len(inspect.signature(callback).parameters) >= 2
        except (ValueError, TypeError):
            wants_old = False
        entry = (callback, wants_old)
        self._subscribers.append(entry)
        return Subscription(self._subscribers, entry)

    def on_change(self, callback):
        """Decorator form of subscribe.

        Usage::

            @count.on_change
            def _(new_val):
                db.save('count', new_val)
        """
        self.subscribe(callback)
        return callback
    
    def __setattr__(self, attr: str, val: Any):
        if attr == 'value':
            self.set(val)
        else:
            object.__setattr__(self, attr, val)

    def __str__(self):
        return str(self.value)
    
    def __call__(self):
        return self.value
    
    def __repr__(self):
        return f"State({self.name}, {self.value}, scope={self.scope})"

    # Reactive Comparison Operators
    def __eq__(self, other): return ComputedState(lambda: self.value == (other.value if isinstance(other, (State, ComputedState)) else other))
    def __ne__(self, other): return ComputedState(lambda: self.value != (other.value if isinstance(other, (State, ComputedState)) else other))
    def __lt__(self, other): return ComputedState(lambda: self.value < (other.value if isinstance(other, (State, ComputedState)) else other))
    def __le__(self, other): return ComputedState(lambda: self.value <= (other.value if isinstance(other, (State, ComputedState)) else other))
    def __gt__(self, other): return ComputedState(lambda: self.value > (other.value if isinstance(other, (State, ComputedState)) else other))
    def __ge__(self, other): return ComputedState(lambda: self.value >= (other.value if isinstance(other, (State, ComputedState)) else other))

    # Reactive Arithmetic Operators
    def __add__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if isinstance(other, (State, ComputedState)) else other
            # If either is a string, concatenate as strings
            if isinstance(self_val, str) or isinstance(other_val, str):
                return str(self_val) + str(other_val)
            else:
                return self_val + other_val
        return ComputedState(compute)
    
    def __radd__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if isinstance(other, (State, ComputedState)) else other
            # If either is a string, concatenate as strings
            if isinstance(self_val, str) or isinstance(other_val, str):
                return str(other_val) + str(self_val)
            else:
                return other_val + self_val
        return ComputedState(compute)
    
    def __sub__(self, other): 
        return ComputedState(lambda: self.value - (other.value if isinstance(other, (State, ComputedState)) else other))
    
    def __rsub__(self, other): 
        return ComputedState(lambda: (other.value if isinstance(other, (State, ComputedState)) else other) - self.value)
    
    def __mul__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if isinstance(other, (State, ComputedState)) else other
            # String repetition: "ab" * 3 or 3 * "ab"
            if isinstance(self_val, str) or isinstance(other_val, str):
                # One must be int for string repetition to work
                if isinstance(self_val, str) and isinstance(other_val, int):
                    return self_val * other_val
                elif isinstance(other_val, str) and isinstance(self_val, int):
                    return self_val * other_val
                else:
                    # Both strings? Convert to numeric or error
                    return self_val * other_val
            else:
                return self_val * other_val
        return ComputedState(compute)
    
    def __rmul__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if isinstance(other, (State, ComputedState)) else other
            # String repetition: "ab" * 3 or 3 * "ab"
            if isinstance(self_val, str) or isinstance(other_val, str):
                if isinstance(other_val, str) and isinstance(self_val, int):
                    return other_val * self_val
                elif isinstance(self_val, str) and isinstance(other_val, int):
                    return other_val * self_val
                else:
                    return other_val * self_val
            else:
                return other_val * self_val
        return ComputedState(compute)
    
    def __truediv__(self, other): 
        return ComputedState(lambda: self.value / (other.value if isinstance(other, (State, ComputedState)) else other))
    
    def __rtruediv__(self, other): 
        return ComputedState(lambda: (other.value if isinstance(other, (State, ComputedState)) else other) / self.value)
    
    def __floordiv__(self, other): 
        return ComputedState(lambda: self.value // (other.value if isinstance(other, (State, ComputedState)) else other))
    
    def __rfloordiv__(self, other): 
        return ComputedState(lambda: (other.value if isinstance(other, (State, ComputedState)) else other) // self.value)
    
    def __mod__(self, other): 
        return ComputedState(lambda: self.value % (other.value if isinstance(other, (State, ComputedState)) else other))
    
    def __rmod__(self, other): 
        return ComputedState(lambda: (other.value if isinstance(other, (State, ComputedState)) else other) % self.value)
    
    def __pow__(self, other): 
        return ComputedState(lambda: self.value ** (other.value if isinstance(other, (State, ComputedState)) else other))
    
    def __rpow__(self, other): 
        return ComputedState(lambda: (other.value if isinstance(other, (State, ComputedState)) else other) ** self.value)
    
    # String formatting support
    def __format__(self, format_spec):
        """Support for f-string formatting: f'{state:03d}'"""
        return format(self.value, format_spec)


class ComputedState:
    """A state derived from other states (e.g. expressions)"""
    def __init__(self, func):
        self.func = func

    @property
    def value(self):
        return self.func()

    def __bool__(self):
        return bool(self.value)
    
    def __call__(self):
        return self.value

    # Reactive Comparison Operators
    def __eq__(self, other): return ComputedState(lambda: self.value == (other.value if hasattr(other, 'value') else other))
    def __ne__(self, other): return ComputedState(lambda: self.value != (other.value if hasattr(other, 'value') else other))
    def __lt__(self, other): return ComputedState(lambda: self.value < (other.value if hasattr(other, 'value') else other))
    def __le__(self, other): return ComputedState(lambda: self.value <= (other.value if hasattr(other, 'value') else other))
    def __gt__(self, other): return ComputedState(lambda: self.value > (other.value if hasattr(other, 'value') else other))
    def __ge__(self, other): return ComputedState(lambda: self.value >= (other.value if hasattr(other, 'value') else other))

    # Logical operators for chaining
    def __and__(self, other):
        return ComputedState(lambda: self.value and (other.value if hasattr(other, 'value') else other))
    
    def __or__(self, other):
        return ComputedState(lambda: self.value or (other.value if hasattr(other, 'value') else other))

    def __invert__(self):
        return ComputedState(lambda: not self.value)

    # Reactive Arithmetic Operators (Mirroring State)
    def __add__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if hasattr(other, 'value') else other
            # If either is a string, concatenate as strings
            if isinstance(self_val, str) or isinstance(other_val, str):
                return str(self_val) + str(other_val)
            else:
                return self_val + other_val
        return ComputedState(compute)
    
    def __radd__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if hasattr(other, 'value') else other
            # If either is a string, concatenate as strings
            if isinstance(self_val, str) or isinstance(other_val, str):
                return str(other_val) + str(self_val)
            else:
                return other_val + self_val
        return ComputedState(compute)
    
    def __sub__(self, other): 
        return ComputedState(lambda: self.value - (other.value if hasattr(other, 'value') else other))
    
    def __rsub__(self, other): 
        return ComputedState(lambda: (other.value if hasattr(other, 'value') else other) - self.value)
    
    def __mul__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if hasattr(other, 'value') else other
            # String repetition: "ab" * 3 or 3 * "ab"
            if isinstance(self_val, str) or isinstance(other_val, str):
                if isinstance(self_val, str) and isinstance(other_val, int):
                    return self_val * other_val
                elif isinstance(other_val, str) and isinstance(self_val, int):
                    return self_val * other_val
                else:
                    return self_val * other_val
            else:
                return self_val * other_val
        return ComputedState(compute)
    
    def __rmul__(self, other): 
        def compute():
            self_val = self.value
            other_val = other.value if hasattr(other, 'value') else other
            # String repetition: "ab" * 3 or 3 * "ab"
            if isinstance(self_val, str) or isinstance(other_val, str):
                if isinstance(other_val, str) and isinstance(self_val, int):
                    return other_val * self_val
                elif isinstance(self_val, str) and isinstance(other_val, int):
                    return other_val * self_val
                else:
                    return other_val * self_val
            else:
                return other_val * self_val
        return ComputedState(compute)
    
    def __truediv__(self, other): 
        return ComputedState(lambda: self.value / (other.value if hasattr(other, 'value') else other))
    
    def __rtruediv__(self, other): 
        return ComputedState(lambda: (other.value if hasattr(other, 'value') else other) / self.value)
    
    def __floordiv__(self, other): 
        return ComputedState(lambda: self.value // (other.value if hasattr(other, 'value') else other))
    
    def __rfloordiv__(self, other): 
        return ComputedState(lambda: (other.value if hasattr(other, 'value') else other) // self.value)
    
    def __mod__(self, other): 
        return ComputedState(lambda: self.value % (other.value if hasattr(other, 'value') else other))
    
    def __rmod__(self, other): 
        return ComputedState(lambda: (other.value if hasattr(other, 'value') else other) % self.value)
    
    def __pow__(self, other): 
        return ComputedState(lambda: self.value ** (other.value if hasattr(other, 'value') else other))
    
    def __rpow__(self, other): 
        return ComputedState(lambda: (other.value if hasattr(other, 'value') else other) ** self.value)
    
    # String formatting support
    def __format__(self, format_spec):
        return format(self.value, format_spec)
