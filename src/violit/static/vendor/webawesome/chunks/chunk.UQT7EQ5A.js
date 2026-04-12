/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o,
  require_react
} from "./chunk.XJOHOSCS.js";
import {
  WaInclude
} from "./chunk.MU3RMA4Y.js";
import {
  __toESM
} from "./chunk.JHZRD2LV.js";

// src/react/include/index.ts
var React = __toESM(require_react(), 1);
var tagName = "wa-include";
var reactWrapper = o({
  tagName,
  elementClass: WaInclude,
  react: React,
  events: {
    onWaLoad: "wa-load",
    onWaIncludeError: "wa-include-error"
  },
  displayName: "WaInclude"
});
var include_default = reactWrapper;

export {
  include_default
};
