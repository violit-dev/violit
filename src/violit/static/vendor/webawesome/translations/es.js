/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import "../chunks/chunk.G3ZVQTTB.js";
import "../chunks/chunk.5OV4QM6R.js";
import {
  registerTranslation
} from "../chunks/chunk.HPOJN4W7.js";
import "../chunks/chunk.JHZRD2LV.js";

// src/translations/es.ts
var translation = {
  $code: "es",
  $name: "Espa\xF1ol",
  $dir: "ltr",
  carousel: "Carrusel",
  clearEntry: "Borrar entrada",
  createOption: (value) => `Crear "${value}"`,
  close: "Cerrar",
  copied: "Copiado",
  copy: "Copiar",
  currentValue: "Valor actual",
  decrement: "Disminuir",
  dropFileHere: "Drop file here or click to browse",
  dropFilesHere: "Drop files here or click to browse",
  error: "Error",
  goToSlide: (slide, count) => `Ir a la diapositiva ${slide} de ${count}`,
  hidePassword: "Ocultar contrase\xF1a",
  increment: "Aumentar",
  loading: "Cargando",
  nextSlide: "Siguiente diapositiva",
  numCharacters: (num) => {
    if (num === 1) return "1 car\xE1cter";
    return `${num} caracteres`;
  },
  numCharactersRemaining: (num) => {
    if (num === 1) return "1 car\xE1cter restante";
    return `${num} caracteres restantes`;
  },
  numOptionsSelected: (num) => {
    if (num === 0) return "No hay opciones seleccionadas";
    if (num === 1) return "1 opci\xF3n seleccionada";
    return `${num} opci\xF3n seleccionada`;
  },
  pauseAnimation: "Pausar animaci\xF3n",
  playAnimation: "Reproducir animaci\xF3n",
  previousSlide: "Diapositiva anterior",
  progress: "Progreso",
  remove: "Eliminar",
  resize: "Cambiar el tama\xF1o",
  scrollableRegion: "Regi\xF3n desplazable",
  scrollToEnd: "Desplazarse hasta el final",
  scrollToStart: "Desplazarse al inicio",
  selectAColorFromTheScreen: "Seleccione un color de la pantalla",
  showPassword: "Mostrar contrase\xF1a",
  slideNum: (slide) => `Diapositiva ${slide}`,
  toggleColorFormat: "Alternar formato de color",
  zoomIn: "Acercar",
  zoomOut: "Alejar"
};
registerTranslation(translation);
var es_default = translation;
export {
  es_default as default
};
