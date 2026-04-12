/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  WaShowEvent
} from "./chunk.4ZAKP7NY.js";
import {
  WaHideEvent
} from "./chunk.MQODJ75V.js";
import {
  WaAfterHideEvent
} from "./chunk.3NKIHICW.js";
import {
  WaAfterShowEvent
} from "./chunk.PX3HMKF7.js";
import {
  details_styles_default
} from "./chunk.5DQYMPDO.js";
import {
  waitForEvent
} from "./chunk.F25QOBDY.js";
import {
  animate,
  parseDuration
} from "./chunk.L6CIKOFQ.js";
import {
  WebAwesomeFormAssociatedElement
} from "./chunk.I3XGXHPO.js";
import {
  e as e2
} from "./chunk.KWDPKKFO.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
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

// src/components/details/details.ts
var WaDetails = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.animationGeneration = 0;
    this.isAnimating = false;
    this.open = false;
    this.disabled = false;
    this.appearance = "outlined";
    this.iconPlacement = "end";
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.detailsObserver?.disconnect();
  }
  firstUpdated() {
    this.body.style.height = this.open ? "auto" : "0";
    if (this.open) {
      this.details.open = true;
    }
    this.detailsObserver = new MutationObserver((changes) => {
      for (const change of changes) {
        if (change.type === "attributes" && change.attributeName === "open") {
          if (this.details.open) {
            this.show();
          } else {
            this.hide();
          }
        }
      }
    });
    this.detailsObserver.observe(this.details, { attributes: true });
  }
  updated(changedProperties) {
    if (changedProperties.has("isAnimating")) {
      this.customStates.set("animating", this.isAnimating);
    }
  }
  handleSummaryClick(event) {
    const eventPath = event.composedPath();
    const hasInteractiveElement = eventPath.some((element) => {
      if (!(element instanceof HTMLElement)) return false;
      const tagName = element.tagName?.toLowerCase();
      if (["a", "button", "input", "textarea", "select"].includes(tagName)) {
        return true;
      }
      if (element instanceof WebAwesomeFormAssociatedElement) {
        return !("disabled" in element) || !element.disabled;
      }
      return false;
    });
    if (hasInteractiveElement) {
      return;
    }
    event.preventDefault();
    if (!this.disabled) {
      if (this.open) {
        this.hide();
      } else {
        this.show();
      }
      this.header.focus();
    }
  }
  handleSummaryKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (this.open) {
        this.hide();
      } else {
        this.show();
      }
    }
    if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
      event.preventDefault();
      this.hide();
    }
    if (event.key === "ArrowDown" || event.key === "ArrowRight") {
      event.preventDefault();
      this.show();
    }
  }
  /** Closes other <wa-details> elements in the same document when they have the same name. */
  closeOthersWithSameName() {
    if (!this.name) return;
    const root = this.getRootNode();
    const otherDetails = root.querySelectorAll(`wa-details[name="${this.name}"]`);
    otherDetails.forEach((detail) => {
      if (detail !== this && detail.open) {
        detail.open = false;
      }
    });
  }
  async handleOpenChange() {
    this.animationGeneration++;
    const generation = this.animationGeneration;
    if (this.open) {
      this.details.open = true;
      const waShow = new WaShowEvent();
      this.dispatchEvent(waShow);
      if (waShow.defaultPrevented) {
        this.open = false;
        this.details.open = false;
        return;
      }
      this.closeOthersWithSameName();
      this.isAnimating = true;
      const duration = parseDuration(getComputedStyle(this.body).getPropertyValue("--show-duration"));
      await animate(
        this.body,
        [
          { height: "0", opacity: "0" },
          { height: `${this.body.scrollHeight}px`, opacity: "1" }
        ],
        {
          duration,
          easing: "linear"
        }
      );
      if (this.animationGeneration !== generation) {
        return;
      }
      this.body.style.height = "auto";
      this.isAnimating = false;
      this.dispatchEvent(new WaAfterShowEvent());
    } else {
      const waHide = new WaHideEvent();
      this.dispatchEvent(waHide);
      if (waHide.defaultPrevented) {
        this.details.open = true;
        this.open = true;
        return;
      }
      this.isAnimating = true;
      const duration = parseDuration(getComputedStyle(this.body).getPropertyValue("--hide-duration"));
      await animate(
        this.body,
        [
          { height: `${this.body.scrollHeight}px`, opacity: "1" },
          { height: "0", opacity: "0" }
        ],
        { duration, easing: "linear" }
      );
      if (this.animationGeneration !== generation) {
        return;
      }
      this.body.style.height = "0";
      this.isAnimating = false;
      this.details.open = false;
      this.dispatchEvent(new WaAfterHideEvent());
    }
  }
  /** Shows the details. */
  async show() {
    if (this.open || this.disabled) {
      return void 0;
    }
    this.open = true;
    return waitForEvent(this, "wa-after-show");
  }
  /** Hides the details */
  async hide() {
    if (!this.open || this.disabled) {
      return void 0;
    }
    this.open = false;
    return waitForEvent(this, "wa-after-hide");
  }
  render() {
    const isRtl = !this.hasUpdated ? this.dir === "rtl" : this.localize.dir() === "rtl";
    return x`
      <details part="base">
        <summary
          part="header"
          role="button"
          aria-expanded=${this.open ? "true" : "false"}
          aria-controls="content"
          aria-disabled=${this.disabled ? "true" : "false"}
          tabindex=${this.disabled ? "-1" : "0"}
          @click=${this.handleSummaryClick}
          @keydown=${this.handleSummaryKeyDown}
        >
          <slot name="summary" part="summary">${this.summary}</slot>

          <span part="icon">
            <slot name="expand-icon">
              <wa-icon library="system" variant="solid" name=${isRtl ? "chevron-left" : "chevron-right"}></wa-icon>
            </slot>
            <slot name="collapse-icon">
              <wa-icon library="system" variant="solid" name=${isRtl ? "chevron-left" : "chevron-right"}></wa-icon>
            </slot>
          </span>
        </summary>

        <div
          class=${e2({
      body: true,
      animating: this.isAnimating
    })}
          role="region"
          aria-labelledby="header"
        >
          <slot part="content" id="content" class="content"></slot>
        </div>
      </details>
    `;
  }
};
WaDetails.css = details_styles_default;
__decorateClass([
  e("details")
], WaDetails.prototype, "details", 2);
__decorateClass([
  e("summary")
], WaDetails.prototype, "header", 2);
__decorateClass([
  e(".body")
], WaDetails.prototype, "body", 2);
__decorateClass([
  e(".expand-icon-slot")
], WaDetails.prototype, "expandIconSlot", 2);
__decorateClass([
  r()
], WaDetails.prototype, "isAnimating", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaDetails.prototype, "open", 2);
__decorateClass([
  n()
], WaDetails.prototype, "summary", 2);
__decorateClass([
  n({ reflect: true })
], WaDetails.prototype, "name", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaDetails.prototype, "disabled", 2);
__decorateClass([
  n({ reflect: true })
], WaDetails.prototype, "appearance", 2);
__decorateClass([
  n({ attribute: "icon-placement", reflect: true })
], WaDetails.prototype, "iconPlacement", 2);
__decorateClass([
  watch("open", { waitUntilFirstUpdate: true })
], WaDetails.prototype, "handleOpenChange", 1);
WaDetails = __decorateClass([
  t("wa-details")
], WaDetails);

export {
  WaDetails
};
