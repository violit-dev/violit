# Tab

**Full documentation:** https://webawesome.com/docs/components/tab


`<wa-tab>` Since 2.0 Stable

Tabs are used inside [tab groups](https://webawesome.com/docs/components/tab-group) to represent and activate [tab panels](https://webawesome.com/docs/components/tab-panel).

This component must be used as a child of `<wa-tab-group>`. Please see the [Tab Group docs](https://webawesome.com/docs/components/tab-group) to see examples of this component in action.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/tab/tab.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaTab from '@awesome.me/webawesome/dist/react/tab';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The tab's label. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`disabled\` disabled | \`boolean\` Disables the tab and prevents selection. Type Default false | | |
| \`panel\` panel | \`string\` The name of the tab panel this tab is associated with. The panel must be located in the same tab group. Type Default '' | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

**Need a hand?** Report a bug Ask for help