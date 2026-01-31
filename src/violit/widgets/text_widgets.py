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

    def heading(self, text, level: int = 1, divider: bool = False, gradient: bool = None, align: str = None, **kwargs):
        """Display heading (h1-h6)
        
        Args:
            text: Heading text
            level: Heading level (1-6)
            divider: Show divider below
            gradient: Apply gradient text effect (default: True for level 1)
            align: Text alignment ('left', 'center', 'right')
            **kwargs: Additional attributes (style, class_, etc.)
        """
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
            
            escaped_content = html_lib.escape(str(content))
            
            # Gradient: default True for h1, False for others
            grade_val = gradient if gradient is not None else (level == 1)
            
            style_parts = []
            
            if isinstance(grade_val, str):
                style_parts.append(f"background: {grade_val}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text")
            elif grade_val:
                style_parts.append("background: linear-gradient(135deg, var(--sl-color-primary-600), var(--sl-color-primary-400)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text")
            
            if align:
                style_parts.append(f"text-align: {align}")
                
            # Merge kwargs style
            if 'style' in kwargs:
                style_parts.append(kwargs.pop('style'))
            
            style_attr = f'style="{"; ".join(style_parts)}"' if style_parts else ""
            
            # Handle additional props via Component? 
            # Component logic for h1-h6 might need distinct handling if we want to pass ID and props
            # But heading implementation currently manually constructs HTML string: f'<h{level} ...>'
            # We should try to use Component if possible, OR construct manual string with props.
            # Using Component is cleaner but requires 'tag' support in Component which works.
            
            # Let's switch to Component for h{level} to handle props automatically
            # But we need to handle the gradient style carefully inside kwargs/style
            
            final_style = "; ".join(style_parts)
            
            # Use Component to render the H tag
            # Note: content is already escaped if we use explicit content arg, BUT Component escapes too.
            # If we pass escaped content to Component, we must disable component escaping.
            
            comp = Component(f"h{level}", id=cid, content=content, escape_content=True, style=final_style, **kwargs)
            html_output = comp.render()
            
            # If divider needed, we need to wrap or append. 
            # Current implementation returns Component("div") wrapper containing H tag string.
            # To allow Props on H tag, we should construct the H tag carefully or return it directly.
            # But 'builder' usually returns a SINGLE component.
            # If divider is used, we return a DIV containing H + Divider. 
            # If no divider, we can return the H component directly?
            # Existing implementation: return Component("div", id=cid, content=html_output)
            # This wraps H in a DIV. This is fine. Use inline style on H tag.
            
            # Let's reconstruct the manual HTML string with props, to maintain wrapper behavior
            props_str = ""
            for k, v in kwargs.items():
                if k == 'class_': k = 'class'
                k = k.replace('_', '-')
                props_str += f' {k}="{html_lib.escape(str(v))}"'
            
            h_tag = f'<h{level} {style_attr}{props_str}>{escaped_content}</h{level}>'
            
            if divider: 
                h_tag += '<sl-divider class="divider"></sl-divider>'
                
            return Component("div", id=cid, content=h_tag)
            
        self._register_component(cid, builder)

    def title(self, text: Union[str, Callable], gradient: bool = True, align: str = None, **kwargs):
        """Display title (h1 with gradient)"""
        self.heading(text, level=1, divider=False, gradient=gradient, align=align, **kwargs)
    
    def header(self, text: Union[str, Callable], divider: bool = True, gradient: bool = False, align: str = None, **kwargs):
        """Display header (h2)"""
        self.heading(text, level=2, divider=divider, gradient=gradient, align=align, **kwargs)
    
    def subheader(self, text: Union[str, Callable], divider: bool = False, gradient: bool = False, align: str = None, **kwargs):
        """Display subheader (h3)"""
        self.heading(text, level=3, divider=divider, gradient=gradient, align=align, **kwargs)

    def text(self, content, size: str = "medium", muted: bool = False, align: str = None, **kwargs):
        """Display text paragraph
        
        Args:
            content: Text content
            size: Text size ('small', 'medium', 'large')
            muted: Use muted color
            align: Text alignment ('left', 'center', 'right')
            **kwargs: Additional attributes (style, class_, etc.)
        """
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
            style_parts = []
            if align:
                style_parts.append(f"text-align: {align}")
            
            # Merge kwargs
            if 'style' in kwargs:
                style_parts.append(kwargs.pop('style'))
            if 'class_' in kwargs:
                cls = f"{cls} {kwargs.pop('class_')}".strip()
                
            style = "; ".join(style_parts)
            
            # XSS protection: enable content escaping
            return Component("p", id=cid, content=val, escape_content=True, class_=cls, style=style, **kwargs)
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

    def code(self, code: Union[str, Callable], language: Optional[str] = None, 
             copy_button: bool = False, line_numbers: bool = False, 
             showcase: bool = False, title: str = None, **props):
        """Display code block with syntax highlighting
        
        Args:
            code: Code content (string or callable)
            language: Programming language for syntax highlighting
            copy_button: Show copy to clipboard button
            line_numbers: Show line numbers
            showcase: Use macOS-style window appearance with colored dots
            title: Window title (only for showcase mode)
        """
        import html as html_lib
        
        cid = self._get_next_cid("code")
        def builder():
            token = rendering_ctx.set(cid)
            code_text = code() if callable(code) else code
            rendering_ctx.reset(token)
            
            escaped_code = html_lib.escape(str(code_text))
            
            # Build line numbers if enabled
            if line_numbers or showcase:
                lines = escaped_code.split('\n')
                numbered_lines = []
                for i, line in enumerate(lines, 1):
                    numbered_lines.append(f'<span class="line-num">{i}</span>{line}')
                escaped_code = '\n'.join(numbered_lines)
                line_num_style = '''
                    .line-num { 
                        display: inline-block; 
                        width: 2.5rem; 
                        text-align: right; 
                        margin-right: 1rem; 
                        color: #6b7280;
                        user-select: none;
                    }
                '''
            else:
                line_num_style = ''
            
            lang_class = f"language-{language}" if language else ""
            
            # Copy button
            copy_btn_html = ''
            if copy_button:
                raw_code = html_lib.escape(str(code_text).replace('"', '&quot;'))
                copy_btn_html = f'''<sl-copy-button value="{raw_code}" 
                    style="position: absolute; top: 0.5rem; right: 0.5rem; --sl-color-primary-600: var(--sl-color-neutral-400);">
                </sl-copy-button>'''
            
            if showcase:
                title_html = f'<div class="code-title">{title}</div>' if title else ''
                
                # macOS-style showcase window
                html_output = f'''
                <div class="code-showcase-{cid}">
                    <style>
                    .code-showcase-{cid} {{
                        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
                        border-radius: 16px;
                        padding: 2rem;
                        margin: 2rem 0;
                        position: relative;
                        overflow: hidden;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    }}
                    .code-showcase-{cid}::before {{
                        content: '';
                        position: absolute;
                        top: 0; left: 0; right: 0;
                        height: 40px;
                        background: linear-gradient(90deg, #1a1a2e, #2d2d5a);
                        border-radius: 16px 16px 0 0;
                    }}
                    .code-showcase-{cid} .code-dots {{
                        position: absolute;
                        top: 15px;
                        left: 20px;
                        display: flex;
                        gap: 8px;
                        z-index: 1;
                    }}
                    .code-showcase-{cid} .code-dot {{
                        width: 12px;
                        height: 12px;
                        border-radius: 50%;
                    }}
                    .code-showcase-{cid} .code-dot.red {{ background: #ff5f56; }}
                    .code-showcase-{cid} .code-dot.yellow {{ background: #ffbd2e; }}
                    .code-showcase-{cid} .code-dot.green {{ background: #27c93f; }}
                    
                    .code-showcase-{cid} .code-title {{
                        position: absolute;
                        top: 12px;
                        right: 20px;
                        color: #666;
                        font-family: sans-serif;
                        font-size: 0.8rem;
                        z-index: 1;
                    }}
                    
                    .code-showcase-{cid} pre {{
                        margin-top: 1.5rem;
                        background: transparent !important;
                        border: none !important;
                        padding: 0 !important;
                    }}
                    .code-showcase-{cid} code {{
                        color: #d4d4d4 !important;
                        font-family: 'JetBrains Mono', 'Fira Code', monospace;
                        font-size: 0.95rem;
                        line-height: 1.8;
                    }}
                    {line_num_style}
                    </style>
                    <div class="code-dots">
                        <div class="code-dot red"></div>
                        <div class="code-dot yellow"></div>
                        <div class="code-dot green"></div>
                    </div>
                    {title_html}
                    {copy_btn_html}
                    <pre><code class="{lang_class}">{escaped_code}</code></pre>
                </div>
                '''
            else:
                html_output = f'''
                <div style="position: relative;">
                    <style>{line_num_style}</style>
                    {copy_btn_html}
                    <pre style="background:var(--sl-bg-card);padding:1rem;border-radius:0.5rem;border:1px solid var(--sl-border);overflow-x:auto;margin:0;">
                        <code class="{lang_class}" style="color:var(--sl-text);font-family:'JetBrains Mono', 'Fira Code', monospace;font-size:0.9rem;line-height:1.6;">{escaped_code}</code>
                    </pre>
                </div>
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
