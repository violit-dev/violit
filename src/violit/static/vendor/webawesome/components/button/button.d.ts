import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
import '../spinner/spinner.js';
/**
 * @summary Buttons represent actions that are available to the user.
 * @documentation https://webawesome.com/docs/components/button
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 * @dependency wa-spinner
 *
 * @event blur - Emitted when the button loses focus.
 * @event focus - Emitted when the button gains focus.
 * @event wa-invalid - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
 *
 * @slot - The button's label.
 * @slot start - An element, such as `<wa-icon>`, placed before the label.
 * @slot end - An element, such as `<wa-icon>`, placed after the label.
 *
 * @csspart base - The component's base wrapper.
 * @csspart start - The container that wraps the `start` slot.
 * @csspart label - The button's label.
 * @csspart end - The container that wraps the `end` slot.
 * @csspart caret - The button's caret icon, a `<wa-icon>` element.
 * @csspart spinner - The spinner that shows when the button is in the loading state.
 *
 * @cssstate disabled - Applied when the button is disabled.
 * @cssstate icon-button - Applied when the button contains only a `<wa-icon>` with no other content.
 * @cssstate link - Applied when the button is rendered as a link (i.e. `href` is set).
 * @cssstate loading - Applied when the button is in the loading state.
 */
export default class WaButton extends WebAwesomeFormAssociatedElement {
    static shadowRootOptions: {
        delegatesFocus: boolean;
        mode: ShadowRootMode;
        serializable?: boolean;
        slotAssignment?: SlotAssignmentMode;
    };
    static css: import("lit").CSSResult[];
    static get validators(): import("../../internal/webawesome-form-associated-element.js").Validator<WebAwesomeFormAssociatedElement>[];
    assumeInteractionOn: string[];
    private readonly hasSlotController;
    private readonly localize;
    button: HTMLButtonElement | HTMLLinkElement;
    labelSlot: HTMLSlotElement;
    invalid: boolean;
    isIconButton: boolean;
    title: string;
    /** The button's theme variant. Defaults to `neutral` if not within another element with a variant. */
    variant: 'neutral' | 'brand' | 'success' | 'warning' | 'danger';
    /** The button's visual appearance. */
    appearance: 'accent' | 'filled' | 'outlined' | 'filled-outlined' | 'plain';
    /** The button's size. */
    size: 'small' | 'medium' | 'large';
    /** Draws the button with a caret. Used to indicate that the button triggers a dropdown menu or similar behavior. */
    withCaret: boolean;
    /**
     * Only required for SSR. Set to `true` if you're slotting in a `start` element so the server-rendered markup
     * includes the start slot before the component hydrates on the client.
     */
    withStart: boolean;
    /**
     * Only required for SSR. Set to `true` if you're slotting in an `end` element so the server-rendered markup
     * includes the end slot before the component hydrates on the client.
     */
    withEnd: boolean;
    /** Disables the button. */
    disabled: boolean;
    /** Draws the button in a loading state. */
    loading: boolean;
    /** Draws a pill-style button with rounded edges. */
    pill: boolean;
    /**
     * The type of button. Note that the default value is `button` instead of `submit`, which is opposite of how native
     * `<button>` elements behave. When the type is `submit`, the button will submit the surrounding form.
     */
    type: 'button' | 'submit' | 'reset';
    /**
     * The name of the button, submitted as a name/value pair with form data, but only when this button is the submitter.
     * This attribute is ignored when `href` is present.
     */
    name: string;
    /**
     * The value of the button, submitted as a pair with the button's name as part of the form data, but only when this
     * button is the submitter. This attribute is ignored when `href` is present.
     */
    value: string;
    /** When set, the underlying button will be rendered as an `<a>` with this `href` instead of a `<button>`. */
    href: string;
    /** Tells the browser where to open the link. Only used when `href` is present. */
    target: '_blank' | '_parent' | '_self' | '_top';
    /** When using `href`, this attribute will map to the underlying link's `rel` attribute. */
    rel?: string;
    /** Tells the browser to download the linked file as this filename. Only used when `href` is present. */
    download?: string;
    /**
     * The "form owner" to associate the button with. If omitted, the closest containing form will be used instead. The
     * value of this attribute must be an id of a form in the same document or shadow root as the button.
     */
    /** Used to override the form owner's `action` attribute. */
    formAction: string;
    /** Used to override the form owner's `enctype` attribute.  */
    formEnctype: 'application/x-www-form-urlencoded' | 'multipart/form-data' | 'text/plain';
    /** Used to override the form owner's `method` attribute.  */
    formMethod: 'post' | 'get';
    /** Used to override the form owner's `novalidate` attribute. */
    formNoValidate: boolean;
    /** Used to override the form owner's `target` attribute. */
    formTarget: '_self' | '_blank' | '_parent' | '_top' | string;
    private constructLightDOMButton;
    private handleClick;
    private handleInvalid;
    private handleLabelSlotChange;
    private isButton;
    private isLink;
    handleDisabledChange(): void;
    handleHrefChange(): void;
    handleLoadingChange(): void;
    setValue(..._args: Parameters<WebAwesomeFormAssociatedElement['setValue']>): void;
    /** Simulates a click on the button. */
    click(): void;
    /** Sets focus on the button. */
    focus(options?: FocusOptions): void;
    /** Removes focus from the button. */
    blur(): void;
    render(): import("lit-html").TemplateResult;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-button': WaButton;
    }
}
