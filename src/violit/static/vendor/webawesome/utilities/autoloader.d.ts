/** Starts the autoloader. */
export declare function startLoader(): void;
/** Stops the autoloader */
export declare function stopLoader(): void;
/**
 * Checks a node for undefined elements and attempts to register them.
 */
export declare function discover(root: Document | Element | ShadowRoot): Promise<void>;
/**
 * Acts as a middleware for Turbo's `turbo:before-render` event to ensure components are auto-loaded before showing the
 * next page, eliminating page-to-page FOUCE in a Turbo environment.
 */
export declare function preventTurboFouce(timeout?: number): void;
