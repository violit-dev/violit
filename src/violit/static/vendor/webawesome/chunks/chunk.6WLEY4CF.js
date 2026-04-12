/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  startLoader
} from "./chunk.RSUSAXIB.js";

// src/webawesome.loader.ts
startLoader();
Promise.race([
  new Promise((resolve) => document.addEventListener("wa-discovery-complete", resolve)),
  new Promise((resolve) => setTimeout(resolve, 2e3))
]).then(() => {
  document.querySelectorAll(".wa-cloak").forEach((el) => el.classList.remove("wa-cloak"));
});
