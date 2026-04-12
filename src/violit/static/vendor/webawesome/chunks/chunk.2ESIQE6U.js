/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  zoomable_frame_styles_default
} from "./chunk.GRV2ULZ4.js";
import {
  parseSpaceDelimitedTokens
} from "./chunk.RMZ7BVDM.js";
import {
  o as o2
} from "./chunk.3MSWQ3RG.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  WebAwesomeElement,
  e,
  n,
  t
} from "./chunk.K4C5PQDP.js";
import {
  o
} from "./chunk.7OBLIRXR.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/internal/color-scheme-controller.ts
var ColorSchemeController = class {
  constructor(host, onThemeChange) {
    this.handleTransitionEnd = () => {
      this.onThemeChange();
    };
    (this.host = host).addController(this);
    this.onThemeChange = onThemeChange;
    this.hiddenElement = document.createElement("div");
    this.hiddenElement.setAttribute("aria-hidden", "true");
    Object.assign(this.hiddenElement.style, {
      position: "absolute",
      width: "0",
      height: "0",
      overflow: "hidden",
      pointerEvents: "none",
      opacity: "0",
      // Transition on a WA surface token — changes whenever the theme class changes
      color: "var(--wa-color-surface-default, transparent)",
      transition: "color 0.001ms"
    });
  }
  hostConnected() {
    this.host.appendChild(this.hiddenElement);
    this.hiddenElement.addEventListener("transitionend", this.handleTransitionEnd);
  }
  hostDisconnected() {
    this.hiddenElement.removeEventListener("transitionend", this.handleTransitionEnd);
    this.hiddenElement.remove();
  }
};

// src/components/zoomable-frame/zoomable-frame.ts
var WaZoomableFrame = class extends WebAwesomeElement {
  constructor() {
    super();
    this.localize = new LocalizeController(this);
    this.availableZoomLevels = [];
    // SSR guard: MutationObserver is not available during server-side rendering
    this.themeObserver = !o ? new MutationObserver(() => this.syncTheme()) : null;
    this.allowfullscreen = false;
    this.loading = "eager";
    this.zoom = 1;
    this.zoomLevels = "25% 50% 75% 100% 125% 150% 175% 200%";
    this.withoutControls = false;
    this.withoutInteraction = false;
    this.withThemeSync = false;
    new ColorSchemeController(this, () => this.syncTheme());
  }
  /** Returns the internal iframe's `window` object. (Readonly property) */
  get contentWindow() {
    return this.iframe?.contentWindow || null;
  }
  /** Returns the internal iframe's `document` object. (Readonly property) */
  get contentDocument() {
    return this.iframe?.contentDocument || null;
  }
  parseZoomLevels(zoomLevelsString) {
    const tokens = parseSpaceDelimitedTokens(zoomLevelsString);
    const levels = [];
    for (const token of tokens) {
      let value;
      if (token.endsWith("%")) {
        const percentage = parseFloat(token.slice(0, -1));
        if (!isNaN(percentage)) {
          value = Math.max(0, percentage / 100);
        } else {
          continue;
        }
      } else {
        value = parseFloat(token);
        if (!isNaN(value)) {
          value = Math.max(0, value);
        } else {
          continue;
        }
      }
      levels.push(value);
    }
    return [...new Set(levels)].sort((a, b) => a - b);
  }
  getCurrentZoomIndex() {
    if (this.availableZoomLevels.length === 0) return -1;
    let closestIndex = 0;
    let closestDiff = Math.abs(this.availableZoomLevels[0] - this.zoom);
    for (let i = 1; i < this.availableZoomLevels.length; i++) {
      const diff = Math.abs(this.availableZoomLevels[i] - this.zoom);
      if (diff < closestDiff) {
        closestDiff = diff;
        closestIndex = i;
      }
    }
    return closestIndex;
  }
  isZoomInDisabled() {
    if (this.availableZoomLevels.length === 0) return false;
    const currentIndex = this.getCurrentZoomIndex();
    return currentIndex >= this.availableZoomLevels.length - 1;
  }
  isZoomOutDisabled() {
    if (this.availableZoomLevels.length === 0) return false;
    const currentIndex = this.getCurrentZoomIndex();
    return currentIndex <= 0;
  }
  updated(changedProperties) {
    if (changedProperties.has("zoom")) {
      this.style.setProperty("--zoom", `${this.zoom}`);
    }
    if (changedProperties.has("zoomLevels")) {
      this.availableZoomLevels = this.parseZoomLevels(this.zoomLevels);
      if (this.availableZoomLevels.length > 0) {
        const currentIndex = this.getCurrentZoomIndex();
        if (Math.abs(this.availableZoomLevels[currentIndex] - this.zoom) > 1e-3) {
          this.zoom = this.availableZoomLevels[currentIndex];
        }
      }
    }
    if (changedProperties.has("withThemeSync")) {
      if (this.withThemeSync) {
        this.themeObserver?.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
        this.syncTheme();
      } else {
        this.themeObserver?.disconnect();
      }
    }
  }
  /** Zooms in to the next available zoom level. */
  zoomIn() {
    if (this.availableZoomLevels.length === 0) {
      this.zoom = Math.min(this.zoom + 0.05, 2);
      return;
    }
    const currentIndex = this.getCurrentZoomIndex();
    if (currentIndex < this.availableZoomLevels.length - 1) {
      this.zoom = this.availableZoomLevels[currentIndex + 1];
    }
  }
  /** Zooms out to the previous available zoom level. */
  zoomOut() {
    if (this.availableZoomLevels.length === 0) {
      this.zoom = Math.max(this.zoom - 0.05, 0);
      return;
    }
    const currentIndex = this.getCurrentZoomIndex();
    if (currentIndex > 0) {
      this.zoom = this.availableZoomLevels[currentIndex - 1];
    }
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.themeObserver?.disconnect();
  }
  syncTheme() {
    if (!this.withThemeSync) return;
    try {
      const iframeRoot = this.contentDocument?.documentElement;
      if (!iframeRoot) return;
      const prefixes = ["wa-theme-", "wa-brand-", "wa-palette-"];
      const schemeCls = /* @__PURE__ */ new Set();
      const themeCls = /* @__PURE__ */ new Set();
      let el = this;
      let schemeFound = false;
      while (el) {
        if (!schemeFound) {
          if (el.classList.contains("wa-dark")) {
            schemeCls.add("wa-dark");
            schemeFound = true;
          } else if (el.classList.contains("wa-light")) {
            schemeCls.add("wa-light");
            schemeFound = true;
          }
        }
        for (const cls of el.classList) {
          if (prefixes.some((p) => cls.startsWith(p))) themeCls.add(cls);
        }
        el = el.parentElement;
      }
      iframeRoot.classList.toggle("wa-dark", schemeCls.has("wa-dark"));
      iframeRoot.classList.toggle("wa-light", schemeCls.has("wa-light"));
      const toRemove = Array.from(iframeRoot.classList).filter((c) => prefixes.some((p) => c.startsWith(p)));
      iframeRoot.classList.remove(...toRemove);
      iframeRoot.classList.add(...themeCls);
    } catch {
    }
  }
  handleLoad() {
    if (this.withThemeSync) this.syncTheme();
    this.dispatchEvent(new Event("load", { bubbles: false, cancelable: false, composed: true }));
  }
  handleError() {
    this.dispatchEvent(new Event("error", { bubbles: false, cancelable: false, composed: true }));
  }
  render() {
    return x`
      <div id="frame-container">
        <iframe
          id="iframe"
          part="iframe"
          ?inert=${this.withoutInteraction}
          ?allowfullscreen=${this.allowfullscreen}
          loading=${this.loading}
          referrerpolicy=${this.referrerpolicy}
          sandbox=${o2(this.sandbox ?? void 0)}
          src=${o2(this.src ?? void 0)}
          srcdoc=${o2(this.srcdoc ?? void 0)}
          @load=${this.handleLoad}
          @error=${this.handleError}
        ></iframe>
      </div>

      ${!this.withoutControls ? x`
            <div id="controls" part="controls">
              <button
                part="zoom-out-button"
                aria-label=${this.localize.term("zoomOut")}
                @click=${this.zoomOut}
                ?disabled=${this.isZoomOutDisabled()}
              >
                <slot name="zoom-out-icon">
                  <wa-icon name="minus" label="Zoom out"></wa-icon>
                </slot>
              </button>
              <span>${this.localize.number(this.zoom, { style: "percent", maximumFractionDigits: 1 })}</span>
              <button
                part="zoom-in-button"
                aria-label=${this.localize.term("zoomIn")}
                @click=${this.zoomIn}
                ?disabled=${this.isZoomInDisabled()}
              >
                <slot name="zoom-in-icon">
                  <wa-icon name="plus" label="Zoom in"></wa-icon>
                </slot>
              </button>
            </div>
          ` : ""}
    `;
  }
};
WaZoomableFrame.css = zoomable_frame_styles_default;
__decorateClass([
  e("#iframe")
], WaZoomableFrame.prototype, "iframe", 2);
__decorateClass([
  n()
], WaZoomableFrame.prototype, "src", 2);
__decorateClass([
  n()
], WaZoomableFrame.prototype, "srcdoc", 2);
__decorateClass([
  n({ type: Boolean })
], WaZoomableFrame.prototype, "allowfullscreen", 2);
__decorateClass([
  n()
], WaZoomableFrame.prototype, "loading", 2);
__decorateClass([
  n()
], WaZoomableFrame.prototype, "referrerpolicy", 2);
__decorateClass([
  n()
], WaZoomableFrame.prototype, "sandbox", 2);
__decorateClass([
  n({ type: Number, reflect: true })
], WaZoomableFrame.prototype, "zoom", 2);
__decorateClass([
  n({ attribute: "zoom-levels" })
], WaZoomableFrame.prototype, "zoomLevels", 2);
__decorateClass([
  n({ type: Boolean, attribute: "without-controls", reflect: true })
], WaZoomableFrame.prototype, "withoutControls", 2);
__decorateClass([
  n({ type: Boolean, attribute: "without-interaction", reflect: true })
], WaZoomableFrame.prototype, "withoutInteraction", 2);
__decorateClass([
  n({ type: Boolean, attribute: "with-theme-sync", reflect: true })
], WaZoomableFrame.prototype, "withThemeSync", 2);
WaZoomableFrame = __decorateClass([
  t("wa-zoomable-frame")
], WaZoomableFrame);

export {
  WaZoomableFrame
};
