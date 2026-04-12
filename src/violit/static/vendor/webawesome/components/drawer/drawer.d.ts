import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../button/button.js';
/**
 * @summary Drawers slide in from a container to expose additional options and information.
 * @documentation https://webawesome.com/docs/components/drawer
 * @status stable
 * @since 2.0
 *
 * @dependency wa-button
 *
 * @slot - The drawer's main content.
 * @slot label - The drawer's label. Alternatively, you can use the `label` attribute.
 * @slot header-actions - Optional actions to add to the header. Works best with `<wa-button>`.
 * @slot footer - The drawer's footer, usually one or more buttons representing various options.
 *
 * @event wa-show - Emitted when the drawer opens.
 * @event wa-after-show - Emitted after the drawer opens and all animations are complete.
 * @event wa-hide - Emitted when the drawer closes.
 * @event wa-after-hide - Emitted after the drawer closes and all animations are complete.
 * @event {{ source: Element }} wa-hide - Emitted when the drawer is requesting to close. Calling
 *  `event.preventDefault()` will prevent the drawer from closing. You can inspect `event.detail.source` to see which
 *  element caused the drawer to close. If the source is the drawer element itself, the user has pressed [[Escape]] or
 *  the drawer has been closed programmatically. Avoid using this unless closing the drawer will result in destructive
 *  behavior such as data loss.
 *
 * @csspart dialog - The drawer's internal `<dialog>` element.
 * @csspart header - The drawer's header. This element wraps the title and header actions.
 * @csspart header-actions - Optional actions to add to the header. Works best with `<wa-button>`.
 * @csspart title - The drawer's title.
 * @csspart close-button - The close button, a `<wa-button>`.
 * @csspart close-button__base - The close button's exported `base` part.
 * @csspart body - The drawer's body.
 * @csspart footer - The drawer's footer.
 *
 * @cssproperty --spacing - The amount of space around and between the drawer's content.
 * @cssproperty --size - The preferred size of the drawer. This will be applied to the drawer's width or height
 *   depending on its `placement`. Note that the drawer will shrink to accommodate smaller screens.
 * @cssproperty [--show-duration=200ms] - The animation duration when showing the drawer.
 * @cssproperty [--hide-duration=200ms] - The animation duration when hiding the drawer.
 *
 * @property modal - Exposes the internal modal utility that controls focus trapping. To temporarily disable focus
 *   trapping and allow third-party modals spawned from an active Shoelace modal, call `modal.activateExternal()` when
 *   the third-party modal opens. Upon closing, call `modal.deactivateExternal()` to restore Shoelace's focus trapping.
 */
export default class WaDrawer extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly localize;
    private readonly hasSlotController;
    private originalTrigger;
    drawer: HTMLDialogElement;
    /** Indicates whether or not the drawer is open. Toggle this attribute to show and hide the drawer. */
    open: boolean;
    /**
     * The drawer's label as displayed in the header. You should always include a relevant label, as it is required for
     * proper accessibility. If you need to display HTML, use the `label` slot instead.
     */
    label: string;
    /** The direction from which the drawer will open. */
    placement: 'top' | 'end' | 'bottom' | 'start';
    /** Disables the header. This will also remove the default close button. */
    withoutHeader: boolean;
    /** When enabled, the drawer will be closed when the user clicks outside of it. */
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
    /** Shows the drawer. */
    private show;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-drawer': WaDrawer;
    }
}
