export declare class WaSelectEvent extends Event {
    readonly detail: WaSelectEventDetail;
    constructor(detail: WaSelectEventDetail);
}
interface WaSelectEventDetail {
    item: Element;
}
declare global {
    interface GlobalEventHandlersEventMap {
        'wa-select': WaSelectEvent;
    }
}
export {};
