/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  registerTranslation
} from "./chunk.HPOJN4W7.js";

// src/translations/de.ts
var translation = {
  $code: "de",
  $name: "Deutsch",
  $dir: "ltr",
  carousel: "Karussell",
  clearEntry: "Eingabe l\xF6schen",
  createOption: (value) => `\u201E${value}" erstellen`,
  close: "Schlie\xDFen",
  copied: "Kopiert",
  copy: "Kopieren",
  currentValue: "Aktueller Wert",
  decrement: "Verringern",
  dropFileHere: "Datei hier ablegen oder zum Durchsuchen klicken",
  dropFilesHere: "Dateien hier ablegen oder zum Durchsuchen klicken",
  error: "Fehler",
  goToSlide: (slide, count) => `Zu Folie ${slide} von ${count} gehen`,
  hidePassword: "Passwort verbergen",
  increment: "Erh\xF6hen",
  loading: "Wird geladen",
  nextSlide: "N\xE4chste Folie",
  numCharacters: (num) => {
    if (num === 1) return "1 Zeichen";
    return `${num} Zeichen`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 Zeichen verbleibend";
    return `${num} Zeichen verbleibend`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Keine Optionen ausgew\xE4hlt";
    if (num === 1) return "1 Option ausgew\xE4hlt";
    return `${num} Optionen ausgew\xE4hlt`;
  },
  pauseAnimation: "Animation pausieren",
  playAnimation: "Animation abspielen",
  previousSlide: "Vorherige Folie",
  progress: "Fortschritt",
  remove: "Entfernen",
  resize: "Gr\xF6\xDFe \xE4ndern",
  scrollableRegion: "Scrollbarer Bereich",
  scrollToEnd: "Zum Ende scrollen",
  scrollToStart: "Zum Anfang scrollen",
  selectAColorFromTheScreen: "Farbe vom Bildschirm ausw\xE4hlen",
  showPassword: "Passwort anzeigen",
  slideNum: (slide) => `Folie ${slide}`,
  toggleColorFormat: "Farbformat wechseln",
  zoomIn: "Hineinzoomen",
  zoomOut: "Herauszoomen"
};
registerTranslation(translation);
var de_default = translation;

export {
  de_default
};
