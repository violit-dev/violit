import contextvars

# Global Contexts
session_ctx = contextvars.ContextVar("session_id", default=None)
rendering_ctx = contextvars.ContextVar("rendering_component", default=None)
fragment_ctx = contextvars.ContextVar("current_fragment", default=None)
page_ctx = contextvars.ContextVar("current_page_renderer", default=None)
layout_ctx = contextvars.ContextVar("layout_ctx", default="main")  # "main" or "sidebar"
initial_render_ctx = contextvars.ContextVar("initial_render", default=False)

# Global Reference for App Instance (used for initial theme sync)
app_instance_ref = [None]
