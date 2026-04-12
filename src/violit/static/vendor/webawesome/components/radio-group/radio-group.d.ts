import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../radio/radio.js';
import type WaRadio from '../radio/radio.js';
/**
 * @summary Radio groups are used to group multiple [radios](/docs/components/radio) so they function as a single form control.
 * @documentation https://webawesome.com/docs/components/radio-group
 * @status stable
 * @since 2.0
 *
 * @dependency wa-radio
 *
 * @slot - The default slot where `<wa-radio>` elements are placed.
 * @slot label - The radio group's label. Required for proper accessibility. Alternatively, you can use the `label`
 *  attribute.
 * @slot hint - Text that describes how to use the radio group. Alternatively, you can use the `hint` attribute.
 *
 * @event change - Emitted when the radio group's selected value changes.
 * @event input - Emitted when the radio group receives user input.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart form-control - The form control that wraps the label, input, and hint.
 * @csspart form-control-label - The label's wrapper.
 * @csspart form-control-input - The input's wrapper.
 * @csspart radios - The wrapper than surrounds radio items, styled as a flex container by default.
 * @csspart hint - The hint's wrapper.
 */
export default class WaRadioGroup extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    private readonly hasSlotController;
    defaultSlot: HTMLSlotElement;
    /**
     * The radio group's label. Required for proper accessibility. If you need to display HTML, use the `label` slot
     * instead.
     */
    label: string;
    /** The radio groups's hint. If you need to display HTML, use the `hint` slot instead. */
    hint: string;
    /** The name of the radio group, submitted as a name/value pair with form data. */
    name: string | null;
    /** Disables the radio group and all child radios. */
    disabled: boolean;
    /** The orientation in which to show radio items. */
    orientation: 'horizontal' | 'vertical';
    private _value;
    get value(): string | number | null;
    /** The current value of the radio group, submitted as a name/value pair with form data. */
    set value(val: string | number | null);
    /** The default value of the form control. Primarily used for resetting the form control. */
    defaultValue: string | null;
    /** The radio group's size. When present, this size will be applied to all `<wa-radio>` items inside. */
    size: 'small' | 'medium' | 'large';
    /** Ensures a child radio is checked before allowing the containing form to submit. */
    required: boolean;
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
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    constructor();
    /**
     * We use the first available radio as the validationTarget similar to native HTML that shows the validation popup on
     * the first radio element.
     */
    get validationTarget(): WaRadio | undefined;
    updated(changedProperties: PropertyValues<this>): void;
    formResetCallback(...args: Parameters<WebAwesomeFormAssociatedElement['formResetCallback']>): void;
    private handleRadioClick;
    private getAllRadios;
    private handleLabelClick;
    private syncRadioElements;
    private handleKeyDown;
    /** Sets focus on the radio group. */
    focus(options?: FocusOptions): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-radio-group': WaRadioGroup;
    }
}
