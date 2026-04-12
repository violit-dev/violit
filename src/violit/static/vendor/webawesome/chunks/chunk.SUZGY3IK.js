/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/events/mutation.ts
var WaMutationEvent = class extends Event {
  constructor(detail) {
    super("wa-mutation", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};

export {
  WaMutationEvent
};
