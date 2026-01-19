from typing import Any, Optional
import html

class Component:
    def __init__(self, tag: Optional[str], id: str, escape_content: bool = False, **props):
        self.tag = tag
        self.id = id
        self.escape_content = escape_content  # XSS protection
        self.props = props

    def render(self) -> str:
        if self.tag is None:
            content = str(self.props.get('content', ''))
            # Escape content if enabled
            return html.escape(content) if self.escape_content else content
            
        attrs = []
        for k, v in self.props.items():
            if k == 'content': continue
            clean_k = k.replace('_', '-') if not k.startswith('on') else k
            if clean_k.startswith('on'):
                attrs.append(f'{clean_k}="{v}"')
            else:
                if v is True: attrs.append(clean_k)
                elif v is False or v is None: continue
                else: 
                    # Escape attribute values for XSS protection
                    escaped_v = html.escape(str(v), quote=True)
                    attrs.append(f'{clean_k}="{escaped_v}"')
        
        props_str = " ".join(attrs)
        content = self.props.get('content', '')
        
        # Escape content if enabled
        if self.escape_content:
            content = html.escape(str(content))
        
        return f"<{self.tag} id=\"{self.id}\" {props_str}>{content}</{self.tag}>"
