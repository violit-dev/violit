/**
 * Like textContent, but better:
 * - Uses assignedNodes to get text content from slots (and falls back to content if nothing is slotted)
 * - Ignores script and style elements
 * @param root - One or more nodes to get text content from.
 * @param depth - By default, will just return element.textContent for any child elements instead of calling the function recursively.
 *                Set to a positive integer to recurse that many levels. Generally a tradeoff between performance and accuracy.
 * @returns
 */
export default function getText(root: Node | Iterable<Node>, depth?: number): string;
