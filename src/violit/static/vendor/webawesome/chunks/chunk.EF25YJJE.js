/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/slide-change.ts
var WaSlideChangeEvent = class extends Event {
  constructor(detail) {
    super("wa-slide-change", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaSlideChangeEvent
};
