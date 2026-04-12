/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/nb.ts
var translation = {
  $code: "nb",
  $name: "Norwegian Bokm\xE5l",
  $dir: "ltr",
  carousel: "Karusell",
  clearEntry: "T\xF8m felt",
  createOption: (value) => `Opprett "${value}"`,
  close: "Lukk",
  copied: "Kopiert",
  copy: "Kopier",
  currentValue: "N\xE5v\xE6rende verdi",
  decrement: "Reduser",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Feil",
  goToSlide: (slide, count) => `G\xE5 til visning ${slide} av ${count}`,
  hidePassword: "Skjul passord",
  increment: "\xD8k",
  loading: "Laster",
  nextSlide: "Neste visning",
  numCharacters: (num) => {
    if (num === 1) return "1 tegn";
    return `${num} tegn`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 tegn gjenst\xE5r";
    return `${num} tegn gjenst\xE5r`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Ingen alternativer valgt";
    if (num === 1) return "Ett alternativ valgt";
    return `${num} alternativer valgt`;
  },
  pauseAnimation: "Sett animasjon p\xE5 pause",
  playAnimation: "Spill av animasjon",
  previousSlide: "Forrige visning",
  progress: "Fremdrift",
  remove: "Fjern",
  resize: "Endre st\xF8rrelse",
  scrollableRegion: "Rullbar region",
  scrollToEnd: "Rull til slutten",
  scrollToStart: "Rull til starten",
  selectAColorFromTheScreen: "Velg en farge fra skjermen",
  showPassword: "Vis passord",
  slideNum: (slide) => `Visning ${slide}`,
  toggleColorFormat: "Bytt fargeformat",
  zoomIn: "Zoom inn",
  zoomOut: "Zoom ut"
};
registerTranslation(translation);
var nb_default = translation;
export {
  nb_default as default
};
