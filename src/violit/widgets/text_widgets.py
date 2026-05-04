"""Text widgets"""

import html as html_lib
import re
import time
from typing import Union, Callable, Optional, Any
from urllib.parse import urlparse
from ..component import Component
from ..context import rendering_ctx
from ..style_utils import merge_cls, merge_style


def _sanitize_markdown_href(raw_href: str) -> str | None:
    href = html_lib.unescape(raw_href).strip()
    if not href or href.startswith("//"):
        return None

    scheme = urlparse(href).scheme.lower()
    if scheme and scheme not in {"http", "https", "mailto", "tel"}:
        return None

    return html_lib.escape(href, quote=True)


def _render_safe_markdown_html(text: str) -> str:
    escaped_text = html_lib.escape(text)
    lines = escaped_text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('### '):
            result.append(f'<h3>{stripped[4:]}</h3>')
            i += 1
        elif stripped.startswith('## '):
            result.append(f'<h2>{stripped[3:]}</h2>')
            i += 1
        elif stripped.startswith('# '):
            result.append(f'<h1>{stripped[2:]}</h1>')
            i += 1
        elif stripped.startswith(('- ', '* ')):
            list_items = []
            while i < len(lines):
                current_line = lines[i].strip()
                if current_line.startswith(('- ', '* ')):
                    list_items.append(f'<li>{current_line[2:]}</li>')
                    i += 1
                elif not current_line:
                    i += 1
                    break
                else:
                    break
            result.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ul>')
        elif re.match(r'^\d+\.\s', stripped):
            list_items = []
            while i < len(lines):
                current_line = lines[i].strip()
                if re.match(r'^\d+\.\s', current_line):
                    clean_item = re.sub(r'^\d+\.\s', '', current_line)
                    list_items.append(f'<li>{clean_item}</li>')
                    i += 1
                elif not current_line:
                    i += 1
                    break
                else:
                    break
            result.append('<ol style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ol>')
        elif not stripped:
            result.append('<br>')
            i += 1
        else:
            result.append(f'{line}<br>')
            i += 1

    html = '\n'.join(result)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', html)
    html = re.sub(r'`(.+?)`', r'<code style="background:var(--vl-bg-card);padding:0.2em 0.4em;border-radius:3px;">\1</code>', html)

    def replace_link(match: re.Match[str]) -> str:
        label = match.group(1)
        raw_href = match.group(2)
        safe_href = _sanitize_markdown_href(raw_href)
        if safe_href is None:
            return f'{label} ({raw_href})'
        return f'<a href="{safe_href}" rel="noopener noreferrer" style="color:var(--vl-primary);">{label}</a>'

    return re.sub(r'\[(.+?)\]\((.+?)\)', replace_link, html)


class TextWidgetsMixin:
    def write(self, *args, **kwargs):
        """Magic write: displays arguments based on their type
        
        Supported types:
        - Strings, Numbers, State: Rendered as Markdown text
        - Pandas DataFrame/Series: Rendered as interactive table
        - Dict/List: Rendered as JSON tree
        - Matplotlib/Plotly Figures: Rendered as charts
        - Exceptions: Rendered as error trace
        """
        from ..state import State, ComputedState
        
        # Buffer for text-like arguments
        text_buffer = []
        
        def flush_buffer():
            if text_buffer:
                self.markdown(*text_buffer)
                text_buffer.clear()
        
        for arg in args:
            # Unwrap state for type checking ONLY
            check_val = arg.value if isinstance(arg, (State, ComputedState)) else arg
            
            # 1. Pandas DataFrame / Series
            is_df = False
            try:
                import pandas as pd
                if isinstance(check_val, (pd.DataFrame, pd.Series, pd.Index)):
                    is_df = True
            except ImportError: pass
            
            if is_df:
                flush_buffer()
                if hasattr(self, 'dataframe'):
                    self.dataframe(arg)
                else:
                    self.markdown(str(arg))
                continue
                
            # 2. Matplotlib Figure
            is_pyplot = False
            try:
                import matplotlib.figure
                if isinstance(check_val, matplotlib.figure.Figure):
                    is_pyplot = True
            except ImportError: pass
            
            if is_pyplot:
                flush_buffer()
                if hasattr(self, 'pyplot'):
                    self.pyplot(arg)
                continue
                
            # 3. Plotly Figure
            is_plotly = False
            try:
                if hasattr(check_val, 'to_plotly_json'):
                    is_plotly = True
            except ImportError: pass
            
            if is_plotly:
                flush_buffer()
                if hasattr(self, 'plotly_chart'):
                    self.plotly_chart(arg)
                continue
                
            # 4. Dict / List (JSON)
            if isinstance(check_val, (dict, list)):
                flush_buffer()
                if hasattr(self, 'json'):
                    self.json(arg)
                else:
                    # Fallback if json widget logic is missing for State
                    # But wait, we need to fix json widget too.
                    self.json(arg)
                continue
                
            # 5. Exception
            if isinstance(check_val, Exception):
                flush_buffer()
                if hasattr(self, 'exception'):
                    self.exception(arg)
                else:
                    self.error(str(arg))
                continue
            
            # Default: Text-like (str, int, float, State, ComputedState)
            text_buffer.append(arg)
            
        # Flush remaining text
        flush_buffer()

    def _write_stream_to_placeholder(self, placeholder, items, cursor=None):
        with placeholder.container():
            for index, item in enumerate(items):
                if isinstance(item, str):
                    text = item
                    if cursor and index == len(items) - 1:
                        text += str(cursor)
                    self.markdown(text)
                else:
                    self.write(item)

    def _normalize_stream_iterator(self, stream):
        candidate = stream() if callable(stream) and not hasattr(stream, "__iter__") else stream
        if hasattr(candidate, "__iter__"):
            return iter(candidate)
        raise TypeError("write_stream expects an iterable, generator, or callable returning an iterable.")

    def _extract_stream_chunk(self, chunk: Any):
        if isinstance(chunk, str):
            return chunk

        if isinstance(chunk, dict):
            if isinstance(chunk.get("text"), str):
                return chunk["text"]
            if isinstance(chunk.get("content"), str):
                return chunk["content"]
            delta = chunk.get("delta") or {}
            if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                return delta["content"]

        choices = getattr(chunk, "choices", None)
        if choices:
            first = choices[0]
            delta = getattr(first, "delta", None)
            if delta is not None:
                content = getattr(delta, "content", None)
                if isinstance(content, str):
                    return content
            message = getattr(first, "message", None)
            if message is not None:
                content = getattr(message, "content", None)
                if isinstance(content, str):
                    return content

        text = getattr(chunk, "text", None)
        if isinstance(text, str):
            return text

        return chunk

    def write_stream(self, stream, *, cursor=None):
        """Stream content into the app, compatible with Streamlit's st.write_stream."""
        placeholder = self.empty()
        iterator = self._normalize_stream_iterator(stream)

        rendered_items = []
        all_text = True

        for raw_chunk in iterator:
            chunk = self._extract_stream_chunk(raw_chunk)
            if isinstance(chunk, str):
                if rendered_items and isinstance(rendered_items[-1], str):
                    rendered_items[-1] += chunk
                else:
                    rendered_items.append(chunk)
            else:
                all_text = False
                rendered_items.append(chunk)

            self._write_stream_to_placeholder(placeholder, rendered_items, cursor=cursor)
            if cursor is not None:
                time.sleep(0)

        self._write_stream_to_placeholder(placeholder, rendered_items, cursor=None)

        if all_text:
            return "".join(item for item in rendered_items if isinstance(item, str))
        return rendered_items
    
    def _render_markdown(self, text: str) -> str:
        """Render markdown to HTML (internal helper)"""
        return _render_safe_markdown_html(text)
    
    def _render_dataframe_html(self, df) -> str:
        """Render pandas DataFrame as HTML table (internal helper)"""
        # Use pandas to_html with custom styling
        html = df.to_html(
            index=True,
            escape=True,
            classes='dataframe',
            border=0
        )
        
        # Add custom styling
        styled_html = f'''
        <div style="overflow-x: auto; margin: 1rem 0;">
            <style>
                .dataframe {{
                    border-collapse: collapse;
                    width: 100%;
                    font-size: 0.9rem;
                }}
                .dataframe th {{
                    background: var(--vl-primary);
                    color: white;
                    padding: 0.75rem;
                    text-align: left;
                    font-weight: 600;
                }}
                .dataframe td {{
                    padding: 0.5rem 0.75rem;
                    border-bottom: 1px solid var(--vl-border);
                }}
                .dataframe tr:hover {{
                    background: var(--vl-bg-card);
                }}
            </style>
            {html}
        </div>
        '''
        return styled_html

    def heading(self, *args, level: int = 1, divider: bool = False, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display heading (h1-h6)

        Args:
            anchor: Optional anchor ID for deep-linking (e.g. '#my-section')
            help: Tooltip text shown next to the heading
        """
        from ..state import State, ComputedState
        import html as html_lib
        
        cid = self._get_next_cid("heading")
        def builder():
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            content = " ".join(parts)
            rendering_ctx.reset(token)
            
            # XSS protection: escape content
            escaped_content = html_lib.escape(str(content))
            
            grad = "gradient-text" if level == 1 else ""
            anchor_attr = f' id="{html_lib.escape(anchor, quote=True)}"' if anchor else ''
            help_html = f' <wa-tooltip for="{cid}_help" content="{html_lib.escape(str(help), quote=True)}"></wa-tooltip><wa-icon id="{cid}_help" name="circle-question" style="font-size:0.7em;color:var(--vl-text-muted);vertical-align:middle;cursor:help;"></wa-icon>' if help else ''
            html_output = f'<h{level}{anchor_attr} class="{grad}">{escaped_content}{help_html}</h{level}>'
            if divider: html_output += '<wa-divider class="divider"></wa-divider>'
            _wd = self._get_widget_defaults("heading")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def title(self, *args, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display title (h1 with gradient)"""
        self.heading(*args, level=1, divider=False, anchor=anchor, help=help, cls=cls, style=style)

    def header(self, *args, divider: bool = True, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display header (h2)"""
        self.heading(*args, level=2, divider=divider, anchor=anchor, help=help, cls=cls, style=style)

    def subheader(self, *args, divider: bool = False, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display subheader (h3)"""
        self.heading(*args, level=3, divider=divider, anchor=anchor, help=help, cls=cls, style=style)

    def text(self, *args, size: str = "medium", muted: bool = False, cls: str = "", style: str = ""):
        """Display text paragraph
        
        Supports multiple arguments which will be joined by spaces.
        """
        from ..state import State, ComputedState
        
        cid = self._get_next_cid("text")
        def builder():
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            val = " ".join(parts)
            rendering_ctx.reset(token)
            
            import html as html_lib
            text_cls = f"text-{size} {'text-muted' if muted else ''}"
            _wd = self._get_widget_defaults("text")
            _fc = merge_cls(_wd.get("cls", ""), text_cls, cls)
            _fs = merge_style(_wd.get("style", ""), style)
            # XSS protection: escape manually, then convert newlines to <br>
            safe_val = html_lib.escape(val).replace('\n', '<br>')
            return Component("p", id=cid, content=safe_val, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)
    
    def caption(self, *args, unsafe_allow_html=False, help: str = None, cls: str = "", style: str = ""):
        """Display caption text (small, muted)

        Args:
            unsafe_allow_html: If True, allow raw HTML in content
            help: Tooltip text
        """
        if unsafe_allow_html:
            self.html(*args, cls=f"text-small text-muted {cls}", style=style)
        else:
            self.text(*args, size="small", muted=True, cls=cls, style=style)

    def markdown(self, *args, unsafe_allow_html=False, help: str = None, cls: str = "", style: str = "", **props):
        """Display markdown-formatted text

        Args:
            unsafe_allow_html: If True, allow raw HTML tags to pass through (not escaped)
            help: Tooltip text
        """
        cid = self._get_next_cid("markdown")
        def builder():
            token = rendering_ctx.set(cid)
            from ..state import State, ComputedState
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            content = " ".join(parts)

            html = content if unsafe_allow_html else _render_safe_markdown_html(content)
            
            rendering_ctx.reset(token)
            _wd = self._get_widget_defaults("markdown")
            _fc = merge_cls(_wd.get("cls", ""), "markdown", cls)
            _fs = merge_style(_wd.get("style", ""), style)
            if help:
                safe_help = html_lib.escape(str(help), quote=True)
                html += f' <wa-tooltip for="{cid}_help" content="{safe_help}"></wa-tooltip><wa-icon id="{cid}_help" name="circle-question" style="font-size:0.85em;vertical-align:middle;cursor:help;"></wa-icon>'
            return Component("div", id=cid, content=html, class_=_fc, style=_fs or None, **props)
        self._register_component(cid, builder)
    
    def html(self, *args, cls: str = "", style: str = "", **props):
        """Display raw HTML content
        
        Use this when you need to render HTML directly without markdown processing.
        For markdown formatting, use app.markdown() instead.
        
        Example:
            app.html('<div class="custom">', count, '</div>')
        """
        cid = self._get_next_cid("html")
        def builder():
            from ..state import State, ComputedState
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            content = " ".join(parts)
            rendering_ctx.reset(token)
            _wd = self._get_widget_defaults("html")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=content, class_=_fc or None, style=_fs or None, **props)
        self._register_component(cid, builder)

    def code(self, code: Union[str, Callable], language: Optional[str] = None,
             showcase: bool = False, title: Optional[str] = None,
             copy_button: bool = True, line_numbers: bool = False,
             wrap_lines: bool = False,
             theme: str = "dark",
             cls: str = "", style: str = "", **props):
        """Display code block with syntax highlighting

        Args:
            code: Code string or callable returning code string
            language: Language for syntax highlighting (e.g. "python", "javascript")
            showcase: If True, show macOS-style window chrome (traffic lights + title bar)
            title: Title text for the title bar (shown in showcase mode)
            copy_button: If True, show a copy-to-clipboard button (default: True)
            line_numbers: If True, show line numbers
            wrap_lines: If True, wrap long lines instead of horizontal scrolling
            theme: Color theme - "dark" (default) or "light"
            cls: Additional CSS classes
            style: Additional inline CSS
        """
        import html as html_lib
        
        cid = self._get_next_cid("code")
        def builder():
            token = rendering_ctx.set(cid)
            code_text = code() if callable(code) else code
            rendering_ctx.reset(token)
            
            # XSS protection: escape code content
            escaped_code = html_lib.escape(str(code_text))
            
            lang_class = f"language-{language}" if language else ""
            
            # Theme colors
            if theme == "light":
                bg_color = "#fafafa"
                border_color = "var(--vl-border, #e5e7eb)"
                bar_bg = "#f0f0f0"
                bar_dot_colors = ("#ff5f57", "#febc2e", "#28c840")
                title_color = "#6b7280"
                line_num_color = "#9ca3af"
                copy_btn_color = "#6b7280"
                copy_btn_hover = "#374151"
                hljs_theme_class = "violit-code-light"
            else:
                bg_color = "#1e1b2e"
                border_color = "rgba(124, 58, 237, 0.15)"
                bar_bg = "#16132a"
                bar_dot_colors = ("#ff5f57", "#febc2e", "#28c840")
                title_color = "#6b6b8d"
                line_num_color = "#4a4a6a"
                copy_btn_color = "#6b6b8d"
                copy_btn_hover = "#a5a5c0"
                hljs_theme_class = "violit-code-dark"
            
            # --- Build line numbers ---
            line_num_html = ""
            if line_numbers:
                lines = code_text.split('\n')
                nums = ''.join(f'<span style="display:block;">{i+1}</span>' for i in range(len(lines)))
                line_num_html = f'''<div style="
                    position: absolute; left: 0; top: 0; bottom: 0;
                    padding: 1rem 0.75rem 1rem 1rem;
                    text-align: right; color: {line_num_color};
                    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
                    font-size: 0.8rem; line-height: 1.7;
                    user-select: none; pointer-events: none;
                    border-right: 1px solid {border_color};
                ">{nums}</div>'''
            
            code_padding_left = "3.5rem" if line_numbers else "1.25rem"
            
            # --- Copy button ---
            copy_btn_html = ""
            if copy_button:
                # Unique copy function name to avoid conflicts
                copy_fn = f"violitCopy_{cid}"
                copy_btn_html = f'''
                <button onclick="{copy_fn}(this)" style="
                    position: absolute; top: 0.6rem; right: 0.6rem;
                    background: transparent; border: 1px solid {border_color};
                    border-radius: 0.375rem; padding: 0.3rem 0.5rem;
                    cursor: pointer; color: {copy_btn_color};
                    font-size: 0.75rem; font-family: inherit;
                    transition: all 0.2s; z-index: 2; display: flex;
                    align-items: center; gap: 0.3rem;
                " onmouseenter="this.style.color='{copy_btn_hover}';this.style.borderColor='{copy_btn_hover}'"
                  onmouseleave="this.style.color='{copy_btn_color}';this.style.borderColor='{border_color}'"
                >
                    <wa-icon name="clipboard" style="font-size: 0.85rem;"></wa-icon>
                    <span>Copy</span>
                </button>
                <script>
                function {copy_fn}(btn) {{
                    const pre = btn.closest('.violit-code-block').querySelector('code');
                    navigator.clipboard.writeText(pre.textContent).then(() => {{
                        const icon = btn.querySelector('wa-icon');
                        const span = btn.querySelector('span');
                        if (icon) icon.setAttribute('name', 'check');
                        if (span) span.textContent = 'Copied!';
                        setTimeout(() => {{
                            if (icon) icon.setAttribute('name', 'clipboard');
                            if (span) span.textContent = 'Copy';
                        }}, 2000);
                    }});
                }}
                </script>
                '''
            
            # --- Title bar (showcase mode) ---
            title_bar_html = ""
            if showcase:
                title_text = f'<span style="margin-left: 0.75rem; font-size: 0.8rem; color: {title_color}; font-family: monospace;">{html_lib.escape(title)}</span>' if title else ''
                title_bar_html = f'''
                <div style="
                    padding: 0.7rem 1rem; background: {bar_bg};
                    display: flex; align-items: center; gap: 0.5rem;
                    border-bottom: 1px solid {border_color};
                ">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {bar_dot_colors[0]};"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {bar_dot_colors[1]};"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {bar_dot_colors[2]};"></div>
                    {title_text}
                </div>
                '''
            
            # --- Assemble ---
            # border-radius: if showcase, top corners are 0 (title bar has them)
            pre_radius = "0" if showcase else "0.625rem"
            outer_radius = "0.625rem"
            
            # Scrollbar colors based on theme
            if theme == "light":
                sb_thumb = "rgba(0, 0, 0, 0.15)"
                sb_thumb_hover = "rgba(0, 0, 0, 0.3)"
            else:
                sb_thumb = "rgba(255, 255, 255, 0.15)"
                sb_thumb_hover = "rgba(255, 255, 255, 0.3)"

            scrollbar_style = f'''
            <style>
            .violit-code-block.{hljs_theme_class} *::-webkit-scrollbar {{
                height: 6px;
                width: 6px;
            }}
            .violit-code-block.{hljs_theme_class} *::-webkit-scrollbar-track {{
                background: transparent;
            }}
            .violit-code-block.{hljs_theme_class} *::-webkit-scrollbar-thumb {{
                background-color: {sb_thumb};
                border-radius: 99px;
                transition: background-color 0.2s;
            }}
            .violit-code-block.{hljs_theme_class} *::-webkit-scrollbar-thumb:hover {{
                background-color: {sb_thumb_hover};
            }}
            .violit-code-block.{hljs_theme_class} *::-webkit-scrollbar-corner {{
                background: transparent;
            }}
            </style>
            '''
            
            html_output = f'''
            {scrollbar_style}
            <div class="violit-code-block {hljs_theme_class}" style="
                position: relative; border-radius: {outer_radius};
                overflow: hidden; border: 1px solid {border_color};
                background: {bg_color};
            ">
                {title_bar_html}
                <div style="position: relative;">
                    {copy_btn_html}
                    {line_num_html}
                    <pre style="
                        margin: 0; padding: 1rem {code_padding_left};
                        padding-left: {code_padding_left}; padding-right: 3.5rem;
                        overflow-x: auto; font-size: 0.875rem; line-height: 1.7;
                        background: {bg_color}; border-radius: {pre_radius};
                        {'white-space: pre-wrap; word-wrap: break-word;' if wrap_lines else ''}
                    "><code class="hljs {lang_class}" style="
                        font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
                        background: transparent; padding: 0;
                        {'white-space: pre-wrap;' if wrap_lines else ''}
                    ">{escaped_code}</code></pre>
                </div>
            </div>
            <script>
            (function() {{
                function highlight() {{
                    var el = document.getElementById('{cid}');
                    if (el && typeof hljs !== 'undefined') {{
                        el.querySelectorAll('pre code').forEach(function(block) {{
                            hljs.highlightElement(block);
                        }});
                    }}
                }}
                
                window._vlLoadLib('hljs', function() {{
                    if (document.readyState === 'loading') {{
                        document.addEventListener('DOMContentLoaded', highlight);
                    }} else {{
                        highlight();
                    }}
                }});
            }})();
            </script>
            '''
            _wd = self._get_widget_defaults("code")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None, **props)
        self._register_component(cid, builder)

    def divider(self, cls: str = "", style: str = ""):
        """Display horizontal divider"""
        cid = self._get_next_cid("divider")
        def builder():
            _wd = self._get_widget_defaults("divider")
            _fc = merge_cls(_wd.get("cls", ""), "divider", cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("wa-divider", id=cid, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)

    def space(self, size="1rem"):
        """Add vertical space between widgets.
        
        Args:
            size: CSS size value (e.g. '0.5rem', '2rem', '20px')
        """
        if isinstance(size, (int, float)):
            size = f'{size}rem'
        cid = self._get_next_cid("space")
        def builder():
            return Component(None, id=cid, content=f'<div style="height:{size}"></div>')
        self._register_component(cid, builder)

    def latex(self, body, cls: str = "", style: str = ""):
        """Display mathematical expression using LaTeX notation (rendered via KaTeX)
        
        Args:
            body: LaTeX formula string (e.g. r'\\frac{a}{b}')
        """
        from ..state import State, ComputedState
        import json as _json

        cid = self._get_next_cid("latex")
        def builder():
            token = rendering_ctx.set(cid)
            if isinstance(body, (State, ComputedState)):
                val = str(body.value)
            elif callable(body):
                val = str(body())
            else:
                val = str(body)
            rendering_ctx.reset(token)

            formula_js = _json.dumps(val)
            _wd = self._get_widget_defaults("latex")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("padding:0.5rem 0; text-align:center; font-size:1.1rem;", _wd.get("style", ""), style)

            html = f'''<div id="{cid}" class="{_fc}" style="{_fs}"></div>
            <script>
            (function() {{
                if (!document.getElementById('_vl_katex_css')) {{
                    var lnk = document.createElement('link');
                    lnk.id = '_vl_katex_css'; lnk.rel = 'stylesheet';
                    lnk.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css';
                    document.head.appendChild(lnk);
                }}
                window._vlLoadLib('katex', function() {{
                    var el = document.getElementById('{cid}');
                    if (el) {{
                        try {{
                            katex.render({formula_js}, el, {{throwOnError: false, displayMode: true}});
                        }} catch(e) {{ el.textContent = {formula_js}; }}
                    }}
                }});
            }})();
            </script>'''
            return Component(None, id=cid, content=html)
        self._register_component(cid, builder)

