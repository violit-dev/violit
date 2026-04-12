import type { PropertyValues } from 'lit';
import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../dropdown-item/dropdown-item.js';
import '../popup/popup.js';
/**
 * @summary Dropdowns display a list of options that can be triggered by a button or other element. They support
 *  keyboard navigation, submenus, and various customization options.
 * @documentation https://webawesome.com/docs/components/dropdown
 * @status stable
 * @since 2.0
 *
 * @dependency wa-dropdown-item
 * @dependency wa-popup
 *
 * @event wa-show - Emitted when the dropdown is about to show.
 * @event wa-after-show - Emitted after the dropdown has been shown.
 * @event wa-hide - Emitted when the dropdown is about to hide.
 * @event wa-after-hide - Emitted after the dropdown has been hidden.
 * @event wa-select - Emitted when an item in the dropdown is selected.
 *
 * @slot - The dropdown's items, typically `<wa-dropdown-item>` elements.
 * @slot trigger - The element that triggers the dropdown, such as a `<wa-button>` or `<button>`.
 *
 * @csspart base - The component's host element.
 * @csspart menu - The dropdown menu container.
 *
 * @cssproperty --show-duration - The duration of the show animation.
 * @cssproperty --hide-duration - The duration of the hide animation.
 */
export default class WaDropdown extends WebAwesomeElement {
    static css: import("lit").CSSResult[];
    private submenuCleanups;
    private readonly localize;
    private userTypedQuery;
    private userTypedTimeout;
    private openSubmenuStack;
    defaultSlot: HTMLSlotElement;
    private menu;
    private popup;
    /** Opens or closes the dropdown. */
    open: boolean;
    /** The dropdown's size. */
    size: 'small' | 'medium' | 'large';
    /**
     * The placement of the dropdown menu in reference to the trigger. The menu will shift to a more optimal location if
     * the preferred placement doesn't have enough room.
     */
    placement: 'top' | 'top-start' | 'top-end' | 'bottom' | 'bottom-start' | 'bottom-end' | 'right' | 'right-start' | 'right-end' | 'left' | 'left-start' | 'left-end';
    /** The distance of the dropdown menu from its trigger. */
    distance: number;
    /** The offset of the dropdown menu along its trigger. */
    skidding: number;
    disconnectedCallback(): void;
    firstUpdated(): void;
    updated(changedProperties: PropertyValues): Promise<void>;
    /** Gets all dropdown items slotted in the menu. */
    private getItems;
    /** Gets all dropdown items in a specific submenu. */
    private getSubmenuItems;
    /** Syncs item sizes with the dropdown's size property. */
    private syncItemSizes;
    /** Handles the submenu navigation stack */
    private addToSubmenuStack;
    /** Removes the last item from the submenu stack */
    private removeFromSubmenuStack;
    /** Gets the current active submenu item */
    private getCurrentSubmenuItem;
    /** Closes all submenus in the dropdown. */
    private closeAllSubmenus;
    /** Closes sibling submenus at the same level as the specified item. */
    private closeSiblingSubmenus;
    /** Get the slotted trigger button, a <wa-button> or <button> element */
    private getTrigger;
    /** Shows the dropdown menu. This should only be called from within updated(). */
    private showMenu;
    /** Hides the dropdown menu. This should only be called from within updated(). */
    private hideMenu;
    /** Handles key down events when the menu is open */
    private handleDocumentKeyDown;
    /** Handles pointer down events when the dropdown is open. */
    private handleDocumentPointerDown;
    /** Handles clicks on the menu. */
    private handleMenuClick;
    /** Prepares dropdown items when they get added or removed */
    private handleMenuSlotChange;
    /** Toggles the dropdown menu */
    private handleTriggerClick;
    /** Handles submenu opening events */
    private handleSubmenuOpening;
    /** Sets up submenu positioning with autoUpdate */
    private setupSubmenuPosition;
    private static handleSubmenuSlotChange;
    private processSubmenuItems;
    /** Cleans up submenu positioning */
    private cleanupSubmenuPosition;
    /** Positions a submenu relative to its parent item */
    private positionSubmenu;
    /** Updates the safe triangle coordinates for a submenu */
    private updateSafeTriangleCoordinates;
    /** Handle global mouse movement for safe triangle logic */
    private handleGlobalMouseMove;
    /** Makes a selection, emits the wa-select event, and closes the dropdown. */
    private makeSelection;
    /** Syncs aria attributes on the slotted trigger element and the menu based on the dropdown's current state */
    private syncAriaAttributes;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-dropdown': WaDropdown;
    }
}
