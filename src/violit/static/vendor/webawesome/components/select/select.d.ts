import type { PropertyValues, TemplateResult } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
import '../option/option.js';
import type WaOption from '../option/option.js';
import '../popup/popup.js';
import type WaPopup from '../popup/popup.js';
import '../tag/tag.js';
/**
 * @summary Selects allow you to choose items from a menu of predefined options.
 * @documentation https://webawesome.com/docs/components/select
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 * @dependency wa-popup
 * @dependency wa-tag
 * @dependency wa-option
 *
 * @slot - The listbox options. Must be `<wa-option>` elements. You can use `<wa-divider>` to group items visually.
 * @slot label - The input's label. Alternatively, you can use the `label` attribute.
 * @slot start - An element, such as `<wa-icon>`, placed at the start of the combobox.
 * @slot end - An element, such as `<wa-icon>`, placed at the end of the combobox.
 * @slot clear-icon - An icon to use in lieu of the default clear icon.
 * @slot expand-icon - The icon to show when the control is expanded and collapsed. Rotates on open and close.
 * @slot hint - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
 *
 * @event change - Emitted when the control's value changes.
 * @event input - Emitted when the control receives input.
 * @event focus - Emitted when the control gains focus.
 * @event blur - Emitted when the control loses focus.
 * @event wa-clear - Emitted when the control's value is cleared.
 * @event wa-show - Emitted when the select's menu opens.
 * @event wa-after-show - Emitted after the select's menu opens and all animations are complete.
 * @event wa-hide - Emitted when the select's menu closes.
 * @event wa-after-hide - Emitted after the select's menu closes and all animations are complete.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @csspart form-control - The form control that wraps the label, input, and hint.
 * @csspart form-control-label - The label's wrapper.
 * @csspart form-control-input - The select's wrapper.
 * @csspart hint - The hint's wrapper.
 * @csspart combobox - The container the wraps the start, end, value, clear icon, and expand button.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart display-input - The element that displays the selected option's label, an `<input>` element.
 * @csspart listbox - The listbox container where options are slotted.
 * @csspart tags - The container that houses option tags when `multiselect` is used.
 * @csspart tag - The individual tags that represent each multiselect option.
 * @csspart tag__content - The tag's content part.
 * @csspart tag__remove-button - The tag's remove button.
 * @csspart tag__remove-button__base - The tag's remove button base part.
 * @csspart clear-button - The clear button.
 * @csspart expand-icon - The container that wraps the expand icon.
 *
 * @cssproperty [--show-duration=100ms] - The duration of the show animation.
 * @cssproperty [--hide-duration=100ms] - The duration of the hide animation.
 * @cssproperty [--tag-max-size=10ch] - When using `multiple`, the max size of tags before their content is truncated.
 *
 * @cssstate blank - The select is empty.
 */
export default class WaSelect extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    assumeInteractionOn: string[];
    private cachedOptions;
    private readonly hasSlotController;
    private readonly localize;
    private selectionOrder;
    private typeToSelectString;
    private typeToSelectTimeout;
    private slotChangePending;
    popup: WaPopup;
    combobox: HTMLSlotElement;
    displayInput: HTMLInputElement;
    valueInput: HTMLInputElement;
    listbox: HTMLSlotElement;
    /** Where to anchor native constraint validation */
    get validationTarget(): HTMLInputElement;
    displayLabel: string;
    currentOption: WaOption;
    selectedOptions: WaOption[];
    /** @internal */
    optionValues: Set<string | null> | undefined;
    /** The name of the select, submitted as a name/value pair with form data. */
    name: string;
    private _defaultValue;
    set defaultValue(val: null | string | string[]);
    get defaultValue(): null | string | string[];
    private rawValuesEqual;
    /**
     * @private
     * A converter for defaultValue from array to string if its multiple. Also fixes some hydration issues.
     */
    private convertDefaultValue;
    private _value;
    /** The select's value. This will be a string for single select or an array for multi-select. */
    set value(val: string | string[] | null);
    get value(): string | string[] | null;
    /** The select's size. */
    size: 'small' | 'medium' | 'large';
    /** Placeholder text to show as a hint when the select is empty. */
    placeholder: string;
    /** Allows more than one option to be selected. */
    multiple: boolean;
    /**
     * The maximum number of selected options to show when `multiple` is true. After the maximum, "+n" will be shown to
     * indicate the number of additional items that are selected. Set to 0 to remove the limit.
     */
    maxOptionsVisible: number;
    /** Disables the select control. */
    disabled: boolean;
    /** Adds a clear button when the select is not empty. */
    withClear: boolean;
    /**
     * Indicates whether or not the select is open. You can toggle this attribute to show and hide the menu, or you can
     * use the `show()` and `hide()` methods and this attribute will reflect the select's open state.
     */
    open: boolean;
    /** The select's visual appearance. */
    appearance: 'filled' | 'outlined' | 'filled-outlined';
    /** Draws a pill-style select with rounded edges. */
    pill: boolean;
    /** The select's label. If you need to display HTML, use the `label` slot instead. */
    label: string;
    /**
     * The preferred placement of the select's menu. Note that the actual placement may vary as needed to keep the listbox
     * inside of the viewport.
     */
    placement: 'top' | 'bottom';
    /** The select's hint. If you need to display HTML, use the `hint` slot instead. */
    hint: string;
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
    /** The select's required attribute. */
    required: boolean;
    /**
     * A function that customizes the tags to be rendered when multiple=true. The first argument is the option, the second
     * is the current tag's index.  The function should return either a Lit TemplateResult or a string containing trusted
     * HTML of the symbol to render at the specified value.
     */
    getTag: (option: WaOption, index: number) => TemplateResult | string | HTMLElement;
    connectedCallback(): void;
    disconnectedCallback(): void;
    private updateDefaultValue;
    private addOpenListeners;
    private removeOpenListeners;
    private handleFocus;
    private handleDocumentFocusIn;
    private handleDocumentKeyDown;
    private handleDocumentMouseDown;
    private handleLabelClick;
    private handleComboboxClick;
    private handleComboboxMouseDown;
    private handleComboboxKeyDown;
    private handleClearClick;
    private handleClearMouseDown;
    private handleOptionClick;
    handleDefaultSlotChange(): void;
    private processSlotChange;
    private handleTagRemove;
    private getAllOptions;
    private getFirstOption;
    private setCurrentOption;
    private setSelectedOptions;
    private toggleOptionSelection;
    selectionChanged(): void;
    protected get tags(): (import("lit-html/directive.js").DirectiveResult<typeof import("lit-html/directives/unsafe-html.js").UnsafeHTMLDirective> | null)[];
    updated(changedProperties: PropertyValues<this>): void;
    handleDisabledChange(): void;
    handleValueChange(): void;
    handleOpenChange(): Promise<void>;
    /** Shows the listbox. */
    show(): Promise<void>;
    /** Hides the listbox. */
    hide(): Promise<void>;
    /** Sets focus on the control. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the control. */
    blur(): void;
    formResetCallback(): void;
    render(): TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-select': WaSelect;
    }
}
