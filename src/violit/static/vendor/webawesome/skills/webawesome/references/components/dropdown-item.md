# Dropdown Item

**Full documentation:** https://webawesome.com/docs/components/dropdown-item


`<wa-dropdown-item>` Since 3.0 Experimental

Represents an individual item within a dropdown menu, supporting standard items, checkboxes, and submenus.

This component must be used as a child of `<wa-dropdown>`. Please see the [Dropdown docs](https://webawesome.com/docs/components/dropdown) to see examples of this component in action.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/dropdown-item/dropdown-item.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaDropdownItem from '@awesome.me/webawesome/dist/react/dropdown-item';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The dropdown item's label. |
| \`details\` | Additional content or details to display after the label. |
| \`icon\` | An optional icon to display before the label. |
| \`submenu\` | \`\` Submenu items, typically elements, to create a nested menu. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`checked\` checked | \`type\` Set to true to check the dropdown item. Only valid when is checkbox. Type boolean Default false | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`disabled\` disabled | \`boolean\` Disables the dropdown item. Type Default false | | |
| \`submenuOpen\` submenuOpen | \`boolean\` Whether the submenu is currently open. Type Default false | | |
| \`type\` type | \`checkbox\` Set to to make the item a checkbox. Type 'normal' \\| 'checkbox' Default 'normal' | | |
| \`value\` value | \`wa-select\` An optional value for the menu item. This is useful for determining which item was selected when listening to the dropdown's event. Type string | | |
| \`variant\` variant | \`'danger' \\| 'default'\` The type of menu item to render. Type Default 'default' | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`closeSubmenu()\` | Closes the submenu. | |
| \`openSubmenu()\` | Opens the submenu. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the dropdown item loses focus. |
| \`focus\` | Emitted when the dropdown item gains focus. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`checkmark\` | \`\` The submenu indicator icon (a element). | \`::part(submenu-icon)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help