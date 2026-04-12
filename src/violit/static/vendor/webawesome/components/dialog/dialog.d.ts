import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../button/button.js';
/**
 * @summary Dialogs, sometimes called "modals", appear above the page and require the user's immediate attention.
 * @documentation https://webawesome.com/docs/components/dialog
 * @status stable
 * @since 2.0
 *
 * @dependency wa-button
 *
 * @slot - The dialog's main content.
 * @slot label - The dialog's label. Alternatively, you can use the `label` attribute.
 * @slot header-actions - Optional actions to add to the header. Works best with `<wa-button>`.
 * @slot footer - The dialog's footer, usually one or more buttons representing various options.
 *
 * @event wa-show - Emitted when the dialog opens.
 * @event wa-after-show - Emitted after the dialog opens and all animations are complete.
 * @event {{ source: Element }} wa-hide - Emitted when the dialog is requested to close. Calling
 *  `event.preventDefault()` will prevent the dialog from closing. You can inspect `event.detail.source` to see which
 *  element caused the dialog to close. If the source is the dialog element itself, the user has pressed [[Escape]] or
 *  the dialog has been closed programmatically. Avoid using this unless closing the dialog will result in destructive
 *  behavior such as data loss.
 * @event wa-after-hide - Emitted after the dialog closes and all animations are complete.
 *
 * @csspart dialog - The dialog's internal `<dialog>` element.
 * @csspart header - The dialog's header. This element wraps the title and header actions.
 * @csspart header-actions - Optional actions to add to the header. Works best with `<wa-button>`.
 * @csspart title - The dialog's title.
 * @csspart close-button - The close button, a `<wa-button>`.
 * @csspart close-button__base - The close button's exported `base` part.
 * @csspart body - The dialog's body.
 * @csspart footer - The dialog's footer.
 *
 * @cssproperty --spacing - The amount of space around and between the dialog's content.
 * @cssproperty --width - The preferred width of the dialog. Note that the dialog will shrink to accommodate smaller screens.
 * @cssproperty [--show-duration=200ms] - The animation duration when showing the dialog.
 * @cssproperty [--hide-duration=200ms] - The animation duration when hiding the dialog.
 */
export default class WaDialog extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly localize;
    private readonly hasSlotController;
    private originalTrigger;
    dialog: HTMLDialogElement;
    /** Indicates whether or not the dialog is open. Toggle this attribute to show and hide the dialog. */
    open: boolean;
    /**
     * The dialog's label as displayed in the header. You should always include a relevant label, as it is required for
     * proper accessibility. If you need to display HTML, use the `label` slot instead.
     */
    label: string;
    /** Disables the header. This will also remove the default close button. */
    withoutHeader: boolean;
    /** When enabled, the dialog will be closed when the user clicks outside of it. */
    lightDismiss: boolean;
    /**
     * Only required for SSR. Set to `true` if you're slotting in a `footer` element so the server-rendered markup
     * includes the footer before the component hydrates on the client.
     */
    withFooter: boolean;
    firstUpdated(): void;
    disconnectedCallback(): void;
    private requestClose;
    private addOpenListeners;
    private removeOpenListeners;
    private handleDialogCancel;
    private handleDialogClick;
    private handleDialogPointerDown;
    private handleDocumentKeyDown;
    handleOpenChange(): void;
    /** Shows the dialog. */
    private show;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-dialog': WaDialog;
    }
}
