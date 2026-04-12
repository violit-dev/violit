/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  getBasePath
} from "./chunk.HGBRCPUS.js";

// src/utilities/autoloader.ts
var observer = new MutationObserver((mutations) => {
  for (const { addedNodes } of mutations) {
    for (const node of addedNodes) {
      if (node.nodeType === Node.ELEMENT_NODE) {
        discover(node);
      }
    }
  }
});
function startLoader() {
  discover(document);
  observer.observe(document.documentElement, { subtree: true, childList: true });
}
function stopLoader() {
  observer.disconnect();
}
async function discover(root) {
  const rootTagName = root instanceof Element ? root.tagName.toLowerCase() : "";
  const rootIsWebAwesomeComponent = rootTagName?.startsWith("wa-");
  const tags = [...root.querySelectorAll(":not(:defined)")].map((el) => el.tagName.toLowerCase()).filter((tag) => tag.startsWith("wa-"));
  if (rootIsWebAwesomeComponent && !customElements.get(rootTagName)) {
    tags.push(rootTagName);
  }
  const preloadSelectors = root.querySelectorAll("[data-wa-preload]");
  const preloadRoots = root instanceof Element && root.hasAttribute("data-wa-preload") ? [root, ...preloadSelectors] : preloadSelectors;
  for (const el of preloadRoots) {
    tags.push(
      ...el.getAttribute("data-wa-preload").split(/\s+/).filter((tag) => tag.startsWith("wa-"))
    );
  }
  const tagsToRegister = [...new Set(tags)];
  const imports = await Promise.allSettled(tagsToRegister.map((tagName) => register(tagName)));
  for (const imp of imports) {
    if (imp.status === "rejected") {
      console.warn(imp.reason);
    }
  }
  await new Promise(requestAnimationFrame);
  root.dispatchEvent(
    new CustomEvent("wa-discovery-complete", {
      bubbles: false,
      cancelable: false,
      composed: true
    })
  );
}
function register(tagName) {
  if (customElements.get(tagName)) {
    return Promise.resolve();
  }
  const tagWithoutPrefix = tagName.replace(/^wa-/i, "");
  const path = getBasePath(`components/${tagWithoutPrefix}/${tagWithoutPrefix}.js`);
  return new Promise((resolve, reject) => {
    import(path).then(() => resolve()).catch(() => reject(new Error(`Unable to autoload <${tagName}> from ${path}`)));
  });
}
function preventTurboFouce(timeout = 2e3) {
  document.addEventListener("turbo:before-render", async (event) => {
    const newBody = event.detail.newBody;
    event.preventDefault();
    try {
      await Promise.race([discover(newBody), new Promise((resolve) => setTimeout(resolve, timeout))]);
    } finally {
      event.detail.resume();
    }
  });
}

export {
  startLoader,
  stopLoader,
  discover,
  preventTurboFouce
};
