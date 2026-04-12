/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o
} from "./chunk.3MSWQ3RG.js";
import {
  breadcrumb_item_styles_default
} from "./chunk.Z73FKN6X.js";
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

// src/components/breadcrumb-item/breadcrumb-item.ts
var WaBreadcrumbItem = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.renderType = "button";
    this.rel = "noreferrer noopener";
  }
  setRenderType() {
    const hasDropdown = this.defaultSlot.assignedElements({ flatten: true }).filter((i) => i.tagName.toLowerCase() === "wa-dropdown").length > 0;
    if (this.href) {
      this.renderType = "link";
      return;
    }
    if (hasDropdown) {
      this.renderType = "dropdown";
      return;
    }
    this.renderType = "button";
  }
  hrefChanged() {
    this.setRenderType();
  }
  handleSlotChange() {
    this.setRenderType();
  }
  render() {
    return x`
      <span part="start" class="start">
        <slot name="start"></slot>
      </span>

      ${this.renderType === "link" ? x`
            <a
              part="label"
              class="label label-link"
              href="${this.href}"
              target="${o(this.target ? this.target : void 0)}"
              rel=${o(this.target ? this.rel : void 0)}
            >
              <slot></slot>
            </a>
          ` : ""}
      ${this.renderType === "button" ? x`
            <button part="label" type="button" class="label label-button">
              <slot @slotchange=${this.handleSlotChange}></slot>
            </button>
          ` : ""}
      ${this.renderType === "dropdown" ? x`
            <div part="label" class="label label-dropdown">
              <slot @slotchange=${this.handleSlotChange}></slot>
            </div>
          ` : ""}

      <span part="end" class="end">
        <slot name="end"></slot>
      </span>

      <span part="separator" class="separator" aria-hidden="true">
        <slot name="separator"></slot>
      </span>
    `;
  }
};
WaBreadcrumbItem.css = breadcrumb_item_styles_default;
__decorateClass([
  e("slot:not([name])")
], WaBreadcrumbItem.prototype, "defaultSlot", 2);
__decorateClass([
  r()
], WaBreadcrumbItem.prototype, "renderType", 2);
__decorateClass([
  n()
], WaBreadcrumbItem.prototype, "href", 2);
__decorateClass([
  n()
], WaBreadcrumbItem.prototype, "target", 2);
__decorateClass([
  n()
], WaBreadcrumbItem.prototype, "rel", 2);
__decorateClass([
  watch("href", { waitUntilFirstUpdate: true })
], WaBreadcrumbItem.prototype, "hrefChanged", 1);
WaBreadcrumbItem = __decorateClass([
  t("wa-breadcrumb-item")
], WaBreadcrumbItem);

export {
  WaBreadcrumbItem
};
