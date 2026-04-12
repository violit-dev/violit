/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "./chunks/chunk.6WLEY4CF.js";
import "./chunks/chunk.D5YFE5NT.js";
import "./chunks/chunk.N2TXQSKF.js";
import {
  allDefined
} from "./chunks/chunk.X55YNZ3B.js";
import {
  serialize
} from "./chunks/chunk.LRYJ2M5H.js";
import "./chunks/chunk.KBS6YHTA.js";
import {
  discover,
  preventTurboFouce,
  startLoader,
  stopLoader
} from "./chunks/chunk.RSUSAXIB.js";
import {
  t
} from "./chunks/chunk.H23DVATU.js";
import {
  e,
  f,
  i,
  l
} from "./chunks/chunk.T3OVPJUT.js";
import "./chunks/chunk.G3ZVQTTB.js";
import "./chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "./chunks/chunk.HPOJN4W7.js";
import {
  getDefaultIconFamily,
  registerIconLibrary,
  setDefaultIconFamily,
  unregisterIconLibrary
} from "./chunks/chunk.S6RZOJNM.js";
import "./chunks/chunk.KPN3YZ6U.js";
import {
  getIconFolder
} from "./chunks/chunk.HCXBOJYW.js";
import {
  getBasePath,
  getIconPath,
  getKitCode,
  setBasePath,
  setIconPath,
  setKitCode
} from "./chunks/chunk.HGBRCPUS.js";
import {
  B,
  T,
  Z
} from "./chunks/chunk.BKE5EYM3.js";
import {
  getAnimationNames,
  getEasingNames
} from "./chunks/chunk.LN7M2NWC.js";
import "./chunks/chunk.JHZRD2LV.js";

// ../../node_modules/lit-html/private-ssr-support.js
var r = null;
var i2 = { boundAttributeSuffix: Z.M, marker: Z.P, markerMatch: Z.A, HTML_RESULT: Z.C, getTemplateHtml: Z.L, overrideDirectiveResolve: (e2, t2) => class extends e2 {
  _$AS(e3, r2) {
    return t2(this, r2);
  }
}, patchDirectiveResolve: (e2, t2) => {
  if (e2.prototype._$AS !== t2) {
    r ?? (r = e2.prototype._$AS.name);
    for (let i3 = e2.prototype; i3 !== Object.prototype; i3 = Object.getPrototypeOf(i3)) if (i3.hasOwnProperty(r)) return void (i3[r] = t2);
    throw Error("Internal error: It is possible that both dev mode and production mode Lit was mixed together during SSR. Please comment on the issue: https://github.com/lit/lit/issues/4527");
  }
}, setDirectiveClass(e2, t2) {
  e2._$litDirective$ = t2;
}, getAttributePartCommittedValue: (e2, r2, i3) => {
  let o = T;
  return e2.j = (e3) => o = e3, e2._$AI(r2, e2, i3), o;
}, connectedDisconnectable: (e2) => ({ ...e2, _$AU: true }), resolveDirective: Z.V, AttributePart: Z.H, PropertyPart: Z.B, BooleanAttributePart: Z.N, EventPart: Z.U, ElementPart: Z.F, TemplateInstance: Z.R, isIterable: Z.D, ChildPart: Z.I };

// ../../node_modules/@lit-labs/ssr-client/lib/hydrate-lit-html.js
var { TemplateInstance: l2, isIterable: s, resolveDirective: d, ChildPart: c, ElementPart: p } = i2;
var f2 = (e2, t2, r2 = {}) => {
  if (void 0 !== t2._$litPart$) throw Error("container already contains a live render");
  let n, o, i3;
  const a = [], l3 = document.createTreeWalker(t2, NodeFilter.SHOW_COMMENT);
  let s2;
  for (; null !== (s2 = l3.nextNode()); ) {
    const t3 = s2.data;
    if (t3.startsWith("lit-part")) {
      if (0 === a.length && void 0 !== n) throw Error(`There must be only one root part per container. Found a part marker (${s2}) when we already have a root part marker (${o})`);
      i3 = m(e2, s2, a, r2), void 0 === n && (n = i3), o ?? (o = s2);
    } else if (t3.startsWith("lit-node")) u(s2, a, r2);
    else if (t3.startsWith("/lit-part")) {
      if (1 === a.length && i3 !== n) throw Error("internal error");
      i3 = h(s2, i3, a);
    }
  }
  if (void 0 === n) {
    const e3 = t2 instanceof ShadowRoot ? "{container.host.localName}'s shadow root" : t2 instanceof DocumentFragment ? "DocumentFragment" : t2.localName;
    console.error(`There should be exactly one root part in a render container, but we didn't find any in ${e3}.`);
  }
  t2._$litPart$ = n;
};
var m = (t2, r2, a, p2) => {
  let f3, m2;
  if (0 === a.length) m2 = new c(r2, null, void 0, p2), f3 = t2;
  else {
    const e2 = a[a.length - 1];
    if ("template-instance" === e2.type) m2 = new c(r2, null, e2.instance, p2), e2.instance._$AV.push(m2), f3 = e2.result.values[e2.instancePartIndex++], e2.templatePartIndex++;
    else if ("iterable" === e2.type) {
      m2 = new c(r2, null, e2.part, p2);
      const t3 = e2.iterator.next();
      if (t3.done) throw f3 = void 0, e2.done = true, Error("Unhandled shorter than expected iterable");
      f3 = t3.value, e2.part._$AH.push(m2);
    } else m2 = new c(r2, null, e2.part, p2);
  }
  if (f3 = d(m2, f3), f3 === T) a.push({ part: m2, type: "leaf" });
  else if (i(f3)) a.push({ part: m2, type: "leaf" }), m2._$AH = f3;
  else if (e(f3)) {
    if (l(f3)) throw Error("compiled templates are not supported");
    const e2 = "lit-part " + w(f3);
    if (r2.data !== e2) throw Error("Hydration value mismatch: Unexpected TemplateResult rendered to part");
    {
      const e3 = c.prototype._$AC(f3), t3 = new l2(e3, m2);
      a.push({ type: "template-instance", instance: t3, part: m2, templatePartIndex: 0, instancePartIndex: 0, result: f3 }), m2._$AH = t3;
    }
  } else s(f3) ? (a.push({ part: m2, type: "iterable", value: f3, iterator: f3[Symbol.iterator](), done: false }), m2._$AH = []) : (a.push({ part: m2, type: "leaf" }), m2._$AH = f3 ?? "");
  return m2;
};
var h = (e2, t2, r2) => {
  if (void 0 === t2) throw Error("unbalanced part marker");
  t2._$AB = e2;
  const n = r2.pop();
  if ("iterable" === n.type && !n.iterator.next().done) throw Error("unexpected longer than expected iterable");
  if (r2.length > 0) return r2[r2.length - 1].part;
};
var u = (e2, t2, n) => {
  const o = /lit-node (\d+)/.exec(e2.data), i3 = parseInt(o[1]), l3 = e2.nextElementSibling;
  if (null === l3) throw Error("could not find node for attribute parts");
  l3.removeAttribute("defer-hydration");
  const s2 = t2[t2.length - 1];
  if ("template-instance" !== s2.type) throw Error("Hydration value mismatch: Primitive found where TemplateResult expected. This usually occurs due to conditional rendering that resulted in a different value or template being rendered between the server and client.");
  {
    const e3 = s2.instance;
    for (; ; ) {
      const t3 = e3._$AD.parts[s2.templatePartIndex];
      if (void 0 === t3 || t3.type !== t.ATTRIBUTE && t3.type !== t.ELEMENT || t3.index !== i3) break;
      if (t3.type === t.ATTRIBUTE) {
        const o2 = new t3.ctor(l3, t3.name, t3.strings, s2.instance, n), i4 = f(o2) ? s2.result.values[s2.instancePartIndex] : s2.result.values, d2 = !(o2.type === t.EVENT || o2.type === t.PROPERTY);
        o2._$AI(i4, o2, s2.instancePartIndex, d2), s2.instancePartIndex += t3.strings.length - 1, e3._$AV.push(o2);
      } else {
        const t4 = new p(l3, s2.instance, n);
        d(t4, s2.result.values[s2.instancePartIndex++]), e3._$AV.push(t4);
      }
      s2.templatePartIndex++;
    }
  }
};
var w = (e2) => {
  const t2 = new Uint32Array(2).fill(5381);
  for (const r3 of e2.strings) for (let e3 = 0; e3 < r3.length; e3++) t2[e3 % 2] = 33 * t2[e3 % 2] ^ r3.charCodeAt(e3);
  const r2 = String.fromCharCode(...new Uint8Array(t2.buffer));
  return btoa(r2);
};

// ../../node_modules/@lit-labs/ssr-client/lit-element-hydrate-support.js
globalThis.litElementHydrateSupport = ({ LitElement: s2 }) => {
  const h2 = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(s2), "observedAttributes").get;
  Object.defineProperty(s2, "observedAttributes", { get() {
    return [...h2.call(this), "defer-hydration"];
  } });
  const e2 = s2.prototype.attributeChangedCallback;
  s2.prototype.attributeChangedCallback = function(t2, i3, s3) {
    "defer-hydration" === t2 && null === s3 && n.call(this), e2.call(this, t2, i3, s3);
  };
  const n = s2.prototype.connectedCallback;
  s2.prototype.connectedCallback = function() {
    this.hasAttribute("defer-hydration") || n.call(this);
  };
  const o = s2.prototype.createRenderRoot;
  s2.prototype.createRenderRoot = function() {
    return this.shadowRoot ? (this._$AG = true, this.shadowRoot) : o.call(this);
  };
  const r2 = Object.getPrototypeOf(s2.prototype).update;
  s2.prototype.update = function(s3) {
    const h3 = this.render();
    if (r2.call(this, s3), this._$AG) {
      this._$AG = false;
      for (let t2 = 0; t2 < this.attributes.length; t2++) {
        const i3 = this.attributes[t2];
        if (i3.name.startsWith("hydrate-internals-")) {
          const t3 = i3.name.slice(18);
          this.removeAttribute(t3), this.removeAttribute(i3.name);
        }
      }
      f2(h3, this.renderRoot, this.renderOptions);
    } else B(h3, this.renderRoot, this.renderOptions);
  };
};
export {
  allDefined,
  discover,
  getAnimationNames,
  getBasePath,
  getDefaultIconFamily,
  getEasingNames,
  getIconFolder,
  getIconPath,
  getKitCode,
  preventTurboFouce,
  registerIconLibrary,
  registerTranslation,
  serialize,
  setBasePath,
  setDefaultIconFamily,
  setIconPath,
  setKitCode,
  startLoader,
  stopLoader,
  unregisterIconLibrary
};
/*! Bundled license information:

lit-html/private-ssr-support.js:
@lit-labs/ssr-client/lib/hydrate-lit-html.js:
  (**
   * @license
   * Copyright 2019 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)
*/
