import Component from '../../components/include/include.js';
import { type EventName } from '@lit/react';
import type { WaIncludeErrorEvent, WaLoadEvent } from '../../events/events.js';
export type { WaIncludeErrorEvent, WaLoadEvent } from '../../events/events.js';
/**
 * @summary Includes give you the power to embed external HTML files into the page.
 * @documentation https://webawesome.com/docs/components/include
 * @status stable
 * @since 2.0
 *
 * @event wa-load - Emitted when the included file is loaded.
 * @event {{ status: number }} wa-include-error - Emitted when the included file fails to load due to an error.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaLoad: EventName<WaLoadEvent>;
    onWaIncludeError: EventName<WaIncludeErrorEvent>;
}>;
export default reactWrapper;
