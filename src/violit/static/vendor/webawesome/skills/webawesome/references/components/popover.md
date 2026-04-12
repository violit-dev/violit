# Popover

**Full documentation:** https://webawesome.com/docs/components/popover


`<wa-popover>` Since 3.0 Stable

Popovers display contextual content and interactive elements in a floating panel.

Popovers display interactive content when their anchor element is clicked. Unlike [tooltips](https://webawesome.com/docs/components/tooltip), popovers can contain links, buttons, and form controls. They appear without an overlay and will close when you click outside or press Escape. Only one popover can be open at a time.

```html
<wa-popover for="popover__overview">
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <p>This popover contains interactive content that users can engage with directly.</p>
    <wa-button appearance="filled" variant="primary" size="small">Take Action</wa-button>
  </div>
</wa-popover>

<wa-button appearance="filled" id="popover__overview">Show popover</wa-button>
```

## Examples

### Assigning an Anchor

Use `<wa-button>` or `<button>` elements as popover anchors. Connect the popover to its anchor by setting the `for` attribute to match the anchor's `id`.

```html
<wa-button appearance="filled" id="popover__anchor-button">Show Popover</wa-button>

<wa-popover for="popover__anchor-button"> I'm anchored to a Web Awesome button. </wa-popover>

<br /><br />

<button class="wa-filled" id="popover__anchor-native-button">Show Popover</button>

<wa-popover for="popover__anchor-native-button"> I'm anchored to a native button. </wa-popover>
```

Make sure the anchor element exists in the DOM before the popover connects. If it doesn't exist, the popover won't attach and you'll see a console warning.

### Opening and Closing

Popovers show when you click their anchor element. You can also control them programmatically by setting the `open` property to `true` or `false`.

Use `data-popover="close"` on any button inside a popover to close it automatically.

```html
<wa-popover for="popover__opening">
  <p>The button below has <code>data-popover="close"</code> so clicking it will close the popover.</p>
  <wa-button appearance="filled" data-popover="close" variant="primary">Dismiss</wa-button>
</wa-popover>

<wa-button appearance="filled" id="popover__opening">Show popover</wa-button>
```

### Placement

Use the `placement` attribute to set where the popover appears relative to its anchor. The popover will automatically reposition if there isn't enough space in the preferred location. The default placement is `top`.

```html
<div style="display: flex; gap: 1rem; align-items: center;">
  <wa-button appearance="filled" id="popover__top">Top</wa-button>
  <wa-popover for="popover__top" placement="top">I'm on the top</wa-popover>

  <wa-button appearance="filled" id="popover__bottom">Bottom</wa-button>
  <wa-popover for="popover__bottom" placement="bottom">I'm on the bottom</wa-popover>

  <wa-button appearance="filled" id="popover__left">Left</wa-button>
  <wa-popover for="popover__left" placement="left">I'm on the left</wa-popover>

  <wa-button appearance="filled" id="popover__right">Right</wa-button>
  <wa-popover for="popover__right" placement="right">I'm on the right</wa-popover>
</div>
```

### Distance

Use the `distance` attribute to control how far the popover appears from its anchor.

```html
<div style="display: flex; gap: 1rem; align-items: center;">
  <wa-button appearance="filled" id="popover__distance-near">Near</wa-button>
  <wa-popover for="popover__distance-near" distance="0">I'm very close</wa-popover>

  <wa-button appearance="filled" id="popover__distance-far">Far</wa-button>
  <wa-popover for="popover__distance-far" distance="30">I'm farther away</wa-popover>
</div>
```

### Arrow Size

Use the `--arrow-size` custom property to change the size of the popover's arrow. To remove it, use the `without-arrow` attribute.

```html
<div style="display: flex; gap: 1rem; align-items: center;">
  <wa-button appearance="filled" id="popover__big-arrow">Big arrow</wa-button>
  <wa-popover for="popover__big-arrow" style="--arrow-size: 8px;">I have a big arrow</wa-popover>

  <wa-button appearance="filled" id="popover__no-arrow">No arrow</wa-button>
  <wa-popover for="popover__no-arrow" without-arrow>I don't have an arrow</wa-popover>
</div>
```

### Setting a Maximum Width

Use the `--max-width` custom property to control the maximum width of the popover.

```html
<wa-button appearance="filled" id="popover__max-width">Toggle me</wa-button>
<wa-popover for="popover__max-width" style="--max-width: 160px;">
  Popovers will usually grow to be much wider, but this one has a custom max width that forces text to wrap.
</wa-popover>
```

### Setting Focus

Use the [`autofocus`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autofocus) global attribute to move focus to a specific form control when the popover opens.

```html
<wa-popover for="popover__autofocus">
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <wa-textarea autofocus placeholder="What's on your mind?" size="small" resize="none" rows="3"></wa-textarea>
    <wa-button appearance="filled" variant="primary" size="small" data-popover="close"> Submit </wa-button>
  </div>
</wa-popover>

<wa-button appearance="filled" id="popover__autofocus">
  <wa-icon name="comment" slot="start"></wa-icon>
  Feedback
</wa-button>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/popover/popover.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaPopover from '@awesome.me/webawesome/dist/react/popover';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The popover's content. Interactive elements such as buttons and links are supported. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`distance\` distance | \`number\` The distance in pixels from which to offset the popover away from its target. Type Default 8 | | |
| \`for\` for | \`string \\| null\` The ID of the popover's anchor element. This must be an interactive/focusable element such as a button. Type Default null | | |
| \`open\` open | \`boolean\` Shows or hides the popover. Type Default false | | |
| \`placement\` placement | \`'top' \\| 'top-start' \\| 'top-end' \\| 'right' \\| 'right-start' \\| 'right-end' \\| 'bottom' \\| 'bottom-start' \\| 'bottom-end' \\| 'left' \\| 'left-start' \\| 'left-end'\` The preferred placement of the popover. Note that the actual placement may vary as needed to keep the popover inside of the viewport. Type Default 'top' | | |
| \`skidding\` skidding | \`number\` The distance in pixels from which to offset the popover along its target. Type Default 0 | | |
| \`withoutArrow\` without-arrow | \`boolean\` Removes the arrow from the popover. Type Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`hide()\` | Hides the popover. | |
| \`show()\` | Shows the popover. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-after-hide\` | Emitted after the popover has hidden and all animations are complete. |
| \`wa-after-show\` | Emitted after the popover has shown and all animations are complete. |
| \`wa-hide\` | Emitted when the popover begins to hide. Canceling this event will stop the popover from hiding. |
| \`wa-show\` | Emitted when the popover begins to show. Canceling this event will stop the popover from showing. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--arrow-size\` | \`0.375rem\` The size of the tiny arrow that points to the popover (set to zero to remove). Default |
| \`--hide-duration\` | \`100ms\` The speed of the hide animation. Default |
| \`--max-width\` | \`25rem\` The maximum width of the popover's body content. Default |
| \`--show-duration\` | \`100ms\` The speed of the show animation. Default |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`open\` | Applied when the popover is open. | \`:state(open)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`body\` | The popover's body where its content is rendered. | \`::part(body)\` |
| \`dialog\` | The native dialog element that contains the popover content. | \`::part(dialog)\` |
| \`popup\` | \`\` The internal element that positions the popover. | \`::part(popup)\` |
| \`popup\_\_arrow\` | \`arrow\` The popup's exported part. Use this to target the popover's arrow. | \`::part(popup\_\_arrow)\` |
| \`popup\_\_popup\` | \`popup\` The 's exported popup part. Use this to target the popover's popup container. | \`::part(popup\_\_popup)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-popup>`](https://webawesome.com/docs/components/popup)

**Need a hand?** Report a bug Ask for help