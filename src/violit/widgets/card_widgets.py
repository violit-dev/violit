"""
Card Widgets - Shoelace Card Components
Provides easy-to-use wrappers for Shoelace card components
"""

from ..component import Component
from ..context import rendering_ctx


class CardWidgetsMixin:
    """Mixin for Shoelace Card components"""
    
    def card(self, content=None, header=None, footer=None, **kwargs):
        """
        Create a Shoelace card component
        
        Args:
            content: Optional card content (str). If None, use as context manager
            header: Optional header content (str)
            footer: Optional footer content (str)
            **kwargs: Additional attributes (e.g., data_post_id="123", class_="custom")
        
        Returns:
            CardContext if content is None, otherwise None
        
        Examples:
            # Simple card with content
            app.card("Hello World!")
            
            # Card with header and footer
            app.card("Content", header="Title", footer="Footer text")
            
            # Context manager for complex content
            with app.card(header="My Card"):
                app.text("Line 1")
                app.text("Line 2")
            
            # With custom attributes
            with app.card(data_post_id="123", class_="custom-card"):
                app.text("Content")
        """
        cid = self._get_next_cid("card")
        
        # Convert kwargs to HTML attributes
        attrs = []
        for key, value in kwargs.items():
            # Convert Python naming to HTML attributes
            attr_name = key.replace('_', '-')
            attrs.append(f'{attr_name}="{value}"')
        
        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        
        if content is None:
            # Context manager mode
            return CardContext(self, cid, header, footer, attrs_str)
        else:
            # Direct content mode
            def builder():
                token = rendering_ctx.set(cid)
                
                try:
                    # Handle callable content (Lambda support for content, header, and footer)
                    current_content = content
                    if callable(content):
                        current_content = content()  # Execute lambda
                    
                    current_header = header
                    if callable(header):
                        current_header = header()
                    
                    current_footer = footer
                    if callable(footer):
                        current_footer = footer()
                    
                    # Set full width for consistency
                    card_style = 'style="width: 100%;"'
                    html_parts = [f'<sl-card{attrs_str} {card_style}>']
                    
                    if current_header:
                        html_parts.append(f'<div slot="header">{current_header}</div>')
                    
                    # Don't wrap content in extra div - user provides styled HTML
                    html_parts.append(str(current_content))
                    
                    if current_footer:
                        html_parts.append(f'<div slot="footer">{current_footer}</div>')
                    
                    html_parts.append('</sl-card>')
                    
                    # Apply full width to wrapper div for consistency
                    return Component("div", id=cid, content=''.join(html_parts), style="width: 100%;")
                finally:
                    rendering_ctx.reset(token)
            
            self._register_component(cid, builder)
    
    def badge(self, text, variant="neutral", pill=False, pulse=False):
        """
        Create a Shoelace badge component
        
        Args:
            text: Badge text
            variant: Badge variant (primary, success, neutral, warning, danger)
            pill: Whether to display as pill shape
            pulse: Whether to show pulse animation
        
        Example:
            app.badge("LIVE", variant="danger", pulse=True)
            app.badge("New", variant="primary", pill=True)
        """
        cid = self._get_next_cid("badge")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = [f'variant="{variant}"']
            if pill:
                attrs.append('pill')
            if pulse:
                attrs.append('pulse')
            
            attrs_str = ' '.join(attrs)
            html = f'<sl-badge {attrs_str}>{text}</sl-badge>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    def icon(self, name, size=None, label=None):
        """
        Create a Shoelace icon component
        
        Args:
            name: Icon name (from Shoelace icon library)
            size: Icon size (e.g., "small", "medium", "large" or CSS value)
            label: Accessibility label
        
        Example:
            app.icon("clock")
            app.icon("heart-fill", size="large", label="Favorite")
        """
        cid = self._get_next_cid("icon")
        
        def builder():
            token = rendering_ctx.set(cid)
            
            attrs = [f'name="{name}"']
            if size:
                attrs.append(f'style="font-size: {size};"' if not size in ['small', 'medium', 'large'] else f'style="font-size: var(--sl-font-size-{size});"')
            if label:
                attrs.append(f'label="{label}"')
            
            attrs_str = ' '.join(attrs)
            html = f'<sl-icon {attrs_str}></sl-icon>'
            
            rendering_ctx.reset(token)
            return Component("span", id=cid, content=html)
        
        self._register_component(cid, builder)
    
    # ============= Predefined Card Themes =============
    
    def live_card(self, content, timestamp=None, post_id=None):
        """
        Create a LIVE card with danger badge and pulse animation
        
        Args:
            content: Card content (will be auto-escaped)
            timestamp: Optional timestamp to display in footer
            post_id: Optional post ID for data attribute
        
        Example:
            app.live_card("Breaking news!", timestamp="2026-01-18 10:30")
            app.live_card(post['content'], post['created_at'], post['id'])
        """
        import html
        escaped_content = html.escape(str(content))
        
        header = '<div><sl-badge variant="danger" pulse><sl-icon name="circle-fill" style="font-size: 0.5rem;"></sl-icon> LIVE</sl-badge></div>'
        footer = None
        if timestamp:
            footer = f'<div style="text-align: right; font-size: 0.85rem; color: var(--sl-color-neutral-600);"><sl-icon name="clock"></sl-icon> {timestamp}</div>'
        
        kwargs = {"style": "margin-bottom: 1rem; width: 100%;"}
        if post_id is not None:
            kwargs["data_post_id"] = str(post_id)
        
        self.card(
            content=f'<div style="font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;">{escaped_content}</div>',
            header=header,
            footer=footer,
            **kwargs
        )
    
    
    def styled_card(self, 
                    content: str,
                    style: str = 'default',
                    header_badge: str = None,
                    header_badge_variant: str = 'neutral',
                    header_text: str = None,
                    footer_text: str = None,
                    data_id: str = None,
                    return_html: bool = False):
        """Styled card with various preset styles
        
        Args:
            content: Card content (auto-escaped)
            style: Card style ('default', 'live', 'admin', 'info', 'warning')
            header_badge: Header badge text
            header_badge_variant: Badge color ('primary', 'success', 'neutral', 'warning', 'danger')
            header_text: Additional header text (e.g., timestamp)
            footer_text: Footer text
            data_id: ID to add as data attribute (for broadcast)
            return_html: If True, return HTML string; if False, register component (for broadcast)
        
        Returns:
            HTML string if return_html=True, otherwise None
        
        Examples:
            # Display on screen
            app.styled_card(
                "Hello world",
                style='live',
                header_badge='LIVE',
                footer_text='2026-01-18'
            )
            
            # Generate HTML for broadcast
            html = app.styled_card(
                "Hello world",
                style='live',
                header_badge='LIVE',
                footer_text='2026-01-18',
                data_id='123',
                return_html=True  # Return HTML only
            )
        """
        import html as html_lib
        escaped_content = html_lib.escape(str(content))
        
        # Style-specific configuration
        styles_config = {
            'live': {
                'content_style': 'font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;',
                'badge_variant': 'danger',
                'badge_pulse': True,
                'badge_icon': 'circle-fill'
            },
            'admin': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'neutral',
                'badge_pill': True,
                'badge_icon': None
            },
            'info': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'primary',
                'badge_icon': 'info-circle'
            },
            'warning': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'warning',
                'badge_icon': 'exclamation-triangle'
            },
            'default': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': header_badge_variant,
                'badge_icon': None
            }
        }
        
        config = styles_config.get(style, styles_config['default'])
        
        # Create header
        header_parts = []
        if header_badge:
            badge_attrs = [f'variant="{config["badge_variant"]}"']
            if config.get('badge_pulse'):
                badge_attrs.append('pulse')
            if config.get('badge_pill'):
                badge_attrs.append('pill')
            
            badge_content = header_badge
            if config.get('badge_icon'):
                badge_content = f'<sl-icon name="{config["badge_icon"]}" style="font-size: 0.5rem;"></sl-icon> {header_badge}'
            
            header_parts.append(f'<sl-badge {" ".join(badge_attrs)}>{badge_content}</sl-badge>')
        
        if header_text:
            header_parts.append(f'<small style="color: var(--sl-color-neutral-500);"><sl-icon name="clock"></sl-icon> {header_text}</small>')
        
        header_html = None
        if header_parts:
            header_html = f'<div style="display: flex; gap: 0.5rem; align-items: center;">{"".join(header_parts)}</div>'
        
        # Create footer
        footer_html = None
        if footer_text:
            footer_html = f'<div style="text-align: right; font-size: 0.85rem; color: var(--sl-color-neutral-600);"><sl-icon name="clock"></sl-icon> {footer_text}</div>'
        
        # If return_html=True, return HTML only (for broadcast)
        if return_html:
            # Data attribute
            data_attr = f' data-post-id="{data_id}"' if data_id else ''
            
            # Wrap header in slot
            header_slot = f'<div slot="header">{header_html}</div>' if header_html else ''
            
            # Wrap footer in slot
            footer_slot = f'<div slot="footer">{footer_html}</div>' if footer_html else ''
            
            # Return full HTML (include wrapper div for layout consistency)
            return f'<div style="width: 100%;"><sl-card{data_attr} style="width: 100%;">{header_slot}<div style="{config["content_style"]}">{escaped_content}</div>{footer_slot}</sl-card></div>'
        
        # Normal mode: register component
        kwargs = {}
        if data_id:
            kwargs['data_post_id'] = str(data_id)
        
        self.card(
            content=f'<div style="{config["content_style"]}">{escaped_content}</div>',
            header=header_html,
            footer=footer_html,
            **kwargs
        )
    
    
    def card_with_actions(self,
                          content: str,
                          style: str = 'default',
                          header_badge: str = None,
                          header_badge_variant: str = 'neutral',
                          header_text: str = None,
                          footer_text: str = None,
                          data_id: str = None):
        """
        Card widget with action buttons
        
        Arranges card and buttons using flexbox, wraps entire thing with data-id.
        
        Args:
            content: Card content
            style: Card style
            header_badge: Header badge
            header_badge_variant: Badge color
            header_text: Additional header text
            footer_text: Footer text
            data_id: data-post-id attribute (for broadcast removal)
        
        Example:
            # Admin page
            app.card_with_actions(
                content=post['content'],
                style='admin',
                header_badge=f'#{post["id"]}',
                header_text=post['created_at'],
                data_id=post['id']
            )
        """
        import html as html_lib
        escaped_content = html_lib.escape(str(content))
        
        # Same style configuration as styled_card
        styles_config = {
            'live': {
                'content_style': 'font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;',
                'badge_variant': 'danger',
                'badge_pulse': True,
                'badge_icon': 'circle-fill'
            },
            'admin': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'neutral',
                'badge_pill': True,
                'badge_icon': None
            },
            'info': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'primary',
                'badge_icon': 'info-circle'
            },
            'warning': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': 'warning',
                'badge_icon': 'exclamation-triangle'
            },
            'default': {
                'content_style': 'white-space: pre-wrap; line-height: 1.5;',
                'badge_variant': header_badge_variant,
                'badge_icon': None
            }
        }
        
        config = styles_config.get(style, styles_config['default'])
        
        # Create header
        header_parts = []
        if header_badge:
            badge_attrs = [f'variant="{config["badge_variant"]}"']
            if config.get('badge_pulse'):
                badge_attrs.append('pulse')
            if config.get('badge_pill'):
                badge_attrs.append('pill')
            
            badge_content = header_badge
            if config.get('badge_icon'):
                badge_content = f'<sl-icon name="{config["badge_icon"]}" style="font-size: 0.5rem;"></sl-icon> {header_badge}'
            
            header_parts.append(f'<sl-badge {" ".join(badge_attrs)}>{badge_content}</sl-badge>')
        
        if header_text:
            header_parts.append(f'<small style="color: var(--sl-color-neutral-500);"><sl-icon name="clock"></sl-icon> {header_text}</small>')
        
        header_html = ''
        if header_parts:
            header_html = f'<div slot="header" style="display: flex; gap: 0.5rem; align-items: center;">{"".join(header_parts)}</div>'
        
        # Create footer
        footer_html = ''
        if footer_text:
            footer_html = f'<div slot="footer"><div style="text-align: right; font-size: 0.85rem; color: var(--sl-color-neutral-600);"><sl-icon name="clock"></sl-icon> {footer_text}</div></div>'
        
        # Data attribute
        data_attr = f' data-post-id="{data_id}"' if data_id else ''
        
        # Arrange card + action area using flexbox layout
        html_content = f'''<div{data_attr} style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem;">
    <div style="flex: 1;">
        <sl-card style="width: 100%;">
            {header_html}
            <div style="{config["content_style"]}">{escaped_content}</div>
            {footer_html}
        </sl-card>
    </div>
</div>'''
        
        # Render with markdown
        self.markdown(html_content)
    
    def info_card(self, content, title=None):
        """
        Create an info card with primary variant
        
        Args:
            content: Card content
            title: Optional title in header
        
        Example:
            app.info_card("Important information", title="Notice")
        """
        header = None
        if title:
            header = f'<div><sl-badge variant="primary"><sl-icon name="info-circle"></sl-icon> {title}</sl-badge></div>'
        
        self.card(
            content=f'<div style="line-height: 1.6;">{content}</div>',
            header=header,
            style="margin-bottom: 1rem;"
        )
    
    def success_card(self, content, title=None):
        """
        Create a success card with success variant
        
        Args:
            content: Card content
            title: Optional title in header
        
        Example:
            app.success_card("Operation completed!", title="Success")
        """
        header = None
        if title:
            header = f'<div><sl-badge variant="success"><sl-icon name="check-circle"></sl-icon> {title}</sl-badge></div>'
        
        self.card(
            content=f'<div style="line-height: 1.6;">{content}</div>',
            header=header,
            style="margin-bottom: 1rem;"
        )
    
    def warning_card(self, content, title=None):
        """
        Create a warning card with warning variant
        
        Args:
            content: Card content
            title: Optional title in header
        
        Example:
            app.warning_card("Please check your settings", title="Warning")
        """
        header = None
        if title:
            header = f'<div><sl-badge variant="warning"><sl-icon name="exclamation-triangle"></sl-icon> {title}</sl-badge></div>'
        
        self.card(
            content=f'<div style="line-height: 1.6;">{content}</div>',
            header=header,
            style="margin-bottom: 1rem;"
        )
    
    def danger_card(self, content, title=None):
        """
        Create a danger card with danger variant
        
        Args:
            content: Card content
            title: Optional title in header
        
        Example:
            app.danger_card("Critical error occurred", title="Error")
        """
        header = None
        if title:
            header = f'<div><sl-badge variant="danger"><sl-icon name="x-circle"></sl-icon> {title}</sl-badge></div>'
        
        self.card(
            content=f'<div style="line-height: 1.6;">{content}</div>',
            header=header,
            style="margin-bottom: 1rem;"
        )


class CardContext:
    """Context manager for card with complex content"""
    
    def __init__(self, app, cid, header, footer, attrs_str):
        self.app = app
        self.cid = cid
        self.header = header
        self.footer = footer
        self.attrs_str = attrs_str
        self.components = []
    
    def __enter__(self):
        from ..context import layout_ctx
        self.token = layout_ctx.set(f"card_{self.cid}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        from ..context import layout_ctx
        from ..state import get_session_store
        
        # Collect all components added inside this context
        store = get_session_store()
        card_components = []
        
        # Get components that were added in this context
        for comp_cid in store['order']:
            if comp_cid.startswith(f"card_{self.cid}") or len(card_components) > 0:
                builder = store['builders'].get(comp_cid) or self.app.static_builders.get(comp_cid)
                if builder:
                    card_components.append(builder().render())
        
        # Build final card HTML
        def builder():
            token = rendering_ctx.set(self.cid)
            
            try:
                # Handle callable header and footer (Lambda support)
                current_header = self.header
                if callable(self.header):
                    current_header = self.header()
                
                current_footer = self.footer
                if callable(self.footer):
                    current_footer = self.footer()
                
                # Add width: 100% to sl-card (consistency with broadcast)
                card_style = 'style="width: 100%;"'
                html_parts = [f'<sl-card{self.attrs_str} {card_style}>']
                
                if current_header:
                    html_parts.append(f'<div slot="header">{current_header}</div>')
                
                # Add collected components as content (no wrapper div)
                if card_components:
                    html_parts.extend(card_components)
                
                if current_footer:
                    html_parts.append(f'<div slot="footer">{current_footer}</div>')
                
                html_parts.append('</sl-card>')
                
                # Apply width: 100% to wrapper div (consistency with list_container)
                return Component("div", id=self.cid, content=''.join(html_parts), style="width: 100%;")
            finally:
                rendering_ctx.reset(token)
        
        self.app._register_component(self.cid, builder)
        layout_ctx.reset(self.token)

