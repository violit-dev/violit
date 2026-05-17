CDN_PRECONNECT_LINKS = """
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="preconnect" href="https://cdn.plot.ly">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
"""


CDN_VENDOR_RESOURCES = """
    <link rel="stylesheet" data-vl-critical="true" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/webawesome.css" />
    <link rel="preload" data-vl-critical="true" as="style" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" /></noscript>
    <script type="module" src="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js"></script>
    <script type="module">
        import { setDefaultIconFamily } from 'https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js';

        setDefaultIconFamily('classic');
    </script>
    <script src="https://unpkg.com/htmx.org@1.9.10" defer></script>
    <link rel="preload" as="script" href="https://cdn.jsdelivr.net/npm/ag-grid-community@31.0.1/dist/ag-grid-community.min.js">
    <link rel="preload" as="script" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js">
    <link rel="preload" as="script" href="/static/vendor/katex/katex.min.js">
    <link rel="preload" as="style" href="/static/vendor/katex/katex.min.css">
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet"></noscript>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-block {
            position: relative;
            border-radius: 0.875rem;
            overflow: hidden;
            border: 1px solid var(--vl-code-border);
            background: var(--vl-code-bg);
            box-shadow: 0 18px 38px color-mix(in srgb, var(--vl-code-border) 10%, transparent);
        }
        .violit-code-block.violit-code-theme-auto {
            --vl-code-bg: linear-gradient(180deg, color-mix(in srgb, var(--vl-bg-card) 94%, var(--vl-bg) 6%), color-mix(in srgb, var(--vl-bg-card) 88%, var(--vl-bg) 12%));
            --vl-code-border: color-mix(in srgb, var(--vl-border) 84%, var(--vl-primary) 16%);
            --vl-code-bar-bg: color-mix(in srgb, var(--vl-bg-card) 74%, var(--vl-bg) 26%);
            --vl-code-title: var(--vl-text-muted);
            --vl-code-line-num: color-mix(in srgb, var(--vl-text-muted) 76%, var(--vl-border) 24%);
            --vl-code-copy: var(--vl-text-muted);
            --vl-code-copy-hover: var(--vl-text);
            --vl-code-copy-bg: color-mix(in srgb, var(--vl-bg-card) 88%, var(--vl-bg) 12%);
            --vl-code-thumb: color-mix(in srgb, var(--vl-text) 18%, transparent);
            --vl-code-thumb-hover: color-mix(in srgb, var(--vl-text) 28%, transparent);
            --vl-code-text: color-mix(in srgb, var(--vl-text) 94%, var(--vl-bg) 6%);
            --vl-code-comment: color-mix(in srgb, var(--vl-text-muted) 82%, var(--vl-bg) 18%);
            --vl-code-keyword: color-mix(in srgb, var(--vl-primary) 68%, var(--vl-text) 32%);
            --vl-code-string: color-mix(in srgb, var(--vl-secondary, var(--vl-primary)) 74%, var(--vl-text) 26%);
            --vl-code-number: color-mix(in srgb, var(--vl-danger, var(--vl-primary)) 70%, var(--vl-text) 30%);
            --vl-code-title-color: color-mix(in srgb, var(--vl-primary) 42%, var(--vl-text) 58%);
            --vl-code-type: color-mix(in srgb, var(--vl-secondary, var(--vl-primary)) 54%, var(--vl-text) 46%);
            --vl-code-meta: color-mix(in srgb, var(--vl-text-muted) 54%, var(--vl-primary) 46%);
            --vl-code-addition: color-mix(in srgb, var(--vl-success, #16a34a) 76%, var(--vl-text) 24%);
            --vl-code-deletion: color-mix(in srgb, var(--vl-danger, #dc2626) 76%, var(--vl-text) 24%);
        }
        .violit-code-block.violit-code-theme-light {
            --vl-code-bg: #fcfcfd;
            --vl-code-border: #d8dee9;
            --vl-code-bar-bg: #f3f4f6;
            --vl-code-title: #6b7280;
            --vl-code-line-num: #94a3b8;
            --vl-code-copy: #667085;
            --vl-code-copy-hover: #0f172a;
            --vl-code-copy-bg: rgba(255, 255, 255, 0.88);
            --vl-code-thumb: rgba(15, 23, 42, 0.16);
            --vl-code-thumb-hover: rgba(15, 23, 42, 0.28);
            --vl-code-text: #24292f;
            --vl-code-comment: #6e7781;
            --vl-code-keyword: #cf222e;
            --vl-code-string: #0a3069;
            --vl-code-number: #0550ae;
            --vl-code-title-color: #8250df;
            --vl-code-type: #116329;
            --vl-code-meta: #953800;
            --vl-code-addition: #1a7f37;
            --vl-code-deletion: #cf222e;
        }
        .violit-code-block.violit-code-theme-dark {
            --vl-code-bg: #0f172a;
            --vl-code-border: #334155;
            --vl-code-bar-bg: #0b1220;
            --vl-code-title: #94a3b8;
            --vl-code-line-num: #64748b;
            --vl-code-copy: #94a3b8;
            --vl-code-copy-hover: #f8fafc;
            --vl-code-copy-bg: rgba(15, 23, 42, 0.78);
            --vl-code-thumb: rgba(255, 255, 255, 0.18);
            --vl-code-thumb-hover: rgba(255, 255, 255, 0.3);
            --vl-code-text: #e5edf5;
            --vl-code-comment: #8b949e;
            --vl-code-keyword: #ff7b72;
            --vl-code-string: #a5d6ff;
            --vl-code-number: #79c0ff;
            --vl-code-title-color: #d2a8ff;
            --vl-code-type: #7ee787;
            --vl-code-meta: #ffa657;
            --vl-code-addition: #7ee787;
            --vl-code-deletion: #ff7b72;
        }
        .violit-code-content {
            position: relative;
        }
        .violit-code-titlebar {
            padding: 0.72rem 1rem;
            background: var(--vl-code-bar-bg);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
        }
        .violit-code-title {
            margin-left: 0.75rem;
            font-size: 0.8rem;
            color: var(--vl-code-title);
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }
        .violit-code-traffic-dot {
            width: 12px;
            height: 12px;
            border-radius: 999px;
            flex: 0 0 auto;
        }
        .violit-code-traffic-dot-close { background: #ff5f57; }
        .violit-code-traffic-dot-minimize { background: #febc2e; }
        .violit-code-traffic-dot-expand { background: #28c840; }
        .violit-code-copy-button {
            position: absolute;
            top: 0.65rem;
            right: 0.65rem;
            display: inline-flex;
            align-items: center;
            gap: 0.32rem;
            padding: 0.34rem 0.56rem;
            border-radius: 0.45rem;
            border: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
            background: var(--vl-code-copy-bg);
            color: var(--vl-code-copy);
            cursor: pointer;
            font-size: 0.75rem;
            font-family: inherit;
            transition: color 0.18s ease, border-color 0.18s ease, background 0.18s ease;
            z-index: 2;
            backdrop-filter: blur(8px);
        }
        .violit-code-copy-button:hover {
            color: var(--vl-code-copy-hover);
            border-color: color-mix(in srgb, var(--vl-code-copy-hover) 42%, var(--vl-code-border) 58%);
        }
        .violit-code-line-numbers {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            padding: 1rem 0.75rem 1rem 1rem;
            text-align: right;
            color: var(--vl-code-line-num);
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            font-size: 0.8rem;
            line-height: 1.7;
            user-select: none;
            pointer-events: none;
            border-right: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
        }
        .violit-code-pre {
            margin: 0;
            padding: 1rem 3.5rem 1rem var(--vl-code-padding-left, 1.25rem);
            overflow-x: auto;
            font-size: 0.875rem;
            line-height: 1.7;
            background: transparent;
        }
        .violit-code-wrap .violit-code-pre {
            white-space: pre-wrap;
            word-break: break-word;
        }
        .violit-code-block pre code.hljs {
            display: block;
            background: transparent !important;
            color: var(--vl-code-text);
            padding: 0;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }
        .violit-code-wrap pre code.hljs {
            white-space: pre-wrap;
        }
        .violit-code-block pre code.hljs.nohighlight {
            color: var(--vl-code-text);
        }
        .violit-code-block *::-webkit-scrollbar {
            height: 6px;
            width: 6px;
        }
        .violit-code-block *::-webkit-scrollbar-track,
        .violit-code-block *::-webkit-scrollbar-corner {
            background: transparent;
        }
        .violit-code-block *::-webkit-scrollbar-thumb {
            background-color: var(--vl-code-thumb);
            border-radius: 999px;
        }
        .violit-code-block *::-webkit-scrollbar-thumb:hover {
            background-color: var(--vl-code-thumb-hover);
        }
        .violit-code-block .hljs-comment,
        .violit-code-block .hljs-quote {
            color: var(--vl-code-comment);
            font-style: italic;
        }
        .violit-code-block .hljs-keyword,
        .violit-code-block .hljs-selector-tag,
        .violit-code-block .hljs-built_in,
        .violit-code-block .hljs-name,
        .violit-code-block .hljs-tag {
            color: var(--vl-code-keyword);
        }
        .violit-code-block .hljs-string,
        .violit-code-block .hljs-symbol,
        .violit-code-block .hljs-bullet,
        .violit-code-block .hljs-template-variable,
        .violit-code-block .hljs-attribute {
            color: var(--vl-code-string);
        }
        .violit-code-block .hljs-number,
        .violit-code-block .hljs-literal,
        .violit-code-block .hljs-variable,
        .violit-code-block .hljs-link {
            color: var(--vl-code-number);
        }
        .violit-code-block .hljs-title,
        .violit-code-block .hljs-title.function_,
        .violit-code-block .hljs-section,
        .violit-code-block .hljs-selector-id {
            color: var(--vl-code-title-color);
        }
        .violit-code-block .hljs-type,
        .violit-code-block .hljs-class .hljs-title,
        .violit-code-block .hljs-selector-class,
        .violit-code-block .hljs-doctag {
            color: var(--vl-code-type);
        }
        .violit-code-block .hljs-meta,
        .violit-code-block .hljs-meta .hljs-keyword,
        .violit-code-block .hljs-regexp {
            color: var(--vl-code-meta);
        }
        .violit-code-block .hljs-addition {
            color: var(--vl-code-addition);
        }
        .violit-code-block .hljs-deletion {
            color: var(--vl-code-deletion);
        }
        .violit-code-block .hljs-operator,
        .violit-code-block .hljs-punctuation,
        .violit-code-block .hljs-subst {
            color: var(--vl-code-text);
        }
    </style>
    <script>
        // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  'https://cdn.plot.ly/plotly-2.27.0.min.js',
            'agGrid':  'https://cdn.jsdelivr.net/npm/ag-grid-community@31.0.1/dist/ag-grid-community.min.js',
                'hljs':    'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js',
                'katex':   '/static/vendor/katex/katex.min.js'
        };
        var _q = {};  // callback queues per lib
        var _s = {};  // loading state: 0=idle, 1=loading, 2=ready
        window._vlLoadLib = function(name, cb) {
            if (window[name]) { cb(); return; }
            if (!_q[name]) _q[name] = [];
            _q[name].push(cb);
            if (_s[name]) return;  // already loading
            _s[name] = 1;
            var s = document.createElement('script');
            s.src = _libs[name];
            s.onload = function() {
                _s[name] = 2;
                var cbs = _q[name] || [];
                _q[name] = [];
                cbs.forEach(function(fn) { fn(); });
            };
            document.head.appendChild(s);
        };

        window._vlPreloadLib = function(name) {
            if (window[name] || _s[name]) return;

            var run = function() {
                window._vlLoadLib(name, function() {});
            };

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(run, { timeout: 1500 });
            } else {
                setTimeout(run, 200);
            }
        };

        var _deferredActionQueue = [];
        var _deferredActionKeys = new Set();
        var _deferredActionBusy = false;

        function _drainDeferredActions() {
            if (_deferredActionBusy || !_deferredActionQueue.length) return;

            if (!window.sendAction) {
                setTimeout(_drainDeferredActions, 50);
                return;
            }

            _deferredActionBusy = true;
            var next = _deferredActionQueue.shift();
            _deferredActionKeys.delete(next.cid + '::' + next.value);
            window.sendAction(next.cid, next.value);

            setTimeout(function() {
                _deferredActionBusy = false;
                if (_deferredActionQueue.length) {
                    if ('requestIdleCallback' in window) {
                        window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
                    } else {
                        setTimeout(_drainDeferredActions, 16);
                    }
                }
            }, 16);
        }

        window._vlQueueDeferredAction = function(cid, value) {
            var key = cid + '::' + value;
            if (_deferredActionKeys.has(key)) return;

            _deferredActionKeys.add(key);
            _deferredActionQueue.push({ cid: cid, value: value });

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
            } else {
                setTimeout(_drainDeferredActions, 0);
            }
        };
    })();
    </script>
                """


LOCAL_VENDOR_RESOURCES = """
    <link rel="stylesheet" data-vl-critical="true" href="/static/vendor/webawesome/styles/webawesome.css" />
    <link rel="preload" data-vl-critical="true" as="style" href="/static/vendor/webawesome/styles/themes/default.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/static/vendor/webawesome/styles/themes/default.css" /></noscript>
    <script type="module" src="/static/vendor/webawesome/webawesome.loader.js"></script>
    <script type="module">
        import { getIconLibrary, registerIconLibrary, setDefaultIconFamily } from '/static/vendor/webawesome/components/icon/library.js';

        const allowRemoteFontAwesomeFallback = %FONTAWESOME_REMOTE_FALLBACK%;
        const fallbackIconUrl = '/static/vendor/fontawesome/regular/circle-question.svg';
        const originalDefaultIconLibrary = getIconLibrary('default');
        const localIconManifestPromise = fetch('/static/vendor/fontawesome/manifest.json')
            .then((response) => response.ok ? response.json() : { solid: [], regular: ['circle-question'], brands: [] })
            .catch(() => ({ solid: [], regular: ['circle-question'], brands: [] }))
            .then((manifest) => ({
                solid: new Set(manifest.solid || []),
                regular: new Set(manifest.regular || []),
                brands: new Set(manifest.brands || []),
            }));

        function getLocalIconFolder(family = 'classic', variant = 'solid') {
            if (family === 'brands') {
                return 'brands';
            }

            if (family === 'classic' && variant === 'regular') {
                return 'regular';
            }

            return 'solid';
        }

        function resolveLocalIconFolder(name, family, variant, manifest) {
            const requestedFolder = getLocalIconFolder(family, variant);

            if (manifest[requestedFolder] && manifest[requestedFolder].has(name)) {
                return requestedFolder;
            }

            for (const folder of ['solid', 'regular', 'brands']) {
                if (folder !== requestedFolder && manifest[folder] && manifest[folder].has(name)) {
                    return folder;
                }
            }

            return null;
        }

        registerIconLibrary('default', {
            resolver: async (name, family = 'classic', variant = 'solid') => {
                const manifest = await localIconManifestPromise;
                const folder = resolveLocalIconFolder(name, family, variant, manifest);

                if (folder) {
                    return `/static/vendor/fontawesome/${folder}/${name}.svg`;
                }

                if (allowRemoteFontAwesomeFallback && originalDefaultIconLibrary && typeof originalDefaultIconLibrary.resolver === 'function') {
                    return originalDefaultIconLibrary.resolver(name, family, variant);
                }

                return fallbackIconUrl;
            },
            mutator: originalDefaultIconLibrary && typeof originalDefaultIconLibrary.mutator === 'function'
                ? originalDefaultIconLibrary.mutator
                : undefined,
            spriteSheet: originalDefaultIconLibrary ? originalDefaultIconLibrary.spriteSheet : undefined,
        });

        setDefaultIconFamily('classic');
    </script>
    <script src="/static/vendor/htmx/htmx.min.js" defer></script>
    <link rel="preload" as="script" href="/static/vendor/ag-grid/ag-grid-community.min.js">
    <link rel="preload" as="script" href="/static/vendor/highlightjs/highlight.min.js">
    <link rel="preload" as="script" href="/static/vendor/katex/katex.min.js">
    <link rel="preload" as="style" href="/static/vendor/katex/katex.min.css">
    <script src="/static/vendor/tailwindcss/tailwind.browser.js" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="/static/vendor/highlightjs/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/static/vendor/highlightjs/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-block {
            position: relative;
            border-radius: 0.875rem;
            overflow: hidden;
            border: 1px solid var(--vl-code-border);
            background: var(--vl-code-bg);
            box-shadow: 0 18px 38px color-mix(in srgb, var(--vl-code-border) 10%, transparent);
        }
        .violit-code-block.violit-code-theme-auto {
            --vl-code-bg: linear-gradient(180deg, color-mix(in srgb, var(--vl-bg-card) 94%, var(--vl-bg) 6%), color-mix(in srgb, var(--vl-bg-card) 88%, var(--vl-bg) 12%));
            --vl-code-border: color-mix(in srgb, var(--vl-border) 84%, var(--vl-primary) 16%);
            --vl-code-bar-bg: color-mix(in srgb, var(--vl-bg-card) 74%, var(--vl-bg) 26%);
            --vl-code-title: var(--vl-text-muted);
            --vl-code-line-num: color-mix(in srgb, var(--vl-text-muted) 76%, var(--vl-border) 24%);
            --vl-code-copy: var(--vl-text-muted);
            --vl-code-copy-hover: var(--vl-text);
            --vl-code-copy-bg: color-mix(in srgb, var(--vl-bg-card) 88%, var(--vl-bg) 12%);
            --vl-code-thumb: color-mix(in srgb, var(--vl-text) 18%, transparent);
            --vl-code-thumb-hover: color-mix(in srgb, var(--vl-text) 28%, transparent);
            --vl-code-text: color-mix(in srgb, var(--vl-text) 94%, var(--vl-bg) 6%);
            --vl-code-comment: color-mix(in srgb, var(--vl-text-muted) 82%, var(--vl-bg) 18%);
            --vl-code-keyword: color-mix(in srgb, var(--vl-primary) 68%, var(--vl-text) 32%);
            --vl-code-string: color-mix(in srgb, var(--vl-secondary, var(--vl-primary)) 74%, var(--vl-text) 26%);
            --vl-code-number: color-mix(in srgb, var(--vl-danger, var(--vl-primary)) 70%, var(--vl-text) 30%);
            --vl-code-title-color: color-mix(in srgb, var(--vl-primary) 42%, var(--vl-text) 58%);
            --vl-code-type: color-mix(in srgb, var(--vl-secondary, var(--vl-primary)) 54%, var(--vl-text) 46%);
            --vl-code-meta: color-mix(in srgb, var(--vl-text-muted) 54%, var(--vl-primary) 46%);
            --vl-code-addition: color-mix(in srgb, var(--vl-success, #16a34a) 76%, var(--vl-text) 24%);
            --vl-code-deletion: color-mix(in srgb, var(--vl-danger, #dc2626) 76%, var(--vl-text) 24%);
        }
        .violit-code-block.violit-code-theme-light {
            --vl-code-bg: #fcfcfd;
            --vl-code-border: #d8dee9;
            --vl-code-bar-bg: #f3f4f6;
            --vl-code-title: #6b7280;
            --vl-code-line-num: #94a3b8;
            --vl-code-copy: #667085;
            --vl-code-copy-hover: #0f172a;
            --vl-code-copy-bg: rgba(255, 255, 255, 0.88);
            --vl-code-thumb: rgba(15, 23, 42, 0.16);
            --vl-code-thumb-hover: rgba(15, 23, 42, 0.28);
            --vl-code-text: #24292f;
            --vl-code-comment: #6e7781;
            --vl-code-keyword: #cf222e;
            --vl-code-string: #0a3069;
            --vl-code-number: #0550ae;
            --vl-code-title-color: #8250df;
            --vl-code-type: #116329;
            --vl-code-meta: #953800;
            --vl-code-addition: #1a7f37;
            --vl-code-deletion: #cf222e;
        }
        .violit-code-block.violit-code-theme-dark {
            --vl-code-bg: #0f172a;
            --vl-code-border: #334155;
            --vl-code-bar-bg: #0b1220;
            --vl-code-title: #94a3b8;
            --vl-code-line-num: #64748b;
            --vl-code-copy: #94a3b8;
            --vl-code-copy-hover: #f8fafc;
            --vl-code-copy-bg: rgba(15, 23, 42, 0.78);
            --vl-code-thumb: rgba(255, 255, 255, 0.18);
            --vl-code-thumb-hover: rgba(255, 255, 255, 0.3);
            --vl-code-text: #e5edf5;
            --vl-code-comment: #8b949e;
            --vl-code-keyword: #ff7b72;
            --vl-code-string: #a5d6ff;
            --vl-code-number: #79c0ff;
            --vl-code-title-color: #d2a8ff;
            --vl-code-type: #7ee787;
            --vl-code-meta: #ffa657;
            --vl-code-addition: #7ee787;
            --vl-code-deletion: #ff7b72;
        }
        .violit-code-content {
            position: relative;
        }
        .violit-code-titlebar {
            padding: 0.72rem 1rem;
            background: var(--vl-code-bar-bg);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
        }
        .violit-code-title {
            margin-left: 0.75rem;
            font-size: 0.8rem;
            color: var(--vl-code-title);
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }
        .violit-code-traffic-dot {
            width: 12px;
            height: 12px;
            border-radius: 999px;
            flex: 0 0 auto;
        }
        .violit-code-traffic-dot-close { background: #ff5f57; }
        .violit-code-traffic-dot-minimize { background: #febc2e; }
        .violit-code-traffic-dot-expand { background: #28c840; }
        .violit-code-copy-button {
            position: absolute;
            top: 0.65rem;
            right: 0.65rem;
            display: inline-flex;
            align-items: center;
            gap: 0.32rem;
            padding: 0.34rem 0.56rem;
            border-radius: 0.45rem;
            border: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
            background: var(--vl-code-copy-bg);
            color: var(--vl-code-copy);
            cursor: pointer;
            font-size: 0.75rem;
            font-family: inherit;
            transition: color 0.18s ease, border-color 0.18s ease, background 0.18s ease;
            z-index: 2;
            backdrop-filter: blur(8px);
        }
        .violit-code-copy-button:hover {
            color: var(--vl-code-copy-hover);
            border-color: color-mix(in srgb, var(--vl-code-copy-hover) 42%, var(--vl-code-border) 58%);
        }
        .violit-code-line-numbers {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            padding: 1rem 0.75rem 1rem 1rem;
            text-align: right;
            color: var(--vl-code-line-num);
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            font-size: 0.8rem;
            line-height: 1.7;
            user-select: none;
            pointer-events: none;
            border-right: 1px solid color-mix(in srgb, var(--vl-code-border) 92%, transparent);
        }
        .violit-code-pre {
            margin: 0;
            padding: 1rem 3.5rem 1rem var(--vl-code-padding-left, 1.25rem);
            overflow-x: auto;
            font-size: 0.875rem;
            line-height: 1.7;
            background: transparent;
        }
        .violit-code-wrap .violit-code-pre {
            white-space: pre-wrap;
            word-break: break-word;
        }
        .violit-code-block pre code.hljs {
            display: block;
            background: transparent !important;
            color: var(--vl-code-text);
            padding: 0;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }
        .violit-code-wrap pre code.hljs {
            white-space: pre-wrap;
        }
        .violit-code-block pre code.hljs.nohighlight {
            color: var(--vl-code-text);
        }
        .violit-code-block *::-webkit-scrollbar {
            height: 6px;
            width: 6px;
        }
        .violit-code-block *::-webkit-scrollbar-track,
        .violit-code-block *::-webkit-scrollbar-corner {
            background: transparent;
        }
        .violit-code-block *::-webkit-scrollbar-thumb {
            background-color: var(--vl-code-thumb);
            border-radius: 999px;
        }
        .violit-code-block *::-webkit-scrollbar-thumb:hover {
            background-color: var(--vl-code-thumb-hover);
        }
        .violit-code-block .hljs-comment,
        .violit-code-block .hljs-quote {
            color: var(--vl-code-comment);
            font-style: italic;
        }
        .violit-code-block .hljs-keyword,
        .violit-code-block .hljs-selector-tag,
        .violit-code-block .hljs-built_in,
        .violit-code-block .hljs-name,
        .violit-code-block .hljs-tag {
            color: var(--vl-code-keyword);
        }
        .violit-code-block .hljs-string,
        .violit-code-block .hljs-symbol,
        .violit-code-block .hljs-bullet,
        .violit-code-block .hljs-template-variable,
        .violit-code-block .hljs-attribute {
            color: var(--vl-code-string);
        }
        .violit-code-block .hljs-number,
        .violit-code-block .hljs-literal,
        .violit-code-block .hljs-variable,
        .violit-code-block .hljs-link {
            color: var(--vl-code-number);
        }
        .violit-code-block .hljs-title,
        .violit-code-block .hljs-title.function_,
        .violit-code-block .hljs-section,
        .violit-code-block .hljs-selector-id {
            color: var(--vl-code-title-color);
        }
        .violit-code-block .hljs-type,
        .violit-code-block .hljs-class .hljs-title,
        .violit-code-block .hljs-selector-class,
        .violit-code-block .hljs-doctag {
            color: var(--vl-code-type);
        }
        .violit-code-block .hljs-meta,
        .violit-code-block .hljs-meta .hljs-keyword,
        .violit-code-block .hljs-regexp {
            color: var(--vl-code-meta);
        }
        .violit-code-block .hljs-addition {
            color: var(--vl-code-addition);
        }
        .violit-code-block .hljs-deletion {
            color: var(--vl-code-deletion);
        }
        .violit-code-block .hljs-operator,
        .violit-code-block .hljs-punctuation,
        .violit-code-block .hljs-subst {
            color: var(--vl-code-text);
        }
    </style>
    <script>
    // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  '/static/vendor/plotly/plotly-2.27.0.min.js',
            'agGrid':  '/static/vendor/ag-grid/ag-grid-community.min.js',
            'hljs':    '/static/vendor/highlightjs/highlight.min.js',
            'katex':   '/static/vendor/katex/katex.min.js'
        };
        var _q = {};  // callback queues per lib
        var _s = {};  // loading state: 0=idle, 1=loading, 2=ready
        window._vlLoadLib = function(name, cb) {
            if (window[name]) { cb(); return; }
            if (!_q[name]) _q[name] = [];
            _q[name].push(cb);
            if (_s[name]) return;  // already loading
            _s[name] = 1;
            var s = document.createElement('script');
            s.src = _libs[name];
            s.onload = function() {
                _s[name] = 2;
                var cbs = _q[name] || [];
                _q[name] = [];
                cbs.forEach(function(fn) { fn(); });
            };
            document.head.appendChild(s);
        };

        window._vlPreloadLib = function(name) {
            if (window[name] || _s[name]) return;

            var run = function() {
                window._vlLoadLib(name, function() {});
            };

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(run, { timeout: 1500 });
            } else {
                setTimeout(run, 200);
            }
        };

        var _deferredActionQueue = [];
        var _deferredActionKeys = new Set();
        var _deferredActionBusy = false;

        function _drainDeferredActions() {
            if (_deferredActionBusy || !_deferredActionQueue.length) return;

            if (!window.sendAction) {
                setTimeout(_drainDeferredActions, 50);
                return;
            }

            _deferredActionBusy = true;
            var next = _deferredActionQueue.shift();
            _deferredActionKeys.delete(next.cid + '::' + next.value);
            window.sendAction(next.cid, next.value);

            setTimeout(function() {
                _deferredActionBusy = false;
                if (_deferredActionQueue.length) {
                    if ('requestIdleCallback' in window) {
                        window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
                    } else {
                        setTimeout(_drainDeferredActions, 16);
                    }
                }
            }, 16);
        }

        window._vlQueueDeferredAction = function(cid, value) {
            var key = cid + '::' + value;
            if (_deferredActionKeys.has(key)) return;

            _deferredActionKeys.add(key);
            _deferredActionQueue.push({ cid: cid, value: value });

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
            } else {
                setTimeout(_drainDeferredActions, 0);
            }
        };
    })();
    </script>
    <!-- Fonts: Inter (local vendor woff2) -->
    <style>
        @font-face {
            font-family: 'Inter';
            font-style: normal;
            font-weight: 100 900;
            font-display: swap;
            src: url('/static/vendor/fonts/inter/inter-latin-ext.woff2') format('woff2');
            unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
        }
        @font-face {
            font-family: 'Inter';
            font-style: normal;
            font-weight: 100 900;
            font-display: swap;
            src: url('/static/vendor/fonts/inter/inter-latin.woff2') format('woff2');
            unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
        }
    </style>
                """


def get_vendor_resources(use_cdn: bool, use_cdn_fontawesome_only: bool, active_theme_name: str, inactive_theme_name: str) -> str:
    template = CDN_VENDOR_RESOURCES if use_cdn else LOCAL_VENDOR_RESOURCES
    return (
        template
        .replace("__ACTIVE_THEME__", active_theme_name)
        .replace("__INACTIVE_THEME__", inactive_theme_name)
        .replace("%FONTAWESOME_REMOTE_FALLBACK%", "true" if use_cdn_fontawesome_only else "false")
    )


def get_preconnect_links(use_cdn: bool) -> str:
    return CDN_PRECONNECT_LINKS if use_cdn else ""