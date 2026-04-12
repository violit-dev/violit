/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  WaSelectEvent
} from "./chunk.2LXKNNNE.js";
import {
  dropdown_styles_default
} from "./chunk.Y4KJ3CGW.js";
import {
  autoUpdate,
  computePosition,
  flip,
  offset,
  shift
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
  animateWithClass
} from "./chunk.L6CIKOFQ.js";
import {
  size_styles_default
} from "./chunk.MEYJNQF4.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  WebAwesomeElement,
  e,
  n,
  t
} from "./chunk.K4C5PQDP.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/internal/active-elements.ts
function* activeElements(activeElement = document.activeElement) {
  if (activeElement === null || activeElement === void 0) return;
  yield activeElement;
  if ("shadowRoot" in activeElement && activeElement.shadowRoot && activeElement.shadowRoot.mode !== "closed") {
    yield* activeElements(activeElement.shadowRoot.activeElement);
  }
}

// src/components/dropdown/dropdown.ts
var openDropdowns = /* @__PURE__ */ new Set();
var WaDropdown = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.submenuCleanups = /* @__PURE__ */ new Map();
    this.localize = new LocalizeController(this);
    this.userTypedQuery = "";
    this.openSubmenuStack = [];
    this.open = false;
    this.size = "medium";
    this.placement = "bottom-start";
    this.distance = 0;
    this.skidding = 0;
    /** Handles key down events when the menu is open */
    this.handleDocumentKeyDown = async (event) => {
      const isRtl = this.localize.dir() === "rtl";
      if (event.key === "Escape" && this.open && isTopDismissible(this)) {
        const trigger = this.getTrigger();
        event.preventDefault();
        event.stopPropagation();
        this.open = false;
        trigger?.focus({ preventScroll: true });
        return;
      }
      const activeElement = [...activeElements()].find((el) => el.localName === "wa-dropdown-item");
      const isFocusedOnItem = activeElement?.localName === "wa-dropdown-item";
      const currentSubmenuItem = this.getCurrentSubmenuItem();
      const isInSubmenu = !!currentSubmenuItem;
      let items;
      let activeItem;
      let activeItemIndex;
      if (isInSubmenu) {
        items = this.getSubmenuItems(currentSubmenuItem);
        activeItem = items.find((item) => item.active || item === activeElement);
        activeItemIndex = activeItem ? items.indexOf(activeItem) : -1;
      } else {
        items = this.getItems();
        activeItem = items.find((item) => item.active || item === activeElement);
        activeItemIndex = activeItem ? items.indexOf(activeItem) : -1;
      }
      let itemToSelect;
      if (event.key === "ArrowUp") {
        event.preventDefault();
        event.stopPropagation();
        if (activeItemIndex > 0) {
          itemToSelect = items[activeItemIndex - 1];
        } else {
          itemToSelect = items[items.length - 1];
        }
      }
      if (event.key === "ArrowDown") {
        event.preventDefault();
        event.stopPropagation();
        if (activeItemIndex !== -1 && activeItemIndex < items.length - 1) {
          itemToSelect = items[activeItemIndex + 1];
        } else {
          itemToSelect = items[0];
        }
      }
      if (event.key === (isRtl ? "ArrowLeft" : "ArrowRight") && isFocusedOnItem && activeItem) {
        if (activeItem.hasSubmenu) {
          event.preventDefault();
          event.stopPropagation();
          activeItem.submenuOpen = true;
          this.addToSubmenuStack(activeItem);
          setTimeout(() => {
            const submenuItems = this.getSubmenuItems(activeItem);
            if (submenuItems.length > 0) {
              submenuItems.forEach((item, index) => item.active = index === 0);
              submenuItems[0].focus({ preventScroll: true });
            }
          }, 0);
          return;
        }
      }
      if (event.key === (isRtl ? "ArrowRight" : "ArrowLeft") && isInSubmenu) {
        event.preventDefault();
        event.stopPropagation();
        const removedItem = this.removeFromSubmenuStack();
        if (removedItem) {
          removedItem.submenuOpen = false;
          setTimeout(() => {
            removedItem.focus({ preventScroll: true });
            removedItem.active = true;
            const parentItems = removedItem.slot === "submenu" ? this.getSubmenuItems(removedItem.parentElement) : this.getItems();
            parentItems.forEach((item) => {
              if (item !== removedItem) {
                item.active = false;
              }
            });
          }, 0);
        }
        return;
      }
      if (event.key === "Home" || event.key === "End") {
        event.preventDefault();
        event.stopPropagation();
        itemToSelect = event.key === "Home" ? items[0] : items[items.length - 1];
      }
      if (event.key === "Tab") {
        await this.hideMenu();
      }
      if (event.key.length === 1 && !(event.metaKey || event.ctrlKey || event.altKey) && !(event.key === " " && this.userTypedQuery === "")) {
        clearTimeout(this.userTypedTimeout);
        this.userTypedTimeout = setTimeout(() => {
          this.userTypedQuery = "";
        }, 1e3);
        this.userTypedQuery += event.key;
        items.some((item) => {
          const label = (item.textContent || "").trim().toLowerCase();
          const selectionQuery = this.userTypedQuery.trim().toLowerCase();
          if (label.startsWith(selectionQuery)) {
            itemToSelect = item;
            return true;
          }
          return false;
        });
      }
      if (itemToSelect) {
        event.preventDefault();
        event.stopPropagation();
        items.forEach((item) => item.active = item === itemToSelect);
        itemToSelect.focus({ preventScroll: true });
        return;
      }
      if ((event.key === "Enter" || event.key === " " && this.userTypedQuery === "") && isFocusedOnItem && activeItem) {
        event.preventDefault();
        event.stopPropagation();
        if (activeItem.hasSubmenu) {
          activeItem.submenuOpen = true;
          this.addToSubmenuStack(activeItem);
          setTimeout(() => {
            const submenuItems = this.getSubmenuItems(activeItem);
            if (submenuItems.length > 0) {
              submenuItems.forEach((item, index) => item.active = index === 0);
              submenuItems[0].focus({ preventScroll: true });
            }
          }, 0);
        } else {
          this.makeSelection(activeItem);
        }
      }
    };
    /** Handles pointer down events when the dropdown is open. */
    this.handleDocumentPointerDown = (event) => {
      const path = event.composedPath();
      const isInDropdownHierarchy = path.some((el) => {
        if (el instanceof HTMLElement) {
          return el === this || el.closest('wa-dropdown, [part="submenu"]');
        }
        return false;
      });
      if (!isInDropdownHierarchy) {
        this.open = false;
      }
    };
    /** Handle global mouse movement for safe triangle logic */
    this.handleGlobalMouseMove = (event) => {
      const currentSubmenuItem = this.getCurrentSubmenuItem();
      if (!currentSubmenuItem?.submenuOpen || !currentSubmenuItem.submenuElement) return;
      const submenuRect = currentSubmenuItem.submenuElement.getBoundingClientRect();
      const isRtl = this.localize.dir() === "rtl";
      const submenuEdgeX = isRtl ? submenuRect.right : submenuRect.left;
      const constrainedX = isRtl ? Math.max(event.clientX, submenuEdgeX) : Math.min(event.clientX, submenuEdgeX);
      const constrainedY = Math.max(submenuRect.top, Math.min(event.clientY, submenuRect.bottom));
      currentSubmenuItem.submenuElement.style.setProperty("--safe-triangle-cursor-x", `${constrainedX}px`);
      currentSubmenuItem.submenuElement.style.setProperty("--safe-triangle-cursor-y", `${constrainedY}px`);
      const composedPath = event.composedPath();
      const submenuItemHovered = currentSubmenuItem.matches(":hover");
      const submenuElementHovered = Boolean(currentSubmenuItem.submenuElement?.matches(":hover"));
      const isOverItem = submenuItemHovered || !!composedPath.find((el) => el === currentSubmenuItem);
      const isOverSubmenu = submenuElementHovered || !!composedPath.find(
        (el) => el instanceof HTMLElement && el.closest('[part="submenu"]') === currentSubmenuItem.submenuElement
      );
      if (!isOverItem && !isOverSubmenu) {
        setTimeout(() => {
          if (!submenuItemHovered && !submenuElementHovered) {
            currentSubmenuItem.submenuOpen = false;
          }
        }, 100);
      }
    };
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    clearInterval(this.userTypedTimeout);
    this.closeAllSubmenus();
    this.submenuCleanups.forEach((cleanup) => cleanup());
    this.submenuCleanups.clear();
    document.removeEventListener("mousemove", this.handleGlobalMouseMove);
    document.removeEventListener("keydown", this.handleDocumentKeyDown);
    document.removeEventListener("pointerdown", this.handleDocumentPointerDown);
    unregisterDismissible(this);
  }
  firstUpdated() {
    this.syncAriaAttributes();
  }
  async updated(changedProperties) {
    if (changedProperties.has("open")) {
      const previousOpen = changedProperties.get("open");
      if (previousOpen === this.open) {
        return;
      }
      if (previousOpen === void 0 && this.open === false) {
        return;
      }
      this.customStates.set("open", this.open);
      if (this.open) {
        await this.showMenu();
      } else {
        this.closeAllSubmenus();
        await this.hideMenu();
      }
    }
    if (changedProperties.has("size")) {
      this.syncItemSizes();
    }
  }
  /** Gets all dropdown items slotted in the menu. */
  getItems(includeDisabled = false) {
    const items = (this.defaultSlot?.assignedElements({ flatten: true }) ?? []).filter(
      (el) => el.localName === "wa-dropdown-item"
    );
    return includeDisabled ? items : items.filter((item) => !item.disabled);
  }
  /** Gets all dropdown items in a specific submenu. */
  getSubmenuItems(parentItem, includeDisabled = false) {
    const submenuSlot = parentItem.shadowRoot?.querySelector('slot[name="submenu"]') || parentItem.querySelector('slot[name="submenu"]');
    if (!submenuSlot) {
      return [];
    }
    const items = submenuSlot.assignedElements({ flatten: true }).filter((el) => el.localName === "wa-dropdown-item");
    return includeDisabled ? items : items.filter((item) => !item.disabled);
  }
  /** Syncs item sizes with the dropdown's size property. */
  syncItemSizes() {
    const items = (this.defaultSlot?.assignedElements({ flatten: true }) ?? []).filter(
      (el) => el.localName === "wa-dropdown-item"
    );
    items.forEach((item) => item.size = this.size);
  }
  /** Handles the submenu navigation stack */
  addToSubmenuStack(item) {
    const index = this.openSubmenuStack.indexOf(item);
    if (index !== -1) {
      this.openSubmenuStack = this.openSubmenuStack.slice(0, index + 1);
    } else {
      this.openSubmenuStack.push(item);
    }
  }
  /** Removes the last item from the submenu stack */
  removeFromSubmenuStack() {
    return this.openSubmenuStack.pop();
  }
  /** Gets the current active submenu item */
  getCurrentSubmenuItem() {
    return this.openSubmenuStack.length > 0 ? this.openSubmenuStack[this.openSubmenuStack.length - 1] : void 0;
  }
  /** Closes all submenus in the dropdown. */
  closeAllSubmenus() {
    const items = this.getItems(true);
    items.forEach((item) => {
      item.submenuOpen = false;
    });
    this.openSubmenuStack = [];
  }
  /** Closes sibling submenus at the same level as the specified item. */
  closeSiblingSubmenus(item) {
    const parentDropdownItem = item.closest('wa-dropdown-item:not([slot="submenu"])');
    let siblingItems;
    if (parentDropdownItem) {
      siblingItems = this.getSubmenuItems(parentDropdownItem, true);
    } else {
      siblingItems = this.getItems(true);
    }
    siblingItems.forEach((siblingItem) => {
      if (siblingItem !== item && siblingItem.submenuOpen) {
        siblingItem.submenuOpen = false;
      }
    });
    if (!this.openSubmenuStack.includes(item)) {
      this.openSubmenuStack.push(item);
    }
  }
  /** Get the slotted trigger button, a <wa-button> or <button> element */
  getTrigger() {
    return this.querySelector('[slot="trigger"]');
  }
  /** Shows the dropdown menu. This should only be called from within updated(). */
  async showMenu() {
    const anchor = this.getTrigger();
    if (!anchor || !this.popup || !this.menu) return;
    const showEvent = new WaShowEvent();
    this.dispatchEvent(showEvent);
    if (showEvent.defaultPrevented) {
      this.open = false;
      return;
    }
    if (this.popup.active) {
      return;
    }
    openDropdowns.forEach((dropdown) => dropdown.open = false);
    this.popup.active = true;
    this.open = true;
    openDropdowns.add(this);
    registerDismissible(this);
    this.syncAriaAttributes();
    document.addEventListener("keydown", this.handleDocumentKeyDown);
    document.addEventListener("pointerdown", this.handleDocumentPointerDown);
    document.addEventListener("mousemove", this.handleGlobalMouseMove);
    this.menu.classList.remove("hide");
    await animateWithClass(this.menu, "show");
    const items = this.getItems();
    if (items.length > 0) {
      items.forEach((item, index) => item.active = index === 0);
      items[0].focus({ preventScroll: true });
    }
    this.dispatchEvent(new WaAfterShowEvent());
  }
  /** Hides the dropdown menu. This should only be called from within updated(). */
  async hideMenu() {
    if (!this.popup || !this.menu) return;
    const hideEvent = new WaHideEvent({ source: this });
    this.dispatchEvent(hideEvent);
    if (hideEvent.defaultPrevented) {
      this.open = true;
      return;
    }
    this.open = false;
    openDropdowns.delete(this);
    unregisterDismissible(this);
    this.syncAriaAttributes();
    document.removeEventListener("keydown", this.handleDocumentKeyDown);
    document.removeEventListener("pointerdown", this.handleDocumentPointerDown);
    document.removeEventListener("mousemove", this.handleGlobalMouseMove);
    this.menu.classList.remove("show");
    await animateWithClass(this.menu, "hide");
    this.popup.active = this.open;
    this.dispatchEvent(new WaAfterHideEvent());
  }
  /** Handles clicks on the menu. */
  handleMenuClick(event) {
    const item = event.target.closest("wa-dropdown-item");
    if (!item || item.disabled) return;
    if (item.hasSubmenu) {
      if (!item.submenuOpen) {
        this.closeSiblingSubmenus(item);
        this.addToSubmenuStack(item);
        item.submenuOpen = true;
      }
      event.stopPropagation();
      return;
    }
    this.makeSelection(item);
  }
  /** Prepares dropdown items when they get added or removed */
  async handleMenuSlotChange() {
    const items = this.getItems(true);
    await Promise.all(items.map((item) => item.updateComplete));
    this.syncItemSizes();
    const hasCheckbox = items.some((item) => item.type === "checkbox");
    const hasSubmenu = items.some((item) => item.hasSubmenu);
    items.forEach((item, index) => {
      item.active = index === 0;
      item.checkboxAdjacent = hasCheckbox;
      item.submenuAdjacent = hasSubmenu;
    });
  }
  /** Toggles the dropdown menu */
  handleTriggerClick() {
    this.open = !this.open;
  }
  /** Handles submenu opening events */
  handleSubmenuOpening(event) {
    const openingItem = event.detail.item;
    this.closeSiblingSubmenus(openingItem);
    this.addToSubmenuStack(openingItem);
    this.setupSubmenuPosition(openingItem);
    this.processSubmenuItems(openingItem);
  }
  /** Sets up submenu positioning with autoUpdate */
  setupSubmenuPosition(item) {
    if (!item.submenuElement) return;
    this.cleanupSubmenuPosition(item);
    const cleanup = autoUpdate(item, item.submenuElement, () => {
      this.positionSubmenu(item);
      this.updateSafeTriangleCoordinates(item);
    });
    this.submenuCleanups.set(item, cleanup);
    const submenuSlot = item.submenuElement.querySelector('slot[name="submenu"]');
    if (submenuSlot) {
      submenuSlot.removeEventListener("slotchange", WaDropdown.handleSubmenuSlotChange);
      submenuSlot.addEventListener("slotchange", WaDropdown.handleSubmenuSlotChange);
      WaDropdown.handleSubmenuSlotChange({ target: submenuSlot });
    }
  }
  static handleSubmenuSlotChange(event) {
    const slot = event.target;
    if (!slot) return;
    const items = slot.assignedElements().filter((el) => el.localName === "wa-dropdown-item");
    if (items.length === 0) return;
    const hasSubmenuItems = items.some((item) => item.hasSubmenu);
    const hasCheckboxItems = items.some((item) => item.type === "checkbox");
    items.forEach((item) => {
      item.submenuAdjacent = hasSubmenuItems;
      item.checkboxAdjacent = hasCheckboxItems;
    });
  }
  processSubmenuItems(item) {
    if (!item.submenuElement) return;
    const submenuItems = this.getSubmenuItems(item, true);
    const hasSubmenuItems = submenuItems.some((subItem) => subItem.hasSubmenu);
    submenuItems.forEach((subItem) => {
      subItem.submenuAdjacent = hasSubmenuItems;
    });
  }
  /** Cleans up submenu positioning */
  cleanupSubmenuPosition(item) {
    const cleanup = this.submenuCleanups.get(item);
    if (cleanup) {
      cleanup();
      this.submenuCleanups.delete(item);
    }
  }
  /** Positions a submenu relative to its parent item */
  positionSubmenu(item) {
    if (!item.submenuElement) return;
    const isRtl = this.localize.dir() === "rtl";
    const placement = isRtl ? "left-start" : "right-start";
    computePosition(item, item.submenuElement, {
      placement,
      middleware: [
        offset({
          mainAxis: 0,
          crossAxis: -5
        }),
        flip({
          fallbackStrategy: "bestFit"
        }),
        shift({
          padding: 8
        })
      ]
    }).then(({ x: x2, y, placement: placement2 }) => {
      item.submenuElement.setAttribute("data-placement", placement2);
      Object.assign(item.submenuElement.style, {
        left: `${x2}px`,
        top: `${y}px`
      });
    });
  }
  /** Updates the safe triangle coordinates for a submenu */
  updateSafeTriangleCoordinates(item) {
    if (!item.submenuElement || !item.submenuOpen) return;
    const isKeyboardNavigation = document.activeElement?.matches(":focus-visible");
    if (isKeyboardNavigation) {
      item.submenuElement.style.setProperty("--safe-triangle-visible", "none");
      return;
    }
    item.submenuElement.style.setProperty("--safe-triangle-visible", "block");
    const submenuRect = item.submenuElement.getBoundingClientRect();
    const isRtl = this.localize.dir() === "rtl";
    item.submenuElement.style.setProperty(
      "--safe-triangle-submenu-start-x",
      `${isRtl ? submenuRect.right : submenuRect.left}px`
    );
    item.submenuElement.style.setProperty("--safe-triangle-submenu-start-y", `${submenuRect.top}px`);
    item.submenuElement.style.setProperty(
      "--safe-triangle-submenu-end-x",
      `${isRtl ? submenuRect.right : submenuRect.left}px`
    );
    item.submenuElement.style.setProperty("--safe-triangle-submenu-end-y", `${submenuRect.bottom}px`);
  }
  /** Makes a selection, emits the wa-select event, and closes the dropdown. */
  makeSelection(item) {
    const trigger = this.getTrigger();
    if (item.disabled) {
      return;
    }
    if (item.type === "checkbox") {
      item.checked = !item.checked;
    }
    const selectEvent = new WaSelectEvent({ item });
    this.dispatchEvent(selectEvent);
    if (!selectEvent.defaultPrevented) {
      this.open = false;
      trigger?.focus({ preventScroll: true });
    }
  }
  /** Syncs aria attributes on the slotted trigger element and the menu based on the dropdown's current state */
  async syncAriaAttributes() {
    const trigger = this.getTrigger();
    let nativeButton;
    if (!trigger) {
      return;
    }
    if (trigger.localName === "wa-button") {
      await customElements.whenDefined("wa-button");
      await trigger.updateComplete;
      nativeButton = trigger.shadowRoot.querySelector('[part="base"]');
    } else {
      nativeButton = trigger;
    }
    if (!nativeButton.hasAttribute("id")) {
      nativeButton.setAttribute("id", uniqueId("wa-dropdown-trigger-"));
    }
    nativeButton.setAttribute("aria-haspopup", "menu");
    nativeButton.setAttribute("aria-expanded", this.open ? "true" : "false");
    this.menu?.setAttribute("aria-expanded", "false");
  }
  render() {
    let active = this.hasUpdated ? this.popup?.active : this.open;
    return x`
      <wa-popup
        placement=${this.placement}
        distance=${this.distance}
        skidding=${this.skidding}
        ?active=${active}
        flip
        flip-fallback-strategy="best-fit"
        shift
        shift-padding="10"
        auto-size="vertical"
        auto-size-padding="10"
      >
        <slot
          name="trigger"
          slot="anchor"
          @click=${this.handleTriggerClick}
          @slotchange=${this.syncAriaAttributes}
        ></slot>
        <div
          id="menu"
          part="menu"
          role="menu"
          tabindex="-1"
          aria-orientation="vertical"
          @click=${this.handleMenuClick}
          @submenu-opening=${this.handleSubmenuOpening}
        >
          <slot @slotchange=${this.handleMenuSlotChange}></slot>
        </div>
      </wa-popup>
    `;
  }
};
WaDropdown.css = [size_styles_default, dropdown_styles_default];
__decorateClass([
  e("slot:not([name])")
], WaDropdown.prototype, "defaultSlot", 2);
__decorateClass([
  e("#menu")
], WaDropdown.prototype, "menu", 2);
__decorateClass([
  e("wa-popup")
], WaDropdown.prototype, "popup", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaDropdown.prototype, "open", 2);
__decorateClass([
  n({ reflect: true })
], WaDropdown.prototype, "size", 2);
__decorateClass([
  n({ reflect: true })
], WaDropdown.prototype, "placement", 2);
__decorateClass([
  n({ type: Number })
], WaDropdown.prototype, "distance", 2);
__decorateClass([
  n({ type: Number })
], WaDropdown.prototype, "skidding", 2);
WaDropdown = __decorateClass([
  t("wa-dropdown")
], WaDropdown);

export {
  WaDropdown
};
