/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/hu.ts
var translation = {
  $code: "hu",
  $name: "Magyar",
  $dir: "ltr",
  carousel: "K\xF6rhinta",
  clearEntry: "Bejegyz\xE9s t\xF6rl\xE9se",
  createOption: (value) => `\u201E${value}" l\xE9trehoz\xE1sa`,
  close: "Bez\xE1r\xE1s",
  copied: "M\xE1solva",
  copy: "M\xE1sol\xE1s",
  currentValue: "Aktu\xE1lis \xE9rt\xE9k",
  decrement: "Cs\xF6kkent\xE9s",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Hiba",
  goToSlide: (slide, count) => `Ugr\xE1s a ${count}/${slide}. di\xE1ra`,
  hidePassword: "Jelsz\xF3 elrejt\xE9se",
  increment: "N\xF6vel\xE9s",
  loading: "Bet\xF6lt\xE9s",
  nextSlide: "K\xF6vetkez\u0151 dia",
  numCharacters: (num) => {
    if (num === 1) return "1 karakter";
    return `${num} karakter`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 karakter maradt";
    return `${num} karakter maradt`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Nincsenek kiv\xE1lasztva opci\xF3k";
    if (num === 1) return "1 lehet\u0151s\xE9g kiv\xE1lasztva";
    return `${num} lehet\u0151s\xE9g kiv\xE1lasztva`;
  },
  pauseAnimation: "Anim\xE1ci\xF3 sz\xFCneteltet\xE9se",
  playAnimation: "Anim\xE1ci\xF3 lej\xE1tsz\xE1sa",
  previousSlide: "El\u0151z\u0151 dia",
  progress: "Folyamat",
  remove: "Elt\xE1vol\xEDt\xE1s",
  resize: "\xC1tm\xE9retez\xE9s",
  scrollableRegion: "G\xF6rgethet\u0151 ter\xFClet",
  scrollToEnd: "G\xF6rgessen a v\xE9g\xE9re",
  scrollToStart: "G\xF6rgessen az elej\xE9re",
  selectAColorFromTheScreen: "Sz\xEDn v\xE1laszt\xE1sa a k\xE9perny\u0151r\u0151l",
  showPassword: "Jelsz\xF3 megjelen\xEDt\xE9se",
  slideNum: (slide) => `${slide}. dia`,
  toggleColorFormat: "Sz\xEDnform\xE1tum v\xE1ltoztat\xE1sa",
  zoomIn: "Nagy\xEDt\xE1s",
  zoomOut: "Kicsiny\xEDt\xE9s"
};
registerTranslation(translation);
var hu_default = translation;
export {
  hu_default as default
};
