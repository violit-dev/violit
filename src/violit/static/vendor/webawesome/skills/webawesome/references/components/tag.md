# Tag

**Full documentation:** https://webawesome.com/docs/components/tag


`<wa-tag>` Since 2.0 Stable

Tags are used as labels to organize things or to indicate a selection.

```html
<wa-tag variant="brand">Brand</wa-tag>
<wa-tag variant="success">Success</wa-tag>
<wa-tag variant="neutral">Neutral</wa-tag>
<wa-tag variant="warning">Warning</wa-tag>
<wa-tag variant="danger">Danger</wa-tag>
```

## Examples

### Appearance

Use the `size` attribute to change a tag's visual appearance. The default appearance is `filled-outlined`.

```html
<div class="wa-stack">
  <p>
    <wa-tag variant="brand" appearance="accent">Accent</wa-tag>
    <wa-tag variant="brand" appearance="filled-outlined">Filled-Outlined</wa-tag>
    <wa-tag variant="brand" appearance="filled">Filled</wa-tag>
    <wa-tag variant="brand" appearance="outlined">Outlined</wa-tag>
  </p>
  <p>
    <wa-tag variant="success" appearance="accent">Accent</wa-tag>
    <wa-tag variant="success" appearance="filled-outlined">Filled-Outlined</wa-tag>
    <wa-tag variant="success" appearance="filled">Filled</wa-tag>
    <wa-tag variant="success" appearance="outlined">Outlined</wa-tag>
  </p>

  <p>
    <wa-tag variant="neutral" appearance="accent">Accent</wa-tag>
    <wa-tag variant="neutral" appearance="filled-outlined">Filled-Outlined</wa-tag>
    <wa-tag variant="neutral" appearance="filled">Filled</wa-tag>
    <wa-tag variant="neutral" appearance="outlined">Outlined</wa-tag>
  </p>

  <p>
    <wa-tag variant="warning" appearance="accent">Accent</wa-tag>
    <wa-tag variant="warning" appearance="filled-outlined">Filled-Outlined</wa-tag>
    <wa-tag variant="warning" appearance="filled">Filled</wa-tag>
    <wa-tag variant="warning" appearance="outlined">Outlined</wa-tag>
  </p>

  <p>
    <wa-tag variant="danger" appearance="accent">Accent</wa-tag>
    <wa-tag variant="danger" appearance="filled-outlined">Filled-Outlined</wa-tag>
    <wa-tag variant="danger" appearance="filled">Filled</wa-tag>
    <wa-tag variant="danger" appearance="outlined">Outlined</wa-tag>
  </p>
</div>
```

### Sizes

Use the `size` attribute to change a tag's size.

```html
<wa-tag size="small">Small</wa-tag>
<wa-tag size="medium">Medium</wa-tag>
<wa-tag size="large">Large</wa-tag>
```

### Pill

Use the `pill` attribute to give tabs rounded edges.

```html
<wa-tag size="small" pill>Small</wa-tag>
<wa-tag size="medium" pill>Medium</wa-tag>
<wa-tag size="large" pill>Large</wa-tag>
```

### Removable

Use the `with-remove` attribute to add a remove button to the tag.

```html
<div class="tags-removable">
  <wa-tag size="small" with-remove>Small</wa-tag>
  <wa-tag size="medium" with-remove>Medium</wa-tag>
  <wa-tag size="large" with-remove>Large</wa-tag>
</div>

<script>
  const div = document.querySelector('.tags-removable');

  div.addEventListener('wa-remove', event => {
    const tag = event.target;
    tag.style.opacity = '0';
    setTimeout(() => (tag.style.opacity = '1'), 2000);
  });
</script>

<style>
  .tags-removable wa-tag {
    transition: opacity var(--wa-transition-normal);
  }
</style>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/tag/tag.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaTag from '@awesome.me/webawesome/dist/react/tag';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The tag's content. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'accent' \\| 'filled' \\| 'outlined' \\| 'filled-outlined'\` The tag's visual appearance. Type Default 'filled-outlined' | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles, variantStyles, sizeStyles\] | | |
| \`pill\` pill | \`boolean\` Draws a pill-style tag with rounded edges. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The tag's size. Type Default 'medium' | | |
| \`variant\` variant | \`neutral\` The tag's theme variant. Defaults to if not within another element with a variant. Type 'brand' \\| 'neutral' \\| 'success' \\| 'warning' \\| 'danger' Default 'neutral' | | |
| \`withRemove\` with-remove | \`boolean\` Makes the tag removable and shows a remove button. Type Default false | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-remove\` | Emitted when the remove button is activated. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |
| \`content\` | The tag's content. | \`::part(content)\` |
| \`remove-button\` | \`\` The tag's remove button, a . | \`::part(remove-button)\` |
| \`remove-button\_\_base\` | \`base\` The remove button's exported part. | \`::part(remove-button\_\_base)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)

**Need a hand?** Report a bug Ask for help