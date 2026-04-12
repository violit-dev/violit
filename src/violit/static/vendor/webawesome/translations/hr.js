/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/hr.ts
var translation = {
  $code: "hr",
  $name: "Hrvatski",
  $dir: "ltr",
  carousel: "Vrtuljak",
  clearEntry: "O\u010Disti unos",
  createOption: (value) => `Stvori "${value}"`,
  close: "Zatvori",
  copied: "Kopirano",
  copy: "Kopiraj",
  currentValue: "Trenutna vrijednost",
  decrement: "Smanji",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Gre\u0161ka",
  goToSlide: (slide, count) => `Idi na slajd ${slide} od ${count}`,
  hidePassword: "Sakrij lozinku",
  increment: "Pove\u0107aj",
  loading: "U\u010Ditavanje",
  nextSlide: "Sljede\u0107i slajd",
  numCharacters: (num) => {
    if (num === 1) return "1 znak";
    const mod10 = num % 10;
    const mod100 = num % 100;
    if (mod10 >= 2 && mod10 <= 4 && !(mod100 >= 12 && mod100 <= 14)) return `${num} znaka`;
    return `${num} znakova`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 preostali znak";
    const mod10 = num % 10;
    const mod100 = num % 100;
    if (mod10 >= 2 && mod10 <= 4 && !(mod100 >= 12 && mod100 <= 14)) return `${num} preostala znaka`;
    return `${num} preostalih znakova`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Nije odabrana nijedna opcija";
    if (num === 1) return "1 opcija je odabrana";
    return `${num} odabranih opcija`;
  },
  pauseAnimation: "Pauziraj animaciju",
  playAnimation: "Reproduciraj animaciju",
  previousSlide: "Prethodni slajd",
  progress: "Napredak",
  remove: "Makni",
  resize: "Promijeni veli\u010Dinu",
  scrollableRegion: "Podru\u010Dje s mogu\u0107no\u0161\u0107u pomicanja",
  scrollToEnd: "Skrolaj do kraja",
  scrollToStart: "Skrolaj na po\u010Detak",
  selectAColorFromTheScreen: "Odaberi boju sa ekrana",
  showPassword: "Poka\u017Ei lozinku",
  slideNum: (slide) => `Slajd ${slide}`,
  toggleColorFormat: "Zamijeni format boje",
  zoomIn: "Pove\u0107aj",
  zoomOut: "Smanji"
};
registerTranslation(translation);
var hr_default = translation;
export {
  hr_default as default
};
