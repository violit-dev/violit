from typing import Iterable, List, Dict, Callable, Optional, Tuple
from starlette.websockets import WebSocket
from .component import Component
from .context import view_ctx

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
        self.sockets: Dict[Tuple[str, str], WebSocket] = {}

    def _resolve_view_id(self, view_id: Optional[str] = None) -> Optional[str]:
        return view_id or view_ctx.get()

    def _make_key(self, sid: str, view_id: Optional[str] = None) -> Optional[Tuple[str, str]]:
        resolved_view_id = self._resolve_view_id(view_id)
        if not sid or not resolved_view_id:
            return
        return (sid, resolved_view_id)

    def register_socket(self, sid: str, view_id: str, ws: WebSocket):
        key = self._make_key(sid, view_id)
        if key is None:
            return
        self.sockets[key] = ws

    def unregister_socket(self, sid: str, view_id: str, ws: Optional[WebSocket] = None):
        key = self._make_key(sid, view_id)
        if key is None:
            return
        current = self.sockets.get(key)
        if current is None:
            return
        if ws is not None and current is not ws:
            return
        self.sockets.pop(key, None)

    def get_socket(self, sid: str, view_id: Optional[str] = None) -> Optional[WebSocket]:
        key = self._make_key(sid, view_id)
        if key is None:
            return None
        return self.sockets.get(key)

    def has_socket(self, sid: str, view_id: Optional[str] = None) -> bool:
        return self.get_socket(sid, view_id) is not None

    def socket_count(self, sid: Optional[str] = None) -> int:
        if sid is None:
            return len(self.sockets)
        return sum(1 for current_sid, _ in self.sockets.keys() if current_sid == sid)

    def iter_sockets(self) -> Iterable[tuple[str, str, WebSocket]]:
        for (sid, current_view_id), socket in list(self.sockets.items()):
            yield sid, current_view_id, socket

    async def _send_json_to_view(self, sid: str, payload: dict, view_id: Optional[str] = None):
        socket = self.get_socket(sid, view_id)
        key = self._make_key(sid, view_id)
        if socket is None or key is None:
            return
        try:
            await socket.send_json(payload)
        except Exception:
            self.sockets.pop(key, None)
        
    def click_attrs(self, cid: str):
        return {"onclick": f"window.sendAction('{cid}')"}
        
    async def push_updates(self, sid: str, components: List[Component], is_navigation: bool = False, view_id: Optional[str] = None):
        """Push component updates to client
        
        Args:
            sid: Session ID
            components: List of components to update
            is_navigation: If True, apply smooth page transition animation.
                          If False (default), update immediately without animation.
        """
        payload = [{"id": c.id, "html": c.render()} for c in components]
        await self._send_json_to_view(
            sid,
            {
                "type": "update",
                "payload": payload,
                "isNavigation": is_navigation,
            },
            view_id=view_id,
        )

    async def push_eval(self, sid: str, code: str, view_id: Optional[str] = None):
        await self._send_json_to_view(sid, {"type": "eval", "code": code}, view_id=view_id)

