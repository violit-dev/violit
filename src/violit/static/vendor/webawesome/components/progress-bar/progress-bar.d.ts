import type { PropertyValues } from 'lit';
import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Progress bars are used to show the status of an ongoing operation.
 * @documentation https://webawesome.com/docs/components/progress-bar
 * @status stable
 * @since 2.0
 *
 * @slot - A label to show inside the progress indicator.
 *
 * @csspart base - The component's base wrapper.
 * @csspart indicator - The progress bar's indicator.
 * @csspart label - The progress bar's label.
 *
 * @cssproperty [--track-height=1rem] - The color of the track.
 * @cssproperty [--track-color=var(--wa-color-neutral-fill-normal)] - The color of the track.
 * @cssproperty [--indicator-color=var(--wa-color-brand-fill-loud)] - The color of the indicator.
 */
export default class WaProgressBar extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly localize;
    /** The current progress as a percentage, 0 to 100. */
    value: number;
    /** When true, percentage is ignored, the label is hidden, and the progress bar is drawn in an indeterminate state. */
    indeterminate: boolean;
    /** A custom label for assistive devices. */
    label: string;
    updated(changedProperties: PropertyValues<this>): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-progress-bar': WaProgressBar;
    }
}
