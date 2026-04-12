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

// src/components/format-number/format-number.ts
var WaFormatNumber = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.value = 0;
    this.type = "decimal";
    this.withoutGrouping = false;
    this.currency = "USD";
    this.currencyDisplay = "symbol";
  }
  static get styles() {
    return [];
  }
  render() {
    if (isNaN(this.value)) {
      return "";
    }
    return this.localize.number(this.value, {
      style: this.type,
      currency: this.currency,
      currencyDisplay: this.currencyDisplay,
      useGrouping: !this.withoutGrouping,
      minimumIntegerDigits: this.minimumIntegerDigits,
      minimumFractionDigits: this.minimumFractionDigits,
      maximumFractionDigits: this.maximumFractionDigits,
      minimumSignificantDigits: this.minimumSignificantDigits,
      maximumSignificantDigits: this.maximumSignificantDigits
    });
  }
};
__decorateClass([
  n({ type: Number })
], WaFormatNumber.prototype, "value", 2);
__decorateClass([
  n()
], WaFormatNumber.prototype, "type", 2);
__decorateClass([
  n({ attribute: "without-grouping", type: Boolean })
], WaFormatNumber.prototype, "withoutGrouping", 2);
__decorateClass([
  n()
], WaFormatNumber.prototype, "currency", 2);
__decorateClass([
  n({ attribute: "currency-display" })
], WaFormatNumber.prototype, "currencyDisplay", 2);
__decorateClass([
  n({ attribute: "minimum-integer-digits", type: Number })
], WaFormatNumber.prototype, "minimumIntegerDigits", 2);
__decorateClass([
  n({ attribute: "minimum-fraction-digits", type: Number })
], WaFormatNumber.prototype, "minimumFractionDigits", 2);
__decorateClass([
  n({ attribute: "maximum-fraction-digits", type: Number })
], WaFormatNumber.prototype, "maximumFractionDigits", 2);
__decorateClass([
  n({ attribute: "minimum-significant-digits", type: Number })
], WaFormatNumber.prototype, "minimumSignificantDigits", 2);
__decorateClass([
  n({ attribute: "maximum-significant-digits", type: Number })
], WaFormatNumber.prototype, "maximumSignificantDigits", 2);
WaFormatNumber = __decorateClass([
  t("wa-format-number")
], WaFormatNumber);

export {
  WaFormatNumber
};
