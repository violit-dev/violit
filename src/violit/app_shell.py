from fastapi.responses import HTMLResponse


NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}


def build_user_css(user_css_blocks: list[str]) -> str:
    if not user_css_blocks:
        return ""
    return "<style id=\"violit-user-css\">\n" + "\n".join(user_css_blocks) + "\n</style>"


def build_shell_html(
    template: str,
    *,
    content: str,
    sidebar_content: str,
    sidebar_style: str,
    sidebar_resizer_style: str,
    main_class: str,
    mode: str,
    title: str,
    html_class: str,
    body_class: str,
    css_vars: str,
    splash_html: str,
    container_max_width: str,
    widget_gap: str,
    sidebar_width: str,
    sidebar_min_width: str,
    sidebar_max_width: str,
    sidebar_resizable: bool,
    csrf_script: str,
    debug_script: str,
    vendor_resources: str,
    user_css: str,
    root_style: str,
    disconnect_timeout: int,
    view_id: str,
) -> str:
    return (
        template.replace("%CONTENT%", content)
        .replace("%SIDEBAR_CONTENT%", sidebar_content)
        .replace("%SIDEBAR_STYLE%", sidebar_style)
        .replace("%SIDEBAR_RESIZER_STYLE%", sidebar_resizer_style)
        .replace("%MAIN_CLASS%", main_class)
        .replace("%MODE%", mode)
        .replace("%TITLE%", title)
        .replace("%HTML_CLASS%", html_class)
        .replace("%BODY_CLASS%", body_class)
        .replace("%CSS_VARS%", css_vars)
        .replace("%SPLASH%", splash_html)
        .replace("%CONTAINER_MAX_WIDTH%", container_max_width)
        .replace("%WIDGET_GAP%", widget_gap)
        .replace("%SIDEBAR_WIDTH%", sidebar_width)
        .replace("%SIDEBAR_MIN_WIDTH%", sidebar_min_width)
        .replace("%SIDEBAR_MAX_WIDTH%", sidebar_max_width)
        .replace("%SIDEBAR_RESIZABLE%", "true" if sidebar_resizable else "false")
        .replace("%CSRF_SCRIPT%", csrf_script)
        .replace("%DEBUG_SCRIPT%", debug_script)
        .replace("%VENDOR_RESOURCES%", vendor_resources)
        .replace("%USER_CSS%", user_css)
        .replace("%ROOT_STYLE%", root_style)
        .replace("%DISCONNECT_TIMEOUT%", str(disconnect_timeout))
        .replace("%VIEW_ID%", view_id)
    )


def build_html_response(html: str) -> HTMLResponse:
    return HTMLResponse(html, headers=NO_CACHE_HEADERS)