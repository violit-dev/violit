/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  number_input_styles_default
} from "./chunk.BEORUVOT.js";
import {
  submitOnEnter
} from "./chunk.DOFHHKB4.js";
import {
  form_control_styles_default
} from "./chunk.346V4PTX.js";
import {
  l
} from "./chunk.KZZR6Z6I.js";
import {
  MirrorValidator
} from "./chunk.R7QX4M6R.js";
import {
  WebAwesomeFormAssociatedElement
} from "./chunk.I3XGXHPO.js";
import {
  e as e2
} from "./chunk.KWDPKKFO.js";
import {
  HasSlotController
} from "./chunk.KIHB3VMB.js";
import {
  size_styles_default
} from "./chunk.MEYJNQF4.js";
import {
  o
} from "./chunk.3MSWQ3RG.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
import {
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

// src/components/number-input/number-input.ts
var WaNumberInput = class extends WebAwesomeFormAssociatedElement {
  constructor() {
    super(...arguments);
    this.assumeInteractionOn = ["blur", "input"];
    this.hasSlotController = new HasSlotController(this, "hint", "label");
    this.localize = new LocalizeController(this);
    this.title = "";
    // make reactive to pass through
    this._value = null;
    this.defaultValue = this.getAttribute("value") || null;
    this.size = "medium";
    this.appearance = "outlined";
    this.pill = false;
    this.label = "";
    this.hint = "";
    this.placeholder = "";
    this.readonly = false;
    this.required = false;
    this.step = 1;
    this.withoutSteppers = false;
    this.inputmode = "numeric";
    this.withLabel = false;
    this.withHint = false;
  }
  static get validators() {
    return [...super.validators, MirrorValidator()];
  }
  /** The current value of the input, submitted as a name/value pair with form data. */
  get value() {
    if (this.valueHasChanged) {
      return this._value;
    }
    return this._value ?? this.defaultValue;
  }
  set value(val) {
    if (this._value === val) {
      return;
    }
    this.valueHasChanged = true;
    this._value = val;
  }
  /** Returns true if the value is at or below the minimum. */
  get isAtMin() {
    if (this.min === void 0) return false;
    const numValue = parseFloat(this.value || "");
    return !isNaN(numValue) && numValue <= this.min;
  }
  /** Returns true if the value is at or above the maximum. */
  get isAtMax() {
    if (this.max === void 0) return false;
    const numValue = parseFloat(this.value || "");
    return !isNaN(numValue) && numValue >= this.max;
  }
  handleChange(event) {
    this.value = this.input.value;
    this.relayNativeEvent(event, { bubbles: true, composed: true });
  }
  handleInput() {
    this.value = this.input.value;
  }
  handleKeyDown(event) {
    submitOnEnter(event, this);
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
      requestAnimationFrame(() => {
        if (this.value !== this.input.value) {
          this.value = this.input.value;
        }
      });
    }
  }
  handleStepperPointerUp(direction, event) {
    if (this.disabled || this.readonly) return;
    if (direction === "up") {
      this.input.stepUp();
    } else {
      this.input.stepDown();
    }
    if (this.value !== this.input.value) {
      this.value = this.input.value;
    }
    this.dispatchEvent(new InputEvent("input", { bubbles: true, composed: true }));
    this.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
    if (event.pointerType !== "touch") {
      this.input.focus();
    }
  }
  handleStepperPointerDown(event) {
    if (event.pointerType === "touch") return;
    event.preventDefault();
    this.input.focus();
  }
  updated(changedProperties) {
    super.updated(changedProperties);
    if (changedProperties.has("value")) {
      this.customStates.set("blank", !this.value);
    }
  }
  handleStepChange() {
    this.input.step = String(this.step);
    this.updateValidity();
  }
  /** Sets focus on the input. */
  focus(options) {
    this.input.focus(options);
  }
  /** Removes focus from the input. */
  blur() {
    this.input.blur();
  }
  /** Selects all the text in the input. */
  select() {
    this.input.select();
  }
  /** Increments the value by the step amount. */
  stepUp() {
    this.input.stepUp();
    if (this.value !== this.input.value) {
      this.value = this.input.value;
    }
  }
  /** Decrements the value by the step amount. */
  stepDown() {
    this.input.stepDown();
    if (this.value !== this.input.value) {
      this.value = this.input.value;
    }
  }
  formResetCallback() {
    this.value = this.defaultValue;
    super.formResetCallback();
  }
  render() {
    const hasLabelSlot = this.hasUpdated ? this.hasSlotController.test("label") : this.withLabel;
    const hasHintSlot = this.hasUpdated ? this.hasSlotController.test("hint") : this.withHint;
    const hasLabel = this.label ? true : !!hasLabelSlot;
    const hasHint = this.hint ? true : !!hasHintSlot;
    return x`
      <label
        part="form-control-label label"
        class=${e2({
      label: true,
      "has-label": hasLabel
    })}
        for="input"
        aria-hidden=${hasLabel ? "false" : "true"}
      >
        <slot name="label">${this.label}</slot>
      </label>

      <div part="base" class="number-field">
        ${!this.withoutSteppers ? x`
              <button
                part="stepper stepper-decrement"
                class="stepper stepper-decrement"
                type="button"
                tabindex="-1"
                aria-label=${this.localize.term("decrement")}
                ?disabled=${this.disabled || this.readonly || this.isAtMin}
                @pointerdown=${this.handleStepperPointerDown}
                @pointerup=${(event) => this.handleStepperPointerUp("down", event)}
              >
                <slot name="decrement-icon">
                  <wa-icon name="minus" library="system"></wa-icon>
                </slot>
              </button>
            ` : ""}

        <slot name="start" part="start" class="start"></slot>

        <input
          part="input"
          id="input"
          class="control"
          type="number"
          inputmode=${o(this.inputmode)}
          title=${this.title}
          name=${o(this.name)}
          ?disabled=${this.disabled}
          ?readonly=${this.readonly}
          ?required=${this.required}
          placeholder=${o(this.placeholder)}
          min=${o(this.min)}
          max=${o(this.max)}
          step=${o(this.step)}
          .value=${l(this.value ?? "")}
          autocomplete=${o(this.autocomplete)}
          ?autofocus=${this.autofocus}
          enterkeyhint=${o(this.enterkeyhint)}
          aria-describedby="hint"
          @change=${this.handleChange}
          @input=${this.handleInput}
          @keydown=${this.handleKeyDown}
        />

        <slot name="end" part="end" class="end"></slot>

        ${!this.withoutSteppers ? x`
              <button
                part="stepper stepper-increment"
                class="stepper stepper-increment"
                type="button"
                tabindex="-1"
                aria-label=${this.localize.term("increment")}
                ?disabled=${this.disabled || this.readonly || this.isAtMax}
                @pointerdown=${this.handleStepperPointerDown}
                @pointerup=${(event) => this.handleStepperPointerUp("up", event)}
              >
                <slot name="increment-icon">
                  <wa-icon name="plus" library="system"></wa-icon>
                </slot>
              </button>
            ` : ""}
      </div>

      <slot
        id="hint"
        part="hint"
        name="hint"
        class=${e2({
      "has-slotted": hasHint
    })}
        aria-hidden=${hasHint ? "false" : "true"}
        >${this.hint}</slot
      >
    `;
  }
};
WaNumberInput.css = [size_styles_default, form_control_styles_default, number_input_styles_default];
WaNumberInput.shadowRootOptions = { ...WebAwesomeFormAssociatedElement.shadowRootOptions, delegatesFocus: true };
__decorateClass([
  e("input")
], WaNumberInput.prototype, "input", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "title", 2);
__decorateClass([
  r()
], WaNumberInput.prototype, "value", 1);
__decorateClass([
  n({ attribute: "value", reflect: true })
], WaNumberInput.prototype, "defaultValue", 2);
__decorateClass([
  n({ reflect: true })
], WaNumberInput.prototype, "size", 2);
__decorateClass([
  n({ reflect: true })
], WaNumberInput.prototype, "appearance", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaNumberInput.prototype, "pill", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "label", 2);
__decorateClass([
  n({ attribute: "hint" })
], WaNumberInput.prototype, "hint", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "placeholder", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaNumberInput.prototype, "readonly", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaNumberInput.prototype, "required", 2);
__decorateClass([
  n({ type: Number })
], WaNumberInput.prototype, "min", 2);
__decorateClass([
  n({ type: Number })
], WaNumberInput.prototype, "max", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "step", 2);
__decorateClass([
  n({ attribute: "without-steppers", type: Boolean })
], WaNumberInput.prototype, "withoutSteppers", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "autocomplete", 2);
__decorateClass([
  n({ type: Boolean })
], WaNumberInput.prototype, "autofocus", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "enterkeyhint", 2);
__decorateClass([
  n()
], WaNumberInput.prototype, "inputmode", 2);
__decorateClass([
  n({ attribute: "with-label", type: Boolean })
], WaNumberInput.prototype, "withLabel", 2);
__decorateClass([
  n({ attribute: "with-hint", type: Boolean })
], WaNumberInput.prototype, "withHint", 2);
__decorateClass([
  watch("step", { waitUntilFirstUpdate: true })
], WaNumberInput.prototype, "handleStepChange", 1);
WaNumberInput = __decorateClass([
  t("wa-number-input")
], WaNumberInput);
WaNumberInput.disableWarning?.("change-in-update");

export {
  WaNumberInput
};
