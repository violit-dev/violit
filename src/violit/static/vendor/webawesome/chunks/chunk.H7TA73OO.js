/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/include-error.ts
var WaIncludeErrorEvent = class extends Event {
  constructor(detail) {
    super("wa-include-error", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaIncludeErrorEvent
};
