import { Marked } from 'marked';
import WebAwesomeElement from '../../internal/webawesome-element.js';
/**
 * @summary Renders markdown content in plain ol' HTML.
 * @documentation https://webawesome.com/docs/components/markdown
 * @status experimental
 * @since 3.4
 */
export default class WaMarkdown extends WebAwesomeElement {
    static css: import("lit").CSSResult;
    /** Returns the shared Marked instance used by all `<wa-markdown>` components. */
    static getMarked(): Marked;
    /** Re-renders all connected `<wa-markdown>` instances. Call this after changing the Marked configuration. */
    static updateAll(): void;
    private renderGeneration;
    private suppressSlotChange;
    /** The tab stop width used when converting leading tabs to spaces during whitespace normalization. */
    tabSize: number;
    /** A reference to the shared Marked instance for convenience. Equivalent to `WaMarkdown.getMarked()`. */
    get marked(): Marked;
    connectedCallback(): void;
    disconnectedCallback(): void;
    /**
     * Normalizes whitespace in the given text by converting leading tabs to spaces, trimming leading/trailing blank
     * lines, and removing the common indentation prefix from all lines.
     */
    private dedent;
    /** Finds the `<script type="text/markdown">` source element inside this component. */
    private getSourceScript;
    /** Reads the script content, normalizes whitespace, parses markdown, and injects the result. */
    renderMarkdown(): void;
    private handleSlotChange;
    render(): import("lit-html").TemplateResult<1>;
}
declare global {
    interface HTMLElementTagNameMap {
        'wa-markdown': WaMarkdown;
    }
}
