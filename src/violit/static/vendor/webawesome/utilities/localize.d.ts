import type { Translation as DefaultTranslation } from '@shoelace-style/localize';
import { LocalizeController as DefaultLocalizationController } from '@shoelace-style/localize';
export declare class LocalizeController extends DefaultLocalizationController<Translation> {
}
export { registerTranslation } from '@shoelace-style/localize';
export interface Translation extends DefaultTranslation {
    $code: string;
    $name: string;
    $dir: 'ltr' | 'rtl';
    carousel: string;
    clearEntry: string;
    close: string;
    createOption: (value: string) => string;
    copied: string;
    copy: string;
    currentValue: string;
    dropFileHere: string;
    decrement: string;
    dropFilesHere: string;
    error: string;
    goToSlide: (slide: number, count: number) => string;
    hidePassword: string;
    increment: string;
    loading: string;
    nextSlide: string;
    numCharacters: (num: number) => string;
    numCharactersRemaining: (num: number) => string;
    numOptionsSelected: (num: number) => string;
    pauseAnimation: string;
    playAnimation: string;
    previousSlide: string;
    progress: string;
    remove: string;
    resize: string;
    scrollableRegion: string;
    scrollToEnd: string;
    scrollToStart: string;
    selectAColorFromTheScreen: string;
    showPassword: string;
    slideNum: (slide: number) => string;
    toggleColorFormat: string;
    zoomIn: string;
    zoomOut: string;
}
