import Component from '../../components/input/input.js';
import { type EventName } from '@lit/react';
import type { WaClearEvent, WaInvalidEvent } from '../../events/events.js';
export type { WaClearEvent, WaInvalidEvent } from '../../events/events.js';
/**
 * @summary Inputs collect data from the user.
 * @documentation https://webawesome.com/docs/components/input
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @slot label - The input's label. Alternatively, you can use the `label` attribute.
 * @slot start - An element, such as `<wa-icon>`, placed at the start of the input control.
 * @slot end - An element, such as `<wa-icon>`, placed at the end of the input control.
 * @slot clear-icon - An icon to use in lieu of the default clear icon.
 * @slot show-password-icon - An icon to use in lieu of the default show password icon.
 * @slot hide-password-icon - An icon to use in lieu of the default hide password icon.
 * @slot hint - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the control loses focus.
 * @event change - Emitted when an alteration to the control's value is committed by the user.
 * @event focus - Emitted when the control gains focus.
 * @event input - Emitted when the control receives input.
 * @event wa-clear - Emitted when the clear button is activated.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart label - The label
 * @csspart hint - The hint's wrapper.
 * @csspart base - The wrapper being rendered as an input
 * @csspart input - The internal `<input>` control.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart clear-button - The clear button.
 * @csspart password-toggle-button - The password toggle button.
 * @csspart end - The container that wraps the `end` slot.
 *
 * @cssstate blank - The input is empty.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaClear: EventName<WaClearEvent>;
    onWaInvalid: EventName<WaInvalidEvent>;
}>;
export default reactWrapper;
