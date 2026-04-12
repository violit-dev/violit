import type { PropertyValues } from 'lit';
import { WebAwesomeFormAssociatedElement } from '../../internal/webawesome-form-associated-element.js';
import '../icon/icon.js';
/**
 * @summary Radios allow the user to select a single option from a group.
 * @documentation https://webawesome.com/docs/components/radio
 * @status stable
 * @since 2.0
 *
 * @dependency wa-icon
 *
 * @slot - The radio's label.
 *
 * @event blur - Emitted when the control loses focus.
 * @event focus - Emitted when the control gains focus.
 *
 * @csspart control - The circular container that wraps the radio's checked state.
 * @csspart checked-icon - The checked icon.
 * @csspart label - The container that wraps the radio's label.
 *
 * @cssproperty --checked-icon-color - The color of the checked icon.
 * @cssproperty --checked-icon-scale - The size of the checked icon relative to the radio.
 *
 * @cssstate checked - Applied when the control is checked.
 * @cssstate disabled - Applied when the control is disabled.
 */
export default class WaRadio extends WebAwesomeFormAssociatedElement {
    static css: import("lit").CSSResult[];
    checked: boolean;
    /** @internal Used by radio group to force disable radios while preserving their original disabled state. */
    forceDisabled: boolean;
    /** The radio's value. When selected, the radio group will receive this value. */
    value: string;
    /** The radio's visual appearance. */
    appearance: 'default' | 'button';
    /**
     * The radio's size. When used inside a radio group, the size will be determined by the radio group's size, which will
     * override this attribute.
     */
    size: 'small' | 'medium' | 'large';
    /** Disables the radio. */
    disabled: boolean;
    constructor();
    connectedCallback(): void;
    private setInitialAttributes;
    updated(changedProperties: PropertyValues<this>): void;
    /**
     * @override
     */
    setValue(): void;
    private handleClick;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-radio': WaRadio;
    }
}
