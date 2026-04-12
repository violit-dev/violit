/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o,
  require_react
} from "./chunk.XJOHOSCS.js";
import {
  WaDropdown
} from "./chunk.UAI2IRMW.js";
import {
  __toESM
} from "./chunk.JHZRD2LV.js";

// src/react/dropdown/index.ts
var React = __toESM(require_react(), 1);
var tagName = "wa-dropdown";
var reactWrapper = o({
  tagName,
  elementClass: WaDropdown,
  react: React,
  events: {
    onWaShow: "wa-show",
    onWaAfterShow: "wa-after-show",
    onWaHide: "wa-hide",
    onWaAfterHide: "wa-after-hide",
    onWaSelect: "wa-select"
  },
  displayName: "WaDropdown"
});
var dropdown_default = reactWrapper;

export {
  dropdown_default
};
