import { type PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
/**
 * @summary Ratings give users a way to quickly view and provide feedback.
 * @documentation https://webawesome.com/docs/components/rating
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @event change - Emitted when the rating's value changes.
 * @event {{ phase: 'start' | 'move' | 'end', value: number }} wa-hover - Emitted when the user hovers over a value. The
 *  `phase` property indicates when hovering starts, moves to a new value, or ends. The `value` property tells what the
 *  rating's value would be if the user were to commit to the hovered value.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart base - The component's base wrapper.
 *
 * @cssproperty --symbol-color - The inactive color for symbols.
 * @cssproperty --symbol-color-active - The active color for symbols.
 * @cssproperty --symbol-spacing - The spacing to use around symbols.
 */
export default class WaRating extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    assumeInteractionOn: string[];
    private readonly localize;
    connectedCallback(): void;
    disconnectedCallback(): void;
    updated(changedProperties: PropertyValues<this>): void;
    private hoverValue;
    private isHovering;
    /** The name of the rating, submitted as a name/value pair with form data. */
    name: string | null;
    /** A label that describes the rating to assistive devices. */
    label: string;
    /** The current rating. */
    value: number;
    /** The default value of the form control. Used to reset the rating to its initial value. */
    defaultValue: number;
    /** The highest rating to show. */
    max: number;
    /**
     * The precision at which the rating will increase and decrease. For example, to allow half-star ratings, set this
     * attribute to `0.5`.
     */
    precision: number;
    /** Makes the rating readonly. */
    readonly: boolean;
    /** Disables the rating. */
    disabled: boolean;
    /** Makes the rating a required field. */
    required: boolean;
    /**
     * A function that customizes the symbol to be rendered. The first and only argument is the rating's current value.
     * The function should return a string containing trusted HTML of the symbol to render at the specified value. Works
     * well with `<wa-icon>` elements.
     */
    getSymbol: (value: number, isSelected: boolean) => string;
    /** The component's size. */
    size: 'small' | 'medium' | 'large';
    private getValueFromPointerPosition;
    private getValueFromXCoordinate;
    private handleClick;
    private setRatingValue;
    private handleKeyDown;
    private handlePointerEnter;
    private handlePointerMove;
    private handlePointerLeave;
    private handlePointerDown;
    private handlePointerUp;
    private roundToPrecision;
    handleHoverValueChange(): void;
    handleIsHoveringChange(): void;
    formResetCallback(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-rating': WaRating;
    }
}
