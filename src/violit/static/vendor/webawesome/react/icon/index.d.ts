import Component from '../../components/icon/icon.js';
import { type EventName } from '@lit/react';
import type { WaErrorEvent, WaLoadEvent } from '../../events/events.js';
export type { WaErrorEvent, WaLoadEvent } from '../../events/events.js';
/**
 * @summary Icons are symbols that can be used to represent various options within an application.
 * @documentation https://webawesome.com/docs/components/icon
 * @status stable
 * @since 2.0
 *
 * @event wa-load - Emitted when the icon has loaded. When using `spriteSheet: true` this will not emit.
 * @event wa-error - Emitted when the icon fails to load due to an error. When using `spriteSheet: true` this will not emit.
 *
 * @csspart svg - The internal SVG element.
 * @csspart use - The `<use>` element generated when using `spriteSheet: true`
 *
 * @cssproperty [--animation-delay=0] Sets when the animation will start.
 * @cssproperty [--animation-direction=normal] Defines whether or not the animation should play in reverse on alternate cycles.
 * @cssproperty [--animation-duration=1s] Defines the length of time that an animation takes to complete one cycle.
 * @cssproperty [--animation-iteration-count=infinite] Defines the number of times an animation cycle is played.
 * @cssproperty [--animation-timing] Describes how the animation will progress over one cycle of its duration.
 * @cssproperty [--beat-fade-opacity] Set lowest opacity value an icon with `beat-fade` animation will fade to and from.
 * @cssproperty [--beat-fade-scale] Set max value that an icon with `beat-fade` animation will scale.
 * @cssproperty [--beat-scale] Set max value that an icon with `beat` animation will scale.
 * @cssproperty [--bounce-height] Set the max height an icon with `bounce` animation will jump to when bouncing.
 * @cssproperty [--bounce-jump-scale-x] Set the icon’s horizontal distortion (“squish”) at the top of the jump.
 * @cssproperty [--bounce-jump-scale-y] Set the icon’s vertical distortion (“squish”) at the top of the jump.
 * @cssproperty [--bounce-land-scale-x] Set the icon’s horizontal distortion (“squish”) when landing after the jump.
 * @cssproperty [--bounce-land-scale-y] Set the icon’s vertical distortion (“squish”) when landing after the jump.
 * @cssproperty [--bounce-rebound] Set the amount of rebound an icon with `bounce` animation has when landing after the jump.
 * @cssproperty [--bounce-start-scale-x] Set the icon’s horizontal distortion (“squish”) when starting to bounce.
 * @cssproperty [--bounce-start-scale-y] Set the icon’s vertical distortion (“squish”) when starting to bounce.
 * @cssproperty [--fade-opacity] Set lowest opacity value an icon with `fade` animation will fade to and from.
 * @cssproperty [--flip-angle] Set rotation angle of flip for an icon with `flip` animation. A positive angle denotes a clockwise rotation, a negative angle a counter-clockwise one.
 * @cssproperty [--flip-x] Set x-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation.
 * @cssproperty [--flip-y] Set y-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation.
 * @cssproperty [--flip-z] Set z-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation.
 * @cssproperty [--primary-color=currentColor] - Sets a duotone icon's primary color.
 * @cssproperty [--primary-opacity=1] - Sets a duotone icon's primary opacity.
 * @cssproperty [--secondary-color=currentColor] - Sets a duotone icon's secondary color.
 * @cssproperty [--secondary-opacity=0.4] - Sets a duotone icon's secondary opacity.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {
    onWaLoad: EventName<WaLoadEvent>;
    onWaError: EventName<WaErrorEvent>;
}>;
export default reactWrapper;
