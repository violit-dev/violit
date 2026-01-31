"""Layout Widgets Mixin for Violit"""

from typing import Union, Callable, Optional, List
from ..component import Component
from ..context import rendering_ctx, fragment_ctx, layout_ctx
from ..style_utils import build_cls


class LayoutWidgetsMixin:
    """Layout widgets (columns, container, expander, tabs, empty, dialog)"""
    
    def columns(self, spec=2, gap="1rem", align="left", cls: str = "", **kwargs):
        """Create column layout
        
        Args:
            spec: Number of columns or list of weights
            gap: Gap between columns
            align: Alignment within each column ("left", "center", "right")
            cls: Additional CSS classes
            **kwargs: Additional Master CSS props
        """
        if isinstance(spec, int):
            count = spec
            weights = ["1fr"] * count
        else:
            count = len(spec)
            weights = [f"{w}fr" for w in spec]
            
        columns_id = self._get_next_cid("columns_container")
        
        column_objects = []
        for i in range(count):
            col = ColumnObject(self, columns_id, i, count, gap)
            column_objects.append(col)
        
        def builder():
            from ..state import get_session_store
            store = get_session_store()
            
            # Determine alignment class for column items
            align_map = {
                "left": "",
                "center": "text:center",
                "right": "text:right"
            }
            align_cls = align_map.get(align, "")
            
            columns_html = []
            for i in range(count):
                col_id = f"{columns_id}_col_{i}"
                col_content = []
                for cid, b in self.static_fragment_components.get(col_id, []):
                    col_content.append(b().render())
                for cid, b in store['fragment_components'].get(col_id, []):
                    col_content.append(b().render())
                columns_html.append(f'<div class="column-item h:full {align_cls}">{"".join(col_content)}</div>')
            
            grid_tmpl = " ".join(weights)
            # Use Master CSS for grid layout where possible, but template needs style
            # Changed ai:stretch to ai:start for Streamlit-like behavior (no forced stretching)
            base_cls = "grid ai:start"
            final_cls = build_cls(f"{base_cls} {cls}", gap=gap, **kwargs)
            
            container_html = f'<div id="{columns_id}" class="{final_cls}" style="grid-template-columns: {grid_tmpl};">{"".join(columns_html)}</div>'
            return Component("div", id=f"{columns_id}_wrapper", content=container_html)
        
        self._register_component(columns_id, builder)
        
        return column_objects

    def container(self, border=True, cls: str = "", **kwargs):
        """Create a container for grouping elements"""
        cid = self._get_next_cid("container")
        
        # Extract semantic props from kwargs
        semantic_props = {}
        html_attrs = {}
        for k, v in kwargs.items():
            if k.startswith('data_') or k.startswith('aria_') or k == 'id':
                html_attrs[k] = v
            else:
                semantic_props[k] = v
        
        class ContainerContext:
            def __init__(self, app, container_id, border, cls, semantic_props, html_attrs):
                self.app = app
                self.container_id = container_id
                self.border = border
                self.cls = cls
                self.semantic_props = semantic_props
                self.html_attrs = html_attrs
                
            def __enter__(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    htmls = []
                    for cid, b in self.app.static_fragment_components.get(self.container_id, []):
                        htmls.append(b().render())
                    for cid, b in store['fragment_components'].get(self.container_id, []):
                        htmls.append(b().render())
                    
                    base_cls = "card" if self.border else ""
                    final_cls = build_cls(f"{base_cls} {self.cls}", **self.semantic_props)
                    
                    inner_html = "".join(htmls)
                    
                    return Component("div", id=self.container_id, content=inner_html, class_=final_cls, **self.html_attrs)
                
                self.app._register_component(self.container_id, builder)
                
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ContainerContext(self, cid, border, cls, semantic_props, html_attrs)

    def expander(self, label, expanded=False, cls: str = "", **kwargs):
        """Create an expandable/collapsible section"""
        cid = self._get_next_cid("expander")
        
        class ExpanderContext:
            def __init__(self, app, expander_id, label, expanded, cls, kwargs):
                self.app = app
                self.expander_id = expander_id
                self.label = label
                self.expanded = expanded
                self.cls = cls
                self.kwargs = kwargs
                
            def __enter__(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    htmls = []
                    for cid, b in self.app.static_fragment_components.get(self.expander_id, []):
                        htmls.append(b().render())
                    for cid, b in store['fragment_components'].get(self.expander_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    open_attr = "open" if self.expanded else ""
                    
                    final_cls = build_cls(self.cls, **self.kwargs)
                    
                    html = f'''
                    <sl-details {open_attr} class="mb:1rem {final_cls}">
                        <span slot="summary" class="font-weight:500">{self.label}</span>
                        <div class="py:0.5rem">{inner_html}</div>
                    </sl-details>
                    '''
                    return Component("div", id=self.expander_id, content=html)
                
                self.app._register_component(self.expander_id, builder)
                
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.expander_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ExpanderContext(self, cid, label, expanded, cls, kwargs)

    def tabs(self, labels: List[str], cls: str = "", **kwargs):
        """Create tabbed interface"""
        cid = self._get_next_cid("tabs")
        
        class TabsManager:
            def __init__(self, app, tabs_id, labels, cls, kwargs):
                self.app = app
                self.tabs_id = tabs_id
                self.labels = labels
                self.cls = cls
                self.kwargs = kwargs
                self.tab_objects = []
                
                for i, label in enumerate(self.labels):
                    tab_obj = TabObject(self.app, f"{self.tabs_id}_tab_{i}", label, i == 0)
                    self.tab_objects.append(tab_obj)
                
                self._register_builder()

            def _register_builder(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    headers = []
                    for i, label in enumerate(self.labels):
                        active = "active" if i == 0 else ""
                        headers.append(f'<sl-tab slot="nav" panel="panel-{i}" {active}>{label}</sl-tab>')
                    
                    panels = []
                    for i, tab_obj in enumerate(self.tab_objects):
                        active = "active" if i == 0 else ""
                        tab_htmls = []
                        for cid, b in self.app.static_fragment_components.get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        for cid, b in store['fragment_components'].get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        
                        panel_content = "".join(tab_htmls)
                        panels.append(f'<sl-tab-panel name="panel-{i}" {active}>{panel_content}</sl-tab-panel>')
                    
                    final_cls = build_cls(self.cls, **self.kwargs)
                    
                    html = f'''
                    <sl-tab-group class="{final_cls}">
                        {"".join(headers)}
                        {"".join(panels)}
                    </sl-tab-group>
                    '''
                    return Component("div", id=self.tabs_id, content=html)
                
                self.app._register_component(self.tabs_id, builder)

            def __enter__(self):
                return self.tab_objects
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
            
            def __iter__(self):
                return iter(self.tab_objects)
            
            def __getitem__(self, index):
                return self.tab_objects[index]
            
            def __len__(self):
                return len(self.tab_objects)
        
        return TabsManager(self, cid, labels, cls, kwargs)

    def empty(self):
        """Create an empty container that can be updated later"""
        cid = self._get_next_cid("empty")
        
        class EmptyContainer:
            def __init__(self, app, container_id):
                self.app = app
                self.container_id = container_id
                self._content_builder = None
                
                def builder():
                    if self._content_builder:
                        return self._content_builder()
                    return Component("div", id=container_id, content="")
                
                app._register_component(container_id, builder)
            
            def write(self, content):
                def new_builder():
                    return Component("div", id=self.container_id, content=str(content))
                self._content_builder = new_builder
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return EmptyContainer(self, cid)

    def dialog(self, title):
        """Create a modal dialog (decorator)"""
        def decorator(func):
            dialog_id = f"dialog_{func.__name__}"
            
            def open_dialog(*args, **kwargs):
                token = fragment_ctx.set(dialog_id)
                func(*args, **kwargs)
                
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    htmls = []
                    for child_cid, child_builder in store['fragment_components'].get(dialog_id, []):
                        htmls.append(child_builder().render())
                    
                    inner_html = "".join(htmls)
                    html = f'''
                    <sl-dialog id="{dialog_id}_modal" label="{title}" open>
                        <div class="p:1rem">{inner_html}</div>
                        <sl-button slot="footer" variant="primary" onclick="document.getElementById('{dialog_id}_modal').hide()">Close</sl-button>
                    </sl-dialog>
                    <script>
                        document.getElementById('{dialog_id}_modal').show();
                    </script>
                    '''
                    return Component("div", id=dialog_id, content=html)
                
                fragment_ctx.reset(token)
                self._register_component(dialog_id, builder)
            
            return open_dialog
        return decorator
    
    def list_container(self, id: Optional[str] = None, gap: str = None, cls: str = "", **kwargs):
        """Create a vertical flex container for lists"""
        cid = id or self._get_next_cid("list_container")
        
        class ListContainerContext:
            def __init__(self, app, container_id, gap, cls, kwargs):
                self.app = app
                self.container_id = container_id
                self.gap = gap
                self.cls = cls
                self.kwargs = kwargs
                
            def __enter__(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    htmls = []
                    for cid, b in self.app.static_fragment_components.get(self.container_id, []):
                        htmls.append(b().render())
                    for cid, b in store['fragment_components'].get(self.container_id, []):
                        htmls.append(b().render())
                    
                    # Use Master CSS for list layout
                    base_cls = "flex flex:col w:full"
                    final_cls = build_cls(f"{base_cls} {self.cls}", gap=self.gap, **self.kwargs)
                    
                    inner_html = "".join(htmls)
                    return Component("div", id=self.container_id, content=inner_html, class_=final_cls)
                
                self.app._register_component(self.container_id, builder)
                
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ListContainerContext(self, cid, gap, cls, kwargs)


class ColumnObject:
    """Represents a single column in a column layout"""
    def __init__(self, app, columns_id, col_index, total_cols, gap):
        self.app = app
        self.columns_id = columns_id
        self.col_index = col_index
        self.col_id = f"{columns_id}_col_{col_index}"
        
    def __enter__(self):
        from ..context import fragment_ctx, rendering_ctx
        self.token = fragment_ctx.set(self.col_id)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import fragment_ctx
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        return getattr(self.app, name)


class TabObject:
    """Represents a single tab in a tab group"""
    def __init__(self, app, tab_id, label, active):
        self.app = app
        self.tab_id = tab_id
        self.label = label
        self.active = active
        
    def __enter__(self):
        from ..context import fragment_ctx
        self.token = fragment_ctx.set(self.tab_id)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import fragment_ctx
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        return getattr(self.app, name)
