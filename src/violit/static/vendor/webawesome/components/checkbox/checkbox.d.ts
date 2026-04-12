import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
/**
 * @summary Checkboxes allow the user to toggle an option on or off.
 * @documentation https://webawesome.com/docs/components/checkbox
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @slot - The checkbox's label.
 * @slot hint - Text that describes how to use the checkbox. Alternatively, you can use the `hint` attribute.
 *
 * @event blur - Emitted when the checkbox loses focus.
 * @event change - Emitted when the checked state changes.
 * @event focus - Emitted when the checkbox gains focus.
 * @event input - Emitted when the checkbox receives input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart base - The component's label .
 * @csspart control - The square container that wraps the checkbox's checked state.
 * @csspart checked-icon - The checked icon, a `<wa-icon>` element.
 * @csspart indeterminate-icon - The indeterminate icon, a `<wa-icon>` element.
 * @csspart label - The container that wraps the checkbox's label.
 * @csspart hint - The hint's wrapper.
 *
 * @cssproperty --checked-icon-color - The color of the checked and indeterminate icons.
 * @cssproperty --checked-icon-scale - The size of the checked and indeterminate icons relative to the checkbox.
 *
 * @cssstate checked - Applied when the checkbox is checked.
 * @cssstate disabled - Applied when the checkbox is disabled.
 * @cssstate indeterminate - Applied when the checkbox is in an indeterminate state.
 *
 */
export default class WaCheckbox extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    private readonly hasSlotController;
    input: HTMLInputElement;
    title: string;
    /** The name of the checkbox, submitted as a name/value pair with form data. */
    name: null;
    private _value;
    /** The value of the checkbox, submitted as a name/value pair with form data. */
    get value(): string | null;
    set value(val: string | null);
    /** The checkbox's size. */
    size: 'small' | 'medium' | 'large';
    /** Disables the checkbox. */
    disabled: boolean;
    /**
     * Draws the checkbox in an indeterminate state. This is usually applied to checkboxes that represents a "select
     * all/none" behavior when associated checkboxes have a mix of checked and unchecked states.
     */
    indeterminate: boolean;
    _checked: boolean | null;
    get checked(): boolean;
    /** Draws the checkbox in a checked state. */
    set checked(val: boolean);
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultChecked: boolean;
    /** Makes the checkbox a required field. */
    required: boolean;
    /** The checkbox's hint. If you need to display HTML, use the `hint` slot instead. */
    hint: string;
    private handleClick;
    connectedCallback(): void;
    handleDefaultCheckedChange(): void;
    handleValueOrCheckedChange(): void;
    handleStateChange(): void;
    handleDisabledChange(): void;
    protected willUpdate(changedProperties: PropertyValues<this>): void;
    formResetCallback(): void;
    /** Simulates a click on the checkbox. */
    click(): void;
    /** Sets focus on the checkbox. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the checkbox. */
    blur(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-checkbox': WaCheckbox;
    }
}
