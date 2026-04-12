/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/lazy-change.ts
var WaLazyChangeEvent = class extends Event {
  constructor() {
    super("wa-lazy-change", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaLazyChangeEvent
};
