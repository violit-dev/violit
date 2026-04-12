/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/id.ts
var translation = {
  $code: "id",
  $name: "Bahasa Indonesia",
  $dir: "ltr",
  carousel: "Karousel",
  clearEntry: "Hapus entri",
  createOption: (value) => `Buat "${value}"`,
  close: "Tutup",
  copied: "Disalin",
  copy: "Salin",
  currentValue: "Nilai saat ini",
  decrement: "Kurangi",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Kesalahan",
  goToSlide: (slide, count) => `Pergi ke slide ${slide} dari ${count}`,
  hidePassword: "Sembunyikan sandi",
  increment: "Tambah",
  loading: "Memuat",
  nextSlide: "Slide berikutnya",
  numCharacters: (num) => {
    if (num === 1) return "1 karakter";
    return `${num} karakter`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 karakter tersisa";
    return `${num} karakter tersisa`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Tidak ada opsi yang dipilih";
    if (num === 1) return "1 opsi yang dipilih";
    return `${num} opsi yang dipilih`;
  },
  pauseAnimation: "Jeda animasi",
  playAnimation: "Putar animasi",
  previousSlide: "Slide sebelumnya",
  progress: "Kemajuan",
  remove: "Hapus",
  resize: "Ubah ukuran",
  scrollableRegion: "Area yang dapat digulir",
  scrollToEnd: "Gulir ke akhir",
  scrollToStart: "Gulir ke awal",
  selectAColorFromTheScreen: "Pilih warna dari layar",
  showPassword: "Tampilkan sandi",
  slideNum: (slide) => `Slide ${slide}`,
  toggleColorFormat: "Beralih format warna",
  zoomIn: "Perbesar",
  zoomOut: "Perkecil"
};
registerTranslation(translation);
var id_default = translation;
export {
  id_default as default
};
