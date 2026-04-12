# Button Group

**Full documentation:** https://webawesome.com/docs/components/button-group


`<wa-button-group>` Since 2.0 Stable

Button groups can be used to group related buttons into sections.

```html
<wa-button-group label="Alignment">
  <wa-button appearance="filled">Left</wa-button>
  <wa-button appearance="filled">Center</wa-button>
  <wa-button appearance="filled">Right</wa-button>
</wa-button-group>
```

## Examples

### Vertical Button Groups

Set the `orientation` attribute to `vertical` to make a vertical button group.

```html
<wa-button-group orientation="vertical" label="Options">
  <wa-button appearance="filled">Button</wa-button>
  <wa-dropdown>
    <wa-button appearance="filled" slot="trigger" with-caret>Dropdown</wa-button>
    <wa-dropdown-item>Item 1</wa-dropdown-item>
    <wa-dropdown-item>Item 2</wa-dropdown-item>
    <wa-dropdown-item>Item 3</wa-dropdown-item>
  </wa-dropdown>
  <wa-button appearance="filled">Button</wa-button>
</wa-button-group>
```

### Pill Buttons

Pill buttons are supported through the button's `pill` attribute.

```html
<wa-button-group label="Alignment">
  <wa-button appearance="filled" size="small" pill>Left</wa-button>
  <wa-button appearance="filled" size="small" pill>Center</wa-button>
  <wa-button appearance="filled" size="small" pill>Right</wa-button>
</wa-button-group>

<br /><br />

<wa-button-group label="Alignment">
  <wa-button appearance="filled" size="medium" pill>Left</wa-button>
  <wa-button appearance="filled" size="medium" pill>Center</wa-button>
  <wa-button appearance="filled" size="medium" pill>Right</wa-button>
</wa-button-group>

<br /><br />

<wa-button-group label="Alignment">
  <wa-button appearance="filled" size="large" pill>Left</wa-button>
  <wa-button appearance="filled" size="large" pill>Center</wa-button>
  <wa-button appearance="filled" size="large" pill>Right</wa-button>
</wa-button-group>
```

### Dropdowns in Button Groups

Dropdowns can be placed into button groups.

```html
<wa-button-group label="Example Button Group">
  <wa-button appearance="filled">Button</wa-button>
  <wa-dropdown>
    <wa-button appearance="filled" slot="trigger" with-caret>Dropdown</wa-button>
    <wa-dropdown-item>Item 1</wa-dropdown-item>
    <wa-dropdown-item>Item 2</wa-dropdown-item>
    <wa-dropdown-item>Item 3</wa-dropdown-item>
  </wa-dropdown>
  <wa-button appearance="filled">Button</wa-button>
</wa-button-group>
```

### Split Buttons

Create a split button using a button and a dropdown. Use a [visually hidden](https://webawesome.com/docs/utilities/visually-hidden) label to ensure the dropdown is accessible to users with assistive devices.

```html
<wa-button-group label="Example Button Group">
  <wa-button appearance="filled" variant="brand">Save</wa-button>
  <wa-dropdown placement="bottom-end">
    <wa-button appearance="filled" slot="trigger" variant="brand">
      <wa-icon name="chevron-down" label="More options"></wa-icon>
    </wa-button>
    <wa-dropdown-item>Save</wa-dropdown-item>
    <wa-dropdown-item>Save as&hellip;</wa-dropdown-item>
    <wa-dropdown-item>Save all</wa-dropdown-item>
  </wa-dropdown>
</wa-button-group>
```

### Tooltips in Button Groups

Buttons can be wrapped in tooltips to provide more detail when the user interacts with them.

```html
<wa-button-group label="Alignment">
  <wa-button appearance="filled" id="button-left">Left</wa-button>
  <wa-button appearance="filled" id="button-center">Center</wa-button>
  <wa-button appearance="filled" id="button-right">Right</wa-button>
</wa-button-group>

<wa-tooltip for="button-left">I'm on the left</wa-tooltip>
<wa-tooltip for="button-center">I'm in the middle</wa-tooltip>
<wa-tooltip for="button-right">I'm on the right</wa-tooltip>
```

### Toolbar Example

Create interactive toolbars with button groups.

```html
<div class="button-group-toolbar">
  <wa-button-group label="History">
    <wa-button appearance="filled" id="undo-button"><wa-icon name="undo" variant="solid" label="Undo"></wa-icon></wa-button>
    <wa-button appearance="filled" id="redo-button"><wa-icon name="redo" variant="solid" label="Redo"></wa-icon></wa-button>
  </wa-button-group>

  <wa-button-group label="Formatting">
    <wa-button appearance="filled" id="button-bold"><wa-icon name="bold" variant="solid" label="Bold"></wa-icon></wa-button>
    <wa-button appearance="filled" id="button-italic"><wa-icon name="italic" variant="solid" label="Italic"></wa-icon></wa-button>
    <wa-button appearance="filled" id="button-underline"><wa-icon name="underline" variant="solid" label="Underline"></wa-icon></wa-button>
  </wa-button-group>

  <wa-button-group label="Alignment">
    <wa-button appearance="filled" id="button-align-left">
      <wa-icon name="align-left" variant="solid" label="Align Left"></wa-icon>
    </wa-button>
    <wa-button appearance="filled" id="button-align-center">
      <wa-icon name="align-center" variant="solid" label="Align Center"></wa-icon>
    </wa-button>
    <wa-button appearance="filled" id="button-align-right">
      <wa-icon name="align-right" variant="solid" label="Align Right"></wa-icon>
    </wa-button>
  </wa-button-group>
</div>

<wa-tooltip for="undo-button">Undo</wa-tooltip>
<wa-tooltip for="redo-button">Redo</wa-tooltip>
<wa-tooltip for="button-bold">Bold</wa-tooltip>
<wa-tooltip for="button-italic">Italic</wa-tooltip>
<wa-tooltip for="button-underline">Underline</wa-tooltip>

<wa-tooltip for="button-align-left">Align Left</wa-tooltip>
<wa-tooltip for="button-align-center">Align Center</wa-tooltip>
<wa-tooltip for="button-align-right">Align Right</wa-tooltip>

<style>
  .button-group-toolbar wa-button-group:not(:last-of-type) {
    margin-right: var(--wa-space-xs);
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
import '@awesome.me/webawesome/dist/components/button-group/button-group.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaButtonGroup from '@awesome.me/webawesome/dist/react/button-group';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | \`\` One or more elements to display in the button group. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles\] | | |
| \`label\` label | \`string\` A label to use for the button group. This won't be displayed on the screen, but it will be announced by assistive devices when interacting with the control and is strongly recommended. Type Default '' | | |
| \`orientation\` orientation | \`'horizontal' \\| 'vertical'\` The button group's orientation. Type Default 'horizontal' | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

**Need a hand?** Report a bug Ask for help