# Progress Ring

**Full documentation:** https://webawesome.com/docs/components/progress-ring


`<wa-progress-ring>` Since 2.0 Stable

Progress rings are used to show the progress of a determinate operation in a circular fashion.

```html
<wa-progress-ring value="25"></wa-progress-ring>
```

## Examples

### Size

Use the `--size` custom property to set the diameter of the progress ring.

```html
<wa-progress-ring value="50" style="--size: 200px;"></wa-progress-ring>
```

### Track and Indicator Width

Use the `--track-width` and `--indicator-width` custom properties to set the width of the progress ring's track and indicator.

```html
<wa-progress-ring value="50" style="--track-width: 6px; --indicator-width: 12px;"></wa-progress-ring>
```

### Colors

To change the color, use the `--track-color` and `--indicator-color` custom properties.

```html
<wa-progress-ring
  value="50"
  style="
    --track-color: pink;
    --indicator-color: deeppink;
  "
>
</wa-progress-ring>
```

### Labels

Use the default slot to show a label inside the progress ring.

```html
<wa-progress-ring value="50" class="progress-ring-values" style="margin-bottom: .5rem;">50%</wa-progress-ring>

<br />

<wa-button appearance="filled" circle><wa-icon name="minus" variant="solid" label="Decrease"></wa-icon></wa-button>
<wa-button appearance="filled" circle><wa-icon name="plus" variant="solid" label="Increase"></wa-icon></wa-button>

<script>
  const progressRing = document.querySelector('.progress-ring-values');
  const subtractButton = progressRing.nextElementSibling.nextElementSibling;
  const addButton = subtractButton.nextElementSibling;

  addButton.addEventListener('click', () => {
    const value = Math.min(100, progressRing.value + 10);
    progressRing.value = value;
    progressRing.textContent = `${value}%`;
  });

  subtractButton.addEventListener('click', () => {
    const value = Math.max(0, progressRing.value - 10);
    progressRing.value = value;
    progressRing.textContent = `${value}%`;
  });
</script>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/progress-ring/progress-ring.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaProgressRing from '@awesome.me/webawesome/dist/react/progress-ring';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | A label to show inside the ring. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`label\` label | \`string\` A custom label for assistive devices. Type Default '' | | |
| \`value\` value | \`number\` The current progress as a percentage, 0 to 100. Type Default 0 | | |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--indicator-color\` | The color of the indicator. |
| \`--indicator-transition-duration\` | The duration of the indicator's transition when the value changes. |
| \`--indicator-width\` | The width of the indicator. Defaults to the track width. |
| \`--size\` | The diameter of the progress ring (cannot be a percentage). |
| \`--track-color\` | The color of the track. |
| \`--track-width\` | The width of the track. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |
| \`indicator\` | The progress ring's indicator. | \`::part(indicator)\` |
| \`label\` | The progress ring label. | \`::part(label)\` |
| \`track\` | The progress ring's track. | \`::part(track)\` |

**Need a hand?** Report a bug Ask for help