"""Data Widgets Mixin for Violit"""

import html as html_lib
from typing import Union, Callable, Optional, Any
import hashlib
import inspect
import json
import re
from ..component import Component
from ..context import rendering_ctx
from ..state import State
from ..style_utils import merge_cls, merge_style, resolve_value


class DataWidgetsMixin:
    """Data display widgets (dataframe, table, data_editor, metric, json)"""

    @staticmethod
    def _sanitize_widget_key(value: Any) -> str:
        raw = str(value)
        normalized = re.sub(r"[^a-zA-Z0-9_-]", "_", raw)
        normalized = re.sub(r"_+", "_", normalized).strip("_")

        if normalized and normalized == raw and len(normalized) <= 64:
            return normalized

        digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
        if not normalized:
            return f"widget_{digest}"
        return f"{normalized[:48]}_{digest}"

    def _resolve_widget_cid(self, widget_type: str, key=None) -> str:
        if key is None:
            return self._get_next_cid(widget_type)
        return f"{widget_type}_{self._sanitize_widget_key(key)}"

    @staticmethod
    def _clone_editor_state_value(value: Any):
        try:
            import pandas as pd  # type: ignore
        except Exception:
            pd = None

        if pd is not None and isinstance(value, pd.DataFrame):
            return value.copy()
        if isinstance(value, list):
            return [dict(row) if isinstance(row, dict) else row for row in value]
        return value

    @staticmethod
    def _coerce_editor_records(value: Any) -> list[dict[str, Any]]:
        try:
            import pandas as pd  # type: ignore
        except Exception:
            pd = None

        if pd is not None and isinstance(value, pd.DataFrame):
            return value.to_dict('records')
        if isinstance(value, list):
            return [dict(row) if isinstance(row, dict) else row for row in value]
        if value is None:
            return []
        if isinstance(value, dict):
            return [dict(value)]
        return []

    @staticmethod
    def _editor_prefers_dataframe(current_value: Any, seed_value: Any) -> bool:
        try:
            import pandas as pd  # type: ignore
        except Exception:
            return False
        return isinstance(current_value, pd.DataFrame) or isinstance(seed_value, pd.DataFrame)

    @staticmethod
    def _build_ag_grid_theme_style(theme: str = "auto", theme_colors: Optional[dict] = None) -> str:
        mode = (theme or "auto").lower()
        if mode == "dark":
            base_background = "#16181d"
            base_surface = "#20242b"
            base_border = "#3a404c"
            base_text = "#f3f4f6"
            base_muted = "#a1a1aa"
            base_accent = "var(--vl-primary)"
            row_hover = "color-mix(in srgb, #20242b, white 8%)"
            selected_row = "color-mix(in srgb, var(--vl-primary), #20242b 78%)"
        elif mode == "light":
            base_background = "#ffffff"
            base_surface = "#f8fafc"
            base_border = "#d7deea"
            base_text = "#111827"
            base_muted = "#6b7280"
            base_accent = "var(--vl-primary)"
            row_hover = "color-mix(in srgb, #f8fafc, var(--vl-primary) 7%)"
            selected_row = "color-mix(in srgb, var(--vl-primary), white 84%)"
        else:
            base_background = "var(--vl-bg-card)"
            base_surface = "color-mix(in srgb, var(--vl-bg-card), var(--vl-text) 3%)"
            base_border = "var(--vl-border)"
            base_text = "var(--vl-text)"
            base_muted = "var(--vl-text-muted)"
            base_accent = "var(--vl-primary)"
            row_hover = "color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 7%)"
            selected_row = "color-mix(in srgb, var(--vl-primary), var(--vl-bg-card) 82%)"

        color_map = {
            "background": base_background,
            "surface": base_surface,
            "border": base_border,
            "text": base_text,
            "muted": base_muted,
            "accent": base_accent,
            "row_hover": row_hover,
            "selected_row": selected_row,
        }
        if theme_colors:
            color_map.update({k: v for k, v in theme_colors.items() if v is not None})

        return "; ".join([
            f"--ag-background-color: {color_map['background']}",
            f"--ag-foreground-color: {color_map['text']}",
            f"--ag-header-background-color: {color_map['surface']}",
            f"--ag-header-foreground-color: {color_map['text']}",
            f"--ag-odd-row-background-color: {color_map['surface']}",
            f"--ag-border-color: {color_map['border']}",
            f"--ag-secondary-border-color: {color_map['border']}",
            f"--ag-row-hover-color: {color_map['row_hover']}",
            f"--ag-selected-row-background-color: {color_map['selected_row']}",
            f"--ag-input-focus-border-color: {color_map['accent']}",
            f"--ag-checkbox-checked-color: {color_map['accent']}",
            f"--ag-range-selection-border-color: {color_map['accent']}",
            f"--ag-font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "--ag-font-size: 0.95rem",
            "--ag-grid-size: 8px",
            "--ag-list-item-height: 36px",
        ])

    @staticmethod
    def _resolve_ag_grid_width(width: Any, use_container_width: bool, content_width: str) -> str:
        if width is None:
            return "100%" if use_container_width else content_width
        if isinstance(width, (int, float)):
            return f"min(100%, {int(width)}px)"
        width_text = str(width).strip()
        if not width_text:
            return "100%" if use_container_width else content_width
        lowered = width_text.lower()
        if lowered == "stretch":
            return "100%"
        if lowered == "content":
            return content_width
        return width_text

    @staticmethod
    def _normalize_ag_grid_column_config_entry(column_config: Any, column_name: str) -> Optional[dict[str, Any]]:
        if not isinstance(column_config, dict) or column_name not in column_config:
            return {}
        raw_value = column_config.get(column_name)
        if raw_value in (None, False):
            return None
        if isinstance(raw_value, str):
            return {"headerName": raw_value}
        if isinstance(raw_value, dict):
            return dict(raw_value)
        return {}

    @staticmethod
    def _normalize_ag_grid_toolbar(toolbar: Any, default_file_name: str) -> dict[str, Any]:
        base = {
            "enabled": False,
            "search": False,
            "export_csv": False,
            "fullscreen": False,
            "search_placeholder": "Search table",
            "csv_file_name": default_file_name,
        }

        if toolbar in (None, False):
            return base

        if toolbar is True:
            base.update({
                "enabled": True,
                "search": True,
                "export_csv": True,
                "fullscreen": True,
            })
            return base

        if isinstance(toolbar, dict):
            enabled = toolbar.get("enabled", True)
            if not enabled:
                return base
            base.update({
                "enabled": True,
                "search": bool(toolbar.get("search", True)),
                "export_csv": bool(toolbar.get("export_csv", toolbar.get("download", toolbar.get("csv", True)))),
                "fullscreen": bool(toolbar.get("fullscreen", True)),
                "search_placeholder": str(toolbar.get("search_placeholder", toolbar.get("placeholder", "Search table"))),
                "csv_file_name": str(toolbar.get("csv_file_name", toolbar.get("file_name", default_file_name))),
            })
            return base

        return base

    def _build_ag_grid_surface_html(self, *, cid: str, height_css: str, width_css: str, grid_style: str,
                                    script_body: str, toolbar_config: dict[str, Any],
                                    toolbar_extra_actions_html: str = "", bottom_html: str = "",
                                    grid_config_hash: str = "") -> str:
        toolbar_html = ""
        if toolbar_config.get("enabled"):
            search_html = ""
            if toolbar_config.get("search"):
                search_html = (
                    f'<input id="{cid}_toolbar_search" class="vl-ag-grid-toolbar__search" '
                    f'type="search" placeholder="{html_lib.escape(str(toolbar_config.get("search_placeholder", "Search table")))}" />'
                )

            actions = []
            if toolbar_config.get("export_csv"):
                actions.append(
                    f'<button type="button" id="{cid}_toolbar_csv" class="vl-ag-grid-toolbar__button">Export CSV</button>'
                )
            if toolbar_config.get("fullscreen"):
                actions.append(
                    f'<button type="button" id="{cid}_toolbar_fullscreen" class="vl-ag-grid-toolbar__button">Fullscreen</button>'
                )
            if toolbar_extra_actions_html:
                actions.append(toolbar_extra_actions_html)

            toolbar_html = f'''
            <div id="{cid}_toolbar" class="vl-ag-grid-toolbar">
                <div class="vl-ag-grid-toolbar__left">{search_html}</div>
                <div class="vl-ag-grid-toolbar__right">{"".join(actions)}</div>
            </div>
            '''

        runtime_config = html_lib.escape(json.dumps({
            "apiKey": f"gridApi_{cid}",
            "surfaceId": f"{cid}_surface",
            "searchInputId": f"{cid}_toolbar_search" if toolbar_config.get("search") else None,
            "csvButtonId": f"{cid}_toolbar_csv" if toolbar_config.get("export_csv") else None,
            "fullscreenButtonId": f"{cid}_toolbar_fullscreen" if toolbar_config.get("fullscreen") else None,
            "fullscreenTargetId": f"{cid}_surface",
            "csvFileName": toolbar_config.get("csv_file_name", "data.csv"),
        }, ensure_ascii=False, separators=(",", ":")), quote=True)

        return f'''
            <style>
                #{cid}_surface {{
                    display: flex;
                    flex-direction: column;
                    gap: 0.625rem;
                    max-width: 100%;
                }}

                #{cid}_toolbar {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 0.75rem;
                    flex-wrap: wrap;
                    padding: 0.625rem 0.75rem;
                    border: 1px solid var(--vl-border);
                    border-radius: 0.875rem;
                    background: color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 3%);
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__left {{
                    flex: 1 1 16rem;
                    min-width: 14rem;
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__right {{
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    flex-wrap: wrap;
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__search {{
                    width: 100%;
                    min-height: 38px;
                    padding: 0.55rem 0.75rem;
                    border: 1px solid var(--vl-border);
                    border-radius: 0.7rem;
                    background: var(--vl-bg-card);
                    color: var(--vl-text);
                    outline: none;
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__search:focus {{
                    border-color: var(--vl-primary);
                    box-shadow: 0 0 0 3px color-mix(in srgb, var(--vl-primary), transparent 82%);
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__button {{
                    min-height: 38px;
                    padding: 0.55rem 0.85rem;
                    border: 1px solid var(--vl-border);
                    border-radius: 0.7rem;
                    background: var(--vl-bg-card);
                    color: var(--vl-text);
                    cursor: pointer;
                    transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
                }}

                #{cid}_toolbar .vl-ag-grid-toolbar__button:hover {{
                    border-color: var(--vl-primary);
                    background: color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 8%);
                    transform: translateY(-1px);
                }}

                #{cid}.vl-ag-grid .ag-body-viewport,
                #{cid}.vl-ag-grid .ag-body-horizontal-scroll-viewport {{
                    -ms-overflow-style: auto !important;
                    scrollbar-width: thin !important;
                }}

                #{cid}.vl-ag-grid .ag-center-cols-viewport {{
                    -ms-overflow-style: none !important;
                    scrollbar-width: none !important;
                }}

                #{cid}.vl-ag-grid .ag-body-vertical-scroll,
                #{cid}.vl-ag-grid .ag-body-vertical-scroll-viewport,
                #{cid}.vl-ag-grid .ag-body-vertical-scroll-container {{
                    display: none !important;
                    width: 0 !important;
                    min-width: 0 !important;
                    max-width: 0 !important;
                    overflow: hidden !important;
                }}

                #{cid}.vl-ag-grid .ag-body-viewport::-webkit-scrollbar,
                #{cid}.vl-ag-grid .ag-body-horizontal-scroll-viewport::-webkit-scrollbar {{
                    display: block !important;
                    width: 10px !important;
                    height: 10px !important;
                }}

                #{cid}.vl-ag-grid .ag-center-cols-viewport::-webkit-scrollbar {{
                    display: none !important;
                    width: 0 !important;
                    height: 0 !important;
                }}

                #{cid}.vl-ag-grid .ag-body-viewport::-webkit-scrollbar-track,
                #{cid}.vl-ag-grid .ag-body-horizontal-scroll-viewport::-webkit-scrollbar-track {{
                    background: transparent;
                }}

                #{cid}.vl-ag-grid .ag-body-viewport::-webkit-scrollbar-thumb,
                #{cid}.vl-ag-grid .ag-body-horizontal-scroll-viewport::-webkit-scrollbar-thumb {{
                    background: color-mix(in srgb, var(--vl-text-muted), transparent 30%);
                    border-radius: 999px;
                }}

                #{cid}.vl-ag-grid .ag-body-viewport::-webkit-scrollbar-thumb:hover,
                #{cid}.vl-ag-grid .ag-body-horizontal-scroll-viewport::-webkit-scrollbar-thumb:hover {{
                    background: color-mix(in srgb, var(--vl-primary), transparent 20%);
                }}

                #{cid}_surface:fullscreen {{
                    padding: 1rem;
                    background: var(--vl-bg-card);
                }}

                #{cid}_surface:fullscreen #{cid} {{
                    width: 100% !important;
                    height: calc(100vh - 6rem) !important;
                }}
            </style>
            <div id="{cid}_surface" class="vl-ag-grid-surface" data-vl-init="ag-grid-surface" data-vl-ag-grid-config="{runtime_config}">
                {toolbar_html}
                <div id="{cid}" data-vl-grid-config-hash="{grid_config_hash}" style="height: {height_css}; width: {width_css}; {grid_style};" class="ag-theme-alpine vl-ag-grid"></div>
                {bottom_html}
            </div>
            <script>(function(){{
                {script_body}
            }})();</script>
            '''
    
    def dataframe(self, df: Union['pd.DataFrame', Callable, State], height=400, 
                  column_defs=None, grid_options=None, on_cell_clicked=None,
                  use_container_width=True, hide_index=False, column_order=None,
                  column_config=None, width=None, toolbar=True,
                  theme: str = "auto", theme_colors: Optional[dict] = None,
                  cls: str = "", style: str = "", **props):
        """Display read-only interactive dataframe with AG Grid."""
        cid = self._get_next_cid("df")
        
        def action(v):
            """Handle cell click events"""
            if on_cell_clicked and callable(on_cell_clicked):
                payload = v
                if isinstance(v, str):
                    stripped = v.strip()
                    if stripped.startswith("{") or stripped.startswith("["):
                        try:
                            payload = json.loads(stripped)
                        except Exception:
                            payload = v
                on_cell_clicked(payload)
        
        def builder():
            import pandas as pd
            # Handle Signal
            token = rendering_ctx.set(cid)
            try:
                current_df = resolve_value(df)
                current_height = resolve_value(height)
                current_column_defs = resolve_value(column_defs)
                current_grid_options = resolve_value(grid_options)
                current_use_container_width = bool(resolve_value(use_container_width))
                current_hide_index = bool(resolve_value(hide_index))
                current_column_order = resolve_value(column_order)
                current_column_config = resolve_value(column_config)
                current_width = resolve_value(width)
                current_toolbar = resolve_value(toolbar)
                current_theme = resolve_value(theme)
                current_theme_colors = resolve_value(theme_colors)
            finally:
                rendering_ctx.reset(token)
                
            if not isinstance(current_df, pd.DataFrame):
                # Fallback or try to convert
                try: current_df = pd.DataFrame(current_df)
                except: return Component("div", id=cid, content="Invalid data format")

            display_df = current_df.copy()

            if not current_hide_index:
                display_df = display_df.reset_index()
            
            # Apply column_order if specified
            if isinstance(current_column_order, (list, tuple)):
                ordered = [c for c in current_column_order if c in display_df.columns]
                if ordered:
                    remaining = [c for c in display_df.columns if c not in ordered]
                    display_df = display_df[ordered + remaining]

            data = display_df.to_dict('records')

            configured_columns = current_column_config if isinstance(current_column_config, dict) else {}
            extra_options = current_grid_options if isinstance(current_grid_options, dict) else {}

            # Use custom column_defs or generate defaults
            if isinstance(current_column_defs, (list, tuple)) and current_column_defs:
                cols = []
                for current_col in current_column_defs:
                    if not isinstance(current_col, dict):
                        cols.append(current_col)
                        continue
                    normalized_col = dict(current_col)
                    normalized_col["editable"] = False
                    cols.append(normalized_col)
            else:
                cols = []
                for column_name in display_df.columns:
                    current_config = self._normalize_ag_grid_column_config_entry(configured_columns, column_name)
                    if current_config is None:
                        continue
                    if current_config.pop("hide", False) or current_config.pop("hidden", False):
                        continue
                    label = current_config.pop("label", None)
                    current_config.pop("editable", None)
                    current_config.pop("readonly", None)
                    column_def = {"field": column_name, "sortable": True, "filter": True, "editable": False}
                    if label is not None and "headerName" not in current_config:
                        column_def["headerName"] = str(label)
                    column_def.update(current_config)
                    column_def["editable"] = False
                    cols.append(column_def)
                if not cols:
                    cols = [{"field": c, "sortable": True, "filter": True, "editable": False} for c in display_df.columns]
            
            # Add cell click handler if provided
            cell_click_handler = ""
            if on_cell_clicked:
                cell_click_handler = f'''
                onCellClicked: (params) => {{
                    const cellData = {{
                        value: params.value,
                        field: params.colDef.field,
                        rowData: params.data,
                        rowIndex: params.rowIndex
                    }};
                    {f"window.sendAction('{cid}', cellData);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(cellData)}}, swap: 'none'}});"}
                }},
                '''
            
            grid_style = self._build_ag_grid_theme_style(theme=current_theme, theme_colors=current_theme_colors)
            content_width = f"min(100%, {max(520, max(1, len(cols)) * 132)}px)"
            container_width = self._resolve_ag_grid_width(current_width, current_use_container_width, content_width)
            resolved_height = f"{int(current_height)}px" if isinstance(current_height, (int, float)) else str(current_height)
            toolbar_config = self._normalize_ag_grid_toolbar(current_toolbar, "dataframe.csv")
            toolbar_bind_config = {
                "apiKey": f"gridApi_{cid}",
                "surfaceId": f"{cid}_surface",
                "searchInputId": f"{cid}_toolbar_search" if toolbar_config.get("search") else None,
                "csvButtonId": f"{cid}_toolbar_csv" if toolbar_config.get("export_csv") else None,
                "fullscreenButtonId": f"{cid}_toolbar_fullscreen" if toolbar_config.get("fullscreen") else None,
                "fullscreenTargetId": f"{cid}_surface",
                "csvFileName": toolbar_config.get("csv_file_name", "dataframe.csv"),
            }
            grid_config_hash = hashlib.sha1(
                json.dumps(
                    {
                        "cols": cols,
                        "grid_options": extra_options,
                        "toolbar": toolbar_config,
                        "width": container_width,
                        "height": resolved_height,
                        "hide_index": current_hide_index,
                    },
                    sort_keys=True,
                    default=str,
                ).encode("utf-8")
            ).hexdigest()
            html = self._build_ag_grid_surface_html(
                cid=cid,
                height_css=resolved_height,
                width_css=container_width,
                grid_style=grid_style,
                toolbar_config=toolbar_config,
                grid_config_hash=grid_config_hash,
                script_body=f'''
                function initGrid() {{
                    const opt = {{ 
                        columnDefs: {json.dumps(cols, default=str)}, 
                        rowData: {json.dumps(data, default=str)},
                        defaultColDef: {{flex: 1, minWidth: 100, resizable: true, editable: false}},
                        suppressScrollOnNewData: true,
                        {cell_click_handler}
                        ...{json.dumps(extra_options)}
                    }};
                    const el = document.querySelector('#{cid}');
                    if (el && window.agGrid) {{ 
                        const gridApi = agGrid.createGrid(el, opt);
                        window['gridApi_{cid}'] = gridApi;
                        if (window.violitRuntime && typeof window.violitRuntime.bindAgGridSurface === 'function') {{
                            window.violitRuntime.bindAgGridSurface({json.dumps(toolbar_bind_config)});
                        }}
                    }}
                    else {{ console.error("agGrid not found"); }}
                }}

                window._vlLoadLib('agGrid', function() {{
                    if (document.readyState === 'loading') {{
                        document.addEventListener('DOMContentLoaded', initGrid);
                    }} else {{
                        initGrid();
                    }}
                }});
                ''',
            )
            _wd = self._get_widget_defaults("dataframe")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action if on_cell_clicked else None)

    def table(self, df: Union['pd.DataFrame', Callable, State], cls: str = "", style: str = "", **props):
        """Display static HTML table (Signal support)"""
        cid = self._get_next_cid("table")
        def builder():
            import pandas as pd
            # Handle Signal
            token = rendering_ctx.set(cid)
            try:
                current_df = resolve_value(df)
            finally:
                rendering_ctx.reset(token)
            
            if not isinstance(current_df, pd.DataFrame):
                try: current_df = pd.DataFrame(current_df)
                except: return Component("div", id=cid, content="Invalid data format")

            # Convert dataframe to HTML table
            html_table = current_df.to_html(index=False, border=0, classes=['data-table'])
            styled_html = f'''
            <div style="overflow-x:auto;border:1px solid var(--vl-border);border-radius:0.5rem;">
                <style>
                    .data-table {{
                        width: 100%;
                        border-collapse: collapse;
                        background: var(--vl-bg-card);
                        color: var(--vl-text);
                    }}
                    .data-table thead {{
                        background: color-mix(in srgb, var(--vl-primary), black 6%);
                        color: white;
                    }}
                    .data-table th, .data-table td {{
                        padding: 0.75rem;
                        text-align: left;
                        border-bottom: 1px solid var(--vl-border);
                    }}
                    .data-table thead th {{
                        background: color-mix(in srgb, var(--vl-primary), black 6%);
                        color: white !important;
                        font-weight: 700;
                    }}
                    .data-table thead th * {{
                        color: inherit !important;
                    }}
                    .data-table tbody td {{
                        color: var(--vl-text);
                    }}
                    .data-table tbody tr:hover {{
                        background: color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 5%);
                    }}
                </style>
                {html_table}
            </div>
            '''
            _wd = self._get_widget_defaults("table")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=styled_html, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def data_editor(self, df: 'pd.DataFrame', num_rows="fixed", height=400, key=None, on_change=None,
                    on_row_click=None, disabled=False, hide_index=False, column_order=None, use_container_width=True,
                    width=None, toolbar=True, row_selection=None, delete_selected=False,
                    column_config=None, validator=None, grid_options=None,
                    theme: str = "auto", theme_colors: Optional[dict] = None,
                    cls: str = "", style: str = "", bind=None, **props):
        """Interactive data editor with optional column config and validation."""
        import pandas as pd
        cid = self._resolve_widget_cid("data_editor", key)

        if bind is not None:
            if not isinstance(bind, State):
                raise TypeError("data_editor bind= must be a State instance.")
            s = bind
        else:
            state_key = f"_vl_widget:data_editor:key:{key}" if key is not None else f"_vl_widget:data_editor:cid:{cid}"
            s = self.state(df.to_dict('records'), key=state_key)

        def _invoke_on_change(updated_df, payload):
            if not on_change:
                return
            try:
                param_count = len(inspect.signature(on_change).parameters)
            except (TypeError, ValueError):
                param_count = 1

            if param_count >= 2:
                on_change(updated_df, payload)
            else:
                on_change(updated_df)

        def _invoke_on_row_click(payload):
            if not on_row_click:
                return

            try:
                param_count = len(inspect.signature(on_row_click).parameters)
            except (TypeError, ValueError):
                param_count = 1

            row_data = payload.get("rowData", {}) if isinstance(payload, dict) else payload
            if param_count >= 2:
                on_row_click(row_data, payload)
            else:
                on_row_click(row_data)

        def _normalize_validation_result(result, fallback_df):
            valid = True
            message = None
            normalized_df = fallback_df

            if isinstance(result, dict):
                valid = result.get("ok", True)
                message = result.get("message")
                if "df" in result:
                    normalized_df = result["df"]
                elif "data" in result:
                    normalized_df = pd.DataFrame(result["data"])
            elif isinstance(result, tuple):
                valid = bool(result[0])
                if len(result) > 1:
                    message = result[1]
                if len(result) > 2:
                    normalized_df = result[2]
            elif isinstance(result, str):
                valid = False
                message = result
            elif result is False:
                valid = False

            if isinstance(normalized_df, list):
                normalized_df = pd.DataFrame(normalized_df)

            return valid, message, normalized_df
        
        def action(v):
            try:
                payload = json.loads(v) if isinstance(v, str) else v
                previous_store_value = self._clone_editor_state_value(s.value)
                previous_data = self._coerce_editor_records(s.value)
                event_payload = payload if isinstance(payload, dict) else {"eventType": "full_sync", "allData": payload}
                event_type = event_payload.get("eventType")

                if event_type == "row_click":
                    _invoke_on_row_click(event_payload)
                    return

                new_data = event_payload.get("allData", previous_data)

                if not isinstance(new_data, list):
                    return

                candidate_df = pd.DataFrame(new_data)

                if validator:
                    try:
                        validation_result = validator(event_payload, candidate_df.copy())
                    except Exception as exc:
                        validation_result = {"ok": False, "message": str(exc)}

                    valid, message, normalized_df = _normalize_validation_result(validation_result, candidate_df)
                    if not valid:
                        s.set(previous_store_value)
                        if message:
                            self.toast(message, variant="danger", icon="triangle-exclamation")
                        return
                    candidate_df = normalized_df if isinstance(normalized_df, pd.DataFrame) else pd.DataFrame(normalized_df)
                    new_data = candidate_df.to_dict('records')

                next_store_value = candidate_df if self._editor_prefers_dataframe(s.value, df) else new_data
                s.set(next_store_value)

                try:
                    _invoke_on_change(pd.DataFrame(new_data), event_payload)
                except Exception as exc:
                    s.set(previous_store_value)
                    self.toast(str(exc), variant="danger", icon="triangle-exclamation")
            except Exception:
                pass
        
        def builder():
            token = rendering_ctx.set(cid)
            try:
                data = self._coerce_editor_records(s.value)
                current_num_rows = resolve_value(num_rows)
                current_height = resolve_value(height)
                current_disabled = resolve_value(disabled)
                current_column_order = resolve_value(column_order)
                current_use_container_width = bool(resolve_value(use_container_width))
                current_width = resolve_value(width)
                current_toolbar = resolve_value(toolbar)
                current_row_selection = resolve_value(row_selection)
                current_delete_selected = bool(resolve_value(delete_selected))
                current_column_config = resolve_value(column_config)
                current_grid_options = resolve_value(grid_options)
                current_theme = resolve_value(theme)
                current_theme_colors = resolve_value(theme_colors)
            finally:
                rendering_ctx.reset(token)
            
            source_df = df if isinstance(df, pd.DataFrame) else pd.DataFrame(data)
            _cols_list = list(source_df.columns)
            if isinstance(current_column_order, (list, tuple)):
                ordered = [c for c in current_column_order if c in _cols_list]
                remaining = [c for c in _cols_list if c not in ordered]
                _cols_list = ordered + remaining

            if isinstance(current_disabled, bool):
                editor_disabled = current_disabled
                disabled_columns = set()
            elif isinstance(current_disabled, (list, tuple, set)):
                editor_disabled = False
                disabled_columns = {str(item) for item in current_disabled}
            else:
                editor_disabled = bool(current_disabled)
                disabled_columns = set()

            editable = not editor_disabled
            configured_columns = current_column_config if isinstance(current_column_config, dict) else {}
            cols = []
            for column_name in _cols_list:
                current_config = self._normalize_ag_grid_column_config_entry(configured_columns, column_name)
                if current_config is None:
                    continue
                if current_config.pop("hide", False) or current_config.pop("hidden", False):
                    continue
                label = current_config.pop("label", None)
                column_editable = current_config.pop("editable", editable and column_name not in disabled_columns)
                if current_config.pop("readonly", False):
                    column_editable = False
                if current_config.pop("disabled", False):
                    column_editable = False
                if column_name in disabled_columns:
                    column_editable = False

                editor_type = current_config.pop("type", current_config.pop("editor", "text"))
                editor_options = current_config.pop("options", current_config.pop("values", None))
                number_min = current_config.pop("min", None)
                number_max = current_config.pop("max", None)
                number_step = current_config.pop("step", None)
                column_def = {
                    "field": column_name,
                    "sortable": True,
                    "filter": True,
                    "editable": column_editable,
                    "__editorType": editor_type,
                    "__options": editor_options,
                    "__numberMin": number_min,
                    "__numberMax": number_max,
                    "__numberStep": number_step,
                }
                if label is not None and "headerName" not in current_config:
                    column_def["headerName"] = str(label)
                column_def.update(current_config)
                cols.append(column_def)

            selection_mode = None
            if isinstance(current_row_selection, str):
                normalized_selection_mode = current_row_selection.strip().lower()
                if normalized_selection_mode in {"single", "multiple"}:
                    selection_mode = normalized_selection_mode
            elif current_row_selection is True:
                selection_mode = "single"

            if current_delete_selected:
                selection_mode = "multiple"

            show_delete_selected = bool(current_delete_selected and selection_mode == "multiple")

            if selection_mode and cols:
                first_col = dict(cols[0])
                first_col.setdefault("checkboxSelection", True)
                if selection_mode == "multiple":
                    first_col.setdefault("headerCheckboxSelection", True)
                    first_col.setdefault("headerCheckboxSelectionFilteredOnly", False)
                first_col.setdefault("pinned", "left")
                first_col.setdefault("minWidth", max(int(first_col.get("minWidth", 120)), 120))
                cols[0] = first_col

            extra_options = {}
            if isinstance(current_grid_options, dict):
                extra_options.update(current_grid_options)
            if props:
                extra_options.update(props)

            toolbar_config = self._normalize_ag_grid_toolbar(current_toolbar, "data_editor.csv")
            add_row_button_html = '' if current_num_rows == "fixed" else f'''
            <button type="button" id="{cid}_toolbar_add" class="vl-ag-grid-toolbar__button" onclick="window.addDataRow_{cid} && window.addDataRow_{cid}()">Add Row</button>
            '''
            delete_selected_button_html = '' if not show_delete_selected else f'''
            <button type="button" id="{cid}_toolbar_delete" class="vl-ag-grid-toolbar__button" onclick="window.deleteSelectedRows_{cid} && window.deleteSelectedRows_{cid}()">Delete Selected</button>
            '''
            action_buttons_html = f"{delete_selected_button_html}{add_row_button_html}"
            toolbar_extra_actions_html = action_buttons_html if toolbar_config.get("enabled") else ""
            bottom_html = "" if toolbar_config.get("enabled") else action_buttons_html

            grid_style = self._build_ag_grid_theme_style(theme=current_theme, theme_colors=current_theme_colors)
            content_width = f"min(100%, {max(520, max(1, len(cols)) * 132)}px)"
            container_width = self._resolve_ag_grid_width(current_width, current_use_container_width, content_width)
            resolved_height = f"{int(current_height)}px" if isinstance(current_height, (int, float)) else str(current_height)
            toolbar_bind_config = {
                "apiKey": f"gridApi_{cid}",
                "surfaceId": f"{cid}_surface",
                "searchInputId": f"{cid}_toolbar_search" if toolbar_config.get("search") else None,
                "csvButtonId": f"{cid}_toolbar_csv" if toolbar_config.get("export_csv") else None,
                "fullscreenButtonId": f"{cid}_toolbar_fullscreen" if toolbar_config.get("fullscreen") else None,
                "fullscreenTargetId": f"{cid}_surface",
                "csvFileName": toolbar_config.get("csv_file_name", "data_editor.csv"),
            }
            grid_config_hash = hashlib.sha1(
                json.dumps(
                    {
                        "cols": cols,
                        "grid_options": extra_options,
                        "toolbar": toolbar_config,
                        "width": container_width,
                        "height": resolved_height,
                        "num_rows": current_num_rows,
                        "row_selection": selection_mode,
                        "delete_selected": show_delete_selected,
                        "disabled": editor_disabled,
                        "disabled_columns": sorted(disabled_columns),
                    },
                    sort_keys=True,
                    default=str,
                ).encode("utf-8")
            ).hexdigest()
            html = self._build_ag_grid_surface_html(
                cid=cid,
                height_css=resolved_height,
                width_css=container_width,
                grid_style=grid_style,
                toolbar_config=toolbar_config,
                toolbar_extra_actions_html=toolbar_extra_actions_html,
                bottom_html=bottom_html,
                grid_config_hash=grid_config_hash,
                script_body=f'''
                const rawColumnDefs = {json.dumps(cols, default=str)};
                const initialRowData = {json.dumps(data, default=str)};
                const extraGridOptions = {json.dumps(extra_options, default=str)};

                function moveCaretToEnd(input) {{
                    if (!input) {{
                        return;
                    }}
                    const currentValue = input.value || '';
                    requestAnimationFrame(() => {{
                        input.focus();
                        if (input.type !== 'number' && typeof input.setSelectionRange === 'function') {{
                            const length = currentValue.length;
                            input.setSelectionRange(length, length);
                        }}
                    }});
                }}

                class TextCellEditor {{
                    init(params) {{
                        this.eInput = document.createElement('input');
                        this.eInput.type = 'text';
                        this.eInput.className = 'ag-input-field-input ag-text-field-input';
                        this.eInput.style.width = '100%';
                        this.eInput.value = params.value ?? '';
                    }}
                    getGui() {{
                        return this.eInput;
                    }}
                    afterGuiAttached() {{
                        moveCaretToEnd(this.eInput);
                    }}
                    getValue() {{
                        return this.eInput.value;
                    }}
                    destroy() {{}}
                    isPopup() {{
                        return false;
                    }}
                }}

                class NumberCellEditor {{
                    init(params) {{
                        this.eInput = document.createElement('input');
                        this.eInput.type = 'number';
                        this.eInput.className = 'ag-input-field-input ag-text-field-input';
                        this.eInput.style.width = '100%';
                        if (params?.column?.colDef?.cellEditorParams) {{
                            const editorParams = params.column.colDef.cellEditorParams;
                            if (editorParams.min !== undefined && editorParams.min !== null) {{
                                this.eInput.min = editorParams.min;
                            }}
                            if (editorParams.max !== undefined && editorParams.max !== null) {{
                                this.eInput.max = editorParams.max;
                            }}
                            if (editorParams.step !== undefined && editorParams.step !== null) {{
                                this.eInput.step = editorParams.step;
                            }}
                        }}
                        this.eInput.value = params.value ?? '';
                    }}
                    getGui() {{
                        return this.eInput;
                    }}
                    afterGuiAttached() {{
                        moveCaretToEnd(this.eInput);
                    }}
                    getValue() {{
                        if (this.eInput.value === '') {{
                            return '';
                        }}
                        return Number(this.eInput.value);
                    }}
                    destroy() {{}}
                    isPopup() {{
                        return false;
                    }}
                }}

                class DateCellEditor {{
                    init(params) {{
                        this.eInput = document.createElement('input');
                        this.eInput.type = 'date';
                        this.eInput.className = 'ag-input-field-input ag-text-field-input';
                        this.eInput.style.width = '100%';
                        this.eInput.value = params.value || '';
                    }}
                    getGui() {{
                        return this.eInput;
                    }}
                    afterGuiAttached() {{
                        moveCaretToEnd(this.eInput);
                    }}
                    getValue() {{
                        return this.eInput.value;
                    }}
                    destroy() {{}}
                    isPopup() {{
                        return false;
                    }}
                }}

                function buildColumnDefs() {{
                    return rawColumnDefs.map((col) => {{
                        const def = {{ ...col }};
                        const editorType = def.__editorType || 'text';
                        const options = def.__options || [];
                        const numberMin = def.__numberMin;
                        const numberMax = def.__numberMax;
                        const numberStep = def.__numberStep;
                        delete def.__editorType;
                        delete def.__options;
                        delete def.__numberMin;
                        delete def.__numberMax;
                        delete def.__numberStep;

                        if (editorType === 'number') {{
                            def.cellEditor = NumberCellEditor;
                            def.cellEditorParams = {{
                                min: numberMin,
                                max: numberMax,
                                step: numberStep
                            }};
                        }} else if (editorType === 'select') {{
                            def.cellEditor = 'agSelectCellEditor';
                            def.cellEditorParams = {{ values: options }};
                        }} else if (editorType === 'checkbox' || editorType === 'boolean') {{
                            def.cellRenderer = 'agCheckboxCellRenderer';
                            def.cellEditor = 'agCheckboxCellEditor';
                            def.cellDataType = 'boolean';
                        }} else if (editorType === 'date') {{
                            def.cellEditor = DateCellEditor;
                        }} else {{
                            def.cellEditor = TextCellEditor;
                        }}

                        return def;
                    }});
                }}

                function initEditor() {{
                    const rowClickEnabled = {json.dumps(bool(on_row_click))};
                    const selectionMode = {json.dumps(selection_mode)};
                    const hasDeleteSelected = {json.dumps(show_delete_selected)};
                    const mergedGridOptions = {{ ...extraGridOptions }};

                    if (selectionMode) {{
                        mergedGridOptions.rowSelection = selectionMode;
                        if (selectionMode === 'multiple' && mergedGridOptions.suppressRowClickSelection === undefined) {{
                            mergedGridOptions.suppressRowClickSelection = true;
                        }}
                    }} else if (rowClickEnabled) {{
                        if (mergedGridOptions.singleClickEdit === undefined) {{
                            mergedGridOptions.singleClickEdit = false;
                        }}
                        if (mergedGridOptions.rowSelection === undefined) {{
                            mergedGridOptions.rowSelection = 'single';
                        }}
                    }}

                    function syncDeleteSelectedButtonState() {{
                        const deleteButton = document.getElementById('{cid}_toolbar_delete');
                        if (!deleteButton || !hasDeleteSelected) {{
                            return;
                        }}
                        const api = window['gridApi_{cid}'];
                        const selectedCount = api && typeof api.getSelectedNodes === 'function'
                            ? api.getSelectedNodes().filter(node => node && node.data).length
                            : 0;
                        const disabled = selectedCount === 0;
                        deleteButton.disabled = disabled;
                        deleteButton.setAttribute('aria-disabled', disabled ? 'true' : 'false');
                    }}

                    const gridOptions = {{
                        columnDefs: buildColumnDefs(),
                        rowData: initialRowData,
                        defaultColDef: {{ flex: 1, minWidth: 100, resizable: true, editable: {json.dumps(editable)} }},
                        suppressScrollOnNewData: true,
                        singleClickEdit: mergedGridOptions.singleClickEdit ?? true,
                        stopEditingWhenCellsLoseFocus: true,
                        onRowClicked: rowClickEnabled ? (params) => {{
                            const allData = [];
                            params.api.forEachNode(node => allData.push(node.data));
                            const payload = {{
                                eventType: 'row_click',
                                rowIndex: params.rowIndex,
                                rowData: params.data,
                                allData
                            }};
                            {f"sendAction('{cid}', payload);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(payload)}} , swap: 'none'}});"}
                        }} : undefined,
                        onCellValueChanged: (params) => {{
                            if (params.oldValue === params.newValue) {{
                                return;
                            }}
                            const allData = [];
                            params.api.forEachNode(node => allData.push(node.data));
                            const payload = {{
                                eventType: 'cell_change',
                                field: params.colDef.field,
                                rowIndex: params.rowIndex,
                                oldValue: params.oldValue,
                                newValue: params.newValue,
                                rowData: params.data,
                                allData
                            }};
                            {f"sendAction('{cid}', payload);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(payload)}} , swap: 'none'}});"}
                        }},
                        onSelectionChanged: selectionMode ? () => {{
                            syncDeleteSelectedButtonState();
                        }} : undefined,
                        onGridReady: (params) => {{
                            // Store API when grid is ready
                            window['gridApi_{cid}'] = params.api;
                            syncDeleteSelectedButtonState();
                        }},
                        ...mergedGridOptions
                    }};
                    const el = document.querySelector('#{cid}');
                    if (el && window.agGrid) {{
                        const gridApi = agGrid.createGrid(el, gridOptions);
                        window['gridApi_{cid}'] = gridApi;
                        if (window.violitRuntime && typeof window.violitRuntime.bindAgGridSurface === 'function') {{
                            window.violitRuntime.bindAgGridSurface({json.dumps(toolbar_bind_config)});
                        }}
                        syncDeleteSelectedButtonState();
                    }}

                    window.deleteSelectedRows_{cid} = function() {{
                        const api = window['gridApi_{cid}'];
                        if (!api || typeof api.getSelectedNodes !== 'function') {{
                            return;
                        }}

                        const selectedNodes = api.getSelectedNodes().filter(node => node && node.data);
                        if (!selectedNodes.length) {{
                            syncDeleteSelectedButtonState();
                            return;
                        }}

                        const selectedIndexSet = new Set(selectedNodes.map(node => Number(node.rowIndex)));
                        const selectedRows = selectedNodes.map(node => node.data);
                        const allData = [];
                        api.forEachNode(node => allData.push(node.data));
                        const remainingData = allData.filter((_row, index) => !selectedIndexSet.has(index));
                        const payload = {{
                            eventType: 'delete_selected',
                            selectedRows,
                            selectedRowIndexes: Array.from(selectedIndexSet.values()),
                            allData: remainingData,
                        }};
                        {f"sendAction('{cid}', payload);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(payload)}} , swap: 'none'}});"}
                    }};
                    
                    window.addDataRow_{cid} = function() {{
                        // Access stored grid API
                        const api = window['gridApi_{cid}'];
                        if (api && api.applyTransaction) {{
                            // Add empty row with all column fields
                            const newRow = {{}};
                            rawColumnDefs.forEach((col) => {{
                                if (Object.prototype.hasOwnProperty.call(col, 'defaultValue')) {{
                                    newRow[col.field] = col.defaultValue;
                                }} else if (col.__editorType === 'number') {{
                                    if (col.__numberMin !== undefined && col.__numberMin !== null) {{
                                        newRow[col.field] = Number(col.__numberMin);
                                    }} else {{
                                        newRow[col.field] = 0;
                                    }}
                                }} else if (col.__editorType === 'select') {{
                                    const options = Array.isArray(col.__options) ? col.__options : [];
                                    newRow[col.field] = options.length ? options[0] : '';
                                }} else if (col.__editorType === 'checkbox' || col.__editorType === 'boolean') {{
                                    newRow[col.field] = false;
                                }} else {{
                                    newRow[col.field] = '';
                                }}
                            }});
                            api.applyTransaction({{add: [newRow]}});
                            // Trigger data update to sync with backend
                            const allData = [];
                            api.forEachNode(node => allData.push(node.data));
                            const payload = {{ eventType: 'row_added', rowData: newRow, allData }};
                            {f"sendAction('{cid}', payload);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(payload)}} , swap: 'none'}});"}
                        }}
                    }};
                }}

                window._vlLoadLib('agGrid', function() {{
                    if (document.readyState === 'loading') {{
                        document.addEventListener('DOMContentLoaded', initEditor);
                    }} else {{
                        initEditor();
                    }}
                }});
                ''',
            )
            _wd = self._get_widget_defaults("data_editor")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def metric(self, label: str, value: Union[str, int, float, State, Callable], delta: Optional[Union[str, State, Callable]] = None, delta_color: str = "normal",
                help: str = None, label_visibility: str = "visible", border: bool = True,
                cls: str = "", style: str = "", height: Union[str, int, float] = "auto"):
        """Display metric value with Signal support"""
        import html as html_lib
        
        cid = self._get_next_cid("metric")
        
        def builder():
            # Handle value and delta signals in a single tracked block
            token = rendering_ctx.set(cid)
            try:
                curr_val = resolve_value(value)
                curr_delta = resolve_value(delta) if delta is not None else None
            finally:
                rendering_ctx.reset(token)

            # XSS protection: escape all values
            escaped_label = html_lib.escape(str(label))
            escaped_val = html_lib.escape(str(curr_val))

            # Help tooltip
            help_html = ""
            if help:
                import html as _h
                help_html = f' <wa-tooltip for="{cid}_help" content="{_h.escape(help)}"></wa-tooltip><wa-icon id="{cid}_help" name="circle-question" style="font-size:0.75em;vertical-align:middle;cursor:help;"></wa-icon>'

            # Label visibility
            label_style = ""
            if label_visibility == "hidden":
                label_style = "visibility:hidden;"
            elif label_visibility == "collapsed":
                label_style = "display:none;"

            delta_html = ""
            if curr_delta:
                escaped_delta = html_lib.escape(str(curr_delta))
                color_map = {"positive": "#10b981", "negative": "#ef4444", "normal": "var(--vl-text-muted)"}
                color = color_map.get(delta_color, "var(--vl-text-muted)")
                icon = "arrow-up" if delta_color == "positive" else "arrow-down" if delta_color == "negative" else ""
                icon_html = f'<wa-icon name="{icon}" style="font-size: 0.8em; margin-right: 2px;"></wa-icon>' if icon else ""
                delta_html = f'<div class="metric-delta" style="color: {color};">{icon_html}{escaped_delta}</div>'

            border_style = "border:1px solid var(--vl-border);border-radius:0.5rem;" if border else ""
            resolved_height = None
            if height not in (None, "", "auto"):
                if height == "fill":
                    resolved_height = "100%"
                elif isinstance(height, (int, float)):
                    resolved_height = f"{int(height)}px"
                else:
                    resolved_height = str(height)

            wrapper_style = f"height: {resolved_height};" if resolved_height else ""
            card_style = f"padding: 1.25rem;{border_style}"
            if resolved_height:
                card_style = f"{card_style}height: {resolved_height};"
            card_cls = merge_cls("card", "vl-metric-card", "vl-metric-card--fill" if height == "fill" else "")

            html_output = f'''
            <div class="{card_cls}" style="{card_style}">
                <div class="metric-label" style="{label_style}">{escaped_label}{help_html}</div>
                <div class="metric-value">{escaped_val}</div>
                {delta_html}
            </div>
            '''
            _wd = self._get_widget_defaults("metric")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), wrapper_style, style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
            
        self._register_component(cid, builder)

    def json(self, body: Any, expanded=True, cls: str = "", style: str = ""):
        """Display JSON data with Signal support"""
        cid = self._get_next_cid("json")
        
        def builder():
            from ..state import State, ComputedState
            import json as json_lib
            
            # Handle Signal
            current_body = body
            if isinstance(body, (State, ComputedState)):
                token = rendering_ctx.set(cid)
                current_body = body.value
                rendering_ctx.reset(token)
            elif callable(body):
                token = rendering_ctx.set(cid)
                current_body = body()
                rendering_ctx.reset(token)
                
            json_str = json_lib.dumps(current_body, indent=2, default=str)
            html = f'''
            <details {"open" if expanded else ""} style="background:var(--vl-bg-card);border:1px solid var(--vl-border);border-radius:0.5rem;padding:0.5rem;">
                <summary style="cursor:pointer;font-size:0.875rem;color:var(--vl-text-muted);">JSON Data</summary>
                <pre style="margin:0.5rem 0 0 0;font-size:0.875rem;color:var(--vl-primary);overflow-x:auto;">{json_str}</pre>
            </details>
            '''
            _wd = self._get_widget_defaults("json")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
            
        self._register_component(cid, builder)

    def heatmap(self, data: Union[dict, State, Callable], 
                start_date=None, end_date=None,
                color_map=None, show_legend=True, 
                show_weekdays=True, show_months=True,
                cell_size=12, gap=3, on_cell_clicked=None, cls: str = "", style: str = "", **props):
        """
        Display GitHub-style activity heatmap
        
        Args:
            data: Dict mapping date strings (YYYY-MM-DD) to values, or State/Callable
            start_date: Start date (string or date object)
            end_date: End date (string or date object)
            color_map: Dict mapping values to colors
                Example: {0: '#ebedf0', 1: '#10b981', 2: '#fbbf24'}
            show_legend: Show color legend
            show_weekdays: Show weekday labels
            show_months: Show month labels
            cell_size: Size of each cell in pixels
            gap: Gap between cells in pixels
            on_cell_clicked: Callback for cell clicks
        
        Example:
            app.heatmap(
                data={date: status for date, status in completions.items()},
                start_date='2026-01-01',
                end_date='2026-12-31',
                color_map={0: '#ebedf0', 1: '#10b981', 2: '#fbbf24'}
            )
        """
        from datetime import date as date_obj, timedelta
        
        cid = self._get_next_cid("heatmap")
        
        def action(v):
            """Handle cell click events"""
            if on_cell_clicked and callable(on_cell_clicked):
                on_cell_clicked(v)
        
        def builder():
            # Handle Signal/Callable
            current_data = data
            if isinstance(data, State):
                token = rendering_ctx.set(cid)
                current_data = data.value
                rendering_ctx.reset(token)
            elif callable(data):
                token = rendering_ctx.set(cid)
                current_data = data()
                rendering_ctx.reset(token)
            
            # Parse dates
            if start_date:
                if isinstance(start_date, str):
                    start = date_obj.fromisoformat(start_date)
                else:
                    start = start_date
            else:
                start = date_obj.today().replace(month=1, day=1)
            
            if end_date:
                if isinstance(end_date, str):
                    end = date_obj.fromisoformat(end_date)
                else:
                    end = end_date
            else:
                end = date_obj.today().replace(month=12, day=31)
            
            # Default color map (use current_color_map to avoid variable shadowing)
            current_color_map = color_map if color_map is not None else {
                0: '#ebedf0',
                1: '#10b981',
                2: '#fbbf24'
            }
            
            # Adjust start to Sunday
            start_day = start - timedelta(days=start.weekday() + 1 if start.weekday() != 6 else 0)
            
            # Generate week data
            weeks = []
            current = start_day
            
            while current <= end:
                week = []
                for _ in range(7):
                    if start <= current <= end:
                        date_str = current.isoformat()
                        value = current_data.get(date_str, 0)
                        week.append({'date': current, 'value': value, 'valid': True})
                    else:
                        week.append({'date': current, 'value': 0, 'valid': False})
                    current += timedelta(days=1)
                weeks.append(week)
            
            # CSS
            css = f'''
            <style>
            .heatmap-{cid} {{
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                overflow-x: auto;
            }}
            .heatmap-{cid} .grid {{
                display: flex;
                gap: {gap}px;
            }}
            .heatmap-{cid} .weekdays {{
                display: flex;
                flex-direction: column;
                gap: {gap}px;
                padding-top: 20px;
                margin-right: 4px;
            }}
            .heatmap-{cid} .day-label {{
                height: {cell_size}px;
                font-size: 9px;
                color: #666;
                display: flex;
                align-items: center;
            }}
            .heatmap-{cid} .week {{
                display: flex;
                flex-direction: column;
                gap: {gap}px;
            }}
            .heatmap-{cid} .month {{
                height: 14px;
                font-size: 9px;
                color: #666;
                text-align: center;
                margin-bottom: 2px;
            }}
            .heatmap-{cid} .cell {{
                width: {cell_size}px;
                height: {cell_size}px;
                border-radius: 2px;
                border: 1px solid #fff;
                cursor: pointer;
            }}
            .heatmap-{cid} .cell:hover {{
                opacity: 0.8;
                border: 1px solid #000;
            }}
            .heatmap-{cid} .cell.today {{
                border: 2px solid #000;
            }}
            .heatmap-{cid} .legend {{
                margin-top: 1rem;
                display: flex;
                gap: 1rem;
                font-size: 11px;
                color: #666;
                align-items: center;
            }}
            .heatmap-{cid} .legend-item {{
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            </style>
            '''
            
            # Weekday labels
            weekday_html = ''
            if show_weekdays:
                weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
                weekday_html = f'''
                <div class="weekdays">
                    {"".join(f'<div class="day-label">{d}</div>' for d in weekdays)}
                </div>
                '''
            
            # Generate weeks HTML
            today = date_obj.today()
            current_month = None
            weeks_html = []
            
            for week in weeks:
                # Month label
                first_valid = next((d for d in week if d['valid']), None)
                if first_valid and show_months:
                    month = first_valid['date'].month
                    month_label = f"{month}" if month != current_month else ""
                    current_month = month
                else:
                    month_label = ""
                
                # Cells
                cells_html = []
                for day in week:
                    if not day['valid']:
                        cells_html.append(f'<div style="width: {cell_size}px; height: {cell_size}px;"></div>')
                    else:
                        value = day['value']
                        bg_color = current_color_map.get(value, '#ebedf0')
                        is_today = day['date'] == today
                        today_class = ' today' if is_today else ''
                        date_str = day['date'].isoformat()
                        
                        # Click handler
                        click_attr = ''
                        if on_cell_clicked:
                            click_js = f"window.sendAction('{cid}', {{date: '{date_str}', value: {value}}});" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify({{date: '{date_str}', value: {value}}})}}), swap: 'none'}});"
                            click_attr = f'onclick="{click_js}"'
                        
                        cells_html.append(
                            f'<div class="cell{today_class}" style="background: {bg_color};" title="{date_str}" {click_attr}></div>'
                        )
                
                weeks_html.append(f'''
                <div class="week">
                    <div class="month">{month_label}</div>
                    {"".join(cells_html)}
                </div>
                ''')
            
            # Legend
            legend_html = ''
            if show_legend:
                legend_items = [
                    f'''<div class="legend-item">
                        <div class="cell" style="background: {color}; border: 1px solid #ddd;"></div>
                        <span>{label}</span>
                    </div>'''
                    for label, color in [('None', current_color_map.get(0, '#ebedf0')), 
                                         ('Done', current_color_map.get(1, '#10b981')), 
                                         ('Skip', current_color_map.get(2, '#fbbf24'))]
                    if color in current_color_map.values()
                ]
                legend_html = f'''
                <div class="legend">
                    <span>Legend:</span>
                    {"".join(legend_items)}
                </div>
                '''
            
            # Final HTML
            html = f'''
            {css}
            <div class="heatmap-{cid}">
                <div class="grid">
                    {weekday_html}
                    <div style="display: flex; gap: {gap}px;">
                        {"".join(weeks_html)}
                    </div>
                </div>
                {legend_html}
            </div>
            '''
            
            _wd = self._get_widget_defaults("heatmap")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action if on_cell_clicked else None)
