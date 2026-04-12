import type { PropertyValues } from 'lit';
import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../icon/icon.js';
/**
 * @summary Details show a brief summary and expand to show additional content.
 * @documentation https://webawesome.com/docs/components/details
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @slot - The details' main content.
 * @slot summary - The details' summary. Alternatively, you can use the `summary` attribute.
 * @slot expand-icon - Optional expand icon to use instead of the default. Works best with `<wa-icon>`.
 * @slot collapse-icon - Optional collapse icon to use instead of the default. Works best with `<wa-icon>`.
 *
 * @event wa-show - Emitted when the details opens.
 * @event wa-after-show - Emitted after the details opens and all animations are complete.
 * @event wa-hide - Emitted when the details closes.
 * @event wa-after-hide - Emitted after the details closes and all animations are complete.
 *
 * @csspart base - The inner `<details>` element used to render the component.
 *                 Styles you apply to the component are automatically applied to this part, so you usually don't need to deal with it unless you need to set the `display` property.
 * @csspart header - The header that wraps both the summary and the expand/collapse icon.
 * @csspart summary - The container that wraps the summary.
 * @csspart icon - The container that wraps the expand/collapse icons.
 * @csspart content - The details content.
 *
 * @cssproperty --spacing - The amount of space around and between the details' content. Expects a single value.
 * @cssproperty [--show-duration=200ms] - The show duration to use when applying built-in animation classes.
 * @cssproperty [--hide-duration=200ms] - The hide duration to use when applying built-in animation classes.
 *
 * @cssstate animating - Applied when the details is animating expand/collapse.
 */
export default class WaDetails extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private detailsObserver;
    private readonly localize;
    details: HTMLDetailsElement;
    header: HTMLElement;
    body: HTMLElement;
    expandIconSlot: HTMLSlotElement;
    private animationGeneration;
    isAnimating: boolean;
    /**
     * Indicates whether or not the details is open. You can toggle this attribute to show and hide the details, or you
     * can use the `show()` and `hide()` methods and this attribute will reflect the details' open state.
     */
    open: boolean;
    /** The summary to show in the header. If you need to display HTML, use the `summary` slot instead. */
    summary: string;
    /** Groups related details elements. When one opens, others with the same name will close. */
    name: string;
    /** Disables the details so it can't be toggled. */
    disabled: boolean;
    /** The element's visual appearance. */
    appearance: 'filled' | 'outlined' | 'filled-outlined' | 'plain';
    /** The location of the expand/collapse icon. */
    iconPlacement: 'start' | 'end';
    disconnectedCallback(): void;
    firstUpdated(): void;
    updated(changedProperties: PropertyValues<this>): void;
    private handleSummaryClick;
    private handleSummaryKeyDown;
    /** Closes other <wa-details> elements in the same document when they have the same name. */
    private closeOthersWithSameName;
    handleOpenChange(): Promise<void>;
    /** Shows the details. */
    show(): Promise<void>;
    /** Hides the details */
    hide(): Promise<void>;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-details': WaDetails;
    }
}
