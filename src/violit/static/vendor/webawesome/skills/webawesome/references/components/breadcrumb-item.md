# Breadcrumb Item

**Full documentation:** https://webawesome.com/docs/components/breadcrumb-item


`<wa-breadcrumb-item>` Since 2.0 Stable

Breadcrumb Items are used inside breadcrumbs to represent different links.

This component must be used as a child of `<wa-breadcrumb>`. Please see the [Breadcrumb docs](https://webawesome.com/docs/components/breadcrumb) to see examples of this component in action.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/breadcrumb-item/breadcrumb-item.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaBreadcrumbItem from '@awesome.me/webawesome/dist/react/breadcrumb-item';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The breadcrumb item's label. |
| \`end\` | \`

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`href\` href | \`string \\| undefined\` Optional URL to direct the user to when the breadcrumb item is activated. When set, a link will be rendered internally. When unset, a button will be rendered instead. Type | | |
| \`rel\` rel | \`rel\` The attribute to use on the link. Only used when href is set. Type string Default 'noreferrer noopener' | | |
| \`target\` target | \`href\` Tells the browser where to open the link. Only used when is set. Type '\_blank' \\| '\_parent' \\| '\_self' \\| '\_top' \\| undefined | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`end\` | \`end\` The container that wraps the slot. | \`::part(end)\` |
| \`label\` | The breadcrumb item's label. | \`::part(label)\` |
| \`separator\` | The container that wraps the separator. | \`::part(separator)\` |
| \`start\` | \`start\` The container that wraps the slot. | \`::part(start)\` |

**Need a hand?** Report a bug Ask for help