/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/utilities/defined.ts
async function allDefined(options) {
  const opts = {
    match: (tagName) => tagName.startsWith("wa-"),
    additionalElements: [],
    root: document,
    ...options
  };
  const additionalElements = Array.isArray(opts.additionalElements) ? opts.additionalElements : [opts.additionalElements];
  const undefinedElements = [...opts.root.querySelectorAll(":not(:defined)")].map((el) => el.localName).filter((tag, index, arr) => arr.indexOf(tag) === index).filter((tag) => opts.match(tag));
  const tagsToAwait = [...undefinedElements, ...additionalElements];
  await Promise.all(tagsToAwait.map((tag) => customElements.whenDefined(tag)));
  await new Promise(requestAnimationFrame);
}

export {
  allDefined
};
