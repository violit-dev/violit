/**
 * Registers a dismissible as open. Call this when the dismissible becomes visible.
 * The most recently registered dismissible is at the top.
 */
export declare function registerDismissible(key: object): void;
/**
 * Unregisters a dismissible. Call this when the dismissible closes or is removed from the DOM.
 */
export declare function unregisterDismissible(key: object): void;
/**
 * Returns true if the given key is the topmost registered dismissible.
 * Use this to guard Escape key handling so only the topmost dismissible responds.
 */
export declare function isTopDismissible(key: object): boolean;
