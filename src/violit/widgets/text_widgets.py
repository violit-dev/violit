"""Text widgets"""

import base64
import html as html_lib
import os
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Union, Callable, Optional, Any
from urllib.parse import urlparse

try:
    import markdown as markdown_lib
except ImportError:  # pragma: no cover - dependency should be installed with violit
    markdown_lib = None

from ..component import Component
from ..context import rendering_ctx
from ..style_utils import merge_cls, merge_style


_HTML_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

_HTML_BLOCKED_TAGS = {
    "base",
    "embed",
    "iframe",
    "link",
    "meta",
    "object",
}

_HTML_URL_ATTRS = {"href", "src", "poster", "action", "formaction", "xlink:href"}

_SAFE_HTML_DATA_MIME_PREFIXES = (
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


def _sanitize_text_key(value: Any) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value)).strip("_") or "text"


def _sanitize_markdown_url(raw_url: str, *, allowed_schemes: set[str], allow_relative: bool = False) -> str | None:
    url = html_lib.unescape(raw_url).strip()
    if not url or url.startswith("//"):
        return None

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    if scheme:
        if scheme not in allowed_schemes:
            return None
    elif not allow_relative:
        return None

    return html_lib.escape(url, quote=True)


def _sanitize_markdown_href(raw_href: str) -> str | None:
    return _sanitize_markdown_url(
        raw_href,
        allowed_schemes={"http", "https", "mailto", "tel"},
        allow_relative=True,
    )


def _sanitize_markdown_src(raw_src: str) -> str | None:
    return _sanitize_markdown_url(
        raw_src,
        allowed_schemes={"http", "https"},
        allow_relative=False,
    )


def _is_safe_html_data_url(url: str) -> bool:
    lowered = url.lower()
    if not lowered.startswith("data:"):
        return False
    header = lowered[5:].split(",", 1)[0].strip()
    mime = header.split(";", 1)[0].strip()
    return any(mime.startswith(prefix) for prefix in _SAFE_HTML_DATA_MIME_PREFIXES)


def _sanitize_html_url(raw_url: str, *, attr_name: str) -> str | None:
    url = html_lib.unescape(raw_url).strip()
    if not url or url.startswith("//"):
        return None

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    if scheme:
        if scheme == "data" and attr_name in {"src", "poster"} and _is_safe_html_data_url(url):
            return html_lib.escape(url, quote=True)
        if scheme not in {"http", "https", "mailto", "tel", "blob"}:
            return None

    return html_lib.escape(url, quote=True)


def _sanitize_css_text(css_text: str) -> str:
    sanitized = css_text
    sanitized = re.sub(r"(?is)expression\s*\([^)]*\)", "", sanitized)
    sanitized = re.sub(r"(?is)-moz-binding\s*:[^;{}]+;?", "", sanitized)
    sanitized = re.sub(r"(?is)behavior\s*:[^;{}]+;?", "", sanitized)
    sanitized = re.sub(r"(?is)url\s*\(\s*(['\"]?)\s*javascript:[^)]*\)", "", sanitized)
    return sanitized.strip()


def _sanitize_html_style(raw_style: str) -> str:
    return _sanitize_css_text(html_lib.unescape(raw_style))


def _merge_anchor_rel(attrs: list[tuple[str, Optional[str]]]) -> list[tuple[str, Optional[str]]]:
    rel_index = next((index for index, (name, _) in enumerate(attrs) if name.lower() == "rel"), None)
    existing_tokens: list[str] = []
    if rel_index is not None and attrs[rel_index][1]:
        existing_tokens = str(attrs[rel_index][1]).split()
    merged_tokens = []
    for token in [*existing_tokens, "noopener", "noreferrer"]:
        if token and token not in merged_tokens:
            merged_tokens.append(token)
    if rel_index is None:
        attrs.append(("rel", " ".join(merged_tokens)))
    else:
        attrs[rel_index] = ("rel", " ".join(merged_tokens))
    return attrs


def _sanitize_html_attrs(tag: str, attrs: list[tuple[str, Optional[str]]]) -> list[tuple[str, Optional[str]]]:
    cleaned: list[tuple[str, Optional[str]]] = []
    target_blank = False

    for raw_name, raw_value in attrs:
        if not raw_name:
            continue
        name = raw_name.strip()
        if not re.fullmatch(r"[A-Za-z_:][-A-Za-z0-9_:.]*", name):
            continue

        lower_name = name.lower()
        if lower_name.startswith("on") or lower_name == "srcdoc":
            continue

        if lower_name == "style":
            if raw_value is None:
                continue
            safe_style = _sanitize_html_style(str(raw_value))
            if safe_style:
                cleaned.append((name, safe_style))
            continue

        if lower_name in _HTML_URL_ATTRS:
            if raw_value is None:
                continue
            safe_url = _sanitize_html_url(str(raw_value), attr_name=lower_name)
            if safe_url is not None:
                cleaned.append((name, html_lib.unescape(safe_url)))
            continue

        if lower_name == "target" and raw_value is not None:
            target_value = str(raw_value).strip()
            if target_value:
                cleaned.append((name, target_value))
                if target_value.lower() == "_blank":
                    target_blank = True
            continue

        if raw_value is None:
            cleaned.append((name, None))
        else:
            cleaned.append((name, html_lib.unescape(str(raw_value))))

    if tag == "a" and target_blank:
        cleaned = _merge_anchor_rel(cleaned)

    return cleaned


def _serialize_html_attrs(attrs: list[tuple[str, Optional[str]]]) -> str:
    parts = []
    for name, value in attrs:
        lower_name = name.lower()
        if value is None:
            parts.append(lower_name)
        else:
            parts.append(f'{lower_name}="{html_lib.escape(str(value), quote=True)}"')
    return " ".join(parts)


class _SafeHtmlParser(HTMLParser):
    def __init__(self, *, allow_javascript: bool):
        super().__init__(convert_charrefs=False)
        self.allow_javascript = allow_javascript
        self.parts: list[str] = []
        self._blocked_stack: list[str] = []
        self._open_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]):
        lower_tag = tag.lower()
        if lower_tag in _HTML_BLOCKED_TAGS or (lower_tag == "script" and not self.allow_javascript):
            self._blocked_stack.append(lower_tag)
            return
        if self._blocked_stack:
            return

        serialized_attrs = _serialize_html_attrs(_sanitize_html_attrs(lower_tag, attrs))
        attr_suffix = f" {serialized_attrs}" if serialized_attrs else ""
        self.parts.append(f"<{lower_tag}{attr_suffix}>")
        if lower_tag not in _HTML_VOID_TAGS:
            self._open_tags.append(lower_tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, Optional[str]]]):
        lower_tag = tag.lower()
        if lower_tag in _HTML_BLOCKED_TAGS or (lower_tag == "script" and not self.allow_javascript):
            return
        if self._blocked_stack:
            return

        serialized_attrs = _serialize_html_attrs(_sanitize_html_attrs(lower_tag, attrs))
        attr_suffix = f" {serialized_attrs}" if serialized_attrs else ""
        self.parts.append(f"<{lower_tag}{attr_suffix} />")

    def handle_endtag(self, tag: str):
        lower_tag = tag.lower()
        if self._blocked_stack:
            if lower_tag == self._blocked_stack[-1]:
                self._blocked_stack.pop()
            return
        if lower_tag in _HTML_VOID_TAGS:
            return
        self.parts.append(f"</{lower_tag}>")
        if self._open_tags:
            for index in range(len(self._open_tags) - 1, -1, -1):
                if self._open_tags[index] == lower_tag:
                    del self._open_tags[index]
                    break

    def handle_data(self, data: str):
        if self._blocked_stack:
            return
        if self._open_tags and self._open_tags[-1] == "style":
            self.parts.append(_sanitize_css_text(data))
            return
        self.parts.append(data)

    def handle_entityref(self, name: str):
        if not self._blocked_stack:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str):
        if not self._blocked_stack:
            self.parts.append(f"&#{name};")

    def handle_comment(self, data: str):
        if not self._blocked_stack:
            self.parts.append(f"<!--{data}-->")

    def get_html(self) -> str:
        return "".join(self.parts)


def _sanitize_html_fragment(html_text: str, *, allow_javascript: bool) -> str:
    parser = _SafeHtmlParser(allow_javascript=allow_javascript)
    parser.feed(html_text)
    parser.close()
    return parser.get_html()


def _read_html_body_file(path: Path) -> Optional[str]:
    try:
        if not path.is_file():
            return None
        file_text = path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    if path.suffix.lower() == ".css":
        return f"<style>\n{file_text}\n</style>"
    return file_text


def _resolve_html_body_part(value: Any) -> str:
    if isinstance(value, os.PathLike):
        path = Path(value)
        resolved_file_text = _read_html_body_file(path)
        if resolved_file_text is not None:
            return resolved_file_text
        return str(path)

    if isinstance(value, str):
        if "\n" in value or "\r" in value:
            return value
        possible_path = Path(value)
        resolved_file_text = _read_html_body_file(possible_path)
        if resolved_file_text is not None:
            return resolved_file_text
        return value

    repr_html = getattr(value, "_repr_html_", None)
    if callable(repr_html):
        rendered = repr_html()
        if rendered is not None:
            return str(rendered)

    return str(value)


def _resolve_html_body(*parts: Any) -> str:
    if not parts:
        return ""
    if len(parts) == 1:
        return _resolve_html_body_part(parts[0])
    return " ".join(_resolve_html_body_part(part) for part in parts)


def _resolve_html_width_style(width: Union[str, int]) -> str:
    if width == "stretch":
        return "display:block; width:100%;"
    if width == "content":
        return "display:inline-block; width:max-content; max-width:100%;"
    if isinstance(width, int) and not isinstance(width, bool):
        if width <= 0:
            raise ValueError("html() width must be a positive integer.")
        return f"display:block; width:min({width}px, 100%); max-width:100%;"
    raise ValueError("html() width must be 'stretch', 'content', or a positive integer.")


def _inject_style_attr(opening_tag: str, style: str, *, extra_attrs: list[str] | None = None) -> str:
    updated_tag = opening_tag

    style_match = re.search(r'style=("|\')(.*?)(\1)', updated_tag, flags=re.IGNORECASE | re.DOTALL)
    if style_match:
        existing_style = style_match.group(2).strip()
        merged_style = f"{existing_style.rstrip(';')} ; {style}" if existing_style else style
        updated_tag = (
            updated_tag[:style_match.start()]
            + f'style={style_match.group(1)}{merged_style}{style_match.group(1)}'
            + updated_tag[style_match.end():]
        )
    else:
        updated_tag = updated_tag[:-1] + f' style="{style}">'

    if extra_attrs:
        for attr in extra_attrs:
            attr_name = attr.split("=", 1)[0].strip().lower()
            if re.search(rf'\b{re.escape(attr_name)}\b', updated_tag, flags=re.IGNORECASE):
                continue
            updated_tag = updated_tag[:-1] + f' {attr}>'

    return updated_tag


def _style_rendered_markdown_html(rendered_html: str) -> str:
    styles = {
        "p": "margin:0 0 0.85rem 0; line-height:1.7;",
        "ul": "margin:0.75rem 0; padding-left:1.5rem; list-style:disc; list-style-position:outside;",
        "ol": "margin:0.75rem 0; padding-left:1.5rem; list-style:decimal; list-style-position:outside;",
        "li": "margin:0.2rem 0; display:list-item;",
        "blockquote": "margin:1rem 0; padding:0.15rem 0 0.15rem 1rem; border-left:4px solid var(--vl-primary); color:var(--vl-text-muted);",
        "pre": "margin:1rem 0; padding:0.9rem 1rem; overflow-x:auto; border-radius:0.75rem; background:var(--vl-bg-card); border:1px solid var(--vl-border);",
        "table": "width:100%; margin:1rem 0; border-collapse:collapse; display:table;",
        "thead": "background:var(--vl-bg-card);",
        "th": "padding:0.65rem 0.75rem; border:1px solid var(--vl-border); text-align:left; font-weight:600;",
        "td": "padding:0.65rem 0.75rem; border:1px solid var(--vl-border); vertical-align:top;",
        "hr": "border:none; border-top:1px solid var(--vl-border); margin:1.25rem 0;",
        "img": "max-width:100%; height:auto; margin:0.9rem 0; border-radius:0.5rem;",
    }

    rendered_html = re.sub(
        r'<div\b([^>]*?)class=("|\")(.*?\bcodehilite\b.*?)(\2)([^>]*)>',
        lambda match: _inject_style_attr(
            match.group(0),
            "margin:1rem 0; border-radius:0.75rem; overflow:hidden; border:1px solid var(--vl-border); background:var(--vl-bg-card);",
        ),
        rendered_html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    for tag_name, style in styles.items():
        rendered_html = re.sub(
            rf'<{tag_name}\b[^>]*>',
            lambda match, style=style: _inject_style_attr(match.group(0), style),
            rendered_html,
            flags=re.IGNORECASE,
        )

    rendered_html = re.sub(
        r'<code\b(?![^>]*(data-vl-code-block|class=|style=))[^>]*>',
        lambda match: _inject_style_attr(
            match.group(0),
            "background:var(--vl-bg-card); padding:0.2em 0.4em; border-radius:0.35rem; font-family:'SF Mono','Fira Code','Consolas',monospace; font-size:0.92em;",
        ),
        rendered_html,
        flags=re.IGNORECASE,
    )

    rendered_html = re.sub(
        r'<pre\b[^>]*>\s*<code\b([^>]*)>',
        lambda match: (
            match.group(0).replace(
                "<code",
                '<code data-vl-code-block="true" style="background:transparent; padding:0; border-radius:0; font-family:\'SF Mono\',\'Fira Code\',\'Consolas\',monospace; font-size:0.92rem;"',
                1,
            )
        ),
        rendered_html,
        flags=re.IGNORECASE,
    )

    return rendered_html


def _sanitize_rendered_markdown_html(rendered_html: str) -> str:
    def replace_anchor(match: re.Match[str]) -> str:
        attrs_before = match.group(1) or ""
        raw_href = match.group(3)
        attrs_after = match.group(5) or ""
        label = match.group(6)
        safe_href = _sanitize_markdown_href(raw_href)
        if safe_href is None:
            return f'{label} ({html_lib.escape(html_lib.unescape(raw_href))})'
        anchor_tag = f'<a{attrs_before} href="{safe_href}"{attrs_after}>'
        return _inject_style_attr(
            anchor_tag,
            "color:var(--vl-primary); text-decoration:underline;",
            extra_attrs=['rel="noopener noreferrer"'],
        ) + label + '</a>'

    rendered_html = re.sub(
        r'<a\b([^>]*?)href=("|\')(.*?)(\2)([^>]*)>(.*?)</a>',
        replace_anchor,
        rendered_html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    def replace_image(match: re.Match[str]) -> str:
        opening_tag = match.group(0)
        src_match = re.search(r'src=("|\')(.*?)(\1)', opening_tag, flags=re.IGNORECASE | re.DOTALL)
        if src_match is None:
            return opening_tag
        safe_src = _sanitize_markdown_src(src_match.group(2))
        alt_match = re.search(r'alt=("|\')(.*?)(\1)', opening_tag, flags=re.IGNORECASE | re.DOTALL)
        alt_text = html_lib.escape(html_lib.unescape(alt_match.group(2))) if alt_match else "image"
        if safe_src is None:
            return f'<span style="color:var(--vl-text-muted);">[image: {alt_text}]</span>'
        sanitized_tag = (
            opening_tag[:src_match.start()]
            + f'src="{safe_src}"'
            + opening_tag[src_match.end():]
        )
        return _inject_style_attr(sanitized_tag, "max-width:100%; height:auto; margin:0.9rem 0; border-radius:0.5rem;", extra_attrs=['loading="lazy"'])

    rendered_html = re.sub(r'<img\b[^>]*?>', replace_image, rendered_html, flags=re.IGNORECASE | re.DOTALL)

    def replace_task_list(match: re.Match[str]) -> str:
        checked = match.group(1).lower() == "x"
        label = match.group(2)
        checkbox_style = (
            "display:inline-flex; align-items:center; justify-content:center; "
            "width:1rem; height:1rem; margin-right:0.55rem; border-radius:0.25rem; "
            f"border:1.5px solid {'var(--vl-primary)' if checked else 'var(--vl-border)'}; "
            f"background:{'var(--vl-primary)' if checked else 'transparent'}; "
            f"color:{'white' if checked else 'transparent'}; font-size:0.75rem; font-weight:700; flex:0 0 auto;"
        )
        checkbox = f'<span aria-hidden="true" style="{checkbox_style}">{"✓" if checked else ""}</span>'
        return (
            '<li style="margin:0.2rem 0; display:flex; align-items:flex-start; list-style:none;">'
            f'{checkbox}<span style="display:inline-block; line-height:1.6;">{label}</span>'
            '</li>'
        )

    rendered_html = re.sub(
        r'<li\b[^>]*>\s*\[([ xX])\]\s*(.*?)</li>',
        replace_task_list,
        rendered_html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return _style_rendered_markdown_html(rendered_html)


def _escape_raw_html_fragments(text: str) -> str:
    return re.sub(r'<[^>\n]+>', lambda match: html_lib.escape(match.group(0)), text)


def _normalize_markdown_indentation(text: str) -> str:
    normalized_lines = []
    in_fence = False

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            normalized_lines.append(line)
            continue

        if in_fence:
            normalized_lines.append(line)
            continue

        match = re.match(r'^( +)([-*+]\s+|\d+\.\s+)(.*)$', line)
        if match is None:
            normalized_lines.append(line)
            continue

        indent_len = len(match.group(1))
        if indent_len == 0:
            normalized_lines.append(line)
            continue

        normalized_indent_len = max(4, ((indent_len + 3) // 4) * 4)
        normalized_lines.append(
            f'{" " * normalized_indent_len}{match.group(2)}{match.group(3)}'
        )

    return "\n".join(normalized_lines)


def _markdown_extensions() -> list[str]:
    return ["fenced_code", "tables", "sane_lists", "nl2br", "codehilite"]


def _markdown_extension_configs() -> dict[str, dict[str, object]]:
    return {
        "codehilite": {
            "guess_lang": False,
            "noclasses": True,
            "css_class": "codehilite",
        }
    }


def _render_safe_markdown_html(text: str) -> str:
    if markdown_lib is None:
        safe_text = html_lib.escape(text).replace('\n', '<br>')
        return safe_text

    rendered_html = markdown_lib.markdown(
        _escape_raw_html_fragments(_normalize_markdown_indentation(text)),
        extensions=_markdown_extensions(),
        extension_configs=_markdown_extension_configs(),
        output_format="html",
    )
    return _sanitize_rendered_markdown_html(rendered_html)


def _render_markdown_html(text: str, *, allow_html: bool) -> str:
    if markdown_lib is None:
        if allow_html:
            return text
        return _render_safe_markdown_html(text)

    source_text = _normalize_markdown_indentation(text)
    if not allow_html:
        source_text = _escape_raw_html_fragments(source_text)

    rendered_html = markdown_lib.markdown(
        source_text,
        extensions=_markdown_extensions(),
        extension_configs=_markdown_extension_configs(),
        output_format="html",
    )
    return _sanitize_rendered_markdown_html(rendered_html)


def _build_visual_stream_html(
    text: str,
    *,
    stream_key: str,
    cursor: Optional[str] = None,
    live_html: Optional[str] = None,
    final_html: Optional[str] = None,
    display_speed: Optional[int] = None,
) -> str:
    encoded_target = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe_key = html_lib.escape(str(stream_key), quote=True)
    safe_cursor = html_lib.escape(str(cursor or ""), quote=True)
    safe_display_speed = html_lib.escape(str(display_speed), quote=True) if display_speed is not None else ""
    encoded_live_html = ""
    if live_html:
        encoded_live_html = base64.b64encode(live_html.encode("utf-8")).decode("ascii")
    encoded_final_html = ""
    if final_html:
        encoded_final_html = base64.b64encode(final_html.encode("utf-8")).decode("ascii")
    live_html_attr = f' data-vl-stream-live-html="{encoded_live_html}"' if encoded_live_html else ""
    final_html_attr = f' data-vl-stream-final-html="{encoded_final_html}"' if encoded_final_html else ""
    display_speed_attr = f' data-vl-stream-speed="{safe_display_speed}"' if safe_display_speed else ""
    return (
        f'<div data-vl-stream-smooth="true" data-vl-stream-key="{safe_key}" '
        f'data-vl-stream-target="{encoded_target}" data-vl-stream-cursor="{safe_cursor}" '
        f'{live_html_attr}'
        f'{final_html_attr}'
        f'{display_speed_attr}'
        'style="display:block;min-width:0;">'
        '<div data-vl-stream-live="true" '
        'style="white-space:pre-wrap;word-break:break-word;line-height:1.7;"></div>'
        '</div>'
    )


class TextWidgetsMixin:
    def write(self, *args, **kwargs):
        """Magic write: displays arguments based on their type
        
        Supported types:
        - Strings, Numbers, State: Rendered as Markdown text
        - Pandas DataFrame/Series: Rendered as interactive table
        - Dict/List: Rendered as JSON tree
        - Matplotlib/Plotly Figures: Rendered as charts
        - Exceptions: Rendered as error trace
        """
        from ..state import State, ComputedState
        
        # Buffer for text-like arguments
        text_buffer = []
        
        def flush_buffer():
            if text_buffer:
                self.markdown(*text_buffer)
                text_buffer.clear()
        
        for arg in args:
            # Unwrap state for type checking ONLY
            check_val = arg.value if isinstance(arg, (State, ComputedState)) else arg
            
            # 1. Pandas DataFrame / Series
            is_df = False
            try:
                import pandas as pd
                if isinstance(check_val, (pd.DataFrame, pd.Series, pd.Index)):
                    is_df = True
            except ImportError: pass
            
            if is_df:
                flush_buffer()
                if hasattr(self, 'dataframe'):
                    self.dataframe(arg)
                else:
                    self.markdown(str(arg))
                continue
                
            # 2. Matplotlib Figure
            is_pyplot = False
            try:
                import matplotlib.figure
                if isinstance(check_val, matplotlib.figure.Figure):
                    is_pyplot = True
            except ImportError: pass
            
            if is_pyplot:
                flush_buffer()
                if hasattr(self, 'pyplot'):
                    self.pyplot(arg)
                continue
                
            # 3. Plotly Figure
            is_plotly = False
            try:
                if hasattr(check_val, 'to_plotly_json'):
                    is_plotly = True
            except ImportError: pass
            
            if is_plotly:
                flush_buffer()
                if hasattr(self, 'plotly_chart'):
                    self.plotly_chart(arg)
                continue
                
            # 4. Dict / List (JSON)
            if isinstance(check_val, (dict, list)):
                flush_buffer()
                if hasattr(self, 'json'):
                    self.json(arg)
                else:
                    # Fallback if json widget logic is missing for State
                    # But wait, we need to fix json widget too.
                    self.json(arg)
                continue
                
            # 5. Exception
            if isinstance(check_val, Exception):
                flush_buffer()
                if hasattr(self, 'exception'):
                    self.exception(arg)
                else:
                    self.error(str(arg))
                continue
            
            # Default: Text-like (str, int, float, State, ComputedState)
            text_buffer.append(arg)
            
        # Flush remaining text
        flush_buffer()

    def _write_stream_to_placeholder(self, placeholder, items, cursor=None, visual_stream_smoothing: bool = True):
        with placeholder.container():
            for index, item in enumerate(items):
                if isinstance(item, str):
                    text = item
                    is_streaming_tail = visual_stream_smoothing and bool(cursor) and index == len(items) - 1
                    if is_streaming_tail:
                        stream_key = f"{getattr(placeholder, 'container_id', 'stream')}:{index}"
                        self.html(
                            _build_visual_stream_html(
                                text,
                                stream_key=stream_key,
                                cursor=cursor,
                                live_html=_render_markdown_html(text, allow_html=False),
                            ),
                            cls="markdown",
                        )
                    else:
                        if cursor and index == len(items) - 1:
                            text += str(cursor)
                        self.markdown(text)
                else:
                    self.write(item)

    def _normalize_stream_iterator(self, stream):
        candidate = stream() if callable(stream) and not hasattr(stream, "__iter__") else stream
        if hasattr(candidate, "__iter__"):
            return iter(candidate)
        raise TypeError("write_stream expects an iterable, generator, or callable returning an iterable.")

    def _extract_stream_chunk(self, chunk: Any):
        if isinstance(chunk, str):
            return chunk

        if isinstance(chunk, dict):
            if isinstance(chunk.get("text"), str):
                return chunk["text"]
            if isinstance(chunk.get("content"), str):
                return chunk["content"]
            delta = chunk.get("delta") or {}
            if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                return delta["content"]

        choices = getattr(chunk, "choices", None)
        if choices:
            first = choices[0]
            delta = getattr(first, "delta", None)
            if delta is not None:
                content = getattr(delta, "content", None)
                if isinstance(content, str):
                    return content
            message = getattr(first, "message", None)
            if message is not None:
                content = getattr(message, "content", None)
                if isinstance(content, str):
                    return content

        text = getattr(chunk, "text", None)
        if isinstance(text, str):
            return text

        return chunk

    def write_stream(self, stream, *, cursor=None, visual_stream_smoothing: bool = True):
        """Stream content into the app, compatible with Streamlit's st.write_stream."""
        placeholder = self.empty()
        iterator = self._normalize_stream_iterator(stream)

        rendered_items = []
        all_text = True

        for raw_chunk in iterator:
            chunk = self._extract_stream_chunk(raw_chunk)
            if isinstance(chunk, str):
                if rendered_items and isinstance(rendered_items[-1], str):
                    rendered_items[-1] += chunk
                else:
                    rendered_items.append(chunk)
            else:
                all_text = False
                rendered_items.append(chunk)

            self._write_stream_to_placeholder(
                placeholder,
                rendered_items,
                cursor=cursor,
                visual_stream_smoothing=visual_stream_smoothing,
            )

        self._write_stream_to_placeholder(
            placeholder,
            rendered_items,
            cursor=None,
            visual_stream_smoothing=visual_stream_smoothing,
        )

        if all_text:
            return "".join(item for item in rendered_items if isinstance(item, str))
        return rendered_items
    
    def _render_markdown(self, text: str) -> str:
        """Render markdown to HTML (internal helper)"""
        return _render_markdown_html(text, allow_html=False)
    
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
                    background: var(--vl-primary);
                    color: white;
                    padding: 0.75rem;
                    text-align: left;
                    font-weight: 600;
                }}
                .dataframe td {{
                    padding: 0.5rem 0.75rem;
                    border-bottom: 1px solid var(--vl-border);
                }}
                .dataframe tr:hover {{
                    background: var(--vl-bg-card);
                }}
            </style>
            {html}
        </div>
        '''
        return styled_html

    def heading(self, *args, level: int = 1, divider: bool = False, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display heading (h1-h6)

        Args:
            anchor: Optional anchor ID for deep-linking (e.g. '#my-section')
            help: Tooltip text shown next to the heading
        """
        from ..state import State, ComputedState
        import html as html_lib
        
        cid = self._get_next_cid("heading")
        def builder():
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            content = " ".join(parts)
            rendering_ctx.reset(token)
            
            # XSS protection: escape content
            escaped_content = html_lib.escape(str(content))
            
            grad = "gradient-text" if level == 1 else ""
            anchor_attr = f' id="{html_lib.escape(anchor, quote=True)}"' if anchor else ''
            help_html = f' <wa-tooltip for="{cid}_help" content="{html_lib.escape(str(help), quote=True)}"></wa-tooltip><wa-icon id="{cid}_help" name="circle-question" style="font-size:0.7em;color:var(--vl-text-muted);vertical-align:middle;cursor:help;"></wa-icon>' if help else ''
            html_output = f'<h{level}{anchor_attr} class="{grad}">{escaped_content}{help_html}</h{level}>'
            if divider: html_output += '<wa-divider class="divider"></wa-divider>'
            _wd = self._get_widget_defaults("heading")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def title(self, *args, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display title (h1 with gradient)"""
        self.heading(*args, level=1, divider=False, anchor=anchor, help=help, cls=cls, style=style)

    def header(self, *args, divider: bool = True, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display header (h2)"""
        self.heading(*args, level=2, divider=divider, anchor=anchor, help=help, cls=cls, style=style)

    def subheader(self, *args, divider: bool = False, anchor: str = None, help: str = None, cls: str = "", style: str = ""):
        """Display subheader (h3)"""
        self.heading(*args, level=3, divider=divider, anchor=anchor, help=help, cls=cls, style=style)

    def text(self, *args, size: str = "medium", muted: bool = False, key: Optional[Union[str, int]] = None, cls: str = "", style: str = ""):
        """Display text paragraph
        
        Supports multiple arguments which will be joined by spaces.
        """
        from ..state import State, ComputedState
        
        cid = f"text_{_sanitize_text_key(key)}" if key is not None else self._get_next_cid("text")
        def builder():
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            val = " ".join(parts)
            rendering_ctx.reset(token)
            
            import html as html_lib
            text_cls = f"text-{size} {'text-muted' if muted else ''}"
            _wd = self._get_widget_defaults("text")
            _fc = merge_cls(_wd.get("cls", ""), text_cls, cls)
            _fs = merge_style(_wd.get("style", ""), style)
            # XSS protection: escape manually, then convert newlines to <br>
            safe_val = html_lib.escape(val).replace('\n', '<br>')
            return Component("p", id=cid, content=safe_val, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)
    
    def caption(self, *args, unsafe_allow_html=False, help: str = None, key: Optional[Union[str, int]] = None, cls: str = "", style: str = ""):
        """Display caption text (small, muted)

        Args:
            unsafe_allow_html: If True, allow raw HTML in content
            help: Tooltip text
        """
        if unsafe_allow_html:
            self.unsafe_html(*args, key=key, cls=f"text-small text-muted {cls}", style=style)
        else:
            self.text(*args, size="small", muted=True, key=key, cls=cls, style=style)

    def markdown(self, *args, unsafe_allow_html=False, help: str = None, key: Optional[Union[str, int]] = None, cls: str = "", style: str = "", **props):
        """Display markdown-formatted text

        Args:
            unsafe_allow_html: If True, allow raw HTML tags to participate in markdown rendering
            help: Tooltip text
        """
        cid = f"markdown_{_sanitize_text_key(key)}" if key is not None else self._get_next_cid("markdown")
        def builder():
            token = rendering_ctx.set(cid)
            from ..state import State, ComputedState
            
            parts = []
            for arg in args:
                if isinstance(arg, (State, ComputedState)):
                    parts.append(str(arg.value))
                elif callable(arg):
                    parts.append(str(arg()))
                else:
                    parts.append(str(arg))
            
            content = " ".join(parts)

            html = _render_markdown_html(content, allow_html=unsafe_allow_html)
            
            rendering_ctx.reset(token)
            _wd = self._get_widget_defaults("markdown")
            _fc = merge_cls(_wd.get("cls", ""), "markdown", cls)
            _fs = merge_style(_wd.get("style", ""), style)
            if help:
                safe_help = html_lib.escape(str(help), quote=True)
                html += f' <wa-tooltip for="{cid}_help" content="{safe_help}"></wa-tooltip><wa-icon id="{cid}_help" name="circle-question" style="font-size:0.85em;vertical-align:middle;cursor:help;"></wa-icon>'
            return Component("div", id=cid, content=html, class_=_fc, style=_fs or None, **props)
        self._register_component(cid, builder)
    
    def html(
        self,
        body: Any,
        *extra_body: Any,
        width: Union[str, int] = "stretch",
        unsafe_allow_javascript: bool = False,
        key: Optional[Union[str, int]] = None,
        cls: str = "",
        style: str = "",
        **props,
    ):
        """Insert HTML into the app.

        This follows Streamlit's st.html closely: HTML is sanitized by default,
        JavaScript is ignored unless unsafe_allow_javascript=True, and true raw
        passthrough is available separately via unsafe_html().
        """
        if "unsafe_allow_html" in props:
            raise TypeError("html() no longer accepts unsafe_allow_html. Use unsafe_html().")

        cid = f"html_{_sanitize_text_key(key)}" if key is not None else self._get_next_cid("html")
        def builder():
            from ..state import State, ComputedState
            token = rendering_ctx.set(cid)
            
            parts = []
            for arg in (body, *extra_body):
                if isinstance(arg, (State, ComputedState)):
                    parts.append(arg.value)
                elif callable(arg):
                    parts.append(arg())
                else:
                    parts.append(arg)

            content = _resolve_html_body(*parts)
            rendering_ctx.reset(token)
            if not content.strip():
                raise ValueError("html() body cannot be empty.")
            _wd = self._get_widget_defaults("html")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style, _resolve_html_width_style(width))
            safe_content = _sanitize_html_fragment(content, allow_javascript=unsafe_allow_javascript)
            return Component("div", id=cid, content=safe_content, class_=_fc or None, style=_fs or None, **props)
        self._register_component(cid, builder)

    def unsafe_html(
        self,
        body: Any,
        *extra_body: Any,
        width: Union[str, int] = "stretch",
        key: Optional[Union[str, int]] = None,
        cls: str = "",
        style: str = "",
        **props,
    ):
        """Render raw HTML without sanitization.

        This is the truly dangerous HTML API. Never pass untrusted input here.
        """
        cid = f"html_{_sanitize_text_key(key)}" if key is not None else self._get_next_cid("html")
        def builder():
            from ..state import State, ComputedState
            token = rendering_ctx.set(cid)

            parts = []
            for arg in (body, *extra_body):
                if isinstance(arg, (State, ComputedState)):
                    parts.append(arg.value)
                elif callable(arg):
                    parts.append(arg())
                else:
                    parts.append(arg)

            content = _resolve_html_body(*parts)
            rendering_ctx.reset(token)
            if not content.strip():
                raise ValueError("unsafe_html() body cannot be empty.")
            _wd = self._get_widget_defaults("html")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style, _resolve_html_width_style(width))
            return Component("div", id=cid, content=content, class_=_fc or None, style=_fs or None, **props)
        self._register_component(cid, builder)

    def code(self, code: Any, language: Any = None,
             showcase: Any = False, title: Any = None,
             copy_button: Any = True, line_numbers: Any = False,
             wrap_lines: Any = False,
             theme: Any = "auto",
             syntax_highlighting: Any = None,
             cls: str = "", style: str = "", **props):
        """Display code block with syntax highlighting

        Args:
            code: Code string or callable returning code string
            language: Language for syntax highlighting (e.g. "python", "javascript")
            showcase: If True, show macOS-style window chrome (traffic lights + title bar)
            title: Title text for the title bar (shown in showcase mode)
            copy_button: If True, show a copy-to-clipboard button (default: True)
            line_numbers: If True, show line numbers
            wrap_lines: If True, wrap long lines instead of horizontal scrolling
            theme: Code block theme - "auto" (default), "light", or "dark"
            syntax_highlighting: If True, force syntax coloring. If False, render as plain code.
                If None, syntax coloring is enabled only when a language is provided.
            cls: Additional CSS classes
            style: Additional inline CSS
        """
        import html as html_lib
        
        cid = self._get_next_cid("code")
        def builder():
            from ..state import State, ComputedState

            def resolve_dynamic(value):
                if isinstance(value, (State, ComputedState)):
                    return value.value
                if callable(value):
                    return value()
                return value

            token = rendering_ctx.set(cid)
            code_text = resolve_dynamic(code)
            resolved_language = resolve_dynamic(language)
            resolved_showcase = bool(resolve_dynamic(showcase))
            resolved_title = resolve_dynamic(title)
            resolved_copy_button = bool(resolve_dynamic(copy_button))
            resolved_line_numbers = bool(resolve_dynamic(line_numbers))
            resolved_wrap_lines = bool(resolve_dynamic(wrap_lines))
            resolved_theme = resolve_dynamic(theme)
            resolved_syntax_highlighting = resolve_dynamic(syntax_highlighting)
            rendering_ctx.reset(token)
            
            # XSS protection: escape code content
            escaped_code = html_lib.escape(str(code_text))
            
            normalized_theme = str(resolved_theme or "auto").strip().lower()
            if normalized_theme not in {"auto", "light", "dark"}:
                normalized_theme = "auto"

            should_highlight = bool(resolved_language) if resolved_syntax_highlighting is None else bool(resolved_syntax_highlighting)

            language_class = f"language-{resolved_language}" if resolved_language else ""
            no_highlight_class = "" if should_highlight else " nohighlight"
            code_classes = " ".join(
                part for part in ["hljs", language_class, no_highlight_class.strip()] if part
            )
            theme_class = f"violit-code-theme-{normalized_theme}"
            
            # --- Build line numbers ---
            line_num_html = ""
            if resolved_line_numbers:
                lines = code_text.split('\n')
                nums = ''.join(f'<span style="display:block;">{i+1}</span>' for i in range(len(lines)))
                line_num_html = f'''<div class="violit-code-line-numbers">{nums}</div>'''
            
            code_padding_left = "3.5rem" if resolved_line_numbers else "1.25rem"
            
            # --- Copy button ---
            copy_btn_html = ""
            if resolved_copy_button:
                # Unique copy function name to avoid conflicts
                copy_fn = f"violitCopy_{cid}"
                copy_btn_html = f'''
                <button type="button" class="violit-code-copy-button" onclick="{copy_fn}(this)">
                    <wa-icon name="clipboard" style="font-size: 0.85rem;"></wa-icon>
                    <span>Copy</span>
                </button>
                <script>
                async function {copy_fn}(btn) {{
                    const pre = btn.closest('.violit-code-block').querySelector('code');
                    const text = pre ? pre.textContent : '';
                    const icon = btn.querySelector('wa-icon');
                    const span = btn.querySelector('span');

                    function setState(label, iconName) {{
                        if (icon) icon.setAttribute('name', iconName);
                        if (span) span.textContent = label;
                    }}

                    function resetState() {{
                        window.setTimeout(() => setState('Copy', 'clipboard'), 1800);
                    }}

                    function legacyCopy(value) {{
                        const textarea = document.createElement('textarea');
                        textarea.value = value;
                        textarea.setAttribute('readonly', '');
                        textarea.style.position = 'fixed';
                        textarea.style.top = '-9999px';
                        textarea.style.left = '-9999px';
                        document.body.appendChild(textarea);
                        textarea.focus();
                        textarea.select();
                        textarea.setSelectionRange(0, textarea.value.length);
                        let copied = false;
                        try {{
                            copied = document.execCommand('copy');
                        }} catch (error) {{
                            copied = false;
                        }}
                        document.body.removeChild(textarea);
                        return copied;
                    }}

                    let copied = false;
                    try {{
                        if (navigator.clipboard && window.isSecureContext) {{
                            await navigator.clipboard.writeText(text);
                            copied = true;
                        }}
                    }} catch (error) {{
                        copied = false;
                    }}

                    if (!copied) {{
                        copied = legacyCopy(text);
                    }}

                    if (copied) {{
                        setState('Copied!', 'check');
                    }} else {{
                        setState('Copy failed', 'triangle-exclamation');
                    }}
                    resetState();
                }}
                </script>
                '''
            
            # --- Title bar (showcase mode) ---
            title_bar_html = ""
            if resolved_showcase:
                title_text = f'<span class="violit-code-title">{html_lib.escape(str(resolved_title))}</span>' if resolved_title else ''
                title_bar_html = f'''
                <div class="violit-code-titlebar">
                    <div class="violit-code-traffic-dot violit-code-traffic-dot-close"></div>
                    <div class="violit-code-traffic-dot violit-code-traffic-dot-minimize"></div>
                    <div class="violit-code-traffic-dot violit-code-traffic-dot-expand"></div>
                    {title_text}
                </div>
                '''
            
            # --- Assemble ---
            html_output = f'''
                        <div class="violit-code-block {theme_class}{' violit-code-showcase' if resolved_showcase else ''}{' violit-code-with-lines' if resolved_line_numbers else ''}{' violit-code-wrap' if resolved_wrap_lines else ''}" style="--vl-code-padding-left: {code_padding_left};">
                {title_bar_html}
                <div class="violit-code-content">
                    {copy_btn_html}
                    {line_num_html}
                    <pre class="violit-code-pre"><code class="{code_classes}" data-vl-syntax-highlighting="{'true' if should_highlight else 'false'}">{escaped_code}</code></pre>
                </div>
            </div>
            '''
            _wd = self._get_widget_defaults("code")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None, data_vl_init="code-highlight", **props)
        self._register_component(cid, builder)

    def divider(self, cls: str = "", style: str = ""):
        """Display horizontal divider"""
        cid = self._get_next_cid("divider")
        def builder():
            _wd = self._get_widget_defaults("divider")
            _fc = merge_cls(_wd.get("cls", ""), "divider", cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("wa-divider", id=cid, class_=_fc, style=_fs or None)
        self._register_component(cid, builder)

    def space(self, size="1rem"):
        """Add vertical space between widgets.
        
        Args:
            size: CSS size value (e.g. '0.5rem', '2rem', '20px')
        """
        if isinstance(size, (int, float)):
            size = f'{size}rem'
        cid = self._get_next_cid("space")
        def builder():
            return Component(None, id=cid, content=f'<div style="height:{size}"></div>')
        self._register_component(cid, builder)

    def latex(self, body, cls: str = "", style: str = ""):
        """Display mathematical expression using LaTeX notation (rendered via KaTeX)
        
        Args:
            body: LaTeX formula string (e.g. r'\\frac{a}{b}')
        """
        from ..state import State, ComputedState
        import json as _json

        cid = self._get_next_cid("latex")
        def builder():
            token = rendering_ctx.set(cid)
            if isinstance(body, (State, ComputedState)):
                val = str(body.value)
            elif callable(body):
                val = str(body())
            else:
                val = str(body)
            rendering_ctx.reset(token)

            formula_js = _json.dumps(val)
            katex_config = html_lib.escape(_json.dumps({"formula": val, "displayMode": True}), quote=True)
            _wd = self._get_widget_defaults("latex")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("padding:0.5rem 0; text-align:center; font-size:1.1rem;", _wd.get("style", ""), style)

            html = f'''<div id="{cid}" class="{_fc}" style="{_fs}" data-vl-init="katex-render" data-vl-katex-config="{katex_config}"></div>'''
            return Component(None, id=cid, content=html)
        self._register_component(cid, builder)

