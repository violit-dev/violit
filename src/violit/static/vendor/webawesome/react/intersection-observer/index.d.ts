import Component from '../../components/intersection-observer/intersection-observer.js';
import { type EventName } from '@lit/react';
import type { WaIntersectEvent } from '../../events/events.js';
export type { WaIntersectEvent } from '../../events/events.js';
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
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaIntersect: EventName<WaIntersectEvent>;
}>;
export default reactWrapper;
