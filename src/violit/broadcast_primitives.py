"""UI primitives for broadcast system"""

# UI Primitives Definition

UI_PRIMITIVES = {
    # List Operations
    'list.append': {
        'description': 'Append item to list (supports custom HTML)',
        'params': ['list_key', 'item_data', 'position'],
        'defaults': {'position': 'prepend'},
        'notes': 'Uses item_data.html if available, otherwise creates default card',
        'example': {
            'type': 'list.append',
            'params': {
                'list_key': 'posts',
                'item_data': 'e.detail',  # Use custom HTML if e.detail.html exists
                'position': 'prepend'
            }
        }
    },
    'list.remove': {
        'description': 'Remove item from list',
        'params': ['list_key', 'item_id'],
        'defaults': {},
        'example': {
            'type': 'list.remove',
            'params': {
                'list_key': 'posts',
                'item_id': 'e.detail.post_id'
            }
        }
    },
    'list.update': {
        'description': 'Update specific item in list',
        'params': ['list_key', 'item_id', 'item_data'],
        'defaults': {},
        'example': {
            'type': 'list.update',
            'params': {
                'list_key': 'posts',
                'item_id': 'e.detail.id',
                'item_data': 'e.detail'
            }
        }
    },
    'list.replace_all': {
        'description': 'Replace entire list (snapshot sync)',
        'params': ['list_key', 'items'],
        'defaults': {},
        'example': {
            'type': 'list.replace_all',
            'params': {
                'list_key': 'posts',
                'items': 'e.detail.posts'
            }
        }
    },
    
    # State Operations
    'state.set': {
        'description': 'Set state value',
        'params': ['state_key', 'value'],
        'defaults': {},
        'example': {
            'type': 'state.set',
            'params': {
                'state_key': 'user_count',
                'value': 'e.detail.count'
            }
        }
    },
    'state.increment': {
        'description': 'Increment state value (numeric only)',
        'params': ['state_key', 'amount'],
        'defaults': {'amount': 1},
        'example': {
            'type': 'state.increment',
            'params': {
                'state_key': 'post_count',
                'amount': 1
            }
        }
    },
    'state.decrement': {
        'description': 'Decrement state value (numeric only)',
        'params': ['state_key', 'amount'],
        'defaults': {'amount': 1},
        'example': {
            'type': 'state.decrement',
            'params': {
                'state_key': 'post_count',
                'amount': 1
            }
        }
    },
    
    # DOM Operations
    'dom.insert': {
        'description': 'Insert HTML element',
        'params': ['container_id', 'html', 'position'],
        'defaults': {'position': 'prepend'},
        'example': {
            'type': 'dom.insert',
            'params': {
                'container_id': 'notifications',
                'html': 'e.detail.html',
                'position': 'prepend'
            }
        }
    },
    'dom.remove': {
        'description': 'Remove DOM element',
        'params': ['selector', 'animate'],
        'defaults': {'animate': True},
        'example': {
            'type': 'dom.remove',
            'params': {
                'selector': '[data-item-id="123"]',
                'animate': True
            }
        }
    },
    'dom.update': {
        'description': 'Update DOM element content',
        'params': ['selector', 'html'],
        'defaults': {},
        'example': {
            'type': 'dom.update',
            'params': {
                'selector': '#status',
                'html': 'e.detail.status'
            }
        }
    },
    
    # Feedback Operations
    'feedback.toast': {
        'description': 'Display toast notification',
        'params': ['message', 'variant', 'duration'],
        'defaults': {'variant': 'neutral', 'duration': 3000},
        'example': {
            'type': 'feedback.toast',
            'params': {
                'message': "'Task completed!'",
                'variant': 'success',
                'duration': 3000
            }
        }
    },
    'feedback.badge': {
        'description': 'Update badge value',
        'params': ['badge_id', 'value'],
        'defaults': {},
        'example': {
            'type': 'feedback.badge',
            'params': {
                'badge_id': 'notification-badge',
                'value': 'e.detail.count'
            }
        }
    },
}


def get_primitive_names():
    """Return list of available primitive names"""
    return list(UI_PRIMITIVES.keys())


def get_primitive_info(primitive_name):
    """Return info for a specific primitive"""
    return UI_PRIMITIVES.get(primitive_name)


def validate_primitive(primitive_dict):
    """Validate primitive dictionary structure"""
    if 'type' not in primitive_dict:
        return False, "Missing 'type' field"
    
    prim_type = primitive_dict['type']
    if prim_type not in UI_PRIMITIVES:
        return False, f"Unknown primitive: {prim_type}"
    
    if 'params' not in primitive_dict:
        return False, "Missing 'params' field"
    
    prim_info = UI_PRIMITIVES[prim_type]
    required_params = prim_info['params']
    provided_params = primitive_dict['params'].keys()
    defaults = prim_info.get('defaults', {})
    missing_params = [p for p in required_params if p not in provided_params and p not in defaults]
    
    if missing_params:
        return False, f"Missing required params: {missing_params}"
    
    return True, "OK"

