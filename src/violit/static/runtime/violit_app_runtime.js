        const runtimeConfig = window.__vlRuntimeConfig || {};
        const disconnectTimeout = Number.isFinite(Number(runtimeConfig.disconnectTimeout))
            ? Number(runtimeConfig.disconnectTimeout)
            : -1;
        const rootPath = typeof runtimeConfig.rootPath === 'string' && runtimeConfig.rootPath && runtimeConfig.rootPath !== '/'
            ? runtimeConfig.rootPath.replace(/\/+$/, '')
            : '';
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
        const withRootPath = (path) => {
            if (typeof path !== 'string' || !path) {
                return path;
            }
            if (/^[a-z]+:/i.test(path) || path.startsWith('//')) {
                return path;
            }
            const normalizedPath = path.startsWith('/') ? path : `/${path}`;
            return rootPath ? `${rootPath}${normalizedPath}` : normalizedPath;
        };
        const buildAppUrl = (path) => new URL(withRootPath(path), window.location.origin);
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
        window._vlRootPath = rootPath;
        window._vlWithRootPath = withRootPath;
        window._vlBuildAppUrl = buildAppUrl;
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

        function collectPersistedExpanderDetails(root) {
            if (!(root instanceof Element)) return [];
            const matches = [];
            const ownInit = root.getAttribute ? (root.getAttribute('data-vl-init') || '') : '';
            if (
                root.tagName
                && root.tagName.toLowerCase() === 'wa-details'
                && ownInit.split(/\s+/).includes('expander-persistence')
            ) {
                matches.push(root);
            }
            root.querySelectorAll('wa-details[data-vl-init~="expander-persistence"]').forEach(function(details) {
                if (!matches.includes(details)) {
                    matches.push(details);
                }
            });
            return matches;
        }

        function readPersistedExpanderConfig(details) {
            if (!(details instanceof Element)) return null;
            const rawConfig = details.getAttribute('data-vl-expander-config');
            if (!rawConfig) return null;
            try {
                return JSON.parse(rawConfig);
            } catch (error) {
                return null;
            }
        }

        function preserveIncomingExpanderOpenState(currentRoot, nextRoot) {
            if (!(currentRoot instanceof Element) || !(nextRoot instanceof Element)) {
                return false;
            }

            const currentDetails = collectPersistedExpanderDetails(currentRoot);
            const nextDetails = collectPersistedExpanderDetails(nextRoot);
            if (!currentDetails.length || !nextDetails.length) {
                return false;
            }

            const currentByStorageKey = new Map();
            currentDetails.forEach(function(details) {
                const config = readPersistedExpanderConfig(details);
                if (config && config.storageKey) {
                    currentByStorageKey.set(config.storageKey, { details, config });
                }
            });

            let mutated = false;
            nextDetails.forEach(function(details) {
                const nextConfig = readPersistedExpanderConfig(details);
                if (!nextConfig || !nextConfig.storageKey) {
                    return;
                }
                const currentMatch = currentByStorageKey.get(nextConfig.storageKey);
                if (!currentMatch) {
                    return;
                }

                const storedOpen = sessionStorage.getItem(nextConfig.storageKey);
                const preservedOpen = storedOpen === null ? currentMatch.details.open === true : storedOpen === 'true';

                if (preservedOpen) {
                    details.setAttribute('open', '');
                } else {
                    details.removeAttribute('open');
                }

                nextConfig.serverOpen = preservedOpen;
                details.setAttribute('data-vl-expander-config', JSON.stringify(nextConfig));
                mutated = true;
            });

            return mutated;
        }

        function preserveIncomingExpanderStatesInHtml(html) {
            if (typeof html !== 'string' || html.indexOf('expander-persistence') === -1) {
                return html;
            }

            const temp = document.createElement('div');
            temp.innerHTML = html;
            Array.from(temp.children).forEach(function(nextRoot) {
                if (!(nextRoot instanceof Element) || !nextRoot.id) {
                    return;
                }
                const currentRoot = document.getElementById(nextRoot.id);
                if (currentRoot) {
                    preserveIncomingExpanderOpenState(currentRoot, nextRoot);
                }
            });
            return temp.innerHTML;
        }

        function blurFocusedWaButtonHost() {
            const activeElement = document.activeElement;
            if (!(activeElement instanceof Element)) {
                return;
            }

            const buttonHost = activeElement.closest('wa-button');
            if (!(buttonHost instanceof HTMLElement)) {
                return;
            }

            const shadowActive = buttonHost.shadowRoot ? buttonHost.shadowRoot.activeElement : null;
            if (shadowActive && typeof shadowActive.blur === 'function') {
                try {
                    shadowActive.blur();
                } catch (error) {}
            }

            if (typeof buttonHost.blur === 'function') {
                try {
                    buttonHost.blur();
                } catch (error) {}
            }
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

        function getCustomInitializerHost(root) {
            if (!(root instanceof Element)) return null;
            if (root.hasAttribute('data-vl-init')) {
                return root;
            }
            return root.querySelector('[data-vl-init]');
        }

        function syncSelectorInnerHtml(currentRoot, nextRoot, selector) {
            const currentNode = currentRoot ? currentRoot.querySelector(selector) : null;
            const nextNode = nextRoot ? nextRoot.querySelector(selector) : null;
            if (!currentNode || !nextNode) return;
            currentNode.innerHTML = nextNode.innerHTML;
        }

        function syncSelectorText(currentRoot, nextRoot, selector) {
            const currentNode = currentRoot ? currentRoot.querySelector(selector) : null;
            const nextNode = nextRoot ? nextRoot.querySelector(selector) : null;
            if (!currentNode || !nextNode) return;
            currentNode.textContent = nextNode.textContent;
        }

        function syncKeyedChildrenOrder(currentContainer, nextContainer, keyAttr) {
            if (!currentContainer || !nextContainer) return;

            const currentByKey = new Map();
            Array.from(currentContainer.children).forEach((child) => {
                const key = child.getAttribute ? child.getAttribute(keyAttr) : null;
                if (key) {
                    currentByKey.set(key, child);
                }
            });

            Array.from(nextContainer.children).forEach((nextChild) => {
                const key = nextChild.getAttribute ? nextChild.getAttribute(keyAttr) : null;
                if (!key) return;

                const currentChild = currentByKey.get(key);
                if (currentChild) {
                    syncElementAttributes(currentChild, nextChild);
                    currentChild.innerHTML = nextChild.innerHTML;
                    currentContainer.appendChild(currentChild);
                    currentByKey.delete(key);
                    return;
                }

                currentContainer.appendChild(nextChild.cloneNode(true));
            });

            currentByKey.forEach((child) => {
                child.remove();
            });
        }

        function trySmartUpdateCustomWidgetWrapper(currentRoot, incomingMarkupOrRoot) {
            if (!(currentRoot instanceof Element)) return false;

            let nextRoot = null;
            if (typeof incomingMarkupOrRoot === 'string') {
                const temp = document.createElement('div');
                temp.innerHTML = incomingMarkupOrRoot;
                nextRoot = temp.firstElementChild;
            } else if (incomingMarkupOrRoot instanceof Element) {
                nextRoot = incomingMarkupOrRoot;
            }

            if (!(nextRoot instanceof Element)) return false;

            const currentHost = getCustomInitializerHost(currentRoot);
            const nextHost = getCustomInitializerHost(nextRoot);
            if (!currentHost || !nextHost) return false;

            const currentInit = currentHost.getAttribute('data-vl-init') || '';
            const nextInit = nextHost.getAttribute('data-vl-init') || '';
            if (!currentInit || currentInit !== nextInit || !currentInit.startsWith('cw-')) {
                return false;
            }

            syncElementAttributes(currentRoot, nextRoot);
            syncElementAttributes(currentHost, nextHost);

            if (currentInit === 'cw-theme-picker') {
                currentHost.innerHTML = nextHost.innerHTML;
            } else if (currentInit === 'cw-dual-range') {
                syncSelectorInnerHtml(currentHost, nextHost, '.cw-widget-header');
                syncSelectorInnerHtml(currentHost, nextHost, '.cw-range-summary');
                syncSelectorInnerHtml(currentHost, nextHost, '.cw-range-copy');
                syncSelectorInnerHtml(currentHost, nextHost, '.cw-range-pillbar');
                syncSelectorText(currentHost, nextHost, '[data-range-start]');
                syncSelectorText(currentHost, nextHost, '[data-range-end]');
                syncSelectorText(currentHost, nextHost, '[data-range-span]');
            } else if (currentInit === 'cw-sortable-board') {
                syncSelectorInnerHtml(currentHost, nextHost, '.cw-widget-header');
                const currentList = currentHost.querySelector('[data-board-list]');
                const nextList = nextHost.querySelector('[data-board-list]');
                syncKeyedChildrenOrder(currentList, nextList, 'data-item-id');
            } else {
                return false;
            }

            if (window.violitRuntime && typeof window.violitRuntime.initElement === 'function') {
                window.violitRuntime.initElement(currentHost);
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

        const captureViewportScroll = () => ({
            x: window.scrollX || 0,
            y: window.scrollY || window.pageYOffset || 0,
        });

        const restoreViewportScroll = (restore) => {
            if (!restore) {
                return;
            }

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
        };

        window.violitRuntime = window.violitRuntime || {};
        const violitRuntime = window.violitRuntime;
        violitRuntime._initializers = violitRuntime._initializers || {};

        violitRuntime.registerInitializer = function(name, initializer) {
            if (!name || typeof initializer !== 'function') {
                return;
            }
            violitRuntime._initializers[name] = initializer;
        };

        violitRuntime.readJsonAttr = function(element, attrName, fallback = null) {
            if (!element || typeof element.getAttribute !== 'function') {
                return fallback;
            }
            const rawValue = element.getAttribute(attrName);
            if (!rawValue) {
                return fallback;
            }
            try {
                return JSON.parse(rawValue);
            } catch (error) {
                console.warn('[violitRuntime] Failed to parse JSON attr', attrName, error);
                return fallback;
            }
        };

        violitRuntime.markBound = function(element, key) {
            if (!element || !key) {
                return false;
            }
            const attrName = `data-vl-bound-${key}`;
            if (element.hasAttribute(attrName)) {
                return true;
            }
            element.setAttribute(attrName, 'true');
            return false;
        };

        violitRuntime.allowFocusedUpdateTree = function(element) {
            if (!element || typeof window._vlAllowNextFocusedUpdate !== 'function') {
                return;
            }
            let current = element;
            while (current) {
                if (current.id) {
                    window._vlAllowNextFocusedUpdate(current.id);
                }
                current = current.parentElement;
            }
        };

        violitRuntime.postLiteAction = async function(cid, value, options = {}) {
            if (mode !== 'lite' || !cid || typeof window.fetch !== 'function') {
                return null;
            }

            const scrollRestore = captureViewportScroll();
            const params = new URLSearchParams();
            params.set('value', typeof value === 'string' ? value : JSON.stringify(value));
            params.set('_vl_skip_clicked', options.skipClicked === false ? 'false' : 'true');
            if (options.extraValues && typeof options.extraValues === 'object') {
                Object.entries(options.extraValues).forEach(([key, extraValue]) => {
                    if (extraValue === undefined || extraValue === null) {
                        return;
                    }
                    params.set(key, String(extraValue));
                });
            }
            if (window._csrf_token) params.set('_csrf_token', window._csrf_token);
            if (window._vlViewId) params.set('_vl_view_id', window._vlViewId);

            const response = await fetch(withRootPath(`/action/${cid}`), {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    ...(window._vlViewId ? { 'X-Violit-View': window._vlViewId } : {}),
                },
                body: params.toString(),
            });
            const html = await response.text();
            if (response.ok && html) {
                applyLiteStreamPayload(html);
                restoreViewportScroll(scrollRestore);
            }
            return { response, html };
        };

        violitRuntime.emitAction = function(cid, value, options = {}) {
            if (!cid) {
                return null;
            }
            if (typeof window.sendAction === 'function') {
                window.sendAction(cid, value);
                return null;
            }
            if (typeof violitRuntime.postLiteAction === 'function') {
                return violitRuntime.postLiteAction(cid, value, options);
            }
            return null;
        };

        violitRuntime.initElement = function(element) {
            if (!element || typeof element.getAttribute !== 'function') {
                return;
            }
            const initNames = (element.getAttribute('data-vl-init') || '')
                .split(/\s+/)
                .map((name) => name.trim())
                .filter(Boolean);

            initNames.forEach((name) => {
                const initializer = violitRuntime._initializers[name];
                if (typeof initializer !== 'function') {
                    return;
                }
                initializer(element);
            });
        };

        violitRuntime.initScope = function(scope = document) {
            const roots = [];
            if (scope instanceof Element || scope instanceof Document || scope instanceof DocumentFragment) {
                roots.push(scope);
            }
            if (scope && scope.jquery && scope.length) {
                scope.each(function() {
                    roots.push(this);
                });
            }

            roots.forEach((root) => {
                if (!root || !root.querySelectorAll) {
                    return;
                }
                if (root instanceof Element && root.hasAttribute('data-vl-init')) {
                    violitRuntime.initElement(root);
                }
                root.querySelectorAll('[data-vl-init]').forEach((element) => {
                    violitRuntime.initElement(element);
                });
            });

            if (typeof window._vlApplyPartBridge === 'function') {
                window._vlApplyPartBridge(scope || document);
            }
            if (typeof window._vlApplyVisualStreamSmoothing === 'function') {
                window._vlApplyVisualStreamSmoothing(scope || document);
            }
        };

        violitRuntime.scheduleScopeInit = function(scope = document) {
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    violitRuntime.initScope(scope);
                });
            });
        };

        violitRuntime.resolveControlTarget = function(element) {
            if (!element) {
                return null;
            }
            if (element.shadowRoot) {
                return element.shadowRoot.querySelector('input, textarea, select') || element;
            }
            return element;
        };

        violitRuntime.readControlValue = function(element, valueProp) {
            if (!element) {
                return '';
            }
            if (valueProp === 'checked') {
                return !!element.checked;
            }
            if (valueProp === 'multiselect-comma') {
                const values = Array.isArray(element.value) ? element.value : (element.value ? [element.value] : []);
                return values.join(',');
            }
            return element.value == null ? '' : element.value;
        };

        violitRuntime.writeControlValue = function(element, valueProp, nextValue) {
            if (!element) {
                return;
            }
            if (valueProp === 'checked') {
                element.checked = !!nextValue;
                return;
            }
            if (valueProp === 'multiselect-comma') {
                if (Array.isArray(nextValue)) {
                    element.value = nextValue;
                } else if (typeof nextValue === 'string' && nextValue) {
                    element.value = nextValue.split(',').filter(Boolean);
                } else {
                    element.value = [];
                }
                return;
            }
            element.value = nextValue == null ? '' : nextValue;
        };

        violitRuntime.normalizeControlValue = function(valueProp, value) {
            if (valueProp === 'checked') {
                return value ? 'true' : 'false';
            }
            if (valueProp === 'multiselect-comma') {
                if (Array.isArray(value)) {
                    return value.join(',');
                }
                return value == null ? '' : String(value);
            }
            return value == null ? '' : String(value);
        };

        violitRuntime.syncControlValue = function(element, config) {
            if (!element || !config || !Object.prototype.hasOwnProperty.call(config, 'desiredValue')) {
                return;
            }

            const desiredValue = config.desiredValue;
            const valueProp = config.valueProp || 'value';
            const applySync = () => {
                const currentValue = violitRuntime.normalizeControlValue(valueProp, violitRuntime.readControlValue(element, valueProp));
                const nextValue = violitRuntime.normalizeControlValue(valueProp, desiredValue);
                if (currentValue !== nextValue) {
                    violitRuntime.writeControlValue(element, valueProp, desiredValue);
                }
                if (config.extraSync === 'textarea-autoresize') {
                    if (typeof element.handleValueChange === 'function') element.handleValueChange();
                    if (typeof element.setTextareaDimensions === 'function') element.setTextareaDimensions();
                }
            };

            applySync();
            if (element.updateComplete && typeof element.updateComplete.then === 'function') {
                element.updateComplete.then(applySync);
            }

            requestAnimationFrame(() => {
                applySync();
                setTimeout(applySync, typeof config.syncDelayMs === 'number' ? config.syncDelayMs : 150);
            });
        };

        violitRuntime.buildControlSyncSignature = function(config = {}) {
            if (!config || !Object.prototype.hasOwnProperty.call(config, 'desiredValue')) {
                return '';
            }
            const valueProp = config.valueProp || 'value';
            return JSON.stringify({
                valueProp,
                desiredValue: violitRuntime.normalizeControlValue(valueProp, config.desiredValue),
                extraSync: config.extraSync || '',
            });
        };

        violitRuntime.bindInputControl = function(element, config = {}) {
            if (!element || !config.cid) {
                return;
            }

            const valueProp = config.valueProp || 'value';
            const eventName = config.eventName || 'change';
            const transport = config.transport || (mode === 'ws' ? 'ws' : 'lite-hx');
            const submitOnEnter = config.submitOnEnter === true;
            const submitDirtyFlag = config.submitDirtyFlag === true;

            const syncSignature = violitRuntime.buildControlSyncSignature(config);
            const previousSyncSignature = element.getAttribute('data-vl-sync-signature') || '';
            if (syncSignature !== previousSyncSignature) {
                violitRuntime.syncControlValue(element, config);
                if (syncSignature) {
                    element.setAttribute('data-vl-sync-signature', syncSignature);
                } else {
                    element.removeAttribute('data-vl-sync-signature');
                }
            }

            const readCurrentValue = () => violitRuntime.readControlValue(element, valueProp);
            const controlTargets = (() => {
                const resolvedTarget = violitRuntime.resolveControlTarget(element);
                const targets = [element];
                if (resolvedTarget && resolvedTarget !== element) {
                    targets.push(resolvedTarget);
                }
                return targets;
            })();
            const shouldSkipEcho = function() {
                if (!Object.prototype.hasOwnProperty.call(element, '_vlSkipNextInputEventValue')) return false;
                const skipValue = element._vlSkipNextInputEventValue;
                delete element._vlSkipNextInputEventValue;
                return violitRuntime.normalizeControlValue(valueProp, readCurrentValue()) === String(skipValue);
            };
            const scheduleControlDispatch = function(key, emit) {
                const pendingKey = `_vlPendingDispatch_${key}`;
                if (element[pendingKey]) {
                    return;
                }
                element[pendingKey] = true;

                const flush = function() {
                    element[pendingKey] = false;
                    emit(readCurrentValue());
                };

                const scheduleFrame = function() {
                    requestAnimationFrame(flush);
                };

                if (element.updateComplete && typeof element.updateComplete.then === 'function') {
                    element.updateComplete.then(scheduleFrame).catch(scheduleFrame);
                    return;
                }
                scheduleFrame();
            };

            if (transport === 'ws') {
                controlTargets.forEach(function(target, index) {
                    const listenerKey = `ws-listener-${config.cid}-${eventName}-${index}`;
                    if (violitRuntime.markBound(target, listenerKey)) {
                        return;
                    }
                    target.addEventListener(eventName, function() {
                        scheduleControlDispatch(`ws_${config.cid}_${eventName}`, function(nextValue) {
                            if (shouldSkipEcho()) return;
                            window.sendAction(config.cid, nextValue);
                        });
                    });
                });
            }

            if (transport === 'lite-direct') {
                controlTargets.forEach(function(target, index) {
                    const listenerKey = `lite-direct-${config.cid}-${eventName}-${index}`;
                    if (violitRuntime.markBound(target, listenerKey)) {
                        return;
                    }
                    target.addEventListener(eventName, function() {
                        scheduleControlDispatch(`lite_${config.cid}_${eventName}`, function(nextValue) {
                            violitRuntime.postLiteAction(config.cid, nextValue);
                        });
                    });
                });
            }

            if (transport === 'lite-hx' && config.useEchoGuard !== false) {
                controlTargets.forEach(function(target, index) {
                    const listenerKey = `lite-echo-${config.cid}-${eventName}-${index}`;
                    if (violitRuntime.markBound(target, listenerKey)) {
                        return;
                    }
                    target.addEventListener(eventName, function(event) {
                        if (!shouldSkipEcho()) return;
                        event.preventDefault();
                        event.stopImmediatePropagation();
                    }, true);
                });
            }

            const bindSubmitOnEnter = function(attempts) {
                if (!submitOnEnter) return;
                const target = violitRuntime.resolveControlTarget(element) || (attempts >= 10 ? element : null);
                if (!target) {
                    setTimeout(function() { bindSubmitOnEnter(attempts + 1); }, 80);
                    return;
                }
                if (violitRuntime.markBound(target, `submit-enter-${config.cid}`)) {
                    return;
                }
                target.addEventListener('keydown', function(event) {
                    if (event.key !== 'Enter') return;
                    event.preventDefault();
                    const currentValue = readCurrentValue();
                    element._vlSkipNextInputEventValue = violitRuntime.normalizeControlValue(valueProp, currentValue);
                    violitRuntime.allowFocusedUpdateTree(element);
                    const payload = { eventType: 'submit', value: currentValue };
                    if (transport === 'ws') {
                        window.sendAction(config.cid, payload);
                        return;
                    }
                    if (transport === 'lite-direct') {
                        violitRuntime.postLiteAction(config.cid, payload, {
                            extraValues: submitDirtyFlag ? { _vl_lite_stream_dirty: 'true' } : null,
                        });
                        return;
                    }
                    if (window.htmx && typeof window.htmx.ajax === 'function') {
                        const values = { value: JSON.stringify(payload) };
                        if (submitDirtyFlag) {
                            values._vl_lite_stream_dirty = 'true';
                        }
                        htmx.ajax('POST', `/action/${config.cid}`, {
                            values,
                            swap: 'none',
                        });
                    }
                });
            };

            bindSubmitOnEnter(0);
        };

        violitRuntime.registerInitializer('input-control', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-input-config', null);
            if (!config) {
                return;
            }
            violitRuntime.bindInputControl(element, config);
        });

        violitRuntime.registerInitializer('part-bridge', function(element) {
            const run = function(attempts) {
                if (!element || !element.isConnected) {
                    return;
                }
                if (element.shadowRoot && typeof window.applyPartStyles === 'function') {
                    window.applyPartStyles(element);
                    return;
                }
                if (attempts < 20) {
                    setTimeout(function() { run(attempts + 1); }, 80);
                }
            };
            run(0);
        });

        violitRuntime.registerInitializer('expander-persistence', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-expander-config', null);
            if (!config || !config.storageKey) {
                return;
            }

            const details = element;
            const storedOpen = sessionStorage.getItem(config.storageKey);
            const serverOpen = config.serverOpen === true;
            const initialOpen = storedOpen === null ? serverOpen : storedOpen === 'true';

            const applyOpen = function(nextOpen) {
                if (details.open !== nextOpen) {
                    details.open = nextOpen;
                }
            };

            const armPersistenceFromSummaryInteraction = function(event) {
                const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
                const fromSummary = path.some(function(node) {
                    if (!node) return false;
                    if (node.tagName === 'SUMMARY') return true;
                    if (typeof node.getAttribute !== 'function') return false;
                    if (node.getAttribute('slot') === 'summary') return true;
                    const partAttr = node.getAttribute('part') || '';
                    if (!partAttr) return false;
                    const parts = partAttr.split(/\s+/);
                    return parts.includes('header') || parts.includes('summary');
                });

                if (!fromSummary) return;
                if (event.type === 'keydown') {
                    const key = event.key || '';
                    if (key !== 'Enter' && key !== ' ') return;
                }

                details.dataset.vlExpanderPersistArmed = 'true';
            };

            const shouldPersistToggle = function() {
                return (
                    details.dataset.vlExpanderPersistArmed === 'true' &&
                    details.isConnected &&
                    document.getElementById(details.id) === details
                );
            };

            const clearPersistArm = function() {
                delete details.dataset.vlExpanderPersistArmed;
            };

            applyOpen(initialOpen);
            requestAnimationFrame(function() {
                applyOpen(initialOpen);
            });

            if (violitRuntime.markBound(details, `expander-persistence-${details.id}`)) {
                return;
            }

            details.addEventListener('click', armPersistenceFromSummaryInteraction, true);
            details.addEventListener('keydown', armPersistenceFromSummaryInteraction, true);
            details.addEventListener('wa-show', function() {
                requestAnimationFrame(function() {
                    if (shouldPersistToggle()) {
                        sessionStorage.setItem(config.storageKey, 'true');
                    }
                    clearPersistArm();
                });
            });
            details.addEventListener('wa-hide', function() {
                requestAnimationFrame(function() {
                    if (shouldPersistToggle()) {
                        sessionStorage.setItem(config.storageKey, 'false');
                    }
                    clearPersistArm();
                });
            });
        });

        violitRuntime.registerInitializer('tabs-persistence', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-tabs-config', null);
            if (!config || !config.storageKey) {
                return;
            }

            const group = element;
            const validPanels = new Set(Array.isArray(config.validPanels) ? config.validPanels : []);
            const defaultPanel = typeof config.defaultPanel === 'string' ? config.defaultPanel : '';
            const serverPanel = typeof config.serverPanel === 'string' ? config.serverPanel : defaultPanel;
            const actionCid = typeof config.actionCid === 'string' ? config.actionCid : '';
            const shouldSyncServer = config.syncServer === true;

            const applyActivePanel = function(panelName) {
                if (!panelName || !validPanels.has(panelName)) return false;
                group.setAttribute('active', panelName);
                requestAnimationFrame(function() {
                    group.setAttribute('active', panelName);
                    if (typeof group.updateActiveTab === 'function') {
                        group.updateActiveTab();
                    }
                });
                return true;
            };

            const syncServer = function(panelName) {
                if (!shouldSyncServer || !actionCid) return;
                if (!panelName || panelName === serverPanel) return;
                if (typeof window.sendAction === 'function') {
                    window.sendAction(actionCid, panelName);
                    return;
                }
                if (mode === 'lite') {
                    violitRuntime.postLiteAction(actionCid, panelName);
                }
            };

            const storedPanel = sessionStorage.getItem(config.storageKey);
            const initialPanel = validPanels.has(storedPanel) ? storedPanel : (validPanels.has(serverPanel) ? serverPanel : defaultPanel);
            applyActivePanel(initialPanel);
            sessionStorage.setItem(config.storageKey, initialPanel);
            syncServer(initialPanel);

            if (violitRuntime.markBound(group, `tabs-persistence-${group.id}`)) {
                return;
            }

            group.addEventListener('wa-tab-show', function(event) {
                const panelName = event.detail && event.detail.name;
                if (!validPanels.has(panelName)) return;
                sessionStorage.setItem(config.storageKey, panelName);
                syncServer(panelName);
            });
        });

        violitRuntime.registerInitializer('dialog-auto-open', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-dialog-config', null);
            if (!config || !config.actionCid) {
                return;
            }

            const dialog = element;
            dialog.open = true;
            requestAnimationFrame(function() {
                dialog.open = true;
            });

            if (violitRuntime.markBound(dialog, `dialog-auto-open-${dialog.id}`)) {
                return;
            }

            dialog.addEventListener('wa-after-hide', function(event) {
                if (!event || !event.target || event.target.id !== dialog.id) {
                    return;
                }
                if (typeof window.sendAction === 'function') {
                    window.sendAction(config.actionCid, 'closed');
                    return;
                }
                if (mode === 'lite') {
                    violitRuntime.postLiteAction(config.actionCid, 'closed');
                }
            });
        });

        violitRuntime.requestDeferredAction = function(cid, value) {
            if (!cid) {
                return;
            }
            if (typeof window._vlQueueDeferredAction === 'function') {
                window._vlQueueDeferredAction(cid, value);
                return;
            }
            violitRuntime.emitAction(cid, value);
        };

        violitRuntime.deferHydration = function(target, hydrate, options = {}) {
            if (typeof hydrate !== 'function') {
                return;
            }

            const viewportOffsetPx = Number.isFinite(Number(options.viewportOffsetPx))
                ? Math.max(0, Number(options.viewportOffsetPx))
                : 180;
            const afterInitialRender = options.afterInitialRender === true;
            let hydrated = false;

            const resolveTarget = function() {
                if (typeof target === 'function') {
                    return target();
                }
                return target;
            };

            const isNearViewport = function(element) {
                if (!element || typeof element.getBoundingClientRect !== 'function') {
                    return true;
                }
                const rect = element.getBoundingClientRect();
                return rect.bottom >= -viewportOffsetPx && rect.top <= window.innerHeight + viewportOffsetPx;
            };

            const finish = function(element) {
                if (hydrated) {
                    return;
                }
                hydrated = true;
                hydrate(element);
            };

            const observe = function() {
                const element = resolveTarget();
                if (!element) {
                    setTimeout(observe, 50);
                    return;
                }

                if (isNearViewport(element)) {
                    finish(element);
                    return;
                }

                if (!('IntersectionObserver' in window)) {
                    finish(element);
                    return;
                }

                const io = new IntersectionObserver(function(entries) {
                    const entry = entries && entries[0];
                    if (!entry) {
                        return;
                    }
                    if (entry.isIntersecting || entry.boundingClientRect.top < window.innerHeight + viewportOffsetPx) {
                        io.disconnect();
                        finish(resolveTarget() || element);
                    }
                }, {
                    rootMargin: `${viewportOffsetPx}px 0px ${viewportOffsetPx + 80}px 0px`,
                });

                io.observe(element);
            };

            if (afterInitialRender && !window.__vlInitialRenderMetrics) {
                const existing = resolveTarget();
                if (existing && isNearViewport(existing)) {
                    observe();
                    return;
                }
                window.addEventListener('violit:initial-render-ready', observe, { once: true });
                return;
            }

            observe();
        };

        violitRuntime.registerInitializer('deferred-chart', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-deferred-chart-config', null);
            const chartId = config && typeof config.cid === 'string' ? config.cid : element.id;
            if (!chartId) {
                return;
            }

            if (!window._vlDeferredChartsRequested) {
                window._vlDeferredChartsRequested = new Set();
            }

            const requestValue = config && Object.prototype.hasOwnProperty.call(config, 'requestValue')
                ? config.requestValue
                : '__REQUEST_DATA__';
            const preloadLib = config && typeof config.preloadLib === 'string' ? config.preloadLib : 'Plotly';
            const trigger = config && typeof config.trigger === 'string' ? config.trigger : 'visible';
            const afterInitialRender = config && config.afterInitialRender === true;
            const viewportOffsetPx = Number.isFinite(Number(config && config.viewportOffsetPx))
                ? Math.max(0, Number(config.viewportOffsetPx))
                : 180;

            const requestHydration = function() {
                if (window._vlDeferredChartsRequested.has(chartId)) return;

                const liveElement = document.getElementById(chartId);
                if (!liveElement) return;

                window._vlDeferredChartsRequested.add(chartId);

                if (preloadLib && typeof window._vlPreloadLib === 'function') {
                    window._vlPreloadLib(preloadLib);
                }

                violitRuntime.requestDeferredAction(chartId, requestValue);
            };

            const observeVisibility = function() {
                const liveElement = document.getElementById(chartId);
                if (!liveElement) {
                    setTimeout(observeVisibility, 50);
                    return;
                }

                if (trigger === 'immediate') {
                    requestHydration();
                    return;
                }

                if (typeof violitRuntime.deferHydration === 'function') {
                    violitRuntime.deferHydration(function() {
                        return document.getElementById(chartId);
                    }, requestHydration, {
                        afterInitialRender: afterInitialRender,
                        viewportOffsetPx: viewportOffsetPx,
                    });
                    return;
                }

                requestHydration();
            };

            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', observeVisibility, { once: true });
            } else {
                observeVisibility();
            }
        });

        violitRuntime.bindAgGridSurface = function(config = {}) {
            if (!config || !config.apiKey) {
                return;
            }

            const getApi = function() {
                return window[config.apiKey];
            };

            if (config.searchInputId) {
                const searchInput = document.getElementById(config.searchInputId);
                if (searchInput && !violitRuntime.markBound(searchInput, `ag-grid-search-${config.searchInputId}`)) {
                    const applyQuickFilter = function() {
                        const api = getApi();
                        if (!api) {
                            return;
                        }
                        const nextValue = searchInput.value || '';
                        if (typeof api.setGridOption === 'function') {
                            api.setGridOption('quickFilterText', nextValue);
                        } else if (typeof api.updateGridOptions === 'function') {
                            api.updateGridOptions({ quickFilterText: nextValue });
                        } else if (typeof api.setQuickFilter === 'function') {
                            api.setQuickFilter(nextValue);
                        }
                    };
                    searchInput.addEventListener('input', applyQuickFilter);
                    requestAnimationFrame(applyQuickFilter);
                }
            }

            if (config.csvButtonId) {
                const csvButton = document.getElementById(config.csvButtonId);
                if (csvButton && !violitRuntime.markBound(csvButton, `ag-grid-csv-${config.csvButtonId}`)) {
                    csvButton.addEventListener('click', function() {
                        const api = getApi();
                        if (api && typeof api.exportDataAsCsv === 'function') {
                            api.exportDataAsCsv({ fileName: config.csvFileName || 'data.csv' });
                        }
                    });
                }
            }

            if (config.fullscreenButtonId) {
                const fullscreenButton = document.getElementById(config.fullscreenButtonId);
                if (fullscreenButton && !violitRuntime.markBound(fullscreenButton, `ag-grid-fullscreen-${config.fullscreenButtonId}`)) {
                    fullscreenButton.addEventListener('click', function() {
                        const target = document.getElementById(config.fullscreenTargetId || config.surfaceId);
                        if (!target) {
                            return;
                        }
                        if (document.fullscreenElement === target) {
                            if (document.exitFullscreen) {
                                document.exitFullscreen().catch(function() {});
                            }
                            return;
                        }
                        if (target.requestFullscreen) {
                            target.requestFullscreen().catch(function() {});
                        }
                    });
                }
            }
        };

        violitRuntime.registerInitializer('ag-grid-surface', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-ag-grid-config', null);
            if (!config) {
                return;
            }
            violitRuntime.bindAgGridSurface(config);
        });

        function applyCodeHighlight(root) {
            if (!root) {
                return;
            }
            root.querySelectorAll('pre code').forEach(function(block) {
                if (block.dataset.vlSyntaxHighlighting !== 'true') {
                    block.classList.add('nohighlight');
                    return;
                }
                if (block.dataset.highlighted) {
                    delete block.dataset.highlighted;
                }
                if (typeof hljs !== 'undefined') {
                    hljs.highlightElement(block);
                }
            });
        }

        function ensureKatexStylesheet() {
            if (document.getElementById('_vl_katex_css')) {
                return;
            }
            const link = document.createElement('link');
            link.id = '_vl_katex_css';
            link.rel = 'stylesheet';
            link.href = '/static/vendor/katex/katex.min.css';
            document.head.appendChild(link);
        }

        violitRuntime.registerInitializer('code-highlight', function(element) {
            if (!element || violitRuntime.markBound(element, `code-highlight-${element.id}`)) {
                return;
            }
            window._vlLoadLib('hljs', function() {
                applyCodeHighlight(element);
            });
        });

        violitRuntime.registerInitializer('katex-render', function(element) {
            const config = violitRuntime.readJsonAttr(element, 'data-vl-katex-config', null);
            if (!element || !config || typeof config.formula !== 'string') {
                return;
            }

            ensureKatexStylesheet();
            window._vlLoadLib('katex', function() {
                try {
                    katex.render(config.formula, element, {
                        throwOnError: false,
                        displayMode: config.displayMode !== false,
                    });
                } catch (error) {
                    element.textContent = config.formula;
                }
            });
        });

        window._vlHandleLiteSelectChange = async (element, cid) => {
            if (mode !== 'lite' || !element || !cid || typeof window.fetch !== 'function') {
                return;
            }
            await violitRuntime.postLiteAction(cid, element.value || '');
        };

        window._vlHandleLiteToggleChange = async (element, cid) => {
            if (mode !== 'lite' || !element || !cid || typeof window.fetch !== 'function') {
                return;
            }
            await violitRuntime.postLiteAction(cid, element.checked ? 'true' : 'false');
        };

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
                        if (!smartUpdated && targetId.endsWith('_wrapper') && currentRoot.querySelector('[data-chat-thread="true"]')) {
                            smartUpdated = trySmartUpdateChatThreadWrapper(currentRoot, incomingRoot);
                        }
                        if (!smartUpdated && targetId.endsWith('_wrapper') && currentRoot.querySelector('[data-vl-grid-config-hash]')) {
                            smartUpdated = trySmartUpdateAgGridWrapper(currentRoot, incomingRoot);
                        }
                        if (targetId.endsWith('_wrapper') && currentRoot.querySelector('.js-plotly-plot')) {
                            smartUpdated = trySmartUpdatePlotlyWrapper(currentRoot, incomingRoot.outerHTML);
                        }

                        if (!smartUpdated) {
                            const agGridScrollState = window._vlCaptureAgGridScroll
                                ? window._vlCaptureAgGridScroll(currentRoot)
                                : null;
                            preserveIncomingExpanderOpenState(currentRoot, incomingRoot);
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
            if (window.violitRuntime && typeof window.violitRuntime.scheduleScopeInit === 'function') {
                window.violitRuntime.scheduleScopeInit(document);
            }
            if (typeof hljs !== 'undefined') {
                document.querySelectorAll('.violit-code-block pre code:not(.hljs)').forEach(function(block) {
                    hljs.highlightElement(block);
                });
            }
        }
        function decodeBase64Utf8(value) {
            if (typeof value !== 'string' || !value) {
                return '';
            }

            try {
                const binary = atob(value);
                const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
                if (typeof TextDecoder !== 'undefined') {
                    return new TextDecoder('utf-8').decode(bytes);
                }
                return decodeURIComponent(Array.from(bytes, (byte) => `%${byte.toString(16).padStart(2, '0')}`).join(''));
            } catch (error) {
                debugLog('[stream-smooth] Failed to decode payload', error);
                return '';
            }
        }

        function applyVisualStreamSmoothing(scope) {
            const root = scope instanceof Element || scope instanceof Document ? scope : document;
            const matches = [];
            if (root instanceof Element && root.matches('[data-vl-stream-smooth="true"]')) {
                matches.push(root);
            }
            if (root.querySelectorAll) {
                root.querySelectorAll('[data-vl-stream-smooth="true"]').forEach((node) => matches.push(node));
            }

            window._vlVisualStreamState = window._vlVisualStreamState || {};
            const activeKeys = new Set();
            const resolveStreamSpeed = (rawValue) => {
                const numeric = Number(rawValue);
                if (!Number.isFinite(numeric)) {
                    return 7;
                }
                return Math.max(1, Math.min(10, Math.round(numeric)));
            };
            const resolveStepSize = (state, remaining) => {
                const desiredLength = (state.target || '').length;
                const speed = Number.isFinite(Number(state.speed)) ? Number(state.speed) : 7;
                const frameBudget = 10 + (speed * 10);
                const baseStep = Math.max(1, Math.ceil(Math.max(desiredLength, remaining) / frameBudget));
                return Math.min(remaining, baseStep);
            };

            const upsertHtmlSnapshot = (state, length, html) => {
                if (!state || !Number.isFinite(Number(length)) || length < 0 || !html) {
                    return;
                }
                const snapshotLength = Number(length);
                const existingSnapshots = Array.isArray(state.htmlSnapshots) ? state.htmlSnapshots : [];
                const filtered = existingSnapshots.filter((entry) => entry && Number.isFinite(Number(entry.length)) && Number(entry.length) <= snapshotLength);
                const sameIndex = filtered.findIndex((entry) => Number(entry.length) === snapshotLength);
                const nextEntry = { length: snapshotLength, html };
                if (sameIndex >= 0) {
                    filtered[sameIndex] = nextEntry;
                } else {
                    filtered.push(nextEntry);
                }
                filtered.sort((left, right) => Number(left.length) - Number(right.length));
                state.htmlSnapshots = filtered.slice(-120);
            };

            const resolveHtmlRenderPayload = (state) => {
                if (!state) {
                    return null;
                }
                const displayed = typeof state.displayed === 'string' ? state.displayed : '';
                const displayedLength = displayed.length;
                const snapshots = Array.isArray(state.htmlSnapshots) ? state.htmlSnapshots : [];
                let snapshot = null;
                for (let index = 0; index < snapshots.length; index += 1) {
                    const entry = snapshots[index];
                    if (!entry || !Number.isFinite(Number(entry.length))) {
                        continue;
                    }
                    if (Number(entry.length) <= displayedLength) {
                        snapshot = entry;
                        continue;
                    }
                    break;
                }
                if (!snapshot && state.liveHtml && displayedLength === (state.target || '').length) {
                    snapshot = { length: displayedLength, html: state.liveHtml };
                }
                if (!snapshot) {
                    return displayedLength > 0 ? { html: '', rawSuffix: displayed } : null;
                }
                const rawSuffix = displayedLength > Number(snapshot.length)
                    ? displayed.slice(Number(snapshot.length))
                    : '';
                return { html: snapshot.html || '', rawSuffix };
            };

            const renderHtmlState = (state, html, rawSuffix) => {
                state.live.style.whiteSpace = 'normal';
                state.live.innerHTML = html || '';
                if (rawSuffix) {
                    const suffixNode = document.createElement('span');
                    suffixNode.style.whiteSpace = 'pre-wrap';
                    suffixNode.textContent = rawSuffix;
                    state.live.appendChild(suffixNode);
                }
                if (!state.cursor) {
                    return;
                }
                const cursorNode = document.createElement('span');
                cursorNode.setAttribute('data-vl-stream-cursor-live', 'true');
                cursorNode.style.whiteSpace = 'pre-wrap';
                cursorNode.textContent = state.cursor;
                state.live.appendChild(cursorNode);
            };

            const syncClosestChatThreadBottom = (state) => {
                if (!state || !state.host || typeof state.host.closest !== 'function') {
                    return;
                }
                const thread = state.host.closest('[data-chat-thread="true"]');
                if (!thread) {
                    return;
                }
                if ((thread.getAttribute('data-chat-scroll-mode') || '').toLowerCase() !== 'bottom') {
                    return;
                }

                const syncBottom = () => {
                    const nextTop = Math.max(thread.scrollHeight - thread.clientHeight, 0);
                    thread.scrollTop = nextTop;
                    if (typeof thread.scrollTo === 'function') {
                        thread.scrollTo({ top: nextTop, behavior: 'auto' });
                    }
                };

                syncBottom();

                const frameKey = '__vlVisualStreamFollowFrame';
                if (thread[frameKey]) {
                    cancelAnimationFrame(thread[frameKey]);
                }
                thread[frameKey] = requestAnimationFrame(() => {
                    thread[frameKey] = 0;
                    syncBottom();
                });
            };

            const renderState = (state) => {
                if (!state || !state.live || !state.host || !state.host.isConnected) {
                    return;
                }
                if (state.finalHtml && state.displayed === (state.target || '')) {
                    state.live.style.whiteSpace = 'normal';
                    state.live.innerHTML = state.finalHtml;
                    syncClosestChatThreadBottom(state);
                    return;
                }
                const htmlPayload = resolveHtmlRenderPayload(state);
                if (htmlPayload) {
                    renderHtmlState(state, htmlPayload.html, htmlPayload.rawSuffix);
                    syncClosestChatThreadBottom(state);
                    return;
                }
                state.live.style.whiteSpace = 'pre-wrap';
                state.live.textContent = state.displayed + (state.cursor || '');
                syncClosestChatThreadBottom(state);
            };

            const scheduleState = (state) => {
                if (!state || state.raf) {
                    return;
                }

                const tick = () => {
                    state.raf = 0;
                    if (!state.host || !state.host.isConnected || !state.live) {
                        return;
                    }

                    const desired = state.target || '';
                    if (!desired.startsWith(state.displayed)) {
                        let prefix = 0;
                        const maxPrefix = Math.min(desired.length, state.displayed.length);
                        while (prefix < maxPrefix && desired[prefix] === state.displayed[prefix]) {
                            prefix += 1;
                        }
                        state.displayed = desired.slice(0, prefix);
                    }

                    const remaining = desired.length - state.displayed.length;
                    if (remaining > 0) {
                        const step = resolveStepSize(state, remaining);
                        state.displayed = desired.slice(0, state.displayed.length + step);
                        renderState(state);
                    } else {
                        renderState(state);
                        return;
                    }

                    if (state.displayed !== desired) {
                        state.raf = requestAnimationFrame(tick);
                    }
                };

                state.raf = requestAnimationFrame(tick);
            };

            matches.forEach((host, index) => {
                const key = host.getAttribute('data-vl-stream-key') || `stream:${index}`;
                activeKeys.add(key);

                const live = host.querySelector('[data-vl-stream-live="true"]') || host;
                const target = decodeBase64Utf8(host.getAttribute('data-vl-stream-target') || '');
                const cursor = host.getAttribute('data-vl-stream-cursor') || '';
                const liveHtml = decodeBase64Utf8(host.getAttribute('data-vl-stream-live-html') || '');
                const finalHtml = decodeBase64Utf8(host.getAttribute('data-vl-stream-final-html') || '');
                const speed = resolveStreamSpeed(host.getAttribute('data-vl-stream-speed'));
                const existing = window._vlVisualStreamState[key];
                const state = existing && typeof existing === 'object' ? existing : {};
                state.displayed = typeof state.displayed === 'string' ? state.displayed : '';
                state.target = target;
                state.cursor = cursor;
                state.liveHtml = liveHtml;
                state.finalHtml = finalHtml;
                state.speed = speed;
                state.host = host;
                state.live = live;
                state.raf = Number.isFinite(Number(state.raf)) ? Number(state.raf) : 0;

                if (state.liveHtml) {
                    upsertHtmlSnapshot(state, target.length, state.liveHtml);
                } else {
                    state.htmlSnapshots = [];
                }

                if (!target.startsWith(state.displayed)) {
                    let prefix = 0;
                    const maxPrefix = Math.min(target.length, state.displayed.length);
                    while (prefix < maxPrefix && target[prefix] === state.displayed[prefix]) {
                        prefix += 1;
                    }
                    state.displayed = target.slice(0, prefix);
                }

                window._vlVisualStreamState[key] = state;
                renderState(state);
                if (state.displayed !== state.target) {
                    scheduleState(state);
                }
            });

            Object.keys(window._vlVisualStreamState).forEach((key) => {
                if (activeKeys.has(key)) {
                    return;
                }
                const state = window._vlVisualStreamState[key];
                if (state && state.raf) {
                    cancelAnimationFrame(state.raf);
                }
                delete window._vlVisualStreamState[key];
            });
        }

        window._vlApplyVisualStreamSmoothing = applyVisualStreamSmoothing;

        function connectLiteStream() {
            if (mode !== 'lite' || typeof window.EventSource === 'undefined') return null;

            if (window._vlLiteStream) {
                try {
                    window._vlLiteStream.close();
                } catch (error) {
                    debugLog('[lite-stream] Failed to close previous EventSource', error);
                }
            }

            const streamUrl = buildAppUrl('/lite-stream');
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

            const preserve = new Set(['id', 'data-vl-ag-grid-mounted']);

            Array.from(target.getAttributeNames()).forEach((name) => {
                if (!preserve.has(name)) {
                    target.removeAttribute(name);
                }
            });

            Array.from(source.getAttributeNames()).forEach((name) => {
                if (!preserve.has(name)) {
                    target.setAttribute(name, source.getAttribute(name));
                }
            });
        }

        if (typeof window._vlFindAgGridViewport !== 'function') {
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
        }

        if (typeof window._vlCaptureAgGridScroll !== 'function') {
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
        }

        if (typeof window._vlHideAgGridDuringScrollRestore !== 'function') {
            window._vlHideAgGridDuringScrollRestore = (root, state) => {
                if (!root || !state || ((state.top || 0) === 0 && (state.left || 0) === 0)) {
                    return () => {};
                }

                return () => {};
            };
        }

        if (typeof window._vlRestoreAgGridScroll !== 'function') {
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
        }

        function getSingleAgGridMount(root) {
            if (!(root instanceof Element)) return null;

            const mounts = [];
            if (root.matches('[data-vl-grid-config-hash]')) {
                mounts.push(root);
            }
            root.querySelectorAll('[data-vl-grid-config-hash]').forEach((el) => mounts.push(el));

            return mounts.length === 1 ? mounts[0] : null;
        }

        function collectAgGridColumnIds(defs) {
            if (!Array.isArray(defs)) {
                return [];
            }

            return defs.reduce((acc, col) => {
                if (!col || typeof col !== 'object') {
                    return acc;
                }
                if (Array.isArray(col.children)) {
                    acc.push(...collectAgGridColumnIds(col.children));
                    return acc;
                }

                const columnId = String(col.colId ?? col.field ?? col.headerName ?? '').trim();
                if (columnId) {
                    acc.push(columnId);
                }
                return acc;
            }, []);
        }

        function extractArrayLiteralAfter(source, marker) {
            if (typeof source !== 'string' || !source || !marker) {
                return null;
            }

            const markerIndex = source.indexOf(marker);
            if (markerIndex === -1) {
                return null;
            }

            const start = source.indexOf('[', markerIndex + marker.length);
            if (start === -1) {
                return null;
            }

            let depth = 0;
            let inString = false;
            let stringQuote = '';
            let escaped = false;

            for (let index = start; index < source.length; index += 1) {
                const char = source[index];

                if (inString) {
                    if (escaped) {
                        escaped = false;
                        continue;
                    }
                    if (char === '\\') {
                        escaped = true;
                        continue;
                    }
                    if (char === stringQuote) {
                        inString = false;
                        stringQuote = '';
                    }
                    continue;
                }

                if (char === '"' || char === '\'' || char === '`') {
                    inString = true;
                    stringQuote = char;
                    continue;
                }

                if (char === '[') {
                    depth += 1;
                    continue;
                }

                if (char === ']') {
                    depth -= 1;
                    if (depth === 0) {
                        return source.slice(start, index + 1);
                    }
                }
            }

            return null;
        }

        function extractAgGridRowDataLiteral(source) {
            const legacyInitialRowDataPattern = /const initialRowData =\s*(\[.*?\]);/;
            const legacyMatch = source.match(legacyInitialRowDataPattern);
            if (legacyMatch && legacyMatch[1]) {
                return legacyMatch[1];
            }
            return extractArrayLiteralAfter(source, 'const initialRowData =') || extractArrayLiteralAfter(source, 'rowData:');
        }

        function extractAgGridColumnDefsLiteral(source) {
            return extractArrayLiteralAfter(source, 'const rawColumnDefs =') || extractArrayLiteralAfter(source, 'columnDefs:');
        }

        function trySmartUpdateAgGridWrapper(currentRoot, incomingMarkupOrRoot) {
            if (!currentRoot || !incomingMarkupOrRoot) return false;

            let nextRoot = incomingMarkupOrRoot;
            let incomingMarkup = '';

            if (typeof incomingMarkupOrRoot === 'string') {
                incomingMarkup = incomingMarkupOrRoot;
                const temp = document.createElement('div');
                temp.innerHTML = incomingMarkupOrRoot;
                nextRoot = temp.firstElementChild;
            } else {
                incomingMarkup = incomingMarkupOrRoot.outerHTML || '';
            }

            if (!(nextRoot instanceof Element) || currentRoot.id !== nextRoot.id) return false;

            const currentGridMount = getSingleAgGridMount(currentRoot);
            const nextGridMount = getSingleAgGridMount(nextRoot);
            if (!currentGridMount || !nextGridMount || !currentGridMount.id || currentGridMount.id !== nextGridMount.id) {
                return false;
            }

            const baseCid = currentGridMount.id;
            const gridApi = window['gridApi_' + baseCid];
            if (!gridApi) {
                return false;
            }

            const rowDataLiteral = extractAgGridRowDataLiteral(incomingMarkup);
            if (!rowDataLiteral) {
                return false;
            }

            const columnDefsLiteral = extractAgGridColumnDefsLiteral(incomingMarkup);

            try {
                const currentStyle = currentGridMount.getAttribute('style') || '';
                const nextStyle = nextGridMount.getAttribute('style') || '';
                if (currentStyle !== nextStyle) {
                    return false;
                }

                const currentConfigHash = currentGridMount.getAttribute('data-vl-grid-config-hash') || '';
                const nextConfigHash = nextGridMount.getAttribute('data-vl-grid-config-hash') || '';
                if (currentConfigHash !== nextConfigHash) {
                    return false;
                }

                const nextData = JSON.parse(rowDataLiteral);
                const nextColumnDefs = columnDefsLiteral ? JSON.parse(columnDefsLiteral) : [];
                const currentColumnIds = typeof gridApi.getColumnState === 'function'
                    ? gridApi.getColumnState().map((col) => String(col.colId || '').trim()).filter(Boolean)
                    : [];
                const currentSchema = currentColumnIds.length
                    ? currentColumnIds
                    : Array.from(currentGridMount.querySelectorAll('.ag-header-cell-text')).map((node) => (node.textContent || '').trim()).filter(Boolean);
                const nextColumnSchema = collectAgGridColumnIds(nextColumnDefs);
                const nextSchema = nextColumnSchema.length
                    ? nextColumnSchema
                    : (nextData.length
                        ? Object.keys(nextData[0]).map((key) => String(key).trim()).filter(Boolean)
                        : currentSchema);

                if (currentSchema.length !== nextSchema.length || currentSchema.some((text, index) => text !== nextSchema[index])) {
                    return false;
                }

                const agGridScrollState = window._vlCaptureAgGridScroll(currentGridMount);
                if (typeof gridApi.setGridOption === 'function') {
                    gridApi.setGridOption('rowData', nextData);
                } else if (typeof gridApi.setRowData === 'function') {
                    gridApi.setRowData(nextData);
                } else {
                    return false;
                }

                copyElementAttributes(currentRoot, nextRoot);
                copyElementAttributes(currentGridMount, nextGridMount);
                window._vlRestoreAgGridScroll(currentGridMount, agGridScrollState);
                return true;
            } catch (e) {
                console.error('Failed to smart update AG Grid wrapper:', e);
                return false;
            }
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

        function getSingleChatThread(root) {
            if (!root) return null;
            const matches = [];
            if (root instanceof Element && root.matches('[data-chat-thread="true"]')) {
                matches.push(root);
            }
            if (root.querySelectorAll) {
                root.querySelectorAll('[data-chat-thread="true"]').forEach((node) => matches.push(node));
            }
            return matches.length === 1 ? matches[0] : null;
        }

        function isChatMessageWrapper(node) {
            return !!(node instanceof Element && node.querySelector('[data-chat-message="true"]'));
        }

        function trySmartUpdateChatMessage(currentRoot, incomingMarkupOrRoot) {
            if (!currentRoot || !incomingMarkupOrRoot) return false;

            let nextRoot = null;
            if (typeof incomingMarkupOrRoot === 'string') {
                const temp = document.createElement('div');
                temp.innerHTML = incomingMarkupOrRoot;
                nextRoot = temp.firstElementChild;
            } else {
                nextRoot = incomingMarkupOrRoot;
            }

            if (!(nextRoot instanceof Element) || currentRoot.id !== nextRoot.id) return false;

            const currentMessage = currentRoot.querySelector('[data-chat-message="true"]');
            const nextMessage = nextRoot.querySelector('[data-chat-message="true"]');
            if (!(currentMessage instanceof Element) || !(nextMessage instanceof Element)) return false;

            const currentChatKey = currentMessage.getAttribute('data-chat-key') || '';
            const nextChatKey = nextMessage.getAttribute('data-chat-key') || '';
            if (currentChatKey && nextChatKey && currentChatKey !== nextChatKey) return false;

            copyElementAttributes(currentRoot, nextRoot);
            if (currentRoot.innerHTML !== nextRoot.innerHTML) {
                currentRoot.innerHTML = nextRoot.innerHTML;
            }
            executeInlineScripts(currentRoot);
            return true;
        }

        function trySmartUpdateChatThreadWrapper(currentRoot, incomingMarkupOrRoot) {
            if (!currentRoot || !incomingMarkupOrRoot) return false;

            let nextRoot = null;
            if (typeof incomingMarkupOrRoot === 'string') {
                const temp = document.createElement('div');
                temp.innerHTML = incomingMarkupOrRoot;
                nextRoot = temp.firstElementChild;
            } else {
                nextRoot = incomingMarkupOrRoot;
            }

            if (!(nextRoot instanceof Element) || currentRoot.id !== nextRoot.id) return false;

            const currentThread = getSingleChatThread(currentRoot);
            const nextThread = getSingleChatThread(nextRoot);
            if (!(currentThread instanceof Element) || !(nextThread instanceof Element)) return false;

            const currentChildren = Array.from(currentThread.children);
            const nextChildren = Array.from(nextThread.children);
            if (!currentChildren.every((child) => child.id) || !nextChildren.every((child) => child.id)) return false;

            copyElementAttributes(currentRoot, nextRoot);
            copyElementAttributes(currentThread, nextThread);

            const currentById = new Map(currentChildren.map((child) => [child.id, child]));
            const nextIds = nextChildren.map((child) => child.id);

            nextChildren.forEach((nextChild, index) => {
                let liveChild = currentById.get(nextChild.id) || null;
                const referenceNode = currentThread.children[index] || null;

                if (!liveChild) {
                    liveChild = nextChild.cloneNode(true);
                    currentThread.insertBefore(liveChild, referenceNode);
                    executeInlineScripts(liveChild);
                    currentById.set(nextChild.id, liveChild);
                    return;
                }

                if (currentThread.children[index] !== liveChild) {
                    currentThread.insertBefore(liveChild, referenceNode);
                }

                if (liveChild.outerHTML === nextChild.outerHTML) {
                    return;
                }

                if (isChatMessageWrapper(liveChild) && isChatMessageWrapper(nextChild)) {
                    if (!trySmartUpdateChatMessage(liveChild, nextChild)) {
                        liveChild.outerHTML = nextChild.outerHTML;
                        liveChild = document.getElementById(nextChild.id);
                    }
                } else {
                    liveChild.outerHTML = nextChild.outerHTML;
                    liveChild = document.getElementById(nextChild.id);
                }

                if (liveChild) {
                    executeInlineScripts(liveChild);
                    currentById.set(nextChild.id, liveChild);
                }
            });

            currentChildren.forEach((child) => {
                if (!nextIds.includes(child.id)) {
                    child.remove();
                }
            });

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

        const scheduleDocumentScopeInit = function() {
            if (window.violitRuntime && typeof window.violitRuntime.scheduleScopeInit === 'function') {
                window.violitRuntime.scheduleScopeInit(document);
            }
        };

        const initializeDomReadyRuntime = function() {
            syncSidebarWidthFromStorage();
            setupSidebarResizer();
            window._vlLoadLib('Plotly', setupPlotlyResizer);
            scheduleDocumentScopeInit();
        };

        // Initialize Resizer and custom element bindings once the DOM exists.
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeDomReadyRuntime, { once: true });
        } else {
            initializeDomReadyRuntime();
        }

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

                // Blank-hiding the grid during restore creates a more noticeable flicker
                // than the scroll correction itself when reactive wrappers are replaced.
                // Preserve the visible DOM and let scroll restoration happen in place.
                return () => {};
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

                window._pendingScrollRestore = captureViewportScroll();
                
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

                    const probeUrl = buildAppUrl('/__violit_boot');
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
                const wsUrl = new URL((location.protocol === 'https:' ? 'wss:' : 'ws:') + "//" + location.host + withRootPath('/ws'));
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

                                    if (!smartUpdated) {
                                        smartUpdated = trySmartUpdateCustomWidgetWrapper(el, item.html);
                                    }

                                    if (!smartUpdated && item.id.endsWith('_wrapper') && el.querySelector('[data-chat-thread="true"]')) {
                                        smartUpdated = trySmartUpdateChatThreadWrapper(el, item.html);
                                    }
                                    if (!smartUpdated && item.id.endsWith('_wrapper') && el.querySelector('[data-vl-grid-config-hash]')) {
                                        smartUpdated = trySmartUpdateAgGridWrapper(el, item.html);
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
                                            const columnDefsLiteral = extractAgGridColumnDefsLiteral(item.html);
                                            const rowDataLiteral = extractAgGridRowDataLiteral(item.html);
                                            const temp = document.createElement('div');
                                            temp.innerHTML = item.html;

                                            const currentGridRoot = document.getElementById(baseCid) || el.querySelector(`#${baseCid}`) || el;
                                            const nextGridRoot = temp.querySelector(`#${baseCid}`);
                                            let canSmartUpdate = !!(rowDataLiteral && currentGridRoot && nextGridRoot);

                                            if (canSmartUpdate) {
                                                const currentStyle = currentGridRoot.getAttribute('style') || '';
                                                const nextStyle = nextGridRoot.getAttribute('style') || '';
                                                if (currentStyle !== nextStyle) {
                                                    canSmartUpdate = false;
                                                }
                                            }

                                            if (canSmartUpdate) {
                                                const currentConfigHash = currentGridRoot.getAttribute('data-vl-grid-config-hash') || '';
                                                const nextConfigHash = nextGridRoot.getAttribute('data-vl-grid-config-hash') || '';
                                                if (currentConfigHash !== nextConfigHash) {
                                                    canSmartUpdate = false;
                                                }
                                            }

                                            if (canSmartUpdate) {
                                                try {
                                                    const nextData = JSON.parse(rowDataLiteral);
                                                    const nextColumnDefs = columnDefsLiteral ? JSON.parse(columnDefsLiteral) : [];
                                                    const currentColumnIds = typeof gridApi.getColumnState === 'function'
                                                        ? gridApi.getColumnState().map((col) => String(col.colId || '').trim()).filter(Boolean)
                                                        : [];
                                                    const currentSchema = currentColumnIds.length ? currentColumnIds : Array.from(currentGridRoot.querySelectorAll('.ag-header-cell-text')).map((node) => (node.textContent || '').trim()).filter(Boolean);
                                                    const nextColumnSchema = collectAgGridColumnIds(nextColumnDefs);
                                                    const nextSchema = nextColumnSchema.length
                                                        ? nextColumnSchema
                                                        : (nextData.length
                                                            ? Object.keys(nextData[0]).map((key) => String(key).trim()).filter(Boolean)
                                                            : currentSchema);
                                                    if (currentSchema.length !== nextSchema.length || currentSchema.some((text, index) => text !== nextSchema[index])) {
                                                        canSmartUpdate = false;
                                                    }
                                                } catch (e) {
                                                    canSmartUpdate = false;
                                                }
                                            }

                                            if (canSmartUpdate) {
                                                try {
                                                    const newData = JSON.parse(rowDataLiteral);
                                                    const agGridScrollState = window._vlCaptureAgGridScroll(currentGridRoot);

                                                    if (typeof gridApi.setGridOption === 'function') {
                                                        gridApi.setGridOption('rowData', newData);
                                                    } else if (typeof gridApi.setRowData === 'function') {
                                                        gridApi.setRowData(newData);
                                                    }

                                                    window._vlRestoreAgGridScroll(currentGridRoot, agGridScrollState);
                                                    smartUpdated = true;
                                                } catch (e) {
                                                    console.error('Failed to parse AG Grid data:', e);
                                                }
                                            } else if (typeof gridApi.destroy === 'function') {
                                                try {
                                                    gridApi.destroy();
                                                } catch (e) {
                                                    console.warn('Failed to destroy AG Grid before full replacement:', e);
                                                }
                                                delete window['gridApi_' + baseCid];
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
                                        const temp = document.createElement('div');
                                        temp.innerHTML = item.html;
                                        const nextRoot = temp.firstElementChild;
                                        if (nextRoot) {
                                            preserveIncomingExpanderOpenState(el, nextRoot);
                                        }
                                        purgePlotly(el);
                                        el.outerHTML = nextRoot ? temp.innerHTML : item.html;
                                        
                                        const newEl = document.getElementById(item.id);
                                        const revealGrid = window._vlHideAgGridDuringScrollRestore(newEl, agGridScrollState);
                                        window._vlRestoreAgGridScroll(newEl, agGridScrollState, revealGrid);
                                        
                                        // Execute scripts
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
                        if (window.violitRuntime && typeof window.violitRuntime.scheduleScopeInit === 'function') {
                            window.violitRuntime.scheduleScopeInit(document);
                        }
                        window._vlApplyPartBridge(document);
                        window._vlApplyVisualStreamSmoothing(document);

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
                    } else if (msg.type === 'client_commands') {
                        const commands = Array.isArray(msg.commands) ? msg.commands : [];
                        commands.forEach((command) => {
                            if (typeof window._vlExecuteClientCommand === 'function') {
                                window._vlExecuteClientCommand(command);
                            }
                        });
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
            const initializeLiteModeRuntime = () => {
                connectLiteStream();

                if (document.body && document.body.dataset.vlLiteRuntimeBound !== 'true') {
                    document.body.dataset.vlLiteRuntimeBound = 'true';

                    document.body.addEventListener('htmx:beforeSwap', function(evt) {
                        blurFocusedWaButtonHost();
                        if (evt.detail.target) {
                            purgePlotly(evt.detail.target);
                        }
                        if (typeof evt.detail.serverResponse === 'string' && evt.detail.serverResponse) {
                            evt.detail.serverResponse = preserveIncomingExpanderStatesInHtml(evt.detail.serverResponse);
                        }
                    });

                    // HTMX swaps can inject whole page/widget trees in lite mode.
                    // Re-run custom initializers so input-control bindings exist on the new DOM.
                    document.body.addEventListener('htmx:afterSettle', function() {
                        scheduleDocumentScopeInit();
                    });
                }
                
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
            };

            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeLiteModeRuntime, { once: true });
            } else {
                initializeLiteModeRuntime();
            }
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

        function closeDialogById(dialogId) {
            if (typeof dialogId !== 'string' || !dialogId) return;
            const dialog = document.getElementById(dialogId);
            if (!dialog) return;
            if (typeof dialog.requestClose === 'function') {
                dialog.requestClose();
                return;
            }
            if (dialog.dialog && typeof dialog.dialog.close === 'function') {
                dialog.dialog.close();
                return;
            }
            if (typeof dialog.hide === 'function') {
                dialog.hide();
                return;
            }
            dialog.open = false;
        }

        function runNavigateCommand(payload) {
            if (!payload || typeof payload !== 'object') return;
            if (payload.mode === 'hash') {
                const targetKey = typeof payload.targetKey === 'string' ? payload.targetKey : null;
                const targetHash = typeof payload.targetHash === 'string' ? payload.targetHash : '';
                window._pageScrollPositions = window._pageScrollPositions || {};
                if (window._currentPageKey) {
                    window._pageScrollPositions[window._currentPageKey] = window.scrollY;
                }
                if (targetKey) {
                    window._pendingPageKey = targetKey;
                    window._currentPageKey = targetKey;
                }
                window.location.hash = targetHash;
                if (targetKey) {
                    window.scrollTo(0, window._pageScrollPositions[targetKey] || 0);
                }
                return;
            }

            if (payload.mode === 'href' && typeof payload.url === 'string' && payload.url) {
                window.location.href = payload.url;
            }
        }

        function runDownloadCommand(payload) {
            if (!payload || typeof payload !== 'object') return;
            if (typeof payload.href !== 'string' || !payload.href) return;
            const link = document.createElement('a');
            link.href = payload.href;
            if (typeof payload.fileName === 'string' && payload.fileName) {
                link.download = payload.fileName;
            }
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function executeClientCommand(command) {
            if (!command || typeof command !== 'object') return false;
            const name = typeof command.name === 'string' ? command.name : '';
            const payload = command.payload && typeof command.payload === 'object' ? command.payload : {};

            if (name === 'toast.show') {
                createToast(String(payload.message || ''), String(payload.variant || 'primary'), String(payload.icon || 'circle-info'));
                return true;
            }

            if (name === 'effect.play') {
                if (payload.effect === 'balloons') {
                    createBalloons();
                    return true;
                }
                if (payload.effect === 'snow') {
                    createSnow();
                    return true;
                }
                return false;
            }

            if (name === 'interval.start') {
                if (typeof payload.id !== 'string' || typeof payload.ms !== 'number') {
                    return false;
                }
                window._vlCreateInterval(payload.id, payload.ms, !!payload.autostart);
                return true;
            }

            if (name === 'dialog.close') {
                closeDialogById(String(payload.id || ''));
                return true;
            }

            if (name === 'navigate') {
                runNavigateCommand(payload);
                return true;
            }

            if (name === 'download.start') {
                runDownloadCommand(payload);
                return true;
            }

            return false;
        }

        window._vlExecuteClientCommand = executeClientCommand;
        
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
        
        const handleBrowserHistoryNavigation = () => {
            if (window._suppressHashRestoreOnce) {
                window._suppressHashRestoreOnce = false;
                return;
            }
            if (mode === 'ws' && !window._wsReady) {
                return;
            }
            setTimeout(restoreFromHash, 40);
        };

        // Note: For ws mode, restoreFromHash is called from ws.onopen.
        // For lite mode, call it on load and also react to later hash changes.
        if (mode !== 'ws') {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => setTimeout(restoreFromHash, 200));
            } else {
                setTimeout(restoreFromHash, 200);
            }
        } else {
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {
                    window._vlLastHiddenAt = Date.now();
                    return;
                }
                if (document.visibilityState === 'visible') {
                    window._vlHandleResume('visibilitychange');
                }
            });
        }

        window.addEventListener('hashchange', handleBrowserHistoryNavigation);
        window.addEventListener('popstate', handleBrowserHistoryNavigation);
        if (mode === 'ws') {
            window.addEventListener('focus', () => window._vlHandleResume('focus'));
            window.addEventListener('online', () => window._vlHandleResume('online'));
            window.addEventListener('pageshow', () => window._vlHandleResume('pageshow'));
            document.addEventListener('pointerdown', () => window._vlRevivePageOnInteraction('pointerdown'), { passive: true, capture: true });
            document.addEventListener('touchstart', () => window._vlRevivePageOnInteraction('touchstart'), { passive: true, capture: true });
            document.addEventListener('keydown', () => window._vlRevivePageOnInteraction('keydown'), { passive: true, capture: true });
        }