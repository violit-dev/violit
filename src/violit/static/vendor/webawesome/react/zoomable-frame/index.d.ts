import Component from '../../components/zoomable-frame/zoomable-frame.js';
/**
 * @summary Zoomable frames render iframe content with zoom and interaction controls.
 * @documentation https://webawesome.com/docs/components/zoomable-frame
 * @status stable
 * @since 3.0
 *
 * @dependency wa-icon
 *
 * @slot zoom-in-icon - The slot that contains the zoom in icon.
 * @slot zoom-out-icon - The slot that contains the zoom out icon.
 *
 * @event load - Emitted when the internal iframe when it finishes loading.
 * @event error - Emitted from the internal iframe when it fails to load.
 *
 * @csspart iframe - The internal `<iframe>` element.
 * @csspart controls - The container that surrounds zoom control buttons.
 * @csspart zoom-in-button - The zoom in button.
 * @csspart zoom-out-button - The zoom out button.
 */
declare const reactWrapper: import("@lit/react").ReactWebComponent<Component, {}>;
export default reactWrapper;
