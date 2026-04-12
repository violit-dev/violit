# Progress Bar

**Full documentation:** https://webawesome.com/docs/components/progress-bar


`<wa-progress-bar>` Since 2.0 Stable

Progress bars are used to show the status of an ongoing operation.

```html
<wa-progress-bar value="40"></wa-progress-bar>
```

## Examples

### Labels

Use the `label` attribute to label the progress bar and tell assistive devices how to announce it.

```html
<wa-progress-bar value="50" label="Upload progress"></wa-progress-bar>
```

### Custom Height

Use the `--track-height` custom property to set the progress bar's height.

```html
<wa-progress-bar value="50" style="--track-height: 6px;"></wa-progress-bar>
```

### Showing Values

Use the default slot to show a value.

```html
<div class="wa-stack">
  <wa-progress-bar value="50" id="progress-bar-demo">50%</wa-progress-bar>

  <div>
    <wa-button pill appearance="filled">
      <wa-icon name="minus" label="Decrease"></wa-icon>
    </wa-button>
    <wa-button pill appearance="filled">
      <wa-icon name="plus" label="Increase"></wa-icon>
    </wa-button>
  </div>
</div>

<script>
  const progressBar = document.querySelector('#progress-bar-demo');
  const subtractButton = document.querySelector('wa-button:has(wa-icon[name="minus"])');
  const addButton = document.querySelector('wa-button:has(wa-icon[name="plus"])');

  addButton.addEventListener('click', () => {
    const value = Math.min(100, progressBar.value + 10);
    progressBar.value = value;
    progressBar.textContent = `${value}%`;
  });

  subtractButton.addEventListener('click', () => {
    const value = Math.max(0, progressBar.value - 10);
    progressBar.value = value;
    progressBar.textContent = `${value}%`;
  });
</script>
```

### Indeterminate

The `indeterminate` attribute can be used to inform the user that the operation is pending, but its status cannot currently be determined. In this state, `value` is ignored and the label, if present, will not be shown.

```html
<wa-progress-bar indeterminate></wa-progress-bar>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/progress-bar/progress-bar.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaProgressBar from '@awesome.me/webawesome/dist/react/progress-bar';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | A label to show inside the progress indicator. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`indeterminate\` indeterminate | \`boolean\` When true, percentage is ignored, the label is hidden, and the progress bar is drawn in an indeterminate state. Type Default false | | |
| \`label\` label | \`string\` A custom label for assistive devices. Type Default '' | | |
| \`value\` value | \`number\` The current progress as a percentage, 0 to 100. Type Default 0 | | |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--indicator-color\` | \`var(--wa-color-brand-fill-loud)\` The color of the indicator. Default |
| \`--track-color\` | \`var(--wa-color-neutral-fill-normal)\` The color of the track. Default |
| \`--track-height\` | \`1rem\` The color of the track. Default |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |
| \`indicator\` | The progress bar's indicator. | \`::part(indicator)\` |
| \`label\` | The progress bar's label. | \`::part(label)\` |

**Need a hand?** Report a bug Ask for help