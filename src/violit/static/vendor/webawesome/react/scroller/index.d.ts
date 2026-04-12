import Component from '../../components/scroller/scroller.js';
/**
 * @summary Scrollers create an accessible container while providing visual cues that help users identify and navigate
 *  through content that scrolls.
 * @documentation https://webawesome.com/docs/components/scroller
 * @status stable
 * @since 3.0
 *
 * @slot - The content to show inside the scroller.
 *
 * @cssproperty [--shadow-color=var(--wa-color-surface-default)] - The base color of the shadow.
 * @cssproperty [--shadow-size=2rem] - The size of the shadow.
 *
 * @csspart content - The container that wraps the slotted content.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {}>;
export default reactWrapper;
