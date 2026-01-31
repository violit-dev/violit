"""Text widgets"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx
from ..style_utils import build_cls


class TextWidgetsMixin:
    def write(self, *args, tag: Optional[str] = "div", unsafe_allow_html: bool = False, cls: str = "", inline: bool = False, **props):
        """Display content with automatic type detection
        
        Args:
            *args: Content to display (can be State, callable, or value)
            tag: HTML tag to wrap content (default: "div")
            unsafe_allow_html: Allow HTML in content (default: False)
            cls: Master CSS classes
            inline: If True, use inline display (default: False)
            **props: Additional semantic props and HTML attributes
        """
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
            
            token = rendering_ctx.set(cid)
            parts = []
            
            try:
                for arg in args:
                    current_value = arg
                    
                    if isinstance(arg, State):
                        current_value = arg.value
                    elif callable(arg):
                        current_value = arg()
                    
                    try:
                        import pandas as pd
                        if isinstance(current_value, pd.DataFrame):
                            parts.append(self._render_dataframe_html(current_value))
                            continue
                    except (ImportError, AttributeError):
                        pass
                    
                    if isinstance(current_value, (dict, list, tuple)):
                        json_str = json.dumps(current_value, indent=2, ensure_ascii=False)
                        # Use Master CSS for JSON block
                        parts.append(f'<pre class="bg:bg-card p:1rem r:0.5rem b:1|solid|border overflow-x:auto"><code class="color:text font:mono">{html_lib.escape(json_str)}</code></pre>')
                        continue
                    
                    text = str(current_value)
                    if _has_markdown(text):
                        parts.append(self._render_markdown(text))
                    else:
                        parts.append(text)
                
                content = " ".join(parts)
                has_html = '<' in content and '>' in content
                
                # Separate HTML attributes from Master CSS props
                html_attrs = {}
                css_props = {}
                for k, v in props.items():
                    if k in ['style', 'id', 'data', 'aria'] or k.startswith('data_') or k.startswith('aria_'):
                        html_attrs[k] = v
                    else:
                        css_props[k] = v
                
                # Add inline display if requested
                if inline:
                    css_props['d'] = 'inline-block'
                
                final_cls = build_cls(cls, **css_props)
                
                return Component(tag, id=cid, content=content, escape_content=not (has_html or unsafe_allow_html), class_=final_cls, **html_attrs)
            
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
                    curr = lines[i].strip()
                    if curr.startswith(('- ', '* ')):
                        list_items.append(f'<li>{curr[2:]}</li>')
                        i += 1
                    elif not curr:
                        i += 1
                        break
                    else:
                        break
                result.append('<ul class="my:0.5rem pl:1.5rem">' + ''.join(list_items) + '</ul>')
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
                result.append('<ol class="my:0.5rem pl:1.5rem">' + ''.join(list_items) + '</ol>')
            elif not stripped:
                result.append('<br>')
                i += 1
            else:
                result.append(line)
                i += 1
        
        html = '\n'.join(result)
        
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', html)
        html = re.sub(r'`(.+?)`', r'<code class="bg:bg-card px:0.4em py:0.2em r:3px">\1</code>', html)
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" class="color:primary">\1</a>', html)
        
        return html
    
    def _render_dataframe_html(self, df) -> str:
        """Render pandas DataFrame as HTML table (internal helper)"""
        html = df.to_html(
            index=True,
            escape=True,
            classes='dataframe',
            border=0
        )
        
        # Use Master CSS for dataframe styling
        styled_html = f'''
        <div class="overflow-x:auto my:1rem">
            <style>
                .dataframe {{ border-collapse: collapse; width: 100%; font-size: 0.9rem; }}
                .dataframe th {{ background: var(--sl-color-primary-600); color: white; padding: 0.75rem; text-align: left; font-weight: 600; }}
                .dataframe td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--sl-color-neutral-200); }}
                .dataframe tr:hover {{ background: var(--sl-color-neutral-50); }}
            </style>
            {html}
        </div>
        '''
        return styled_html

    def heading(self, text, level: int = 1, divider: bool = False, gradient: bool = None, align: str = None, cls: str = "", **kwargs):
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
            
            escaped_content = html_lib.escape(str(content))
            
            grade_val = gradient if gradient is not None else (level == 1)
            
            # Use Master CSS for gradient and alignment
            base_cls = ""
            if isinstance(grade_val, str):
                # Custom gradient passed as string - tricky to map to Master CSS directly if it's complex CSS
                # Fallback to style attribute for custom gradient string
                kwargs['style'] = f"background: {grade_val}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; {kwargs.get('style', '')}"
            elif grade_val:
                # Standard gradient
                base_cls += " bg:linear-gradient(135deg,primary-600,primary-400) -webkit-background-clip:text -webkit-text-fill-color:transparent background-clip:text"
            
            if align:
                base_cls += f" text:{align}"
            
            final_cls = build_cls(f"{base_cls} {cls}", **kwargs)
            
            # Construct H tag
            # We use manual construction to ensure props are applied to H tag, not wrapper
            props_str = f'class="{final_cls}"'
            
            # Handle other props that might be passed (id, data-*, etc)
            # kwargs are already consumed by build_cls for style props, but we might have others?
            # build_cls consumes known style props. We should separate them?
            # For simplicity in this mixin, we assume kwargs are mostly style props or standard HTML attrs.
            # Let's add any remaining kwargs as attributes if they weren't consumed? 
            # build_cls doesn't modify kwargs.
            
            h_tag = f'<h{level} {props_str}>{escaped_content}</h{level}>'
            
            if divider: 
                h_tag += '<sl-divider class="my:1.5rem w:full" style="--color:var(--sl-border)"></sl-divider>'
                
            return Component("div", id=cid, content=h_tag)
            
        self._register_component(cid, builder)

    def title(self, text: Union[str, Callable], gradient: bool = True, align: str = None, cls: str = "", **kwargs):
        """Display title (h1 with gradient)"""
        self.heading(text, level=1, divider=False, gradient=gradient, align=align, cls=cls, **kwargs)
    
    def header(self, text: Union[str, Callable], divider: bool = True, gradient: bool = False, align: str = None, cls: str = "", **kwargs):
        """Display header (h2)"""
        self.heading(text, level=2, divider=divider, gradient=gradient, align=align, cls=cls, **kwargs)
    
    def subheader(self, text: Union[str, Callable], divider: bool = False, gradient: bool = False, align: str = None, cls: str = "", **kwargs):
        """Display subheader (h3)"""
        self.heading(text, level=3, divider=divider, gradient=gradient, align=align, cls=cls, **kwargs)

    def text(self, content, size: str = "medium", muted: bool = False, align: str = None, cls: str = "", **kwargs):
        """Display text paragraph
        
        Args:
            content: Text content (can be State or callable)
            size: Text size ("small", "medium", "large", or custom like "3rem")
            muted: If True, use muted color
            align: Text alignment ("left", "center", "right")
            cls: Additional Master CSS classes
            **kwargs: Additional semantic props (including style)
        """
        from ..state import State
        
        cid = self._get_next_cid("text")
        
        # Extract style props OUTSIDE builder (captured by closure, safe for multiple renders)
        weight_val = kwargs.pop('weight', None)
        color_val = kwargs.pop('color', None)
        user_style = kwargs.pop('style', '')
        remaining_kwargs = kwargs.copy()  # For build_cls
        
        def builder():
            token = rendering_ctx.set(cid)
            val = content.value if isinstance(content, State) else (content() if callable(content) else content)
            rendering_ctx.reset(token)
            
            # Build inline style for reliable rendering
            style_parts = ["margin: 0;"]
            
            # Apply size as inline style
            if size == "small": 
                style_parts.append("font-size: 0.875rem;")
            elif size == "large": 
                style_parts.append("font-size: 1.125rem;")
            elif size != "medium":
                style_parts.append(f"font-size: {size};")
            
            # Apply weight and color
            if weight_val:
                style_parts.append(f"font-weight: {weight_val};")
            if color_val:
                style_parts.append(f"color: {color_val};")
            
            # Text alignment
            if align:
                style_parts.append(f"text-align: {align};")
            if muted:
                style_parts.append("color: var(--sl-text-muted);")
            
            # User style (gradient etc)
            if user_style:
                style_parts.append(user_style)
            
            combined_style = " ".join(style_parts)
            
            # Build cls for remaining props
            final_cls = build_cls(cls, **remaining_kwargs)
            
            return Component("p", id=cid, content=val, escape_content=True, class_=final_cls, style=combined_style)
        self._register_component(cid, builder)
    
    def caption(self, text: Union[str, Callable], cls: str = "", **kwargs):
        """Display caption text (small, muted)"""
        self.text(text, size="small", muted=True, cls=cls, **kwargs)

    def markdown(self, text: Union[str, Callable], cls: str = "", **props):
        """Display markdown-formatted text"""
        cid = self._get_next_cid("markdown")
        def builder():
            token = rendering_ctx.set(cid)
            content = text() if callable(text) else text
            
            import re
            lines = content.split('\n')
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
                        curr = lines[i].strip()
                        if curr.startswith(('- ', '* ')):
                            list_items.append(f'<li>{curr[2:]}</li>')
                            i += 1
                        elif not curr:
                            i += 1
                            break
                        else:
                            break
                    result.append('<ul class="my:0.5rem pl:1.5rem">' + ''.join(list_items) + '</ul>')
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
                    result.append('<ol class="my:0.5rem pl:1.5rem">' + ''.join(list_items) + '</ol>')
                elif not stripped:
                    result.append('<br>')
                    i += 1
                else:
                    result.append(line)
                    i += 1
            
            html = '\n'.join(result)
            
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            html = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', html)
            html = re.sub(r'`(.+?)`', r'<code class="bg:bg-card px:0.4em py:0.2em r:3px">\1</code>', html)
            html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" class="color:primary">\1</a>', html)
            
            rendering_ctx.reset(token)
            
            final_cls = build_cls(f"markdown {cls}", **props)
            return Component("div", id=cid, content=html, class_=final_cls)
        self._register_component(cid, builder)
    
    def html(self, html_content: Union[str, Callable], cls: str = "", **props):
        """Display raw HTML content"""
        cid = self._get_next_cid("html")
        def builder():
            token = rendering_ctx.set(cid)
            content = html_content() if callable(html_content) else html_content
            rendering_ctx.reset(token)
            
            final_cls = build_cls(cls, **props)
            return Component("div", id=cid, content=content, class_=final_cls)
        self._register_component(cid, builder)

    def code(self, code: Union[str, Callable], language: Optional[str] = None, 
             copy_button: bool = False, line_numbers: bool = False, 
             showcase: bool = False, title: str = None, cls: str = "", **props):
        """Display code block with syntax highlighting"""
        import html as html_lib
        
        cid = self._get_next_cid("code")
        def builder():
            token = rendering_ctx.set(cid)
            code_text = code() if callable(code) else code
            rendering_ctx.reset(token)
            
            escaped_code = html_lib.escape(str(code_text))
            
            if line_numbers or showcase:
                lines = escaped_code.split('\n')
                numbered_lines = []
                for i, line in enumerate(lines, 1):
                    numbered_lines.append(f'<span class="line-num">{i}</span>{line}')
                escaped_code = '\n'.join(numbered_lines)
                line_num_style = '.line-num { display: inline-block; width: 2.5rem; text-align: right; margin-right: 1rem; color: #6b7280; user-select: none; }'
            else:
                line_num_style = ''
            
            lang_class = f"language-{language}" if language else ""
            
            copy_btn_html = ''
            if copy_button:
                raw_code = html_lib.escape(str(code_text).replace('"', '&quot;'))
                copy_btn_html = f'''<sl-copy-button value="{raw_code}" 
                    class="abs top:0.5rem right:0.5rem" style="--sl-color-primary-600: var(--sl-color-neutral-400);">
                </sl-copy-button>'''
            
            final_cls = build_cls(cls, **props)
            
            if showcase:
                title_html = f'<div class="code-title">{title}</div>' if title else ''
                
                html_output = f'''
                <div class="code-showcase-{cid} {final_cls}">
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
                    .code-showcase-{cid} .code-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
                    .code-showcase-{cid} .code-dot.red {{ background: #ff5f56; }}
                    .code-showcase-{cid} .code-dot.yellow {{ background: #ffbd2e; }}
                    .code-showcase-{cid} .code-dot.green {{ background: #27c93f; }}
                    
                    .code-showcase-{cid} .code-title {{
                        position: absolute; top: 12px; right: 20px; color: #666; font-family: sans-serif; font-size: 0.8rem; z-index: 1;
                    }}
                    
                    .code-showcase-{cid} pre {{
                        margin-top: 1.5rem; background: transparent !important; border: none !important; padding: 0 !important;
                    }}
                    .code-showcase-{cid} code {{
                        color: #d4d4d4 !important; font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.95rem; line-height: 1.8;
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
                <div class="rel {final_cls}">
                    <style>{line_num_style}</style>
                    {copy_btn_html}
                    <pre class="bg:bg-card p:1rem r:0.5rem b:1|solid|border overflow-x:auto m:0">
                        <code class="{lang_class} color:text font:mono font-size:0.9rem lh:1.6">{escaped_code}</code>
                    </pre>
                </div>
                '''
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def divider(self, cls: str = "", **kwargs):
        """Display horizontal divider"""
        cid = self._get_next_cid("divider")
        def builder():
            final_cls = build_cls(f"divider {cls}", **kwargs)
            return Component("sl-divider", id=cid, class_=final_cls)
        self._register_component(cid, builder)

    def success(self, body, icon="check-circle", cls: str = "", **kwargs):
        """Display success message"""
        self._alert(body, "success", icon, cls, **kwargs)

    def info(self, body, icon="info-circle", cls: str = "", **kwargs):
        """Display info message"""
        self._alert(body, "primary", icon, cls, **kwargs)

    def warning(self, body, icon="exclamation-triangle", cls: str = "", **kwargs):
        """Display warning message"""
        self._alert(body, "warning", icon, cls, **kwargs)

    def error(self, body, icon="exclamation-octagon", cls: str = "", **kwargs):
        """Display error message"""
        self._alert(body, "danger", icon, cls, **kwargs)

    def _alert(self, body, variant, icon_name, cls: str = "", **kwargs):
        cid = self._get_next_cid("alert")
        def builder():
            icon_html = f'<sl-icon slot="icon" name="{icon_name}"></sl-icon>'
            final_cls = build_cls(f"mb:1rem {cls}", **kwargs)
            html = f'<sl-alert variant="{variant}" open class="{final_cls}">{icon_html}{body}</sl-alert>'
            return Component("div", id=cid, content=html)
        self._register_component(cid, builder)
