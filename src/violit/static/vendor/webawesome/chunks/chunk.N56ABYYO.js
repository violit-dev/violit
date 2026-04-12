/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o,
  require_react
} from "./chunk.XJOHOSCS.js";
import {
  WaSelect
} from "./chunk.AWDGFOXI.js";
import {
  __toESM
} from "./chunk.JHZRD2LV.js";

// src/react/select/index.ts
var React = __toESM(require_react(), 1);
var tagName = "wa-select";
var reactWrapper = o({
  tagName,
  elementClass: WaSelect,
  react: React,
  events: {
    onWaClear: "wa-clear",
    onWaShow: "wa-show",
    onWaAfterShow: "wa-after-show",
    onWaHide: "wa-hide",
    onWaAfterHide: "wa-after-hide",
    onWaInvalid: "wa-invalid"
  },
  displayName: "WaSelect"
});
var select_default = reactWrapper;

export {
  select_default
};
