/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/hover.ts
var WaHoverEvent = class extends Event {
  constructor(detail) {
    super("wa-hover", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaHoverEvent
};
