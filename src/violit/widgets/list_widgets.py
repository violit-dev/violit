"""List widgets for reactive list management"""

from typing import Callable, Any, List as ListType
from ..component import Component
from ..context import rendering_ctx
from ..state import State


class ListWidgetsMixin:
    
    def reactive_list(self, 
                     items: ListType[Any] = None,
                     render_item: Callable[[Any], str] = None,
                     key: str = None,
                     container_id: str = None,
                     empty_message: str = None,
                     reverse: bool = False,
                     item_gap: str = "1rem"):
        """Create a reactive list that updates when items change"""
        cid = self._get_next_cid("reactive_list")
        container_id = container_id or f"{cid}-container"
        
        state_key = key or f"list:{cid}"
        if isinstance(items, State):
            list_state = items
        else:
            list_state = self.state(items or [], key=state_key)
        
        def builder():
            token = rendering_ctx.set(cid)
            current_items = list_state.value
            rendering_ctx.reset(token)
            
            if not current_items:
                if empty_message:
                    content = f'<div style="text-align: center; padding: 2rem; color: var(--sl-text-muted);">{empty_message}</div>'
                else:
                    content = ''
            else:
                items_to_render = list(reversed(current_items)) if reverse else current_items
                
                if render_item:
                    rendered_items = []
                    for item in items_to_render:
                        item_html = render_item(item)
                        rendered_items.append(item_html)
                    content = ''.join(rendered_items)
                else:
                    content = ''.join([f'<div style="padding: 0.5rem;">{item}</div>' for item in items_to_render])
            
            html = f'''
            <div id="{container_id}" style="display: flex; flex-direction: column; gap: {item_gap}; width: 100%;">
                {content}
            </div>
            '''
            
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
        
        return list_state
    
    def card_list(self,
                 items: ListType[dict] = None,
                 key: str = None,
                 container_id: str = None,
                 empty_message: str = "No items yet",
                 card_type: str = "live",
                 reverse: bool = True):
        """Reactive list for card items"""
        def render_card(item):
            if card_type == 'live':
                return self.live_card_html(
                    item.get('content', ''),
                    item.get('created_at'),
                    item.get('id')
                )
            elif card_type == 'admin':
                card_html = f'<div data-post-id="{item.get("id")}">'
                card_html += self.live_card_html(
                    item.get('content', ''),
                    item.get('created_at'),
                    item.get('id')
                )
                card_html += '</div>'
                return card_html
            else:
                return self.live_card_html(
                    item.get('content', ''),
                    item.get('created_at'),
                    item.get('id')
                )
        
        return self.reactive_list(
            items=items,
            render_item=render_card,
            key=key,
            container_id=container_id,
            empty_message=empty_message,
            reverse=reverse
        )






