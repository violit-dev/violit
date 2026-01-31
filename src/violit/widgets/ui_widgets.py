"""
UI Widgets - General purpose UI components using Shoelace
"""

from typing import Union, Callable, Optional, List
from ..component import Component
from ..context import rendering_ctx
from ..state import State
from ..style_utils import build_cls, get_variant_styles


class UIWidgetsMixin:
    """General purpose UI widgets based on Shoelace components"""
    
    def link(self, text: str, url: str, icon: str = None, new_tab: bool = True, 
             variant: str = "primary", size: str = None, cls: str = "", **kwargs):
        """External link"""
        cid = self._get_next_cid("link")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            target = 'target="_blank" rel="noopener noreferrer"' if new_tab else ''
            
            # Map legacy variants to Master CSS
            base_styles = "text-decoration:none"
            variant_cls = ""
            if variant == "primary":
                variant_cls = "color:primary-600"
            elif variant == "muted":
                variant_cls = "color:neutral-500"
            
            # Build final class string
            final_cls = build_cls(cls, size=size, **kwargs)
            if variant_cls:
                final_cls = f"{variant_cls} {final_cls}"
            
            icon_html = f'<sl-icon name="{icon}" style="margin-right: 0.25rem;"></sl-icon>' if icon else ''
            # Use style for text-decoration as it's safer, classes for colors/sizes
            html = f'<a href="{url}" {target} class="{final_cls}" style="{base_styles}">{icon_html}{text}</a>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def link_button(self, text: str, url: str, icon: str = None, new_tab: bool = True,
                    variant: str = "primary", size: str = "medium", outline: bool = False,
                    cls: str = "", **kwargs):
        """Button-styled external link"""
        cid = self._get_next_cid("link_btn")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            target = 'target="_blank"' if new_tab else ''
            outline_attr = 'outline' if outline else ''
            icon_html = f'<sl-icon slot="prefix" name="{icon}"></sl-icon>' if icon else ''
            
            final_cls = build_cls(cls, **kwargs)
            
            html = f'''<sl-button href="{url}" {target} variant="{variant}" size="{size}" {outline_attr} class="{final_cls}">
                {icon_html}{text}
            </sl-button>'''
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def avatar(self, image: str = None, initials: str = None, label: str = None,
               size: str = None, shape: str = "circle", cls: str = "", **kwargs):
        """User avatar"""
        cid = self._get_next_cid("avatar")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = []
            if image: attrs.append(f'image="{image}"')
            if initials: attrs.append(f'initials="{initials}"')
            if label: attrs.append(f'label="{label}"')
            
            # Shoelace avatar styling via CSS variables
            style_parts = []
            if size: style_parts.append(f"--size: {size}")
            
            if shape == "square":
                kwargs['r'] = 0
            elif shape == "rounded":
                kwargs['r'] = "8px"
                
            final_cls = build_cls(cls, **kwargs)
            style_attr = f'style="{"; ".join(style_parts)}"' if style_parts else ''
            
            html = f'<sl-avatar {" ".join(attrs)} class="{final_cls}" {style_attr}></sl-avatar>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def tag(self, text: str, variant: str = "neutral", size: str = "medium",
            removable: bool = False, pill: bool = False, cls: str = "", **kwargs):
        """Tag/Chip component"""
        cid = self._get_next_cid("tag")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = [f'variant="{variant}"', f'size="{size}"']
            if removable: attrs.append('removable')
            if pill: attrs.append('pill')
            
            final_cls = build_cls(cls, **kwargs)
            
            html = f'<sl-tag {" ".join(attrs)} class="{final_cls}">{text}</sl-tag>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def tooltip(self, content: str, text: str = None, placement: str = "top",
                trigger: str = "hover", cls: str = "", **kwargs):
        """Tooltip wrapper"""
        cid = self._get_next_cid("tooltip")
        
        def builder():
            token = rendering_ctx.set(cid)
            final_cls = build_cls(cls, **kwargs)
            
            if text:
                html = f'''<sl-tooltip content="{content}" placement="{placement}" trigger="{trigger}" class="{final_cls}">
                    <span>{text}</span>
                </sl-tooltip>'''
            else:
                html = f'<sl-tooltip content="{content}" placement="{placement}" trigger="{trigger}" class="{final_cls}"></sl-tooltip>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def rating(self, value: float = 0, max_value: int = 5, readonly: bool = True,
               precision: float = 1, size: str = None, key: str = None,
               on_change: Callable = None, cls: str = "", **kwargs):
        """Star rating widget"""
        cid = self._get_next_cid("rating")
        
        if readonly:
            def builder():
                token = rendering_ctx.set(cid)
                style = f'style="--symbol-size: {size};"' if size else ''
                readonly_attr = 'readonly' if readonly else ''
                final_cls = build_cls(cls, **kwargs)
                
                html = f'<sl-rating value="{value}" max="{max_value}" precision="{precision}" {readonly_attr} {style} class="{final_cls}"></sl-rating>'
                
                rendering_ctx.reset(token)
                return Component("span", id=cid, content=html)
            
            self._register_component(cid, builder)
        else:
            state_key = key or f"rating:{cid}"
            s = self.state(value, key=state_key)
            
            def action(v):
                try:
                    s.set(float(v))
                    if on_change: on_change(float(v))
                except ValueError: pass
            
            def builder():
                token = rendering_ctx.set(cid)
                cv = s.value
                rendering_ctx.reset(token)
                
                style = f'style="--symbol-size: {size};"' if size else ''
                final_cls = build_cls(cls, **kwargs)
                
                if self.mode == 'lite':
                    attrs = f'hx-post="/action/{cid}" hx-trigger="sl-change" hx-swap="none" hx-vals="js:{{value: event.target.value}}"'
                else:
                    attrs = f'onsl-change="window.sendAction(\'{cid}\', this.value)"'
                
                html = f'<sl-rating id="{cid}" value="{cv}" max="{max_value}" precision="{precision}" {style} {attrs} class="{final_cls}"></sl-rating>'
                
                return Component("span", id=cid, content=html)
            
            self._register_component(cid, builder, action=action)
            return s
    
    def copy_button(self, text: str, label: str = None, size: str = "medium", cls: str = "", **kwargs):
        """Copy to clipboard button"""
        cid = self._get_next_cid("copy")
        
        def builder():
            token = rendering_ctx.set(cid)
            import html as html_lib
            escaped_text = html_lib.escape(text)
            
            final_cls = build_cls(cls, **kwargs)
            label_html = f'<span style="margin-left: 0.5rem;">{label}</span>' if label else ''
            html = f'<sl-copy-button value="{escaped_text}" size="{size}" class="{final_cls}">{label_html}</sl-copy-button>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def breadcrumb(self, items: List[Union[str, dict]], separator: str = None, cls: str = "", **kwargs):
        """Breadcrumb navigation"""
        cid = self._get_next_cid("breadcrumb")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            separator_html = f'<sl-icon slot="separator" name="{separator}"></sl-icon>' if separator else ''
            final_cls = build_cls(cls, **kwargs)
            
            items_html = []
            for item in items:
                if isinstance(item, str):
                    items_html.append(f'<sl-breadcrumb-item>{item}</sl-breadcrumb-item>')
                else:
                    label = item.get('label', '')
                    url = item.get('url')
                    if url:
                        items_html.append(f'<sl-breadcrumb-item href="{url}">{label}</sl-breadcrumb-item>')
                    else:
                        items_html.append(f'<sl-breadcrumb-item>{label}</sl-breadcrumb-item>')
            
            html = f'<sl-breadcrumb class="{final_cls}">{separator_html}{"".join(items_html)}</sl-breadcrumb>'
            
            rendering_ctx.reset(token)
            return Component("nav", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def skeleton(self, variant: str = "paragraph", lines: int = 3, effect: str = "sheen", cls: str = "", **kwargs):
        """Loading skeleton placeholder"""
        cid = self._get_next_cid("skeleton")
        
        def builder():
            token = rendering_ctx.set(cid)
            final_cls = build_cls(cls, **kwargs)
            
            if variant == "paragraph":
                skeletons = []
                for i in range(lines):
                    width = "100%" if i < lines - 1 else "75%"
                    skeletons.append(f'<sl-skeleton effect="{effect}" style="width: {width}; margin-bottom: 0.5rem;"></sl-skeleton>')
                html = f'<div class="{final_cls}">{"".join(skeletons)}</div>'
            elif variant == "card":
                # Use Master CSS for card skeleton layout
                html = f'''<div class="b:1|solid|neutral-200 r:8 p:1rem {final_cls}">
                    <sl-skeleton effect="{effect}" style="width: 40%; height: 1.5rem; margin-bottom: 1rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 100%; margin-bottom: 0.5rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 100%; margin-bottom: 0.5rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 75%;"></sl-skeleton>
                </div>'''
            elif variant == "avatar":
                html = f'<sl-skeleton effect="{effect}" style="width: 48px; height: 48px; border-radius: 50%;" class="{final_cls}"></sl-skeleton>'
            elif variant == "button":
                html = f'<sl-skeleton effect="{effect}" style="width: 100px; height: 40px; border-radius: 4px;" class="{final_cls}"></sl-skeleton>'
            else:
                html = f'<sl-skeleton effect="{effect}" class="{final_cls}"></sl-skeleton>'
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def details(self, summary: str, content: str = None, open: bool = False, cls: str = "", **kwargs):
        """Collapsible details section"""
        cid = self._get_next_cid("details")
        
        def builder():
            token = rendering_ctx.set(cid)
            final_cls = build_cls(cls, **kwargs)
            open_attr = 'open' if open else ''
            html = f'<sl-details summary="{summary}" {open_attr} class="{final_cls}">{content or ""}</sl-details>'
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def divider_text(self, text: str, cls: str = "", **kwargs):
        """Divider with text label"""
        cid = self._get_next_cid("divider_text")
        
        def builder():
            token = rendering_ctx.set(cid)
            final_cls = build_cls(cls, **kwargs)
            
            # Using Master CSS for layout
            html = f'''<div class="flex ai:center gap:1rem my:1.5rem {final_cls}">
                <div class="flex:1 h:1 bg:neutral-200"></div>
                <span class="color:neutral-500 font-size:0.875rem">{text}</span>
                <div class="flex:1 h:1 bg:neutral-200"></div>
            </div>'''
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def box(self, padding: str = None, margin: str = None, background: str = None,
            border: str = None, radius: str = None, shadow: str = None,
            center: bool = False, gradient: str = None, variant: str = None,
            animation: str = None, cls: str = "", **kwargs):
        """Styled container box"""
        return BoxContext(self, padding, margin, background, border, radius, shadow, center, gradient, variant, animation, cls, **kwargs)
    
    def spacer(self, height: str = "1rem"):
        """Vertical spacer"""
        cid = self._get_next_cid("spacer")
        
        def builder():
            return Component("div", id=cid, style=f"height: {height};")
        
        self._register_component(cid, builder)


class BoxContext:
    """Context manager for styled box container"""
    
    def __init__(self, app, padding, margin, background, border, radius, shadow, center, gradient, variant=None, animation=None, cls="", **kwargs):
        self.app = app
        # Extract style BEFORE storing kwargs (safe for multiple renders)
        self.user_style = kwargs.pop('style', '')
        self.kwargs = kwargs
        self.padding = padding
        self.margin = margin
        self.background = background
        self.border = border
        self.radius = radius
        self.shadow = shadow
        self.center = center
        self.gradient = gradient
        self.variant = variant
        self.animation = animation
        self.cls = cls
        self.cid = app._get_next_cid("box")
        self.token = None
    
    def __enter__(self):
        def builder():
            from ..state import get_session_store
            store = get_session_store()
            
            # Render child components
            htmls = []
            for cid, b in self.app.static_fragment_components.get(self.cid, []):
                htmls.append(b().render())
            for cid, b in store['fragment_components'].get(self.cid, []):
                htmls.append(b().render())
            
            token = rendering_ctx.set(self.cid)
            
            # 1. Get Variant Styles (Predefined Master CSS classes)
            variant_cls = get_variant_styles(self.variant) if self.variant else ""
            
            # 2. Handle Custom Animations (Keep existing logic for complex animations)
            style_tag = ""
            if self.variant == "hero" and (self.animation == "pulse" or self.animation is None):
                style_tag = f'''
                <style>
                .box-{self.cid}::before {{
                    content: '';
                    position: absolute;
                    top: -50%; left: -50%;
                    width: 200%; height: 200%;
                    background: radial-gradient(circle, rgba(138, 43, 226, 0.1) 0%, transparent 60%);
                    animation: box-pulse-{self.cid} 8s ease-in-out infinite;
                    z-index: 0;
                }}
                @keyframes box-pulse-{self.cid} {{
                    0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                    50% {{ transform: scale(1.1); opacity: 0.8; }}
                }}
                .box-{self.cid} > * {{ position: relative; z-index: 1; }}
                </style>
                '''
            
            # 3. Build Semantic Props into Master CSS
            # Merge explicit props with kwargs to avoid duplicate argument errors
            build_props = self.kwargs.copy()
            
            if self.padding is not None: build_props['p'] = self.padding
            if self.margin is not None: build_props['m'] = self.margin
            if self.background is not None: build_props['bg'] = self.background
            if self.border is not None: build_props['b'] = self.border
            if self.radius is not None: build_props['r'] = self.radius
            if self.shadow is not None: build_props['shadow'] = self.shadow
            if self.center: build_props['center'] = self.center

            semantic_cls = build_cls(self.cls, **build_props)
            
            # Handle gradient specifically (as it's often complex)
            gradient_style = ""
            if self.gradient:
                if self.gradient == "primary":
                    semantic_cls += " bg:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(168,85,247,0.05))"
                elif self.gradient == "success":
                    semantic_cls += " bg:linear-gradient(135deg,rgba(34,197,94,0.1),rgba(74,222,128,0.05))"
                elif self.gradient == "danger":
                    semantic_cls += " bg:linear-gradient(135deg,rgba(239,68,68,0.1),rgba(248,113,113,0.05))"
                else:
                    # Custom gradient string - use style attribute to be safe or try Master CSS
                    gradient_style = f"background: {self.gradient};"

            content = style_tag + "".join(htmls)
            
            # Combine all classes
            final_cls = f"box-{self.cid} {variant_cls} {semantic_cls}".strip()
            
            # Combine gradient_style with user_style
            final_style = f"{gradient_style} {self.user_style}".strip() if (gradient_style or self.user_style) else ""
            
            rendering_ctx.reset(token)
            return Component("div", id=self.cid, content=content, class_=final_cls, style=final_style if final_style else None)
        
        self.app._register_component(self.cid, builder)
        
        from ..context import fragment_ctx
        self.token = fragment_ctx.set(self.cid)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import fragment_ctx
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        return getattr(self.app, name)
