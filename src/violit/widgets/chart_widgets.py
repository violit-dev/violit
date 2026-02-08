"""Chart Widgets Mixin for Violit"""

from typing import Union, Optional, Any, Callable
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from ..component import Component
from ..context import rendering_ctx, initial_render_ctx
from ..state import State, get_session_store
from ..style_utils import merge_cls, merge_style


# [OPTIMIZED] Plotly render script with fast updates
# - Uses Plotly.newPlot for first render, Plotly.react for updates
# - Single rAF instead of double (saves ~16ms)
# - Hidden containers still defer via IntersectionObserver
_PLOTLY_RENDER_SCRIPT = """
<script>(function(){{
    var d = {fj};
    var cid = '{cid}';
    var cfg = {{responsive: true, displayModeBar: false}};

    function _vlDraw() {{
        var el = document.getElementById(cid);
        if (!el || !window.Plotly) return;
        d.layout.autosize = true;
        delete d.layout.width;
        // Use newPlot for first render, react for updates
        if (el.hasAttribute('data-plotly-init')) {{
            Plotly.react(cid, d.data, d.layout, cfg);
        }} else {{
            el.setAttribute('data-plotly-init', '1');
            Plotly.newPlot(cid, d.data, d.layout, cfg);
        }}
    }}

    function _vlSchedule() {{
        requestAnimationFrame(_vlDraw);
    }}

    function initPlot() {{
        var el = document.getElementById(cid);
        if (!el) return;

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

    // Ensure DOM is ready before initializing
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initPlot);
    }} else {{
        initPlot();
    }}
}})();</script>
"""

# Threshold for asynchronous data loading (number of data points)
# Large figures are deferred until the page is loaded to ensure O(1) initial page load
_ASYNC_CHART_THRESHOLD = 50000


class ChartWidgetsMixin:
    """Chart widgets (line, bar, area, scatter, plotly, pyplot, etc.)"""
    
    def plotly_chart(self, fig: Union[go.Figure, Callable, State], use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display Plotly chart with Signal/Lambda support"""
        cid = self._get_next_cid("plot")
        
        def builder():
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
                <div id="{cid}" class="js-plotly-plot" style="{width_style} height: 500px; display: flex; align-items: center; justify-content: center; background: var(--sl-bg-card); border: 1px solid var(--sl-border); border-radius: var(--sl-radius);">
                    <div style="text-align: center;">
                        <sl-spinner style="font-size: 2rem; --indicator-color: var(--sl-primary); margin-bottom: 0.75rem;"></sl-spinner>
                        <div style="font-size: 0.85rem; color: var(--sl-text-muted); font-weight: 500;">Loading dataset ({data_points:,} points)...</div>
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
                store = get_session_store()
                if 'forced_dirty' not in store:
                    store['forced_dirty'] = set()
                store['forced_dirty'].add(cid)

        self._register_component(cid, builder, action=action)


    def pyplot(self, fig=None, use_container_width=True, cls: str = "", style: str = "", **props):
        """Display Matplotlib figure"""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import io
        import base64
        
        cid = self._get_next_cid("pyplot")
        
        def builder():
            current_fig = fig if fig is not None else plt.gcf()
            
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

    def line_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display simple line chart"""
        cid = self._get_next_cid("line_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(trace_cls(x=x_data, y=y_data, mode='lines+markers', name=trace_name))
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
        
        self._register_component(cid, builder)

    def bar_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display simple bar chart"""
        cid = self._get_next_cid("bar_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=x_data, y=y_data, name=trace_name))
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
        
        self._register_component(cid, builder)

    def area_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display area chart"""
        cid = self._get_next_cid("area_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(trace_cls(x=x_data, y=y_data, fill='tozeroy', name=trace_name))
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
        
        self._register_component(cid, builder)

    def scatter_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", cls: str = "", style: str = "", **props):
        """Display scatter chart"""
        cid = self._get_next_cid("scatter_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(trace_cls(x=x_data, y=y_data, mode='markers', name=trace_name))
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
        
        self._register_component(cid, builder)

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

    def _parse_chart_data(self, data, x, y):
        """Parse chart data into x, y, and trace name"""
        if isinstance(data, pd.DataFrame):
            if x and y:
                x_data = data[x].tolist()
                y_data = data[y].tolist()
                trace_name = y
            elif y:
                x_data = list(range(len(data)))
                y_data = data[y].tolist()
                trace_name = y
            else:
                cols = data.columns.tolist()
                x_data = data[cols[0]].tolist()
                y_data = data[cols[1]].tolist() if len(cols) > 1 else list(range(len(data)))
                trace_name = cols[1] if len(cols) > 1 else 'Value'
        elif isinstance(data, (list, tuple)):
            x_data = list(range(len(data)))
            y_data = list(data)
            trace_name = 'Value'
        else:
            x_data = []
            y_data = []
            trace_name = 'Value'
        
        return x_data, y_data, trace_name
