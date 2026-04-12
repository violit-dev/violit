/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  WaResizeEvent
} from "./chunk.DP5YIFD7.js";
import {
  resize_observer_styles_default
} from "./chunk.MAHGF7JK.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
import {
  WebAwesomeElement,
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

// src/components/resize-observer/resize-observer.ts
var WaResizeObserver = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.observedElements = [];
    this.disabled = false;
  }
  connectedCallback() {
    super.connectedCallback();
    if (!o) {
      this.resizeObserver = new ResizeObserver((entries) => {
        this.dispatchEvent(new WaResizeEvent({ entries }));
      });
      if (!this.disabled) {
        this.updateComplete.then(() => {
          this.startObserver();
        });
      }
    }
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.stopObserver();
  }
  handleSlotChange() {
    if (!this.disabled) {
      this.startObserver();
    }
  }
  startObserver() {
    const slot = this.shadowRoot.querySelector("slot");
    if (slot !== null) {
      const elements = slot.assignedElements({ flatten: true });
      this.observedElements.forEach((el) => this.resizeObserver.unobserve(el));
      this.observedElements = [];
      elements.forEach((el) => {
        this.resizeObserver.observe(el);
        this.observedElements.push(el);
      });
    }
  }
  stopObserver() {
    this.resizeObserver.disconnect();
  }
  handleDisabledChange() {
    if (this.disabled) {
      this.stopObserver();
    } else {
      this.startObserver();
    }
  }
  render() {
    return x` <slot @slotchange=${this.handleSlotChange}></slot> `;
  }
};
WaResizeObserver.css = resize_observer_styles_default;
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaResizeObserver.prototype, "disabled", 2);
__decorateClass([
  watch("disabled", { waitUntilFirstUpdate: true })
], WaResizeObserver.prototype, "handleDisabledChange", 1);
WaResizeObserver = __decorateClass([
  t("wa-resize-observer")
], WaResizeObserver);

export {
  WaResizeObserver
};
