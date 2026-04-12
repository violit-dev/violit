/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  progress_ring_styles_default
} from "./chunk.6WFYAIVE.js";
import {
  o
} from "./chunk.BQNDCXAL.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  WebAwesomeElement,
  e,
  n,
  r,
  t
} from "./chunk.K4C5PQDP.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/progress-ring/progress-ring.ts
var WaProgressRing = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.value = 0;
    this.label = "";
  }
  updated(changedProperties) {
    super.updated(changedProperties);
    if (changedProperties.has("value")) {
      const radius = parseFloat(getComputedStyle(this.indicator).getPropertyValue("r"));
      const circumference = 2 * Math.PI * radius;
      const offset = circumference - this.value / 100 * circumference;
      this.indicatorOffset = `${offset}px`;
    }
  }
  render() {
    return x`
      <div
        part="base"
        class="progress-ring"
        role="progressbar"
        aria-label=${this.label.length > 0 ? this.label : this.localize.term("progress")}
        aria-describedby="label"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow="${this.value}"
        style=${o({ "--percentage": this.value / 100 })}
      >
        <svg class="image">
          <circle part="track" class="track"></circle>
          <circle
            part="indicator"
            class="indicator"
            style=${o({ "stroke-dashoffset": this.indicatorOffset })}
          ></circle>
        </svg>

        <slot id="label" part="label" class="label"></slot>
      </div>
    `;
  }
};
WaProgressRing.css = progress_ring_styles_default;
__decorateClass([
  e(".indicator")
], WaProgressRing.prototype, "indicator", 2);
__decorateClass([
  r()
], WaProgressRing.prototype, "indicatorOffset", 2);
__decorateClass([
  n({ type: Number, reflect: true })
], WaProgressRing.prototype, "value", 2);
__decorateClass([
  n()
], WaProgressRing.prototype, "label", 2);
WaProgressRing = __decorateClass([
  t("wa-progress-ring")
], WaProgressRing);
WaProgressRing.disableWarning?.("change-in-update");

export {
  WaProgressRing
};
