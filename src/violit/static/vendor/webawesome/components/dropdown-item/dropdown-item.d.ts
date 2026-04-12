import type { PropertyValues } from 'lit';
import WebAwesomeElement from '../../internal/webawesome-element.js';
import '../icon/icon.js';
/**
 * @summary Represents an individual item within a dropdown menu, supporting standard items, checkboxes, and submenus.
 * @documentation https://webawesome.com/docs/components/dropdown-item
 * @status experimental
 * @since 3.0
 *
 * @dependency wa-icon
 *
 * @event blur - Emitted when the dropdown item loses focus.
 * @event focus - Emitted when the dropdown item gains focus.
 *
 * @slot - The dropdown item's label.
 * @slot icon - An optional icon to display before the label.
 * @slot details - Additional content or details to display after the label.
 * @slot submenu - Submenu items, typically `<wa-dropdown-item>` elements, to create a nested menu.
 *
 * @csspart checkmark - The checkmark icon (a `<wa-icon>` element) when the item is a checkbox.
 * @csspart icon - The container for the icon slot.
 * @csspart label - The container for the label slot.
 * @csspart details - The container for the details slot.
 * @csspart submenu-icon - The submenu indicator icon (a `<wa-icon>` element).
 * @csspart submenu - The submenu container.
 */
export default class WaDropdownItem extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    private readonly hasSlotController;
    submenuElement: HTMLDivElement;
    /** @internal The controller will set this property to true when the item is active. */
    active: boolean;
    /** The type of menu item to render. */
    variant: 'danger' | 'default';
    /**
     * @internal The dropdown item's size.
     */
    size: 'small' | 'medium' | 'large';
    /**
     * @internal The controller will set this property to true when at least one checkbox exists in the dropdown. This
     * allows non-checkbox items to draw additional space to align properly with checkbox items.
     */
    checkboxAdjacent: boolean;
    /**
     * @internal The controller will set this property to true when at least one item with a submenu exists in the
     * dropdown. This allows non-submenu items to draw additional space to align properly with items that have submenus.
     */
    submenuAdjacent: boolean;
    /**
     * An optional value for the menu item. This is useful for determining which item was selected when listening to the
     * dropdown's `wa-select` event.
     */
    value: string;
    /** Set to `checkbox` to make the item a checkbox. */
    type: 'normal' | 'checkbox';
    /** Set to true to check the dropdown item. Only valid when `type` is `checkbox`. */
    checked: boolean;
    /** Disables the dropdown item. */
    disabled: boolean;
    /** Whether the submenu is currently open. */
    submenuOpen: boolean;
    /** @internal Store whether this item has a submenu */
    hasSubmenu: boolean;
    connectedCallback(): void;
    disconnectedCallback(): void;
    firstUpdated(): void;
    updated(changedProperties: PropertyValues<this>): void;
    private handleSlotChange;
    /** Update the has-submenu custom state */
    private updateHasSubmenuState;
    /** Opens the submenu. */
    openSubmenu(): Promise<void>;
    /** Notifies the parent dropdown that this item is opening its submenu */
    private notifyParentOfOpening;
    /** Closes the submenu. */
    closeSubmenu(): Promise<void>;
    /** Gets all dropdown items in the submenu. */
    private getSubmenuItems;
    /** Prevents click events from firing on the host when the item is disabled (e.g. programmatic .click() calls). */
    private handleHostClick;
    /** Prevents click events from firing when the item is disabled. */
    private handleClick;
    /** Handles mouse enter to open the submenu */
    private handleMouseEnter;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-dropdown-item': WaDropdownItem;
    }
}
