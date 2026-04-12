/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/finish.ts
var WaFinishEvent = class extends Event {
  constructor() {
    super("wa-finish", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaFinishEvent
};
