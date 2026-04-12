import type WaIcon from '../icon/icon.js';
export type IconLibraryHostElement = WaIcon;
export type IconLibraryResolver = (name: string, family: string, variant: string, autoWidth: boolean) => string | Promise<string>;
export type IconLibraryMutator = (svg: SVGElement, hostElement?: IconLibraryHostElement) => void;
export interface IconLibrary {
    name: string;
    resolver: IconLibraryResolver;
    mutator?: IconLibraryMutator;
    spriteSheet?: boolean;
}
/** Adds an icon to the list of watched icons. */
export declare function watchIcon(icon: WaIcon): void;
/** Removes an icon from the list of watched icons. */
export declare function unwatchIcon(icon: WaIcon): void;
/** Returns a library from the registry. */
export declare function getIconLibrary(name?: string): IconLibrary | undefined;
/** Adds an icon library to the registry, or overrides an existing one. */
export declare function registerIconLibrary(name: string, options: Omit<IconLibrary, 'name'>): void;
/** Removes an icon library from the registry. */
export declare function unregisterIconLibrary(name: string): void;
/** Sets the default icon family. */
export declare function setDefaultIconFamily(family: string): void;
/** Gets the default icon family. */
export declare function getDefaultIconFamily(): string;
