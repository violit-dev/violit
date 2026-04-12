import type { PropertyValues } from 'lit';
import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Zoomable frames render iframe content with zoom and interaction controls.
 * @documentation https://webawesome.com/docs/components/zoomable-frame
 * @status stable
 * @since 3.0
 *
 * @dependency wa-icon
 *
 * @slot zoom-in-icon - The slot that contains the zoom in icon.
 * @slot zoom-out-icon - The slot that contains the zoom out icon.
 *
 * @event load - Emitted when the internal iframe when it finishes loading.
 * @event error - Emitted from the internal iframe when it fails to load.
 *
 * @csspart iframe - The internal `<iframe>` element.
 * @csspart controls - The container that surrounds zoom control buttons.
 * @csspart zoom-in-button - The zoom in button.
 * @csspart zoom-out-button - The zoom out button.
 */
export default class WaZoomableFrame extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly localize;
    private availableZoomLevels;
    private themeObserver;
    constructor();
    iframe: HTMLIFrameElement;
    /** The URL of the content to display. */
    src: string;
    /** Inline HTML to display. */
    srcdoc: string;
    /** Allows fullscreen mode. */
    allowfullscreen: boolean;
    /** Controls iframe loading behavior. */
    loading: 'eager' | 'lazy';
    /** Controls referrer information. */
    referrerpolicy: string;
    /** Security restrictions for the iframe. */
    sandbox: string;
    /** The current zoom of the frame, e.g. 0 = 0% and 1 = 100%. */
    zoom: number;
    /**
     * The zoom levels to step through when using zoom controls. This does not restrict programmatic changes to the zoom.
     */
    zoomLevels: string;
    /** Removes the zoom controls. */
    withoutControls: boolean;
    /** Disables interaction when present. */
    withoutInteraction: boolean;
    /** Enables automatic theme syncing (light/dark mode and theme selector classes) from the host document to the iframe. */
    withThemeSync: boolean;
    /** Returns the internal iframe's `window` object. (Readonly property) */
    get contentWindow(): Window | null;
    /** Returns the internal iframe's `document` object. (Readonly property) */
    get contentDocument(): Document | null;
    private parseZoomLevels;
    private getCurrentZoomIndex;
    private isZoomInDisabled;
    private isZoomOutDisabled;
    updated(changedProperties: PropertyValues<this>): void;
    /** Zooms in to the next available zoom level. */
    zoomIn(): void;
    /** Zooms out to the previous available zoom level. */
    zoomOut(): void;
    disconnectedCallback(): void;
    private syncTheme;
    private handleLoad;
    private handleError;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-zoomable-frame': WaZoomableFrame;
    }
}
