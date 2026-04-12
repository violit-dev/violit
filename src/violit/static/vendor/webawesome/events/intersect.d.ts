/** Emitted when an element's intersection state changes. */
export declare class WaIntersectEvent extends Event {
    readonly detail?: WaIntersectEventDetail;
    constructor(detail?: WaIntersectEventDetail);
}
interface WaIntersectEventDetail {
    entry?: IntersectionObserverEntry;
}
declare global {
    interface GlobalEventHandlersEventMap {
        'wa-intersect': WaIntersectEvent;
    }
}
export {};
