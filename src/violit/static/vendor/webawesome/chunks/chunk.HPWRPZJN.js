/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  o
} from "./chunk.BQNDCXAL.js";
import {
  WaErrorEvent
} from "./chunk.YDQCS2HK.js";
import {
  WaLoadEvent
} from "./chunk.WDIIGUNP.js";
import {
  LocalizeController
} from "./chunk.G3ZVQTTB.js";
import {
  animated_image_styles_default
} from "./chunk.O6YZRY24.js";
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

// src/components/animated-image/animated-image.ts
var WaAnimatedImage = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.localize = new LocalizeController(this);
    this.isLoaded = false;
  }
  handleClick() {
    this.play = !this.play;
  }
  handleKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      this.play = !this.play;
    }
  }
  handleLoad() {
    const canvas = document.createElement("canvas");
    const { width, height } = this.animatedImage;
    canvas.width = width;
    canvas.height = height;
    canvas.getContext("2d").drawImage(this.animatedImage, 0, 0, width, height);
    this.frozenFrame = canvas.toDataURL("image/gif");
    if (!this.isLoaded) {
      this.dispatchEvent(new WaLoadEvent());
      this.isLoaded = true;
    }
  }
  handleError() {
    this.dispatchEvent(new WaErrorEvent());
  }
  handlePlayChange() {
    if (this.play) {
      this.animatedImage.src = "";
      this.animatedImage.src = this.src;
    }
  }
  handleSrcChange() {
    this.isLoaded = false;
  }
  render() {
    const verb = this.localize.term(this.play ? "pauseAnimation" : "playAnimation");
    const label = `${verb} ${this.alt}`;
    return x`
      <div
        class="animated-image"
        tabindex="0"
        role="button"
        aria-pressed=${this.play ? "true" : "false"}
        aria-label=${label}
        @click=${this.handleClick}
        @keydown=${this.handleKeyDown}
      >
        <img
          class="animated"
          src=${this.src}
          alt=${this.alt}
          crossorigin="anonymous"
          aria-hidden=${this.play ? "false" : "true"}
          role="presentation"
          @load=${this.handleLoad}
          @error=${this.handleError}
        />

        ${this.isLoaded ? x`
              <img
                class="frozen"
                src=${this.frozenFrame}
                alt=${this.alt}
                aria-hidden=${this.play ? "true" : "false"}
                role="presentation"
              />

              <div part="control-box" class="control-box" aria-hidden="true">
                <slot name="play-icon">
                  <wa-icon
                    name="play"
                    library="system"
                    variant="solid"
                    class="default"
                    style=${o({ "margin-inline-start": "3px" })}
                  ></wa-icon>
                </slot>
                <slot name="pause-icon">
                  <wa-icon name="pause" library="system" variant="solid" class="default"></wa-icon>
                </slot>
              </div>
            ` : ""}
      </div>
    `;
  }
};
WaAnimatedImage.css = animated_image_styles_default;
__decorateClass([
  e(".animated")
], WaAnimatedImage.prototype, "animatedImage", 2);
__decorateClass([
  r()
], WaAnimatedImage.prototype, "frozenFrame", 2);
__decorateClass([
  r()
], WaAnimatedImage.prototype, "isLoaded", 2);
__decorateClass([
  n()
], WaAnimatedImage.prototype, "src", 2);
__decorateClass([
  n()
], WaAnimatedImage.prototype, "alt", 2);
__decorateClass([
  n({ type: Boolean, reflect: true })
], WaAnimatedImage.prototype, "play", 2);
__decorateClass([
  watch("play", { waitUntilFirstUpdate: true })
], WaAnimatedImage.prototype, "handlePlayChange", 1);
__decorateClass([
  watch("src")
], WaAnimatedImage.prototype, "handleSrcChange", 1);
WaAnimatedImage = __decorateClass([
  t("wa-animated-image")
], WaAnimatedImage);

export {
  WaAnimatedImage
};
