# Tab Panel

**Full documentation:** https://webawesome.com/docs/components/tab-panel


`<wa-tab-panel>` Since 2.0 Stable

Tab panels are used inside [tab groups](https://webawesome.com/docs/components/tab-group) to display tabbed content.

This component must be used as a child of `<wa-tab-group>`. Please see the [Tab Group docs](https://webawesome.com/docs/components/tab-group) to see examples of this component in action.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/tab-panel/tab-panel.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaTabPanel from '@awesome.me/webawesome/dist/react/tab-panel';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The tab panel's content. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`active\` active | \`boolean\` When true, the tab panel will be shown. Type Default false | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`name\` name | \`string\` The tab panel's name. Type Default '' | | |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--padding\` | The tab panel's padding. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

**Need a hand?** Report a bug Ask for help