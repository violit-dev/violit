# Option

**Full documentation:** https://webawesome.com/docs/components/option


`<wa-option>` Since 2.0 Stable

Options define the selectable items within a select component.

This component must be used as a child of `<wa-select>`. Please see the [Select docs](https://webawesome.com/docs/components/select) to see examples of this component in action.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/option/option.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaOption from '@awesome.me/webawesome/dist/react/option';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The option's label. |
| \`end\` | \`\` An element, such as , placed before the label. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`defaultLabel\` | \`label\` The default , generated from the element contents. Will be equal to label in most cases. Type string | | |
| \`defaultSelected\` selected | \`boolean\` Selects an option initially. Type Default false | | |
| \`disabled\` disabled | \`boolean\` Draws the option in a disabled state, preventing selection. Type Default false | | |
| \`label\` label | \`string\` The option’s plain text label. Usually automatically generated, but can be useful to provide manually for cases involving complex content. Type | | |
| \`value\` value | \`string\` The option's value. When selected, the containing form control will receive this value. The value must be unique from other options in the same group. Values may not contain spaces, as spaces are used as delimiters when listing multiple values. Type Default '' | | |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`current\` | The user has keyed into the option, but hasn't selected it yet (shows a highlight) | \`:state(current)\` |
| \`disabled\` | Applied when the option is disabled | \`:state(disabled)\` |
| \`hover\` | \`:hover\` Like but works while dragging in Safari | \`:state(hover)\` |
| \`selected\` | The option is selected and has aria-selected="true" | \`:state(selected)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`checked-icon\` | \`

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help