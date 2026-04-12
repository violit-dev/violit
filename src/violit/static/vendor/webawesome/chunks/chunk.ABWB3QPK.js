/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  button_group_styles_default
} from "./chunk.IYHS4N4A.js";
import {
  WebAwesomeElement,
  e,
  n,
  r,
  t
} from "./chunk.K4C5PQDP.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/button-group/button-group.ts
var WaButtonGroup = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.disableRole = false;
    this.hasOutlined = false;
    this.label = "";
    this.orientation = "horizontal";
  }
  updated(changedProperties) {
    super.updated(changedProperties);
    if (changedProperties.has("orientation")) {
      this.setAttribute("aria-orientation", this.orientation);
    }
  }
  handleFocus(event) {
    const button = findButton(event.target);
    button?.classList.add("button-focus");
  }
  handleBlur(event) {
    const button = findButton(event.target);
    button?.classList.remove("button-focus");
  }
  handleMouseOver(event) {
    const button = findButton(event.target);
    button?.classList.add("button-hover");
  }
  handleMouseOut(event) {
    const button = findButton(event.target);
    button?.classList.remove("button-hover");
  }
  render() {
    return x`
      <slot
        part="base"
        class="button-group"
        role="${this.disableRole ? "presentation" : "group"}"
        aria-label=${this.label}
        aria-orientation=${this.orientation}
        @focusout=${this.handleBlur}
        @focusin=${this.handleFocus}
        @mouseover=${this.handleMouseOver}
        @mouseout=${this.handleMouseOut}
      ></slot>
    `;
  }
};
WaButtonGroup.css = [button_group_styles_default];
__decorateClass([
  e("slot")
], WaButtonGroup.prototype, "defaultSlot", 2);
__decorateClass([
  r()
], WaButtonGroup.prototype, "disableRole", 2);
__decorateClass([
  r()
], WaButtonGroup.prototype, "hasOutlined", 2);
__decorateClass([
  n()
], WaButtonGroup.prototype, "label", 2);
__decorateClass([
  n({ reflect: true })
], WaButtonGroup.prototype, "orientation", 2);
WaButtonGroup = __decorateClass([
  t("wa-button-group")
], WaButtonGroup);
function findButton(el) {
  const selector = "wa-button, wa-radio-button";
  return el.closest(selector) ?? el.querySelector(selector);
}

export {
  WaButtonGroup
};
