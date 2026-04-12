import { LitElement } from 'lit';
import WebAwesomeElement from './webawesome-element.js';
export interface Validator<T extends WebAwesomeFormAssociatedElement = WebAwesomeFormAssociatedElement> {
    observedAttributes?: string[];
    checkValidity: (element: T) => {
        message: string;
        isValid: boolean;
        invalidKeys: Exclude<keyof ValidityState, 'valid'>[];
    };
    message?: string | ((element: T) => string);
}
export interface WebAwesomeFormControl extends WebAwesomeElement {
    name: null | string;
    disabled?: boolean;
    defaultValue?: unknown;
    defaultChecked?: boolean;
    checked?: boolean;
    defaultSelected?: boolean;
    selected?: boolean;
    get form(): HTMLFormElement | null;
    set form(val: string);
    value?: unknown;
    pattern?: string;
    min?: number | string | Date;
    max?: number | string | Date;
    step?: number | 'any';
    required?: boolean;
    minlength?: number;
    maxlength?: number;
    readonly validity: ValidityState;
    readonly validationMessage: string;
    checkValidity: () => boolean;
    getForm: () => HTMLFormElement | null;
    reportValidity: () => boolean;
    setCustomValidity: (message: string) => void;
    hasInteracted: boolean;
    valueHasChanged?: boolean;
    /** Convenience API for `setCustomValidity()` */
    customError: null | string;
}
export declare class WebAwesomeFormAssociatedElement extends WebAwesomeElement implements Omit<ElementInternals, 'form' | 'setFormValue'>, WebAwesomeFormControl {
    static formAssociated: boolean;
    /**
     * Validators are static because they have `observedAttributes`, essentially attributes to "watch"
     * for changes. Whenever these attributes change, we want to be notified and update the validator.
     */
    static get validators(): Validator[];
    static get observedAttributes(): string[];
    /** The name of the input, submitted as a name/value pair with form data. */
    name: string | null;
    /** Disables the form control. */
    disabled: boolean;
    required: boolean;
    assumeInteractionOn: string[];
    input?: (HTMLElement & {
        value: unknown;
    }) | HTMLInputElement | HTMLTextAreaElement;
    validators: Validator[];
    valueHasChanged: boolean;
    hasInteracted: boolean;
    customError: string | null;
    private emittedEvents;
    constructor();
    states: CustomStateSet;
    connectedCallback(): void;
    firstUpdated(...args: Parameters<LitElement['firstUpdated']>): void;
    emitInvalid: (e: Event) => void;
    protected willUpdate(changedProperties: Parameters<LitElement['willUpdate']>[0]): void;
    private handleInteraction;
    get labels(): NodeList;
    getForm(): HTMLFormElement | null;
    /**
     * By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
     * to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
     * the same document or shadow root for this to work.
     */
    set form(val: string);
    get form(): HTMLFormElement | null;
    get validity(): ValidityState;
    get willValidate(): boolean;
    get validationMessage(): string;
    checkValidity(): boolean;
    reportValidity(): boolean;
    /**
     * Override this to change where constraint validation popups are anchored.
     */
    get validationTarget(): undefined | HTMLElement;
    setValidity(...args: Parameters<typeof this.internals.setValidity>): void;
    setCustomStates(): void;
    /**
     * Do not use this when creating a "Validator". This is intended for end users of components.
     * We track manually defined custom errors so we don't clear them on accident in our validators.
     *
     */
    setCustomValidity(message: string): void;
    formResetCallback(): void;
    formDisabledCallback(isDisabled: boolean): void;
    /**
     * Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
     * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
     * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
     */
    formStateRestoreCallback(state: string | File | FormData | null, reason: 'autocomplete' | 'restore'): void;
    setValue(...args: Parameters<typeof this.internals.setFormValue>): void;
    get allValidators(): Validator<WebAwesomeFormAssociatedElement>[];
    /**
     * Reset validity is a way of removing manual custom errors and native validation.
     */
    resetValidity(): void;
    updateValidity(): void;
}
