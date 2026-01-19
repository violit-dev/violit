"""Chart Widgets Mixin for Violit"""

from typing import Union, Optional, Any, Callable
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from ..component import Component
from ..context import rendering_ctx
from ..state import State


class ChartWidgetsMixin:
    """Chart widgets (line, bar, area, scatter, plotly, pyplot, etc.)"""
    
    def plotly_chart(self, fig: Union[go.Figure, Callable, State], use_container_width=True, render_mode="svg", **props):
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

            # Force render_mode if requested (default: svg)
            # Convert scattergl to scatter for SVG rendering
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
            <div id="{cid}" style="{width_style} height: 500px;"></div>
            <script>(function(){{
                const d = {fj};
                if (window.Plotly) {{
                    Plotly.newPlot('{cid}', d.data, d.layout, {{responsive: true}});
                }} else {{
                    console.error("Plotly not found");
                }}
            }})();</script>
            '''
            return Component("div", id=f"{cid}_wrapper", content=html)
            
        self._register_component(cid, builder)


    def pyplot(self, fig=None, use_container_width=True, **props):
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
            return Component("div", id=cid, content=html, class_="pyplot-container")
        
        self._register_component(cid, builder)

    def line_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", **props):
        """Display simple line chart"""
        cid = self._get_next_cid("line_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(cls(x=x_data, y=y_data, mode='lines+markers', name=trace_name))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" style="{container_width} height: {height}px;"></div>
            <script>(function(){{
                const d = {fj};
                Plotly.newPlot('{cid}', d.data, d.layout, {{responsive: true}});
            }})();</script>
            '''
            return Component("div", id=f"{cid}_wrapper", content=html)
        
        self._register_component(cid, builder)

    def bar_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", **props):
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
            <div id="{cid}" style="{container_width} height: {height}px;"></div>
            <script>(function(){{
                const d = {fj};
                Plotly.newPlot('{cid}', d.data, d.layout, {{responsive: true}});
            }})();</script>
            '''
            return Component("div", id=f"{cid}_wrapper", content=html)
        
        self._register_component(cid, builder)

    def area_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", **props):
        """Display area chart"""
        cid = self._get_next_cid("area_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(cls(x=x_data, y=y_data, fill='tozeroy', name=trace_name))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" style="{container_width} height: {height}px;"></div>
            <script>(function(){{
                const d = {fj};
                Plotly.newPlot('{cid}', d.data, d.layout, {{responsive: true}});
            }})();</script>
            '''
            return Component("div", id=f"{cid}_wrapper", content=html)
        
        self._register_component(cid, builder)

    def scatter_chart(self, data, x=None, y=None, width=None, height=400, use_container_width=True, render_mode="svg", **props):
        """Display scatter chart"""
        cid = self._get_next_cid("scatter_chart")
        
        def builder():
            x_data, y_data, trace_name = self._parse_chart_data(data, x, y)
            
            fig = go.Figure()
            cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            fig.add_trace(cls(x=x_data, y=y_data, mode='markers', name=trace_name))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = pio.to_json(fig)
            container_width = "width: 100%;" if use_container_width else f"width: {width}px;" if width else "width: 100%;"
            html = f'''
            <div id="{cid}" style="{container_width} height: {height}px;"></div>
            <script>(function(){{
                const d = {fj};
                Plotly.newPlot('{cid}', d.data, d.layout, {{responsive: true}});
            }})();</script>
            '''
            return Component("div", id=f"{cid}_wrapper", content=html)
        
        self._register_component(cid, builder)

    def bokeh_chart(self, figure, use_container_width=True, **props):
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
            return Component("div", id=cid, content=html)
        
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
