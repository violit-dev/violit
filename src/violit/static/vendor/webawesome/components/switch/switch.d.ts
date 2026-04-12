import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
/**
 * @summary Switches allow the user to toggle an option on or off.
 * @documentation https://webawesome.com/docs/components/switch
 * @status stable
 * @since 2.0
 *
 * @slot - The switch's label.
 * @slot hint - Text that describes how to use the switch. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the control loses focus.
 * @event change - Emitted when the control's checked state changes.
 * @event input - Emitted when the control receives input.
 * @event focus - Emitted when the control gains focus.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart base - The component's base wrapper.
 * @csspart control - The control that houses the switch's thumb.
 * @csspart thumb - The switch's thumb.
 * @csspart label - The switch's label.
 * @csspart hint - The hint's wrapper.
 *
 * @cssproperty --width - The width of the switch.
 * @cssproperty --height - The height of the switch.
 * @cssproperty --thumb-size - The size of the thumb.
 */
export default class WaSwitch extends WebAwesomeFormAssociatedElement {
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    private readonly hasSlotController;
    input: HTMLInputElement;
    title: string;
    /** The name of the switch, submitted as a name/value pair with form data. */
    name: string | null;
    private _value;
    /** The value of the switch, submitted as a name/value pair with form data. */
    get value(): string | null;
    set value(val: string | null);
    /** The switch's size. */
    size: 'small' | 'medium' | 'large';
    /** Disables the switch. */
    disabled: boolean;
    _checked: boolean | null;
    get checked(): boolean;
    /** Draws the checkbox in a checked state. */
    set checked(val: boolean);
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultChecked: boolean;
    /** Makes the switch a required field. */
    required: boolean;
    /** The switch's hint. If you need to display HTML, use the `hint` slot instead. */
    hint: string;
    /**
     * Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
     * includes the hint before the component hydrates on the client.
     */
    withHint: boolean;
    private handleClick;
    private handleKeyDown;
    protected willUpdate(changedProperties: PropertyValues<this>): void;
    handleValueOrCheckedChange(): void;
    handleStateChange(): void;
    handleDisabledChange(): void;
    /** Simulates a click on the switch. */
    click(): void;
    /** Sets focus on the switch. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the switch. */
    blur(): void;
    setValue(value: string | File | FormData | null, stateValue?: string | File | FormData | null | undefined): void;
    formResetCallback(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-switch': WaSwitch;
    }
}
