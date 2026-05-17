"""Layout Widgets Mixin for Violit"""

import hashlib
import re

from functools import wraps

from typing import Any, Union, Callable, Optional, List, Sequence
from ..component import Component
from ..context import rendering_ctx, fragment_ctx, layout_ctx, registration_pass_ctx, session_ctx
from ..style_utils import merge_cls, merge_style


def _reset_dynamic_fragment_children(fragment_id: str):
    """Clear runtime-only fragment children before a nested layout re-renders.

    Reactive sub-renders recreate the child widgets for containers, tabs, columns,
    and similar layout scopes. Without clearing the previous dynamic child list,
    the same builders are appended repeatedly and the DOM appears duplicated.
    """
    if session_ctx.get() is None:
        return

    from ..state import get_session_store

    store = get_session_store()
    store['fragment_components'][fragment_id] = []


def _sanitize_layout_key(value: Any) -> str:
    raw = str(value)
    normalized = re.sub(r"[^a-zA-Z0-9_-]", "_", raw)
    normalized = re.sub(r"_+", "_", normalized).strip("_")

    if normalized and normalized == raw and len(normalized) <= 64:
        return normalized

    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
    if not normalized:
        return f"layout_{digest}"
    return f"{normalized[:48]}_{digest}"


def _resolve_dynamic_layout_value(value: Any) -> Any:
    from ..state import State, ComputedState

    if isinstance(value, (State, ComputedState)):
        return value.value
    if callable(value):
        return value()
    return value


def _resolve_columns_gap(gap: Any) -> str:
    gap_tokens = {
        None: "0",
        "xxsmall": "0.25rem",
        "xsmall": "0.5rem",
        "small": "1rem",
        "medium": "2rem",
        "large": "4rem",
        "xlarge": "6rem",
        "xxlarge": "8rem",
    }
    return gap_tokens.get(gap, str(gap))


def _resolve_group_width(width: Any) -> str:
    if width in (None, "", "stretch"):
        return ""
    if isinstance(width, (int, float)):
        return f"width: min(100%, {int(width)}px);"
    return f"width: min(100%, {width});"


def _resolve_flex_alignment(value: Optional[str], axis: str) -> str:
    if value is None:
        return ""

    maps = {
        "align": {
            "left": "flex-start",
            "start": "flex-start",
            "center": "center",
            "right": "flex-end",
            "end": "flex-end",
            "stretch": "stretch",
        },
        "justify": {
            "top": "flex-start",
            "start": "flex-start",
            "center": "center",
            "bottom": "flex-end",
            "end": "flex-end",
            "between": "space-between",
            "around": "space-around",
            "evenly": "space-evenly",
        },
    }
    return maps.get(axis, {}).get(value, value)


def _should_mark_placeholder_dirty() -> bool:
    return session_ctx.get() is not None and registration_pass_ctx.get() is None


class LayoutWidgetsMixin:
    """Layout widgets (columns, container, expander, tabs, empty, dialog)"""
    
    def columns(self, spec: Union[int, Sequence[Union[int, float]]] = 2, gap="small", vertical_alignment="top", cls: str = "", style: str = "",
                border: bool = False, width: Union[str, int] = "stretch", equal_height: bool = False,
                align: Optional[str] = None, justify: Optional[str] = None):
        """Create column layout - spec can be an int (equal width) or list of weights
        
        Args:
            spec: Number of equal-width columns (int) or list of weight ratios (e.g. [1, 2, 1])
            gap: Gap between columns (token like "small" or a CSS value)
            vertical_alignment: Vertical alignment of column contents - "top", "center", or "bottom"
            cls: Additional CSS classes
            style: Additional inline styles
            border: Whether to add a border/card surface to each column
            width: Width of the column group - "stretch" or a fixed width
            equal_height: Whether sibling columns should stretch to a matching height
            align: Cross-axis alignment for children inside each column
            justify: Main-axis alignment for children inside each column
        """
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
            _reset_dynamic_fragment_children(col.col_id)
            column_objects.append(col)
        
        # Register the columns container builder
        def builder():
            from ..state import get_session_store
            store = get_session_store()

            current_gap = _resolve_dynamic_layout_value(gap)
            current_vertical_alignment = _resolve_dynamic_layout_value(vertical_alignment)
            current_border = bool(_resolve_dynamic_layout_value(border))
            current_width = _resolve_dynamic_layout_value(width)
            current_equal_height = bool(_resolve_dynamic_layout_value(equal_height))
            current_align = _resolve_dynamic_layout_value(align)
            current_justify = _resolve_dynamic_layout_value(justify)

            resolved_gap = _resolve_columns_gap(current_gap)
            width_style = _resolve_group_width(current_width)
            column_align = _resolve_flex_alignment(current_align, "align")
            column_justify = _resolve_flex_alignment(current_justify, "justify")
            
            grid_tmpl = " ".join(weights)
            # Use CSS variable for grid-template-columns so it can be overridden by CSS
            # The --vl-cols variable and gap are set inline, but display:grid is handled by CSS class
            _va_map = {"top": "start", "center": "center", "bottom": "end"}
            _va = _va_map.get(current_vertical_alignment, "start")
            grid_align = "stretch" if (current_equal_height or column_align or column_justify) else _va
            container_cls = merge_cls(
                "columns",
                "columns--bordered" if current_border else "",
                "columns--equal-height" if current_equal_height else "",
            )
            column_item_cls = merge_cls(
                "column-item",
                "column-item--bordered" if current_border else "",
            )
            columns_html = []
            for i in range(count):
                col_id = f"{columns_id}_col_{i}"
                col_content = []
                for cid, b in self.static_fragment_components.get(col_id, []):
                    col_content.append(b().render())
                for cid, b in store['fragment_components'].get(col_id, []):
                    col_content.append(b().render())
                columns_html.append(
                    f'<div class="{column_item_cls}">'
                    f'{"".join(col_content)}</div>'
                )
            joined_cols = "".join(columns_html)
            container_style = f"--vl-cols: {grid_tmpl}; --vl-gap: {resolved_gap}; align-items: {grid_align};"
            if column_align:
                container_style += f" --vl-column-align: {column_align};"
            if column_justify:
                container_style += f" --vl-column-justify: {column_justify};"
            if column_align or column_justify:
                container_style += " --vl-column-single-child-height: auto;"
            if width_style:
                container_style = f"{container_style} {width_style}"
            container_html = f'<div id="{columns_id}" class="{container_cls}" style="{container_style}">{joined_cols}</div>'
            _wd = self._get_widget_defaults("columns")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{columns_id}_wrapper", content=container_html, class_=_fc or None, style=_fs or None)
        
        self._register_component(columns_id, builder)
        
        return column_objects

    def container(self, border=False, height=None, cls: str = "", style: str = "",
                  fill_height: bool = False, align: Optional[str] = None,
                  justify: Optional[str] = None, spacing: Any = None,
                  widget_gap: Any = None, **kwargs):
        """
        Create a container for grouping elements
        
        Args:
            border: Whether to show border (card style)
            height: Container height (int for pixels, str for CSS value). Adds scrollbar when content overflows.
            fill_height: Whether the container should stretch to fill its parent height.
            align: Cross-axis alignment for children when using flex layout.
            justify: Main-axis alignment for children when using flex layout.
            spacing: Optional local spacing preset override for this container subtree.
            widget_gap: Optional explicit local widget gap override for this container subtree.
            **kwargs: Additional HTML attributes (e.g., data_post_id="123", style="...")
        
        Example:
            with app.container(data_post_id="123"):
                app.text("Content")
                app.button("Delete")
        """
        cid = self._get_next_cid("container")
        
        class ContainerContext:
            def __init__(self, app, container_id, border, height, user_cls, user_style,
                         fill_height, align, justify, spacing, widget_gap, attrs):
                self.app = app
                self.container_id = container_id
                self.border = border
                self.height = height
                self.user_cls = user_cls
                self.user_style = user_style
                self.fill_height = fill_height
                self.align = align
                self.justify = justify
                self.spacing = spacing
                self.widget_gap = widget_gap
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
                    
                    # Height support (scrollable container)
                    layout_styles = []
                    if self.height is not None:
                        h = f"{self.height}px" if isinstance(self.height, (int, float)) else self.height
                        layout_styles.append(f"height: {h}; overflow-y: auto;")

                    if self.fill_height:
                        layout_styles.append("height: 100%;")

                    align_value = _resolve_flex_alignment(self.align, "align")
                    justify_value = _resolve_flex_alignment(self.justify, "justify")
                    if self.fill_height or align_value or justify_value:
                        layout_styles.append("display: flex; flex-direction: column;")
                    if align_value:
                        layout_styles.append(f"align-items: {align_value};")
                    if justify_value:
                        layout_styles.append(f"justify-content: {justify_value};")

                    current_spacing = _resolve_dynamic_layout_value(self.spacing)
                    current_widget_gap = _resolve_dynamic_layout_value(self.widget_gap)
                    _, runtime_profile, runtime_widget_gap = self.app._get_spacing_runtime_values()
                    effective_profile = runtime_profile
                    effective_widget_gap = runtime_widget_gap
                    if current_spacing is not None:
                        _, effective_profile, effective_widget_gap = self.app._resolve_spacing_values(current_spacing, None)
                    normalized_local_widget_gap = self.app._normalize_spacing_widget_gap(current_widget_gap)
                    if normalized_local_widget_gap is not None:
                        effective_widget_gap = normalized_local_widget_gap
                    layout_styles.append(self.app._build_spacing_css_vars(effective_profile, effective_widget_gap))
                    
                    _wd = self.app._get_widget_defaults("container")
                    _fc = merge_cls(_wd.get("cls", ""), "fragment", border_class, self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), " ".join(layout_styles), self.user_style)
                    # Pass kwargs to Component
                    return Component("div", id=self.container_id, content=inner_html, class_=_fc or None, style=_fs or None, **self.attrs)
                
                self.app._register_component(self.container_id, builder)
                _reset_dynamic_fragment_children(self.container_id)
                
                # Now set fragment context
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ContainerContext(self, cid, border, height, cls, style, fill_height, align, justify, spacing, widget_gap, kwargs)

    def expander(self, label, expanded=False, icon=None, cls: str = "", style: str = ""):
        """Create an expandable/collapsible section
        
        Args:
            label: Section header text, State, ComputedState, or callable returning text
            expanded: Whether the section is initially expanded
            icon: Optional icon (emoji or string) to display before the label
        """
        cid = self._get_next_cid("expander")
        summary_cid = f"{cid}__summary"
        details_cid = f"{cid}__details"
        
        class ExpanderContext:
            def __init__(self, app, expander_id, label, expanded, icon=None, user_cls="", user_style=""):
                self.app = app
                self.expander_id = expander_id
                self.label = label
                self.expanded = expanded
                self.icon = icon
                self.user_cls = user_cls
                self.user_style = user_style
                
            def __enter__(self):
                def summary_builder():
                    from ..state import State, ComputedState

                    token = rendering_ctx.set(summary_cid)
                    try:
                        if isinstance(self.label, (State, ComputedState)):
                            resolved_label = str(self.label.value)
                        elif callable(self.label):
                            resolved_label = str(self.label())
                        else:
                            resolved_label = str(self.label)

                        if isinstance(self.icon, (State, ComputedState)):
                            resolved_icon = str(self.icon.value)
                        elif callable(self.icon):
                            resolved_icon = str(self.icon())
                        else:
                            resolved_icon = str(self.icon) if self.icon is not None else ""
                    finally:
                        rendering_ctx.reset(token)

                    icon_html = f'{resolved_icon} ' if resolved_icon else ''
                    return Component(
                        "span",
                        id=summary_cid,
                        content=f"{icon_html}{resolved_label}",
                        slot="summary",
                        style="font-weight:500;",
                    )

                if session_ctx.get() is None:
                    self.app.static_builders[summary_cid] = summary_builder
                else:
                    from ..state import get_session_store
                    store = get_session_store()
                    store['builders'][summary_cid] = summary_builder

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
                    summary_html = summary_builder().render()
                    restore_script = f'''
                    <script>
                    (function() {{
                        const details = document.getElementById({details_cid!r});
                        if (!details) return;

                        const storageKey = {'vl_expander_open:' + self.expander_id!r};
                        const storedOpen = sessionStorage.getItem(storageKey);
                        const serverOpen = {str(bool(self.expanded)).lower()};
                        const initialOpen = storedOpen === null ? serverOpen : storedOpen === 'true';

                        const applyOpen = function(nextOpen) {{
                            if (details.open !== nextOpen) {{
                                details.open = nextOpen;
                            }}
                        }};

                        const armPersistenceFromSummaryInteraction = function(event) {{
                            const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
                            const fromSummary = path.some(function(node) {{
                                return !!(node && typeof node.getAttribute === 'function' && node.getAttribute('slot') === 'summary');
                            }});

                            if (!fromSummary) return;
                            if (event.type === 'keydown') {{
                                const key = event.key || '';
                                if (key !== 'Enter' && key !== ' ') return;
                            }}

                            details.dataset.vlExpanderPersistArmed = 'true';
                        }};

                        const shouldPersistToggle = function() {{
                            return (
                                details.dataset.vlExpanderPersistArmed === 'true' &&
                                details.isConnected &&
                                document.getElementById(details.id) === details
                            );
                        }};

                        const clearPersistArm = function() {{
                            delete details.dataset.vlExpanderPersistArmed;
                        }};

                        applyOpen(initialOpen);
                        requestAnimationFrame(function() {{
                            applyOpen(initialOpen);
                        }});

                        if (!details.dataset.vlExpanderPersistenceBound) {{
                            details.dataset.vlExpanderPersistenceBound = 'true';
                            details.addEventListener('click', armPersistenceFromSummaryInteraction, true);
                            details.addEventListener('keydown', armPersistenceFromSummaryInteraction, true);
                            details.addEventListener('wa-show', function() {{
                                requestAnimationFrame(function() {{
                                    if (shouldPersistToggle()) {{
                                        sessionStorage.setItem(storageKey, 'true');
                                    }}
                                    clearPersistArm();
                                }});
                            }});
                            details.addEventListener('wa-hide', function() {{
                                requestAnimationFrame(function() {{
                                    if (shouldPersistToggle()) {{
                                        sessionStorage.setItem(storageKey, 'false');
                                    }}
                                    clearPersistArm();
                                }});
                            }});
                        }}
                    }})();
                    </script>
                    '''
                    html = f'''
                    <wa-details id="{details_cid}" {open_attr}>
                        {summary_html}
                        <div style="padding:0.5rem 0; display:flex; flex-direction:column; width:100%; min-width:0;">{inner_html}</div>
                    </wa-details>
                    {restore_script}
                    '''
                    _wd = self.app._get_widget_defaults("expander")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=self.expander_id, content=html, class_=_fc or None, style=_fs or None)
                
                self.app._register_component(self.expander_id, builder)
                _reset_dynamic_fragment_children(self.expander_id)
                
                # Now set fragment context for children
                from ..context import fragment_ctx
                self.token = fragment_ctx.set(self.expander_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                from ..context import fragment_ctx
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ExpanderContext(self, cid, label, expanded, icon, cls, style)

    def tabs(self, labels: List[str], cls: str = "", style: str = "", *, key: Any = None):
        """Create tabbed interface.

        Args:
            labels: Tab labels in display order.
            cls: Additional CSS classes for the outer wrapper.
            style: Additional inline styles for the outer wrapper.
            key: Optional stable identifier for preserving active-tab state across
                 rerenders when surrounding component order can change.
        """
        cid = f"tabs_{_sanitize_layout_key(key)}" if key is not None else self._get_next_cid("tabs")
        
        class TabsManager:
            def __init__(self, app, tabs_id, labels, user_cls="", user_style=""):
                self.app = app
                self.tabs_id = tabs_id
                self.labels = labels
                self.user_cls = user_cls
                self.user_style = user_style
                self.tab_objects = []
                self.panel_names = [f"panel-{i}" for i in range(len(self.labels))]
                self.default_panel = self.panel_names[0] if self.panel_names else ""
                self.active_tab_state = self.app.state(self.default_panel, key=f"{self.tabs_id}__active_tab")
                self.action_cid = f"{self.tabs_id}__active_tab_action"
                
                # Create tab objects immediately
                for i, label in enumerate(self.labels):
                    tab_obj = TabObject(self.app, f"{self.tabs_id}_tab_{i}", label, i == 0)
                    _reset_dynamic_fragment_children(tab_obj.tab_id)
                    self.tab_objects.append(tab_obj)

                def tab_action(panel_name):
                    if panel_name in self.panel_names:
                        self.active_tab_state.set(panel_name)

                self.app.static_actions[self.action_cid] = tab_action
                
                # Register tabs builder immediately
                self._register_builder()

            def _register_builder(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    store['actions'][self.action_cid] = self.app.static_actions[self.action_cid]

                    active_panel = self.active_tab_state.value
                    if active_panel not in self.panel_names:
                        active_panel = self.default_panel
                    group_id = f"{self.tabs_id}_group"
                    
                    # Build tab headers
                    headers = []
                    for i, label in enumerate(self.labels):
                        panel_name = self.panel_names[i]
                        headers.append(f'<wa-tab slot="nav" panel="{panel_name}">{label}</wa-tab>')
                    
                    # Build tab panels
                    panels = []
                    for i, tab_obj in enumerate(self.tab_objects):
                        panel_name = self.panel_names[i]
                        # Render tab content
                        tab_htmls = []
                        # Check static
                        for cid, b in self.app.static_fragment_components.get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        # Check session
                        for cid, b in store['fragment_components'].get(tab_obj.tab_id, []):
                            tab_htmls.append(b().render())
                        
                        panel_content = "".join(tab_htmls)
                        panels.append(f'<wa-tab-panel name="{panel_name}">{panel_content}</wa-tab-panel>')

                    restore_script = f'''
                    <script>
                    (function() {{
                        const group = document.getElementById('{group_id}');
                        if (!group) return;

                        const storageKey = 'vl_active_tab:{self.tabs_id}';
                        const validPanels = new Set({self.panel_names!r});
                        const defaultPanel = {self.default_panel!r};
                        const serverPanel = {active_panel!r};
                        const actionCid = {self.action_cid!r};
                        const shouldSyncServer = group.dataset.vlSyncServer === 'true';

                        const applyActivePanel = function(panelName) {{
                            if (!panelName || !validPanels.has(panelName)) return false;
                            group.setAttribute('active', panelName);
                            requestAnimationFrame(function() {{
                                group.setAttribute('active', panelName);
                                if (typeof group.updateActiveTab === 'function') {{
                                    group.updateActiveTab();
                                }}
                            }});
                            return true;
                        }};

                        const syncServer = function(panelName) {{
                            if (!shouldSyncServer) return;
                            if (!panelName || panelName === serverPanel) return;
                            if (typeof window.sendAction === 'function') {{
                                window.sendAction(actionCid, panelName);
                            }}
                        }};

                        const storedPanel = sessionStorage.getItem(storageKey);
                        const initialPanel = validPanels.has(storedPanel) ? storedPanel : (validPanels.has(serverPanel) ? serverPanel : defaultPanel);
                        applyActivePanel(initialPanel);
                        sessionStorage.setItem(storageKey, initialPanel);
                        syncServer(initialPanel);

                        if (!group.dataset.vlTabPersistenceBound) {{
                            group.dataset.vlTabPersistenceBound = 'true';
                            group.addEventListener('wa-tab-show', function(event) {{
                                const panelName = event.detail && event.detail.name;
                                if (!validPanels.has(panelName)) return;
                                sessionStorage.setItem(storageKey, panelName);
                                syncServer(panelName);
                            }});
                        }}
                    }})();
                    </script>
                    '''
                    
                    html = f'''
                    <wa-tab-group id="{group_id}" active="{active_panel}">
                        {"".join(headers)}
                        {"".join(panels)}
                    </wa-tab-group>
                    {restore_script}
                    '''
                    _wd = self.app._get_widget_defaults("tabs")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=self.tabs_id, content=html, class_=_fc or None, style=_fs or None)
                
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
        
        return TabsManager(self, cid, labels, cls, style)

    def empty(self):
        """Create an empty container that can be updated later"""
        cid = self._get_next_cid("empty")
        _app = self

        # Register the empty placeholder builder.
        # Renders dynamic (session) fragment children when present,
        # falls back to static (initial-render) children otherwise.
        def builder():
            from ..state import get_session_store
            from ..context import rendering_ctx
            store = get_session_store()

            token = rendering_ctx.set(cid)
            htmls = []
            dyn = store['fragment_components'].get(cid)
            if dyn is not None:
                for child_cid, b in dyn:
                    try:
                        htmls.append(b().render())
                    except Exception:
                        pass
            else:
                for child_cid, b in _app.static_fragment_components.get(cid, []):
                    try:
                        htmls.append(b().render())
                    except Exception:
                        pass
            rendering_ctx.reset(token)
            return Component("div", id=cid, content="".join(htmls))

        _app._register_component(cid, builder)

        class EmptyContainer:
            """Proxy object for the empty placeholder widget."""

            @property
            def container_id(self_):
                return cid

            def container(self_):
                """Context manager; write widget calls inside the placeholder."""
                class _PlaceholderCtx:
                    def __enter__(ctx_self):
                        from ..state import get_session_store
                        from ..context import fragment_ctx
                        store = get_session_store()
                        # Clear previous dynamic children so they don't accumulate
                        store['fragment_components'][cid] = []
                        ctx_self._token = fragment_ctx.set(cid)
                        return ctx_self

                    def __exit__(ctx_self, *_):
                        from ..context import fragment_ctx, session_ctx
                        from ..state import get_session_store
                        fragment_ctx.reset(ctx_self._token)
                        # Only force a follow-up dirty update when mutating outside an active render pass.
                        if _should_mark_placeholder_dirty():
                            store = get_session_store()
                            store.setdefault('forced_dirty', set()).add(cid)

                return _PlaceholderCtx()

            def empty(self_):
                """Clear the placeholder content."""
                from ..state import get_session_store
                store = get_session_store()
                store['fragment_components'][cid] = []
                if _should_mark_placeholder_dirty():
                    store.setdefault('forced_dirty', set()).add(cid)

            def write(self_, content):
                """Replace placeholder content with a plain string."""
                from ..state import get_session_store
                write_cid = f"{cid}_write"
                def _write_builder():
                    return Component(None, id=write_cid, content=str(content))
                store = get_session_store()
                store['fragment_components'][cid] = [(write_cid, _write_builder)]
                if _should_mark_placeholder_dirty():
                    store.setdefault('forced_dirty', set()).add(cid)

            def __getattr__(self_, name):
                return getattr(_app, name)

        return EmptyContainer()

    def dialog(self, title, width="small"):
        """Create a modal dialog (decorator)
        
        Args:
            title: Dialog title
            width: Dialog width - "small", "medium", "large", or CSS value
        """
        _width_map = {"small": "400px", "medium": "600px", "large": "800px"}
        dialog_width = _width_map.get(width, width)
        
        def decorator(func):
            dialog_id = f"dialog_{func.__name__}"
            modal_id = f"{dialog_id}_modal"

            def builder():
                from ..state import get_session_store
                store = get_session_store()

                htmls = []
                for child_cid, child_builder in store['fragment_components'].get(dialog_id, []):
                    htmls.append(child_builder().render())

                inner_html = "".join(htmls)
                if not inner_html:
                    return Component("div", id=dialog_id, content="")

                html = f'''
                <wa-dialog id="{modal_id}" label="{title}" open light-dismiss style="--width: {dialog_width};">
                    <div style="padding:1rem;">{inner_html}</div>
                </wa-dialog>
                <script>
                    (() => {{
                        const dialog = document.getElementById('{modal_id}');
                        if (!dialog) return;
                        dialog.open = true;
                        requestAnimationFrame(() => {{
                            dialog.open = true;
                        }});
                        if (dialog.dataset.vlHideBound === 'true') return;
                        dialog.dataset.vlHideBound = 'true';
                        // Listen for native close event (e.g. backdrop click, escape key, etc.)
                        dialog.addEventListener('wa-after-hide', (e) => {{
                            if (e.target.id === '{modal_id}') {{
                                window.sendAction('{dialog_id}', 'closed');
                            }}
                        }});
                    }})();
                </script>
                '''
                return Component("div", id=dialog_id, content=html)

            def close_dialog(*args, **kwargs):
                self._enqueue_eval(
                    f"""
                    (() => {{
                        const dialog = document.getElementById('{modal_id}');
                        if (!dialog) return;
                        if (typeof dialog.requestClose === 'function') {{
                            dialog.requestClose();
                            return;
                        }}
                        if (dialog.dialog && typeof dialog.dialog.close === 'function') {{
                            dialog.dialog.close();
                            return;
                        }}
                        if (typeof dialog.hide === 'function') {{
                            dialog.hide();
                            return;
                        }}
                        dialog.open = false;
                    }})();
                    """
                )

            def dialog_action(value=None):
                if value == 'closed':
                    return
                close_dialog()

            self._register_component(dialog_id, builder, action=dialog_action)
            
            # Create a function to open the dialog
            def open_dialog(*args, **kwargs):
                from ..state import get_session_store
                store = get_session_store()
                # Clear previous children so re-opening doesn't accumulate
                store['fragment_components'][dialog_id] = []

                # Set fragment context for dialog content
                token = fragment_ctx.set(dialog_id)

                # Execute the dialog content function
                func(*args, **kwargs)

                fragment_ctx.reset(token)
                
                from ..context import session_ctx
                sid = session_ctx.get()
                        
                # Force dirty to update it immediately
                if sid is not None:
                    store.setdefault('forced_dirty', set()).add(dialog_id)

            open_dialog.open = open_dialog
            open_dialog.close = close_dialog
            
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
                _reset_dynamic_fragment_children(self.container_id)
                
                # Set fragment context
                self.token = fragment_ctx.set(self.container_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return ListContainerContext(self, cid, gap, style_props)

    def popover(self, label, use_container_width=False, disabled=False, help=None, cls: str = "", style: str = ""):
        """Create a popover container triggered by a button click.
        
        Args:
            label: Button label text
            use_container_width: If True, button takes full container width
            disabled: If True, button is disabled
            help: Optional help tooltip text
            cls: Additional CSS classes
            style: Additional inline styles
        
        Example:
            with app.popover("Settings"):
                app.text("Popover content")
                app.slider("Volume", 0, 100, 50)
        """
        cid = self._get_next_cid("popover")
        
        class PopoverContext:
            def __init__(self, app, popover_id, label, use_container_width, disabled, help_text, user_cls, user_style):
                self.app = app
                self.popover_id = popover_id
                self.label = label
                self.use_container_width = use_container_width
                self.disabled = disabled
                self.help_text = help_text
                self.user_cls = user_cls
                self.user_style = user_style
                
            def __enter__(self):
                def builder():
                    from ..state import get_session_store
                    store = get_session_store()
                    
                    htmls = []
                    for child_cid, b in self.app.static_fragment_components.get(self.popover_id, []):
                        htmls.append(b().render())
                    for child_cid, b in store['fragment_components'].get(self.popover_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    
                    disabled_attr = 'disabled' if self.disabled else ''
                    width_style = 'style="width:100%;"' if self.use_container_width else ''
                    help_attr = f'title="{self.help_text}"' if self.help_text else ''
                    
                    html = f'''
                    <wa-dropdown id="{self.popover_id}" {disabled_attr}>
                        <wa-button slot="trigger" with-caret variant="neutral" appearance="outlined" {disabled_attr} {width_style} {help_attr}>
                            {self.label}
                        </wa-button>
                        <div style="padding: 1rem; background: var(--wa-color-surface-raised, var(--vl-bg-card)); border-radius: var(--wa-border-radius-m, var(--vl-radius)); min-width: 200px; max-width: 400px; box-shadow: 0 18px 38px rgba(15, 23, 42, 0.18);">
                            {inner_html}
                        </div>
                    </wa-dropdown>
                    '''
                    _wd = self.app._get_widget_defaults("popover")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=f"{self.popover_id}_wrap", content=html, class_=_fc or None, style=_fs or None)
                
                self.app._register_component(self.popover_id, builder)
                _reset_dynamic_fragment_children(self.popover_id)
                self.token = fragment_ctx.set(self.popover_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return PopoverContext(self, cid, label, use_container_width, disabled, help, cls, style)


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
        """Proxy app methods while preserving this column as the active fragment."""
        attr = getattr(self.app, name)

        if not callable(attr):
            return attr

        @wraps(attr)
        def column_bound(*args, **kwargs):
            from ..context import fragment_ctx

            token = fragment_ctx.set(self.col_id)
            try:
                return attr(*args, **kwargs)
            finally:
                fragment_ctx.reset(token)

        return column_bound


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

