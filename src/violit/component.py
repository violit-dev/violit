from typing import Any, Mapping, Optional
import html
import re
from urllib.parse import urlparse


_PRIVATE_PROP_KEYS = {
    "__violit_allow_event_attrs__",
}

_SAFE_PUBLIC_ATTRS = {
    "accept",
    "action",
    "alt",
    "appearance",
    "autocomplete",
    "autocapitalize",
    "autocorrect",
    "autofocus",
    "checked",
    "class",
    "cols",
    "disabled",
    "distance",
    "draggable",
    "exportparts",
    "for",
    "formaction",
    "height",
    "hint",
    "href",
    "id",
    "inputmode",
    "label",
    "loading",
    "max",
    "maxlength",
    "max-options-visible",
    "min",
    "minlength",
    "multiple",
    "name",
    "open",
    "part",
    "pattern",
    "placeholder",
    "placement",
    "poster",
    "readonly",
    "rel",
    "required",
    "resize",
    "role",
    "rows",
    "selected",
    "size",
    "skidding",
    "slot",
    "spellcheck",
    "src",
    "step",
    "style",
    "tabindex",
    "target",
    "title",
    "tooltip",
    "type",
    "value",
    "variant",
    "width",
    "with-clear",
}

_SAFE_ATTR_PREFIXES = (
    "aria-",
    "data-",
    "hx-",
)

_SAFE_ATTR_NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.:-]*$")
_SAFE_CUSTOM_ATTR_RE = re.compile(r"^[a-z][a-z0-9_.:-]*-[a-z0-9_.:-]+$")
_EVENT_ATTR_RE = re.compile(r"^on[a-z]", re.IGNORECASE)
_URL_ATTRS = {"action", "formaction", "href", "poster", "src"}
_SAFE_DATA_URL_PREFIXES = (
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/avif",
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/webm",
    "audio/ogg",
    "video/mp4",
    "video/webm",
    "video/ogg",
)

_TAILWIND_WAIT_EXACT_TOKENS = {
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
    "border",
    "rounded",
    "shadow",
    "ring",
    "uppercase",
    "lowercase",
    "capitalize",
    "italic",
}

_TAILWIND_WAIT_EXCLUDED_TOKENS = {
    "text-small",
    "text-medium",
    "text-large",
    "text-muted",
}

_TAILWIND_WAIT_PREFIXES = (
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
    "overflow-",
    "overscroll-",
    "inset-",
    "top-",
    "right-",
    "bottom-",
    "left-",
    "start-",
    "end-",
    "z-",
    "animate-",
    "bg-",
    "text-",
    "font-",
    "tracking-",
    "leading-",
    "decoration-",
    "underline-",
    "color-",
    "border-",
    "rounded-",
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


def normalize_component_attr_name(name: str) -> str:
    raw_name = name[:-1] if name.endswith('_') and not name.endswith('__') else name
    clean_name = raw_name if raw_name.startswith('on') else raw_name.replace('_', '-')
    return clean_name.strip()


def sanitize_inline_style(style: str) -> str:
    sanitized = str(style)
    sanitized = re.sub(r"(?is)expression\s*\([^)]*\)", "", sanitized)
    sanitized = re.sub(r"(?is)-moz-binding\s*:[^;{}]+;?", "", sanitized)
    sanitized = re.sub(r"(?is)behavior\s*:[^;{}]+;?", "", sanitized)
    sanitized = re.sub(r"(?is)url\s*\(\s*(['\"]?)\s*javascript:[^)]*\)", "", sanitized)
    return sanitized.strip()


def _is_safe_data_url(url: str) -> bool:
    lowered = url.lower()
    if not lowered.startswith("data:"):
        return False
    header = lowered[5:].split(",", 1)[0].strip()
    mime = header.split(";", 1)[0].strip()
    return any(mime.startswith(prefix) for prefix in _SAFE_DATA_URL_PREFIXES)


def sanitize_component_url(raw_url: Any, *, attr_name: str) -> str | None:
    url = html.unescape(str(raw_url)).strip()
    if not url or url.startswith("//"):
        return None

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    if scheme:
        if scheme == "data" and attr_name in {"src", "poster"} and _is_safe_data_url(url):
            return url
        if scheme not in {"http", "https", "mailto", "tel", "blob"}:
            return None

    return url


def class_string_needs_tailwind_wait(class_string: Any) -> bool:
    raw_value = str(class_string or "").strip()
    if not raw_value:
        return False

    for token in re.split(r"\s+", raw_value):
        normalized = token.strip()
        if not normalized:
            continue
        core = normalized.split(":")[-1].lstrip("!")
        if not core:
            continue
        if core in _TAILWIND_WAIT_EXCLUDED_TOKENS:
            continue
        if core.startswith("[") or "[" in core:
            return True
        if core in _TAILWIND_WAIT_EXACT_TOKENS:
            return True
        if core.startswith(_TAILWIND_WAIT_PREFIXES):
            return True

    return False


def is_allowed_public_attr(name: str) -> bool:
    lowered = name.lower()
    if lowered in _SAFE_PUBLIC_ATTRS:
        return True
    if lowered.startswith(_SAFE_ATTR_PREFIXES):
        return True
    if _SAFE_CUSTOM_ATTR_RE.fullmatch(lowered):
        return True
    return False


def normalize_public_component_props(
    props: Mapping[str, Any],
    *,
    allow_event_handlers: bool = False,
) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for raw_name, raw_value in props.items():
        if raw_name in _PRIVATE_PROP_KEYS or raw_name == "content":
            continue

        clean_name = normalize_component_attr_name(str(raw_name))
        if not clean_name or not _SAFE_ATTR_NAME_RE.fullmatch(clean_name):
            raise ValueError(f"Unsupported attribute name: {raw_name}")

        lowered = clean_name.lower()
        if _EVENT_ATTR_RE.match(lowered):
            if allow_event_handlers:
                normalized[lowered] = raw_value
                continue
            raise ValueError(
                f"Event handler attribute '{lowered}' is not allowed on public widget props. "
                "Use the widget callback API instead."
            )

        if not is_allowed_public_attr(lowered):
            raise ValueError(f"Unsupported public widget attribute: {lowered}")

        if raw_value is None or raw_value is False:
            continue
        if lowered == "style":
            safe_style = sanitize_inline_style(str(raw_value))
            if safe_style:
                normalized[lowered] = safe_style
            continue
        if lowered in _URL_ATTRS:
            safe_url = sanitize_component_url(raw_value, attr_name=lowered)
            if safe_url is not None:
                normalized[lowered] = safe_url
            continue
        normalized[lowered] = raw_value

    return normalized


def serialize_public_component_attrs(
    props: Mapping[str, Any],
    *,
    allow_event_handlers: bool = False,
) -> str:
    normalized = normalize_public_component_props(props, allow_event_handlers=allow_event_handlers)
    parts: list[str] = []

    for name, value in normalized.items():
        if value is True:
            parts.append(name)
        elif value is False or value is None:
            continue
        else:
            raw_value = str(value)
            if allow_event_handlers and _EVENT_ATTR_RE.match(name):
                escaped_value = raw_value
            else:
                escaped_value = html.escape(raw_value, quote=True)
            parts.append(f'{name}="{escaped_value}"')

    return " ".join(parts)

class Component:
    def __init__(self, tag, id=None, content=None, escape_content=False, **props):
        self.tag = tag
        self.id = id
        self.escape_content = escape_content  # XSS protection
        self.props = props
        if content is not None:
            self.props['content'] = content

    def render(self) -> str:
        if self.tag is None:
            content = str(self.props.get('content', ''))
            # Escape content if enabled
            return html.escape(content) if self.escape_content else content

        props = dict(self.props)
        class_value = props.get('class') or props.get('class_') or ''
        if (
            class_string_needs_tailwind_wait(class_value)
            and 'data_vl_tailwind_wait' not in props
            and 'data-vl-tailwind-wait' not in props
        ):
            props['data_vl_tailwind_wait'] = 'true'

        props_str = serialize_public_component_attrs(props, allow_event_handlers=True)
        content = props.get('content', '')
        
        # Escape content if enabled
        if self.escape_content:
            content = html.escape(str(content))
        
        escaped_id = html.escape(str(self.id), quote=True)
        attr_suffix = f" {props_str}" if props_str else ""
        return f"<{self.tag} id=\"{escaped_id}\"{attr_suffix}>{content}</{self.tag}>"
