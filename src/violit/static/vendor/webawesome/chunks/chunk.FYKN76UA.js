/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/expand.ts
var WaExpandEvent = class extends Event {
  constructor() {
    super("wa-expand", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaExpandEvent
};
