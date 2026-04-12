/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o as o2
} from "./chunk.2BXLTQVW.js";
import {
  page_mobile_styles_default
} from "./chunk.WKX3BKNK.js";
import {
  page_styles_default
} from "./chunk.2MOO23UE.js";
import {
  visually_hidden_styles_default
} from "./chunk.I4KXAHPX.js";
import {
  l
} from "./chunk.KZZR6Z6I.js";
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

// src/components/page/page.ts
function toPx(value, element = document.documentElement) {
  if (!Number.isNaN(Number(value))) {
    return Number(value);
  }
  if (!window.CSS || !CSS.registerProperty) {
    if (typeof value === "string" && value.endsWith("px")) {
      return parseFloat(value);
    }
    return Number(value) || 0;
  }
  const resolver = "--wa-length-resolver";
  if (!CSS.registerProperty.toString().includes(resolver)) {
    try {
      CSS.registerProperty({
        name: resolver,
        syntax: "<length>",
        inherits: false,
        initialValue: "0px"
      });
    } catch (e2) {
    }
  }
  const previousValue = element.style.getPropertyValue(resolver);
  element.style.setProperty(resolver, value);
  const computedValue = getComputedStyle(element)?.getPropertyValue(resolver);
  element.style.setProperty(resolver, previousValue);
  if (computedValue?.endsWith("px")) {
    return parseFloat(computedValue);
  }
  return Number(computedValue) || 0;
}
function toLength(px) {
  return Number.isNaN(Number(px)) ? px : `${px}px`;
}
var WaPage = class extends WebAwesomeElement {
  constructor() {
    super();
    // SSR guard: ResizeObserver is not available during server-side rendering
    this.headerResizeObserver = !o ? this.slotResizeObserver("header") : null;
    this.subheaderResizeObserver = !o ? this.slotResizeObserver("subheader") : null;
    this.bannerResizeObserver = !o ? this.slotResizeObserver("banner") : null;
    this.footerResizeObserver = !o ? this.slotResizeObserver("footer") : null;
    this.handleNavigationToggle = (e2) => {
      if (this.view === "desktop") {
        this.hideNavigation();
        return;
      }
      const path = e2.composedPath();
      const navigationToggleSlot = this.navigationToggleSlot;
      if (path.find((el) => {
        return el.hasAttribute?.("data-toggle-nav") || el.assignedSlot === navigationToggleSlot || el === navigationToggleSlot;
      })) {
        e2.preventDefault();
        this.toggleNavigation();
      }
    };
    this.view = "desktop";
    this.navOpen = false;
    this.mobileBreakpoint = "768px";
    this.navigationPlacement = "start";
    this.disableNavigationToggle = false;
    this.pageResizeObserver = !o ? new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentBoxSize) {
          const contentBoxSize = entry.borderBoxSize[0];
          const pageWidth = contentBoxSize.inlineSize;
          const oldView = this.view;
          if (pageWidth >= toPx(this.mobileBreakpoint)) {
            this.view = "desktop";
          } else {
            this.view = "mobile";
          }
          this.requestUpdate("view", oldView);
        }
      }
      if (entries.length > 0) {
        this.updateAsideAndMenuHeights();
      }
    }) : null;
    this.updateNavigationToggleState = (e2) => {
      if (e2) {
        const slotName = e2.target.name;
        if (!["navigation", "navigation-header", "navigation-footer"].includes(slotName)) return;
      }
      const hasCustomToggle = Boolean(this.querySelector(":not([slot='toggle-navigation']) [data-toggle-nav]"));
      const hasNavigationContent = Boolean(this.querySelector('[slot="navigation"]')) || Boolean(this.querySelector('[slot="navigation-header"]')) || Boolean(this.querySelector('[slot="navigation-footer"]'));
      this.disableNavigationToggle = hasCustomToggle || !hasNavigationContent;
    };
    this.updateAsideAndMenuHeights = () => {
      const visiblePixels = this.visiblePixelsInViewport(this.main);
      if (visiblePixels == null) {
        return;
      }
      this.aside.style.setProperty("--main-height", `${visiblePixels}px`);
      this.menu.style.setProperty("--main-height", `${visiblePixels}px`);
    };
    if (!o) {
      this.addEventListener("click", this.handleNavigationToggle);
    }
  }
  slotResizeObserver(slot) {
    return new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentBoxSize) {
          const contentBoxSize = entry.borderBoxSize[0];
          this.style.setProperty(`--${slot}-height`, `${contentBoxSize.blockSize}px`);
        }
      }
    });
  }
  update(changedProperties) {
    if (changedProperties.has("view")) {
      this.hideNavigation();
    }
    super.update(changedProperties);
  }
  connectedCallback() {
    super.connectedCallback();
    if (!o) {
      this.pageResizeObserver?.observe(this);
      document.addEventListener("scroll", this.updateAsideAndMenuHeights, { passive: true });
      this.updateAsideAndMenuHeights();
      setTimeout(this.updateAsideAndMenuHeights);
      setTimeout(() => {
        this.headerResizeObserver?.observe(this.header);
        this.subheaderResizeObserver?.observe(this.subheader);
        this.bannerResizeObserver?.observe(this.banner);
        this.footerResizeObserver?.observe(this.footer);
      });
    }
  }
  /**
   * https://stackoverflow.com/a/26831113
   * This prevents awkward gaps when scrolling the page and the aside / menu dont "fill" the gaps.
   */
  visiblePixelsInViewport(element) {
    if (!element) {
      return null;
    }
    const elementHeight = element.clientHeight;
    const windowHeight = window.innerHeight;
    const { top, bottom } = element.getBoundingClientRect();
    return Math.max(0, top > 0 ? Math.min(elementHeight, windowHeight - top) : Math.min(bottom, windowHeight));
  }
  firstUpdated() {
    if (!document.getElementById("main-content")) {
      const div = document.createElement("div");
      div.id = "main-content";
      div.slot = "skip-to-content-target";
      this.prepend(div);
    }
    this.shadowRoot.addEventListener("slotchange", this.updateNavigationToggleState);
    this.updateNavigationToggleState();
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.pageResizeObserver?.unobserve(this);
    this.headerResizeObserver?.unobserve(this.header);
    this.subheaderResizeObserver?.unobserve(this.subheader);
    this.footerResizeObserver?.unobserve(this.footer);
    this.bannerResizeObserver?.unobserve(this.banner);
    document.removeEventListener("scroll", this.updateAsideAndMenuHeights);
  }
  /**
   * Shows the mobile navigation drawer
   */
  showNavigation() {
    this.navOpen = true;
  }
  /**
   * Hides the mobile navigation drawer
   */
  hideNavigation() {
    this.navOpen = false;
  }
  /**
   * Toggles the mobile navigation drawer
   */
  toggleNavigation() {
    this.navOpen = !this.navOpen;
  }
  render() {
    return x`
      <a href="#main-content" part="skip-to-content" class="wa-visually-hidden">
        <slot name="skip-to-content">Skip to content</slot>
      </a>

      <!-- unsafeHTML needed for SSR until this is solved: https://github.com/lit/lit/issues/4696 -->
      ${o2(`
        <style id="mobile-styles">
          ${page_mobile_styles_default(toLength(this.mobileBreakpoint))}
        </style>
      `)}

      <div class="base" part="base">
        <div class="banner" part="banner">
          <slot name="banner"></slot>
        </div>
        <div class="header" part="header">
          <slot name="navigation-toggle">
            <wa-button part="navigation-toggle" size="small" appearance="plain" variant="neutral">
              <slot name="navigation-toggle-icon">
                <wa-icon name="bars" part="navigation-toggle-icon" label="Toggle navigation drawer"></wa-icon>
              </slot>
            </wa-button>
          </slot>
          <slot name="header"></slot>
        </div>
        <div class="subheader" part="subheader">
          <slot name="subheader"></slot>
        </div>
        <div class="body" part="body">
          <div class="menu" part="menu">
            <slot name="menu">
              <nav name="navigation" class="navigation" part="navigation navigation-desktop">
                <!-- Add fallback divs so that CSS grid works properly. -->
                <slot name="desktop-navigation-header">
                  <slot name=${this.view === "desktop" ? "navigation-header" : "___"}><div></div></slot>
                </slot>
                <slot name="desktop-navigation">
                  <slot name=${this.view === "desktop" ? "navigation" : "____"}><div></div></slot>
                </slot>
                <slot name="desktop-navigation-footer">
                  <slot name=${this.view === "desktop" ? "navigation-footer" : "___"}><div></div></slot>
                </slot>
              </nav>
            </slot>
          </div>
          <div class="main" part="main">
            <div class="main-header" part="main-header">
              <slot name="main-header"></slot>
            </div>
            <div class="main-content" part="main-content">
              <slot name="skip-to-content-target"></slot>
              <slot></slot>
            </div>
            <div class="main-footer" part="main-footer">
              <slot name="main-footer"></slot>
            </div>
          </div>
          <div class="aside" part="aside">
            <slot name="aside"></slot>
          </div>
        </div>
        <div class="footer" part="footer">
          <slot name="footer"></slot>
        </div>
      </div>
      <wa-drawer
        part="drawer"
        placement=${this.navigationPlacement}
        light-dismiss
        ?open=${l(this.navOpen)}
        @wa-after-show=${() => this.navOpen = this.navigationDrawer.open}
        @wa-after-hide=${() => this.navOpen = this.navigationDrawer.open}
        exportparts="
          dialog:drawer__dialog,
          overlay:drawer__overlay,
          panel:drawer__panel,
          header:drawer__header,
          header-actions:drawer__header-actions,
          title:drawer__title,
          close-button:drawer__close-button,
          close-button__base:drawer__close-button__base,
          body:drawer__body,
          footer:drawer__footer
        "
        class="navigation-drawer"
      >
        <slot slot="label" part="navigation-header" name="mobile-navigation-header">
          <slot name=${this.view === "mobile" ? "navigation-header" : "___"}></slot>
        </slot>
        <slot name="mobile-navigation">
          <slot name=${this.view === "mobile" ? "navigation" : "____"}></slot>
        </slot>

        <slot slot="footer" name="mobile-navigation-footer">
          <slot part="navigation-footer" name=${this.view === "mobile" ? "navigation-footer" : "___"}></slot>
        </slot>
      </wa-drawer>
    `;
  }
};
WaPage.css = [visually_hidden_styles_default, page_styles_default];
__decorateClass([
  e("[part~='header']")
], WaPage.prototype, "header", 2);
__decorateClass([
  e("[part~='menu']")
], WaPage.prototype, "menu", 2);
__decorateClass([
  e("[part~='main']")
], WaPage.prototype, "main", 2);
__decorateClass([
  e("[part~='aside']")
], WaPage.prototype, "aside", 2);
__decorateClass([
  e("[part~='subheader']")
], WaPage.prototype, "subheader", 2);
__decorateClass([
  e("[part~='footer']")
], WaPage.prototype, "footer", 2);
__decorateClass([
  e("[part~='banner']")
], WaPage.prototype, "banner", 2);
__decorateClass([
  e("[part~='drawer']")
], WaPage.prototype, "navigationDrawer", 2);
__decorateClass([
  e("slot[name~='navigation-toggle']")
], WaPage.prototype, "navigationToggleSlot", 2);
__decorateClass([
  n({ attribute: "view", reflect: true })
], WaPage.prototype, "view", 2);
__decorateClass([
  n({ attribute: "nav-open", reflect: true, type: Boolean })
], WaPage.prototype, "navOpen", 2);
__decorateClass([
  n({ attribute: "mobile-breakpoint", type: String })
], WaPage.prototype, "mobileBreakpoint", 2);
__decorateClass([
  n({ attribute: "navigation-placement", reflect: true })
], WaPage.prototype, "navigationPlacement", 2);
__decorateClass([
  n({ attribute: "disable-navigation-toggle", reflect: true, type: Boolean })
], WaPage.prototype, "disableNavigationToggle", 2);
WaPage = __decorateClass([
  t("wa-page")
], WaPage);
if (typeof CSSStyleSheet !== "undefined" && typeof document !== "undefined" && "adoptedStyleSheets" in document) {
  const stylesheet = new CSSStyleSheet();
  stylesheet.replaceSync(`
  :is(html, body):has(wa-page) {
    min-height: 100%;
    padding: 0;
    margin: 0;
  }

    /**
    Because headers are sticky, this is needed to make sure page fragment anchors scroll down past the headers / subheaders and are visible.
    IE: \`<a href="#id-for-h2">\` anchors.
    */
    wa-page :is(*, *:after, *:before) {
    scroll-margin-top: var(--scroll-margin-top);
    }

    wa-page[view='desktop'] [data-toggle-nav] {
    display: none;
    }

    wa-page[view='mobile'] .wa-desktop-only, wa-page[view='desktop'] .wa-mobile-only {
    display: none !important;
    }
  `);
  document.adoptedStyleSheets = [...document.adoptedStyleSheets, stylesheet];
}

export {
  WaPage
};
