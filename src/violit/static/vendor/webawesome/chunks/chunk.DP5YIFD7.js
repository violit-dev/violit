/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/resize.ts
var WaResizeEvent = class extends Event {
  constructor(detail) {
    super("wa-resize", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaResizeEvent
};
