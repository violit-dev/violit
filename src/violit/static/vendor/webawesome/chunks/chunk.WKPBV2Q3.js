/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o,
  require_react
} from "./chunk.XJOHOSCS.js";
import {
  WaDetails
} from "./chunk.RF7KCC7B.js";
import {
  __toESM
} from "./chunk.JHZRD2LV.js";

// src/react/details/index.ts
var React = __toESM(require_react(), 1);
var tagName = "wa-details";
var reactWrapper = o({
  tagName,
  elementClass: WaDetails,
  react: React,
  events: {
    onWaShow: "wa-show",
    onWaAfterShow: "wa-after-show",
    onWaHide: "wa-hide",
    onWaAfterHide: "wa-after-hide"
  },
  displayName: "WaDetails"
});
var details_default = reactWrapper;

export {
  details_default
};
