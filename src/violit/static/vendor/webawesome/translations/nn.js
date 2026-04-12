/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/nn.ts
var translation = {
  $code: "nn",
  $name: "Norwegian Nynorsk",
  $dir: "ltr",
  carousel: "Karusell",
  clearEntry: "T\xF8m felt",
  createOption: (value) => `Opprett "${value}"`,
  close: "Lukk",
  copied: "Kopiert",
  copy: "Kopier",
  currentValue: "N\xE5verande verdi",
  decrement: "Reduser",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Feil",
  goToSlide: (slide, count) => `G\xE5 til visning ${slide} av ${count}`,
  hidePassword: "G\xF8ym passord",
  increment: "Auk",
  loading: "Lastar",
  nextSlide: "Neste visning",
  numCharacters: (num) => {
    if (num === 1) return "1 teikn";
    return `${num} teikn`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 teikn att";
    return `${num} teikn att`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Ingen alternativ valt";
    if (num === 1) return "Eitt alternativ valt";
    return `${num} alternativ valt`;
  },
  pauseAnimation: "Set animasjon p\xE5 pause",
  playAnimation: "Spel av animasjon",
  previousSlide: "F\xF8rre visning",
  progress: "Framdrift",
  remove: "Fjern",
  resize: "Endre storleik",
  scrollableRegion: "Rullbar region",
  scrollToEnd: "Rull til slutten",
  scrollToStart: "Rull til starten",
  selectAColorFromTheScreen: "Vel ein farge fr\xE5 skjermen",
  showPassword: "Vis passord",
  slideNum: (slide) => `Visning ${slide}`,
  toggleColorFormat: "Byt fargeformat",
  zoomIn: "Zoom inn",
  zoomOut: "Zoom ut"
};
registerTranslation(translation);
var nn_default = translation;
export {
  nn_default as default
};
