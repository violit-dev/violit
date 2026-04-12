import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary A carousel item represent a slide within a carousel.
 *
 * @since 2.0
 * @status experimental
 *
 * @slot - The carousel item's content..
 *
 * @cssproperty --aspect-ratio - The slide's aspect ratio. Inherited from the carousel by default.
 *
 */
export default class WaCarouselItem extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    connectedCallback(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-carousel-item': WaCarouselItem;
    }
}
