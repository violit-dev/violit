/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.JHZRD2LV.js";

// src/events/create.ts
var WaCreateEvent = class extends Event {
  constructor(detail) {
    super("wa-create", { bubbles: true, cancelable: true, composed: true });
    this.detail = detail;
  }
};
export {
  WaCreateEvent
};
