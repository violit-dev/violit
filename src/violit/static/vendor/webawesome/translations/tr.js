/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/tr.ts
var translation = {
  $code: "tr",
  $name: "T\xFCrk\xE7e",
  $dir: "ltr",
  carousel: "Atl\u0131kar\u0131nca",
  clearEntry: "Giri\u015Fi sil",
  createOption: (value) => `"${value}" olu\u015Ftur`,
  close: "Kapat",
  copied: "Kopyaland\u0131",
  copy: "Kopya",
  currentValue: "Mevcut de\u011Fer",
  decrement: "Azalt",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Hata",
  goToSlide: (slide, count) => `${count} slayttan ${slide} slayta gidin`,
  hidePassword: "\u015Eifreyi sakla",
  increment: "Art\u0131r",
  loading: "Y\xFCkleme",
  nextSlide: "Sonraki slayt",
  numCharacters: (num) => {
    if (num === 1) return "1 karakter";
    return `${num} karakter`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 karakter kald\u0131";
    return `${num} karakter kald\u0131`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Hi\xE7bir se\xE7enek se\xE7ilmedi";
    if (num === 1) return "1 se\xE7enek se\xE7ildi";
    return `${num} se\xE7enek se\xE7ildi`;
  },
  pauseAnimation: "Animasyonu duraklat",
  playAnimation: "Animasyonu oynat",
  previousSlide: "Bir onceki slayt",
  progress: "\u0130lerleme",
  remove: "Kald\u0131r",
  resize: "Yeniden boyutland\u0131r",
  scrollableRegion: "Kayd\u0131r\u0131labilir alan",
  scrollToEnd: "Sona kay",
  scrollToStart: "Ba\u015Fa kay",
  selectAColorFromTheScreen: "Ekrandan bir renk se\xE7in",
  showPassword: "\u015Eifreyi g\xF6ster",
  slideNum: (slide) => `Slayt ${slide}`,
  toggleColorFormat: "Renk bi\xE7imini de\u011Fi\u015Ftir",
  zoomIn: "Yak\u0131nla\u015Ft\u0131r",
  zoomOut: "Uzakla\u015Ft\u0131r"
};
registerTranslation(translation);
var tr_default = translation;
export {
  tr_default as default
};
