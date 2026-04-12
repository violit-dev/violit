/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  drag
} from "./chunk.WYNTFJHW.js";
import {
  comparison_styles_default
} from "./chunk.3V4ARLUJ.js";
import {
  clamp
} from "./chunk.O6IZ4I7T.js";
import {
  o
} from "./chunk.BQNDCXAL.js";
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
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/comparison/comparison.ts
var WaComparison = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.position = 50;
  }
  handleDrag(event) {
    const { width } = this.getBoundingClientRect();
    const isRtl = this.localize.dir() === "rtl";
    event.preventDefault();
    drag(this, {
      onMove: (x2) => {
        this.customStates.set("dragging", true);
        this.position = parseFloat(clamp(x2 / width * 100, 0, 100).toFixed(2));
        if (isRtl) this.position = 100 - this.position;
      },
      onStop: () => {
        this.customStates.set("dragging", false);
      },
      initialEvent: event
    });
  }
  handleKeyDown(event) {
    const isLtr = this.matches(":dir(ltr)");
    const isRtl = this.localize.dir() === "rtl";
    if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) {
      const incr = event.shiftKey ? 10 : 1;
      let newPosition = this.position;
      event.preventDefault();
      if (isLtr && event.key === "ArrowLeft" || isRtl && event.key === "ArrowRight") {
        newPosition -= incr;
      }
      if (isLtr && event.key === "ArrowRight" || isRtl && event.key === "ArrowLeft") {
        newPosition += incr;
      }
      if (event.key === "Home") {
        newPosition = 0;
      }
      if (event.key === "End") {
        newPosition = 100;
      }
      newPosition = clamp(newPosition, 0, 100);
      this.position = newPosition;
    }
  }
  handlePositionChange() {
    this.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
  }
  render() {
    const isRtl = this.hasUpdated ? this.localize.dir() === "rtl" : this.dir === "rtl";
    return x`
      <div id="comparison" class="image" part="base">
        <div part="before" class="before">
          <slot name="before"></slot>
        </div>

        <div
          part="after"
          class="after"
          style=${o({
      clipPath: isRtl ? `inset(0 0 0 ${100 - this.position}%)` : `inset(0 ${100 - this.position}% 0 0)`
    })}
        >
          <slot name="after"></slot>
        </div>
      </div>

      <div
        part="divider"
        class="divider"
        style=${o({
      left: isRtl ? `${100 - this.position}%` : `${this.position}%`
    })}
        @keydown=${this.handleKeyDown}
        @mousedown=${this.handleDrag}
        @touchstart=${this.handleDrag}
      >
        <div
          part="handle"
          class="handle"
          role="scrollbar"
          aria-valuenow=${this.position}
          aria-valuemin="0"
          aria-valuemax="100"
          aria-controls="comparison"
          tabindex="0"
        >
          <slot name="handle">
            <wa-icon library="system" name="grip-vertical" variant="solid"></wa-icon>
          </slot>
        </div>
      </div>
    `;
  }
};
WaComparison.css = comparison_styles_default;
__decorateClass([
  e(".handle")
], WaComparison.prototype, "handle", 2);
__decorateClass([
  n({ type: Number, reflect: true })
], WaComparison.prototype, "position", 2);
__decorateClass([
  watch("position", { waitUntilFirstUpdate: true })
], WaComparison.prototype, "handlePositionChange", 1);
WaComparison = __decorateClass([
  t("wa-comparison")
], WaComparison);

export {
  WaComparison
};
