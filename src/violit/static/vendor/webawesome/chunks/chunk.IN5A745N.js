/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  WaHoverEvent
} from "./chunk.XW6BKGGI.js";
import {
  rating_styles_default
} from "./chunk.5YVRGMJI.js";
import {
  o as o2
} from "./chunk.2BXLTQVW.js";
import {
  clamp
} from "./chunk.O6IZ4I7T.js";
import {
  RequiredValidator
} from "./chunk.SDDRXMOC.js";
import {
  WebAwesomeFormAssociatedElement
} from "./chunk.I3XGXHPO.js";
import {
  e
} from "./chunk.KWDPKKFO.js";
import {
  size_styles_default
} from "./chunk.MEYJNQF4.js";
import {
  o
} from "./chunk.BQNDCXAL.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
import {
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

// src/components/rating/rating.ts
var WaRating = class extends WebAwesomeFormAssociatedElement {
  constructor() {
    super(...arguments);
    this.assumeInteractionOn = ["change"];
    this.localize = new LocalizeController(this);
    this.hoverValue = 0;
    this.isHovering = false;
    this.name = null;
    this.label = "";
    this.value = 0;
    this.defaultValue = 0;
    this.max = 5;
    this.precision = 1;
    this.readonly = false;
    this.disabled = false;
    this.required = false;
    this.getSymbol = (_value, isSelected) => {
      return isSelected ? '<wa-icon name="star" library="system" variant="solid"></wa-icon>' : '<wa-icon name="star" library="system" variant="regular"></wa-icon>';
    };
    this.size = "medium";
    this.handleClick = (event) => {
      if (this.disabled) {
        return;
      }
      this.setRatingValue(this.getValueFromXCoordinate(event.clientX));
      this.updateComplete.then(() => {
        this.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
      });
    };
    this.handleKeyDown = (event) => {
      const isLtr = this.matches(":dir(ltr)");
      const isRtl = this.localize.dir() === "rtl";
      const oldValue = this.value;
      if (this.disabled || this.readonly) {
        return;
      }
      if (event.key === "ArrowDown" || isLtr && event.key === "ArrowLeft" || isRtl && event.key === "ArrowRight") {
        const decrement = event.shiftKey ? 1 : this.precision;
        this.value = Math.max(0, this.value - decrement);
        event.preventDefault();
      }
      if (event.key === "ArrowUp" || isLtr && event.key === "ArrowRight" || isRtl && event.key === "ArrowLeft") {
        const increment = event.shiftKey ? 1 : this.precision;
        this.value = Math.min(this.max, this.value + increment);
        event.preventDefault();
      }
      if (event.key === "Home") {
        this.value = 0;
        event.preventDefault();
      }
      if (event.key === "End") {
        this.value = this.max;
        event.preventDefault();
      }
      if (this.value !== oldValue) {
        this.updateComplete.then(() => {
          this.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
        });
      }
    };
    this.handlePointerEnter = (event) => {
      this.isHovering = true;
      this.hoverValue = this.getValueFromPointerPosition(event);
    };
    this.handlePointerMove = (event) => {
      this.hoverValue = this.getValueFromPointerPosition(event);
    };
    this.handlePointerLeave = () => {
      this.isHovering = false;
    };
    this.handlePointerDown = (event) => {
      if (event.button !== 0) {
        return;
      }
      this.isHovering = true;
      this.hoverValue = this.getValueFromPointerPosition(event);
      this.setPointerCapture(event.pointerId);
      event.preventDefault();
    };
    this.handlePointerUp = (event) => {
      this.releasePointerCapture(event.pointerId);
      this.isHovering = false;
    };
  }
  static get validators() {
    return [...super.validators, RequiredValidator()];
  }
  connectedCallback() {
    super.connectedCallback();
    this.setAttribute("role", "slider");
    this.setAttribute("aria-valuenow", String(this.value));
    this.setAttribute("aria-valuemin", "0");
    this.setAttribute("aria-valuemax", String(this.max));
    this.setAttribute("aria-disabled", this.disabled ? "true" : "false");
    this.setAttribute("aria-readonly", this.readonly ? "true" : "false");
    if (this.label) {
      this.setAttribute("aria-label", this.label);
    }
    if (!this.disabled && !this.readonly) {
      this.tabIndex = 0;
    } else {
      this.tabIndex = -1;
    }
    this.addEventListener("click", this.handleClick);
    this.addEventListener("keydown", this.handleKeyDown);
    this.addEventListener("pointerenter", this.handlePointerEnter);
    this.addEventListener("pointermove", this.handlePointerMove);
    this.addEventListener("pointerleave", this.handlePointerLeave);
    this.addEventListener("pointerdown", this.handlePointerDown);
    this.addEventListener("pointerup", this.handlePointerUp);
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.removeEventListener("click", this.handleClick);
    this.removeEventListener("keydown", this.handleKeyDown);
    this.removeEventListener("pointerenter", this.handlePointerEnter);
    this.removeEventListener("pointermove", this.handlePointerMove);
    this.removeEventListener("pointerleave", this.handlePointerLeave);
    this.removeEventListener("pointerdown", this.handlePointerDown);
    this.removeEventListener("pointerup", this.handlePointerUp);
  }
  updated(changedProperties) {
    super.updated(changedProperties);
    if (changedProperties.has("value")) {
      this.setAttribute("aria-valuenow", String(this.value));
    }
    if (changedProperties.has("max")) {
      this.setAttribute("aria-valuemax", String(this.max));
    }
    if (changedProperties.has("disabled")) {
      this.setAttribute("aria-disabled", this.disabled ? "true" : "false");
      this.tabIndex = this.disabled || this.readonly ? -1 : 0;
    }
    if (changedProperties.has("readonly")) {
      this.setAttribute("aria-readonly", this.readonly ? "true" : "false");
      this.tabIndex = this.disabled || this.readonly ? -1 : 0;
    }
    if (changedProperties.has("label")) {
      if (this.label) {
        this.setAttribute("aria-label", this.label);
      } else {
        this.removeAttribute("aria-label");
      }
    }
  }
  getValueFromPointerPosition(event) {
    return this.getValueFromXCoordinate(event.clientX);
  }
  getValueFromXCoordinate(coordinate) {
    const isRtl = this.localize.dir() === "rtl";
    const { left, right, width } = this.getBoundingClientRect();
    const value = isRtl ? this.roundToPrecision((right - coordinate) / width * this.max, this.precision) : this.roundToPrecision((coordinate - left) / width * this.max, this.precision);
    return clamp(value, 0, this.max);
  }
  setRatingValue(newValue) {
    if (this.disabled || this.readonly) {
      return;
    }
    this.value = newValue === this.value ? 0 : newValue;
    this.isHovering = false;
  }
  roundToPrecision(numberToRound, precision = 0.5) {
    const multiplier = 1 / precision;
    return Math.ceil(numberToRound * multiplier) / multiplier;
  }
  handleHoverValueChange() {
    this.dispatchEvent(
      new WaHoverEvent({
        phase: "move",
        value: this.hoverValue
      })
    );
  }
  handleIsHoveringChange() {
    this.dispatchEvent(
      new WaHoverEvent({
        phase: this.isHovering ? "start" : "end",
        value: this.hoverValue
      })
    );
  }
  formResetCallback() {
    this.value = this.defaultValue;
    super.formResetCallback();
  }
  render() {
    const isRtl = this.hasUpdated ? this.localize.dir() === "rtl" : this.dir;
    const counter = Array.from(Array(this.max).keys());
    let displayValue = 0;
    if (this.disabled || this.readonly) {
      displayValue = this.value;
    } else {
      displayValue = this.isHovering ? this.hoverValue : this.value;
    }
    return x`
      <div
        part="base"
        class=${e({
      rating: true,
      "rating-readonly": this.readonly,
      "rating-disabled": this.disabled
    })}
      >
        <span class="symbols">
          ${counter.map((index) => {
      const isSelected = displayValue >= index + 1;
      if (displayValue > index && displayValue < index + 1) {
        return x`
                <span
                  class=${e({
          symbol: true,
          "partial-symbol-container": true,
          "symbol-hover": this.isHovering && Math.ceil(displayValue) === index + 1
        })}
                  role="presentation"
                >
                  <div
                    style=${o({
          clipPath: isRtl ? `inset(0 ${(displayValue - index) * 100}% 0 0)` : `inset(0 0 0 ${(displayValue - index) * 100}%)`
        })}
                  >
                    ${o2(this.getSymbol(index + 1, false))}
                  </div>
                  <div
                    class="partial-filled"
                    style=${o({
          clipPath: isRtl ? `inset(0 0 0 ${100 - (displayValue - index) * 100}%)` : `inset(0 ${100 - (displayValue - index) * 100}% 0 0)`
        })}
                  >
                    ${o2(this.getSymbol(index + 1, true))}
                  </div>
                </span>
              `;
      }
      return x`
              <span
                class=${e({
        symbol: true,
        "symbol-hover": this.isHovering && Math.ceil(displayValue) === index + 1,
        "symbol-active": displayValue >= index + 1
      })}
                role="presentation"
              >
                ${o2(this.getSymbol(index + 1, isSelected))}
              </span>
            `;
    })}
        </span>
      </div>
    `;
  }
};
WaRating.css = [size_styles_default, rating_styles_default];
__decorateClass([
  r()
], WaRating.prototype, "hoverValue", 2);
__decorateClass([
  r()
], WaRating.prototype, "isHovering", 2);
__decorateClass([
  n()
], WaRating.prototype, "name", 2);
__decorateClass([
  n()
], WaRating.prototype, "label", 2);
__decorateClass([
  n({ type: Number })
], WaRating.prototype, "value", 2);
__decorateClass([
  n({ type: Number, attribute: "default-value" })
], WaRating.prototype, "defaultValue", 2);
__decorateClass([
  n({ type: Number })
], WaRating.prototype, "max", 2);
__decorateClass([
  n({ type: Number })
], WaRating.prototype, "precision", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaRating.prototype, "readonly", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaRating.prototype, "disabled", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaRating.prototype, "required", 2);
__decorateClass([
  n()
], WaRating.prototype, "getSymbol", 2);
__decorateClass([
  n({ reflect: true })
], WaRating.prototype, "size", 2);
__decorateClass([
  watch("hoverValue")
], WaRating.prototype, "handleHoverValueChange", 1);
__decorateClass([
  watch("isHovering")
], WaRating.prototype, "handleIsHoveringChange", 1);
WaRating = __decorateClass([
  t("wa-rating")
], WaRating);

export {
  WaRating
};
