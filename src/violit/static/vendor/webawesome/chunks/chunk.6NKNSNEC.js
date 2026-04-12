/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  skeleton_styles_default
} from "./chunk.AJDO4JA4.js";
import {
  WebAwesomeElement,
  n,
  t
} from "./chunk.K4C5PQDP.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/skeleton/skeleton.ts
var WaSkeleton = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.effect = "none";
  }
  render() {
    return x` <div part="indicator" class="indicator"></div> `;
  }
};
WaSkeleton.css = skeleton_styles_default;
__decorateClass([
  n({ reflect: true })
], WaSkeleton.prototype, "effect", 2);
WaSkeleton = __decorateClass([
  t("wa-skeleton")
], WaSkeleton);

export {
  WaSkeleton
};
