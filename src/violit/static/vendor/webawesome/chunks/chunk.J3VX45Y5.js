/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  radio_styles_default
} from "./chunk.MN256RSG.js";
import {
  form_control_styles_default
} from "./chunk.346V4PTX.js";
import {
  WebAwesomeFormAssociatedElement
} from "./chunk.I3XGXHPO.js";
import {
  size_styles_default
} from "./chunk.MEYJNQF4.js";
import {
  n,
  r,
  t
} from "./chunk.K4C5PQDP.js";
import {
  o
} from "./chunk.7OBLIRXR.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/radio/radio.ts
var WaRadio = class extends WebAwesomeFormAssociatedElement {
  constructor() {
    super();
    this.checked = false;
    this.forceDisabled = false;
    this.appearance = "default";
    this.disabled = false;
    this.handleClick = () => {
      if (!this.disabled && !this.forceDisabled) {
        this.checked = true;
      }
    };
    if (!o) {
      this.addEventListener("click", this.handleClick);
    }
  }
  connectedCallback() {
    super.connectedCallback();
    this.setInitialAttributes();
  }
  setInitialAttributes() {
    this.setAttribute("role", "radio");
    this.tabIndex = 0;
    this.setAttribute("aria-disabled", this.disabled || this.forceDisabled ? "true" : "false");
  }
  updated(changedProperties) {
    super.updated(changedProperties);
    if (changedProperties.has("checked")) {
      this.customStates.set("checked", this.checked);
      this.setAttribute("aria-checked", this.checked ? "true" : "false");
      if (!this.disabled && !this.forceDisabled) {
        this.tabIndex = this.checked ? 0 : -1;
      }
    }
    if (changedProperties.has("disabled") || changedProperties.has("forceDisabled")) {
      const effectivelyDisabled = this.disabled || this.forceDisabled;
      this.customStates.set("disabled", effectivelyDisabled);
      this.setAttribute("aria-disabled", effectivelyDisabled ? "true" : "false");
      if (effectivelyDisabled) {
        this.tabIndex = -1;
      } else {
        this.tabIndex = this.checked ? 0 : -1;
      }
    }
  }
  /**
   * @override
   */
  setValue() {
  }
  render() {
    return x`
      <span part="control" class="control">
        ${this.checked ? x`
              <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" part="checked-icon" class="checked-icon">
                <circle cx="8" cy="8" r="8" />
              </svg>
            ` : ""}
      </span>

      <slot part="label" class="label"></slot>
    `;
  }
};
WaRadio.css = [form_control_styles_default, size_styles_default, radio_styles_default];
__decorateClass([
  r()
], WaRadio.prototype, "checked", 2);
__decorateClass([
  r()
], WaRadio.prototype, "forceDisabled", 2);
__decorateClass([
  n({ reflect: true })
], WaRadio.prototype, "value", 2);
__decorateClass([
  n({ reflect: true })
], WaRadio.prototype, "appearance", 2);
__decorateClass([
  n({ reflect: true })
], WaRadio.prototype, "size", 2);
__decorateClass([
  n({ type: Boolean })
], WaRadio.prototype, "disabled", 2);
WaRadio = __decorateClass([
  t("wa-radio")
], WaRadio);
WaRadio.disableWarning?.("change-in-update");

export {
  WaRadio
};
