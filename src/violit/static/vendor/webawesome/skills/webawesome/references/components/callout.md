# Callout

**Full documentation:** https://webawesome.com/docs/components/callout


`<wa-callout>` Since 3.0 Stable

Callouts are used to display important messages inline.

```html
<wa-callout>
  <wa-icon slot="icon" name="circle-info" variant="regular"></wa-icon>
  This is a standard callout. You can customize its content and even the icon.
</wa-callout>
```

## Examples

### Variants

Set the `variant` attribute to change the callout's variant.

```html
<wa-callout variant="brand">
  <wa-icon slot="icon" name="circle-info" variant="regular"></wa-icon>
  <strong>This is super informative</strong><br />
  You can tell by how pretty the callout is.
</wa-callout>

<br />

<wa-callout variant="success">
  <wa-icon slot="icon" name="circle-check" variant="regular"></wa-icon>
  <strong>Your changes have been saved</strong><br />
  You can safely exit the app now.
</wa-callout>

<br />

<wa-callout variant="neutral">
  <wa-icon slot="icon" name="gear" variant="regular"></wa-icon>
  <strong>Your settings have been updated</strong><br />
  Settings will take effect on next login.
</wa-callout>

<br />

<wa-callout variant="warning">
  <wa-icon slot="icon" name="triangle-exclamation" variant="regular"></wa-icon>
  <strong>Your session has ended</strong><br />
  Please login again to continue.
</wa-callout>

<br />

<wa-callout variant="danger">
  <wa-icon slot="icon" name="circle-exclamation" variant="regular"></wa-icon>
  <strong>Your account has been deleted</strong><br />
  We're very sorry to see you go!
</wa-callout>
```

### Appearance

Use the `appearance` attribute to change the callout's visual appearance (the default is `filled-outlined`).

```html
<wa-callout variant="brand" appearance="accent">
  <wa-icon slot="icon" name="square-check"></wa-icon>
  This <strong>accent</strong> callout draws attention
</wa-callout>

<br />

<wa-callout variant="brand" appearance="filled-outlined">
  <wa-icon slot="icon" name="fill-drip" variant="regular"></wa-icon>
  This callout is both <strong>filled</strong> and <strong>outlined</strong>
</wa-callout>

<br />

<wa-callout variant="brand" appearance="filled">
  <wa-icon slot="icon" name="fill" variant="regular"></wa-icon>
  This callout is only <strong>filled</strong>
</wa-callout>

<br />

<wa-callout variant="brand" appearance="outlined">
  <wa-icon slot="icon" name="lines-leaning" variant="regular"></wa-icon>
  Here's an <strong>outlined</strong> callout
</wa-callout>

<br />

<wa-callout variant="brand" appearance="plain">
  <wa-icon slot="icon" name="font" variant="regular"></wa-icon>
  No bells and whistles on this <strong>plain</strong> callout
</wa-callout>
```

### Sizes

Use the `size` attribute to change a callout's size.

```html
<wa-callout size="large">
  <wa-icon slot="icon" name="circle-info" variant="regular"></wa-icon>
  This is meant to be very emphasized.
</wa-callout>

<br />

<wa-callout size="medium">
  <wa-icon slot="icon" name="circle-info" variant="regular"></wa-icon>
  Normal-sized callout.
</wa-callout>

<br />

<wa-callout size="small">
  <wa-icon slot="icon" name="circle-info" variant="regular"></wa-icon>
  Just a small tip!
</wa-callout>
```

### Without Icons

Icons are optional. Simply omit the `icon` slot if you don't want them.

```html
<wa-callout variant="brand"> Nothing fancy here, just a simple callout. </wa-callout>
```

### Styling

You can customize the callout's appearance mostly by setting regular CSS properties. `background`, `border`, `border-radius`, `color`, `padding`, `margin`, etc. work as expected.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/callout/callout.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaCallout from '@awesome.me/webawesome/dist/react/callout';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The callout's main content. |
| \`icon\` | \`

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'accent' \\| 'filled' \\| 'outlined' \\| 'plain' \\| 'filled-outlined'\` The callout's visual appearance. Type | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles, variantStyles, sizeStyles\] | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The callout's size. Type Default 'medium' | | |
| \`variant\` variant | \`brand\` The callout's theme variant. Defaults to if not within another element with a variant. Type 'brand' \\| 'neutral' \\| 'success' \\| 'warning' \\| 'danger' Default 'brand' | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`icon\` | The container that wraps the optional icon. | \`::part(icon)\` |
| \`message\` | The container that wraps the callout's main content. | \`::part(message)\` |

**Need a hand?** Report a bug Ask for help