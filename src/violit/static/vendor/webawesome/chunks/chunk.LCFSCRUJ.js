/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/selection-change.ts
var WaSelectionChangeEvent = class extends Event {
  constructor(detail) {
    super("wa-selection-change", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaSelectionChangeEvent
};
