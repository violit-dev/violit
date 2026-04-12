/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/lazy-load.ts
var WaLazyLoadEvent = class extends Event {
  constructor() {
    super("wa-lazy-load", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaLazyLoadEvent
};
