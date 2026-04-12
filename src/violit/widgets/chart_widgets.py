"""Chart Widgets Mixin for Violit"""

from typing import Union, Optional, Any, Callable
from ..component import Component
from ..context import rendering_ctx, initial_render_ctx
from ..state import State, get_session_store
from ..style_utils import merge_cls, merge_style


# [OPTIMIZED] Plotly render script with fast updates
# - Uses global Set (window._vlPlotlyInited) instead of DOM attribute
#   This survives outerHTML replacement, preventing flicker on reactive updates
# - Already-initialized charts skip clientWidth check and IntersectionObserver delay
# - Uses Plotly.react() for updates (no two-pass sizing = no flicker)
_PLOTLY_RENDER_SCRIPT = """
<script>(function(){{
    var d = {fj};
    var cid = '{cid}';
    var cfg = {{responsive: true, displayModeBar: false}};

    if (!window._vlPlotlyInited) window._vlPlotlyInited = new Set();

    function _vlDraw() {{
        var el = document.getElementById(cid);
        if (!el || !window.Plotly) return;
        d.layout.autosize = true;
        delete d.layout.width;
        delete d.layout.height;
        if (window._vlPlotlyInited.has(cid)) {{
            Plotly.react(cid, d.data, d.layout, cfg);
        }} else {{
            window._vlPlotlyInited.add(cid);
            Plotly.newPlot(cid, d.data, d.layout, cfg);
        }}
    }}

    function _vlSchedule() {{
        requestAnimationFrame(_vlDraw);
    }}

    function initPlot() {{
        var el = document.getElementById(cid);
        if (!el) return;

        if (window._vlPlotlyInited.has(cid)) {{
            _vlSchedule();
            return;
        }}

        if (el.clientWidth < 10) {{
            var io = new IntersectionObserver(function(entries) {{
                if (entries[0].isIntersecting && entries[0].boundingClientRect.width > 10) {{
                    io.disconnect();
                    _vlSchedule();
                }}
            }});
            io.observe(el);
        }} else {{
            _vlSchedule();
        }}
    }}

    // Wait for Plotly library to load (lazy loaded)
    window._vlLoadLib('Plotly', function() {{
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initPlot);
        }} else {{
            initPlot();
        }}
    }});
}})();</script>
"""

# Threshold for asynchronous data loading (number of data points)
# Large figures are deferred until the page is loaded to ensure fine-grained reactivity initial page load
_ASYNC_CHART_THRESHOLD = 50000


class ChartWidgetsMixin:
    """Chart widgets (line, bar, area, scatter, plotly, pyplot, etc.)"""

    def _chart_should_defer_first_render(self, cid):
        if getattr(self, 'mode', None) != 'ws':
            return False

        store = get_session_store()
        requested = store.setdefault('_vl_chart_requested', set())
        return cid not in requested

    def _chart_mark_requested(self, cid):
        store = get_session_store()
        store.setdefault('_vl_chart_requested', set()).add(cid)
        store.setdefault('forced_dirty', set()).add(cid)

    def _chart_placeholder_component(self, cid, widget_name, height, use_container_width, cls, style, message):
        width_style = "width: 100%;" if use_container_width else ""
        html = f'''
        <div id="{cid}" class="js-plotly-plot" data-vl-deferred-chart="true" style="{width_style} height: {height}px; display: flex; align-items: center; justify-content: center; background: var(--vl-bg-card); border: 1px solid var(--vl-border); border-radius: var(--vl-radius);">
            <div style="text-align: center;">
                <wa-spinner style="font-size: 1.5rem; margin-bottom: 0.75rem;"></wa-spinner>
                <div style="font-size: 0.85rem; color: var(--vl-text-muted); font-weight: 500;">{message}</div>
            </div>
        </div>
        <script>
            (function() {{
                const chartId = '{cid}';

                if (!window._vlDeferredChartsRequested) {{
                    window._vlDeferredChartsRequested = new Set();
                }}

                const requestHydration = () => {{
                    if (window._vlDeferredChartsRequested.has(chartId)) return;

                    const el = document.getElementById(chartId);
                    if (!el) return;

                    window._vlDeferredChartsRequested.add(chartId);

                    if (window._vlPreloadLib) window._vlPreloadLib('Plotly');

                    if (window._vlQueueDeferredAction) {{
                        window._vlQueueDeferredAction(chartId, '__REQUEST_DATA__');
                    }} else if (window.sendAction) {{
                        window.sendAction(chartId, '__REQUEST_DATA__');
                    }}
                }};

                const observeVisibility = () => {{
                    const el = document.getElementById(chartId);
                    if (!el) {{
                        setTimeout(observeVisibility, 50);
                        return;
                    }}

                    if (window._vlPreloadLib) window._vlPreloadLib('Plotly');

                    if (!('IntersectionObserver' in window)) {{
                        requestHydration();
                        return;
                    }}

                    const io = new IntersectionObserver((entries) => {{
                        const entry = entries[0];
                        if (!entry) return;
                        if (entry.isIntersecting || entry.boundingClientRect.top < window.innerHeight + 240) {{
                            io.disconnect();
                            requestHydration();
                        }}
                    }}, {{ rootMargin: '240px 0px 320px 0px' }});

                    io.observe(el);
                }};

                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', observeVisibility, {{ once: true }});
                }} else {{
                    observeVisibility();
                }}
            }})();
        </script>
        '''
        _wd = self._get_widget_defaults(widget_name)
        _fc = merge_cls(_wd.get("cls", ""), cls)
        _fs = merge_style(_wd.get("style", ""), style)
        return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
    
    def plotly_chart(self, fig: Union['go.Figure', Callable, State], use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display Plotly chart with Signal/Lambda support"""
        cid = self._get_next_cid("plot")
        
        def builder():
            if self._chart_should_defer_first_render(cid):
                return self._chart_placeholder_component(
                    cid,
                    "plotly_chart",
                    500,
                    use_container_width,
                    cls,
                    style,
                    "Preparing Plotly chart...",
                )

            import plotly.graph_objects as go
            import plotly.io as pio
            # Handle Signal/Lambda/Direct Figure
            current_fig = fig
            if isinstance(fig, State):
                token = rendering_ctx.set(cid)
                current_fig = fig.value
                rendering_ctx.reset(token)
            elif callable(fig):
                token = rendering_ctx.set(cid)
                current_fig = fig()
                rendering_ctx.reset(token)
            
            if current_fig is None:
                return Component("div", id=f"{cid}_wrapper", content="No data")

            # [OPTIMIZATION] Automatically lighten large figures to reduce JSON size (Transport Bottleneck)
            data_points = 0
            if hasattr(current_fig, "data"):
                import numpy as np
                for trace in current_fig.data:
                    # Rounding massive arrays to 4 decimals reduces JSON size by ~60% with no visual loss
                    if hasattr(trace, "y") and trace.y is not None:
                        count = len(trace.y)
                        data_points += count
                        if count > 50000:
                            trace.update(y=np.round(trace.y, 4))
                    if hasattr(trace, "x") and trace.x is not None:
                        if len(trace.x) > 50000:
                            trace.update(x=np.round(trace.x, 4))

            # [OPTIMIZATION] Async load large figures on initial page load
            # This ensures the first HTML response is small and the splash screen appears instantly.
            if initial_render_ctx.get() and data_points > _ASYNC_CHART_THRESHOLD:
                width_style = "width: 100%;" if use_container_width else ""
                html = f'''
                <div id="{cid}" class="js-plotly-plot" style="{width_style} height: 500px; display: flex; align-items: center; justify-content: center; background: var(--vl-bg-card); border: 1px solid var(--vl-border); border-radius: var(--vl-radius);">
                    <div style="text-align: center;">
                        <wa-spinner style="font-size: 2rem; margin-bottom: 0.75rem;"></wa-spinner>
                        <div style="font-size: 0.85rem; color: var(--vl-text-muted); font-weight: 500;">Loading dataset ({data_points:,} points)...</div>
                    </div>
                </div>
                <script>
                    (function() {{
                        const check = () => {{
                            if (window.sendAction) {{
                                window.sendAction('{cid}', '__REQUEST_DATA__');
                            }} else {{
                                setTimeout(check, 50);
                            }}
                        }};
                        check();
                    }})();
                </script>
                '''
                _wd = self._get_widget_defaults("plotly_chart")
                _fc = merge_cls(_wd.get("cls", ""), cls)
                _fs = merge_style(_wd.get("style", ""), style)
                return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)

            # Force render_mode if requested (default: svg)
            if render_mode == "svg" and hasattr(current_fig, "data"):
                has_scattergl = any(trace.type == 'scattergl' for trace in current_fig.data)
                if has_scattergl:
                    # Create new figure with converted traces
                    new_traces = []
                    for trace in current_fig.data:
                        if trace.type == 'scattergl':
                            trace_dict = trace.to_plotly_json()
                            trace_dict['type'] = 'scatter'
                            new_traces.append(go.Scatter(trace_dict))
                        else:
                            new_traces.append(trace)
                    # Recreate figure with new traces and original layout
                    current_fig = go.Figure(data=new_traces, layout=current_fig.layout)
                
            fj = pio.to_json(current_fig)
            width_style = "width: 100%;" if use_container_width else ""
            html = f'''
            <div id="{cid}" class="js-plotly-plot" style="{width_style} height: 500px;"></div>
            ''' + _PLOTLY_RENDER_SCRIPT.format(fj=fj, cid=cid)
            _wd = self._get_widget_defaults("plotly_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
            
        def action(val):
            if val == '__REQUEST_DATA__':
                self._chart_mark_requested(cid)

        self._register_component(cid, builder, action=action)


    def pyplot(self, fig=None, use_container_width=True, cls: str = "", style: str = "", **props):
        """Display Matplotlib figure"""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        from matplotlib.text import Text
        import io
        import base64
        import sys

        # Set Korean font defaults for Matplotlib
        selected_font = None
        try:
            from matplotlib import rc
            if sys.platform == 'win32':
                # Windows fonts
                fonts = ['Malgun Gothic', 'NanumGothic', 'NanumSquare']
            elif sys.platform == 'darwin':
                # macOS fonts
                fonts = ['AppleGothic', 'NanumGothic', 'NanumSquare']
            else:
                # Linux/other
                fonts = ['NanumGothic', 'DejaVu Sans']
            
            # Find first available font
            available_fonts = [f.name for f in font_manager.fontManager.ttflist]
            for font in fonts:
                if font in available_fonts:
                    rc('font', family=font)
                    selected_font = font
                    break
            
            # Fix minus sign display issue
            matplotlib.rcParams['axes.unicode_minus'] = False
        except Exception:
            pass
        
        cid = self._get_next_cid("pyplot")
        
        def builder():
            current_fig = fig if fig is not None else plt.gcf()

            if selected_font:
                try:
                    font_props = font_manager.FontProperties(family=selected_font)
                    for text_artist in current_fig.findobj(match=lambda artist: isinstance(artist, Text)):
                        text_artist.set_fontproperties(font_props)
                except Exception:
                    pass
            
            buf = io.BytesIO()
            current_fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            
            width_style = "width: 100%;" if use_container_width else ""
            html = f'<img src="data:image/png;base64,{img_base64}" style="{width_style} height: auto;" />'
            _wd = self._get_widget_defaults("pyplot")
            _fc = merge_cls(_wd.get("cls", ""), "pyplot-container", cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc, style=_fs or None)
        
        self._register_component(cid, builder)

    def line_chart(self, data, x=None, y=None, color=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display simple line chart"""
        cid = self._get_next_cid("line_chart")
        
        def builder():
            if self._chart_should_defer_first_render(cid):
                return self._chart_placeholder_component(
                    cid,
                    "line_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing line chart...",
                )

            import plotly.graph_objects as go
            import plotly.io as pio
            traces = self._parse_chart_data(data, x, y, color=color)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            for t in traces:
                fig.add_trace(trace_cls(x=t['x'], y=t['y'], mode='lines+markers', name=t['name']))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" class="js-plotly-plot" style="{container_width} height: {height}px;"></div>
            ''' + _PLOTLY_RENDER_SCRIPT.format(fj=fj, cid=cid)
            _wd = self._get_widget_defaults("line_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        def action(val):
            if val == '__REQUEST_DATA__':
                self._chart_mark_requested(cid)

        self._register_component(cid, builder, action=action)

    def bar_chart(self, data, x=None, y=None, color=None, horizontal=False, stack=False, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display simple bar chart"""
        cid = self._get_next_cid("bar_chart")
        
        def builder():
            if self._chart_should_defer_first_render(cid):
                return self._chart_placeholder_component(
                    cid,
                    "bar_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing bar chart...",
                )

            import plotly.graph_objects as go
            import plotly.io as pio
            traces = self._parse_chart_data(data, x, y, color=color)
            
            fig = go.Figure()
            for t in traces:
                if horizontal:
                    fig.add_trace(go.Bar(x=t['y'], y=t['x'], name=t['name'], orientation='h'))
                else:
                    fig.add_trace(go.Bar(x=t['x'], y=t['y'], name=t['name']))
            if stack:
                fig.update_layout(barmode='stack')
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" class="js-plotly-plot" style="{container_width} height: {height}px;"></div>
            ''' + _PLOTLY_RENDER_SCRIPT.format(fj=fj, cid=cid)
            _wd = self._get_widget_defaults("bar_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        def action(val):
            if val == '__REQUEST_DATA__':
                self._chart_mark_requested(cid)

        self._register_component(cid, builder, action=action)

    def area_chart(self, data, x=None, y=None, color=None, stack=False, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display area chart"""
        cid = self._get_next_cid("area_chart")
        
        def builder():
            if self._chart_should_defer_first_render(cid):
                return self._chart_placeholder_component(
                    cid,
                    "area_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing area chart...",
                )

            import plotly.graph_objects as go
            import plotly.io as pio
            traces = self._parse_chart_data(data, x, y, color=color)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            for t in traces:
                fill_kw = {'stackgroup': 'one'} if stack else {'fill': 'tozeroy'}
                fig.add_trace(trace_cls(x=t['x'], y=t['y'], name=t['name'], **fill_kw))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" class="js-plotly-plot" style="{container_width} height: {height}px;"></div>
            ''' + _PLOTLY_RENDER_SCRIPT.format(fj=fj, cid=cid)
            _wd = self._get_widget_defaults("area_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        def action(val):
            if val == '__REQUEST_DATA__':
                self._chart_mark_requested(cid)

        self._register_component(cid, builder, action=action)

    def scatter_chart(self, data, x=None, y=None, color=None, size=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display scatter chart"""
        cid = self._get_next_cid("scatter_chart")
        
        def builder():
            if self._chart_should_defer_first_render(cid):
                return self._chart_placeholder_component(
                    cid,
                    "scatter_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing scatter chart...",
                )

            import plotly.graph_objects as go
            import plotly.io as pio
            traces = self._parse_chart_data(data, x, y, color=color)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            for t in traces:
                marker_kw = {}
                if size and isinstance(data, __import__('pandas').DataFrame) and size in data.columns:
                    marker_kw['size'] = data[size].tolist()
                fig.add_trace(trace_cls(x=t['x'], y=t['y'], mode='markers', name=t['name'], marker=marker_kw or None))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" class="js-plotly-plot" style="{container_width} height: {height}px;"></div>
            ''' + _PLOTLY_RENDER_SCRIPT.format(fj=fj, cid=cid)
            _wd = self._get_widget_defaults("scatter_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=f"{cid}_wrapper", content=html, class_=_fc or None, style=_fs or None)
        
        def action(val):
            if val == '__REQUEST_DATA__':
                self._chart_mark_requested(cid)

        self._register_component(cid, builder, action=action)

    def bokeh_chart(self, figure, use_container_width=True, cls: str = "", style: str = "", **props):
        """Display Bokeh chart"""
        from bokeh.embed import components
        
        cid = self._get_next_cid("bokeh_chart")
        
        def builder():
            script, div = components(figure)
            width_style = "width: 100%;" if use_container_width else ""
            html = f'''
            <div style="{width_style}">
                {div}
                {script}
            </div>
            '''
            _wd = self._get_widget_defaults("bokeh_chart")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def _parse_chart_data(self, data, x, y, color=None):
        """Parse chart data into list of trace dicts [{x, y, name}, ...]
        
        Supports multi-series via:
        - color param: column name to group by for multiple traces
        - y as list: multiple y columns become separate traces
        """
        import pandas as pd
        if isinstance(data, pd.DataFrame):
            # Determine x column
            cols = data.columns.tolist()
            if x:
                x_col = x
            else:
                x_col = cols[0] if len(cols) > 1 else None

            # Multi-series via color (group-by column)
            if color and color in data.columns:
                traces = []
                x_src = x_col or cols[0]
                y_src = y or (cols[1] if len(cols) > 1 else cols[0])
                for group_val, group_df in data.groupby(color):
                    traces.append({
                        'x': group_df[x_src].tolist(),
                        'y': group_df[y_src].tolist(),
                        'name': str(group_val)
                    })
                return traces

            # Multi-series via y as list
            if isinstance(y, (list, tuple)):
                x_data = data[x_col].tolist() if x_col else list(range(len(data)))
                return [{'x': x_data, 'y': data[col].tolist(), 'name': col} for col in y if col in data.columns]

            # Single series
            if x and y:
                return [{'x': data[x].tolist(), 'y': data[y].tolist(), 'name': y}]
            elif y:
                return [{'x': list(range(len(data))), 'y': data[y].tolist(), 'name': y}]
            else:
                x_data = data[cols[0]].tolist()
                y_data = data[cols[1]].tolist() if len(cols) > 1 else list(range(len(data)))
                name = cols[1] if len(cols) > 1 else 'Value'
                return [{'x': x_data, 'y': y_data, 'name': name}]
        elif isinstance(data, (list, tuple)):
            return [{'x': list(range(len(data))), 'y': list(data), 'name': 'Value'}]
        else:
            return [{'x': [], 'y': [], 'name': 'Value'}]
