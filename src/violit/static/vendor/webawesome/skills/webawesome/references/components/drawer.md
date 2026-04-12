# Drawer

**Full documentation:** https://webawesome.com/docs/components/drawer


`<wa-drawer>` Since 2.0 Stable

Drawers slide in from a container to expose additional options and information.

```html
<wa-drawer label="Drawer" id="drawer-overview">
  Drawers are great for showing additional content without leaving the current page.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('#drawer-overview');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

## Examples

### Drawer without Header

Headers are enabled by default. To render a drawer without a header, add the `without-header` attribute.

```html
<wa-drawer label="Drawer" without-header class="drawer-without-header">
  Look ma, no header!
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-without-header');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Drawer with Footer

Footers can be used to display titles and more. Use the `footer` slot to add a footer to the drawer.

```html
<wa-drawer label="Drawer" class="drawer-footer">
  This drawer has a footer where you can put actions and other controls.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-footer');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Opening and Closing Drawers Declaratively

You can open and close drawers with JavaScript by toggling the `open` attribute, but you can also do it declaratively. Add the `data-drawer="open id"` to any button on the page, where `id` is the ID of the drawer you want to open.

```html
<wa-drawer label="Drawer" id="drawer-opening">
  This drawer was opened declaratively using a data attribute on the button.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled" data-drawer="open drawer-opening">Open Drawer</wa-button>
```

Similarly, you can add `data-drawer="close"` to a button _inside_ of a drawer to tell it to close.

```html
<wa-drawer label="Drawer" id="drawer-dismiss">
  Click the button below to close this drawer — no JavaScript required!
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled" data-drawer="open drawer-dismiss">Open Drawer</wa-button>
```

### Slide in From Start

By default, drawers slide in from the end. To make the drawer slide in from the start, set the `placement` attribute to `start`.

```html
<wa-drawer label="Drawer" placement="start" class="drawer-placement-start">
  This drawer slides in from the start.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-placement-start');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Slide in From Top

To make the drawer slide in from the top, set the `placement` attribute to `top`.

```html
<wa-drawer label="Drawer" placement="top" class="drawer-placement-top">
  This drawer slides in from the top.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-placement-top');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Slide in From Bottom

To make the drawer slide in from the bottom, set the `placement` attribute to `bottom`.

```html
<wa-drawer label="Drawer" placement="bottom" class="drawer-placement-bottom">
  This drawer slides in from the bottom.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-placement-bottom');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Custom Size

Use the `--size` custom property to set the drawer's size. This will be applied to the drawer's width or height depending on its `placement`.

```html
<wa-drawer label="Drawer" class="drawer-custom-size" style="--size: 50vw;">
  This drawer is always 50% of the viewport.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-custom-size');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Scrolling

By design, a drawer's height will never exceed 100% of its container. As such, drawers will not scroll with the page to ensure the header and footer are always accessible to the user.

```html
<wa-drawer label="Drawer" class="drawer-scrolling">
  <div style="height: 150vh; border: dashed 2px var(--wa-color-surface-border); padding: 0 1rem;">
    <p>Scroll down and give it a try! 👇</p>
  </div>
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-scrolling');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Header Actions

The header shows a functional close button by default. You can use the `header-actions` slot to add additional [buttons](https://webawesome.com/docs/components/button) if needed.

```html
<wa-drawer label="Drawer" class="drawer-header-actions">
  <wa-button class="new-window" slot="header-actions" appearance="plain">
    <wa-icon name="arrow-up-right-from-square" variant="solid" label="Open in new window"></wa-icon>
  </wa-button>
  You can add custom actions to the header, like the button up there to open in a new window.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-header-actions');
  const openButton = drawer.nextElementSibling;
  const newWindowButton = drawer.querySelector('.new-window');

  openButton.addEventListener('click', () => (drawer.open = true));
  newWindowButton.addEventListener('click', () => window.open(location.href));
</script>
```

### Light Dismissal

If you want the drawer to close when the user clicks on the overlay, add the `light-dismiss` attribute.

```html
<wa-drawer label="Drawer" light-dismiss class="drawer-light-dismiss">
  This drawer will close when you click on the overlay.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-light-dismiss');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

### Preventing the Drawer from Closing

By default, drawers will close when the user clicks the close button, clicks the overlay, or presses the Escape key. In most cases, the default behavior is the best behavior in terms of UX. However, there are situations where this may be undesirable, such as when data loss will occur.

To keep the drawer open in such cases, you can cancel the `wa-hide` event. When canceled, the drawer will remain open and pulse briefly to draw the user's attention to it.

You can use `event.detail.source` to determine what triggered the request to close. This example prevents the drawer from closing when the overlay is clicked, but allows the close button or Escape to dismiss it.

```html
<wa-drawer label="Drawer" class="drawer-deny-close">
  This drawer will only close when you click the button below.
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-deny-close');
  const openButton = drawer.nextElementSibling;
  const closeButton = drawer.querySelector('wa-button[slot="footer"]');

  openButton.addEventListener('click', () => (drawer.open = true));

  // Prevent the drawer from closing unless the close button is clicked
  drawer.addEventListener('wa-hide', event => {
    if (event.detail.source !== closeButton) {
      event.preventDefault();
    }
  });
</script>
```

### Setting Initial Focus

To give focus to a specific element when the drawer opens, use the `autofocus` attribute.

```html
<wa-drawer label="Drawer" class="drawer-focus">
  <wa-input autofocus placeholder="I will have focus when the drawer is opened"></wa-input>
  <wa-button slot="footer" variant="brand" data-drawer="close">Close</wa-button>
</wa-drawer>

<wa-button appearance="filled">Open Drawer</wa-button>

<script>
  const drawer = document.querySelector('.drawer-focus');
  const input = drawer.querySelector('wa-input');
  const openButton = drawer.nextElementSibling;

  openButton.addEventListener('click', () => (drawer.open = true));
</script>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/drawer/drawer.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaDrawer from '@awesome.me/webawesome/dist/react/drawer';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The drawer's main content. |
| \`footer\` | The drawer's footer, usually one or more buttons representing various options. |
| \`header-actions\` | \`\` Optional actions to add to the header. Works best with . |
| \`label\` | \`label\` The drawer's . Alternatively, you can use the label attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`label\` label | \`label\` The drawer's as displayed in the header. You should always include a relevant label, as it is required for proper accessibility. If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`lightDismiss\` light-dismiss | \`boolean\` When enabled, the drawer will be closed when the user clicks outside of it. Type Default true | | |
| \`modal\` | \`modal.activateExternal()\` Exposes the internal modal utility that controls focus trapping. To temporarily disable focus trapping and allow third-party modals spawned from an active Shoelace modal, call when the third-party modal opens. Upon closing, call modal.deactivateExternal() to restore Shoelace's focus trapping. | | |
| \`open\` open | \`boolean\` Indicates whether or not the drawer is open. Toggle this attribute to show and hide the drawer. Type Default false | | |
| \`placement\` placement | \`'top' \\| 'end' \\| 'bottom' \\| 'start'\` The direction from which the drawer will open. Type Default 'end' | | |
| \`withFooter\` with-footer | \`true\` Only required for SSR. Set to if you're slotting in a footer element so the server-rendered markup includes the footer before the component hydrates on the client. Type boolean Default false | | |
| \`withoutHeader\` without-header | \`boolean\` Disables the header. This will also remove the default close button. Type Default false | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-after-hide\` | Emitted after the drawer closes and all animations are complete. |
| \`wa-after-show\` | Emitted after the drawer opens and all animations are complete. |
| \`wa-hide\` | \`event.preventDefault()\` Emitted when the drawer is requesting to close. Calling will prevent the drawer from closing. You can inspect event.detail.source to see which element caused the drawer to close. If the source is the drawer element itself, the user has pressed Escape or the drawer has been closed programmatically. Avoid using this unless closing the drawer will result in destructive behavior such as data loss. |
| \`wa-show\` | Emitted when the drawer opens. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--hide-duration\` | \`200ms\` The animation duration when hiding the drawer. Default |
| \`--show-duration\` | \`200ms\` The animation duration when showing the drawer. Default |
| \`--size\` | \`placement\` The preferred size of the drawer. This will be applied to the drawer's width or height depending on its . Note that the drawer will shrink to accommodate smaller screens. |
| \`--spacing\` | The amount of space around and between the drawer's content. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`body\` | The drawer's body. | \`::part(body)\` |
| \`close-button\` | \`\` The close button, a . | \`::part(close-button)\` |
| \`close-button\_\_base\` | \`base\` The close button's exported part. | \`::part(close-button\_\_base)\` |
| \`dialog\` | \`\` The drawer's internal element. | \`::part(dialog)\` |
| \`footer\` | The drawer's footer. | \`::part(footer)\` |
| \`header\` | The drawer's header. This element wraps the title and header actions. | \`::part(header)\` |
| \`header-actions\` | \`\` Optional actions to add to the header. Works best with . | \`::part(header-actions)\` |
| \`title\` | The drawer's title. | \`::part(title)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)

**Need a hand?** Report a bug Ask for help