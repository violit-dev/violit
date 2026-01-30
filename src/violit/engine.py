from typing import List, Dict, Callable
from starlette.websockets import WebSocket
from .component import Component

class LiteEngine:
    def click_attrs(self, cid: str):
        return {"hx-post": f"/action/{cid}", "hx-swap": "none"}

    def wrap_oob(self, components: List[Component]):
        html = ""
        for comp in components:
            rendered = comp.render().strip()
            # Inject hx-swap-oob="true" into the root tag of the component
            tag_end = rendered.find(' ')
            if tag_end == -1: tag_end = rendered.find('>')
            html += rendered[:tag_end] + ' hx-swap-oob="true"' + rendered[tag_end:]
        return html

class WsEngine:
    def __init__(self):
        self.sockets: Dict[str, WebSocket] = {}
        
    def click_attrs(self, cid: str):
        return {"onclick": f"window.sendAction('{cid}')"}
        
    async def push_updates(self, sid: str, components: List[Component], is_navigation: bool = False):
        """Push component updates to client
        
        Args:
            sid: Session ID
            components: List of components to update
            is_navigation: If True, apply smooth page transition animation.
                          If False (default), update immediately without animation.
        """
        if sid in self.sockets:
            payload = [{"id": c.id, "html": c.render()} for c in components]
            await self.sockets[sid].send_json({
                "type": "update", 
                "payload": payload,
                "isNavigation": is_navigation  # Flag for client to determine animation
            })

    async def push_eval(self, sid: str, code: str):
        if sid in self.sockets:
            await self.sockets[sid].send_json({"type": "eval", "code": code})

