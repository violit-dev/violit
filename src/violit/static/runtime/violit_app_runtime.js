        const runtimeConfig = window.__vlRuntimeConfig || {};
        const disconnectTimeout = Number.isFinite(Number(runtimeConfig.disconnectTimeout))
            ? Number(runtimeConfig.disconnectTimeout)
            : -1;
        const viewId = typeof runtimeConfig.viewId === 'string' && runtimeConfig.viewId
            ? runtimeConfig.viewId
            : null;
        const viewRestoreToken = typeof runtimeConfig.viewRestoreToken === 'string' && runtimeConfig.viewRestoreToken
            ? runtimeConfig.viewRestoreToken
            : null;
        const viewParamName = '_vl_view_id';
        const reloadParamName = '_vlr';
        const viewStorageKey = 'violit:view-id:' + window.location.pathname;
        const viewRestoreTokenStorageKey = 'violit:view-restore-token:' + window.location.pathname;
        const viewRestoreCookieName = '_vl_reload_view';
        const logViewIdIssue = (...args) => {
            if (window._debug_mode === true) {
                console.log(...args);
            }
        };

        const readStoredViewId = () => {
            try {
                return window.sessionStorage.getItem(viewStorageKey);
            } catch (error) {
                logViewIdIssue('[view-id] failed to read sessionStorage', error);
                return null;
            }
        };

        const writeStoredViewId = (nextViewId) => {
            try {
                if (nextViewId) {
                    window.sessionStorage.setItem(viewStorageKey, nextViewId);
                } else {
                    window.sessionStorage.removeItem(viewStorageKey);
                }
            } catch (error) {
                logViewIdIssue('[view-id] failed to write sessionStorage', error);
            }
        };

        const readStoredViewRestoreToken = () => {
            try {
                return window.sessionStorage.getItem(viewRestoreTokenStorageKey);
            } catch (error) {
                logViewIdIssue('[view-id] failed to read restore token from sessionStorage', error);
                return null;
            }
        };

        const writeStoredViewRestoreToken = (nextToken) => {
            try {
                if (nextToken) {
                    window.sessionStorage.setItem(viewRestoreTokenStorageKey, nextToken);
                } else {
                    window.sessionStorage.removeItem(viewRestoreTokenStorageKey);
                }
            } catch (error) {
                logViewIdIssue('[view-id] failed to write restore token to sessionStorage', error);
            }
        };

        const replaceCurrentUrl = (mutate) => {
            const url = new URL(window.location.href);
            mutate(url);
            const nextUrl = url.pathname + url.search + url.hash;
            const currentUrl = window.location.pathname + window.location.search + window.location.hash;
            if (nextUrl !== currentUrl) {
                window.history.replaceState(window.history.state, '', nextUrl);
            }
        };

        const stripLegacyViewIdFromUrl = () => {
            replaceCurrentUrl((url) => {
                url.searchParams.delete(viewParamName);
            });
        };

        const stripTransientRuntimeParamsFromUrl = () => {
            replaceCurrentUrl((url) => {
                url.searchParams.delete(viewParamName);
                url.searchParams.delete(reloadParamName);
            });
        };

        const clearReloadViewCookie = () => {
            const cookiePath = window.location.pathname || '/';
            const secureFlag = window.location.protocol === 'https:' ? '; Secure' : '';
            document.cookie = `${viewRestoreCookieName}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=${cookiePath}; SameSite=Lax${secureFlag}`;
        };

        const syncReloadViewCookie = () => {
            const activeRestoreToken = window._vlViewRestoreToken || readStoredViewRestoreToken();
            if (!activeRestoreToken) {
                return;
            }
            const cookiePath = window.location.pathname || '/';
            const secureFlag = window.location.protocol === 'https:' ? '; Secure' : '';
            document.cookie = `${viewRestoreCookieName}=${encodeURIComponent(activeRestoreToken)}; path=${cookiePath}; max-age=15; SameSite=Lax${secureFlag}`;
        };

        window._vlViewId = viewId;
        window._vlViewRestoreToken = viewRestoreToken;
        writeStoredViewId(viewId);
        writeStoredViewRestoreToken(viewRestoreToken);
        clearReloadViewCookie();
        if (window.location.search.includes(viewParamName + '=') || window.location.search.includes(reloadParamName + '=')) {
            stripTransientRuntimeParamsFromUrl();
        }
        window.addEventListener('beforeunload', syncReloadViewCookie);
        window.addEventListener('pagehide', syncReloadViewCookie);

        // Honor server-provided debug mode only.
        window._debug_mode = window._debug_mode === true;

        // Sidebar navigation is handled via direct onclick on each wa-button.
        // No delegated listener needed.
        window._vlSidebarResizable = runtimeConfig.sidebarResizable === true;
        window._vlSidebarStorageKey = 'violit:sidebar-width:' + window.location.pathname;
        
        // Debug logging helper
        const debugLog = (...args) => {
            if (window._debug_mode) {
                console.log(...args);
            }
        };

        function getTextLikeHost(root) {
            if (!(root instanceof Element)) return null;
            const tag = root.tagName ? root.tagName.toLowerCase() : '';
            if (tag === 'wa-input' || tag === 'wa-textarea') {
                return root;
            }
            return root.querySelector('wa-input, wa-textarea');
        }

        function syncElementAttributes(target, source) {
            if (!target || !source) return;
            const preserve = new Set(['id', 'data-ws-listener', 'data-vl-echo-guard']);
            const sourceAttrs = new Map(Array.from(source.attributes).map((attr) => [attr.name, attr.value]));

            Array.from(target.attributes).forEach((attr) => {
                if (preserve.has(attr.name)) return;
                if (!sourceAttrs.has(attr.name)) {
                    target.removeAttribute(attr.name);
                }
            });

            sourceAttrs.forEach((value, name) => {
                if (name === 'id') return;
                target.setAttribute(name, value);
            });
        }

        function trySmartUpdateTextLikeWidget(currentRoot, incomingMarkupOrRoot) {
            const currentHost = getTextLikeHost(currentRoot);
            if (!currentHost) return false;

            let nextHost = null;
            if (typeof incomingMarkupOrRoot === 'string') {
                const temp = document.createElement('div');
                temp.innerHTML = incomingMarkupOrRoot;
                nextHost = getTextLikeHost(temp);
            } else {
                nextHost = getTextLikeHost(incomingMarkupOrRoot);
            }

            if (!nextHost) return false;

            const currentTag = currentHost.tagName ? currentHost.tagName.toLowerCase() : '';
            const nextTag = nextHost.tagName ? nextHost.tagName.toLowerCase() : '';
            if (!currentTag || currentTag !== nextTag) return false;

            const currentInner = currentHost.shadowRoot
                ? currentHost.shadowRoot.querySelector('input, textarea')
                : null;
            const shadowActive = currentHost.shadowRoot ? currentHost.shadowRoot.activeElement : null;
            const focusSnapshot = {
                isFocused: document.activeElement === currentHost || !!shadowActive || (document.activeElement && currentHost.contains(document.activeElement)),
                selectionStart: currentInner && typeof currentInner.selectionStart === 'number' ? currentInner.selectionStart : null,
                selectionEnd: currentInner && typeof currentInner.selectionEnd === 'number' ? currentInner.selectionEnd : null,
                selectionDirection: currentInner && typeof currentInner.selectionDirection === 'string' ? currentInner.selectionDirection : 'none',
            };

            syncElementAttributes(currentHost, nextHost);

            const nextValue = nextHost.getAttribute('value') ?? (typeof nextHost.value === 'string' ? nextHost.value : '');
            currentHost.value = nextValue;
            currentHost.setAttribute('value', nextValue);

            const restoreFocus = (attempt = 0) => {
                const liveInner = currentHost.shadowRoot
                    ? currentHost.shadowRoot.querySelector('input, textarea')
                    : null;
                const focusTarget = liveInner || currentHost;

                if (!liveInner && currentTag.startsWith('wa-') && attempt < 8) {
                    setTimeout(() => restoreFocus(attempt + 1), 40);
                    return;
                }

                if (liveInner && typeof liveInner.value === 'string' && liveInner.value !== nextValue) {
                    liveInner.value = nextValue;
                }

                if (focusSnapshot.isFocused && typeof focusTarget.focus === 'function') {
                    focusTarget.focus({ preventScroll: true });
                }

                if (
                    focusSnapshot.isFocused
                    && liveInner
                    && typeof liveInner.setSelectionRange === 'function'
                    && focusSnapshot.selectionStart !== null
                    && focusSnapshot.selectionEnd !== null
                ) {
                    const valueLength = typeof liveInner.value === 'string' ? liveInner.value.length : 0;
                    const start = Math.min(focusSnapshot.selectionStart, valueLength);
                    const end = Math.min(focusSnapshot.selectionEnd, valueLength);
                    liveInner.setSelectionRange(start, end, focusSnapshot.selectionDirection || 'none');
                }
            };

            if (currentHost.hasAttribute('data-vl-part-cls') && currentHost.shadowRoot && window.applyPartStyles) {
                requestAnimationFrame(() => window.applyPartStyles(currentHost));
            }

            if (focusSnapshot.isFocused) {
                requestAnimationFrame(() => restoreFocus());
            } else {
                restoreFocus();
            }

            return true;
        }
        window._vlLastHiddenAt = document.visibilityState === 'hidden' ? Date.now() : 0;
        window._vlResumeCheckTimers = [];
        
        // Attach per-view metadata to HTMX requests in lite mode.
        if (mode === 'lite' && (window._csrf_token || window._vlViewId)) {
            const attachHtmxMetadata = function() {
                if (!document.body || document.body.dataset.vlHtmxMetaBound === 'true') return;
                document.body.dataset.vlHtmxMetaBound = 'true';
                document.body.addEventListener('htmx:configRequest', function(evt) {
                    evt.detail.parameters = evt.detail.parameters || {};
                    evt.detail.headers = evt.detail.headers || {};
                    if (window._csrf_token) {
                        evt.detail.parameters['_csrf_token'] = window._csrf_token;
                    }
                    if (window._vlViewId) {
                        evt.detail.parameters['_vl_view_id'] = window._vlViewId;
                        evt.detail.headers['X-Violit-View'] = window._vlViewId;
                    }
                });
            };
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', attachHtmxMetadata, { once: true });
            } else {
                attachHtmxMetadata();
            }
        }

        function applyLiteStreamPayload(payload) {
            if (!payload) return;

            const temp = document.createElement('div');
            temp.innerHTML = payload;
            const roots = Array.from(temp.children);
            const canAppendLiteRoot = (root) => {
                if (!(root instanceof Element)) return false;
                const rootId = root.id || '';
                if (!rootId) return false;
                if (rootId.includes('dialog')) return true;
                if (rootId === 'toast-injector' || rootId === 'effects-injector') return true;
                return false;
            };

            roots.forEach((incomingRoot) => {
                if (!(incomingRoot instanceof Element)) return;

                incomingRoot.removeAttribute('hx-swap-oob');

                const targetId = incomingRoot.id;
                let updatedRoot = null;

                if (targetId) {
                    const currentRoot = document.getElementById(targetId);
                    if (currentRoot) {
                        let smartUpdated = trySmartUpdateTextLikeWidget(currentRoot, incomingRoot);
                        if (targetId.endsWith('_wrapper') && currentRoot.querySelector('.js-plotly-plot')) {
                            smartUpdated = trySmartUpdatePlotlyWrapper(currentRoot, incomingRoot.outerHTML);
                        }

                        if (!smartUpdated) {
                            const agGridScrollState = window._vlCaptureAgGridScroll
                                ? window._vlCaptureAgGridScroll(currentRoot)
                                : null;
                            purgePlotly(currentRoot);
                            currentRoot.outerHTML = incomingRoot.outerHTML;
                            updatedRoot = document.getElementById(targetId);
                            if (window._vlRestoreAgGridScroll && agGridScrollState) {
                                const revealGrid = window._vlHideAgGridDuringScrollRestore
                                    ? window._vlHideAgGridDuringScrollRestore(updatedRoot, agGridScrollState)
                                    : null;
                                window._vlRestoreAgGridScroll(updatedRoot, agGridScrollState, revealGrid);
                            }
                        } else {
                            updatedRoot = currentRoot;
                        }
                    }
                }

                if (!updatedRoot) {
                    if (!canAppendLiteRoot(incomingRoot)) {
                        return;
                    }
                    document.body.appendChild(incomingRoot);
                    updatedRoot = incomingRoot;
                }

                executeInlineScripts(updatedRoot);
            });

            if (window.htmx && typeof window.htmx.process === 'function') {
                window.htmx.process(document.body);
            }
            if (typeof window._vlApplyPartBridge === 'function') {
                window._vlApplyPartBridge(document);
            }
            if (typeof hljs !== 'undefined') {
                document.querySelectorAll('.violit-code-block pre code:not(.hljs)').forEach(function(block) {
                    hljs.highlightElement(block);
                });
            }
        }

        function connectLiteStream() {
            if (mode !== 'lite' || typeof window.EventSource === 'undefined') return null;

            if (window._vlLiteStream) {
                try {
                    window._vlLiteStream.close();
                } catch (error) {
                    debugLog('[lite-stream] Failed to close previous EventSource', error);
                }
            }

            const streamUrl = new URL('/lite-stream', window.location.origin);
            if (window._vlViewId) {
                streamUrl.searchParams.set('_vl_view_id', window._vlViewId);
            }

            const eventSource = new EventSource(streamUrl.toString(), { withCredentials: true });
            window._vlLiteStream = eventSource;

            eventSource.addEventListener('oob', function(event) {
                if (!event || typeof event.data !== 'string' || !event.data) return;
                try {
                    const payload = JSON.parse(event.data);
                    if (typeof payload === 'string' && payload) {
                        applyLiteStreamPayload(payload);
                    }
                } catch (error) {
                    debugLog('[lite-stream] Failed to process OOB payload', error);
                }
            });

            eventSource.onerror = function(error) {
                debugLog('[lite-stream] EventSource error', error);
            };

            return eventSource;
        }

        window.connectLiteStream = connectLiteStream;
        
        // Helper to clean up Plotly instances before removing elements
        function purgePlotly(container) {
            if (!window.Plotly) return;
            if (container.classList && container.classList.contains('js-plotly-plot')) {
                Plotly.purge(container);
            }
            if (container.querySelectorAll) {
                container.querySelectorAll('.js-plotly-plot').forEach(p => Plotly.purge(p));
            }
        }

        function copyElementAttributes(target, source) {
            if (!target || !source) return;

            Array.from(target.getAttributeNames()).forEach((name) => {
                if (name !== 'id') {
                    target.removeAttribute(name);
                }
            });

            Array.from(source.getAttributeNames()).forEach((name) => {
                if (name !== 'id') {
                    target.setAttribute(name, source.getAttribute(name));
                }
            });
        }

        function executeInlineScripts(root) {
            if (!root || !root.querySelectorAll) return;
            root.querySelectorAll('script').forEach((s) => {
                const script = document.createElement('script');
                script.textContent = s.textContent;
                document.body.appendChild(script);
                script.remove();
            });
        }

        function trySmartUpdatePlotlyWrapper(el, itemHtml) {
            if (!el || !itemHtml) return false;

            const temp = document.createElement('div');
            temp.innerHTML = itemHtml;

            const nextWrapper = temp.firstElementChild;
            const currentPlot = el.querySelector('.js-plotly-plot');
            const nextPlot = temp.querySelector('.js-plotly-plot');

            if (!nextWrapper || !currentPlot || !nextPlot) return false;
            if (currentPlot.parentElement !== el || nextPlot.parentElement !== nextWrapper) return false;
            if (currentPlot.id !== nextPlot.id) return false;
            if (nextPlot.hasAttribute('data-vl-deferred-chart')) return false;

            copyElementAttributes(el, nextWrapper);
            copyElementAttributes(currentPlot, nextPlot);

            Array.from(el.children).forEach((child) => {
                if (child !== currentPlot) {
                    child.remove();
                }
            });

            executeInlineScripts(temp);
            return true;
        }

        function restartPageEnterAnimation(pageEl) {
            if (!pageEl || !pageEl.classList || !pageEl.classList.contains('page-container')) return;
            if (!document.body.classList.contains('anim-soft')) return;
            pageEl.style.animation = 'none';
            pageEl.style.removeProperty('opacity');
            void pageEl.offsetWidth;
            pageEl.style.animation = 'fade-in 0.3s ease-out';
        }

        function resolveCssSizeToPx(value) {
            if (!value) return 0;
            if (typeof value === 'number') return value;
            const probe = document.createElement('div');
            probe.style.position = 'absolute';
            probe.style.visibility = 'hidden';
            probe.style.width = value;
            document.body.appendChild(probe);
            const px = probe.getBoundingClientRect().width;
            probe.remove();
            return px;
        }

        function applySidebarWidth(widthValue, persist = true) {
            const root = document.getElementById('root');
            if (!root) return;
            root.style.setProperty('--vl-sidebar-width', widthValue);
            document.documentElement.style.setProperty('--vl-sidebar-width', widthValue);
            if (persist && window._vlSidebarResizable) {
                try {
                    localStorage.setItem(window._vlSidebarStorageKey, widthValue);
                } catch (err) {
                    debugLog('Failed to persist sidebar width', err);
                }
            }
        }

        function syncSidebarWidthFromStorage() {
            if (!window._vlSidebarResizable) return;
            try {
                const savedWidth = localStorage.getItem(window._vlSidebarStorageKey);
                if (savedWidth) {
                    applySidebarWidth(savedWidth, false);
                }
            } catch (err) {
                debugLog('Failed to restore sidebar width', err);
            }
        }

        function setupSidebarResizer() {
            if (!window._vlSidebarResizable) return;
            const resizer = document.getElementById('sidebar-resizer');
            const sidebar = document.getElementById('sidebar');
            if (!resizer || !sidebar) return;

            let dragState = null;

            const endDrag = () => {
                if (!dragState) return;
                dragState = null;
                document.body.classList.remove('sidebar-resizing');
                window.removeEventListener('pointermove', onDrag);
                window.removeEventListener('pointerup', endDrag);
                window.removeEventListener('pointercancel', endDrag);
            };

            const onDrag = (event) => {
                if (!dragState || window.innerWidth <= 768) return;
                const nextWidth = Math.min(dragState.maxWidth, Math.max(dragState.minWidth, dragState.startWidth + (event.clientX - dragState.startX)));
                applySidebarWidth(`${Math.round(nextWidth)}px`);
            };

            resizer.addEventListener('pointerdown', (event) => {
                if (window.innerWidth <= 768 || sidebar.classList.contains('collapsed')) return;
                const computed = getComputedStyle(document.documentElement);
                const minWidth = resolveCssSizeToPx(computed.getPropertyValue('--sidebar-min-width').trim()) || 220;
                const maxWidth = resolveCssSizeToPx(computed.getPropertyValue('--sidebar-max-width').trim()) || 560;
                dragState = {
                    startX: event.clientX,
                    startWidth: sidebar.getBoundingClientRect().width,
                    minWidth,
                    maxWidth,
                };
                document.body.classList.add('sidebar-resizing');
                resizer.setPointerCapture(event.pointerId);
                window.addEventListener('pointermove', onDrag);
                window.addEventListener('pointerup', endDrag);
                window.addEventListener('pointercancel', endDrag);
                event.preventDefault();
            });
        }

        const VL_PART_BRIDGE_PROPERTIES = [
            'background',
            'background-color',
            'background-image',
            'color',
            'border',
            'border-color',
            'border-width',
            'border-style',
            'border-radius',
            'box-shadow',
            'backdrop-filter',
            'filter',
            'opacity',
            'transform',
            'font-size',
            'font-weight',
            'font-family',
            'font-style',
            'line-height',
            'letter-spacing',
            'text-transform',
            'text-decoration',
            'text-align',
            'padding',
            'padding-top',
            'padding-right',
            'padding-bottom',
            'padding-left',
            'white-space'
        ];

        const VL_PART_BRIDGE_ALIASES = {
            'WA-INPUT': {
                'form-control-input': 'input',
            },
            'WA-SELECT': {
                'form-control-input': 'display-input',
                'input': 'display-input',
            },
            'WA-TEXTAREA': {
                'form-control-input': 'textarea',
            },
        };

        function getPartBridgeRoot() {
            let root = document.getElementById('vl-part-bridge-root');
            if (root) return root;
            root = document.createElement('div');
            root.id = 'vl-part-bridge-root';
            root.setAttribute('aria-hidden', 'true');
            root.style.cssText = 'position:absolute;left:-9999px;top:0;width:0;height:0;overflow:hidden;visibility:hidden;pointer-events:none;';
            document.body.appendChild(root);
            return root;
        }

        function waitForAnimationFrames(count = 2) {
            return new Promise((resolve) => {
                const step = (remaining) => {
                    if (remaining <= 0) {
                        resolve();
                        return;
                    }
                    requestAnimationFrame(() => step(remaining - 1));
                };
                step(count);
            });
        }

        function splitUtilityTokens(className) {
            if (!className) return [];

            const tokens = [];
            let current = '';
            let bracketDepth = 0;
            let parenDepth = 0;
            let quoteChar = null;
            let escapeNext = false;

            for (const char of String(className).trim()) {
                if (escapeNext) {
                    current += char;
                    escapeNext = false;
                    continue;
                }

                if (char === '\\') {
                    current += char;
                    escapeNext = true;
                    continue;
                }

                if (quoteChar) {
                    current += char;
                    if (char === quoteChar) quoteChar = null;
                    continue;
                }

                if (char === '"' || char === "'") {
                    current += char;
                    quoteChar = char;
                    continue;
                }

                if (char === '[') {
                    bracketDepth += 1;
                    current += char;
                    continue;
                }

                if (char === ']') {
                    bracketDepth = Math.max(0, bracketDepth - 1);
                    current += char;
                    continue;
                }

                if (char === '(') {
                    parenDepth += 1;
                    current += char;
                    continue;
                }

                if (char === ')') {
                    parenDepth = Math.max(0, parenDepth - 1);
                    current += char;
                    continue;
                }

                if (/\s/.test(char) && bracketDepth === 0 && parenDepth === 0) {
                    const token = current.trim();
                    if (token) tokens.push(token);
                    current = '';
                    continue;
                }

                current += char;
            }

            const finalToken = current.trim();
            if (finalToken) tokens.push(finalToken);
            return tokens;
        }

        function expandHostStateSelectors(selector, partSelector) {
            const variants = [selector];
            const mappings = [
                {
                    needle: `${partSelector}:hover`,
                    replacements: [`:host(:hover) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:active`,
                    replacements: [`:host(:active) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus-visible`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus-within`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:disabled`,
                    replacements: [`:host([disabled]) ${partSelector}`, `:host(:state(disabled)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:checked`,
                    replacements: [`:host([checked]) ${partSelector}`, `:host(:state(checked)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:indeterminate`,
                    replacements: [`:host([indeterminate]) ${partSelector}`, `:host(:state(indeterminate)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:invalid`,
                    replacements: [`:host(:state(user-invalid)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:valid`,
                    replacements: [`:host(:state(user-valid)) ${partSelector}`],
                },
            ];

            mappings.forEach(({ needle, replacements }) => {
                if (!selector.includes(needle)) return;
                replacements.forEach((replacement) => {
                    variants.push(selector.split(needle).join(replacement));
                });
            });

            if (selector === partSelector || selector.startsWith(`${partSelector}[`) || selector.startsWith(`${partSelector}.`)) {
                variants.push(`:host([checked]) ${partSelector}`);
                variants.push(`:host(:state(checked)) ${partSelector}`);
                variants.push(`:host([disabled]) ${partSelector}`);
                variants.push(`:host(:state(disabled)) ${partSelector}`);
                variants.push(`:host(:focus-within) ${partSelector}`);
                variants.push(`:host(:state(focused)) ${partSelector}`);
            }

            return Array.from(new Set(variants));
        }

        function transformUtilitySelectorForPart(selector, classSelector, partSelector) {
            if (!selector || !selector.includes(classSelector)) return [];
            const rewritten = selector.split(classSelector).join(partSelector).trim();
            if (!rewritten) return [];
            const expanded = expandHostStateSelectors(rewritten, partSelector);
            return Array.from(new Set(expanded.flatMap((item) => {
                const normalized = String(item || '').trim();
                if (!normalized) return [];
                if (normalized.includes(':host')) return [normalized];
                return [normalized, `:host ${normalized}`];
            })));
        }

        function serializeImportantStyleDeclaration(styleDecl) {
            if (!styleDecl) return '';
            return Array.from(styleDecl)
                .map((prop) => {
                    const value = styleDecl.getPropertyValue(prop);
                    if (!value) return '';
                    return `${prop}:${value.trim()} !important;`;
                })
                .filter(Boolean)
                .join('');
        }

        function collectDeclaredProperties(cssText) {
            const props = new Set();
            if (!cssText) return props;
            const matches = String(cssText).matchAll(/([a-zA-Z-]+)\s*:/g);
            for (const match of matches) {
                const prop = match[1] && match[1].trim().toLowerCase();
                if (prop) props.add(prop);
            }
            return props;
        }

        function isPropCoveredByGeneratedCss(prop, declaredProps) {
            const normalized = String(prop || '').trim().toLowerCase();
            if (!normalized) return false;
            if (declaredProps.has(normalized)) return true;

            if (normalized === 'background' || normalized.startsWith('background-')) {
                return declaredProps.has('background') || declaredProps.has('background-color') || declaredProps.has('background-image');
            }

            if (normalized === 'border' || normalized.startsWith('border-')) {
                return declaredProps.has('border')
                    || declaredProps.has('border-color')
                    || declaredProps.has('border-width')
                    || declaredProps.has('border-style')
                    || declaredProps.has('border-radius');
            }

            if (normalized.startsWith('padding-') || normalized === 'padding') {
                return declaredProps.has('padding')
                    || declaredProps.has('padding-top')
                    || declaredProps.has('padding-right')
                    || declaredProps.has('padding-bottom')
                    || declaredProps.has('padding-left');
            }

            if (normalized.startsWith('color')) {
                return declaredProps.has('color');
            }

            return false;
        }

        function serializeUtilityRuleForPart(rule, classSelector, partSelector, parentSelector = '') {
            if (!rule) return '';

            const selectorText = String(rule.selectorText || '').trim();
            const resolvedSelector = selectorText && parentSelector && selectorText.includes('&')
                ? selectorText.split('&').join(parentSelector)
                : selectorText;

            if (rule.type === CSSRule.STYLE_RULE) {
                const selectors = resolvedSelector
                    ? resolvedSelector
                        .split(',')
                        .map((selector) => selector.trim())
                        .flatMap((selector) => transformUtilitySelectorForPart(selector, classSelector, partSelector))
                    : [];

                const declarationText = serializeImportantStyleDeclaration(rule.style);
                const ownRule = selectors.length && declarationText
                    ? `${Array.from(new Set(selectors)).join(',')}{${declarationText}}`
                    : '';
                const nestedRules = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, resolvedSelector))
                    .filter(Boolean)
                    .join('');
                return `${ownRule}${nestedRules}`;
            }

            if (rule.type === CSSRule.MEDIA_RULE) {
                const inner = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .join('');
                return inner ? `@media ${rule.conditionText}{${inner}}` : '';
            }

            if (rule.type === CSSRule.SUPPORTS_RULE) {
                const inner = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .join('');
                return inner ? `@supports ${rule.conditionText}{${inner}}` : '';
            }

            if (rule.type === CSSRule.KEYFRAMES_RULE || rule.type === CSSRule.FONT_FACE_RULE) {
                return rule.cssText;
            }

            if (rule.cssRules?.length) {
                return Array.from(rule.cssRules)
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .filter(Boolean)
                    .join('');
            }

            return '';
        }

        function transformCssTextForPart(cssText, token, partSelector) {
            if (!cssText) return '';

            const root = getPartBridgeRoot();
            const parserStyle = document.createElement('style');
            parserStyle.textContent = cssText;
            root.appendChild(parserStyle);

            try {
                const classSelector = `.${CSS.escape(token)}`;
                return Array.from(parserStyle.sheet?.cssRules || [])
                    .map((rule) => serializeUtilityRuleForPart(rule, classSelector, partSelector))
                    .filter(Boolean)
                    .join('\n');
            } catch (err) {
                debugLog('Failed to transform utility rule for part bridge', err);
                return '';
            } finally {
                parserStyle.remove();
            }
        }

        async function ensureTailwindTokensGenerated(className) {
            const normalized = (className || '').trim();
            if (!normalized) return;

            const root = getPartBridgeRoot();
            const probe = document.createElement('div');
            probe.className = normalized;
            probe.style.cssText = 'display:block;position:absolute;left:-9999px;top:0;visibility:hidden;pointer-events:none;';
            probe.textContent = 'M';
            root.appendChild(probe);
            await waitForAnimationFrames(2);
            probe.remove();
        }

        function getTailwindRuntimeSheets() {
            if (window._vlTailwindRuntimeSheets?.length) {
                return window._vlTailwindRuntimeSheets;
            }

            const sheets = Array.from(document.styleSheets || []).filter((sheet) => {
                const owner = sheet.ownerNode;
                if (!owner || owner.tagName !== 'STYLE') return false;
                const text = owner.textContent || '';
                return text.includes('tailwindcss v4') || text.includes('@layer theme, base, components, utilities');
            });

            window._vlTailwindRuntimeSheets = sheets;
            return sheets;
        }

        function collectGeneratedCssForToken(token, partSelector) {
            const classSelector = `.${CSS.escape(token)}`;
            const cssBlocks = [];

            getTailwindRuntimeSheets().forEach((sheet) => {
                try {
                    Array.from(sheet.cssRules || []).forEach((rule) => {
                        const cssBlock = serializeUtilityRuleForPart(rule, classSelector, partSelector);
                        if (cssBlock) cssBlocks.push(cssBlock);
                    });
                } catch (err) {
                    // Ignore cross-origin or protected stylesheets.
                }
            });

            return cssBlocks.join('\n');
        }

        async function buildTailwindPartCss(className, partSelector) {
            const normalized = (className || '').trim();
            if (!normalized) return '';

            window._vlTailwindPartCssCache = window._vlTailwindPartCssCache || new Map();
            const cacheKey = `${partSelector}::${normalized}`;
            if (window._vlTailwindPartCssCache.has(cacheKey)) {
                return window._vlTailwindPartCssCache.get(cacheKey);
            }

            await ensureTailwindTokensGenerated(normalized);

            const cssBlocks = [];
            for (const token of splitUtilityTokens(normalized)) {
                const cssBlock = collectGeneratedCssForToken(token, partSelector);
                if (cssBlock) cssBlocks.push(cssBlock);
            }

            const finalCss = cssBlocks.join('\n');
            window._vlTailwindPartCssCache.set(cacheKey, finalCss);
            return finalCss;
        }

        async function computeTailwindPartStyles(className) {
            const normalized = (className || '').trim();
            if (!normalized) return {};

            window._vlTailwindPartStyleCache = window._vlTailwindPartStyleCache || new Map();
            if (window._vlTailwindPartStyleCache.has(normalized)) {
                return window._vlTailwindPartStyleCache.get(normalized);
            }

            const root = getPartBridgeRoot();
            const baseline = document.createElement('div');
            const probe = document.createElement('div');
            const baseCss = 'display: block; position: absolute; left: -9999px; top: 0; visibility: hidden; pointer-events: none;';
            baseline.style.cssText = baseCss;
            probe.style.cssText = baseCss;
            baseline.textContent = 'M';
            probe.textContent = 'M';

            await ensureTailwindTokensGenerated(normalized);

            probe.className = normalized;
            root.appendChild(baseline);
            root.appendChild(probe);
            await waitForAnimationFrames(1);

            const baselineStyle = getComputedStyle(baseline);
            const probeStyle = getComputedStyle(probe);
            const styles = {};

            VL_PART_BRIDGE_PROPERTIES.forEach((prop) => {
                const nextValue = probeStyle.getPropertyValue(prop).trim();
                const baseValue = baselineStyle.getPropertyValue(prop).trim();
                if (nextValue && nextValue !== baseValue) {
                    styles[prop] = nextValue;
                }
            });

            baseline.remove();
            probe.remove();
            window._vlTailwindPartStyleCache.set(normalized, styles);
            return styles;
        }

        async function applyTailwindPartStyles(host) {
            if (!host || !host.shadowRoot) return;

            let partMap = null;
            try {
                partMap = JSON.parse(host.getAttribute('data-vl-part-cls') || '{}');
            } catch (err) {
                debugLog('Failed to parse data-vl-part-cls', err);
                return;
            }

            host.shadowRoot.querySelectorAll('[data-vl-part-props]').forEach((partEl) => {
                const previousProps = (partEl.getAttribute('data-vl-part-props') || '')
                    .split('|')
                    .map((item) => item.trim())
                    .filter(Boolean);
                previousProps.forEach((prop) => partEl.style.removeProperty(prop));
                partEl.removeAttribute('data-vl-part-props');
            });

            let combinedCss = '';

            for (const [partName, className] of Object.entries(partMap)) {
                if (!partName || !className) continue;
                const aliasMap = VL_PART_BRIDGE_ALIASES[host.tagName] || {};
                const resolvedPartName = aliasMap[partName] || partName;
                const selector = `[part~="${CSS.escape(resolvedPartName)}"]`;
                const cssText = await buildTailwindPartCss(className, selector);
                const styles = await computeTailwindPartStyles(className);
                const declaredProps = collectDeclaredProperties(cssText);

                if (cssText) {
                    combinedCss += `${cssText}\n`;
                }

                host.shadowRoot.querySelectorAll(selector).forEach((partEl) => {
                    const appliedProps = [];
                    Object.entries(styles).forEach(([prop, value]) => {
                        if (!value) return;
                        if (isPropCoveredByGeneratedCss(prop, declaredProps)) return;
                        partEl.style.setProperty(prop, value, 'important');
                        appliedProps.push(prop);
                    });

                    if (appliedProps.length) {
                        partEl.setAttribute('data-vl-part-props', appliedProps.join('|'));
                    } else {
                        partEl.removeAttribute('data-vl-part-props');
                    }
                });
            }

            let styleEl = host.shadowRoot.querySelector('style[data-vl-part-style="true"]');
            if (combinedCss.trim()) {
                if (!styleEl) {
                    styleEl = document.createElement('style');
                    styleEl.setAttribute('data-vl-part-style', 'true');
                    host.shadowRoot.appendChild(styleEl);
                }
                styleEl.textContent = combinedCss;
            } else if (styleEl) {
                styleEl.remove();
            }
        }

        async function runTailwindPartBridge(scope = document) {
            const hosts = scope && scope.querySelectorAll ? scope.querySelectorAll('[data-vl-part-cls]') : [];
            await Promise.all(Array.from(hosts).map((host) => applyTailwindPartStyles(host)));
        }

        window._vlApplyPartBridge = function(scope = document) {
            const schedule = () => {
                const invoke = () => {
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => runTailwindPartBridge(scope));
                    });
                };

                invoke();
                setTimeout(invoke, 120);
                setTimeout(invoke, 360);
            };

            if (window.__vlTailwindReady) {
                schedule();
                return;
            }

            window.addEventListener('violit:tailwind-ready', schedule, { once: true });
        };

        window.applyPartStyles = applyTailwindPartStyles;

        // [FIX] Plotly Auto-Resize Logic
        // Handles resizing when:
        // 1. Window resizes
        // 2. Tab switches (visibility changes)
        // 3. Container size changes (sidebar toggle, etc)
        function setupPlotlyResizer() {
            if (!window.Plotly || window._vlPlotlyResizerBound) return;
            window._vlPlotlyResizerBound = true;

            const resizeTimers = new WeakMap();
            const sizeCache = new WeakMap();

            const requestPlotResize = (el, force = false, delay = 80) => {
                if (!el) return;
                const pending = resizeTimers.get(el);
                if (pending) {
                    clearTimeout(pending);
                }

                const timer = setTimeout(() => {
                    resizeTimers.delete(el);
                    if (el.offsetParent === null) return;

                    if (typeof window._vlPlotlyRequestResize === 'function' && el.id) {
                        window._vlPlotlyRequestResize(el.id, force);
                        return;
                    }

                    if (window.Plotly && el.querySelector('.plot-container')) {
                        Plotly.Plots.resize(el);
                    }
                }, delay);

                resizeTimers.set(el, timer);
            };

            // 1. Resize on window resize (with debounce for performance)
            let resizeTimer;
            window.addEventListener('resize', () => {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(() => {
                    document.querySelectorAll('.js-plotly-plot').forEach(el => {
                        if (el.offsetParent !== null) {
                            requestPlotResize(el, true, 60);
                        }
                    });
                }, 150);
            });

            // 2. Resize on Tab Switch
            // Charts in previously hidden tabs are handled by IntersectionObserver
            // in the chart render script. This handler covers charts that were
            // already rendered but may need resizing after a tab switch.
            document.addEventListener('wa-tab-show', (event) => {
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        document.querySelectorAll('.js-plotly-plot').forEach(el => {
                            if (el.offsetParent !== null) {
                                requestPlotResize(el, true, 40);
                            }
                        });
                    });
                });
            });
            
            // 3. ResizeObserver for container changes
            const ro = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const el = entry.target;
                    if (!el.classList.contains('js-plotly-plot') || el.offsetParent === null) {
                        continue;
                    }

                    const nextSize = {
                        width: Math.round(entry.contentRect.width || 0),
                        height: Math.round(entry.contentRect.height || 0),
                    };
                    if (nextSize.width < 10) {
                        continue;
                    }

                    const prevSize = sizeCache.get(el);
                    sizeCache.set(el, nextSize);
                    if (prevSize && Math.abs(prevSize.width - nextSize.width) < 2 && Math.abs(prevSize.height - nextSize.height) < 2) {
                        continue;
                    }

                    requestPlotResize(el, true, 60);
                }
            });

            // Observe existing plots
            document.querySelectorAll('.js-plotly-plot').forEach(el => ro.observe(el));

            // Observe new plots added dynamically
            const mo = new MutationObserver(mutations => {
                for (let mutation of mutations) {
                    for (let node of mutation.addedNodes) {
                        if (node.nodeType === 1) {
                            if (node.classList.contains('js-plotly-plot')) {
                                ro.observe(node);
                            }
                            node.querySelectorAll('.js-plotly-plot').forEach(el => ro.observe(el));
                        }
                    }
                }
            });
            mo.observe(document.body, { childList: true, subtree: true });
        }

        // Initialize Resizer
        document.addEventListener('DOMContentLoaded', function() {
            syncSidebarWidthFromStorage();
            setupSidebarResizer();
            window._vlLoadLib('Plotly', setupPlotlyResizer);
            window._vlApplyPartBridge(document);
        });

        if (mode === 'ws') {
            // Interval infrastructure
            window._vlIntervals = window._vlIntervals || {};

            window._vlCreateInterval = function(id, ms, autostart) {
                if (window._vlIntervals[id]) return; // prevent duplicates

                var ctrl = {
                    _timer:   null,
                    _paused:  !autostart,
                    _stopped: false,
                    _ms:      ms,
                    _id:      id,

                    _tick: function() {
                        if (window._ws && window._ws.readyState === 1) {
                            window._ws.send(JSON.stringify({ type: 'tick', id: id }));
                        }
                    },

                    start: function() {
                        if (!ctrl._paused && !ctrl._stopped && !ctrl._timer) {
                            ctrl._timer = setInterval(ctrl._tick, ctrl._ms);
                        }
                    },

                    pause: function() {
                        ctrl._paused = true;
                        if (ctrl._timer) { clearInterval(ctrl._timer); ctrl._timer = null; }
                    },

                    resume: function() {
                        ctrl._paused = false;
                        ctrl._stopped = false;
                        ctrl.start();
                    },

                    stop: function() {
                        ctrl._stopped = true;
                        if (ctrl._timer) { clearInterval(ctrl._timer); ctrl._timer = null; }
                        delete window._vlIntervals[id];
                    }
                };

                window._vlIntervals[id] = ctrl;

                // Wait for WebSocket to be ready, then start
                if (autostart) {
                    function waitAndStart() {
                        if (window._ws && window._ws.readyState === 1) {
                            ctrl.start();
                        } else {
                            setTimeout(waitAndStart, 200);
                        }
                    }
                    waitAndStart();
                }
            };
            // End interval infrastructure

            window._wsReady = false;
            window._actionQueue = [];
            window._ws = null;
            window._vlWsHelloReceived = false;
            window._vlReloadScheduled = false;
            window._vlRecoveryLoopActive = false;
            window._vlHeartbeatReplyTimer = null;
            window._vlHeartbeatProbeQueuedActions = false;
            window._vlLastSocketAckAt = Date.now();
            window._vlHasEverBeenReady = false;
            window._vlVisibleStaleSince = 0;
            window._vlLastInteractionRecoveryAt = 0;
            
            // Page scroll position memory: { pageKey: scrollY }
            window._pageScrollPositions = {};
            window._currentPageKey = null;
            window._pendingPageKey = null;
            window._pendingScrollRestore = null;
            window._suppressHashRestoreOnce = false;

            window._vlFindAgGridViewport = (root) => {
                const scope = root && typeof root.querySelectorAll === 'function' ? root : document;
                const candidates = Array.from(scope.querySelectorAll('.ag-center-cols-viewport, .ag-body-viewport'));
                if (!candidates.length) {
                    return null;
                }
                return candidates.find((candidate) => {
                    return candidate.scrollTop > 0 || candidate.scrollLeft > 0 || candidate.scrollHeight > candidate.clientHeight || candidate.scrollWidth > candidate.clientWidth;
                }) || candidates[0];
            };

            window._vlCaptureAgGridScroll = (root) => {
                const viewport = window._vlFindAgGridViewport(root);
                if (!viewport) {
                    return null;
                }
                return {
                    top: viewport.scrollTop || 0,
                    left: viewport.scrollLeft || 0
                };
            };

            window._vlHideAgGridDuringScrollRestore = (root, state) => {
                if (!root || !state || ((state.top || 0) === 0 && (state.left || 0) === 0)) {
                    return () => {};
                }

                const previousVisibility = root.style.visibility;
                root.style.visibility = 'hidden';

                return () => {
                    root.style.visibility = previousVisibility;
                };
            };

            window._vlRestoreAgGridScroll = (root, state, onDone) => {
                if (!state) {
                    if (typeof onDone === 'function') {
                        onDone();
                    }
                    return;
                }

                let attempts = 0;
                const maxAttempts = 12;
                let finished = false;

                const finish = () => {
                    if (finished) {
                        return;
                    }
                    finished = true;
                    if (typeof onDone === 'function') {
                        onDone();
                    }
                };

                const restore = () => {
                    const viewport = window._vlFindAgGridViewport(root);
                    if (!viewport) {
                        if (attempts < maxAttempts) {
                            attempts += 1;
                            requestAnimationFrame(restore);
                        } else {
                            finish();
                        }
                        return;
                    }

                    viewport.scrollTop = state.top || 0;
                    viewport.scrollLeft = state.left || 0;

                    if (attempts < 2) {
                        attempts += 1;
                        requestAnimationFrame(restore);
                        return;
                    }

                    setTimeout(() => {
                        const finalViewport = window._vlFindAgGridViewport(root);
                        if (finalViewport) {
                            finalViewport.scrollTop = state.top || 0;
                            finalViewport.scrollLeft = state.left || 0;
                        }
                        finish();
                    }, 80);
                };

                restore();
            };

            window._vlSocketAckAgeMs = () => {
                const lastAckAt = window._vlLastSocketAckAt || 0;
                if (lastAckAt <= 0) {
                    return Number.POSITIVE_INFINITY;
                }
                return Date.now() - lastAckAt;
            };

            window._vlFlushActionQueue = (reason = 'flush') => {
                if (!window._wsReady || !window._ws || window._ws.readyState !== WebSocket.OPEN || window._actionQueue.length === 0) {
                    return false;
                }

                debugLog(`[WebSocket] Flushing ${window._actionQueue.length} queued action(s) after ${reason}.`);
                const queuedPayloads = window._actionQueue.splice(0, window._actionQueue.length);
                queuedPayloads.forEach((queuedPayload) => {
                    window._ws.send(JSON.stringify(queuedPayload));
                });
                return true;
            };
            
            // Define sendAction IMMEDIATELY (before WebSocket connection)
            window._vlAllowFocusedUpdates = window._vlAllowFocusedUpdates || {};
            window._vlAllowNextFocusedUpdate = (cid) => {
                if (!cid) return;
                window._vlAllowFocusedUpdates[cid] = true;
            };

            window.sendAction = (cid, val) => {
                debugLog(`[sendAction] Called with cid=${cid}, val=${val}`);

                if (val && typeof val === 'object' && val.eventType === 'submit') {
                    window._vlAllowNextFocusedUpdate(cid);
                }

                if (cid.startsWith('nav_menu')) {
                    if (window._pendingPageKey === val || window._currentPageKey === val) {
                        debugLog(`[sendAction] Skipping duplicate navigation for ${val}`);
                        return;
                    }
                }

                window._pendingScrollRestore = {
                    x: window.scrollX || 0,
                    y: window.scrollY || window.pageYOffset || 0
                };
                
                const payload = {
                    type: 'click',
                    id: cid,
                    value: val
                };
                
                if (window._csrf_token) {
                    payload._csrf_token = window._csrf_token;
                }
                if (window._vlViewId) {
                    payload._vl_view_id = window._vlViewId;
                }
                
                const urlParams = new URLSearchParams(window.location.search);
                const nativeToken = urlParams.get('_native_token');
                if (nativeToken) {
                    payload._native_token = nativeToken;
                }
                
                if (cid.startsWith('nav_menu')) {
                    if (window._currentPageKey) {
                        window._pageScrollPositions[window._currentPageKey] = window.scrollY;
                        debugLog(`Saved scroll ${window.scrollY}px for page: ${window._currentPageKey}`);
                    }
                    window._pendingPageKey = val;
                    const pageName = val.replace('page_', '');
                    window._suppressHashRestoreOnce = true;
                    window.location.hash = pageName;
                    debugLog(`Updated hash: #${pageName}`);
                }
                
                const socketOpen = !!(window._ws && window._ws.readyState === WebSocket.OPEN);
                if (!window._wsReady || !socketOpen) {
                    debugLog(`WebSocket not ready, queueing action: ${cid}`);
                    window._actionQueue.push(payload);
                    if (!socketOpen && (!window._ws || window._ws.readyState !== WebSocket.CONNECTING)) {
                        window._vlScheduleWsRecovery(`action:${cid}`);
                    }
                } else {
                    const ackAgeMs = window._vlSocketAckAgeMs();
                    if (window._vlTimeout <= 0 && ackAgeMs > 45000) {
                        debugLog(`[sendAction] WebSocket looks stale before ${cid} (${ackAgeMs}ms since last ack); queueing action and probing transport.`);
                        window._actionQueue.push(payload);
                        window._vlHeartbeatProbeQueuedActions = true;
                        window._vlSendHeartbeat('action-stale-probe');
                        return;
                    }

                    debugLog(`Sending action to server: ${cid}`);
                    try {
                        window._ws.send(JSON.stringify(payload));
                    } catch (error) {
                        debugLog(`[sendAction] WebSocket send failed for ${cid}`, error);
                        window._actionQueue.push(payload);
                        window._vlScheduleWsRecovery(`send-failed:${cid}`);
                    }
                }
            };

            window._vlBuildHardReloadUrl = () => {
                const url = new URL(window.location.href);
                url.searchParams.set(reloadParamName, Date.now().toString());
                return url.toString();
            };

            window._vlHardReload = () => {
                if (window._vlReloadScheduled) {
                    return;
                }
                window._vlReloadScheduled = true;
                window.location.replace(window._vlBuildHardReloadUrl());
            };

            window._vlMarkSocketAck = () => {
                window._vlLastSocketAckAt = Date.now();
                window._vlVisibleStaleSince = 0;
                if (window._vlHeartbeatReplyTimer) {
                    clearTimeout(window._vlHeartbeatReplyTimer);
                    window._vlHeartbeatReplyTimer = null;
                }

                if (window._vlHeartbeatProbeQueuedActions) {
                    window._vlHeartbeatProbeQueuedActions = false;
                    try {
                        window._vlFlushActionQueue('heartbeat-ack');
                    } catch (error) {
                        debugLog('[WebSocket] Failed to flush queued actions after heartbeat ack.', error);
                        window._vlScheduleWsRecovery('heartbeat-ack-flush-failed');
                    }
                }
            };

            window._vlScheduleWsRecovery = (reason) => {
                if (mode !== 'ws' || window._intentionalDisconnect || window._vlRecoveryLoopActive) {
                    return;
                }

                window._wsReady = false;
                window._vlWsHelloReceived = false;
                window._vlRecoveryLoopActive = true;
                debugLog(`[WebSocket] Recovery scheduled (${reason}).`);

                let retryDelay = 50;
                const maxDelay = 2000;

                const checkServer = () => {
                    if (window._intentionalDisconnect) {
                        window._vlRecoveryLoopActive = false;
                        return;
                    }

                    const probeUrl = new URL('/__violit_boot', window.location.origin);
                    probeUrl.searchParams.set('_t', Date.now().toString());

                    fetch(probeUrl.toString(), { cache: 'no-store' })
                        .then(async (response) => {
                            if (response.ok) {
                                let nextBootId = null;
                                try {
                                    const payload = await response.json();
                                    nextBootId = typeof payload.bootId === 'string' ? payload.bootId : null;
                                } catch (error) {
                                    debugLog('[WebSocket] Failed to parse boot probe response.', error);
                                }

                                window._vlRecoveryLoopActive = false;
                                if (window._vlBootId && nextBootId && window._vlBootId !== nextBootId) {
                                    debugLog(`[WebSocket] Server boot changed during recovery (${window._vlBootId} != ${nextBootId}). Reloading...`);
                                    window._vlHardReload();
                                    return;
                                }

                                debugLog('[WebSocket] Server reachable during recovery. Reconnecting socket...');
                                window._vlReconnectWebSocket(reason);
                            } else {
                                retryDelay = Math.min(retryDelay * 1.5, maxDelay);
                                setTimeout(checkServer, retryDelay);
                            }
                        })
                        .catch(() => {
                            retryDelay = Math.min(retryDelay * 1.5, maxDelay);
                            setTimeout(checkServer, retryDelay);
                        });
                };

                setTimeout(checkServer, retryDelay);
            };

            window._vlSendHeartbeat = (reason = 'heartbeat') => {
                if (!window._ws || window._ws.readyState !== WebSocket.OPEN) {
                    if (!window._intentionalDisconnect && (!window._ws || window._ws.readyState !== WebSocket.CONNECTING)) {
                        window._vlScheduleWsRecovery(`${reason}:socket-unavailable`);
                    }
                    return false;
                }

                try {
                    window._ws.send(JSON.stringify({ type: 'ping' }));
                    const expectsHeartbeatAck = window._vlTimeout > 0 || reason === 'resume' || reason === 'action-stale-probe';
                    if (expectsHeartbeatAck) {
                        if (window._vlHeartbeatReplyTimer) {
                            clearTimeout(window._vlHeartbeatReplyTimer);
                        }
                        const heartbeatTimeoutMs = reason === 'action-stale-probe' ? 5000 : 10000;
                        window._vlHeartbeatReplyTimer = setTimeout(() => {
                            if (!window._intentionalDisconnect) {
                                if (window._vlTimeout <= 0 && document.visibilityState === 'hidden' && reason !== 'action-stale-probe') {
                                    debugLog(`[WebSocket] Heartbeat timeout deferred while page is hidden (${reason}).`);
                                    return;
                                }
                                debugLog(`[WebSocket] Heartbeat timed out (${reason}).`);
                                window._vlScheduleWsRecovery(`${reason}:heartbeat-timeout`);
                            }
                        }, heartbeatTimeoutMs);
                    }
                    return true;
                } catch (error) {
                    debugLog(`[WebSocket] Heartbeat send failed (${reason}).`, error);
                    window._vlScheduleWsRecovery(`${reason}:heartbeat-send-failed`);
                    return false;
                }
            };

            window._vlProbeWsAfterResume = () => {
                if (mode !== 'ws' || window._intentionalDisconnect) {
                    return;
                }

                const socketOpen = !!(window._ws && window._ws.readyState === WebSocket.OPEN);
                if (!socketOpen || !window._wsReady) {
                    if (!window._ws || window._ws.readyState !== WebSocket.CONNECTING) {
                        window._vlScheduleWsRecovery('resume');
                    }
                    return;
                }

                const ackAgeMs = Date.now() - (window._vlLastSocketAckAt || 0);
                if (ackAgeMs > 30000) {
                    window._vlSendHeartbeat('resume');
                }
            };

            window._vlClearResumeCheckTimers = () => {
                if (!Array.isArray(window._vlResumeCheckTimers) || window._vlResumeCheckTimers.length === 0) {
                    return;
                }
                window._vlResumeCheckTimers.forEach((timerId) => clearTimeout(timerId));
                window._vlResumeCheckTimers = [];
            };

            window._vlScheduleResumeChecks = (reason = 'resume') => {
                window._vlClearResumeCheckTimers();

                [1000, 4000].forEach((delayMs) => {
                    const timerId = setTimeout(() => {
                        if (document.visibilityState !== 'visible' || window._intentionalDisconnect) {
                            return;
                        }

                        const socketOpen = !!(window._ws && window._ws.readyState === WebSocket.OPEN);
                        const ackAgeMs = window._vlSocketAckAgeMs();
                        if (!socketOpen || !window._wsReady || ackAgeMs > 45000) {
                            debugLog(`[WebSocket] Running follow-up resume probe (${reason}, ${delayMs}ms).`);
                            window._vlProbeWsAfterResume();
                        }
                    }, delayMs);
                    window._vlResumeCheckTimers.push(timerId);
                });
            };

            window._vlHandleResume = (reason = 'resume') => {
                if (mode !== 'ws' || window._intentionalDisconnect) {
                    return;
                }

                const hiddenDurationMs = window._vlLastHiddenAt > 0 ? Date.now() - window._vlLastHiddenAt : 0;
                window._vlLastHiddenAt = 0;

                const socketOpen = !!(window._ws && window._ws.readyState === WebSocket.OPEN);
                const socketConnecting = !!(window._ws && window._ws.readyState === WebSocket.CONNECTING);
                const ackAgeMs = window._vlSocketAckAgeMs();

                if (hiddenDurationMs > 60000 && !socketConnecting && (!window._wsReady || ackAgeMs > 45000)) {
                    debugLog(`[WebSocket] Page resumed after ${hiddenDurationMs}ms hidden; forcing soft reconnect (${reason}).`);
                    window._vlReconnectWebSocket(`${reason}:long-hidden`);
                    window._vlScheduleResumeChecks(`${reason}:post-reconnect`);
                    return;
                }

                if (socketOpen && window._wsReady) {
                    // Even after a shorter hidden interval, mobile browsers can keep the
                    // WebSocket looking OPEN while having already dropped the transport.
                    // Always verify liveness on resume instead of relying on the long-hidden threshold.
                    window._vlSendHeartbeat('resume');
                } else {
                    window._vlProbeWsAfterResume();
                }
                window._vlScheduleResumeChecks(reason);
            };

            window._vlEnsureLivePage = (reason = 'watchdog') => {
                if (mode !== 'ws' || window._intentionalDisconnect || !window._vlHasEverBeenReady) {
                    return;
                }

                if (document.visibilityState !== 'visible') {
                    window._vlVisibleStaleSince = 0;
                    return;
                }

                const socket = window._ws;
                const socketState = socket ? socket.readyState : WebSocket.CLOSED;
                const socketOpen = socketState === WebSocket.OPEN;
                const ackAgeMs = window._vlSocketAckAgeMs();
                const transportStale = !socketOpen || !window._wsReady || ackAgeMs > 45000;

                if (!transportStale) {
                    window._vlVisibleStaleSince = 0;
                    return;
                }

                if (window._vlVisibleStaleSince <= 0) {
                    window._vlVisibleStaleSince = Date.now();
                }

                if (!socketOpen || !window._wsReady) {
                    if (!socket || socket.readyState !== WebSocket.CONNECTING) {
                        window._vlScheduleWsRecovery(`${reason}:not-ready`);
                    }
                } else if (!window._vlHeartbeatReplyTimer) {
                    window._vlSendHeartbeat(reason);
                }

                const staleVisibleMs = Date.now() - window._vlVisibleStaleSince;
                if (staleVisibleMs > 20000 && navigator.onLine !== false) {
                    debugLog(`[WebSocket] Visible page stayed stale for ${staleVisibleMs}ms (${reason}). Hard reloading...`);
                    window._vlHardReload();
                }
            };

            window._vlRevivePageOnInteraction = (reason = 'interaction') => {
                if (mode !== 'ws' || window._intentionalDisconnect || !window._vlHasEverBeenReady) {
                    return;
                }

                if (document.visibilityState !== 'visible') {
                    return;
                }

                const socketOpen = !!(window._ws && window._ws.readyState === WebSocket.OPEN);
                const ackAgeMs = window._vlSocketAckAgeMs();
                if (socketOpen && window._wsReady && ackAgeMs <= 10000) {
                    return;
                }

                const now = Date.now();
                if (now - window._vlLastInteractionRecoveryAt < 1000) {
                    return;
                }

                window._vlLastInteractionRecoveryAt = now;
                window._vlEnsureLivePage(reason);
            };

            window._vlFinalizeWsReady = () => {
                if (window._wsReady) {
                    return;
                }

                window._wsReady = true;
                window._vlHasEverBeenReady = true;
                window._vlVisibleStaleSince = 0;

                window._vlFlushActionQueue('ws-ready');

                setTimeout(restoreFromHash, 100);
            };

            window._vlBuildWsUrl = () => {
                const wsUrl = new URL((location.protocol === 'https:' ? 'wss:' : 'ws:') + "//" + location.host + "/ws");
                if (window._vlViewId) {
                    wsUrl.searchParams.set('_vl_view_id', window._vlViewId);
                }
                return wsUrl;
            };

            window._vlDisposeSocket = (socket) => {
                if (!socket) {
                    return;
                }

                socket.onclose = null;
                socket.onopen = null;
                socket.onerror = null;
                socket.onmessage = null;

                if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
                    try {
                        socket.close();
                    } catch (error) {
                        debugLog('[WebSocket] Failed to close previous socket.', error);
                    }
                }
            };

            window._vlAttachWebSocketHandlers = (socket) => {
                socket.onclose = () => {
                    if (window._ws !== socket) {
                        return;
                    }
                    if (window._vlHeartbeatReplyTimer) {
                        clearTimeout(window._vlHeartbeatReplyTimer);
                        window._vlHeartbeatReplyTimer = null;
                    }
                    if (window._intentionalDisconnect) return;
                    window._vlScheduleWsRecovery('close');
                };

                socket.onopen = () => {
                    if (window._ws !== socket) {
                        return;
                    }
                    debugLog('[WebSocket] Connected successfully');
                    window._vlReloadScheduled = false;
                    window._vlRecoveryLoopActive = false;
                };

                socket.onerror = (error) => {
                    if (window._ws !== socket) {
                        return;
                    }
                    window._wsReady = false;
                    debugLog('[WebSocket] Error:', error);
                };

                socket.onmessage = (e) => {
                    if (window._ws !== socket) {
                        return;
                    }
                    debugLog('[WebSocket] Message received');
                    const msg = JSON.parse(e.data);
                    window._vlMarkSocketAck();
                    if (msg.type === 'hello') {
                        window._vlServerBootId = msg.bootId || null;

                        if (msg.hasOwnProperty('viewAlive') && msg.viewAlive === false) {
                            debugLog(`[WebSocket] Server forgot our session/view (TTL expired). Hard reloading into new session...`);
                            window._vlHardReload();
                            return;
                        }

                        if (typeof msg.viewId === 'string' && msg.viewId) {
                            window._vlViewId = msg.viewId;
                            writeStoredViewId(msg.viewId);
                        }

                        if (window._vlBootId && msg.bootId && window._vlBootId !== msg.bootId) {
                            debugLog(`[WebSocket] Boot mismatch detected (${window._vlBootId} != ${msg.bootId}). Hard reloading...`);
                            window._vlHardReload();
                            return;
                        }

                        window._vlWsHelloReceived = true;
                        window._vlFinalizeWsReady();
                        return;
                    }
                    if (msg.type === 'pong') {
                        return;
                    }
                    if(msg.type === 'update') {
                        // Check if this is a navigation update (page transition)
                        // Server sends isNavigation flag based on action type
                        const isNavigation = msg.isNavigation === true;
                    
                        const applyUpdates = (payload) => {
                            payload.forEach(item => {
                                const el = document.getElementById(item.id);
                                const allowFocusedUpdate = !!(window._vlAllowFocusedUpdates && window._vlAllowFocusedUpdates[item.id]);
                            
                                // Focus Guard: Skip update if element is focused input to prevent interrupting typing
                                // BUT allow page navigation updates to proceed.
                                if (!isNavigation && !allowFocusedUpdate && el && document.activeElement && el.contains(document.activeElement)) {
                                     const tag = document.activeElement.tagName.toLowerCase();
                                     const isInput = tag === 'input' || tag === 'textarea' || tag.startsWith('wa-input') || tag.startsWith('wa-textarea') || tag.startsWith('wa-slider');
                                     
                                     // If it's an input, block update. If it's a button (nav menu), ALLOW update.
                                     if (isInput) {
                                         return;
                                     }
                                }

                                if (allowFocusedUpdate && window._vlAllowFocusedUpdates) {
                                    delete window._vlAllowFocusedUpdates[item.id];
                                }

                                if(el) {
                                    // Smart update for specific widget types to preserve animations/instances
                                    const widgetType = item.id.split('_')[0];
                                    let smartUpdated = false;
                                    
                                    // Checkbox/Toggle: Update checked property only (preserve animation)
                                    if (widgetType === 'checkbox' || widgetType === 'toggle') {
                                        // Parse new HTML to extract checked state
                                        const temp = document.createElement('div');
                                        temp.innerHTML = item.html;
                                        const newCheckbox = temp.querySelector('wa-checkbox, wa-switch');
                                        
                                        if (newCheckbox) {
                                            // Find the actual checkbox element (may be direct or nested)
                                            const checkboxEl = el.tagName && (el.tagName.toLowerCase() === 'wa-checkbox' || el.tagName.toLowerCase() === 'wa-switch')
                                                ? el 
                                                : el.querySelector('wa-checkbox, wa-switch');
                                            
                                            if (checkboxEl) {
                                                const shouldBeChecked = newCheckbox.hasAttribute('checked');
                                                // Only update if different to avoid interrupting user interaction
                                                if (checkboxEl.checked !== shouldBeChecked) {
                                                    checkboxEl.checked = shouldBeChecked;
                                                }
                                                smartUpdated = true;
                                            }
                                        }
                                    }

                                    if (!smartUpdated && (widgetType === 'input' || widgetType === 'textarea')) {
                                        smartUpdated = trySmartUpdateTextLikeWidget(el, item.html);
                                    }
                                    
                                    // Slider: Update value property only (preserve drag interaction)
                                    if (widgetType === 'slider') {
                                        const temp = document.createElement('div');
                                        temp.innerHTML = item.html;
                                        const newRange = temp.querySelector('wa-slider');
                                        if (newRange) {
                                            const rangeEl = el.tagName && el.tagName.toLowerCase() === 'wa-slider'
                                                ? el : el.querySelector('wa-slider');
                                            if (rangeEl) {
                                                const newVal = newRange.getAttribute('value');
                                                if (newVal !== null && rangeEl.value !== parseFloat(newVal)) {
                                                    rangeEl.value = parseFloat(newVal);
                                                }
                                                smartUpdated = true;
                                            }
                                        }
                                    }
                                    
                                    // AG Grid-backed widgets: update rowData without replacing the whole DOM.
                                    // This avoids the destroy/recreate flash that happens when dataframe widgets
                                    // are rerendered reactively after a click.
                                    if (widgetType === 'df' || (widgetType === 'data' && item.id.includes('editor'))) {
                                        const baseCid = item.id.replace('_wrapper', '');
                                        const gridApi = window['gridApi_' + baseCid];
                                        if (gridApi) {
                                            const match = item.html.match(/rowData:\s*(\[.*?\])/s);
                                            if (match) {
                                                try {
                                                    const newData = JSON.parse(match[1]);
                                                    const gridRoot = document.getElementById(baseCid) || el.querySelector(`#${baseCid}`) || el;
                                                    const agGridScrollState = window._vlCaptureAgGridScroll(gridRoot);

                                                    if (typeof gridApi.setGridOption === 'function') {
                                                        gridApi.setGridOption('rowData', newData);
                                                    } else if (typeof gridApi.setRowData === 'function') {
                                                        gridApi.setRowData(newData);
                                                    }

                                                    window._vlRestoreAgGridScroll(gridRoot, agGridScrollState);
                                                    smartUpdated = true;
                                                } catch (e) {
                                                    console.error('Failed to parse AG Grid data:', e);
                                                }
                                            }
                                        }
                                    }

                                    // Tabs: when only the active panel changed, preserve the existing DOM
                                    // so nested chart/widget instances don't get torn down and redrawn.
                                    if (!smartUpdated && widgetType === 'tabs') {
                                        const temp = document.createElement('div');
                                        temp.innerHTML = item.html;
                                        const nextGroup = temp.querySelector('wa-tab-group');
                                        const currentGroup = el.tagName && el.tagName.toLowerCase() === 'wa-tab-group'
                                            ? el
                                            : el.querySelector('wa-tab-group');

                                        if (currentGroup && nextGroup) {
                                            const currentPanels = Array.from(currentGroup.querySelectorAll(':scope > wa-tab-panel'));
                                            const nextPanels = Array.from(nextGroup.querySelectorAll(':scope > wa-tab-panel'));
                                            const currentTabs = Array.from(currentGroup.querySelectorAll(':scope > wa-tab[slot="nav"]'));
                                            const nextTabs = Array.from(nextGroup.querySelectorAll(':scope > wa-tab[slot="nav"]'));

                                            const samePanelMarkup = currentPanels.length === nextPanels.length && currentPanels.every((panel, index) => {
                                                const nextPanel = nextPanels[index];
                                                return !!nextPanel && panel.getAttribute('name') === nextPanel.getAttribute('name') && panel.innerHTML === nextPanel.innerHTML;
                                            });

                                            const sameTabMarkup = currentTabs.length === nextTabs.length && currentTabs.every((tab, index) => {
                                                const nextTab = nextTabs[index];
                                                return !!nextTab && tab.getAttribute('panel') === nextTab.getAttribute('panel') && tab.textContent === nextTab.textContent;
                                            });

                                            if (samePanelMarkup && sameTabMarkup) {
                                                const nextActive = nextGroup.getAttribute('active');
                                                if (nextActive) {
                                                    currentGroup.setAttribute('active', nextActive);
                                                    requestAnimationFrame(() => {
                                                        currentGroup.setAttribute('active', nextActive);
                                                        if (typeof currentGroup.updateActiveTab === 'function') {
                                                            currentGroup.updateActiveTab();
                                                        }
                                                    });
                                                }
                                                smartUpdated = true;
                                            }
                                        }
                                    }

                                    // Plotly chart wrappers: keep the existing plot DOM and rerun the incoming
                                    // render script so Plotly.react updates traces without nuking the background.
                                    if (!smartUpdated && item.id.endsWith('_wrapper') && el.querySelector('.js-plotly-plot')) {
                                        smartUpdated = trySmartUpdatePlotlyWrapper(el, item.html);
                                    }
                                    
                                    // Default: Full DOM replacement
                                    if (!smartUpdated) {
                                        const agGridScrollState = window._vlCaptureAgGridScroll(el);
                                        purgePlotly(el);
                                        el.outerHTML = item.html;
                                        
                                        const newEl = document.getElementById(item.id);
                                        const revealGrid = window._vlHideAgGridDuringScrollRestore(newEl, agGridScrollState);
                                        window._vlRestoreAgGridScroll(newEl, agGridScrollState, revealGrid);
                                        
                                        // Execute scripts
                                        const temp = document.createElement('div');
                                        temp.innerHTML = item.html;
                                        executeInlineScripts(temp);

                                        if (isNavigation && newEl && newEl.classList.contains('page-container')) {
                                            requestAnimationFrame(() => restartPageEnterAnimation(newEl));
                                        }
                                    }
                                } else {
                                    // If the element does not exist, it might be a new element that belongs inside a re-rendered parent container.
                                    // It will automatically be created when its parent container replaces its innerHTML.
                                    // But if we are in Lite mode or handled via generic layout, we might need to append it if it's top-level or absolute (like dialogs)
                                    if (item.id.includes('dialog')) {
                                        debugLog("[WebSocket] Element not found for dialog, appending to body: " + item.id);
                                        const container = document.createElement('div');
                                        container.id = item.id;
                                        container.innerHTML = item.html;
                                        document.body.appendChild(container);

                                        // Trigger scripts for the newly appended dialog
                                        container.querySelectorAll('script').forEach(s => {
                                            const script = document.createElement('script');
                                            script.textContent = s.textContent;
                                            document.body.appendChild(script);
                                            script.remove();
                                        });
                                    } else {
                                        debugLog("[WebSocket] Element not found for update, skipping appending to end: " + item.id);
                                    }
                                }
                            });
                        };
                        
                        // Apply updates immediately (no View Transition).
                        // CSS fade-in on .page-container handles the smooth entrance.
                        applyUpdates(msg.payload);
                        window._vlApplyPartBridge(document);

                        // Preserve the user's viewport position for same-page reactive updates.
                        if (!isNavigation && window._pendingScrollRestore) {
                            const restore = window._pendingScrollRestore;
                            const restoreScroll = () => {
                                window.scrollTo(restore.x || 0, restore.y || 0);
                            };

                            requestAnimationFrame(() => {
                                restoreScroll();
                                requestAnimationFrame(() => {
                                    restoreScroll();
                                    setTimeout(restoreScroll, 80);
                                });
                            });

                            debugLog(`[Scroll] Restored viewport to y=${restore.y}px after reactive update`);
                            window._pendingScrollRestore = null;
                        }
                        
                        // Page scroll position management after navigation
                        if (isNavigation && window._pendingPageKey) {
                            const targetKey = window._pendingPageKey;
                            window._currentPageKey = targetKey;
                            window._pendingPageKey = null;
                            window._pendingScrollRestore = null;
                            
                            // Restore saved scroll position, or scroll to top for first visit
                            const savedScroll = window._pageScrollPositions[targetKey];
                            // Use requestAnimationFrame to ensure DOM is updated before scrolling
                            requestAnimationFrame(() => {
                                if (savedScroll !== undefined && savedScroll > 0) {
                                    window.scrollTo(0, savedScroll);
                                    debugLog(`[Navigation] Restored scroll ${savedScroll}px for page: ${targetKey}`);
                                } else {
                                    window.scrollTo(0, 0);
                                    debugLog(`[Navigation] Scroll to top for page: ${targetKey}`);
                                }
                            });
                        }
                        
                        // Re-highlight code blocks after DOM update
                        if (typeof hljs !== 'undefined') {
                            document.querySelectorAll('.violit-code-block pre code:not(.hljs)').forEach(function(block) {
                                hljs.highlightElement(block);
                            });
                        }
                    } else if (msg.type === 'eval') {
                        const func = new Function(msg.code);
                        func();
                    } else if (msg.type === 'interval_ctrl') {
                        // Server-initiated interval control (pause/resume/stop)
                        const ctrl = window._vlIntervals && window._vlIntervals[msg.id];
                        if (ctrl) {
                            if      (msg.action === 'pause')  ctrl.pause();
                            else if (msg.action === 'resume') ctrl.resume();
                            else if (msg.action === 'stop')   ctrl.stop();
                        }
                    }
                };
            };

            window._vlConnectWebSocket = () => {
                const socket = new WebSocket(window._vlBuildWsUrl().toString());
                window._ws = socket;
                window._intentionalDisconnect = false;
                window._vlAttachWebSocketHandlers(socket);
                return socket;
            };

            window._vlReconnectWebSocket = (reason = 'reconnect') => {
                debugLog(`[WebSocket] Reconnecting socket (${reason})...`);
                if (window._vlHeartbeatReplyTimer) {
                    clearTimeout(window._vlHeartbeatReplyTimer);
                    window._vlHeartbeatReplyTimer = null;
                }
                window._vlClearResumeCheckTimers();
                window._wsReady = false;
                window._vlWsHelloReceived = false;
                window._vlDisposeSocket(window._ws);
                return window._vlConnectWebSocket();
            };

            window._ws = null;
            
            window._vlTimeout = disconnectTimeout;
            window._vlLastActivity = Date.now();
            window._vlConnectWebSocket();

            if (window._vlTimeout >= 0) {
                // Send ping every 25 seconds to prevent network timeout
                setInterval(() => {
                    if (window._ws && window._ws.readyState === 1) {
                        if (window._vlTimeout > 0 && (Date.now() - window._vlLastActivity) > window._vlTimeout * 1000) {
                            debugLog("[WebSocket] Disconnecting due to inactivity timeout.");
                            window._intentionalDisconnect = true;
                            if (window._vlHeartbeatReplyTimer) {
                                clearTimeout(window._vlHeartbeatReplyTimer);
                                window._vlHeartbeatReplyTimer = null;
                            }
                            window._ws.close();
                            document.body.style.transition = 'opacity 0.5s';
                            document.body.style.opacity = '0.5';
                            document.body.style.pointerEvents = 'none';
                        } else {
                            window._vlSendHeartbeat('interval');
                        }
                    } else if (!window._intentionalDisconnect && window._ws && window._ws.readyState !== WebSocket.CONNECTING) {
                        window._vlScheduleWsRecovery('interval:socket-closed');
                    }
                }, 25000);

                setInterval(() => {
                    window._vlEnsureLivePage('interval-watchdog');
                }, 5000);

                if (window._vlTimeout > 0) {
                    const resetActivity = () => { window._vlLastActivity = Date.now(); };
                    document.addEventListener('mousemove', resetActivity, {passive: true});
                    document.addEventListener('keydown', resetActivity, {passive: true});
                    document.addEventListener('click', resetActivity, {passive: true});
                    document.addEventListener('scroll', resetActivity, {passive: true});
                }
            }
        } else {
             // Lite Mode (HTMX) specifics
            document.addEventListener('DOMContentLoaded', () => {
                connectLiteStream();

                document.body.addEventListener('htmx:beforeSwap', function(evt) {
                    if (evt.detail.target) {
                        purgePlotly(evt.detail.target);
                    }
                });
                
                // Hot reload support for lite mode: poll server health
                let serverAlive = true;
                const checkServerHealth = () => {
                    // Add timestamp to prevent caching
                    const pollUrl = location.href.split('#')[0] + (location.href.indexOf('?') === -1 ? '?' : '&') + '_t=' + Date.now();
                    
                    fetch(pollUrl, { cache: 'no-store' })
                        .then(r => {
                            if (r.ok) {
                                if (!serverAlive) {
                                    debugLog("[Hot Reload] Server back online. Reloading...");
                                    document.body.style.opacity = '1'; // Restore opacity
                                    window.location.reload();
                                }
                                serverAlive = true;
                                // Ensure opacity is 1 if server is alive
                                document.body.style.opacity = '1';
                                document.body.style.pointerEvents = 'auto';
                            } else {
                                throw new Error('Server error');
                            }
                        })
                        .catch(() => {
                            if (serverAlive) {
                                debugLog("[Hot Reload] Server down. Waiting for restart...");
                                // Dim the page to indicate connection lost
                                document.body.style.transition = 'opacity 0.5s';
                                document.body.style.opacity = '0.5';
                                document.body.style.pointerEvents = 'none';
                            }
                            serverAlive = false;
                        });
                };
                setInterval(checkServerHealth, 2000);
            });
        }
        
        function toggleSidebar() {
            const sb = document.getElementById('sidebar');
            const main = document.getElementById('main');
            const isMobile = window.innerWidth <= 768;
            
            if (isMobile) {
                // Mobile: slide-over overlay mode
                const isOpen = sb.classList.contains('mobile-open');
                sb.classList.toggle('mobile-open');
                
                let backdrop = document.querySelector('.vl-sidebar-backdrop');
                if (!isOpen) {
                    // Opening
                    if (!backdrop) {
                        backdrop = document.createElement('div');
                        backdrop.className = 'vl-sidebar-backdrop';
                        backdrop.onclick = toggleSidebar;
                        document.body.appendChild(backdrop);
                    }
                    requestAnimationFrame(() => backdrop.classList.add('active'));
                    sb.style.display = 'flex'; // Ensure visible
                } else {
                    // Closing
                    if (backdrop) {
                        backdrop.classList.remove('active');
                        setTimeout(() => backdrop.remove(), 300);
                    }
                }
            } else {
                // Desktop: original collapse behavior
                sb.classList.toggle('collapsed');
                main.classList.toggle('sidebar-collapsed');
            }
        }
        
        // Auto-close sidebar on mobile after nav button click
        document.addEventListener('click', function(e) {
            const btn = e.target.closest('#sidebar wa-button');
            if (btn) {
                if (window.innerWidth <= 768) {
                    setTimeout(function() {
                        var sb = document.getElementById('sidebar');
                        if (sb && sb.classList.contains('mobile-open')) {
                            toggleSidebar();
                        }
                    }, 150);
                }
            }
        });

        function createToast(message, variant = 'primary', icon = 'circle-info') {
            const variantColors = { primary: '#0ea5e9', success: '#10b981', warning: '#f59e0b', danger: '#ef4444' };
            const toast = document.createElement('div');
            // Use CSS variables directly so theme changes are reflected automatically
            toast.style.cssText = `position: fixed; top: 20px; right: 20px; z-index: 10000; min-width: 300px; background: var(--wa-color-surface-raised, var(--vl-bg-card)); color: var(--vl-text); border: 1px solid var(--vl-border); border-left: 4px solid ${variantColors[variant]}; border-radius: 4px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); display: flex; align-items: center; gap: 12px; opacity: 0; transform: translateX(400px); transition: all 0.3s;`;
            const normalizedIcon = window.__vlNormalizeIconName ? window.__vlNormalizeIconName(icon) : icon;
            const iconEl = document.createElement('wa-icon');
            iconEl.setAttribute('name', normalizedIcon || 'circle-info');
            iconEl.style.fontSize = '1rem';
            iconEl.style.color = variantColors[variant] || 'var(--vl-text-muted)';

            const messageEl = document.createElement('div');
            messageEl.style.flex = '1';
            messageEl.style.fontSize = '14px';
            messageEl.textContent = message;

            const closeButton = document.createElement('button');
            closeButton.type = 'button';
            closeButton.textContent = '\u00D7';
            closeButton.onclick = function() { toast.remove(); };
            closeButton.style.cssText = 'background: none; border: none; cursor: pointer; padding: 4px; color: var(--vl-text-muted); font-size: 20px;';

            toast.appendChild(iconEl);
            toast.appendChild(messageEl);
            toast.appendChild(closeButton);
            document.body.appendChild(toast);
            requestAnimationFrame(() => { toast.style.opacity = '1'; toast.style.transform = 'translateX(0)'; });
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(400px)'; setTimeout(() => toast.remove(), 300); }, 3300);
        }
        function createBalloons() {
            const emojis = ['\uD83C\uDF88', '\uD83C\uDF89', '\u2728', '\uD83C\uDF8A', '\uD83C\uDF81', '\uD83C\uDF8F'];
            for (let i = 0; i < 60; i++) {
                const b = document.createElement('div');
                b.className = 'balloon';
                b.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                b.style.left = (Math.random() * 100) + 'vw';
                const startY = 100 + Math.random() * 20; // Start at 100vh-120vh (bottom)
                b.style.setProperty('--start-y', startY + 'vh');
                const duration = 4 + Math.random() * 3;
                b.style.setProperty('--duration', duration + 's');
                b.style.animationDelay = (Math.random() * 0.5) + 's';
                document.body.appendChild(b);
                setTimeout(() => b.remove(), (duration + 1) * 1000);
            }
        }
        function createSnow() {
            const emojis = ['\u2744\uFE0F', '\u2603\uFE0F', '\u2745', '\uD83E\uDDCA'];
            for (let i = 0; i < 50; i++) {
                const s = document.createElement('div');
                s.className = 'snowflake';
                s.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                s.style.left = Math.random() * 100 + 'vw';
                const duration = 4 + Math.random() * 4;
                s.style.setProperty('--duration', duration + 's');
                s.style.animationDelay = Math.random() * 1.0 + 's';
                document.body.appendChild(s);
                setTimeout(() => s.remove(), (duration + 5) * 1000);
            }
        }
        
        // Restore state from URL Hash (or force Home if no hash)
        function restoreFromHash() {
            const getNavButtonPageKey = (btn) => {
                if (!btn) return null;
                const dataKey = btn.getAttribute('data-page-key');
                if (dataKey) return dataKey;
                const onclickAttr = btn.getAttribute('onclick') || '';
                const keyMatch = onclickAttr.match(/'(page_[^']+)'/);
                if (keyMatch) return keyMatch[1];
                const hxVals = btn.getAttribute('hx-vals') || '';
                const hxMatch = hxVals.match(/"value"\s*:\s*"(page_[^"]+)"/);
                return hxMatch ? hxMatch[1] : null;
            };

            const isNavButtonActive = (btn) => {
                if (!btn) return false;
                return btn.getAttribute('data-nav-active') === 'true'
                    || (btn.getAttribute('variant') === 'brand' && btn.getAttribute('appearance') === 'accent');
            };

            // Decode the URL hash, including encoded non-ASCII characters.
            let hash = window.location.hash.substring(1); // Remove #
            try {
                hash = decodeURIComponent(hash);
            } catch (e) {
                debugLog('Hash decode error:', e);
            }
            
            // If no hash, treat it as Home and avoid stale initial navigation state.
            if (!hash || hash === 'home') {
                debugLog('[Navigation] No hash found, forcing Home page');
                const tryClickHome = (attempts = 0) => {
                    if (attempts >= 20) return;
                    const navButtons = document.querySelectorAll('#sidebar wa-button');
                    if (navButtons.length > 0) {
                        const homeBtn = navButtons[0]; // First button is Home
                        const homeKey = getNavButtonPageKey(homeBtn);
                        if (!isNavButtonActive(homeBtn)) {
                            homeBtn.click();
                            debugLog('[Navigation] Clicked Home button');
                        } else if (homeKey) {
                            window._currentPageKey = homeKey;
                        }
                    } else {
                        setTimeout(() => tryClickHome(attempts + 1), 100);
                    }
                };
                tryClickHome();
                return;
            }
            
            const targetKey = 'page_' + hash;
            debugLog(`[Navigation] Restoring from hash: "${hash}" (key: ${targetKey})`);
            
            const tryRestore = (attempts = 0) => {
                // Stop after 5 seconds
                if (attempts >= 50) {
                     console.warn(`[Navigation] Failed to restore hash "${hash}"`);
                     return;
                }
                
                const navButtons = document.querySelectorAll('#sidebar wa-button');
                if (navButtons.length === 0) {
                    setTimeout(() => tryRestore(attempts + 1), 100);
                    return;
                }
                
                for (let btn of navButtons) {
                    const btnKey = getNavButtonPageKey(btn);
                    if (btnKey === targetKey) {
                        debugLog(`[Navigation] Found target button for hash "${hash}". Clicking...`);
                        
                        // Check if already active to avoid redundant clicks
                        if (isNavButtonActive(btn)) {
                            window._currentPageKey = targetKey;
                            debugLog('  - Already active, skipping click.');
                            return;
                        }
                        
                        btn.click();
                        return;
                    }
                }
                
                // Keep retrying in case the specific button hasn't rendered yet (unlikely if container exists)
                setTimeout(() => tryRestore(attempts + 1), 100);
            };
            
            tryRestore();
        }
        
        // Note: For ws mode, restoreFromHash is called from ws.onopen
        // For lite mode, call it on load:
        if (mode !== 'ws') {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => setTimeout(restoreFromHash, 200));
            } else {
                setTimeout(restoreFromHash, 200);
            }
        } else {
            const handleBrowserHistoryNavigation = () => {
                if (window._suppressHashRestoreOnce) {
                    window._suppressHashRestoreOnce = false;
                    return;
                }
                if (!window._wsReady) {
                    return;
                }
                setTimeout(restoreFromHash, 40);
            };

            window.addEventListener('hashchange', handleBrowserHistoryNavigation);
            window.addEventListener('popstate', handleBrowserHistoryNavigation);
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {
                    window._vlLastHiddenAt = Date.now();
                    return;
                }
                if (document.visibilityState === 'visible') {
                    window._vlHandleResume('visibilitychange');
                }
            });
            window.addEventListener('focus', () => window._vlHandleResume('focus'));
            window.addEventListener('online', () => window._vlHandleResume('online'));
            window.addEventListener('pageshow', () => window._vlHandleResume('pageshow'));
            document.addEventListener('pointerdown', () => window._vlRevivePageOnInteraction('pointerdown'), { passive: true, capture: true });
            document.addEventListener('touchstart', () => window._vlRevivePageOnInteraction('touchstart'), { passive: true, capture: true });
            document.addEventListener('keydown', () => window._vlRevivePageOnInteraction('keydown'), { passive: true, capture: true });
        }