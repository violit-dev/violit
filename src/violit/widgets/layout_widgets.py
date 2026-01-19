"""Layout Widgets Mixin for Violit"""

from typing import Union, Callable, Optional, List
from ..component import Component
from ..context import rendering_ctx, fragment_ctx, layout_ctx


class LayoutWidgetsMixin:
    """Layout widgets (columns, container, expander, tabs, empty, dialog)"""
    
    def columns(self, spec=2, gap="1rem"):
        """Create column layout - spec can be an int (equal width) or list of weights"""
        if isinstance(spec, int):
            count = spec
            weights = ["1fr"] * count
        else:
            count = len(spec)
            weights = [f"{w}fr" for w in spec]
            
        columns_id = self._get_next_cid("columns_container")
        
        # Create individual column objects
        column_objects = []
        for i in range(count):
            col = ColumnObject(self, columns_id, i, count, gap)
            column_objects.append(col)
        
        # Register the columns container builder
        def builder():
            from ..state import get_session_store
            store = get_session_store()
            
            # Collect HTML from all columns
            columns_html = []
            for i in range(count):
                col_id = f"{columns_id}_col_{i}"
                col_content = []
                # Check static
                for cid, b in self.static_fragment_components.get(col_id, []):
                    col_content.append(b().render())
                # Check session
                for cid, b in store['fragment_components'].get(col_id, []):
                    col_content.append(b().render())
                columns_html.append(f'<div class="column-item">{"".join(col_content)}</div>')
            
            grid_tmpl = " ".join(weights)
            container_html = f'<div id="{columns_id}" class="columns" style="display: grid; grid-template-columns: {grid_tmpl}; gap: {gap};">{"".join(columns_html)}</div>'
            return Component("div", id=f"{columns_id}_wrapper", content=container_html)
        
        self._register_component(columns_id, builder)
        
        return column_objects

    def container(self, border=True, **kwargs):
        """
        Create a container for grouping elements
        
        Args:
            border: Whether to show border (card style)
            **kwargs: Additional HTML attributes (e.g., data_post_id="123", style="...")
        
        Example:
            with app.container(data_post_id="123"):
                app.text("Content")
                app.button("Delete")
        """
        cid = self._get_next_cid("container")
        
        class ContainerContext:
            def __init__(self, app, container_id, border, attrs):
                self.app = app
                self.container_id = container_id
                self.border = border
                self.attrs = attrs
                
            def __enter__(self):
                # Register builder BEFORE entering context
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    # Render child components
                    htmls = []
                    # Static first
                    for cid, b in self.app.static_fragment_components.get(self.container_id, []):
                        htmls.append(b().render())
                    # Dynamic next
                    for cid, b in store['fragment_components'].get(self.container_id, []):
                        htmls.append(b().render())
                    
                    border_class = "card" if self.border else ""
                    inner_html = "".join(htmls)
                    
                    # Pass kwargs to Component
                    return Component("div", id=self.container_id, content=inner_html, class_=border_class, **self.attrs)
                
                self.app._register_component(self.container_id, builder)
                
                # Now set fragment context
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ContainerContext(self, cid, border, kwargs)

    def expander(self, label, expanded=False):
        """Create an expandable/collapsible section"""
        cid = self._get_next_cid("expander")
        
        class ExpanderContext:
            def __init__(self, app, expander_id, label, expanded):
                self.app = app
                self.expander_id = expander_id
                self.label = label
                self.expanded = expanded
                
            def __enter__(self):
                # Register builder BEFORE entering context
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    # Render child components
                    htmls = []
                    # Static
                    for cid, b in self.app.static_fragment_components.get(self.expander_id, []):
                        htmls.append(b().render())
                    # Dynamic
                    for cid, b in store['fragment_components'].get(self.expander_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    open_attr = "open" if self.expanded else ""
                    html = f'''
                    <sl-details {open_attr} style="margin-bottom:1rem;">
                        <span slot="summary" style="font-weight:500;">{self.label}</span>
                        <div style="padding:0.5rem 0;">{inner_html}</div>
                    </sl-details>
                    '''
                    return Component("div", id=self.expander_id, content=html)
                
                self.app._register_component(self.expander_id, builder)
                
                # Now set fragment context for children
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.expander_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ExpanderContext(self, cid, label, expanded)

    def tabs(self, labels: List[str]):
        """Create tabbed interface"""
        cid = self._get_next_cid("tabs")
        
        class TabsManager:
            def __init__(self, app, tabs_id, labels):
                self.app = app
                self.tabs_id = tabs_id
                self.labels = labels
                self.tab_objects = []
                
                # Create tab objects immediately
                for i, label in enumerate(self.labels):
                    tab_obj = TabObject(self.app, f"{self.tabs_id}_tab_{i}", label, i == 0)
                    self.tab_objects.append(tab_obj)
                
                # Register tabs builder immediately
                self._register_builder()

            def _register_builder(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    # Build tab headers
                    headers = []
                    for i, label in enumerate(self.labels):
                        active = "active" if i == 0 else ""
                        headers.append(f'<sl-tab slot="nav" panel="panel-{i}" {active}>{label}</sl-tab>')
                    
                    # Build tab panels
                    panels = []
                    for i, tab_obj in enumerate(self.tab_objects):
                        active = "active" if i == 0 else ""
                        # Render tab content
                        tab_htmls = []
                        # Check static
                        for cid, b in self.app.static_fragment_components.get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        # Check session
                        for cid, b in store['fragment_components'].get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        
                        panel_content = "".join(tab_htmls)
                        panels.append(f'<sl-tab-panel name="panel-{i}" {active}>{panel_content}</sl-tab-panel>')
                    
                    html = f'''
                    <sl-tab-group>
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
            
            # Make it iterable and indexable
            def __iter__(self):
                return iter(self.tab_objects)
            
            def __getitem__(self, index):
                return self.tab_objects[index]
            
            def __len__(self):
                return len(self.tab_objects)
        
        return TabsManager(self, cid, labels)

    def empty(self):
        """Create an empty container that can be updated later"""
        cid = self._get_next_cid("empty")
        
        class EmptyContainer:
            def __init__(self, app, container_id):
                self.app = app
                self.container_id = container_id
                self._content_builder = None
                
                # Register initial empty builder
                def builder():
                    if self._content_builder:
                        return self._content_builder()
                    return Component("div", id=container_id, content="")
                
                app._register_component(container_id, builder)
            
            def write(self, content):
                """Update the empty container with new content"""
                def new_builder():
                    return Component("div", id=self.container_id, content=str(content))
                self._content_builder = new_builder
            
            def __getattr__(self, name):
                # Proxy to app for method calls
                return getattr(self.app, name)
        
        return EmptyContainer(self, cid)

    def dialog(self, title):
        """Create a modal dialog (decorator)"""
        def decorator(func):
            dialog_id = f"dialog_{func.__name__}"
            
            # Create a function to open the dialog
            def open_dialog(*args, **kwargs):
                # Set fragment context for dialog content
                token = fragment_ctx.set(dialog_id)
                
                # Execute the dialog content function
                func(*args, **kwargs)
                
                # Build dialog HTML
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    # Render dialog content
                    htmls = []
                    for child_cid, child_builder in store['fragment_components'].get(dialog_id, []):
                        htmls.append(child_builder().render())
                    
                    inner_html = "".join(htmls)
                    html = f'''
                    <sl-dialog id="{dialog_id}_modal" label="{title}" open>
                        <div style="padding:1rem;">{inner_html}</div>
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
    
    def list_container(self, id: Optional[str] = None, gap: str = None, **style_props):
        """Create a vertical flex container for lists
        
        General list layout container using predefined styles.
        
        Args:
            id: Container ID (for broadcast removal)
            gap: Item spacing (CSS value, default: predefined 1rem)
            **style_props: Additional style properties (if needed)
        
        Example:
            with app.list_container(id="posts_container"):
                for post in posts:
                    app.styled_card(...)
        """
        cid = id or self._get_next_cid("list_container")
        
        class ListContainerContext:
            def __init__(self, app, container_id, gap, style_props):
                self.app = app
                self.container_id = container_id
                self.gap = gap
                self.style_props = style_props
                
            def __enter__(self):
                # Register builder
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    # Render child components
                    htmls = []
                    # Static
                    for cid, b in self.app.static_fragment_components.get(self.container_id, []):
                        htmls.append(b().render())
                    # Dynamic
                    for cid, b in store['fragment_components'].get(self.container_id, []):
                        htmls.append(b().render())
                    
                    # Use predefined class + optional customizations
                    extra_styles = []
                    if self.gap:
                        extra_styles.append(f"gap: {self.gap}")
                    for k, v in self.style_props.items():
                        extra_styles.append(f"{k.replace('_', '-')}: {v}")
                    
                    style_str = "; ".join(extra_styles) if extra_styles else None
                    
                    inner_html = "".join(htmls)
                    if style_str:
                        return Component("div", id=self.container_id, content=inner_html, class_="violit-list-container", style=style_str)
                    else:
                        return Component("div", id=self.container_id, content=inner_html, class_="violit-list-container")
                
                self.app._register_component(self.container_id, builder)
                
                # Set fragment context
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ListContainerContext(self, cid, gap, style_props)


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
        # We don't set rendering_ctx here because individual widgets inside will set their own
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import fragment_ctx
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        """Proxy to app for method calls within column context"""
        return getattr(self.app, name)


class TabObject:
    """Represents a single tab in a tab group"""
    def __init__(self, app, tab_id, label, active):
        self.app = app
        self.tab_id = tab_id
        self.label = label
        self.active = active
        
    def __enter__(self):
        self.token = fragment_ctx.set(self.tab_id)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        return getattr(self.app, name)

