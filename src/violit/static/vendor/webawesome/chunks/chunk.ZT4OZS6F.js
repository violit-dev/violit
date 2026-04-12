/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/cancel.ts
var WaCancelEvent = class extends Event {
  constructor() {
    super("wa-cancel", { bubbles: true, cancelable: false, composed: true });
  }
};

export {
  WaCancelEvent
};
