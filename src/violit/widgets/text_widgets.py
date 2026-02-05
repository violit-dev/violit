"""Text widgets"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx


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

    def heading(self, *args, level: int = 1, divider: bool = False):
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
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def title(self, *args):
        """Display title (h1 with gradient)"""
        self.heading(*args, level=1, divider=False)
    
    def header(self, *args, divider: bool = True):
        """Display header (h2)"""
        self.heading(*args, level=2, divider=divider)
    
    def subheader(self, *args, divider: bool = False):
        """Display subheader (h3)"""
        self.heading(*args, level=3, divider=divider)

    def text(self, *args, size: str = "medium", muted: bool = False):
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
            
            cls = f"text-{size} {'text-muted' if muted else ''}"
            # XSS protection: enable content escaping
            return Component("p", id=cid, content=val, escape_content=True, class_=cls)
        self._register_component(cid, builder)
    
    def caption(self, *args):
        """Display caption text (small, muted)"""
        self.text(*args, size="small", muted=True)

    def markdown(self, *args, **props):
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
            return Component("div", id=cid, content=html, class_="markdown", **props)
        self._register_component(cid, builder)
    
    def html(self, *args, **props):
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
            return Component("div", id=cid, content=content, **props)
        self._register_component(cid, builder)

    def code(self, code: Union[str, Callable], language: Optional[str] = None, **props):
        """Display code block with syntax highlighting"""
        import html as html_lib
        
        cid = self._get_next_cid("code")
        def builder():
            token = rendering_ctx.set(cid)
            code_text = code() if callable(code) else code
            rendering_ctx.reset(token)
            
            # XSS protection: escape code content
            escaped_code = html_lib.escape(str(code_text))
            
            lang_class = f"language-{language}" if language else ""
            html_output = f'''
            <pre style="background:var(--sl-bg-card);padding:1rem;border-radius:0.5rem;border:1px solid var(--sl-border);overflow-x:auto;">
                <code class="{lang_class}" style="color:var(--sl-text);font-family:monospace;">{escaped_code}</code>
            </pre>
            '''
            return Component("div", id=cid, content=html_output, **props)
        self._register_component(cid, builder)

    def divider(self):
        """Display horizontal divider"""
        cid = self._get_next_cid("divider")
        def builder():
            return Component("sl-divider", id=cid, class_="divider")
        self._register_component(cid, builder)

    def success(self, body, icon="check-circle"):
        """Display success message"""
        self._alert(body, "success", icon)

    def info(self, body, icon="info-circle"):
        """Display info message"""
        self._alert(body, "primary", icon)

    def warning(self, body, icon="exclamation-triangle"):
        """Display warning message"""
        self._alert(body, "warning", icon)

    def error(self, body, icon="exclamation-octagon"):
        """Display error message"""
        self._alert(body, "danger", icon)

    def _alert(self, body, variant, icon_name):
        cid = self._get_next_cid("alert")
        def builder():
            icon_html = f'<sl-icon slot="icon" name="{icon_name}"></sl-icon>'
            html = f'<sl-alert variant="{variant}" open style="margin-bottom:1rem;">{icon_html}{body}</sl-alert>'
            return Component("div", id=cid, content=html)
        self._register_component(cid, builder)
