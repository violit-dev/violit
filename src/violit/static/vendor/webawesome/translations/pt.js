/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/pt.ts
var translation = {
  $code: "pt",
  $name: "Portugu\xEAs",
  $dir: "ltr",
  carousel: "Carrossel",
  clearEntry: "Limpar entrada",
  createOption: (value) => `Criar "${value}"`,
  close: "Fechar",
  copied: "Copiado",
  copy: "Copiar",
  currentValue: "Valor atual",
  decrement: "Diminuir",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Erro",
  goToSlide: (slide, count) => `V\xE1 para o slide ${slide} de ${count}`,
  hidePassword: "Esconder a senha",
  increment: "Aumentar",
  loading: "Carregando",
  nextSlide: "Pr\xF3ximo slide",
  numCharacters: (num) => {
    if (num === 1) return "1 caractere";
    return `${num} caracteres`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 caractere restante";
    return `${num} caracteres restantes`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "Nenhuma op\xE7\xE3o selecionada";
    if (num === 1) return "1 op\xE7\xE3o selecionada";
    return `${num} op\xE7\xF5es selecionadas`;
  },
  pauseAnimation: "Pausar anima\xE7\xE3o",
  playAnimation: "Reproduzir anima\xE7\xE3o",
  previousSlide: "Slide anterior",
  progress: "Progresso",
  remove: "Remover",
  resize: "Mudar o tamanho",
  scrollableRegion: "Regi\xE3o rol\xE1vel",
  scrollToEnd: "Rolar at\xE9 o final",
  scrollToStart: "Rolar at\xE9 o in\xEDcio",
  selectAColorFromTheScreen: "Selecionar uma cor da tela",
  showPassword: "Mostrar senha",
  slideNum: (slide) => `Slide ${slide}`,
  toggleColorFormat: "Trocar o formato de cor",
  zoomIn: "Aumentar zoom",
  zoomOut: "Diminuir zoom"
};
registerTranslation(translation);
var pt_default = translation;
export {
  pt_default as default
};
