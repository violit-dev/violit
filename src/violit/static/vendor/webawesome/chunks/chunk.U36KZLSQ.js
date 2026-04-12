/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/collapse.ts
var WaCollapseEvent = class extends Event {
  constructor() {
    super("wa-collapse", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaCollapseEvent
};
