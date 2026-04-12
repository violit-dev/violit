import Component from '../../components/copy-button/copy-button.js';
import { type EventName } from '@lit/react';
import type { WaCopyEvent, WaErrorEvent } from '../../events/events.js';
export type { WaCopyEvent, WaErrorEvent } from '../../events/events.js';
/**
 * @summary Copies text data to the clipboard when the user clicks the trigger.
 * @documentation https://webawesome.com/docs/components/copy
 * @status experimental
 * @since 2.7
 *
 * @dependency wa-icon
 * @dependency wa-tooltip
 *
 * @event wa-copy - Emitted when the data has been copied.
 * @event wa-error - Emitted when the data could not be copied.
 *
 * @slot - The trigger element. By default, a copy icon button is rendered so this is optional. If desired, you can slot
 *  in a custom element such as `<wa-button>` or `<button>`.
 * @slot copy-icon - The icon to show in the default copy state. Works best with `<wa-icon>`.
 * @slot success-icon - The icon to show when the content is copied. Works best with `<wa-icon>`.
 * @slot error-icon - The icon to show when a copy error occurs. Works best with `<wa-icon>`.
 *
 * @cssstate success - Applied when the copy operation succeeds.
 * @cssstate error - Applied when the copy operation fails.
 *
 * @csspart button - The internal `<button>` element.
 * @csspart copy-icon - The container that holds the copy icon.
 * @csspart success-icon - The container that holds the success icon.
 * @csspart error-icon - The container that holds the error icon.
 * @csspart tooltip__base - The tooltip's exported `base` part.
 * @csspart tooltip__base__popup - The tooltip's exported `popup` part.
 * @csspart tooltip__base__arrow - The tooltip's exported `arrow` part.
 * @csspart tooltip__body - The tooltip's exported `body` part.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaCopy: EventName<WaCopyEvent>;
    onWaError: EventName<WaErrorEvent>;
}>;
export default reactWrapper;
