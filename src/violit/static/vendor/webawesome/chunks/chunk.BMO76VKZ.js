/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/start.ts
var WaStartEvent = class extends Event {
  constructor() {
    super("wa-start", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaStartEvent
};
