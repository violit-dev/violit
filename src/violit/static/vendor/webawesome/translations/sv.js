/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/sv.ts
var translation = {
  $code: "sv",
  $name: "Svenska",
  $dir: "ltr",
  carousel: "Karusell",
  clearEntry: "\xC5terst\xE4ll val",
  createOption: (value) => `Skapa "${value}"`,
  close: "St\xE4ng",
  copied: "Kopierade",
  copy: "Kopiera",
  currentValue: "Nuvarande v\xE4rde",
  decrement: "Minska",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Fel",
  goToSlide: (slide, count) => `G\xE5 till bild ${slide} av ${count}`,
  hidePassword: "D\xF6lj l\xF6senord",
  increment: "\xD6ka",
  loading: "L\xE4ser in",
  nextSlide: "N\xE4sta bild",
  numCharacters: (num) => {
    if (num === 1) return "1 tecken";
    return `${num} tecken`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 tecken kvar";
    return `${num} tecken kvar`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Inga alternativ har valts";
    if (num === 1) return "1 alternativ valt";
    return `${num} alternativ valda`;
  },
  pauseAnimation: "Pausa animation",
  playAnimation: "Spela upp animation",
  previousSlide: "F\xF6reg\xE5ende bild",
  progress: "Framsteg",
  remove: "Ta bort",
  resize: "\xC4ndra storlek",
  scrollableRegion: "Scrollbart omr\xE5de",
  scrollToEnd: "Skrolla till slutet",
  scrollToStart: "Skrolla till b\xF6rjan",
  selectAColorFromTheScreen: "V\xE4lj en f\xE4rg fr\xE5n sk\xE4rmen",
  showPassword: "Visa l\xF6senord",
  slideNum: (slide) => `Bild ${slide}`,
  toggleColorFormat: "V\xE4xla f\xE4rgformat",
  zoomIn: "Zooma in",
  zoomOut: "Zooma ut"
};
registerTranslation(translation);
var sv_default = translation;
export {
  sv_default as default
};
