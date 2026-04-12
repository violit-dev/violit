/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  split_panel_styles_default
} from "./chunk.UF4WDITO.js";
import {
  drag
} from "./chunk.WYNTFJHW.js";
import {
  WaRepositionEvent
} from "./chunk.ZWQCGLB5.js";
import {
  clamp
} from "./chunk.O6IZ4I7T.js";
import {
  o as o2
} from "./chunk.3MSWQ3RG.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
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

// src/components/split-panel/split-panel.ts
var WaSplitPanel = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.isCollapsed = false;
    this.localize = new LocalizeController(this);
    this.positionBeforeCollapsing = 0;
    this.position = 50;
    this.orientation = "horizontal";
    this.disabled = false;
    this.snapThreshold = 12;
  }
  connectedCallback() {
    super.connectedCallback();
    if (!o) {
      this.resizeObserver = new ResizeObserver((entries) => this.handleResize(entries));
      this.updateComplete.then(() => this.resizeObserver.observe(this));
      this.detectSize();
      this.cachedPositionInPixels = this.percentageToPixels(this.position);
    }
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.resizeObserver?.unobserve(this);
  }
  detectSize() {
    const { width, height } = this.getBoundingClientRect();
    this.size = this.orientation === "vertical" ? height : width;
  }
  percentageToPixels(value) {
    return this.size * (value / 100);
  }
  pixelsToPercentage(value) {
    return value / this.size * 100;
  }
  handleDrag(event) {
    const isRtl = this.hasUpdated ? this.localize.dir() === "rtl" : this.dir === "rtl";
    if (this.disabled) {
      return;
    }
    if (event.cancelable) {
      event.preventDefault();
    }
    drag(this, {
      onMove: (x2, y) => {
        let newPositionInPixels = this.orientation === "vertical" ? y : x2;
        if (this.primary === "end") {
          newPositionInPixels = this.size - newPositionInPixels;
        }
        if (this.snap) {
          const snaps = this.snap.split(" ");
          snaps.forEach((value) => {
            let snapPoint;
            if (value.endsWith("%")) {
              snapPoint = this.size * (parseFloat(value) / 100);
            } else {
              snapPoint = parseFloat(value);
            }
            if (isRtl && this.orientation === "horizontal") {
              snapPoint = this.size - snapPoint;
            }
            if (newPositionInPixels >= snapPoint - this.snapThreshold && newPositionInPixels <= snapPoint + this.snapThreshold) {
              newPositionInPixels = snapPoint;
            }
          });
        }
        this.position = clamp(this.pixelsToPercentage(newPositionInPixels), 0, 100);
      },
      initialEvent: event
    });
  }
  handleKeyDown(event) {
    if (this.disabled) {
      return;
    }
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End", "Enter"].includes(event.key)) {
      let newPosition = this.position;
      const incr = (event.shiftKey ? 10 : 1) * (this.primary === "end" ? -1 : 1);
      event.preventDefault();
      if (event.key === "ArrowLeft" && this.orientation === "horizontal" || event.key === "ArrowUp" && this.orientation === "vertical") {
        newPosition -= incr;
      }
      if (event.key === "ArrowRight" && this.orientation === "horizontal" || event.key === "ArrowDown" && this.orientation === "vertical") {
        newPosition += incr;
      }
      if (event.key === "Home") {
        newPosition = this.primary === "end" ? 100 : 0;
      }
      if (event.key === "End") {
        newPosition = this.primary === "end" ? 0 : 100;
      }
      if (event.key === "Enter") {
        if (this.isCollapsed) {
          newPosition = this.positionBeforeCollapsing;
          this.isCollapsed = false;
        } else {
          const positionBeforeCollapsing = this.position;
          newPosition = 0;
          requestAnimationFrame(() => {
            this.isCollapsed = true;
            this.positionBeforeCollapsing = positionBeforeCollapsing;
          });
        }
      }
      this.position = clamp(newPosition, 0, 100);
    }
  }
  handleResize(entries) {
    const { width, height } = entries[0].contentRect;
    this.size = this.orientation === "vertical" ? height : width;
    if (isNaN(this.cachedPositionInPixels) || this.position === Infinity) {
      this.cachedPositionInPixels = Number(this.getAttribute("position-in-pixels"));
      this.positionInPixels = Number(this.getAttribute("position-in-pixels"));
      this.position = this.pixelsToPercentage(this.positionInPixels);
    }
    if (this.primary) {
      const newPosition = this.pixelsToPercentage(this.cachedPositionInPixels);
      if (this.position !== newPosition) {
        this.position = newPosition;
      }
    }
  }
  handlePositionChange() {
    this.cachedPositionInPixels = this.percentageToPixels(this.position);
    const newPositionInPixels = this.percentageToPixels(this.position);
    if (this.positionInPixels !== newPositionInPixels) {
      this.positionInPixels = newPositionInPixels;
    }
    this.isCollapsed = false;
    this.positionBeforeCollapsing = 0;
    this.dispatchEvent(new WaRepositionEvent());
  }
  handlePositionInPixelsChange() {
    const newPosition = this.pixelsToPercentage(this.positionInPixels);
    if (this.position !== newPosition) {
      this.position = newPosition;
    }
  }
  handleVerticalChange() {
    this.detectSize();
  }
  render() {
    const gridTemplate = this.orientation === "vertical" ? "gridTemplateRows" : "gridTemplateColumns";
    const gridTemplateAlt = this.orientation === "vertical" ? "gridTemplateColumns" : "gridTemplateRows";
    const isRtl = this.hasUpdated ? this.localize.dir() === "rtl" : this.dir === "rtl";
    const primary = `
      clamp(
        0%,
        clamp(
          var(--min),
          ${this.position}% - var(--divider-width) / 2,
          var(--max)
        ),
        calc(100% - var(--divider-width))
      )
    `;
    const secondary = "auto";
    if (!this.style) {
      this.style = {};
    }
    if (this.primary === "end") {
      if (isRtl && this.orientation === "horizontal") {
        this.style[gridTemplate] = `${primary} var(--divider-width) ${secondary}`;
      } else {
        this.style[gridTemplate] = `${secondary} var(--divider-width) ${primary}`;
      }
    } else {
      if (isRtl && this.orientation === "horizontal") {
        this.style[gridTemplate] = `${secondary} var(--divider-width) ${primary}`;
      } else {
        this.style[gridTemplate] = `${primary} var(--divider-width) ${secondary}`;
      }
    }
    this.style[gridTemplateAlt] = "";
    return x`
      <slot name="start" part="panel start" class="start"></slot>

      <div
        part="divider"
        class="divider"
        tabindex=${o2(this.disabled ? void 0 : "0")}
        role="separator"
        aria-valuenow=${this.position}
        aria-valuemin="0"
        aria-valuemax="100"
        aria-label=${this.localize.term("resize")}
        @keydown=${this.handleKeyDown}
        @mousedown=${this.handleDrag}
        @touchstart=${this.handleDrag}
      >
        <slot name="divider"></slot>
      </div>

      <slot name="end" part="panel end" class="end"></slot>
    `;
  }
};
WaSplitPanel.css = split_panel_styles_default;
__decorateClass([
  e(".divider")
], WaSplitPanel.prototype, "divider", 2);
__decorateClass([
  n({ type: Number, reflect: true })
], WaSplitPanel.prototype, "position", 2);
__decorateClass([
  n({ attribute: "position-in-pixels", type: Number })
], WaSplitPanel.prototype, "positionInPixels", 2);
__decorateClass([
  n({ reflect: true })
], WaSplitPanel.prototype, "orientation", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaSplitPanel.prototype, "disabled", 2);
__decorateClass([
  n()
], WaSplitPanel.prototype, "primary", 2);
__decorateClass([
  n()
], WaSplitPanel.prototype, "snap", 2);
__decorateClass([
  n({ type: Number, attribute: "snap-threshold" })
], WaSplitPanel.prototype, "snapThreshold", 2);
__decorateClass([
  watch("position")
], WaSplitPanel.prototype, "handlePositionChange", 1);
__decorateClass([
  watch("positionInPixels")
], WaSplitPanel.prototype, "handlePositionInPixelsChange", 1);
__decorateClass([
  watch("vertical")
], WaSplitPanel.prototype, "handleVerticalChange", 1);
WaSplitPanel = __decorateClass([
  t("wa-split-panel")
], WaSplitPanel);

export {
  WaSplitPanel
};
