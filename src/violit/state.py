from typing import Any, Dict, Set
from cachetools import TTLCache
from .context import session_ctx, rendering_ctx, app_instance_ref
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

GLOBAL_STORE = TTLCache(maxsize=1000, ttl=1800)

def get_session_store():
    sid = session_ctx.get()
    if sid not in GLOBAL_STORE:
        initial_theme = 'light'
        base_count = 0  # Initialize before conditional block
        
        if app_instance_ref[0]:
            initial_theme = app_instance_ref[0].theme_manager.preset_name
        
        # INHERIT component_count from static context (None) to avoid ID collisions
        # Static components (created at import/init time) consume IDs starting from 0.
        # Dynamic components (created in session) MUST start after them.
        if None in GLOBAL_STORE:
            base_count = GLOBAL_STORE[None].get('component_count', 0)
            
        GLOBAL_STORE[sid] = {
            'states': {}, 
            'tracker': DependencyTracker(),
            'builders': {},
            'actions': {},
            'component_count': base_count,  # Start from where initial build left off
            'fragment_components': {},
            'order': [],
            'sidebar_order': [],
            'theme': Theme(initial_theme)
        }
    return GLOBAL_STORE[sid]

class State:
    def __init__(self, name: str, default_value: Any):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'default_value', default_value)

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
        store['states'][self.name] = new_value
        if 'dirty_states' not in store: store['dirty_states'] = set()
        store['dirty_states'].add(self.name)
    
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

    # Logical operators for chaining
    def __and__(self, other):
        return ComputedState(lambda: self.value and (other.value if hasattr(other, 'value') else other))
    
    def __or__(self, other):
        return ComputedState(lambda: self.value or (other.value if hasattr(other, 'value') else other))

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
