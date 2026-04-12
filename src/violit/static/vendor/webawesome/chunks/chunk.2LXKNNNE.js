/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/select.ts
var WaSelectEvent = class extends Event {
  constructor(detail) {
    super("wa-select", { bubbles: true, cancelable: true, composed: true });
    this.detail = detail;
  }
};

export {
  WaSelectEvent
};
