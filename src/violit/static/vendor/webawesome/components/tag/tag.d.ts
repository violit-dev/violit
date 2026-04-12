import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../button/button.js';
/**
 * @summary Tags are used as labels to organize things or to indicate a selection.
 * @documentation https://webawesome.com/docs/components/tag
 * @status stable
 * @since 2.0
 *
 * @dependency wa-button
 *
 * @slot - The tag's content.
 *
 * @event wa-remove - Emitted when the remove button is activated.
 *
 * @csspart base - The component's base wrapper.
 * @csspart content - The tag's content.
 * @csspart remove-button - The tag's remove button, a `<wa-button>`.
 * @csspart remove-button__base - The remove button's exported `base` part.
 */
export default class WaTag extends WebAwesomeElement {
    static css: import("lit").CSSResult[];
    private readonly localize;
    /** The tag's theme variant. Defaults to `neutral` if not within another element with a variant. */
    variant: 'brand' | 'neutral' | 'success' | 'warning' | 'danger';
    /** The tag's visual appearance. */
    appearance: 'accent' | 'filled' | 'outlined' | 'filled-outlined';
    /** The tag's size. */
    size: 'small' | 'medium' | 'large';
    /** Draws a pill-style tag with rounded edges. */
    pill: boolean;
    /** Makes the tag removable and shows a remove button. */
    withRemove: boolean;
    private handleRemoveClick;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-tag': WaTag;
    }
}
