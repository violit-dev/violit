"""
Style Utilities for Violit
Provides merge helpers for cls (class) and style (inline CSS) parameters.
"""


def merge_cls(*class_strings: str) -> str:
    """Merge multiple class strings into one, removing empty/None values.
    
    Args:
        *class_strings: Variable number of class strings to merge.
        
    Returns:
        Combined class string with duplicates preserved (CSS specificity matters).
        
    Example:
        merge_cls("r:full shadow:md", "", "mt:2rem") → "r:full shadow:md mt:2rem"
    """
    parts = []
    for s in class_strings:
        if s:
            stripped = s.strip()
            if stripped:
                parts.append(stripped)
    return " ".join(parts)


def merge_style(*style_strings: str) -> str:
    """Merge multiple inline style strings into one, removing empty/None values.
    
    Args:
        *style_strings: Variable number of CSS inline style strings to merge.
        
    Returns:
        Combined style string. Later values override earlier ones for same property.
        
    Example:
        merge_style("margin-top: 2rem;", "", "--sl-color-primary-600: cyan;")
        → "margin-top: 2rem; --sl-color-primary-600: cyan;"
    """
    parts = []
    for s in style_strings:
        if s:
            stripped = s.strip()
            if stripped:
                # Ensure trailing semicolon for proper concatenation
                if not stripped.endswith(";"):
                    stripped += ";"
                parts.append(stripped)
    result = " ".join(parts)
    return result.strip()


def wrap_html(html: str, cls: str = "", style: str = "") -> str:
    """Wrap HTML content with a div if cls or style are provided.
    
    Used for Component(None, ...) widgets where we can't pass class/style
    directly to the Component constructor.
    
    Args:
        html: Raw HTML content
        cls: CSS classes to apply
        style: Inline CSS styles to apply
        
    Returns:
        Original HTML if no cls/style, wrapped HTML otherwise.
    """
    if not cls and not style:
        return html
    attrs = []
    if cls:
        attrs.append(f'class="{cls}"')
    if style:
        attrs.append(f'style="{style}"')
    return f'<div {" ".join(attrs)}>{html}</div>'
