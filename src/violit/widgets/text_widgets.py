"""Text widgets"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx


class TextWidgetsMixin:
    def write(self, *args, tag: Optional[str] = "div", unsafe_allow_html: bool = False, **props):
        """Display content with automatic type detection"""
        from ..state import State
        import re
        import json
        import html as html_lib
        
        cid = self._get_next_cid("comp")
        
        def builder():
            def _has_markdown(text: str) -> bool:
                """Check if text contains markdown syntax"""
                markdown_patterns = [
                    r'^#{1,6}\s',           # Headers: # ## ###
                    r'\*\*[^*]+\*\*',       # Bold: **text**
                    r'(?<!\*)\*[^*\n]+\*',  # Italic: *text*
                    r'`[^`]+`',             # Code: `text`
                    r'\[.+?\]\(.+?\)',      # Links: [text](url)
                    r'^[-*]\s',             # Lists: - or *
                    r'^\d+\.\s',            # Numbered lists: 1. 2.
                ]
                for pattern in markdown_patterns:
                    if re.search(pattern, text, re.MULTILINE):
                        return True
                return False
            
            # Set rendering context once for entire builder
            token = rendering_ctx.set(cid)
            parts = []
            
            try:
                for arg in args:
                    current_value = arg
                    
                    # State object: read value (registers dependency)
                    if isinstance(arg, State):
                        current_value = arg.value
                    
                    # Callable/Lambda: execute (registers dependency)
                    elif callable(arg):
                        current_value = arg()
                    
                    # DataFrame (pandas)
                    try:
                        import pandas as pd
                        if isinstance(current_value, pd.DataFrame):
                            parts.append(self._render_dataframe_html(current_value))
                            continue
                    except (ImportError, AttributeError):
                        pass
                    
                    # Dict or List → JSON
                    if isinstance(current_value, (dict, list, tuple)):
                        json_str = json.dumps(current_value, indent=2, ensure_ascii=False)
                        parts.append(f'<pre style="background:var(--sl-bg-card);padding:1rem;border-radius:0.5rem;border:1px solid var(--sl-border);overflow-x:auto;"><code style="color:var(--sl-text);font-family:monospace;">{html_lib.escape(json_str)}</code></pre>')
                        continue
                    
                    # String with markdown → render as markdown
                    text = str(current_value)
                    if _has_markdown(text):
                        parts.append(self._render_markdown(text))
                    else:
                        # Plain text
                        parts.append(text)
                
                # Join all parts
                content = " ".join(parts)
                
                # Check if any HTML in content
                has_html = '<' in content and '>' in content
                return Component(tag, id=cid, content=content, escape_content=not (has_html or unsafe_allow_html), **props)
            
            finally:
                rendering_ctx.reset(token)
        
        self._register_component(cid, builder)
    
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

    def heading(self, text, level: int = 1, divider: bool = False):
        """Display heading (h1-h6)"""
        from ..state import State
        import html as html_lib
        
        cid = self._get_next_cid("heading")
        def builder():
            token = rendering_ctx.set(cid)
            if isinstance(text, State):
                content = text.value
            elif callable(text):
                content = text()
            else:
                content = text
            rendering_ctx.reset(token)
            
            # XSS protection: escape content
            escaped_content = html_lib.escape(str(content))
            
            grad = "gradient-text" if level == 1 else ""
            html_output = f'<h{level} class="{grad}">{escaped_content}</h{level}>'
            if divider: html_output += '<sl-divider class="divider"></sl-divider>'
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def title(self, text: Union[str, Callable]):
        """Display title (h1 with gradient)"""
        self.heading(text, level=1, divider=False)
    
    def header(self, text: Union[str, Callable], divider: bool = True):
        """Display header (h2)"""
        self.heading(text, level=2, divider=divider)
    
    def subheader(self, text: Union[str, Callable], divider: bool = False):
        """Display subheader (h3)"""
        self.heading(text, level=3, divider=divider)

    def text(self, content, size: str = "medium", muted: bool = False):
        """Display text paragraph"""
        from ..state import State
        
        cid = self._get_next_cid("text")
        def builder():
            token = rendering_ctx.set(cid)
            if isinstance(content, State):
                val = content.value
            elif callable(content):
                val = content()
            else:
                val = content
            rendering_ctx.reset(token)
            cls = f"text-{size} {'text-muted' if muted else ''}"
            # XSS protection: enable content escaping
            return Component("p", id=cid, content=val, escape_content=True, class_=cls)
        self._register_component(cid, builder)
    
    def caption(self, text: Union[str, Callable]):
        """Display caption text (small, muted)"""
        self.text(text, size="small", muted=True)

    def markdown(self, text: Union[str, Callable], **props):
        """Display markdown-formatted text"""
        cid = self._get_next_cid("markdown")
        def builder():
            token = rendering_ctx.set(cid)
            content = text() if callable(text) else text
            
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
    
    def html(self, html_content: Union[str, Callable], **props):
        """Display raw HTML content
        
        Use this when you need to render HTML directly without markdown processing.
        For markdown formatting, use app.markdown() instead.
        
        Example:
            app.html('<div class="custom">Hello</div>')
        """
        cid = self._get_next_cid("html")
        def builder():
            token = rendering_ctx.set(cid)
            content = html_content() if callable(html_content) else html_content
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

    def html(self, html_content: Union[str, Callable], **props):
        """Render raw HTML"""
        cid = self._get_next_cid("html")
        def builder():
            token = rendering_ctx.set(cid)
            content = html_content() if callable(html_content) else html_content
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=content, **props)
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
