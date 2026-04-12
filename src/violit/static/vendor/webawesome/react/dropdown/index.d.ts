import Component from '../../components/dropdown/dropdown.js';
import { type EventName } from '@lit/react';
import type { WaAfterHideEvent, WaAfterShowEvent, WaHideEvent, WaSelectEvent, WaShowEvent } from '../../events/events.js';
export type { WaAfterHideEvent, WaAfterShowEvent, WaHideEvent, WaSelectEvent, WaShowEvent, } from '../../events/events.js';
/**
 * @summary Dropdowns display a list of options that can be triggered by a button or other element. They support
 *  keyboard navigation, submenus, and various customization options.
 * @documentation https://webawesome.com/docs/components/dropdown
 * @status stable
 * @since 2.0
 *
 * @dependency wa-dropdown-item
 * @dependency wa-popup
 *
 * @event wa-show - Emitted when the dropdown is about to show.
 * @event wa-after-show - Emitted after the dropdown has been shown.
 * @event wa-hide - Emitted when the dropdown is about to hide.
 * @event wa-after-hide - Emitted after the dropdown has been hidden.
 * @event wa-select - Emitted when an item in the dropdown is selected.
 *
 * @slot - The dropdown's items, typically `<wa-dropdown-item>` elements.
 * @slot trigger - The element that triggers the dropdown, such as a `<wa-button>` or `<button>`.
 *
 * @csspart base - The component's host element.
 * @csspart menu - The dropdown menu container.
 *
 * @cssproperty --show-duration - The duration of the show animation.
 * @cssproperty --hide-duration - The duration of the hide animation.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaShow: EventName<WaShowEvent>;
    onWaAfterShow: EventName<WaAfterShowEvent>;
    onWaHide: EventName<WaHideEvent>;
    onWaAfterHide: EventName<WaAfterHideEvent>;
    onWaSelect: EventName<WaSelectEvent>;
}>;
export default reactWrapper;
