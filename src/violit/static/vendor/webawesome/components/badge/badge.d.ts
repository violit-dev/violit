import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Badges are used to draw attention and display statuses or counts.
 * @documentation https://webawesome.com/docs/components/badge
 * @status stable
 * @since 2.0
 *
 * @slot - The badge's content.
 * @slot start - An element, such as `<wa-icon>`, placed before the label.
 * @slot end - An element, such as `<wa-icon>`, placed after the label.
 *
 * @csspart base - The component's base wrapper.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart end - The container that wraps the `end` slot.
 *
 * @cssproperty --pulse-color - The color of the badge's pulse effect when using `attention="pulse"`.
 *
 */
export default class WaBadge extends WebAwesomeElement {
    static css: import("lit").CSSResult[];
    /** The badge's theme variant. Defaults to `brand` if not within another element with a variant. */
    variant: 'brand' | 'neutral' | 'success' | 'warning' | 'danger';
    /** The badge's visual appearance. */
    appearance: 'accent' | 'filled' | 'outlined' | 'filled-outlined';
    /** Draws a pill-style badge with rounded edges. */
    pill: boolean;
    /** Adds an animation to draw attention to the badge. */
    attention: 'none' | 'pulse' | 'bounce';
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-badge': WaBadge;
    }
}
