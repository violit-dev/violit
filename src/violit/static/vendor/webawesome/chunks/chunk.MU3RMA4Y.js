/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  WaIncludeErrorEvent
} from "./chunk.H7TA73OO.js";
import {
  include_styles_default
} from "./chunk.FDYDBGOC.js";
import {
  requestInclude
} from "./chunk.WGFDW2LC.js";
import {
  WaLoadEvent
} from "./chunk.WDIIGUNP.js";
import {
  watch
} from "./chunk.PZAN6FPN.js";
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

// src/components/include/include.ts
var WaInclude = class extends WebAwesomeElement {
  constructor() {
    super(...arguments);
    this.mode = "cors";
    this.allowScripts = false;
  }
  executeScript(script) {
    const newScript = document.createElement("script");
    [...script.attributes].forEach((attr) => newScript.setAttribute(attr.name, attr.value));
    newScript.textContent = script.textContent;
    script.parentNode.replaceChild(newScript, script);
  }
  async handleSrcChange() {
    try {
      const src = this.src;
      const file = await requestInclude(src, this.mode);
      if (src !== this.src) {
        return;
      }
      if (!file.ok) {
        this.dispatchEvent(new WaIncludeErrorEvent({ status: file.status }));
        return;
      }
      this.innerHTML = file.html;
      if (this.allowScripts) {
        [...this.querySelectorAll("script")].forEach((script) => this.executeScript(script));
      }
      this.dispatchEvent(new WaLoadEvent());
    } catch {
      this.dispatchEvent(new WaIncludeErrorEvent({ status: -1 }));
    }
  }
  render() {
    return x`<slot></slot>`;
  }
};
WaInclude.css = include_styles_default;
__decorateClass([
  n()
], WaInclude.prototype, "src", 2);
__decorateClass([
  n()
], WaInclude.prototype, "mode", 2);
__decorateClass([
  n({ attribute: "allow-scripts", type: Boolean })
], WaInclude.prototype, "allowScripts", 2);
__decorateClass([
  watch("src")
], WaInclude.prototype, "handleSrcChange", 1);
WaInclude = __decorateClass([
  t("wa-include")
], WaInclude);

export {
  WaInclude
};
