# Split Panel

**Full documentation:** https://webawesome.com/docs/components/split-panel


`<wa-split-panel>` Since 2.0 Stable

Split panels display two adjacent panels, allowing the user to reposition them.

```html
<wa-split-panel>
  <div
    slot="start"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    Start
  </div>
  <div
    slot="end"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    End
  </div>
</wa-split-panel>
```

## Examples

### Initial Position

To set the initial position, use the `position` attribute. If no position is provided, it will default to 50% of the available space.

```html
<wa-split-panel position="75">
  <div
    slot="start"
    style="
      height: 200px;
      background: var(--wa-color-surface-lowered);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    "
  >
    Start
  </div>
  <div
    slot="end"
    style="
      height: 200px;
      background: var(--wa-color-surface-lowered);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    "
  >
    End
  </div>
</wa-split-panel>
```

### Initial Position in Pixels

To set the initial position in pixels instead of a percentage, use the `position-in-pixels` attribute.

```html
<wa-split-panel position-in-pixels="150">
  <div
    slot="start"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    Start
  </div>
  <div
    slot="end"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    End
  </div>
</wa-split-panel>
```

### Orientation

Set the `orientation` attribute to `vertical` and provide a height to render the split panel in a vertical orientation where the start and end panels are stacked.

```html
<wa-split-panel orientation="vertical" style="height: 400px;">
  <div
    slot="start"
    style="height: 100%; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    Start
  </div>
  <div
    slot="end"
    style="height: 100%; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    End
  </div>
</wa-split-panel>
```

### Snapping

To snap panels at specific positions while dragging, add the `snap` attribute with one or more space-separated values. Values must be in pixels or percentages. For example, to snap the panel at `100px` and `50%`, use `snap="100px 50%"`. You can also customize how close the divider must be before snapping with the `snap-threshold` attribute.

```html
<div class="split-panel-snapping">
  <wa-split-panel snap="100px 50%">
    <div
      slot="start"
      style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
    >
      Start
    </div>
    <div
      slot="end"
      style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
    >
      End
    </div>
  </wa-split-panel>

  <div class="split-panel-snapping-dots"></div>
</div>

<style>
  .split-panel-snapping {
    position: relative;
  }

  .split-panel-snapping-dots::before,
  .split-panel-snapping-dots::after {
    content: '';
    position: absolute;
    bottom: -12px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--wa-color-neutral-fill-loud);
    transform: translateX(-3px);
  }

  .split-panel-snapping-dots::before {
    left: 100px;
  }

  .split-panel-snapping-dots::after {
    left: 50%;
  }
</style>
```

### Disabled

Add the `disabled` attribute to prevent the divider from being repositioned.

```html
<wa-split-panel disabled>
  <div
    slot="start"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    Start
  </div>
  <div
    slot="end"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    End
  </div>
</wa-split-panel>
```

### Setting the Primary Panel

By default, both panels will grow or shrink proportionally when the host element is resized. If a primary panel is designated, it will maintain its size and the secondary panel will grow or shrink to fit the remaining space. You can set the primary panel to `start` or `end` using the `primary` attribute.

Try resizing the example below with each option and notice how the panels respond.

```html
<div class="split-panel-primary">
  <wa-split-panel>
    <div
      slot="start"
      style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
    >
      Start
    </div>
    <div
      slot="end"
      style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
    >
      End
    </div>
  </wa-split-panel>

  <wa-select label="Primary Panel" style="max-width: 200px; margin-top: 1rem;">
    <wa-option value="" selected>None</wa-option>
    <wa-option value="start">Start</wa-option>
    <wa-option value="end">End</wa-option>
  </wa-select>
</div>

<script>
  const container = document.querySelector('.split-panel-primary');
  const splitPanel = container.querySelector('wa-split-panel');
  const select = container.querySelector('wa-select');

  select.addEventListener('change', () => (splitPanel.primary = select.value));
</script>
```

### Min & Max

To set a minimum or maximum size of the primary panel, use the `--min` and `--max` custom properties. Since the secondary panel is flexible, size constraints can only be applied to the primary panel. If no primary panel is designated, these constraints will be applied to the `start` panel.

This examples demonstrates how you can ensure both panels are at least 150px using `--min`, `--max`, and the `calc()` function.

```html
<wa-split-panel style="--min: 150px; --max: calc(100% - 150px);">
  <div
    slot="start"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    Start
  </div>
  <div
    slot="end"
    style="height: 200px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden;"
  >
    End
  </div>
</wa-split-panel>
```

### Nested Split Panels

Create complex layouts that can be repositioned independently by nesting split panels.

```html
<wa-split-panel>
  <div
    slot="start"
    style="height: 400px; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden"
  >
    Start
  </div>
  <div slot="end">
    <wa-split-panel orientation="vertical" style="height: 400px;">
      <div
        slot="start"
        style="height: 100%; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden"
      >
        Top
      </div>
      <div
        slot="end"
        style="height: 100%; background: var(--wa-color-surface-lowered); display: flex; align-items: center; justify-content: center; overflow: hidden"
      >
        Bottom
      </div>
    </wa-split-panel>
  </div>
</wa-split-panel>
```

### Customizing the Divider

You can target the `divider` part to apply CSS properties to the divider. To add a custom handle, slot an icon into the `divider` slot. When customizing the divider, make sure to think about focus styles for keyboard users.

```html
<wa-split-panel style="--divider-width: 20px;">
  <wa-icon slot="divider" name="grip-vertical" variant="solid"></wa-icon>
  <div
    slot="start"
    style="
      height: 200px;
      background: var(--wa-color-surface-lowered);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    "
  >
    Start
  </div>
  <div
    slot="end"
    style="
      height: 200px;
      background: var(--wa-color-surface-lowered);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    "
  >
    End
  </div>
</wa-split-panel>
```

Here's a more elaborate example that changes the divider's color and width and adds a styled handle.

```html
<div class="split-panel-divider">
  <wa-split-panel>
    <wa-icon slot="divider" name="grip-vertical" variant="solid"></wa-icon>
    <div
      slot="start"
      style="
        height: 200px;
        background: var(--wa-color-surface-lowered);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      "
    >
      Start
    </div>
    <div
      slot="end"
      style="
        height: 200px;
        background: var(--wa-color-surface-lowered);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      "
    >
      End
    </div>
  </wa-split-panel>
</div>

<style>
  .split-panel-divider wa-split-panel {
    --divider-width: 4px;
  }

  .split-panel-divider wa-split-panel::part(divider) {
    background-color: var(--wa-color-red-50);
  }

  .split-panel-divider wa-icon {
    position: absolute;
    border-radius: var(--wa-border-radius-l);
    background: var(--wa-color-red-50);
    color: white;
    padding: 0.5rem 0.25rem;
  }

  .split-panel-divider wa-split-panel::part(divider):focus-visible {
    background-color: var(--wa-color-blue-50);
  }

  .split-panel-divider wa-split-panel:focus-within wa-icon {
    background-color: var(--wa-color-blue-50);
    color: white;
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
import '@awesome.me/webawesome/dist/components/split-panel/split-panel.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaSplitPanel from '@awesome.me/webawesome/dist/react/split-panel';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`divider\` | The divider. Useful for slotting in a custom icon that renders as a handle. |
| \`end\` | Content to place in the end panel. |
| \`start\` | Content to place in the start panel. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`disabled\` disabled | \`boolean\` Disables resizing. Note that the position may still change as a result of resizing the host element. Type Default false | | |
| \`orientation\` orientation | \`'horizontal' \\| 'vertical'\` Sets the split panel's orientation. Type Default 'horizontal' | | |
| \`position\` position | \`number\` The current position of the divider from the primary panel's edge as a percentage 0-100. Defaults to 50% of the container's initial size. Type Default 50 | | |
| \`positionInPixels\` position-in-pixels | \`number\` The current position of the divider from the primary panel's edge in pixels. Type | | |
| \`primary\` primary | \`'start' \\| 'end' \\| undefined\` If no primary panel is designated, both panels will resize proportionally when the host element is resized. If a primary panel is designated, it will maintain its size and the other panel will grow or shrink as needed when the host element is resized. Type | | |
| \`snap\` snap | \`"100px 50%"\` One or more space-separated values at which the divider should snap. Values can be in pixels or percentages, e.g. . Type string \\| undefined | | |
| \`snapThreshold\` snap-threshold | \`number\` How close the divider must be to a snap point until snapping occurs. Type Default 12 | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-reposition\` | Emitted when the divider's position changes. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--divider-hit-area\` | \`12px\` The invisible region around the divider where dragging can occur. This is usually wider than the divider to facilitate easier dragging. Default |
| \`--divider-width\` | \`4px\` The width of the visible divider. Default |
| \`--max\` | \`100%\` The maximum allowed size of the primary panel. Default |
| \`--min\` | \`0\` The minimum allowed size of the primary panel. Default |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`divider\` | The divider that separates the start and end panels. | \`::part(divider)\` |
| \`end\` | The end panel. | \`::part(end)\` |
| \`panel\` | Targets both the start and end panels. | \`::part(panel)\` |
| \`start\` | The start panel. | \`::part(start)\` |

**Need a hand?** Report a bug Ask for help