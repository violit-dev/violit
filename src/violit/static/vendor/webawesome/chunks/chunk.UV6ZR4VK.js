/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  card_styles_default
} from "./chunk.D2ESGZCU.js";
import {
  HasSlotController
} from "./chunk.KIHB3VMB.js";
import {
  size_styles_default
} from "./chunk.MEYJNQF4.js";
import {
  WebAwesomeElement,
  n,
  t
} from "./chunk.K4C5PQDP.js";
import {
  x
} from "./chunk.BKE5EYM3.js";
import {
  __decorateClass
} from "./chunk.JHZRD2LV.js";

// src/components/card/card.ts
var WaCard = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.hasSlotController = new HasSlotController(
      this,
      "footer",
      "header",
      "media",
      "header-actions",
      "footer-actions",
      "actions"
    );
    this.appearance = "outlined";
    this.withHeader = false;
    this.withMedia = false;
    this.withFooter = false;
    this.orientation = "vertical";
  }
  willUpdate() {
    if (!this.withHeader && this.hasSlotController.test("header")) this.withHeader = true;
    if (!this.withMedia && this.hasSlotController.test("media")) this.withMedia = true;
    if (!this.withFooter && this.hasSlotController.test("footer")) this.withFooter = true;
  }
  render() {
    if (this.orientation === "horizontal") {
      return x`
        <slot name="media" part="media" class="media"></slot>
        <div part="body" class="body"><slot></slot></div>
        <slot name="actions" part="actions" class="actions"></slot>
      `;
    }
    return x`
      <slot name="media" part="media" class="media"></slot>

      ${this.hasSlotController.test("header-actions") ? x` <header part="header" class="header has-actions">
            <slot name="header"></slot>
            <slot name="header-actions"></slot>
          </header>` : x` <header part="header" class="header">
            <slot name="header"></slot>
          </header>`}

      <div part="body" class="body"><slot></slot></div>
      ${this.hasSlotController.test("footer-actions") ? x` <footer part="footer" class="footer has-actions">
            <slot name="footer"></slot>
            <slot name="footer-actions"></slot>
          </footer>` : x` <footer part="footer" class="footer">
            <slot name="footer"></slot>
          </footer>`}
    `;
  }
};
WaCard.css = [size_styles_default, card_styles_default];
__decorateClass([
  n({ reflect: true })
], WaCard.prototype, "appearance", 2);
__decorateClass([
  n({ attribute: "with-header", type: Boolean, reflect: true })
], WaCard.prototype, "withHeader", 2);
__decorateClass([
  n({ attribute: "with-media", type: Boolean, reflect: true })
], WaCard.prototype, "withMedia", 2);
__decorateClass([
  n({ attribute: "with-footer", type: Boolean, reflect: true })
], WaCard.prototype, "withFooter", 2);
__decorateClass([
  n({ reflect: true })
], WaCard.prototype, "orientation", 2);
WaCard = __decorateClass([
  t("wa-card")
], WaCard);
WaCard.disableWarning?.("change-in-update");

export {
  WaCard
};
