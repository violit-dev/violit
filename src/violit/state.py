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
        if app_instance_ref[0]:
            initial_theme = app_instance_ref[0].theme_manager.preset_name
            
        GLOBAL_STORE[sid] = {
            'states': {}, 
            'tracker': DependencyTracker(),
            'builders': {},
            'actions': {},
            'component_count': 0,
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
