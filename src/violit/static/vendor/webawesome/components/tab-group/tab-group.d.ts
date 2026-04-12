import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../button/button.js';
import '../tab-panel/tab-panel.js';
import '../tab/tab.js';
/**
 * @summary Tab groups organize content into a container that shows one section at a time.
 * @documentation https://webawesome.com/docs/components/tab-group
 * @status stable
 * @since 2.0
 *
 * @dependency wa-button
 * @dependency wa-tab
 * @dependency wa-tab-panel
 *
 * @slot - Used for grouping tab panels in the tab group. Must be `<wa-tab-panel>` elements.
 * @slot nav - Used for grouping tabs in the tab group. Must be `<wa-tab>` elements. Note that `<wa-tab>` will set this
 *  slot on itself automatically.
 *
 * @event {{ name: String }} wa-tab-show - Emitted when a tab is shown.
 * @event {{ name: String }} wa-tab-hide - Emitted when a tab is hidden.
 *
 * @csspart base - The component's base wrapper.
 * @csspart nav - The tab group's navigation container where tabs are slotted in.
 * @csspart tabs - The container that wraps the tabs.
 * @csspart body - The tab group's body where tab panels are slotted in.
 * @csspart scroll-button - The previous/next scroll buttons that show when tabs are scrollable, a `<wa-button>`.
 * @csspart scroll-button-start - The starting scroll button.
 * @csspart scroll-button-end - The ending scroll button.
 * @csspart scroll-button__base - The scroll button's exported `base` part.
 *
 * @cssproperty --indicator-color - The color of the active tab indicator.
 * @cssproperty --track-color - The color of the indicator's track (the line that separates tabs from panels).
 * @cssproperty --track-width - The width of the indicator's track (the line that separates tabs from panels).
 */
export default class WaTabGroup extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private activeTab?;
    private mutationObserver;
    private resizeObserver;
    private tabs;
    private focusableTabs;
    private panels;
    private readonly localize;
    tabGroup: HTMLElement;
    /** Default slot for `<wa-tab-panel>` children (inside the `body` part container). */
    defaultSlot: HTMLSlotElement;
    nav: HTMLElement;
    private hasScrollControls;
    /** Sets the active tab. */
    active: string;
    /** The placement of the tabs. */
    placement: 'top' | 'bottom' | 'start' | 'end';
    /**
     * When set to auto, navigating tabs with the arrow keys will instantly show the corresponding tab panel. When set to
     * manual, the tab will receive focus but will not show until the user presses spacebar or enter.
     */
    activation: 'auto' | 'manual';
    /** Disables the scroll arrows that appear when tabs overflow. */
    withoutScrollControls: boolean;
    connectedCallback(): void;
    disconnectedCallback(): void;
    private getAllTabs;
    private getAllPanels;
    private getActiveTab;
    private handleClick;
    private handleKeyDown;
    private findNextFocusableTab;
    private handleScrollToStart;
    private handleScrollToEnd;
    private setActiveTab;
    private setAriaLabels;
    private syncTabsAndPanels;
    updateActiveTab(): void;
    updateScrollControls(): void;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-tab-group': WaTabGroup;
    }
}
