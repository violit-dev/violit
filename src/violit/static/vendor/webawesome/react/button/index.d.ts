import Component from '../../components/button/button.js';
import { type EventName } from '@lit/react';
import type { WaInvalidEvent } from '../../events/events.js';
export type { WaInvalidEvent } from '../../events/events.js';
/**
 * @summary Buttons represent actions that are available to the user.
 * @documentation https://webawesome.com/docs/components/button
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 * @dependency wa-spinner
 *
 * @event blur - Emitted when the button loses focus.
 * @event focus - Emitted when the button gains focus.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @slot - The button's label.
 * @slot start - An element, such as `<wa-icon>`, placed before the label.
 * @slot end - An element, such as `<wa-icon>`, placed after the label.
 *
 * @csspart base - The component's base wrapper.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart label - The button's label.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart caret - The button's caret icon, a `<wa-icon>` element.
 * @csspart spinner - The spinner that shows when the button is in the loading state.
 *
 * @cssstate disabled - Applied when the button is disabled.
 * @cssstate icon-button - Applied when the button contains only a `<wa-icon>` with no other content.
 * @cssstate link - Applied when the button is rendered as a link (i.e. `href` is set).
 * @cssstate loading - Applied when the button is in the loading state.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaInvalid: EventName<WaInvalidEvent>;
}>;
export default reactWrapper;
