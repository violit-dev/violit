from typing import Any, Dict, Set, Tuple
from cachetools import TTLCache
from .context import session_ctx, view_ctx, rendering_ctx, app_instance_ref
from .theme import Theme

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

# Persistent store for static components (created during app initialization)
STATIC_STORE = {}

# TTL-cached store for per-view runtime state (expires after 1800s of inactivity)
VIEW_STORE = TTLCache(maxsize=4000, ttl=1800)

# TTL-cached store for per-browser-session state (expires after 1800s of inactivity)
SESSION_STORE = TTLCache(maxsize=1000, ttl=1800)


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


def get_browser_session_store() -> Dict[str, Any]:
    sid = session_ctx.get()
    if sid is None:
        return {}

    store = _refresh_ttl_entry(SESSION_STORE, sid)
    if store is None:
        store = {}
        SESSION_STORE[sid] = store
    return store


def get_session_store():
    sid = session_ctx.get()
    current_view_id = view_ctx.get()
    
    # Static context (initial build)
    if sid is None or current_view_id is None:
        return _get_static_store()
        
    key: Tuple[str, str] = (sid, current_view_id)
    store = _refresh_ttl_entry(VIEW_STORE, key)
    if store is None:
        static_store = _get_static_store()
        base_count = static_store.get('component_count', 0)
        runtime_store = _create_runtime_store(base_count=base_count)
        runtime_store['interval_callbacks'] = dict(static_store.get('interval_callbacks', {}))
        runtime_store['_interval_count'] = static_store.get('_interval_count', 0)
        VIEW_STORE[key] = runtime_store
        store = runtime_store
    return store


def touch_runtime_stores(session_id: str | None = None, view_id: str | None = None) -> None:
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
    def __init__(self, name: str, default_value: Any):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'default_value', default_value)
        object.__setattr__(self, '_subscribers', [])  # list of (callback, wants_old_val)

    @property
    def value(self):
        store = get_session_store()
        current_comp_id = rendering_ctx.get()
        if current_comp_id:
            store['tracker'].register_dependency(self.name, current_comp_id)
        return store['states'].get(self.name, self.default_value)
    
    @value.setter
    def value(self, new_value: Any):
        self.set(new_value)

    def set(self, new_value: Any):
        store = get_session_store()
        old_value = store['states'].get(self.name, self.default_value)
        store['states'][self.name] = new_value
        if 'dirty_states' not in store: store['dirty_states'] = set()
        store['dirty_states'].add(self.name)
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
        return f"State({self.name}, {self.value})"

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
