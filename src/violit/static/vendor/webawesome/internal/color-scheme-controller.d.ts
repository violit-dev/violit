import type { ReactiveController, ReactiveControllerHost } from 'lit';
export declare class ColorSchemeController implements ReactiveController {
    private host;
    private hiddenElement;
    private onThemeChange;
    constructor(host: ReactiveControllerHost & Element, onThemeChange: () => void);
    hostConnected(): void;
    hostDisconnected(): void;
    private handleTransitionEnd;
}
