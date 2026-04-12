# Spinner

**Full documentation:** https://webawesome.com/docs/components/spinner


`<wa-spinner>` Since 2.0 Stable

Spinners are used to show the progress of an indeterminate operation.

```html
<wa-spinner></wa-spinner>
```

## Examples

### Size

Spinners are sized based on the current font size. To change their size, set the `font-size` property on the spinner itself or on a parent element as shown below.

```html
<wa-spinner></wa-spinner>
<wa-spinner style="font-size: 2rem;"></wa-spinner>
<wa-spinner style="font-size: 3rem;"></wa-spinner>
```

### Track Width

The width of the spinner's track can be changed by setting the `--track-width` custom property.

```html
<wa-spinner style="font-size: 50px; --track-width: 10px;"></wa-spinner>
```

### Color

The spinner's colors can be changed by setting the `--indicator-color` and `--track-color` custom properties.

```html
<wa-spinner style="font-size: 3rem; --indicator-color: deeppink; --track-color: pink;"></wa-spinner>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/spinner/spinner.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaSpinner from '@awesome.me/webawesome/dist/react/spinner';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--indicator-color\` | The color of the spinner's indicator. |
| \`--speed\` | The time it takes for the spinner to complete one animation cycle. |
| \`--track-color\` | The color of the track. |
| \`--track-width\` | The width of the track. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

**Need a hand?** Report a bug Ask for help