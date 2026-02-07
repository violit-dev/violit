"""Text widgets"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx
from ..style_utils import merge_cls, merge_style


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
    
    def _render_markdown(self, text: str) -> str:
        """Render markdown to HTML (internal helper)"""
        import re
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Headers
            if stripped.startswith('### '):
                result.append(f'<h3>{stripped[4:]}</h3>')
                i += 1
            elif stripped.startswith('## '):
                result.append(f'<h2>{stripped[3:]}</h2>')
                i += 1
            elif stripped.startswith('# '):
                result.append(f'<h1>{stripped[2:]}</h1>')
                i += 1
            # Unordered lists
            elif stripped.startswith(('- ', '* ')):
                list_items = []
                while i < len(lines):
                    curr = lines[i].strip()
                    if curr.startswith(('- ', '* ')):
                        list_items.append(f'<li>{curr[2:]}</li>')
                        i += 1
                    elif not curr:
                        i += 1
                        break
                    else:
                        break
                result.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ul>')
            # Ordered lists
            elif re.match(r'^\d+\.\s', stripped):
                list_items = []
                while i < len(lines):
                    curr = lines[i].strip()
                    if re.match(r'^\d+\.\s', curr):
                        clean_item = re.sub(r'^\d+\.\s', '', curr)
                        list_items.append(f'<li>{clean_item}</li>')
                        i += 1
                    elif not curr:
                        i += 1
                        break
                    else:
                        break
                result.append('<ol style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ol>')
            # Empty line
            elif not stripped:
                result.append('<br>')
                i += 1
            # Regular text
            else:
                result.append(line)
                i += 1
        
        html = '\n'.join(result)
        
        # Inline elements
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', html)
        html = re.sub(r'`(.+?)`', r'<code style="background:var(--sl-bg-card);padding:0.2em 0.4em;border-radius:3px;">\1</code>', html)
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:var(--sl-primary);">\1</a>', html)
        
        return html
    
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
                    background: var(--sl-color-primary-600);
                    color: white;
                    padding: 0.75rem;
                    text-align: left;
                    font-weight: 600;
                }}
                .dataframe td {{
                    padding: 0.5rem 0.75rem;
                    border-bottom: 1px solid var(--sl-color-neutral-200);
                }}
                .dataframe tr:hover {{
                    background: var(--sl-color-neutral-50);
                }}
            </style>
            {html}
        </div>
        '''
        return styled_html

    def heading(self, *args, level: int = 1, divider: bool = False, cls: str = "", style: str = ""):
        """Display heading (h1-h6)"""
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
            html_output = f'<h{level} class="{grad}">{escaped_content}</h{level}>'
            if divider: html_output += '<sl-divider class="divider"></sl-divider>'
            _wd = self._get_widget_defaults("heading")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def title(self, *args, cls: str = "", style: str = ""):
        """Display title (h1 with gradient)"""
        self.heading(*args, level=1, divider=False, cls=cls, style=style)
    
    def header(self, *args, divider: bool = True, cls: str = "", style: str = ""):
        """Display header (h2)"""
        self.heading(*args, level=2, divider=divider, cls=cls, style=style)
    
    def subheader(self, *args, divider: bool = False, cls: str = "", style: str = ""):
        """Display subheader (h3)"""
        self.heading(*args, level=3, divider=divider, cls=cls, style=style)

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
            
            text_cls = f"text-{size} {'text-muted' if muted else ''}"
            _wd = self._get_widget_defaults("text")
            _fc = merge_cls(_wd.get("cls", ""), text_cls, cls)
            _fs = merge_style(_wd.get("style", ""), style)
            # XSS protection: enable content escaping
            return Component("p", id=cid, content=val, escape_content=True, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)
    
    def caption(self, *args, cls: str = "", style: str = ""):
        """Display caption text (small, muted)"""
        self.text(*args, size="small", muted=True, cls=cls, style=style)

    def markdown(self, *args, cls: str = "", style: str = "", **props):
        """Display markdown-formatted text
        
        Supports multiple arguments which will be joined by spaces.
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
                
            # Enhanced markdown conversion - line-by-line processing
            import re
            lines = content.split('\n')
            result = []
            i = 0
            
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                
                # Headers
                if stripped.startswith('### '):
                    result.append(f'<h3>{stripped[4:]}</h3>')
                    i += 1
                elif stripped.startswith('## '):
                    result.append(f'<h2>{stripped[3:]}</h2>')
                    i += 1
                elif stripped.startswith('# '):
                    result.append(f'<h1>{stripped[2:]}</h1>')
                    i += 1
                # Unordered lists
                elif stripped.startswith(('- ', '* ')):
                    list_items = []
                    while i < len(lines):
                        curr = lines[i].strip()
                        if curr.startswith(('- ', '* ')):
                            list_items.append(f'<li>{curr[2:]}</li>')
                            i += 1
                        elif not curr:  # Empty line
                            i += 1
                            break
                        else:
                            break
                    result.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ul>')
                # Ordered lists
                elif re.match(r'^\d+\.\s', stripped):
                    list_items = []
                    while i < len(lines):
                        curr = lines[i].strip()
                        if re.match(r'^\d+\.\s', curr):
                            clean_item = re.sub(r'^\d+\.\s', '', curr)
                            list_items.append(f'<li>{clean_item}</li>')
                            i += 1
                        elif not curr:  # Empty line
                            i += 1
                            break
                        else:
                            break
                    result.append('<ol style="margin: 0.5rem 0; padding-left: 1.5rem;">' + ''.join(list_items) + '</ol>')
                # Empty line
                elif not stripped:
                    result.append('<br>')
                    i += 1
                # Regular text
                else:
                    result.append(line)
                    i += 1
            
            html = '\n'.join(result)
            
            # Inline elements (bold, italic, code, links)
            # Bold **text** (before italic to avoid conflicts)
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            # Italic *text* (avoid matching list markers)
            html = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', html)
            # Code `text`
            html = re.sub(r'`(.+?)`', r'<code style="background:var(--sl-bg-card);padding:0.2em 0.4em;border-radius:3px;">\1</code>', html)
            # Links [text](url)
            html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:var(--sl-primary);">\1</a>', html)
            
            rendering_ctx.reset(token)
            _wd = self._get_widget_defaults("markdown")
            _fc = merge_cls(_wd.get("cls", ""), "markdown", cls)
            _fs = merge_style(_wd.get("style", ""), style)
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
                border_color = "var(--sl-border, #e5e7eb)"
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
                    <sl-icon name="clipboard" style="font-size: 0.85rem;"></sl-icon>
                    <span>Copy</span>
                </button>
                <script>
                function {copy_fn}(btn) {{
                    const pre = btn.closest('.violit-code-block').querySelector('code');
                    navigator.clipboard.writeText(pre.textContent).then(() => {{
                        const icon = btn.querySelector('sl-icon');
                        const span = btn.querySelector('span');
                        if (icon) icon.setAttribute('name', 'check2');
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
            
            html_output = f'''
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
                    "><code class="hljs {lang_class}" style="
                        font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
                        background: transparent; padding: 0;
                    ">{escaped_code}</code></pre>
                </div>
            </div>
            <script>
            (function() {{
                var el = document.getElementById('{cid}');
                if (el && typeof hljs !== 'undefined') {{
                    el.querySelectorAll('pre code').forEach(function(block) {{
                        hljs.highlightElement(block);
                    }});
                }}
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
            return Component("sl-divider", id=cid, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)

    def success(self, body, icon="check-circle", cls: str = "", style: str = ""):
        """Display success message"""
        self._alert(body, "success", icon, cls=cls, style=style)

    def info(self, body, icon="info-circle", cls: str = "", style: str = ""):
        """Display info message"""
        self._alert(body, "primary", icon, cls=cls, style=style)

    def warning(self, body, icon="exclamation-triangle", cls: str = "", style: str = ""):
        """Display warning message"""
        self._alert(body, "warning", icon, cls=cls, style=style)

    def error(self, body, icon="exclamation-octagon", cls: str = "", style: str = ""):
        """Display error message"""
        self._alert(body, "danger", icon, cls=cls, style=style)

    def _alert(self, body, variant, icon_name, cls: str = "", style: str = ""):
        cid = self._get_next_cid("alert")
        def builder():
            icon_html = f'<sl-icon slot="icon" name="{icon_name}"></sl-icon>'
            html = f'<sl-alert variant="{variant}" open style="margin-bottom:1rem;">{icon_html}{body}</sl-alert>'
            _wd = self._get_widget_defaults("alert")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)
