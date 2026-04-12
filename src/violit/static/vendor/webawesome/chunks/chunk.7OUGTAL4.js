/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  breadcrumb_styles_default
} from "./chunk.2UDUPMFW.js";
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

// src/components/breadcrumb/breadcrumb.ts
var WaBreadcrumb = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.separatorDir = this.localize.dir();
    this.label = "";
  }
  // Generates a clone of the separator element to use for each breadcrumb item
  getSeparator() {
    const separator = this.separatorSlot.assignedElements({ flatten: true })[0];
    const clone = separator.cloneNode(true);
    [clone, ...clone.querySelectorAll("[id]")].forEach((el) => el.removeAttribute("id"));
    clone.setAttribute("data-default", "");
    clone.slot = "separator";
    return clone;
  }
  handleSlotChange() {
    const items = [...this.defaultSlot.assignedElements({ flatten: true })].filter(
      (item) => item.tagName.toLowerCase() === "wa-breadcrumb-item"
    );
    items.forEach((item, index) => {
      const separator = item.querySelector('[slot="separator"]');
      if (separator === null) {
        item.append(this.getSeparator());
      } else if (separator.hasAttribute("data-default")) {
        separator.replaceWith(this.getSeparator());
      } else {
      }
      if (index === items.length - 1) {
        item.setAttribute("aria-current", "page");
      } else {
        item.removeAttribute("aria-current");
      }
    });
  }
  render() {
    if (this.separatorDir !== this.localize.dir()) {
      this.separatorDir = this.localize.dir();
      this.updateComplete.then(() => this.handleSlotChange());
    }
    return x`
      <nav part="base" class="breadcrumb" aria-label=${this.label}>
        <slot @slotchange=${this.handleSlotChange}></slot>
      </nav>

      <span hidden aria-hidden="true">
        <slot name="separator">
          <wa-icon
            name=${this.localize.dir() === "rtl" ? "chevron-left" : "chevron-right"}
            library="system"
            variant="solid"
          ></wa-icon>
        </slot>
      </span>
    `;
  }
};
WaBreadcrumb.css = breadcrumb_styles_default;
__decorateClass([
  e("slot")
], WaBreadcrumb.prototype, "defaultSlot", 2);
__decorateClass([
  e('slot[name="separator"]')
], WaBreadcrumb.prototype, "separatorSlot", 2);
__decorateClass([
  n()
], WaBreadcrumb.prototype, "label", 2);
WaBreadcrumb = __decorateClass([
  t("wa-breadcrumb")
], WaBreadcrumb);

export {
  WaBreadcrumb
};
