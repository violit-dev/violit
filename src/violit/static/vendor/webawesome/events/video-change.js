/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.JHZRD2LV.js";

// src/events/video-change.ts
var WaVideoChangeEvent = class extends Event {
  constructor(detail) {
    super("wa-video-change", { bubbles: true, cancelable: false, composed: true });
    this.detail = detail;
  }
};
export {
  WaVideoChangeEvent
};
