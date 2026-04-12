import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../tooltip/tooltip.js';
import type WaTooltip from '../tooltip/tooltip.js';
/**
 * <wa-slider>
 *
 * @summary Ranges allow the user to select a single value within a given range using a slider.
 * @documentation https://webawesome.com/docs/components/range
 * @status stable
 * @since 2.0
 *
 * @dependency wa-tooltip
 *
 * @slot label - The slider label. Alternatively, you can use the `label` attribute.
 * @slot hint - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
 *  instead.
 * @slot reference - One or more reference labels to show visually below the slider.
 *
 * @event blur - Emitted when the control loses focus.
 * @event change - Emitted when an alteration to the control's value is committed by the user.
 * @event focus - Emitted when the control gains focus.
 * @event input - Emitted when the control receives input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart label - The element that contains the sliders's label.
 * @csspart hint - The element that contains the slider's description.
 * @csspart slider - The focusable element with `role="slider"`. Contains the track and reference slot.
 * @csspart track - The slider's track.
 * @csspart indicator - The colored indicator that shows from the start of the slider to the current value.
 * @csspart markers - The container that holds all the markers when `with-markers` is used.
 * @csspart marker - The individual markers that are shown when `with-markers` is used.
 * @csspart references - The container that holds references that get slotted in.
 * @csspart thumb - The slider's thumb.
 * @csspart thumb-min - The min value thumb in a range slider.
 * @csspart thumb-max - The max value thumb in a range slider.
 * @csspart tooltip - The tooltip, a `<wa-tooltip>` element.
 * @csspart tooltip__tooltip - The tooltip's `tooltip` part.
 * @csspart tooltip__content - The tooltip's `content` part.
 * @csspart tooltip__arrow - The tooltip's `arrow` part.
 *
 * @cssstate disabled - Applied when the slider is disabled.
 * @cssstate dragging - Applied when the slider is being dragged.
 * @cssstate focused - Applied when the slider has focus.
 * @cssstate user-valid - Applied when the slider is valid and the user has sufficiently interacted with it.
 * @cssstate user-invalid - Applied when the slider is invalid and the user has sufficiently interacted with it.
 *
 * @cssproperty [--track-size=0.75em] - The height or width of the slider's track.
 * @cssproperty [--marker-width=0.1875em] - The width of each individual marker.
 * @cssproperty [--marker-height=0.1875em] - The height of each individual marker.
 * @cssproperty [--thumb-width=1.25em] - The width of the thumb.
 * @cssproperty [--thumb-height=1.25em] - The height of the thumb.
 */
export default class WaSlider extends WebAwesomeFormAssociatedElement {
    static formAssociated: boolean;
    static observeSlots: boolean;
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    private draggableTrack;
    private draggableThumbMin;
    private draggableThumbMax;
    private readonly hasSlotController;
    private readonly localize;
    private trackBoundingClientRect;
    private valueWhenDraggingStarted;
    private activeThumb;
    private lastTrackPosition;
    protected get focusableAnchor(): HTMLElement;
    /** Override validation target to point to the focusable element */
    get validationTarget(): HTMLElement;
    slider: HTMLElement;
    thumb: HTMLElement;
    thumbMin: HTMLElement;
    thumbMax: HTMLElement;
    track: HTMLElement;
    tooltip: WaTooltip;
    /**
     * The slider's label. If you need to provide HTML in the label, use the `label` slot instead.
     */
    label: string;
    /** The slider hint. If you need to display HTML, use the hint slot instead. */
    hint: string;
    /** The name of the slider. This will be submitted with the form as a name/value pair. */
    name: string;
    /** The minimum value of a range selection. Used only when range attribute is set. */
    minValue: number;
    /** The maximum value of a range selection. Used only when range attribute is set. */
    maxValue: number;
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultValue: number;
    private _value;
    /** The current value of the slider, submitted as a name/value pair with form data. */
    get value(): number;
    set value(val: number | null);
    /** Converts the slider to a range slider with two thumbs. */
    range: boolean;
    /** Get if this is a range slider */
    get isRange(): boolean;
    /** Disables the slider. */
    disabled: boolean;
    /** Makes the slider a read-only field. */
    readonly: boolean;
    /** The orientation of the slider. */
    orientation: 'horizontal' | 'vertical';
    /** The slider's size. */
    size: 'small' | 'medium' | 'large';
    /** The starting value from which to draw the slider's fill, which is based on its current value. */
    indicatorOffset: number;
    /** The minimum value allowed. */
    min: number;
    /** The maximum value allowed. */
    max: number;
    /** The granularity the value must adhere to when incrementing and decrementing. */
    step: number;
    /** Tells the browser to focus the slider when the page loads or a dialog is shown. */
    autofocus: boolean;
    /** The distance of the tooltip from the slider's thumb. */
    tooltipDistance: number;
    /** The placement of the tooltip in reference to the slider's thumb. */
    tooltipPlacement: 'top' | 'right' | 'bottom' | 'left';
    /** Draws markers at each step along the slider. */
    withMarkers: boolean;
    /** Draws a tooltip above the thumb when the control has focus or is dragged. */
    withTooltip: boolean;
    /**
     * Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
     * includes the label before the component hydrates on the client.
     */
    withLabel: boolean;
    /**
     * Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
     * includes the hint before the component hydrates on the client.
     */
    withHint: boolean;
    /**
     * A custom formatting function to apply to the value. This will be shown in the tooltip and announced by screen
     * readers. Must be set with JavaScript. Property only.
     */
    valueFormatter: (value: number) => string;
    firstUpdated(): void;
    protected willUpdate(changedProperties: PropertyValues<this>): void;
    updated(changedProperties: PropertyValues<this>): void;
    /** @internal Called when a containing fieldset is disabled. */
    formDisabledCallback(isDisabled: boolean): void;
    /** @internal Called when the form is reset. */
    formResetCallback(): void;
    /** Clamps a number to min/max while ensuring it's a valid step interval. */
    private clampAndRoundToStep;
    /** Given a value, returns its percentage within a range of min/max. */
    private getPercentageFromValue;
    /** Converts coordinates to slider value */
    private getValueFromCoordinates;
    private handleBlur;
    private handleFocus;
    private handleKeyDown;
    private handleLabelPointerDown;
    private setValueFromCoordinates;
    private setThumbValueFromCoordinates;
    private showTooltip;
    private hideTooltip;
    private showRangeTooltips;
    private hideRangeTooltips;
    /** Updates the form value submission for range sliders */
    private updateFormValue;
    /** Sets focus to the slider. */
    focus(): void;
    /** Removes focus from the slider. */
    blur(): void;
    /**
     * Decreases the slider's value by `step`. This is a programmatic change, so `input` and `change` events will not be
     * emitted when this is called.
     */
    stepDown(): void;
    /**
     * Increases the slider's value by `step`. This is a programmatic change, so `input` and `change` events will not be
     * emitted when this is called.
     */
    stepUp(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-slider': WaSlider;
    }
}
