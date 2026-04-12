/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/copy.ts
var WaCopyEvent = class extends Event {
  constructor(detail) {
    super("wa-copy", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaCopyEvent
};
