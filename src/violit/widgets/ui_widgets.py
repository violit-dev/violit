"""
UI Widgets - General purpose UI components using Shoelace
"""

from typing import Union, Callable, Optional, List
from ..component import Component
from ..context import rendering_ctx
from ..state import State


class UIWidgetsMixin:
    """General purpose UI widgets based on Shoelace components"""
    
    def link(self, text: str, url: str, icon: str = None, new_tab: bool = True, 
             variant: str = None, size: str = None):
        """External link
        
        Args:
            text: Link text
            url: Target URL
            icon: Optional icon name (Shoelace icons)
            new_tab: Open in new tab (default True)
            variant: Style variant ('primary', 'neutral', 'muted')
            size: Text size ('small', 'medium', 'large')
        """
        cid = self._get_next_cid("link")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            target = 'target="_blank" rel="noopener noreferrer"' if new_tab else ''
            
            # Build style
            styles = ["text-decoration: none"]
            if variant == "primary":
                styles.append("color: var(--sl-color-primary-600)")
            elif variant == "muted":
                styles.append("color: var(--sl-color-neutral-500)")
            else:
                styles.append("color: var(--sl-color-primary-600)")
            
            if size == "small":
                styles.append("font-size: 0.875rem")
            elif size == "large":
                styles.append("font-size: 1.125rem")
            
            style_str = "; ".join(styles)
            
            icon_html = f'<sl-icon name="{icon}" style="margin-right: 0.25rem;"></sl-icon>' if icon else ''
            html = f'<a href="{url}" {target} style="{style_str}">{icon_html}{text}</a>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def link_button(self, text: str, url: str, icon: str = None, new_tab: bool = True,
                    variant: str = "primary", size: str = "medium", outline: bool = False):
        """Button-styled external link
        
        Args:
            text: Button text
            url: Target URL
            icon: Optional icon name
            new_tab: Open in new tab
            variant: Button variant ('primary', 'success', 'neutral', 'warning', 'danger')
            size: Button size ('small', 'medium', 'large')
            outline: Use outline style
        """
        cid = self._get_next_cid("link_btn")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            target = 'target="_blank"' if new_tab else ''
            outline_attr = 'outline' if outline else ''
            icon_html = f'<sl-icon slot="prefix" name="{icon}"></sl-icon>' if icon else ''
            
            html = f'''<sl-button href="{url}" {target} variant="{variant}" size="{size}" {outline_attr}>
                {icon_html}{text}
            </sl-button>'''
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def avatar(self, image: str = None, initials: str = None, label: str = None,
               size: str = None, shape: str = "circle"):
        """User avatar
        
        Args:
            image: Image URL
            initials: Initials to display (if no image)
            label: Accessibility label
            size: Size in CSS units (e.g., '48px', '3rem')
            shape: 'circle', 'square', or 'rounded'
        """
        cid = self._get_next_cid("avatar")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = []
            if image:
                attrs.append(f'image="{image}"')
            if initials:
                attrs.append(f'initials="{initials}"')
            if label:
                attrs.append(f'label="{label}"')
            
            style_parts = []
            if size:
                style_parts.append(f"--size: {size}")
            if shape == "square":
                style_parts.append("border-radius: 0")
            elif shape == "rounded":
                style_parts.append("border-radius: 8px")
            
            style_attr = f'style="{"; ".join(style_parts)}"' if style_parts else ''
            
            html = f'<sl-avatar {" ".join(attrs)} {style_attr}></sl-avatar>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def tag(self, text: str, variant: str = "neutral", size: str = "medium",
            removable: bool = False, pill: bool = False):
        """Tag/Chip component
        
        Args:
            text: Tag text
            variant: Color variant ('primary', 'success', 'neutral', 'warning', 'danger')
            size: Tag size ('small', 'medium', 'large')
            removable: Show remove button
            pill: Pill shape
        """
        cid = self._get_next_cid("tag")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = [f'variant="{variant}"', f'size="{size}"']
            if removable:
                attrs.append('removable')
            if pill:
                attrs.append('pill')
            
            html = f'<sl-tag {" ".join(attrs)}>{text}</sl-tag>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def tooltip(self, content: str, text: str = None, placement: str = "top",
                trigger: str = "hover"):
        """Tooltip wrapper
        
        Args:
            content: Tooltip content
            text: Text to wrap with tooltip (if not using as context manager)
            placement: Tooltip placement ('top', 'bottom', 'left', 'right')
            trigger: Trigger method ('hover', 'click', 'focus')
        """
        cid = self._get_next_cid("tooltip")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            if text:
                html = f'''<sl-tooltip content="{content}" placement="{placement}" trigger="{trigger}">
                    <span>{text}</span>
                </sl-tooltip>'''
            else:
                html = f'<sl-tooltip content="{content}" placement="{placement}" trigger="{trigger}"></sl-tooltip>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def rating(self, value: float = 0, max_value: int = 5, readonly: bool = True,
               precision: float = 1, size: str = None, key: str = None,
               on_change: Callable = None):
        """Star rating widget
        
        Args:
            value: Current rating value
            max_value: Maximum rating
            readonly: Read-only mode
            precision: Rating precision (0.5 for half stars)
            size: Icon size in CSS units
            key: State key
            on_change: Callback on rating change
        """
        cid = self._get_next_cid("rating")
        
        if readonly:
            # Static rating display
            def builder():
                token = rendering_ctx.set(cid)
                
                style = f'style="--symbol-size: {size};"' if size else ''
                readonly_attr = 'readonly' if readonly else ''
                
                html = f'<sl-rating value="{value}" max="{max_value}" precision="{precision}" {readonly_attr} {style}></sl-rating>'
                
                rendering_ctx.reset(token)
                return Component("span", id=cid, content=html)
            
            self._register_component(cid, builder)
        else:
            # Interactive rating
            state_key = key or f"rating:{cid}"
            s = self.state(value, key=state_key)
            
            def action(v):
                try:
                    s.set(float(v))
                    if on_change:
                        on_change(float(v))
                except ValueError:
                    pass
            
            def builder():
                token = rendering_ctx.set(cid)
                cv = s.value
                rendering_ctx.reset(token)
                
                style = f'style="--symbol-size: {size};"' if size else ''
                
                if self.mode == 'lite':
                    attrs = f'hx-post="/action/{cid}" hx-trigger="sl-change" hx-swap="none" hx-vals="js:{{value: event.target.value}}"'
                else:
                    attrs = f'onsl-change="window.sendAction(\'{cid}\', this.value)"'
                
                html = f'<sl-rating id="{cid}" value="{cv}" max="{max_value}" precision="{precision}" {style} {attrs}></sl-rating>'
                
                return Component("span", id=cid, content=html)
            
            self._register_component(cid, builder, action=action)
            return s
    
    def copy_button(self, text: str, label: str = None, size: str = "medium"):
        """Copy to clipboard button
        
        Args:
            text: Text to copy
            label: Button label
            size: Button size
        """
        cid = self._get_next_cid("copy")
        
        def builder():
            token = rendering_ctx.set(cid)
            import html as html_lib
            escaped_text = html_lib.escape(text)
            
            label_html = f'<span style="margin-left: 0.5rem;">{label}</span>' if label else ''
            html = f'<sl-copy-button value="{escaped_text}" size="{size}">{label_html}</sl-copy-button>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def breadcrumb(self, items: List[Union[str, dict]], separator: str = None):
        """Breadcrumb navigation
        
        Args:
            items: List of strings or dicts with 'label' and optional 'url'
            separator: Separator character (default: '/')
        """
        cid = self._get_next_cid("breadcrumb")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            separator_html = f'<sl-icon slot="separator" name="{separator}"></sl-icon>' if separator else ''
            
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
            
            html = f'<sl-breadcrumb>{separator_html}{"".join(items_html)}</sl-breadcrumb>'
            
            rendering_ctx.reset(token)
            return Component("nav", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def skeleton(self, variant: str = "paragraph", lines: int = 3, effect: str = "sheen"):
        """Loading skeleton placeholder
        
        Args:
            variant: Skeleton type ('paragraph', 'card', 'avatar', 'button')
            lines: Number of lines for paragraph variant
            effect: Animation effect ('sheen', 'pulse', 'none')
        """
        cid = self._get_next_cid("skeleton")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            if variant == "paragraph":
                skeletons = []
                for i in range(lines):
                    width = "100%" if i < lines - 1 else "75%"
                    skeletons.append(f'<sl-skeleton effect="{effect}" style="width: {width}; margin-bottom: 0.5rem;"></sl-skeleton>')
                html = f'<div>{"".join(skeletons)}</div>'
            elif variant == "card":
                html = f'''<div style="border: 1px solid var(--sl-color-neutral-200); border-radius: 8px; padding: 1rem;">
                    <sl-skeleton effect="{effect}" style="width: 40%; height: 1.5rem; margin-bottom: 1rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 100%; margin-bottom: 0.5rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 100%; margin-bottom: 0.5rem;"></sl-skeleton>
                    <sl-skeleton effect="{effect}" style="width: 75%;"></sl-skeleton>
                </div>'''
            elif variant == "avatar":
                html = f'<sl-skeleton effect="{effect}" style="width: 48px; height: 48px; border-radius: 50%;"></sl-skeleton>'
            elif variant == "button":
                html = f'<sl-skeleton effect="{effect}" style="width: 100px; height: 40px; border-radius: 4px;"></sl-skeleton>'
            else:
                html = f'<sl-skeleton effect="{effect}"></sl-skeleton>'
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def details(self, summary: str, content: str = None, open: bool = False):
        """Collapsible details section (Shoelace sl-details)
        
        Args:
            summary: Summary text (always visible)
            content: Collapsible content
            open: Whether to start open
        """
        cid = self._get_next_cid("details")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            open_attr = 'open' if open else ''
            html = f'<sl-details summary="{summary}" {open_attr}>{content or ""}</sl-details>'
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def divider_text(self, text: str):
        """Divider with text label
        
        Args:
            text: Label text to display in divider
        """
        cid = self._get_next_cid("divider_text")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            html = f'''<div style="display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0;">
                <div style="flex: 1; height: 1px; background: var(--sl-color-neutral-200);"></div>
                <span style="color: var(--sl-color-neutral-500); font-size: 0.875rem;">{text}</span>
                <div style="flex: 1; height: 1px; background: var(--sl-color-neutral-200);"></div>
            </div>'''
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def box(self, padding: str = None, margin: str = None, background: str = None,
            border: str = None, radius: str = None, shadow: str = None,
            center: bool = False, gradient: str = None, variant: str = None,
            animation: str = None, **kwargs):
        """Styled container box
        
        Args:
            padding: CSS padding
            margin: CSS margin
            background: Background color
            border: Border style
            radius: Border radius
            shadow: Box shadow ('sm', 'md', 'lg', 'xl' or custom CSS)
            center: Center content
            gradient: Gradient background (e.g., 'primary', 'success', or CSS gradient)
            variant: Preset style variant:
                - 'hero': Landing page hero section with animated background
                - 'cta': Call-to-action section
                - 'stat': Statistics card
                - 'footer': Page footer
            animation: Animation effect ('pulse', 'fade-in')
            **kwargs: Additional attributes (e.g., onmouseover, style, class_)
        
        Returns:
            Context manager for content
        """
        return BoxContext(self, padding, margin, background, border, radius, shadow, center, gradient, variant, animation, **kwargs)
    
    def spacer(self, height: str = "1rem"):
        """Vertical spacer
        
        Args:
            height: Spacer height in CSS units
        """
        cid = self._get_next_cid("spacer")
        
        def builder():
            return Component("div", id=cid, style=f"height: {height};")
        
        self._register_component(cid, builder)


class BoxContext:
    """Context manager for styled box container"""
    
    def __init__(self, app, padding, margin, background, border, radius, shadow, center, gradient, variant=None, animation=None, **kwargs):
        self.app = app
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
        self.cid = app._get_next_cid("box")
        self.token = None
    
    def __enter__(self):
        # Register builder BEFORE entering context (like ContainerContext)
        def builder():
            from ..state import get_session_store
            store = get_session_store()
            
            # Render child components
            htmls = []
            # Static first
            for cid, b in self.app.static_fragment_components.get(self.cid, []):
                htmls.append(b().render())
            # Dynamic next
            for cid, b in store['fragment_components'].get(self.cid, []):
                htmls.append(b().render())
            
            token = rendering_ctx.set(self.cid)
            
            # Apply variant presets
            v_padding = self.padding
            v_margin = self.margin
            v_background = self.background
            v_border = self.border
            v_radius = self.radius
            v_shadow = self.shadow
            v_center = self.center
            v_gradient = self.gradient
            style_tag = ""
            
            if self.variant == "hero":
                v_padding = v_padding or "4rem 2rem"
                v_margin = v_margin or "0 0 3rem 0"
                v_radius = v_radius or "24px"
                v_center = True
                # Beautiful violet gradient that works on both dark and light themes
                v_gradient = v_gradient or "linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(168, 85, 247, 0.12) 25%, rgba(192, 132, 252, 0.08) 50%, rgba(216, 180, 254, 0.1) 75%, rgba(139, 92, 246, 0.12) 100%)"
                
                if self.animation == "pulse" or self.animation is None:
                    style_tag = f'''
                    <style>
                    .box-{self.cid} {{
                        position: relative;
                        overflow: hidden;
                    }}
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
                    
            elif self.variant == "cta":
                v_padding = v_padding or "4rem 2rem"
                v_margin = v_margin or "3rem 0"
                v_radius = v_radius or "24px"
                v_center = True
                v_gradient = v_gradient or "linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(217, 70, 239, 0.1) 100%)"
                
            elif self.variant == "stat":
                v_padding = v_padding or "2rem"
                v_radius = v_radius or "16px"
                v_center = True
                v_gradient = v_gradient or "linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%)"
                v_border = v_border or "1px solid rgba(139, 92, 246, 0.2)"
                
            elif self.variant == "glass":
                v_padding = v_padding or "2rem"
                v_radius = v_radius or "16px"
                # Glass effect defaults (light mode optimized, can be overridden by kwargs style)
                # We use specific style injection because backdrop-filter isn't a standard 'background' prop
                style_tag = f'''
                <style>
                .box-{self.cid} {{
                    background: rgba(255, 255, 255, 0.7);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.5);
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
                }}
                /* Dark mode adjustment if app theme is dark (basic detection via parent class often needed, 
                   but here we set a safe default or assume light/hybrid usage. 
                   For generic support, we stick to white-transparent glass which looks good on colors.) */
                </style>
                '''
                
            elif self.variant == "footer":
                v_padding = v_padding or "3rem 0"
                v_margin = v_margin or "4rem 0 0 0"
                v_center = True
                v_border = v_border or "none"
                style_tag = f'''
                <style>
                .box-{self.cid} {{
                    border-top: 1px solid var(--sl-color-neutral-200) !important;
                }}
                </style>
                '''
            
            styles = []
            if v_padding:
                styles.append(f"padding: {v_padding}")
            if v_margin:
                styles.append(f"margin: {v_margin}")
            if v_radius:
                styles.append(f"border-radius: {v_radius}")
            
            if v_gradient:
                if v_gradient == "primary":
                    styles.append("background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(168, 85, 247, 0.05))")
                elif v_gradient == "success":
                    styles.append("background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(74, 222, 128, 0.05))")
                elif v_gradient == "danger":
                    styles.append("background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(248, 113, 113, 0.05))")
                else:
                    styles.append(f"background: {v_gradient}")
            elif v_background:
                styles.append(f"background: {v_background}")
            
            if v_border:
                styles.append(f"border: {v_border}")
            
            if v_shadow:
                if v_shadow == "sm":
                    styles.append("box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05)")
                elif v_shadow == "md":
                    styles.append("box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)")
                elif v_shadow == "lg":
                    styles.append("box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1)")
                elif v_shadow == "xl":
                    styles.append("box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1)")
                else:
                    styles.append(f"box-shadow: {v_shadow}")
            
            if v_center:
                styles.append("text-align: center")
            
            # Merge custom styles from kwargs
            if 'style' in self.kwargs:
                styles.append(self.kwargs.pop('style'))
            
            content = style_tag + "".join(htmls)
            box_class = f"box-{self.cid}" if self.variant else ""
            
            # Merge custom class
            if 'class_' in self.kwargs:
                custom_class = self.kwargs.pop('class_')
                box_class = f"{box_class} {custom_class}".strip()
            
            rendering_ctx.reset(token)
            return Component("div", id=self.cid, content=content, style="; ".join(styles), class_=box_class, **self.kwargs)
        
        self.app._register_component(self.cid, builder)
        
        # Now set fragment context for children
        from ..context import fragment_ctx
        self.token = fragment_ctx.set(self.cid)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import fragment_ctx
        fragment_ctx.reset(self.token)
    
    def __getattr__(self, name):
        return getattr(self.app, name)


# Note: Landing page specialized widgets have been removed.
# Use basic widgets with options instead:
#   - hero() -> box(variant="hero") + html() + link_button()
#   - code_showcase() -> code(showcase=True)
#   - stat_cards() -> columns() + box(variant="stat") + html()
#   - feature_cards() -> columns() + card(hover=True, accent=True)
#   - comparison_table() -> table(styled=True, highlight_row=n, title="...")
#   - theme_gallery() -> html() with custom grid
#   - cta_section() -> box(variant="cta") + html() + link_button()
#   - footer() -> box(variant="footer") + html()

