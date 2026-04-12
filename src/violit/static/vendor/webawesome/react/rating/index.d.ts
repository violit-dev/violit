import Component from '../../components/rating/rating.js';
import { type EventName } from '@lit/react';
import type { WaHoverEvent, WaInvalidEvent } from '../../events/events.js';
export type { WaHoverEvent, WaInvalidEvent } from '../../events/events.js';
/**
 * @summary Ratings give users a way to quickly view and provide feedback.
 * @documentation https://webawesome.com/docs/components/rating
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @event change - Emitted when the rating's value changes.
 * @event {{ phase: 'start' | 'move' | 'end', value: number }} wa-hover - Emitted when the user hovers over a value. The
 *  `phase` property indicates when hovering starts, moves to a new value, or ends. The `value` property tells what the
 *  rating's value would be if the user were to commit to the hovered value.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart base - The component's base wrapper.
 *
 * @cssproperty --symbol-color - The inactive color for symbols.
 * @cssproperty --symbol-color-active - The active color for symbols.
 * @cssproperty --symbol-spacing - The spacing to use around symbols.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaHover: EventName<WaHoverEvent>;
    onWaInvalid: EventName<WaInvalidEvent>;
}>;
export default reactWrapper;
