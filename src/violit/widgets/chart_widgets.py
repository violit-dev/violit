"""Chart Widgets Mixin for Violit"""

import base64
import json

from typing import Union, Optional, Any, Callable
from ..component import Component
from ..context import rendering_ctx, initial_render_ctx
from ..state import State, get_session_store
from ..style_utils import merge_cls, merge_style


def _plotly_json_dumps(fig) -> str:
    """Serialize Plotly figures with plain arrays instead of Plotly 6 typed-array blobs."""

    import numpy as np

    def _normalize(value):
        if isinstance(value, dict):
            if set(value.keys()) == {"dtype", "bdata"}:
                try:
                    array = np.frombuffer(base64.b64decode(value["bdata"]), dtype=np.dtype(value["dtype"]))
                    return array.tolist()
                except Exception:
                    return value
            return {key: _normalize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [_normalize(item) for item in value]
        return value

    return json.dumps(_normalize(fig.to_plotly_json()), ensure_ascii=False, separators=(",", ":"))


# [OPTIMIZED] Plotly render script with fast updates
# - Uses global Set (window._vlPlotlyInited) instead of DOM attribute
#   This survives outerHTML replacement, preventing flicker on reactive updates
# - Already-initialized charts skip clientWidth check and IntersectionObserver delay
# - Uses Plotly.react() for updates (no two-pass sizing = no flicker)
_PLOTLY_RENDER_SCRIPT = """
<script>(function(){{
    var d = {fj};
    var cid = '{cid}';
    var cfg = {{responsive: false, displayModeBar: false}};
    var explicitHeight = d.layout && d.layout.height != null ? Math.round(d.layout.height) : null;

    if (!window._vlPlotlyInited) window._vlPlotlyInited = new Set();
    if (!window._vlPlotlyStates) window._vlPlotlyStates = {{}};
    if (!window._vlPlotlyResizeHandlers) window._vlPlotlyResizeHandlers = {{}};

    var state = window._vlPlotlyStates[cid] || (window._vlPlotlyStates[cid] = {{
        lastWidth: 0,
        lastHeight: 0,
        resizeTimer: null,
        waiting: false,
        resizeObserver: null,
        rendering: false
    }});

    function _vlGetEl() {{
        return document.getElementById(cid);
    }}

    function _vlIsVisible(el) {{
        return !!(el && el.offsetParent !== null);
    }}

    function _vlMeasure(el) {{
        var rect = el.getBoundingClientRect();
        var width = Math.round(rect.width || el.clientWidth || 0);
        var height = explicitHeight != null ? explicitHeight : Math.round(rect.height || el.clientHeight || 0);
        return {{ width: width, height: height }};
    }}

    function _vlApplyLayout(size) {{
        d.layout = d.layout || {{}};
        d.layout.autosize = false;
        d.layout.width = size.width;
        if (size.height > 10) {{
            d.layout.height = size.height;
        }} else if (explicitHeight != null) {{
            d.layout.height = explicitHeight;
        }}
    }}

    function _vlCommitSize(size) {{
        state.lastWidth = size.width;
        state.lastHeight = size.height > 10 ? size.height : (explicitHeight || 0);
    }}

    function _vlResizeExisting() {{
        var el = _vlGetEl();
        if (!el || !_vlIsVisible(el) || !window.Plotly || !window._vlPlotlyInited.has(cid) || !el.querySelector('.plot-container')) return;

        var size = _vlMeasure(el);
        var nextHeight = size.height > 10 ? size.height : (explicitHeight || 0);
        if (size.width < 10) return;
        if (Math.abs(state.lastWidth - size.width) < 2 && Math.abs(state.lastHeight - nextHeight) < 2) return;

        _vlCommitSize(size);
        if (window.Plotly.relayout) {{
            Plotly.relayout(el, {{ autosize: false, width: size.width, height: nextHeight }});
        }} else if (window.Plotly.Plots && window.Plotly.Plots.resize) {{
            Plotly.Plots.resize(el);
        }}
    }}

    function _vlDraw(force) {{
        var el = _vlGetEl();
        if (!el || !_vlIsVisible(el) || !window.Plotly) return;
        if (state.rendering) return;
        var isInitialMount = !el.querySelector('.plot-container');

        var size = _vlMeasure(el);
        var nextHeight = size.height > 10 ? size.height : (explicitHeight || 0);
        if (size.width < 10) return;

        if (!force && window._vlPlotlyInited.has(cid) && el.querySelector('.plot-container') && Math.abs(state.lastWidth - size.width) < 2 && Math.abs(state.lastHeight - nextHeight) < 2) {{
            return;
        }}

        _vlApplyLayout(size);
        state.rendering = true;
        if (isInitialMount) {{
            el.style.opacity = '0';
            el.style.transition = 'opacity 140ms ease-out';
        }}
        var renderResult = window._vlPlotlyInited.has(cid)
            ? Plotly.react(el, d.data, d.layout, cfg)
            : Plotly.newPlot(el, d.data, d.layout, cfg);

        return Promise.resolve(renderResult).then(function() {{
            window._vlPlotlyInited.add(cid);
            _vlCommitSize(size);
            if (isInitialMount) {{
                requestAnimationFrame(function() {{
                    var mountedEl = _vlGetEl();
                    if (mountedEl) {{
                        mountedEl.style.opacity = '1';
                    }}
                }});
            }}
        }}).finally(function() {{
            state.rendering = false;
        }});
    }}

    function _vlWaitForStableWidth(callback) {{
        if (state.waiting) return;
        state.waiting = true;

        var lastWidth = 0;
        var stableFrames = 0;

        function step() {{
            var el = _vlGetEl();
            if (!el || !window.Plotly) {{
                state.waiting = false;
                return;
            }}
            if (!_vlIsVisible(el)) {{
                requestAnimationFrame(step);
                return;
            }}

            var width = Math.round(el.getBoundingClientRect().width || el.clientWidth || 0);
            if (width < 10) {{
                requestAnimationFrame(step);
                return;
            }}

            if (Math.abs(width - lastWidth) <= 1) {{
                stableFrames += 1;
            }} else {{
                stableFrames = 1;
                lastWidth = width;
            }}

            if (stableFrames >= 3) {{
                state.waiting = false;
                callback();
                return;
            }}

            requestAnimationFrame(step);
        }}

        requestAnimationFrame(step);
    }}

    function _vlScheduleRender(force) {{
        _vlWaitForStableWidth(function() {{
            if (!window._vlPlotlyQueue) window._vlPlotlyQueue = Promise.resolve();
            window._vlPlotlyQueue = window._vlPlotlyQueue.then(function() {{
                return new Promise(function(resolve) {{
                    requestAnimationFrame(function() {{
                        var renderPromise = _vlDraw(!!force);
                        if (renderPromise && typeof renderPromise.finally === 'function') {{
                            renderPromise.finally(function() {{ setTimeout(resolve, 30); }});
                        }} else {{
                            setTimeout(resolve, 30);
                        }}
                    }});
                }});
            }});
        }});
    }}

    function _vlScheduleResize(force) {{
        clearTimeout(state.resizeTimer);
        state.resizeTimer = setTimeout(function() {{
            if (state.rendering) {{
                _vlScheduleResize(force);
                return;
            }}
            var el = _vlGetEl();
            if (el && window._vlPlotlyInited.has(cid) && el.querySelector('.plot-container')) {{
                _vlResizeExisting();
            }} else {{
                _vlScheduleRender(force);
            }}
        }}, 80);
    }}

    function _vlBindResizeObserver() {{
        var el = _vlGetEl();
        if (!el || !('ResizeObserver' in window)) return;

        if (state.resizeObserver) state.resizeObserver.disconnect();
        state.resizeObserver = new ResizeObserver(function(entries) {{
            var entry = entries && entries[0];
            if (!entry || !_vlIsVisible(el)) return;

            var width = Math.round(entry.contentRect.width || 0);
            var height = explicitHeight != null ? explicitHeight : Math.round(entry.contentRect.height || 0);
            if (width < 10) return;
            if (Math.abs(state.lastWidth - width) < 2 && Math.abs(state.lastHeight - height) < 2) return;

            _vlScheduleResize(true);
        }});
        state.resizeObserver.observe(el);
    }}

    window._vlPlotlyResizeHandlers[cid] = function(force) {{
        if (!_vlGetEl()) return;
        _vlScheduleResize(!!force);
    }};

    function initPlot() {{
        var el = _vlGetEl();
        if (!el) return;

        _vlBindResizeObserver();
        _vlScheduleRender(!window._vlPlotlyInited.has(cid));

    }}

    // Wait for Plotly library to load (lazy loaded)
    window._vlLoadLib('Plotly', function() {{
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initPlot, {{ once: true }});
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

    def _chart_should_defer_first_render(self, cid, data_points=0):
        if getattr(self, 'mode', None) != 'ws':
            return False

        from ..context import initial_render_ctx
        if not initial_render_ctx.get(False):
            return False

        _ASYNC_CHART_THRESHOLD = 5000
        if data_points < _ASYNC_CHART_THRESHOLD:
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
            import plotly.graph_objects as go
            current_fig = self._resolve_chart_data(fig, cid)
            
            data_points_est = 0
            if current_fig and hasattr(current_fig, "data"):
                for trace in current_fig.data:
                    if hasattr(trace, "y") and trace.y is not None:
                        data_points_est += len(trace.y)
                    elif hasattr(trace, "x") and trace.x is not None:
                        data_points_est += len(trace.x)

            if self._chart_should_defer_first_render(cid, data_points=data_points_est):
                return self._chart_placeholder_component(
                    cid,
                    "plotly_chart",
                    500,
                    use_container_width,
                    cls,
                    style,
                    "Preparing Plotly chart...",
                )
            
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
                
            fj = _plotly_json_dumps(current_fig)
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
            current_fig = self._resolve_chart_data(fig, cid) if fig is not None else plt.gcf()
            if current_fig is None:
                current_fig = plt.gcf()

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
            import plotly.graph_objects as go
            current_data = self._resolve_chart_data(data, cid)
            
            data_points_est = 0
            if hasattr(current_data, "size"):
                data_points_est = current_data.size
            elif isinstance(current_data, list):
                data_points_est = sum(len(row) if isinstance(row, (list, tuple)) else 1 for row in current_data)

            if self._chart_should_defer_first_render(cid, data_points=data_points_est):
                return self._chart_placeholder_component(
                    cid,
                    "line_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing line chart...",
                )
            traces = self._parse_chart_data(current_data, x, y, color=color)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            for t in traces:
                fig.add_trace(trace_cls(x=t['x'], y=t['y'], mode='lines+markers', name=t['name']))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = _plotly_json_dumps(fig)
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
            import plotly.graph_objects as go
            current_data = self._resolve_chart_data(data, cid)
            
            data_points_est = 0
            if hasattr(current_data, "size"):
                data_points_est = current_data.size
            elif isinstance(current_data, list):
                data_points_est = sum(len(row) if hasattr(row, "__len__") else 1 for row in current_data)

            if self._chart_should_defer_first_render(cid, data_points=data_points_est):
                return self._chart_placeholder_component(
                    cid,
                    "bar_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing bar chart...",
                )
            traces = self._parse_chart_data(current_data, x, y, color=color)
            
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
            
            fj = _plotly_json_dumps(fig)
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
            import plotly.graph_objects as go
            current_data = self._resolve_chart_data(data, cid)
            
            data_points_est = 0
            if hasattr(current_data, "size"):
                data_points_est = current_data.size
            elif isinstance(current_data, list):
                data_points_est = sum(len(row) if hasattr(row, "__len__") else 1 for row in current_data)

            if self._chart_should_defer_first_render(cid, data_points=data_points_est):
                return self._chart_placeholder_component(
                    cid,
                    "area_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing area chart...",
                )
            traces = self._parse_chart_data(current_data, x, y, color=color)
            
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
            
            fj = _plotly_json_dumps(fig)
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
            import plotly.graph_objects as go
            current_data = self._resolve_chart_data(data, cid)
            
            data_points_est = 0
            if hasattr(current_data, "size"):
                data_points_est = current_data.size
            elif isinstance(current_data, list):
                data_points_est = sum(len(row) if hasattr(row, "__len__") else 1 for row in current_data)

            if self._chart_should_defer_first_render(cid, data_points=data_points_est):
                return self._chart_placeholder_component(
                    cid,
                    "scatter_chart",
                    height,
                    use_container_width,
                    cls,
                    style,
                    "Preparing scatter chart...",
                )
            traces = self._parse_chart_data(current_data, x, y, color=color)
            
            fig = go.Figure()
            trace_cls = go.Scattergl if render_mode == "webgl" else go.Scatter
            for t in traces:
                marker_kw = {}
                if size and isinstance(current_data, __import__('pandas').DataFrame) and size in current_data.columns:
                    marker_kw['size'] = current_data[size].tolist()
                fig.add_trace(trace_cls(x=t['x'], y=t['y'], mode='markers', name=t['name'], marker=marker_kw or None))
            fig.update_layout(
                height=height,
                margin=dict(l=0, r=0, t=30, b=0),
                template='plotly_white'
            )
            
            fj = _plotly_json_dumps(fig)
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
            current_figure = self._resolve_chart_data(figure, cid)
            if current_figure is None:
                return Component("div", id=cid, content="No data")

            script, div = components(current_figure)
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

    def _resolve_chart_data(self, data, cid=None):
        current_data = data
        token = rendering_ctx.set(cid) if cid else None
        try:
            for _ in range(3):
                if isinstance(current_data, State):
                    current_data = current_data.value
                    continue
                if callable(current_data):
                    current_data = current_data()
                    continue
                break
            return current_data
        finally:
            if token is not None:
                rendering_ctx.reset(token)

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
