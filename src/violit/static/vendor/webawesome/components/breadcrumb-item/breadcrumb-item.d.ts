import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Breadcrumb Items are used inside breadcrumbs to represent different links.
 * @documentation https://webawesome.com/docs/components/breadcrumb-item
 * @status stable
 * @since 2.0
 *
 * @slot - The breadcrumb item's label.
 * @slot start - An element, such as `<wa-icon>`, placed before the label.
 * @slot end - An element, such as `<wa-icon>`, placed after the label.
 * @slot separator - The separator to use for the breadcrumb item. This will only change the separator for this item. If
 * you want to change it for all items in the group, set the separator on `<wa-breadcrumb>` instead.
 *
 * @csspart label - The breadcrumb item's label.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart separator - The container that wraps the separator.
 */
export default class WaBreadcrumbItem extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    defaultSlot: HTMLSlotElement;
    private renderType;
    /**
     * Optional URL to direct the user to when the breadcrumb item is activated. When set, a link will be rendered
     * internally. When unset, a button will be rendered instead.
     */
    href?: string;
    /** Tells the browser where to open the link. Only used when `href` is set. */
    target?: '_blank' | '_parent' | '_self' | '_top';
    /** The `rel` attribute to use on the link. Only used when `href` is set. */
    rel: string;
    private setRenderType;
    hrefChanged(): void;
    handleSlotChange(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-breadcrumb-item': WaBreadcrumbItem;
    }
}
