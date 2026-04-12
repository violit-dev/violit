/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/da.ts
var translation = {
  $code: "da",
  $name: "Dansk",
  $dir: "ltr",
  carousel: "Karrusel",
  clearEntry: "Ryd indtastning",
  createOption: (value) => `Opret "${value}"`,
  close: "Luk",
  copied: "Kopieret",
  copy: "Kopier",
  currentValue: "Nuv\xE6rende v\xE6rdi",
  decrement: "Formindsk",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Fejl",
  goToSlide: (slide, count) => `G\xE5 til dias ${slide} af ${count}`,
  hidePassword: "Skjul adgangskode",
  increment: "For\xF8g",
  loading: "Indl\xE6ser",
  nextSlide: "N\xE6ste slide",
  numCharacters: (num) => {
    if (num === 1) return "1 tegn";
    return `${num} tegn`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 tegn tilbage";
    return `${num} tegn tilbage`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Ingen valgt";
    if (num === 1) return "1 valgt";
    return `${num} valgt`;
  },
  pauseAnimation: "Pause animation",
  playAnimation: "Afspil animation",
  previousSlide: "Forrige dias",
  progress: "Status",
  remove: "Fjern",
  resize: "Tilpas st\xF8rrelse",
  scrollableRegion: "Rullebar region",
  scrollToEnd: "Scroll til slut",
  scrollToStart: "Scroll til start",
  selectAColorFromTheScreen: "V\xE6lg en farve fra sk\xE6rmen",
  showPassword: "Vis adgangskode",
  slideNum: (slide) => `Slide ${slide}`,
  toggleColorFormat: "Skift farveformat",
  zoomIn: "Zoom ind",
  zoomOut: "Zoom ud"
};
registerTranslation(translation);
var da_default = translation;
export {
  da_default as default
};
