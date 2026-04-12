import Component from '../../components/number-input/number-input.js';
import { type EventName } from '@lit/react';
import type { WaInvalidEvent } from '../../events/events.js';
export type { WaInvalidEvent } from '../../events/events.js';
/**
 * @summary Number inputs allow users to enter and edit numeric values with optional stepper buttons.
 * @documentation https://webawesome.com/docs/components/number-input
 * @status experimental
 * @since 3.2
 *
 * @dependency wa-icon
 *
 * @slot label - The input's label. Alternatively, you can use the `label` attribute.
 * @slot start - An element, such as `<wa-icon>`, placed at the start of the input control.
 * @slot end - An element, such as `<wa-icon>`, placed at the end of the input control (before steppers).
 * @slot increment-icon - An icon to use in lieu of the default increment icon.
 * @slot decrement-icon - An icon to use in lieu of the default decrement icon.
 * @slot hint - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the control loses focus.
 * @event change - Emitted when an alteration to the control's value is committed by the user.
 * @event focus - Emitted when the control gains focus.
 * @event input - Emitted when the control receives input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart label - The label element.
 * @csspart form-control-label - Alias for the label element.
 * @csspart hint - The hint element.
 * @csspart base - The wrapper containing the input and steppers.
 * @csspart input - The internal `<input>` control.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart stepper - Both stepper buttons (for shared styling).
 * @csspart stepper-increment - The increment (+) button on the end side.
 * @csspart stepper-decrement - The decrement (-) button on the start side.
 *
 * @cssstate blank - The input is empty.
 * @cssstate focused - The input has focus.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaInvalid: EventName<WaInvalidEvent>;
}>;
export default reactWrapper;
