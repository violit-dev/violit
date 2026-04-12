import Component from '../../components/popover/popover.js';
import { type EventName } from '@lit/react';
import type { WaAfterHideEvent, WaAfterShowEvent, WaHideEvent, WaShowEvent } from '../../events/events.js';
export type { WaAfterHideEvent, WaAfterShowEvent, WaHideEvent, WaShowEvent } from '../../events/events.js';
/**
 * @summary Popovers display contextual content and interactive elements in a floating panel.
 * @documentation https://webawesome.com/docs/components/popover
 * @status stable
 * @since 3.0
 *
 * @dependency wa-popup
 *
 * @slot - The popover's content. Interactive elements such as buttons and links are supported.
 *
 * @event wa-show - Emitted when the popover begins to show. Canceling this event will stop the popover from showing.
 * @event wa-after-show - Emitted after the popover has shown and all animations are complete.
 * @event wa-hide - Emitted when the popover begins to hide. Canceling this event will stop the popover from hiding.
 * @event wa-after-hide - Emitted after the popover has hidden and all animations are complete.
 *
 * @csspart dialog - The native dialog element that contains the popover content.
 * @csspart body - The popover's body where its content is rendered.
 * @csspart popup - The internal `<wa-popup>` element that positions the popover.
 * @csspart popup__popup - The popup's exported `popup` part. Use this to target the popover's popup container.
 * @csspart popup__arrow - The popup's exported `arrow` part. Use this to target the popover's arrow.
 *
 * @cssproperty [--arrow-size=0.375rem] - The size of the tiny arrow that points to the popover (set to zero to remove).
 * @cssproperty [--max-width=25rem] - The maximum width of the popover's body content.
 * @cssproperty [--show-duration=100ms] - The speed of the show animation.
 * @cssproperty [--hide-duration=100ms] - The speed of the hide animation.
 *
 * @cssstate open - Applied when the popover is open.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaShow: EventName<WaShowEvent>;
    onWaAfterShow: EventName<WaAfterShowEvent>;
    onWaHide: EventName<WaHideEvent>;
    onWaAfterHide: EventName<WaAfterHideEvent>;
}>;
export default reactWrapper;
