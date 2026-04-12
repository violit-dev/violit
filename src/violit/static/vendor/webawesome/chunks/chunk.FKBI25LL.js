/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  WebAwesomeElement,
  n,
  t
} from "./chunk.K4C5PQDP.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/format-bytes/format-bytes.ts
var WaFormatBytes = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.value = 0;
    this.unit = "byte";
    this.display = "short";
  }
  static get styles() {
    return [];
  }
  render() {
    if (isNaN(this.value)) {
      return "";
    }
    const bitPrefixes = ["", "kilo", "mega", "giga", "tera"];
    const bytePrefixes = ["", "kilo", "mega", "giga", "tera", "peta"];
    const prefix = this.unit === "bit" ? bitPrefixes : bytePrefixes;
    const index = Math.max(0, Math.min(Math.floor(Math.log10(this.value) / 3), prefix.length - 1));
    const unit = prefix[index] + this.unit;
    const valueToFormat = parseFloat((this.value / Math.pow(1e3, index)).toPrecision(3));
    return this.localize.number(valueToFormat, {
      style: "unit",
      unit,
      unitDisplay: this.display
    });
  }
};
__decorateClass([
  n({ type: Number })
], WaFormatBytes.prototype, "value", 2);
__decorateClass([
  n()
], WaFormatBytes.prototype, "unit", 2);
__decorateClass([
  n()
], WaFormatBytes.prototype, "display", 2);
WaFormatBytes = __decorateClass([
  t("wa-format-bytes")
], WaFormatBytes);

export {
  WaFormatBytes
};
