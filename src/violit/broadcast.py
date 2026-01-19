"""WebSocket-based real-time broadcasting system"""

import asyncio
import threading
from typing import Dict, Any, Callable, Optional, List
import json
import uuid

from .broadcast_primitives import UI_PRIMITIVES, validate_primitive


class Broadcaster:
    """WebSocket-based real-time broadcasting system"""
    
    def __init__(self, app):
        self.app = app
        self._bindings: Dict[str, Dict] = {}
        self._primitives = UI_PRIMITIVES
        self._router_injected = False
    
    # Core: Event Broadcasting
    
    def get_active_sessions(self) -> list:
        if not hasattr(self.app, 'ws_engine') or not self.app.ws_engine:
            return []
        return list(self.app.ws_engine.sockets.keys())
    
    async def _broadcast_eval_async(self, js_code: str, exclude_session: Optional[str] = None):
        if not hasattr(self.app, 'ws_engine') or not self.app.ws_engine:
            print("[BROADCAST] WebSocket engine not available.")
            return
        
        active_sids = self.get_active_sessions()
        
        if exclude_session:
            active_sids = [sid for sid in active_sids if sid != exclude_session]
        
        print(f"[BROADCAST] Starting: {len(active_sids)} sessions")
        
        success_count = 0
        for sid in active_sids:
            try:
                await self.app.ws_engine.push_eval(sid, js_code)
                success_count += 1
            except Exception as e:
                print(f"[BROADCAST] Failed for session {sid[:8]}...: {e}")
        
        print(f"[BROADCAST] Completed: {success_count}/{len(active_sids)} successful")
    
    def eval_all(self, js_code: str, exclude_current: bool = False):
        """Send JavaScript code to all clients (low-level API)
        
        Args:
            js_code: JavaScript code to execute
            exclude_current: Exclude current session
        """
        from .context import session_ctx
        
        exclude_session = None
        if exclude_current:
            try:
                exclude_session = session_ctx.get()
            except:
                pass
        
        def run_broadcast():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._broadcast_eval_async(js_code, exclude_session))
                loop.close()
            except Exception as e:
                print(f"[BROADCAST] Execution failed: {e}")
        
        thread = threading.Thread(target=run_broadcast, daemon=True)
        thread.start()
    
    def broadcast_event(self, event_name: str, data: Dict[str, Any], 
                       exclude_current: bool = False):
        """Broadcast domain event to all clients
        
        Args:
            event_name: Event name (e.g. 'post_added', 'user_joined')
            data: Event data (must be JSON-serializable)
            exclude_current: Exclude current session
        """
        # Auto-generate event ID for deduplication
        if '_eventId' not in data:
            data['_eventId'] = str(uuid.uuid4())
        
        data_json = json.dumps(data)
        
        js_code = f"""
        (function() {{
            const event = new CustomEvent('{event_name}', {{
                detail: {data_json}
            }});
            window.dispatchEvent(event);
            console.log('🔔 Event received: {event_name}');
        }})();
        """
        
        self.eval_all(js_code, exclude_current=exclude_current)
    
    # Widget-Level Bindings
    
    def bind_list(self, 
                  list_key: str,
                  on_append: str = None,
                  on_remove: str = None,
                  on_update: str = None,
                  on_replace: str = None) -> None:
        """Register event bindings for list widget
        
        Args:
            list_key: List widget key
            on_append: Event name to trigger append
            on_remove: Event name to trigger remove
            on_update: Event name to trigger update
            on_replace: Event name to trigger replace_all
        """
        if on_append:
            self._register_binding(on_append, {
                'type': 'list.append',
                'params': {
                    'list_key': list_key,
                    'item_data': 'e.detail',
                    'position': 'prepend'
                }
            })
        
        if on_remove:
            self._register_binding(on_remove, {
                'type': 'list.remove',
                'params': {
                    'list_key': list_key,
                    'item_id': 'e.detail.id || e.detail.post_id'
                }
            })
        
        if on_update:
            self._register_binding(on_update, {
                'type': 'list.update',
                'params': {
                    'list_key': list_key,
                    'item_id': 'e.detail.id',
                    'item_data': 'e.detail'
                }
            })
        
        if on_replace:
            self._register_binding(on_replace, {
                'type': 'list.replace_all',
                'params': {
                    'list_key': list_key,
                    'items': 'e.detail.items || e.detail'
                }
            })
    
    def bind_state(self,
                   state_key: str,
                   on_set: str = None,
                   on_increment: str = None,
                   on_decrement: str = None) -> None:
        """Register event bindings for state
        
        Args:
            state_key: State key
            on_set: Event name to trigger set
            on_increment: Event name to trigger increment
            on_decrement: Event name to trigger decrement
        """
        if on_set:
            self._register_binding(on_set, {
                'type': 'state.set',
                'params': {
                    'state_key': state_key,
                    'value': 'e.detail.value || e.detail'
                }
            })
        
        if on_increment:
            self._register_binding(on_increment, {
                'type': 'state.increment',
                'params': {
                    'state_key': state_key,
                    'amount': 'e.detail.amount || 1'
                }
            })
        
        if on_decrement:
            self._register_binding(on_decrement, {
                'type': 'state.decrement',
                'params': {
                    'state_key': state_key,
                    'amount': 'e.detail.amount || 1'
                }
            })
    
    def bind_feedback(self,
                     on_toast: str = None,
                     message_expr: str = None,
                     variant: str = 'neutral',
                     duration: int = 3000) -> None:
        """Register feedback (toast) binding
        
        Args:
            on_toast: Event name to trigger toast
            message_expr: Message JS expression (default: 'e.detail.message')
            variant: Toast variant
            duration: Display duration (ms)
        """
        if on_toast:
            self._register_binding(on_toast, {
                'type': 'feedback.toast',
                'params': {
                    'message': message_expr or 'e.detail.message',
                    'variant': f"'{variant}'",
                    'duration': duration
                }
            })
    
    # App-Level Bindings
    
    def bind_event(self,
                   event_name: str,
                   primitives: List[Dict[str, Any]],
                   dedupe: bool = True) -> None:
        """Register app-level event binding (multiple primitives)
        
        Use when one event affects multiple UI elements
        
        Args:
            event_name: Event name
            primitives: List of primitives to execute
            dedupe: Prevent duplicate events (default: True)
        """
        for primitive in primitives:
            # Validate primitive
            valid, msg = validate_primitive(primitive)
            if not valid:
                print(f"[BROADCAST] Warning: Invalid primitive for event '{event_name}': {msg}")
                continue
            
            self._register_binding(event_name, primitive)
        
        # Set metadata
        if dedupe:
            if event_name not in self._bindings:
                self._bindings[event_name] = {'primitives': [], 'meta': {}}
            self._bindings[event_name]['meta']['dedupe'] = True
    
    # ========== Internal: Binding Registry ==========
    
    def _register_binding(self, event_name: str, primitive: Dict):
        """Register binding in registry (internal)"""
        if event_name not in self._bindings:
            self._bindings[event_name] = {
                'primitives': [],
                'meta': {'dedupe': True}  # Default: prevent duplicates
            }
        self._bindings[event_name]['primitives'].append(primitive)
    
    def get_bindings(self) -> Dict:
        """Return currently registered bindings (for debugging)"""
        return self._bindings
    
    # ========== Router & Helpers Injection ==========
    
    def register_js_helpers(self) -> str:
        """
        Register client-side JavaScript helper functions
        
        Provides safe DOM manipulation functions for XSS protection.
        Call once at page startup.
        
        Returns:
            <script> tag containing JavaScript helper functions
        """
        return """
<script>
// ========== Violit JS Helpers (XSS-Safe) ==========

window.violit = window.violit || {};

// HTML escape (XSS protection)
window.violit.escapeHtml = (text) => {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

// Convert newlines to <br> (safe)
window.violit.nl2br = (text) => {
    return window.violit.escapeHtml(text).replace(/\\n/g, '<br>');
};

// Create Live Card (same structure as Python styled_card)
window.violit.createLiveCard = (data) => {
    // Create wrapper div (layout consistency)
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'width: 100%;';
    
    const card = document.createElement('sl-card');
    card.setAttribute('data-post-id', data.id);
    card.style.cssText = 'width: 100%;';
    
    // Header - LIVE badge only (same as Python styled_card)
    const headerWrapper = document.createElement('div');
    headerWrapper.setAttribute('slot', 'header');
    
    const headerInner = document.createElement('div');
    headerInner.style.cssText = 'display: flex; gap: 0.5rem; align-items: center;';
    
    const badge = document.createElement('sl-badge');
    badge.setAttribute('variant', 'danger');
    badge.setAttribute('pulse', '');
    badge.innerHTML = '<sl-icon name="circle-fill" style="font-size: 0.5rem;"></sl-icon> LIVE';
    
    headerInner.appendChild(badge);
    headerWrapper.appendChild(headerInner);
    
    // Body - content (XSS protection: use escapeHtml)
    const body = document.createElement('div');
    body.style.cssText = 'font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;';
    body.textContent = data.content;  // textContent auto-escapes
    
    // Footer - timestamp (same as Python styled_card)
    const footerWrapper = document.createElement('div');
    footerWrapper.setAttribute('slot', 'footer');
    
    const footerInner = document.createElement('div');
    footerInner.style.cssText = 'text-align: right; font-size: 0.85rem; color: var(--sl-color-neutral-600);';
    footerInner.innerHTML = `<sl-icon name="clock"></sl-icon> ${window.violit.escapeHtml(data.created_at)}`;
    
    footerWrapper.appendChild(footerInner);
    
    card.appendChild(headerWrapper);
    card.appendChild(body);
    card.appendChild(footerWrapper);
    
    wrapper.appendChild(card);
    
    return wrapper;  // Return wrapper
};

console.log('✅ Violit helpers loaded (XSS-safe)');
</script>
        """
    
    def inject_all(self) -> None:
        """
        Auto-inject helpers + router into HTML template (convenience method)
        
        This method calls both register_js_helpers() and inject_router()
        to automatically inject into HTML template.
        
        Call once at page startup or in setup function.
        
        Example:
            def setup_bindings():
                # ... binding setup ...
                app.broadcaster.inject_all()  # Auto-inject
        """
        if self._router_injected:
            print("[BROADCAST] Warning: Scripts already injected!")
            return
        
        helpers_script = self.register_js_helpers()
        router_script = self.inject_router()
        
        # Modify HTML_TEMPLATE in violit.app module
        from . import app as vl_app_module
        vl_app_module.HTML_TEMPLATE = vl_app_module.HTML_TEMPLATE.replace(
            '</body>',
            f'{helpers_script}{router_script}</body>'
        )
        
        print("[BROADCAST] [OK] Helpers and Router injected into HTML template")
    
    def inject_router(self) -> str:
        """
        Inject single event router + binding data
        
        This method should be called once at page startup.
        Injects a single router that handles all events and registered bindings.
        
        Returns:
            <script> tag (router + binding data)
        
        Example:
            # Manual injection (advanced users)
            vl.app.HTML_TEMPLATE = vl.app.HTML_TEMPLATE.replace(
                '</body>',
                f'{app.broadcaster.register_js_helpers()}'
                f'{app.broadcaster.inject_router()}'
                f'</body>'
            )
            
            # Auto injection (recommended)
            app.broadcaster.inject_all()
        """
        if self._router_injected:
            print("[BROADCAST] Warning: Router already injected!")
        
        self._router_injected = True
        bindings_json = json.dumps(self._bindings, ensure_ascii=False)
        
        return f"""
<script>
// ========== Violit Event Router (Single Instance) ==========

window.violit = window.violit || {{}};
window.violit.eventCache = window.violit.eventCache || new Map(); // Prevent duplicates
window.violit.bindings = {bindings_json};

// ========== UI Primitives Implementation ==========

window.violit.primitives = {{
    // ===== List Operations =====
    'list.append': (params) => {{
        const container = document.getElementById(`${{params.list_key}}_reactive_list_container`);
        if (!container) {{
            console.warn(`[Violit] List container not found: ${{params.list_key}}`);
            return;
        }}
        
        const data = params.item_data;
        let element;
        
        // Use custom HTML if provided (flexibility)
        if (data.html) {{
            const temp = document.createElement('div');
            temp.innerHTML = data.html;
            element = temp.firstChild;
        }} else {{
            // Create default card (backward compatibility)
            element = window.violit.createLiveCard(data);
        }}
        
        if (params.position === 'prepend') {{
            container.insertBefore(element, container.firstChild);
        }} else {{
            container.appendChild(element);
        }}
        
        // Animation
        element.style.opacity = '0';
        element.style.transform = 'translateY(-20px)';
        setTimeout(() => {{
            element.style.transition = 'all 0.5s ease-out';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }}, 10);
        
        console.log(`[Violit] List append: ${{params.list_key}}`, data.html ? '(custom HTML)' : '(default card)');
    }},
    
    'list.remove': (params) => {{
        const itemId = params.item_id;
        const cards = document.querySelectorAll(`[data-post-id="${{itemId}}"]`);
        
        cards.forEach(card => {{
            card.style.transition = 'all 500ms ease-out';
            card.style.opacity = '0';
            card.style.transform = 'translateX(50px)';
            setTimeout(() => card.remove(), 500);
        }});
        
        console.log(`[Violit] List remove: ${{itemId}}`);
    }},
    
    'list.update': (params) => {{
        const itemId = params.item_id;
        const card = document.querySelector(`[data-post-id="${{itemId}}"]`);
        if (card) {{
            const newCard = window.violit.createLiveCard(params.item_data);
            card.replaceWith(newCard);
            console.log(`[Violit] List update: ${{itemId}}`);
        }}
    }},
    
    'list.replace_all': (params) => {{
        const container = document.getElementById(`${{params.list_key}}_reactive_list_container`);
        if (container) {{
            container.innerHTML = '';
            params.items.forEach(item => {{
                const card = window.violit.createLiveCard(item);
                container.appendChild(card);
            }});
            console.log(`[Violit] List replace all: ${{params.list_key}}`);
        }}
    }},
    
    // ===== State Operations =====
    'state.set': (params) => {{
        const elements = document.querySelectorAll(`[data-state-key="${{params.state_key}}"]`);
        elements.forEach(el => {{
            el.textContent = params.value;
        }});
        console.log(`[Violit] State set: ${{params.state_key}} = ${{params.value}}`);
    }},
    
    'state.increment': (params) => {{
        const elements = document.querySelectorAll(`[data-state-key="${{params.state_key}}"]`);
        elements.forEach(el => {{
            const current = parseInt(el.textContent) || 0;
            el.textContent = current + (params.amount || 1);
        }});
        console.log(`[Violit] State increment: ${{params.state_key}} +${{params.amount || 1}}`);
    }},
    
    'state.decrement': (params) => {{
        const elements = document.querySelectorAll(`[data-state-key="${{params.state_key}}"]`);
        elements.forEach(el => {{
            const current = parseInt(el.textContent) || 0;
            el.textContent = current - (params.amount || 1);
        }});
        console.log(`[Violit] State decrement: ${{params.state_key}} -${{params.amount || 1}}`);
    }},
    
    // ===== DOM Operations =====
    'dom.insert': (params) => {{
        const container = document.getElementById(params.container_id);
        if (container) {{
            const temp = document.createElement('div');
            temp.innerHTML = params.html;
            const element = temp.firstChild;
            
            if (params.position === 'prepend') {{
                container.insertBefore(element, container.firstChild);
            }} else {{
                container.appendChild(element);
            }}
            console.log(`[Violit] DOM insert: ${{params.container_id}}`);
        }}
    }},
    
    'dom.remove': (params) => {{
        const elements = document.querySelectorAll(params.selector);
        elements.forEach(el => {{
            if (params.animate) {{
                el.style.transition = 'opacity 300ms';
                el.style.opacity = '0';
                setTimeout(() => el.remove(), 300);
            }} else {{
                el.remove();
            }}
        }});
        console.log(`[Violit] DOM remove: ${{params.selector}}`);
    }},
    
    'dom.update': (params) => {{
        const elements = document.querySelectorAll(params.selector);
        elements.forEach(el => {{
            el.innerHTML = params.html;
        }});
        console.log(`[Violit] DOM update: ${{params.selector}}`);
    }},
    
    // ===== Feedback Operations =====
    'feedback.toast': (params) => {{
        const alert = document.createElement('sl-alert');
        alert.variant = params.variant || 'neutral';
        alert.closable = true;
        alert.duration = params.duration || 3000;
        
        const iconName = {{
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'danger': 'exclamation-octagon',
            'neutral': 'info-circle'
        }}[params.variant] || 'info-circle';
        
        alert.innerHTML = `<sl-icon slot="icon" name="${{iconName}}"></sl-icon>${{params.message}}`;
        document.body.appendChild(alert);
        alert.toast();
        
        console.log(`[Violit] Toast: ${{params.message}}`);
    }},
    
    'feedback.badge': (params) => {{
        const badge = document.querySelector(`#${{params.badge_id}}`);
        if (badge) {{
            badge.textContent = params.value;
            console.log(`[Violit] Badge update: ${{params.badge_id}} = ${{params.value}}`);
        }}
    }}
}};

// ========== Event Router ==========

window.violit.routeEvent = (eventName, detail) => {{
    const binding = window.violit.bindings[eventName];
    if (!binding) {{
        console.warn(`[Violit] No binding found for event: ${{eventName}}`);
        return;
    }}
    
    // Check duplicates
    if (binding.meta?.dedupe) {{
        const eventId = detail._eventId || JSON.stringify(detail);
        if (window.violit.eventCache.has(eventId)) {{
            console.log(`[Violit] Duplicate event ignored: ${{eventName}}`);
            return;
        }}
        window.violit.eventCache.set(eventId, Date.now());
        
        // Clean cache (keep only recent 100)
        if (window.violit.eventCache.size > 100) {{
            const firstKey = window.violit.eventCache.keys().next().value;
            window.violit.eventCache.delete(firstKey);
        }}
    }}
    
    // Execute primitives
    binding.primitives.forEach(primitive => {{
        try {{
            // Evaluate parameters (execute JS expressions)
            const evaluatedParams = {{}};
            const e = {{ detail }}; // Event object
            
            for (const [key, value] of Object.entries(primitive.params)) {{
                if (typeof value === 'string' && value.includes('e.detail')) {{
                    try {{
                        evaluatedParams[key] = eval(value);
                    }} catch (err) {{
                        console.warn(`[Violit] Failed to evaluate param ${{key}}: ${{value}}`, err);
                        evaluatedParams[key] = value;
                    }}
                }} else {{
                    evaluatedParams[key] = value;
                }}
            }}
            
            // Execute primitive
            const primitiveFunc = window.violit.primitives[primitive.type];
            if (primitiveFunc) {{
                primitiveFunc(evaluatedParams);
            }} else {{
                console.error(`[Violit] Unknown primitive: ${{primitive.type}}`);
            }}
        }} catch (error) {{
            console.error(`[Violit] Error executing primitive ${{primitive.type}}:`, error);
        }}
    }});
    
    console.log(`✅ Event routed: ${{eventName}}`);
}};

// ========== Global Event Listener (Single Instance) ==========

// Prevent duplicate listener registration on page reload
if (!window.violit.listenersRegistered) {{
    // Connect all custom events to router
    Object.keys(window.violit.bindings).forEach(eventName => {{
        window.addEventListener(eventName, (e) => {{
            window.violit.routeEvent(eventName, e.detail);
        }});
    }});
    
    window.violit.listenersRegistered = true;
    console.log('✅ Violit Event Router loaded');
    console.log('📋 Registered events:', Object.keys(window.violit.bindings));
}} else {{
    console.log('⚠️ Violit Event Router already loaded (skipped duplicate registration)');
}}
</script>
        """
    
    # ========== Legacy/Compatibility APIs ==========
    
    def reload_all(self, exclude_current: bool = False):
        """Reload all client pages (Legacy API)"""
        self.eval_all("window.location.reload();", exclude_current=exclude_current)


# Convenience function
def create_broadcaster(app) -> Broadcaster:
    """
    Create Broadcaster instance
    
    Args:
        app: Violit App instance
        
    Returns:
        Broadcaster instance
    """
    return Broadcaster(app)
