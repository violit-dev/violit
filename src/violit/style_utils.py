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
        merge_cls("r:full shadow:md", "", "mt:2rem") ??"r:full shadow:md mt:2rem"
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
        merge_style("margin-top: 2rem;", "", "--vl-primary: cyan;")
        ??"margin-top: 2rem; --vl-primary: cyan;"
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


def resolve_value(arg):
    """Resolve a reactive argument to its plain value at render time.

    Handles the three reactive forms Violit supports:
    - State / ComputedState   ??.value
    - callable (lambda/func)  ??called with no arguments
    - plain value             ??returned as-is

    Use this inside every builder that accepts content arguments so that
    State, ComputedState, and lambda are all evaluated correctly.

    Example::

        val = str(resolve_value(body))          # single arg
        parts = [str(resolve_value(a)) for a in args]  # *args
    """
    # Import here to avoid circular imports (style_utils is a leaf module)
    from .state import State, ComputedState  # noqa: PLC0415
    if isinstance(arg, (State, ComputedState)):
        return arg.value
    if callable(arg):
        return arg()
    return arg


def wrap_html(html: str, cls: str = "", style: str = "", wrapper_id: str = "") -> str:
    """Wrap HTML content with a div if cls or style are provided (and optionally give it an ID).
    
    If wrapper_id is provided, the wrapper div will always be created.
    
    Args:
        html: Raw HTML content
        cls: CSS classes to apply
        style: Inline CSS styles to apply
        wrapper_id: Optional ID for the wrapping div
        
    Returns:
        Original HTML if no cls/style/id, wrapped HTML otherwise.
    """
    if not cls and not style and not wrapper_id:
        return html
    attrs = []
    if wrapper_id:
        attrs.append(f'id="{wrapper_id}"')
    if cls:
        attrs.append(f'class="{cls}"')
    if style:
        attrs.append(f'style="{style}"')
    return f'<div {" ".join(attrs)}>{html}</div>'
