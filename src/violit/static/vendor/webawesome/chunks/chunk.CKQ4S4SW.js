/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  avatar_styles_default
} from "./chunk.4VXUYGRW.js";
import {
  WaErrorEvent
} from "./chunk.YDQCS2HK.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
import {
  WebAwesomeElement,
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

// src/components/avatar/avatar.ts
var WaAvatar = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.hasError = false;
    this.image = "";
    this.label = "";
    this.initials = "";
    this.loading = "eager";
    this.shape = "circle";
  }
  handleImageChange() {
    this.hasError = false;
  }
  handleImageLoadError() {
    this.hasError = true;
    this.dispatchEvent(new WaErrorEvent());
  }
  render() {
    const avatarWithImage = x`
      <img
        part="image"
        class="image"
        src="${this.image}"
        loading="${this.loading}"
        role="img"
        aria-label=${this.label}
        @error="${this.handleImageLoadError}"
      />
    `;
    let avatarWithoutImage = x``;
    if (this.initials) {
      avatarWithoutImage = x`<div part="initials" class="initials" role="img" aria-label=${this.label}>
        ${this.initials}
      </div>`;
    } else {
      avatarWithoutImage = x`
        <slot name="icon" part="icon" class="icon" role="img" aria-label=${this.label}>
          <wa-icon name="user" library="system" variant="solid"></wa-icon>
        </slot>
      `;
    }
    return x` ${this.image && !this.hasError ? avatarWithImage : avatarWithoutImage} `;
  }
};
WaAvatar.css = avatar_styles_default;
__decorateClass([
  r()
], WaAvatar.prototype, "hasError", 2);
__decorateClass([
  n()
], WaAvatar.prototype, "image", 2);
__decorateClass([
  n()
], WaAvatar.prototype, "label", 2);
__decorateClass([
  n()
], WaAvatar.prototype, "initials", 2);
__decorateClass([
  n()
], WaAvatar.prototype, "loading", 2);
__decorateClass([
  n({ reflect: true })
], WaAvatar.prototype, "shape", 2);
__decorateClass([
  watch("image")
], WaAvatar.prototype, "handleImageChange", 1);
WaAvatar = __decorateClass([
  t("wa-avatar")
], WaAvatar);

export {
  WaAvatar
};
