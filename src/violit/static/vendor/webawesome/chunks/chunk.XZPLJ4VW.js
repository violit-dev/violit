/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/intersect.ts
var WaIntersectEvent = class extends Event {
  constructor(detail) {
    super("wa-intersect", { bubbles: false, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaIntersectEvent
};
