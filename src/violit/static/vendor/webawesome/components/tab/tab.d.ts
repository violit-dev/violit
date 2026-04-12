import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Tabs are used inside [tab groups](/docs/components/tab-group) to represent and activate [tab panels](/docs/components/tab-panel).
 * @documentation https://webawesome.com/docs/components/tab
 * @status stable
 * @since 2.0
 *
 * @slot - The tab's label.
 *
 * @csspart base - The component's base wrapper.
 */
export default class WaTab extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly attrId;
    private readonly componentId;
    tab: HTMLElement;
    /** The name of the tab panel this tab is associated with. The panel must be located in the same tab group. */
    panel: string;
    /** @internal Draws the tab in an active state. */
    active: boolean;
    /** Disables the tab and prevents selection. */
    disabled: boolean;
    /**
     * @internal
     * Need to wrap in a `@property()` otherwise NextJS blows up.
     */
    tabIndex: number;
    connectedCallback(): void;
    handleActiveChange(): void;
    handleDisabledChange(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-tab': WaTab;
    }
}
