"""Data Widgets Mixin for Violit"""

from typing import Union, Callable, Optional, Any
import json
from ..component import Component
from ..context import rendering_ctx
from ..state import State
from ..style_utils import merge_cls, merge_style, resolve_value


class DataWidgetsMixin:
    """Data display widgets (dataframe, table, data_editor, metric, json)"""
    
    def dataframe(self, df: Union['pd.DataFrame', Callable, State], height=400, 
                  column_defs=None, grid_options=None, on_cell_clicked=None,
                  use_container_width=True, hide_index=False, column_order=None,
                  cls: str = "", style: str = "", **props):
        """Display interactive dataframe with AG Grid"""
        cid = self._get_next_cid("df")
        
        def action(v):
            """Handle cell click events"""
            if on_cell_clicked and callable(on_cell_clicked):
                on_cell_clicked(v)
        
        def builder():
            import pandas as pd
            # Handle Signal
            token = rendering_ctx.set(cid)
            try:
                current_df = resolve_value(df)
            finally:
                rendering_ctx.reset(token)
                
            if not isinstance(current_df, pd.DataFrame):
                # Fallback or try to convert
                try: current_df = pd.DataFrame(current_df)
                except: return Component("div", id=cid, content="Invalid data format")

            data = current_df.to_dict('records')
            
            # Apply column_order if specified
            if column_order:
                ordered = [c for c in column_order if c in current_df.columns]
                current_df = current_df[ordered]

            # Optionally hide index
            if hide_index and current_df.index.name:
                current_df = current_df.reset_index(drop=True)

            # Use custom column_defs or generate defaults
            if column_defs:
                cols = column_defs
            else:
                cols = [{"field": c, "sortable": True, "filter": True} for c in current_df.columns]
            
            # Merge grid_options
            extra_options = grid_options or {}
            
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
            
            html = f'''
            <div id="{cid}" style="height: {height}px; width: 100%;" class="ag-theme-alpine-dark"></div>
            <script>(function(){{
                function initGrid() {{
                    const opt = {{ 
                        columnDefs: {json.dumps(cols, default=str)}, 
                        rowData: {json.dumps(data, default=str)},
                        defaultColDef: {{flex: 1, minWidth: 100, resizable: true}},
                        {cell_click_handler}
                        ...{json.dumps(extra_options)}
                    }};
                    const el = document.querySelector('#{cid}');
                    if (el && window.agGrid) {{ 
                        const gridApi = agGrid.createGrid(el, opt);
                        window['gridApi_{cid}'] = gridApi;
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
            }})();</script>
            '''
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
                        background: var(--vl-primary);
                        color: white;
                    }}
                    .data-table th, .data-table td {{
                        padding: 0.75rem;
                        text-align: left;
                        border-bottom: 1px solid var(--vl-border);
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
                    disabled=False, hide_index=False, column_order=None, use_container_width=True,
                    cls: str = "", style: str = "", **props):
        """Interactive data editor (simplified version)"""
        import pandas as pd
        cid = self._get_next_cid("data_editor")
        
        state_key = key or f"data_editor:{cid}"
        s = self.state(df.to_dict('records'), key=state_key)
        
        def action(v):
            try:
                new_data = json.loads(v) if isinstance(v, str) else v
                s.set(new_data)
                if on_change: on_change(pd.DataFrame(new_data))
            except: pass
        
        def builder():
            # Subscribe to own state - client-side will handle smart updates
            token = rendering_ctx.set(cid)
            data = s.value
            rendering_ctx.reset(token)
            
            # Apply column_order and hide_index
            _cols_list = list(df.columns)
            if column_order:
                _cols_list = [c for c in column_order if c in _cols_list]
            editable = not disabled
            cols = [{"field": c, "sortable": True, "filter": True, "editable": editable} for c in _cols_list]
            add_row_btn = '' if num_rows == "fixed" else f'''
            <wa-button size="small" appearance="outlined" with-start style="margin-top:0.5rem;" onclick="addDataRow_{cid}()">
                <wa-icon slot="start" name="circle-plus"></wa-icon>
                Add Row
            </wa-button>
            '''
            
            html = f'''
            <div>
                <div id="{cid}" style="height: {height}px; width: 100%;" class="ag-theme-alpine-dark"></div>
                {add_row_btn}
            </div>
            <script>(function(){{
                function initEditor() {{
                    const gridOptions = {{
                        columnDefs: {json.dumps(cols, default=str)},
                        rowData: {json.dumps(data, default=str)},
                        defaultColDef: {{ flex: 1, minWidth: 100, resizable: true, editable: true }},
                        onCellValueChanged: (params) => {{
                            const allData = [];
                            params.api.forEachNode(node => allData.push(node.data));
                            {f"sendAction('{cid}', allData);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(allData)}} , swap: 'none'}});"}
                        }},
                        onGridReady: (params) => {{
                            // Store API when grid is ready
                            window['gridApi_{cid}'] = params.api;
                        }}
                    }};
                    const el = document.querySelector('#{cid}');
                    if (el && window.agGrid) {{
                        const gridApi = agGrid.createGrid(el, gridOptions);
                        window['gridApi_{cid}'] = gridApi;
                    }}
                    
                    window.addDataRow_{cid} = function() {{
                        // Access stored grid API
                        const api = window['gridApi_{cid}'];
                        if (api && api.applyTransaction) {{
                            // Add empty row with all column fields
                            const newRow = {{}};
                            {json.dumps([c for c in df.columns])}.forEach(col => newRow[col] = '');
                            api.applyTransaction({{add: [newRow]}});
                            // Trigger data update to sync with backend
                            const allData = [];
                            api.forEachNode(node => allData.push(node.data));
                            {f"sendAction('{cid}', allData);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(allData)}} , swap: 'none'}});"}
                        }}
                    }};
                }}

                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', initEditor);
                }} else {{
                    initEditor();
                }}
            }})();</script>
            '''
            _wd = self._get_widget_defaults("data_editor")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def metric(self, label: str, value: Union[str, int, float, State, Callable], delta: Optional[Union[str, State, Callable]] = None, delta_color: str = "normal",
                help: str = None, label_visibility: str = "visible", border: bool = True,
                cls: str = "", style: str = ""):
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
                delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.25rem; font-weight: 500;">{icon_html}{escaped_delta}</div>'

            border_style = "border:1px solid var(--vl-border);border-radius:0.5rem;" if border else ""

            html_output = f'''
            <div class="card" style="padding: 1.25rem;{border_style}">
                <div style="font-size: 0.875rem; color: var(--vl-text-muted); margin-bottom: 0.5rem; font-weight: 500;{label_style}">{escaped_label}{help_html}</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: var(--vl-text);">{escaped_val}</div>
                {delta_html}
            </div>
            '''
            _wd = self._get_widget_defaults("metric")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
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
