/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  scroller_styles_default
} from "./chunk.A4KPVHRW.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  WebAwesomeElement,
  e,
  n,
  r,
  t,
  t2
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

// src/components/scroller/scroller.ts
var WaScroller = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.resizeObserver = null;
    this.canScroll = false;
    this.orientation = "horizontal";
    this.withoutScrollbar = false;
    this.withoutShadow = false;
  }
  connectedCallback() {
    super.connectedCallback();
    if (!o) {
      this.resizeObserver = new ResizeObserver(() => this.updateScroll());
      this.resizeObserver.observe(this);
    }
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.resizeObserver?.disconnect();
  }
  handleKeyDown(event) {
    if (event.key === "Home") {
      event.preventDefault();
      this.content.scrollTo({
        left: this.orientation === "horizontal" ? 0 : void 0,
        top: this.orientation === "vertical" ? 0 : void 0
      });
    }
    if (event.key === "End") {
      event.preventDefault();
      this.content.scrollTo({
        left: this.orientation === "horizontal" ? this.content.scrollWidth : void 0,
        top: this.orientation === "vertical" ? this.content.scrollHeight : void 0
      });
    }
  }
  handleSlotChange() {
    this.updateScroll();
  }
  updateScroll() {
    if (this.orientation === "horizontal") {
      const clientWidth = Math.ceil(this.content.clientWidth);
      const scrollLeft = Math.abs(Math.ceil(this.content.scrollLeft));
      const scrollWidth = Math.ceil(this.content.scrollWidth);
      const maxScroll = scrollWidth - clientWidth;
      this.canScroll = maxScroll > 0;
      const startShadowOpacity = Math.min(1, scrollLeft / (maxScroll * 0.05));
      const endShadowOpacity = Math.min(1, (maxScroll - scrollLeft) / (maxScroll * 0.05));
      this.style.setProperty("--start-shadow-opacity", String(startShadowOpacity || 0));
      this.style.setProperty("--end-shadow-opacity", String(endShadowOpacity || 0));
    } else {
      const clientHeight = Math.ceil(this.content.clientHeight);
      const scrollTop = Math.abs(Math.ceil(this.content.scrollTop));
      const scrollHeight = Math.ceil(this.content.scrollHeight);
      const maxScroll = scrollHeight - clientHeight;
      this.canScroll = maxScroll > 0;
      const startShadowOpacity = Math.min(1, scrollTop / (maxScroll * 0.05));
      const endShadowOpacity = Math.min(1, (maxScroll - scrollTop) / (maxScroll * 0.05));
      this.style.setProperty("--start-shadow-opacity", String(startShadowOpacity || 0));
      this.style.setProperty("--end-shadow-opacity", String(endShadowOpacity || 0));
    }
  }
  render() {
    return x`
      ${this.withoutShadow ? "" : x`
            <div id="start-shadow" part="start-shadow" aria-hidden="true"></div>
            <div id="end-shadow" part="end-shadow" aria-hidden="true"></div>
          `}

      <div
        id="content"
        part="content"
        role="region"
        aria-label=${this.localize.term("scrollableRegion")}
        aria-orientation=${this.orientation}
        tabindex=${this.canScroll ? "0" : "-1"}
        @keydown=${this.handleKeyDown}
        @scroll=${this.updateScroll}
      >
        <slot @slotchange=${this.handleSlotChange}></slot>
      </div>
    `;
  }
};
WaScroller.css = [scroller_styles_default];
__decorateClass([
  e("#content")
], WaScroller.prototype, "content", 2);
__decorateClass([
  r()
], WaScroller.prototype, "canScroll", 2);
__decorateClass([
  n({ reflect: true })
], WaScroller.prototype, "orientation", 2);
__decorateClass([
  n({ attribute: "without-scrollbar", type: Boolean, reflect: true })
], WaScroller.prototype, "withoutScrollbar", 2);
__decorateClass([
  n({ attribute: "without-shadow", type: Boolean, reflect: true })
], WaScroller.prototype, "withoutShadow", 2);
__decorateClass([
  t2({ passive: true })
], WaScroller.prototype, "updateScroll", 1);
WaScroller = __decorateClass([
  t("wa-scroller")
], WaScroller);

export {
  WaScroller
};
