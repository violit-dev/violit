"""
Style Utilities for Violit
Provides merge helpers for cls (class) and style (inline CSS) parameters.
"""

import json


AUTO_PART_WIDGETS = {
    "button": "base",
    "input": "input",
    "text_area": "textarea",
    "selectbox": "input",
    "multiselect": "input",
    "number_input": "input",
    "slider": "slider",
    "checkbox": {"surface": "control", "text": "label"},
    "toggle": {"surface": "control", "text": "label"},
    "radio": {"surface": "control", "text": "label"},
}

HOST_EXACT_TOKENS = {
    "block",
    "inline",
    "inline-block",
    "flex",
    "inline-flex",
    "grid",
    "inline-grid",
    "contents",
    "hidden",
    "relative",
    "absolute",
    "fixed",
    "sticky",
    "static",
    "sr-only",
    "not-sr-only",
    "transform",
    "transform-gpu",
    "transform-cpu",
    "transform-none",
    "filter",
    "filter-none",
    "outline",
    "outline-none",
    "isolate",
}

HOST_PREFIXES = (
    "m-",
    "mx-",
    "my-",
    "mt-",
    "mr-",
    "mb-",
    "ml-",
    "ms-",
    "me-",
    "space-",
    "w-",
    "h-",
    "min-w-",
    "min-h-",
    "max-w-",
    "max-h-",
    "size-",
    "flex-",
    "grid-",
    "col-",
    "row-",
    "justify-",
    "items-",
    "content-",
    "self-",
    "place-",
    "order-",
    "basis-",
    "grow-",
    "shrink-",
    "overflow-",
    "overscroll-",
    "pos-",
    "position-",
    "inset-",
    "top-",
    "right-",
    "bottom-",
    "left-",
    "start-",
    "end-",
    "z-",
    "float-",
    "clear-",
    "object-",
    "aspect-",
    "container-",
    "columns-",
    "translate-",
    "rotate-",
    "scale-",
    "skew-",
    "origin-",
    "perspective-",
    "outline-",
    "filter-",
    "cursor-",
    "pointer-events-",
    "resize-",
    "select-",
    "snap-",
    "scroll-",
    "touch-",
    "will-change-",
    "animate-",
)

PART_EXACT_TOKENS = {
    "border",
    "rounded",
    "shadow",
    "ring",
    "uppercase",
    "lowercase",
    "capitalize",
    "italic",
    "not-italic",
    "antialiased",
    "subpixel-antialiased",
    "appearance-none",
}

PART_PREFIXES = (
    "bg-",
    "text-",
    "font-",
    "tracking-",
    "leading-",
    "decoration-",
    "underline-",
    "case-",
    "color-",
    "c-",
    "border-",
    "b-",
    "rounded-",
    "rd-",
    "shadow-",
    "ring-",
    "opacity-",
    "backdrop-",
    "fill-",
    "stroke-",
    "p-",
    "px-",
    "py-",
    "pt-",
    "pr-",
    "pb-",
    "pl-",
    "ps-",
    "pe-",
)

HOST_ARBITRARY_PROPERTIES = {
    "display",
    "margin",
    "margin-top",
    "margin-right",
    "margin-bottom",
    "margin-left",
    "width",
    "height",
    "min-width",
    "min-height",
    "max-width",
    "max-height",
    "position",
    "top",
    "right",
    "bottom",
    "left",
    "transform",
    "filter",
    "outline",
    "outline-offset",
    "justify-content",
    "align-items",
    "gap",
    "flex",
    "flex-basis",
    "order",
    "z-index",
    "overflow",
    "overflow-x",
    "overflow-y",
}

PART_ARBITRARY_PROPERTIES = {
    "background",
    "background-color",
    "background-image",
    "color",
    "border",
    "border-color",
    "border-width",
    "border-style",
    "border-radius",
    "box-shadow",
    "backdrop-filter",
    "font-size",
    "font-weight",
    "font-family",
    "font-style",
    "line-height",
    "letter-spacing",
    "text-transform",
    "text-decoration",
    "text-align",
    "padding",
    "padding-top",
    "padding-right",
    "padding-bottom",
    "padding-left",
    "white-space",
    "appearance",
}

TEXT_PART_EXACT_TOKENS = {
    "uppercase",
    "lowercase",
    "capitalize",
    "italic",
    "not-italic",
    "antialiased",
    "subpixel-antialiased",
}

TEXT_PART_PREFIXES = (
    "text-",
    "font-",
    "tracking-",
    "leading-",
    "decoration-",
    "underline-",
    "case-",
    "color-",
    "c-",
)

SURFACE_PART_EXACT_TOKENS = {
    "border",
    "rounded",
    "shadow",
    "ring",
    "appearance-none",
}

SURFACE_PART_PREFIXES = (
    "bg-",
    "border-",
    "b-",
    "rounded-",
    "rd-",
    "shadow-",
    "ring-",
    "opacity-",
    "backdrop-",
    "fill-",
    "stroke-",
    "p-",
    "px-",
    "py-",
    "pt-",
    "pr-",
    "pb-",
    "pl-",
    "ps-",
    "pe-",
)

TEXT_PART_ARBITRARY_PROPERTIES = {
    "color",
    "font-size",
    "font-weight",
    "font-family",
    "font-style",
    "line-height",
    "letter-spacing",
    "text-transform",
    "text-decoration",
    "text-align",
    "white-space",
}

SURFACE_PART_ARBITRARY_PROPERTIES = {
    "background",
    "background-color",
    "background-image",
    "border",
    "border-color",
    "border-width",
    "border-style",
    "border-radius",
    "box-shadow",
    "backdrop-filter",
    "padding",
    "padding-top",
    "padding-right",
    "padding-bottom",
    "padding-left",
    "appearance",
    "opacity",
    "filter",
    "transform",
}


def merge_cls(*class_strings: str) -> str:
    """Merge multiple class strings into one, removing empty/None values.
    
    Args:
        *class_strings: Variable number of class strings to merge.
        
    Returns:
        Combined class string with duplicates preserved (CSS specificity matters).
        
    Example:
        merge_cls("rounded-full shadow-md", "", "mt-8") ??"rounded-full shadow-md mt-8"
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


def merge_part_cls(*part_maps):
    """Merge multiple shadow-part class maps.

    Later maps extend earlier ones. When the same part key appears multiple
    times, its class strings are concatenated using merge_cls semantics.
    """
    merged = {}
    for part_map in part_maps:
        if not part_map:
            continue
        for part_name, class_string in part_map.items():
            if not class_string:
                continue
            merged[part_name] = merge_cls(merged.get(part_name, ""), class_string)
    return merged


def split_uno_tokens(class_string: str):
    """Split UnoCSS classes while preserving bracketed arbitrary values."""
    if not class_string:
        return []

    tokens = []
    current = []
    bracket_depth = 0
    paren_depth = 0
    quote_char = None
    escape_next = False

    for char in class_string.strip():
        if escape_next:
            current.append(char)
            escape_next = False
            continue

        if char == "\\":
            current.append(char)
            escape_next = True
            continue

        if quote_char:
            current.append(char)
            if char == quote_char:
                quote_char = None
            continue

        if char in {'"', "'"}:
            current.append(char)
            quote_char = char
            continue

        if char == "[":
            bracket_depth += 1
            current.append(char)
            continue

        if char == "]":
            bracket_depth = max(0, bracket_depth - 1)
            current.append(char)
            continue

        if char == "(":
            paren_depth += 1
            current.append(char)
            continue

        if char == ")":
            paren_depth = max(0, paren_depth - 1)
            current.append(char)
            continue

        if char.isspace() and bracket_depth == 0 and paren_depth == 0:
            token = "".join(current).strip()
            if token:
                tokens.append(token)
            current = []
            continue

        current.append(char)

    token = "".join(current).strip()
    if token:
        tokens.append(token)
    return tokens


def _extract_core_utility(token: str) -> str:
    core = (token or "").strip()
    while core.startswith("!"):
        core = core[1:]

    bracket_depth = 0
    paren_depth = 0
    quote_char = None
    escape_next = False
    last_colon = -1

    for index, char in enumerate(core):
        if escape_next:
            escape_next = False
            continue
        if char == "\\":
            escape_next = True
            continue
        if quote_char:
            if char == quote_char:
                quote_char = None
            continue
        if char in {'"', "'"}:
            quote_char = char
            continue
        if char == "[":
            bracket_depth += 1
            continue
        if char == "]":
            bracket_depth = max(0, bracket_depth - 1)
            continue
        if char == "(":
            paren_depth += 1
            continue
        if char == ")":
            paren_depth = max(0, paren_depth - 1)
            continue
        if char == ":" and bracket_depth == 0 and paren_depth == 0:
            last_colon = index

    if last_colon >= 0:
        core = core[last_colon + 1:]
    while core.startswith("!"):
        core = core[1:]
    return core


def _extract_arbitrary_property(core: str):
    if not core.startswith("[") or not core.endswith("]"):
        return None
    inner = core[1:-1].strip()
    if not inner:
        return None

    bracket_depth = 0
    paren_depth = 0
    quote_char = None
    escape_next = False

    for index, char in enumerate(inner):
        if escape_next:
            escape_next = False
            continue
        if char == "\\":
            escape_next = True
            continue
        if quote_char:
            if char == quote_char:
                quote_char = None
            continue
        if char in {'"', "'"}:
            quote_char = char
            continue
        if char == "[":
            bracket_depth += 1
            continue
        if char == "]":
            bracket_depth = max(0, bracket_depth - 1)
            continue
        if char == "(":
            paren_depth += 1
            continue
        if char == ")":
            paren_depth = max(0, paren_depth - 1)
            continue
        if char == ":" and bracket_depth == 0 and paren_depth == 0:
            return inner[:index].strip().lower()
    return None


def _classify_widget_token(token: str) -> str:
    core = _extract_core_utility(token)
    if not core:
        return "host"

    arbitrary_property = _extract_arbitrary_property(core)
    if arbitrary_property:
        if arbitrary_property in HOST_ARBITRARY_PROPERTIES or arbitrary_property.startswith("--"):
            return "host"
        if arbitrary_property in PART_ARBITRARY_PROPERTIES:
            return "part"
        return "host"

    if core in HOST_EXACT_TOKENS or core.startswith(HOST_PREFIXES):
        return "host"
    if core in PART_EXACT_TOKENS or core.startswith(PART_PREFIXES):
        return "part"
    return "host"


def _classify_widget_token_family(token: str) -> str:
    core = _extract_core_utility(token)
    if not core:
        return "host"

    arbitrary_property = _extract_arbitrary_property(core)
    if arbitrary_property:
        if arbitrary_property in HOST_ARBITRARY_PROPERTIES or arbitrary_property.startswith("--"):
            return "host"
        if arbitrary_property in TEXT_PART_ARBITRARY_PROPERTIES:
            return "text"
        if arbitrary_property in SURFACE_PART_ARBITRARY_PROPERTIES:
            return "surface"
        if arbitrary_property in PART_ARBITRARY_PROPERTIES:
            return "surface"
        return "host"

    if core in HOST_EXACT_TOKENS or core.startswith(HOST_PREFIXES):
        return "host"
    if core in TEXT_PART_EXACT_TOKENS or core.startswith(TEXT_PART_PREFIXES):
        return "text"
    if core in SURFACE_PART_EXACT_TOKENS or core.startswith(SURFACE_PART_PREFIXES):
        return "surface"
    if core in PART_EXACT_TOKENS or core.startswith(PART_PREFIXES):
        return "surface"
    return "host"


def auto_split_widget_cls(widget_type: str, class_string: str):
    """Split cls into host classes and auto part classes for supported widgets."""
    part_name = AUTO_PART_WIDGETS.get(widget_type)
    if not part_name or not class_string:
        return merge_cls(class_string), {}

    if isinstance(part_name, str):
        host_tokens = []
        part_tokens = []
        for token in split_uno_tokens(class_string):
            if _classify_widget_token(token) == "part":
                part_tokens.append(token)
            else:
                host_tokens.append(token)

        part_map = {part_name: " ".join(part_tokens)} if part_tokens else {}
        return " ".join(host_tokens), part_map

    host_tokens = []
    part_tokens = {key: [] for key in set(part_name.values())}
    for token in split_uno_tokens(class_string):
        token_family = _classify_widget_token_family(token)
        if token_family == "surface":
            part_tokens.setdefault(part_name.get("surface", "surface"), []).append(token)
        elif token_family == "text":
            part_tokens.setdefault(part_name.get("text", "text"), []).append(token)
        else:
            host_tokens.append(token)

    part_map = {
        resolved_part: " ".join(tokens)
        for resolved_part, tokens in part_tokens.items()
        if tokens
    }
    return " ".join(host_tokens), part_map


def serialize_part_cls(part_map) -> str:
    """Serialize a part->class mapping for safe embedding in a data attribute."""
    if not part_map:
        return ""
    return json.dumps(part_map, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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
