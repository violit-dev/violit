export declare class WaCreateEvent extends Event {
    readonly detail: WaCreateEventDetail;
    constructor(detail: WaCreateEventDetail);
}
export interface WaCreateEventDetail {
    inputValue: string;
}
declare global {
    interface GlobalEventHandlersEventMap {
        'wa-create': WaCreateEvent;
    }
}
