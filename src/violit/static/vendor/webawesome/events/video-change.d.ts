export declare class WaVideoChangeEvent extends Event {
    readonly detail: WaVideoChangeEventDetail;
    constructor(detail: WaVideoChangeEventDetail);
}
export interface WaVideoChangeEventDetail {
    previousIndex: number;
    currentIndex: number;
    video: {
        title?: string;
        poster?: string;
        duration?: string;
        sources: {
            src: string;
            type: string;
        }[];
        tracks: {
            src: string;
            kind: string;
            srclang: string;
            label: string;
        }[];
    };
}
declare global {
    interface GlobalEventHandlersEventMap {
        'wa-video-change': WaVideoChangeEvent;
    }
}
