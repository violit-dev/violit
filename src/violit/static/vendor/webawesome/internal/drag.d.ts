interface DragOptions {
    /** Callback that runs as dragging occurs. */
    onMove: (x: number, y: number) => void;
    /** Callback that runs when dragging stops. */
    onStop: () => void;
    /**
     * When an initial event is passed, the first drag will be triggered immediately using the coordinates therein. This
     * is useful when the drag is initiated by a mousedown/touchstart event but you want the initial "click" to activate
     * a drag (e.g. positioning a handle initially at the click target).
     */
    initialEvent: PointerEvent;
}
/** Begins listening for dragging. */
export declare function drag(container: HTMLElement, options?: Partial<DragOptions>): void;
/**
 * Attaches the necessary events to make an element draggable.
 *
 * This by itself will not make the element draggable, but it provides the events and callbacks necessary to facilitate
 * dragging. Use the `clientX` and `clientY` arguments of each callback to update the UI as desired when dragging.
 *
 * Drag functionality will be enabled as soon as the constructor is called. A `start()` and `stop()` method can be used
 * to start and stop it, if needed.
 *
 * Use `touch-action: none` on touch devices if scrolling occurs while dragging. Avoid preventing the touchstart event!
 *
 * @usage
 *
 * const draggable = new DraggableElement(element, {
 *   start: (clientX, clientY) => { ... },
 *   move: (clientX, clientY) => { ... },
 *   stop: (clientX, clientY) => { ... }
 * });
 */
export declare class DraggableElement {
    private element;
    private isActive;
    private isDragging;
    private options;
    constructor(el: Element, options: Partial<DraggableElementOptions>);
    private handleDragStart;
    private handleDragStop;
    private handleDragMove;
    /** Start listening to drags. */
    start(): void;
    /** Stop listening to drags. */
    stop(): void;
    /** Starts or stops the drag listeners. */
    toggle(isActive?: boolean): void;
}
export interface DraggableElementOptions {
    /** Runs when dragging starts. */
    start: (clientX: number, clientY: number) => void;
    /** Runs as the user is dragging. This may execute often, so avoid expensive operations. */
    move: (clientX: number, clientY: number) => void;
    /** Runs when dragging ends. */
    stop: (clientX: number, clientY: number) => void;
}
export {};
