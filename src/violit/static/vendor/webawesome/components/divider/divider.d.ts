import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Dividers are used to visually separate or group elements.
 * @documentation https://webawesome.com/docs/components/divider
 * @status stable
 * @since 2.0
 *
 * @cssproperty --color - The color of the divider.
 * @cssproperty --width - The width of the divider.
 * @cssproperty --spacing - The spacing of the divider.
 */
export default class WaDivider extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    /** Sets the divider's orientation. */
    orientation: 'horizontal' | 'vertical';
    connectedCallback(): void;
    handleVerticalChange(): void;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-divider': WaDivider;
    }
}
