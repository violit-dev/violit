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
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/format-date/format-date.ts
var WaFormatDate = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.date = /* @__PURE__ */ new Date();
    this.hourFormat = "auto";
  }
  static get styles() {
    return [];
  }
  render() {
    const date = new Date(this.date);
    const hour12 = this.hourFormat === "auto" ? void 0 : this.hourFormat === "12";
    if (isNaN(date.getMilliseconds())) {
      return void 0;
    }
    const displayDate = this.localize.date(date, {
      weekday: this.weekday,
      era: this.era,
      year: this.year,
      month: this.month,
      day: this.day,
      hour: this.hour,
      minute: this.minute,
      second: this.second,
      timeZoneName: this.timeZoneName,
      timeZone: this.timeZone,
      hour12
    });
    return x`<time datetime=${date.toISOString()}>${displayDate}</time>`;
  }
};
__decorateClass([
  n()
], WaFormatDate.prototype, "date", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "weekday", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "era", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "year", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "month", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "day", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "hour", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "minute", 2);
__decorateClass([
  n()
], WaFormatDate.prototype, "second", 2);
__decorateClass([
  n({ attribute: "time-zone-name" })
], WaFormatDate.prototype, "timeZoneName", 2);
__decorateClass([
  n({ attribute: "time-zone" })
], WaFormatDate.prototype, "timeZone", 2);
__decorateClass([
  n({ attribute: "hour-format" })
], WaFormatDate.prototype, "hourFormat", 2);
WaFormatDate = __decorateClass([
  t("wa-format-date")
], WaFormatDate);

export {
  WaFormatDate
};
