/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  dropdown_item_styles_default
} from "./chunk.PWJU7FNZ.js";
import {
  animateWithClass
} from "./chunk.L6CIKOFQ.js";
import {
  HasSlotController
} from "./chunk.KIHB3VMB.js";
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

// src/components/dropdown-item/dropdown-item.ts
var WaDropdownItem = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.hasSlotController = new HasSlotController(this, "[default]", "start", "end");
    this.active = false;
    this.variant = "default";
    this.size = "medium";
    this.checkboxAdjacent = false;
    this.submenuAdjacent = false;
    this.type = "normal";
    this.checked = false;
    this.disabled = false;
    this.submenuOpen = false;
    this.hasSubmenu = false;
    this.handleSlotChange = () => {
      this.hasSubmenu = this.hasSlotController.test("submenu");
      this.updateHasSubmenuState();
      if (this.hasSubmenu) {
        this.setAttribute("aria-haspopup", "menu");
        this.setAttribute("aria-expanded", this.submenuOpen ? "true" : "false");
      } else {
        this.removeAttribute("aria-haspopup");
        this.removeAttribute("aria-expanded");
      }
    };
    /** Prevents click events from firing on the host when the item is disabled (e.g. programmatic .click() calls). */
    this.handleHostClick = (event) => {
      if (this.disabled) {
        event.preventDefault();
        event.stopImmediatePropagation();
      }
    };
    /** Prevents click events from firing when the item is disabled. */
    this.handleClick = (event) => {
      if (this.disabled) {
        event.preventDefault();
        event.stopImmediatePropagation();
      }
    };
  }
  connectedCallback() {
    super.connectedCallback();
    this.addEventListener("click", this.handleHostClick);
    this.addEventListener("mouseenter", this.handleMouseEnter.bind(this));
    this.shadowRoot.addEventListener("click", this.handleClick, { capture: true });
    this.shadowRoot.addEventListener("slotchange", this.handleSlotChange);
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.closeSubmenu();
    this.removeEventListener("click", this.handleHostClick);
    this.removeEventListener("mouseenter", this.handleMouseEnter);
    this.shadowRoot.removeEventListener("click", this.handleClick, { capture: true });
    this.shadowRoot.removeEventListener("slotchange", this.handleSlotChange);
  }
  firstUpdated() {
    this.setAttribute("tabindex", "-1");
    this.hasSubmenu = this.hasSlotController.test("submenu");
    this.updateHasSubmenuState();
  }
  updated(changedProperties) {
    if (changedProperties.has("active")) {
      this.setAttribute("tabindex", this.active ? "0" : "-1");
      this.customStates.set("active", this.active);
    }
    if (changedProperties.has("checked")) {
      if (this.type === "checkbox") {
        this.setAttribute("aria-checked", this.checked ? "true" : "false");
      } else {
        this.removeAttribute("aria-checked");
      }
      this.customStates.set("checked", this.checked);
    }
    if (changedProperties.has("disabled")) {
      this.setAttribute("aria-disabled", this.disabled ? "true" : "false");
      this.customStates.set("disabled", this.disabled);
      this.style.pointerEvents = this.disabled ? "none" : "";
    }
    if (changedProperties.has("type")) {
      if (this.type === "checkbox") {
        this.setAttribute("role", "menuitemcheckbox");
        this.setAttribute("aria-checked", this.checked ? "true" : "false");
      } else {
        this.setAttribute("role", "menuitem");
        this.removeAttribute("aria-checked");
      }
    }
    if (changedProperties.has("submenuOpen")) {
      this.customStates.set("submenu-open", this.submenuOpen);
      if (this.submenuOpen) {
        this.openSubmenu();
      } else {
        this.closeSubmenu();
      }
    }
  }
  /** Update the has-submenu custom state */
  updateHasSubmenuState() {
    this.customStates.set("has-submenu", this.hasSubmenu);
  }
  /** Opens the submenu. */
  async openSubmenu() {
    const submenu = this.submenuElement;
    if (!this.hasSubmenu || !submenu || !this.isConnected) return;
    this.notifyParentOfOpening();
    submenu.showPopover?.();
    submenu.hidden = false;
    submenu.setAttribute("data-visible", "");
    this.submenuOpen = true;
    this.setAttribute("aria-expanded", "true");
    await animateWithClass(submenu, "show");
    setTimeout(() => {
      const items = this.getSubmenuItems();
      if (items.length > 0) {
        items.forEach((item, index) => item.active = index === 0);
        items[0].focus({ preventScroll: true });
      }
    }, 0);
  }
  /** Notifies the parent dropdown that this item is opening its submenu */
  notifyParentOfOpening() {
    const event = new CustomEvent("submenu-opening", {
      bubbles: true,
      composed: true,
      detail: { item: this }
    });
    this.dispatchEvent(event);
    const parent = this.parentElement;
    if (parent) {
      const siblings = [...parent.children].filter(
        (el) => el !== this && el.localName === "wa-dropdown-item" && el.getAttribute("slot") === this.getAttribute("slot") && el.submenuOpen
      );
      siblings.forEach((sibling) => {
        sibling.submenuOpen = false;
      });
    }
  }
  /** Closes the submenu. */
  async closeSubmenu() {
    const submenu = this.submenuElement;
    if (!this.hasSubmenu || !submenu) return;
    this.submenuOpen = false;
    this.setAttribute("aria-expanded", "false");
    if (!submenu.hidden) {
      await animateWithClass(submenu, "hide");
      if (submenu?.isConnected) {
        submenu.hidden = true;
        submenu.removeAttribute("data-visible");
        submenu.hidePopover?.();
      }
    }
  }
  /** Gets all dropdown items in the submenu. */
  getSubmenuItems() {
    return [...this.children].filter(
      (el) => el.localName === "wa-dropdown-item" && el.getAttribute("slot") === "submenu" && !el.hasAttribute("disabled")
    );
  }
  /** Handles mouse enter to open the submenu */
  handleMouseEnter() {
    if (this.hasSubmenu && !this.disabled) {
      this.notifyParentOfOpening();
      this.submenuOpen = true;
    }
  }
  render() {
    return x`
      ${this.type === "checkbox" ? x`
            <wa-icon
              id="check"
              part="checkmark"
              exportparts="svg:checkmark__svg"
              library="system"
              name="check"
            ></wa-icon>
          ` : ""}

      <span id="icon" part="icon">
        <slot name="icon"></slot>
      </span>

      <span id="label" part="label">
        <slot></slot>
      </span>

      <span id="details" part="details">
        <slot name="details"></slot>
      </span>

      ${this.hasSubmenu ? x`
            <wa-icon
              id="submenu-indicator"
              part="submenu-icon"
              exportparts="svg:submenu-icon__svg"
              library="system"
              name="chevron-right"
            ></wa-icon>
          ` : ""}
      ${this.hasSubmenu ? x`
            <div
              id="submenu"
              part="submenu"
              popover="manual"
              role="menu"
              tabindex="-1"
              aria-orientation="vertical"
              hidden
            >
              <slot name="submenu"></slot>
            </div>
          ` : ""}
    `;
  }
};
WaDropdownItem.css = dropdown_item_styles_default;
__decorateClass([
  e("#submenu")
], WaDropdownItem.prototype, "submenuElement", 2);
__decorateClass([
  n({ type: Boolean })
], WaDropdownItem.prototype, "active", 2);
__decorateClass([
  n({ reflect: true })
], WaDropdownItem.prototype, "variant", 2);
__decorateClass([
  n({ reflect: true })
], WaDropdownItem.prototype, "size", 2);
__decorateClass([
  n({ attribute: "checkbox-adjacent", type: Boolean, reflect: true })
], WaDropdownItem.prototype, "checkboxAdjacent", 2);
__decorateClass([
  n({ attribute: "submenu-adjacent", type: Boolean, reflect: true })
], WaDropdownItem.prototype, "submenuAdjacent", 2);
__decorateClass([
  n()
], WaDropdownItem.prototype, "value", 2);
__decorateClass([
  n({ reflect: true })
], WaDropdownItem.prototype, "type", 2);
__decorateClass([
  n({ type: Boolean })
], WaDropdownItem.prototype, "checked", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaDropdownItem.prototype, "disabled", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaDropdownItem.prototype, "submenuOpen", 2);
__decorateClass([
  r()
], WaDropdownItem.prototype, "hasSubmenu", 2);
WaDropdownItem = __decorateClass([
  t("wa-dropdown-item")
], WaDropdownItem);

export {
  WaDropdownItem
};
