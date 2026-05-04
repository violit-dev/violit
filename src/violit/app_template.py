HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html class="%HTML_CLASS%">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="htmx-config" content='{"defaultSwapDelay":0,"defaultSettleDelay":0}'>
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="preconnect" href="https://cdn.plot.ly">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <title>%TITLE%</title>
    <script>var mode = window.__vlMode = "%MODE%";</script>
    %CSRF_SCRIPT%
    %DEBUG_SCRIPT%
    %VENDOR_RESOURCES%
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        :root { 
            %CSS_VARS%
            --sidebar-width: %SIDEBAR_WIDTH%;
            --sidebar-min-width: %SIDEBAR_MIN_WIDTH%;
            --sidebar-max-width: %SIDEBAR_MAX_WIDTH%;
            --vl-sidebar-width: var(--sidebar-width);
        }
           wa-callout { --wa-color-brand-fill-loud: var(--vl-primary); }
           wa-callout::part(base) { border: 1px solid var(--vl-border); }
        
           wa-button {
               --wa-color-brand-fill-loud: var(--vl-primary);
               --wa-color-brand-border-loud: color-mix(in srgb, var(--vl-primary), black 10%);
             caret-color: transparent;
        }
        wa-badge {
            padding: 0.4em 0.7em;
            line-height: 1.1;
            border-width: var(--wa-border-width-s, 1px);
            border-style: solid;
        }
        html {
            overflow-y: scroll;
            scrollbar-gutter: stable;
        }
        html.vl-splash-active, body.vl-splash-active {
            overflow: hidden !important;
            overscroll-behavior: none;
        }
        body { margin: 0; background: var(--vl-bg); color: var(--vl-text); font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; min-height: 100vh; overflow-x: hidden; transition: background 0.3s, color 0.3s; }
        
        /* Soft Animation Mode - Only for sidebar; page transitions are applied by JS on navigation only */
        body.anim-soft #sidebar { transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease, opacity 0.3s ease; }
        
        /* Hard Animation Mode */
        body.anim-hard *, body.anim-hard ::part(base) { transition: none !important; animation: none !important; }
        
        #root { display: flex; width: 100%; min-height: 100vh; }
        #sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: var(--vl-sidebar-width);
            height: 100vh;
            background: var(--vl-bg-card);
            border-right: 1px solid var(--vl-border);
            padding: 2rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            overflow-y: auto;
            overflow-x: hidden;
            white-space: nowrap;
            z-index: 1100;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease, opacity 0.3s ease;
        }
        #sidebar.collapsed { width: 0 !important; padding: 2rem 0 !important; border-right: none !important; opacity: 0 !important; pointer-events: none; }
        #sidebar-resizer {
            position: fixed;
            top: 0;
            left: var(--vl-sidebar-width);
            width: 14px;
            height: 100vh;
            transform: translateX(-50%);
            cursor: col-resize;
            z-index: 1101;
            background: transparent;
            touch-action: none;
            transition: opacity 0.2s ease;
        }
        #sidebar-resizer::after {
            content: '';
            position: absolute;
            inset: 0;
            width: 2px;
            margin: 0 auto;
            background: color-mix(in srgb, var(--vl-border), var(--vl-primary) 22%);
            opacity: 0.55;
            transition: background 0.2s ease, opacity 0.2s ease;
        }
        #sidebar-resizer:hover::after,
        body.sidebar-resizing #sidebar-resizer::after {
            background: var(--vl-primary);
            opacity: 1;
        }
        #sidebar.collapsed + #sidebar-resizer,
        #sidebar-resizer[style*='display: none'] {
            opacity: 0;
            pointer-events: none;
        }
        body.sidebar-resizing {
            cursor: col-resize;
            user-select: none;
        }
        
        #main {
            flex: 1;
            margin-left: var(--vl-sidebar-width);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0 1.5rem 3rem 2.5rem;
            transition: margin-left 0.3s ease, padding 0.3s ease;
        }
        #main.sidebar-collapsed { margin-left: 0; }
        /* Chat input container positioning - pinned composers respect sidebar */
        .chat-input-container[data-chat-pinned="true"] { left: var(--vl-sidebar-width) !important; transition: left 0.3s ease; }
        #sidebar.collapsed ~ #main .chat-input-container[data-chat-pinned="true"],
        #main.sidebar-collapsed .chat-input-container[data-chat-pinned="true"] { left: 0 !important; }
        
        #header { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; padding: 1rem 0; display: flex; align-items: center; }
        #app { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; display: flex; flex-direction: column; gap: 1.5rem; }
        .nav-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            width: 100%;
        }
        .nav-container wa-button {
            width: 100%;
            caret-color: transparent;
        }
        
        .fragment { display: flex; flex-direction: column; gap: 1.25rem; width: 100%; }
        .page-container { display: flex; flex-direction: column; gap: %WIDGET_GAP%; width: 100%; }
        .card { background: var(--vl-bg-card); border: 1px solid var(--vl-border); padding: 1.5rem; border-radius: var(--vl-radius); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
        
        /* Widget spacing - natural breathing room */
        .page-container > div { margin-bottom: 0.5rem; }
        
        /* Headings need more space above to separate sections */
        h1, h2, h3 { font-weight: 600; margin: 0; }
        h1 { font-size: 2.25rem; line-height: 1.2; margin-bottom: 1rem; }
        h2 { font-size: 1.5rem; line-height: 1.3; margin-top: 1.5rem; margin-bottom: 0.75rem; }
        h3 { font-size: 1.25rem; line-height: 1.4; margin-top: 1.25rem; margin-bottom: 0.5rem; }
        .page-container > h1:first-child, .page-container > h2:first-child, .page-container > h3:first-child,
        h1:first-child, h2:first-child, h3:first-child { margin-top: 0; }
        
        /* Web Awesome component spacing */
        wa-input, wa-select, wa-textarea, wa-slider, wa-checkbox, wa-switch, wa-radio-group, wa-color-picker {
            display: block;
            margin-bottom: 1rem;
        }
        wa-textarea::part(form-control-input) {
            min-height: 6.25rem;
        }
        wa-textarea::part(textarea) {
            min-height: 6.25rem;
            line-height: 1.5;
            box-sizing: border-box;
        }
        wa-callout {
            margin-bottom: 1.25rem;
        }
        wa-callout.vl-alert {
            --vl-alert-accent: var(--vl-primary);
            --vl-alert-border: color-mix(in srgb, var(--vl-alert-accent) 34%, var(--vl-border) 66%);
            --vl-alert-text: color-mix(in srgb, var(--vl-alert-accent) 38%, var(--vl-text) 62%);
            --vl-alert-strong: color-mix(in srgb, var(--vl-alert-accent) 74%, var(--vl-text) 26%);
            --vl-alert-bg-start: color-mix(in srgb, white 84%, var(--vl-alert-accent) 16%);
            --vl-alert-bg-end: color-mix(in srgb, var(--vl-bg-card) 87%, var(--vl-alert-accent) 13%);
            --vl-alert-bg: linear-gradient(135deg, var(--vl-alert-bg-start) 0%, var(--vl-alert-bg-end) 100%);
            --vl-alert-icon-bg: color-mix(in srgb, var(--vl-alert-accent) 14%, white 86%);
            --vl-alert-inline-bg: color-mix(in srgb, var(--vl-alert-accent) 10%, var(--vl-bg) 90%);
            --vl-alert-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
            display: flex;
            align-items: center;
            gap: 0.9rem;
            padding: 1rem 1.15rem;
            border: 1px solid var(--vl-alert-border);
            border-inline-start: 4px solid var(--vl-alert-accent);
            border-radius: calc(var(--vl-radius) + 0.35rem);
            background: var(--vl-alert-bg);
            color: var(--vl-alert-text);
            box-shadow: var(--vl-alert-shadow);
        }
        html.wa-dark wa-callout.vl-alert {
            --vl-alert-border: color-mix(in srgb, var(--vl-alert-accent) 44%, var(--vl-border) 56%);
            --vl-alert-text: color-mix(in srgb, var(--vl-alert-accent) 18%, var(--vl-text) 82%);
            --vl-alert-strong: color-mix(in srgb, var(--vl-alert-accent) 58%, white 42%);
            --vl-alert-bg-start: color-mix(in srgb, var(--vl-bg-card) 84%, var(--vl-alert-accent) 16%);
            --vl-alert-bg-end: color-mix(in srgb, var(--vl-bg) 88%, var(--vl-alert-accent) 12%);
            --vl-alert-icon-bg: color-mix(in srgb, var(--vl-alert-accent) 22%, var(--vl-bg-card) 78%);
            --vl-alert-inline-bg: color-mix(in srgb, var(--vl-alert-accent) 16%, var(--vl-bg) 84%);
            --vl-alert-shadow: 0 16px 38px rgba(0, 0, 0, 0.28);
        }
        wa-callout.vl-alert::part(icon) {
            flex: 0 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 2.35rem;
            min-width: 2.35rem;
            height: 2.35rem;
            border-radius: 999px;
            background: var(--vl-alert-icon-bg);
            color: var(--vl-alert-accent);
        }
        wa-callout.vl-alert::part(message) {
            flex: 1 1 auto;
            overflow: visible;
        }
        wa-callout.vl-alert[data-vl-has-icon="false"] {
            gap: 0;
        }
        wa-callout.vl-alert[data-vl-has-icon="false"]::part(icon) {
            display: none;
        }
        wa-callout.vl-alert > wa-icon[slot='icon'] {
            margin: 0;
            width: 1.15rem;
            height: 1.15rem;
            font-size: 1.15rem;
        }
        wa-callout.vl-alert.vl-alert--info {
            --vl-alert-accent: #2563eb;
        }
        wa-callout.vl-alert.vl-alert--success {
            --vl-alert-accent: var(--vl-success);
        }
        wa-callout.vl-alert.vl-alert--warning {
            --vl-alert-accent: var(--vl-warning);
        }
        wa-callout.vl-alert.vl-alert--danger {
            --vl-alert-accent: var(--vl-danger);
        }
        wa-callout.vl-alert.vl-alert--neutral {
            --vl-alert-accent: color-mix(in srgb, var(--vl-text-muted) 74%, var(--vl-border) 26%);
        }
        .vl-alert__body {
            display: block;
            width: 100%;
            line-height: 1.6;
        }
        .vl-alert__body strong {
            font-weight: 700;
            color: var(--vl-alert-strong);
        }
        .vl-alert__body code {
            padding: 0.15rem 0.4rem;
            border-radius: 0.45rem;
            background: var(--vl-alert-inline-bg);
            color: var(--vl-alert-strong);
            font-size: 0.92em;
        }
        wa-button {
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
        }
        wa-divider, .divider {
            --color: var(--vl-border);
            margin: 1.5rem 0;
            width: 100%;
        }
        
        /* Column layouts - using CSS variables for flexible override */
        .columns { 
            display: grid; 
            grid-template-columns: var(--vl-cols, 1fr 1fr); 
            gap: var(--vl-gap, 1rem); 
            align-items: stretch;
            width: 100%; 
            margin-bottom: 0.5rem; 
        }
        .column-item {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            min-width: 0;
        }
        .columns.columns--bordered > .column-item {
            padding: 1rem;
            border: 1px solid var(--vl-border);
            border-radius: 0.85rem;
            background: var(--vl-surface);
        }
        .columns.columns--equal-height > .column-item {
            height: 100%;
        }
        .columns.columns--equal-height > .column-item > :first-child:last-child {
            height: 100%;
        }
        .vl-metric-card {
            box-sizing: border-box;
        }
        .vl-metric-card--fill {
            height: 100%;
        }
        wa-button.vl-button-fill {
            display: block;
            height: 100%;
            margin-top: 0;
            margin-bottom: 0;
        }
        wa-button.vl-button-fill::part(base) {
            width: 100%;
            min-height: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .column { flex: 1; display: flex; flex-direction: column; gap: 0.75rem; }
        
        /* List container - predefined layout for reactive lists */
        .violit-list-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            width: 100%;
        }
        .violit-list-container > * {
            width: 100%;
        }
        .violit-list-container wa-card {
            width: 100%;
        }
        
        .gradient-text { background: linear-gradient(to right, var(--vl-primary), var(--vl-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-muted { color: var(--vl-text-muted); }
        .metric-label { color: var(--vl-text-muted); font-size: 0.875rem; margin-bottom: 0.25rem; }
        .metric-value { font-size: 2rem; font-weight: 600; }
        .no-select { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
        
        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Animations for Balloons and Snow */
        @keyframes float-up {
            0% { transform: translateY(var(--start-y, 100vh)) rotate(0deg); opacity: 1; }
            100% { transform: translateY(-20vh) rotate(360deg); opacity: 0; }
        }
        @keyframes fall-down {
            0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
        }
        .balloon, .snowflake {
            position: fixed;
            z-index: 9999;
            pointer-events: none;
            font-size: 2rem;
            user-select: none;
        }
        .balloon { animation: float-up var(--duration) linear forwards; }
        .snowflake { animation: fall-down var(--duration) linear forwards; }
        
        /* ===== Mobile Responsive ===== */
        @media (max-width: 768px) {
            /* Prevent horizontal scroll at root level */
            html, body { overflow-x: hidden; }
            
            /* Force text wrapping on mobile */
            body {
                font-size: 17px !important;
                line-height: 1.7 !important;
                overflow-wrap: break-word;
                word-wrap: break-word;
            }
            
            /* Sidebar: off-canvas overlay on mobile */
            #sidebar {
                width: 280px !important;
                transform: translateX(-100%);
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease !important;
                z-index: 2000;
            }
            #sidebar-resizer {
                display: none !important;
            }
            #sidebar.mobile-open {
                transform: translateX(0) !important;
                box-shadow: 4px 0 24px rgba(0,0,0,0.18);
            }
            #sidebar.collapsed {
                transform: translateX(-100%) !important;
                width: 280px !important;
                padding: 2rem 1rem !important;
                opacity: 1 !important;
            }
            
            /* Sidebar backdrop for overlay */
            .vl-sidebar-backdrop {
                position: fixed;
                inset: 0;
                background: rgba(0,0,0,0.4);
                z-index: 1999;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
            }
            .vl-sidebar-backdrop.active {
                opacity: 1;
                pointer-events: auto;
            }
            
            /* Main: full width, no sidebar offset */
            #main {
                margin-left: 0 !important;
                padding: 0 1rem 2rem 1rem !important;
                max-width: 100vw;
            }
            
            /* App container: constrain width, less gap */
            #app {
                gap: 1rem;
                max-width: 100%;
            }
            
            /* Columns: stack vertically on mobile */
            .columns {
                grid-template-columns: 1fr !important;
            }
            .column-item {
                height: auto !important;
            }
            
            /* Chat input: full width on mobile */
            .chat-input-container {
                left: 0 !important;
                width: 100% !important;
            }
            
            /* Typography: improve readability on mobile */
            h1 { font-size: 1.75rem !important; }
            h2 { font-size: 1.3rem !important; }
            h3 { font-size: 1.1rem !important; }
            p, span, div, li { overflow-wrap: break-word; word-wrap: break-word; }
            
            /* Images & videos: prevent overflow */
            img, video, iframe { max-width: 100%; height: auto; }
            
            /* Code blocks: constrain to viewport */
            .violit-code-block { max-width: calc(100vw - 2rem); overflow: hidden; }
            pre, .code-block { overflow-x: auto; max-width: 100%; }
            pre { font-size: 0.82rem !important; }
            
            /* Cards: tighter padding on mobile */
            .card { padding: 1rem; }
            
            /* Table: horizontal scroll wrapper */
            .ag-theme-alpine, .ag-theme-alpine-dark, table {
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                max-width: 100%;
            }

            .vl-ag-grid {
                border: 1px solid var(--ag-border-color, var(--vl-border));
                border-radius: var(--vl-radius);
                overflow: hidden;
                background: var(--ag-background-color, var(--vl-bg-card));
                color: var(--ag-foreground-color, var(--vl-text));
            }

            .vl-ag-grid .ag-root-wrapper,
            .vl-ag-grid .ag-header,
            .vl-ag-grid .ag-row,
            .vl-ag-grid .ag-cell,
            .vl-ag-grid .ag-input-field-input,
            .vl-ag-grid .ag-picker-field-wrapper {
                transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
            }
            
            /* Ensure minimum readable font size for small text */
            .page-container p, .page-container span, .page-container div {
                font-size: max(0.9rem, inherit);
            }
            
            /* Hide hamburger when no sidebar content */
            #sidebar[style*="display: none"] ~ #main #header {
                display: none;
            }
        }
    </style>
    %USER_CSS%
</head>
<body class="%BODY_CLASS%">
    %SPLASH%
    <div id="root" style="%ROOT_STYLE%">
        <div id="sidebar" style="%SIDEBAR_STYLE%">
            %SIDEBAR_CONTENT%
        </div>
        <div id="sidebar-resizer" style="%SIDEBAR_RESIZER_STYLE%" aria-hidden="true"></div>
    <div id="main" class="%MAIN_CLASS%">
        <div id="header">
             <wa-button variant="neutral" appearance="plain" onclick="toggleSidebar()"><wa-icon name="list" style="pointer-events: none;"></wa-icon></wa-button>
        </div>
        <div id="app">%CONTENT%</div>
    </div>
    </div>
    <div id="toast-injector" style="display:none;"></div>
    <script>
        window.__vlRuntimeConfig = {
            sidebarResizable: %SIDEBAR_RESIZABLE%,
            disconnectTimeout: %DISCONNECT_TIMEOUT%,
            viewId: "%VIEW_ID%",
            viewRestoreToken: "%VIEW_RESTORE_TOKEN%"
        };
    </script>
    <script src="/static/runtime/violit_app_runtime.js?v=%RUNTIME_ASSET_VERSION%"></script>
</body>
</html>
"""