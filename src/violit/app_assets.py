CDN_VENDOR_RESOURCES = """
    <link rel="stylesheet" data-vl-critical="true" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/webawesome.css" />
    <link rel="preload" data-vl-critical="true" as="style" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" /></noscript>
    <script type="module" src="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js"></script>
    <script type="module">
        import { getIconLibrary, registerIconLibrary, setDefaultIconFamily } from 'https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js';

        const legacyViolitIconAliases = Object.freeze({
            'person-fill': 'user',
            'check-circle': 'circle-check',
            'x-circle': 'circle-xmark',
            'info-circle': 'circle-info',
            'exclamation-triangle': 'triangle-exclamation',
            'exclamation-circle': 'circle-exclamation',
            'exclamation-octagon': 'octagon-exclamation',
            'plus-circle': 'circle-plus',
            'circle-fill': 'circle',
            'journal-text': 'note-sticky',
            'check2': 'check'
        });

        const defaultLibrary = getIconLibrary('default');
        if (defaultLibrary) {
            registerIconLibrary('default', {
                resolver: (name, family, variant, autoWidth) => {
                    const normalized = legacyViolitIconAliases[name] || name;
                    return defaultLibrary.resolver(normalized, family, variant, autoWidth);
                },
                mutator: defaultLibrary.mutator,
                spriteSheet: defaultLibrary.spriteSheet
            });
        }

        setDefaultIconFamily('classic');
        window.__vlNormalizeIconName = function(name) {
            return legacyViolitIconAliases[name] || name || 'circle-question';
        };
    </script>
    <script src="https://unpkg.com/htmx.org@1.9.10" defer></script>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet"></noscript>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-light pre code.hljs { background: transparent !important; }
        .violit-code-dark pre code.hljs { background: transparent !important; }
    </style>
    <script>
        // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  'https://cdn.plot.ly/plotly-2.27.0.min.js',
            'agGrid':  'https://cdn.jsdelivr.net/npm/ag-grid-community@31.0.1/dist/ag-grid-community.min.js',
                'hljs':    'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js',
                'katex':   'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js'
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
        import { getIconLibrary, registerIconLibrary, setDefaultIconFamily } from '/static/vendor/webawesome/webawesome.loader.js';

        const legacyViolitIconAliases = Object.freeze({
            'person-fill': 'user',
            'check-circle': 'circle-check',
            'x-circle': 'circle-xmark',
            'info-circle': 'circle-info',
            'exclamation-triangle': 'triangle-exclamation',
            'exclamation-circle': 'circle-exclamation',
            'exclamation-octagon': 'octagon-exclamation',
            'plus-circle': 'circle-plus',
            'circle-fill': 'circle',
            'journal-text': 'note-sticky',
            'check2': 'check'
        });

        const defaultLibrary = getIconLibrary('default');
        if (defaultLibrary) {
            registerIconLibrary('default', {
                resolver: (name, family, variant, autoWidth) => {
                    const normalized = legacyViolitIconAliases[name] || name;
                    return defaultLibrary.resolver(normalized, family, variant, autoWidth);
                },
                mutator: defaultLibrary.mutator,
                spriteSheet: defaultLibrary.spriteSheet
            });
        }

        setDefaultIconFamily('classic');
        window.__vlNormalizeIconName = function(name) {
            return legacyViolitIconAliases[name] || name || 'circle-question';
        };
    </script>
    <script src="/static/vendor/htmx/htmx.min.js" defer></script>
    <script src="/static/vendor/tailwindcss/tailwind.browser.js" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="/static/vendor/highlightjs/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/static/vendor/highlightjs/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-light pre code.hljs { background: transparent !important; }
        .violit-code-dark pre code.hljs { background: transparent !important; }
    </style>
    <script>
    // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  '/static/vendor/plotly/plotly-2.27.0.min.js',
            'agGrid':  '/static/vendor/ag-grid/ag-grid-community.min.js',
            'hljs':    '/static/vendor/highlightjs/highlight.min.js',
            'katex':   'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js'
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


def get_vendor_resources(use_cdn: bool, active_theme_name: str, inactive_theme_name: str) -> str:
    template = CDN_VENDOR_RESOURCES if use_cdn else LOCAL_VENDOR_RESOURCES
    return template.replace("__ACTIVE_THEME__", active_theme_name).replace("__INACTIVE_THEME__", inactive_theme_name)