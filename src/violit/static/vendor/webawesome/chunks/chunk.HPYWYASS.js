/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  popover_styles_default
} from "./chunk.7GZL6M3M.js";
import {
  WaPopup
} from "./chunk.CCGRUHHE.js";
import {
  isTopDismissible,
  registerDismissible,
  unregisterDismissible
} from "./chunk.52WA2DJO.js";
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
  uniqueId
} from "./chunk.O6IZ4I7T.js";
import {
  waitForEvent
} from "./chunk.F25QOBDY.js";
import {
  animateWithClass
} from "./chunk.L6CIKOFQ.js";
import {
  e as e2
} from "./chunk.KWDPKKFO.js";
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

// src/components/popover/popover.ts
var openPopovers = /* @__PURE__ */ new Set();
var WaPopover = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.anchor = null;
    this.placement = "top";
    this.open = false;
    this.distance = 8;
    this.skidding = 0;
    this.for = null;
    this.withoutArrow = false;
    this.eventController = new AbortController();
    this.handleAnchorClick = () => {
      this.open = !this.open;
    };
    this.handleBodyClick = (event) => {
      const target = event.target;
      const button = target.closest('[data-popover="close"]');
      if (button) {
        event.stopPropagation();
        this.open = false;
      }
    };
    this.handleDocumentKeyDown = (event) => {
      if (event.key === "Escape" && this.open && isTopDismissible(this)) {
        event.preventDefault();
        event.stopPropagation();
        this.open = false;
        if (this.anchor && typeof this.anchor.focus === "function") {
          this.anchor.focus();
        }
      }
    };
    this.handleDocumentClick = (event) => {
      if (this.anchor && event.composedPath().includes(this.anchor)) {
        return;
      }
      if (!event.composedPath().includes(this)) {
        this.open = false;
      }
    };
  }
  connectedCallback() {
    super.connectedCallback();
    if (!this.id) {
      this.id = uniqueId("wa-popover-");
    }
    if (this.eventController.signal.aborted) {
      this.eventController = new AbortController();
    }
    if (this.for && this.anchor) {
      this.anchor = null;
      this.handleForChange();
    }
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    document.removeEventListener("keydown", this.handleDocumentKeyDown);
    unregisterDismissible(this);
    this.eventController.abort();
  }
  firstUpdated() {
    if (this.open) {
      this.dialog.show();
      this.popup.active = true;
      this.popup.reposition();
    }
  }
  updated(changedProperties) {
    if (changedProperties.has("open")) {
      this.customStates.set("open", this.open);
    }
  }
  async handleOpenChange() {
    if (this.open) {
      const waShowEvent = new WaShowEvent();
      this.dispatchEvent(waShowEvent);
      if (waShowEvent.defaultPrevented) {
        this.open = false;
        return;
      }
      openPopovers.forEach((popover) => popover.open = false);
      document.addEventListener("keydown", this.handleDocumentKeyDown, { signal: this.eventController.signal });
      document.addEventListener("click", this.handleDocumentClick, { signal: this.eventController.signal });
      this.dialog.show();
      this.popup.active = true;
      openPopovers.add(this);
      registerDismissible(this);
      requestAnimationFrame(() => {
        const elementToFocus = this.querySelector("[autofocus]");
        if (elementToFocus && typeof elementToFocus.focus === "function") {
          elementToFocus.focus();
        } else {
          this.dialog.focus();
        }
      });
      await animateWithClass(this.popup.popup, "show-with-scale");
      this.popup.reposition();
      this.dispatchEvent(new WaAfterShowEvent());
    } else {
      const waHideEvent = new WaHideEvent();
      this.dispatchEvent(waHideEvent);
      if (waHideEvent.defaultPrevented) {
        this.open = true;
        return;
      }
      document.removeEventListener("keydown", this.handleDocumentKeyDown);
      document.removeEventListener("click", this.handleDocumentClick);
      openPopovers.delete(this);
      unregisterDismissible(this);
      await animateWithClass(this.popup.popup, "hide-with-scale");
      this.popup.active = false;
      this.dialog.close();
      this.dispatchEvent(new WaAfterHideEvent());
    }
  }
  handleForChange() {
    const rootNode = this.getRootNode();
    if (!rootNode) {
      return;
    }
    const newAnchor = this.for ? rootNode.getElementById(this.for) : null;
    const oldAnchor = this.anchor;
    if (newAnchor === oldAnchor) {
      return;
    }
    const { signal } = this.eventController;
    if (newAnchor) {
      newAnchor.addEventListener("click", this.handleAnchorClick, { signal });
    }
    if (oldAnchor) {
      oldAnchor.removeEventListener("click", this.handleAnchorClick);
    }
    this.anchor = newAnchor;
    if (this.for && !newAnchor) {
      console.warn(
        `A popover was assigned to an element with an ID of "${this.for}" but the element could not be found.`,
        this
      );
    }
  }
  async handleOptionsChange() {
    if (this.hasUpdated) {
      await this.updateComplete;
      this.popup.reposition();
    }
  }
  /** Shows the popover. */
  async show() {
    if (this.open) {
      return void 0;
    }
    this.open = true;
    return waitForEvent(this, "wa-after-show");
  }
  /** Hides the popover. */
  async hide() {
    if (!this.open) {
      return void 0;
    }
    this.open = false;
    return waitForEvent(this, "wa-after-hide");
  }
  render() {
    return x`
      <dialog part="dialog" class="dialog">
        <wa-popup
          part="popup"
          exportparts="
            popup:popup__popup,
            arrow:popup__arrow
          "
          class=${e2({
      popover: true,
      "popover-open": this.open
    })}
          placement=${this.placement}
          distance=${this.distance}
          skidding=${this.skidding}
          flip
          shift
          ?arrow=${!this.withoutArrow}
          .anchor=${this.anchor}
        >
          <div part="body" class="body" @click=${this.handleBodyClick}>
            <slot></slot>
          </div>
        </wa-popup>
      </dialog>
    `;
  }
};
WaPopover.css = popover_styles_default;
WaPopover.dependencies = { "wa-popup": WaPopup };
__decorateClass([
  e("dialog")
], WaPopover.prototype, "dialog", 2);
__decorateClass([
  e(".body")
], WaPopover.prototype, "body", 2);
__decorateClass([
  e("wa-popup")
], WaPopover.prototype, "popup", 2);
__decorateClass([
  r()
], WaPopover.prototype, "anchor", 2);
__decorateClass([
  n()
], WaPopover.prototype, "placement", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaPopover.prototype, "open", 2);
__decorateClass([
  n({ type: Number })
], WaPopover.prototype, "distance", 2);
__decorateClass([
  n({ type: Number })
], WaPopover.prototype, "skidding", 2);
__decorateClass([
  n()
], WaPopover.prototype, "for", 2);
__decorateClass([
  n({ attribute: "without-arrow", type: Boolean, reflect: true })
], WaPopover.prototype, "withoutArrow", 2);
__decorateClass([
  watch("open", { waitUntilFirstUpdate: true })
], WaPopover.prototype, "handleOpenChange", 1);
__decorateClass([
  watch("for")
], WaPopover.prototype, "handleForChange", 1);
__decorateClass([
  watch(["distance", "placement", "skidding"])
], WaPopover.prototype, "handleOptionsChange", 1);
WaPopover = __decorateClass([
  t("wa-popover")
], WaPopover);

export {
  WaPopover
};
