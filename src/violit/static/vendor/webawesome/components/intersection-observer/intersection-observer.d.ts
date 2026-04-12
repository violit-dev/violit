import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Tracks immediate child elements and fires events as they move in and out of view.
 * @documentation https://webawesome.com/docs/components/intersection-observer
 * @status stable
 * @since 2.0
 *
 * @slot - Elements to track. Only immediate children of the host are monitored.
 *
 * @event {{ entry: IntersectionObserverEntry }} wa-intersect - Fired when a tracked element begins or ceases intersecting.
 */
export default class WaIntersectionObserver extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private intersectionObserver;
    private observedElements;
    /** Element ID to define the viewport boundaries for tracked targets. */
    root: string | null;
    /** Offset space around the root boundary. Accepts values like CSS margin syntax. */
    rootMargin: string;
    /** One or more space-separated values representing visibility percentages that trigger the observer callback. */
    threshold: string;
    /**
     * CSS class applied to elements during intersection. Automatically removed when elements leave
     * the viewport, enabling pure CSS styling based on visibility state.
     */
    intersectClass: string;
    /** If enabled, observation ceases after initial intersection. */
    once: boolean;
    /** Deactivates the intersection observer functionality. */
    disabled: boolean;
    connectedCallback(): void;
    disconnectedCallback(): void;
    private handleSlotChange;
    /** Converts threshold property string into numeric array. */
    private parseThreshold;
    /** Locates and returns the root element using the specified ID. */
    private resolveRoot;
    /** Initializes or reinitializes the intersection observer instance. */
    private startObserver;
    /** Halts the intersection observer and cleans up. */
    private stopObserver;
    handleDisabledChange(): void;
    handleOptionsChange(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-intersection-observer': WaIntersectionObserver;
    }
}
