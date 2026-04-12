import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../button-group/button-group.js';
import '../button/button.js';
import '../icon/icon.js';
import '../input/input.js';
import type WaInput from '../input/input.js';
import '../popup/popup.js';
import type WaPopup from '../popup/popup.js';
export interface WaColorPickerSwatch {
    color: string;
    label: string;
}
/**
 * @summary Color pickers allow the user to select a color.
 * @documentation https://webawesome.com/docs/components/color-picker
 * @status stable
 * @since 2.0
 *
 * @dependency wa-button
 * @dependency wa-button-group
 * @dependency wa-input
 * @dependency wa-popup
 * @dependency wa-visually-hidden
 *
 * @slot label - The color picker's form label. Alternatively, you can use the `label` attribute.
 * @slot hint - The color picker's form hint. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the color picker loses focus.
 * @event change - Emitted when the color picker's value changes.
 * @event focus - Emitted when the color picker receives focus.
 * @event input - Emitted when the color picker receives input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart base - The component's base wrapper.
 * @csspart trigger - The color picker's dropdown trigger.
 * @csspart swatches - The container that holds the swatches.
 * @csspart swatch - Each individual swatch.
 * @csspart grid - The color grid.
 * @csspart grid-handle - The color grid's handle.
 * @csspart slider - Hue and opacity sliders.
 * @csspart slider-handle - Hue and opacity slider handles.
 * @csspart hue-slider - The hue slider.
 * @csspart hue-slider-handle - The hue slider's handle.
 * @csspart opacity-slider - The opacity slider.
 * @csspart opacity-slider-handle - The opacity slider's handle.
 * @csspart preview - The preview color.
 * @csspart input - The text input.
 * @csspart eyedropper-button - The eye dropper button.
 * @csspart eyedropper-button__base - The eye dropper button's exported `button` part.
 * @csspart eyedropper-button__start - The eye dropper button's exported `start` part.
 * @csspart eyedropper-button__label - The eye dropper button's exported `label` part.
 * @csspart eyedropper-button__end - The eye dropper button's exported `end` part.
 * @csspart eyedropper-button__caret - The eye dropper button's exported `caret` part.
 * @csspart format-button - The format button.
 * @csspart format-button__base - The format button's exported `button` part.
 * @csspart format-button__start - The format button's exported `start` part.
 * @csspart format-button__label - The format button's exported `label` part.
 * @csspart format-button__end - The format button's exported `end` part.
 * @csspart format-button__caret - The format button's exported `caret` part.
 *
 * @cssproperty --grid-width - The width of the color grid.
 * @cssproperty --grid-height - The height of the color grid.
 * @cssproperty --grid-handle-size - The size of the color grid's handle.
 * @cssproperty --slider-height - The height of the hue and alpha sliders.
 * @cssproperty --slider-handle-size - The diameter of the slider's handle.
 */
export default class WaColorPicker extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    private readonly hasSlotController;
    private isSafeValue;
    private readonly localize;
    base: HTMLElement;
    input: WaInput;
    triggerLabel: HTMLElement;
    triggerButton: HTMLButtonElement;
    get validationTarget(): HTMLButtonElement | WaInput;
    popup: WaPopup;
    previewButton: HTMLButtonElement;
    trigger: HTMLButtonElement;
    private hasFocus;
    private isDraggingGridHandle;
    private isEmpty;
    private inputValue;
    private hue;
    private saturation;
    private brightness;
    private alpha;
    private _value;
    /** The current value of the input, submitted as a name/value pair with form data. */
    get value(): string | null;
    /**
     * The current value of the color picker. The value's format will vary based the `format` attribute. To get the value
     * in a specific format, use the `getFormattedValue()` method. The value is submitted as a name/value pair with form
     * data.
     */
    set value(val: string | null);
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultValue: string | null;
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
    private hasEyeDropper;
    /**
     * The color picker's label. This will not be displayed, but it will be announced by assistive devices. If you need to
     * display HTML, you can use the `label` slot` instead.
     */
    label: string;
    /**
     * The color picker's hint. If you need to display HTML, use the `hint` slot instead.
     */
    hint: string;
    /**
     * The format to use. If opacity is enabled, these will translate to HEXA, RGBA, HSLA, and HSVA respectively. The color
     * picker will accept user input in any format (including CSS color names) and convert it to the desired format.
     */
    format: 'hex' | 'rgb' | 'hsl' | 'hsv';
    /** Determines the size of the color picker's trigger */
    size: 'small' | 'medium' | 'large';
    /**
     * The preferred placement of the color picker's popup. Note that the actual placement will vary as configured to
     * keep the panel inside of the viewport.
     */
    placement: 'top' | 'top-start' | 'top-end' | 'bottom' | 'bottom-start' | 'bottom-end' | 'right' | 'right-start' | 'right-end' | 'left' | 'left-start' | 'left-end';
    /** Removes the button that lets users toggle between format.   */
    withoutFormatToggle: boolean;
    /** The name of the form control, submitted as a name/value pair with form data. */
    name: string | null;
    /** Disables the color picker. */
    disabled: boolean;
    /**
     * Indicates whether or not the popup is open. You can toggle this attribute to show and hide the popup, or you
     * can use the `show()` and `hide()` methods and this attribute will reflect the popup's open state.
     */
    open: boolean;
    /** Shows the opacity slider. Enabling this will cause the formatted value to be HEXA, RGBA, or HSLA. */
    opacity: boolean;
    /** By default, values are lowercase. With this attribute, values will be uppercase instead. */
    uppercase: boolean;
    /**
     * One or more predefined color swatches to display as presets in the color picker. Can include any format the color
     * picker can parse, including HEX(A), RGB(A), HSL(A), HSV(A), and CSS color names. Each color must be separated by a
     * semicolon (`;`). Alternatively, you can pass an array of color values or an array of `{ color, label }` objects to
     * this property using JavaScript. When using objects with labels, the label will be used for the swatch's accessible
     * name instead of the raw color value.
     */
    swatches: string | string[] | WaColorPickerSwatch[];
    /** Makes the color picker a required field. */
    required: boolean;
    constructor();
    private handleCopy;
    private handleFocusIn;
    private handleFocusOut;
    private handleFormatToggle;
    private handleAlphaDrag;
    private handleHueDrag;
    private handleGridDrag;
    private handleAlphaKeyDown;
    private handleHueKeyDown;
    private handleGridKeyDown;
    private handleInputChange;
    private handleInputInput;
    private handleInputKeyDown;
    private handleTouchMove;
    private parseColor;
    private setColor;
    private setLetterCase;
    private syncValues;
    private handleAfterHide;
    private handleAfterShow;
    private handleEyeDropper;
    private selectSwatch;
    /** Generates a hex string from HSV values. Hue must be 0-360. All other arguments must be 0-100. */
    getHexString(hue: number, saturation: number, brightness: number, alpha?: number): string;
    private stopNestedEventPropagation;
    handleFormatChange(): void;
    handleOpacityChange(): void;
    protected willUpdate(changedProperties: PropertyValues<this>): void;
    handleValueChange(oldValue: string | undefined, newValue: string): void;
    /** Sets focus on the color picker. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the color picker. */
    blur(): void;
    /** Returns the current value as a string in the specified format. */
    getFormattedValue(format?: 'hex' | 'hexa' | 'rgb' | 'rgba' | 'hsl' | 'hsla' | 'hsv' | 'hsva'): string;
    private reportValidityAfterShow;
    /** Checks for validity and shows the browser's validation message if the control is invalid. */
    reportValidity(): boolean;
    formResetCallback(): void;
    firstUpdated(changedProperties: PropertyValues<this>): void;
    private handleKeyDown;
    private handleDocumentKeyDown;
    private handleDocumentMouseDown;
    handleTriggerClick(): void;
    handleTriggerKeyDown(event: KeyboardEvent): Promise<void>;
    handleTriggerKeyUp(event: KeyboardEvent): void;
    updateAccessibleTrigger(): void;
    /** Shows the color picker panel. */
    show(): Promise<void>;
    /** Hides the color picker panel */
    hide(): Promise<void>;
    addOpenListeners(): void;
    removeOpenListeners(): void;
    handleOpenChange(): Promise<void>;
    render(): import("lit-html").TemplateResult<1>;
}
