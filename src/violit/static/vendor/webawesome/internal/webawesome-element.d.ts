import type { CSSResultGroup, PropertyValues } from 'lit';
import { LitElement } from 'lit';
declare module 'lit' {
    interface PropertyDeclaration {
        /**
         * Specifies the property's default value
         */
        default?: any;
        initial?: any;
    }
}
export default class WebAwesomeElement extends LitElement {
    #private;
    /** One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. */
    static css?: CSSResultGroup;
    /** Prepends host styles to the component's styles. */
    static get styles(): CSSResultGroup;
    initialReflectedProperties: Map<string, unknown>;
    internals: ElementInternals;
    dir: string;
    lang: string;
    didSSR: boolean;
    constructor();
    connectedCallback(): void;
    attributeChangedCallback(name: string, oldValue: string | null, newValue: string | null): void;
    protected willUpdate(changedProperties: Parameters<LitElement['willUpdate']>[0]): void;
    protected firstUpdated(changedProperties: Parameters<LitElement['firstUpdated']>[0]): void;
    protected update(changedProperties: PropertyValues<this>): void;
    /**
     * @internal Methods for setting and checking custom states.
     */
    customStates: {
        /** Adds or removes the specified custom state. */
        set: (customState: string, active: boolean) => void;
        /** Determines whether or not the element currently has the specified state. */
        has: (customState: string) => boolean;
    };
    /**
     * @internal Given a native event, this function cancels it and dispatches it again from the host element using the desired
     * event options.
     */
    relayNativeEvent(event: Event, eventOptions?: EventInit): void;
}
