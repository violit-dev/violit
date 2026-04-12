import { type PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
/**
 * @summary Number inputs allow users to enter and edit numeric values with optional stepper buttons.
 * @documentation https://webawesome.com/docs/components/number-input
 * @status experimental
 * @since 3.2
 *
 * @dependency wa-icon
 *
 * @slot label - The input's label. Alternatively, you can use the `label` attribute.
 * @slot start - An element, such as `<wa-icon>`, placed at the start of the input control.
 * @slot end - An element, such as `<wa-icon>`, placed at the end of the input control (before steppers).
 * @slot increment-icon - An icon to use in lieu of the default increment icon.
 * @slot decrement-icon - An icon to use in lieu of the default decrement icon.
 * @slot hint - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the control loses focus.
 * @event change - Emitted when an alteration to the control's value is committed by the user.
 * @event focus - Emitted when the control gains focus.
 * @event input - Emitted when the control receives input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart label - The label element.
 * @csspart form-control-label - Alias for the label element.
 * @csspart hint - The hint element.
 * @csspart base - The wrapper containing the input and steppers.
 * @csspart input - The internal `<input>` control.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart stepper - Both stepper buttons (for shared styling).
 * @csspart stepper-increment - The increment (+) button on the end side.
 * @csspart stepper-decrement - The decrement (-) button on the start side.
 *
 * @cssstate blank - The input is empty.
 * @cssstate focused - The input has focus.
 */
export default class WaNumberInput extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    assumeInteractionOn: string[];
    private readonly hasSlotController;
    private readonly localize;
    input: HTMLInputElement;
    title: string;
    private _value;
    /** The current value of the input, submitted as a name/value pair with form data. */
    get value(): string | null;
    set value(val: string | null);
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultValue: string | null;
    /** The input's size. */
    size: 'small' | 'medium' | 'large';
    /** The input's visual appearance. */
    appearance: 'filled' | 'outlined' | 'filled-outlined';
    /** Draws a pill-style input with rounded edges. */
    pill: boolean;
    /** The input's label. If you need to display HTML, use the `label` slot instead. */
    label: string;
    /** The input's hint. If you need to display HTML, use the `hint` slot instead. */
    hint: string;
    /** Placeholder text to show as a hint when the input is empty. */
    placeholder: string;
    /** Makes the input readonly. */
    readonly: boolean;
    /** Makes the input a required field. */
    required: boolean;
    /** The input's minimum value. */
    min: number;
    /** The input's maximum value. */
    max: number;
    /**
     * Specifies the granularity that the value must adhere to, or the special value `any` which means no stepping is
     * implied, allowing any numeric value.
     */
    step: number | 'any';
    /** Hides the increment/decrement stepper buttons. */
    withoutSteppers: boolean;
    /**
     * Specifies what permission the browser has to provide assistance in filling out form field values. Refer to
     * [this page on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for available values.
     */
    autocomplete: string;
    /** Indicates that the input should receive focus on page load. */
    autofocus: boolean;
    /** Used to customize the label or icon of the Enter key on virtual keyboards. */
    enterkeyhint: 'enter' | 'done' | 'go' | 'next' | 'previous' | 'search' | 'send';
    /**
     * Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual
     * keyboard on supportive devices.
     */
    inputmode: 'numeric' | 'decimal';
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
    /** Returns true if the value is at or below the minimum. */
    private get isAtMin();
    /** Returns true if the value is at or above the maximum. */
    private get isAtMax();
    private handleChange;
    private handleInput;
    private handleKeyDown;
    private handleStepperPointerUp;
    private handleStepperPointerDown;
    updated(changedProperties: PropertyValues<this>): void;
    handleStepChange(): void;
    /** Sets focus on the input. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the input. */
    blur(): void;
    /** Selects all the text in the input. */
    select(): void;
    /** Increments the value by the step amount. */
    stepUp(): void;
    /** Decrements the value by the step amount. */
    stepDown(): void;
    formResetCallback(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-number-input': WaNumberInput;
    }
}
