/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  qr_code_styles_default
} from "./chunk.XW6K5DFW.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
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

// src/components/qr-code/qr-code.ts
var QrCreator;
var WaQrCode = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.value = "";
    this.label = "";
    this.size = 128;
    this.fill = "";
    this.background = "";
    this.radius = 0;
    this.errorCorrection = "H";
    this.generated = false;
  }
  firstUpdated(changedProperties) {
    super.firstUpdated(changedProperties);
    if (this.hasUpdated) {
      this.generate();
    }
  }
  generate() {
    if (!this.hasUpdated) {
      return;
    }
    if (!QrCreator) {
      import("./qr-creator.es6.min.6HXLA5WI.js").then((mod) => {
        QrCreator = mod.default;
        this.generate();
      });
      return;
    }
    this.canvas.style.maxWidth = `${this.size}px`;
    this.canvas.style.maxHeight = `${this.size}px`;
    const computedStyle = getComputedStyle(this);
    QrCreator.render(
      {
        text: this.value,
        radius: this.radius,
        ecLevel: this.errorCorrection,
        // Use the deprecated `fill` attribute if set, otherwise use the current text color
        fill: this.fill || computedStyle.color,
        // Use the deprecated `background` attribute if set, otherwise use transparent (the host has the bg color now)
        background: this.background || null,
        // We draw the canvas larger and scale its container down to avoid blurring on high-density displays
        size: this.size * 2
      },
      this.canvas
    );
    this.generated = true;
  }
  render() {
    return x`
      <canvas
        part="base"
        class="qr-code"
        role="img"
        aria-label=${this.label?.length > 0 ? this.label : this.value}
        @transitionend=${(event) => {
      if (event.propertyName === "color") {
        this.generate();
      }
    }}
      ></canvas>
    `;
  }
};
WaQrCode.css = qr_code_styles_default;
__decorateClass([
  e("canvas")
], WaQrCode.prototype, "canvas", 2);
__decorateClass([
  n()
], WaQrCode.prototype, "value", 2);
__decorateClass([
  n()
], WaQrCode.prototype, "label", 2);
__decorateClass([
  n({ type: Number })
], WaQrCode.prototype, "size", 2);
__decorateClass([
  n()
], WaQrCode.prototype, "fill", 2);
__decorateClass([
  n()
], WaQrCode.prototype, "background", 2);
__decorateClass([
  n({ type: Number })
], WaQrCode.prototype, "radius", 2);
__decorateClass([
  n({ attribute: "error-correction" })
], WaQrCode.prototype, "errorCorrection", 2);
__decorateClass([
  r()
], WaQrCode.prototype, "generated", 2);
__decorateClass([
  watch(["background", "errorCorrection", "fill", "radius", "size", "value"], { waitUntilFirstUpdate: true })
], WaQrCode.prototype, "generate", 1);
WaQrCode = __decorateClass([
  t("wa-qr-code")
], WaQrCode);

export {
  WaQrCode
};
