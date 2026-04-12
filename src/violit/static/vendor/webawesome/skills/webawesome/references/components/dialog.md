# Dialog

**Full documentation:** https://webawesome.com/docs/components/dialog


`<wa-dialog>` Since 2.0 Stable

Dialogs, sometimes called "modals", appear above the page and require the user's immediate attention.

```html
<wa-dialog label="Dialog" id="dialog-overview">
  This is a standard dialog. You can put any content you want in here!
  <wa-button appearance="filled" slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('#dialog-overview');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

## Examples

### Dialog without Header

Headers are enabled by default. To render a dialog without a header, add the `without-header` attribute.

```html
<wa-dialog label="Dialog" without-header class="dialog-without-header">
  Look ma, no header! Sometimes you just need a clean, simple dialog.
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-without-header');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

### Dialog with Footer

Footers can be used to display titles and more. Use the `footer` slot to add a footer to the dialog.

```html
<wa-dialog label="Dialog" class="dialog-footer">
  Check out the footer below — it's a great place for actions and buttons.
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-footer');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

### Opening and Closing Dialogs Declaratively

You can open and close dialogs with JavaScript by toggling the `open` attribute, but you can also do it declaratively. Add the `data-dialog="open id"` to any button on the page, where `id` is the ID of the dialog you want to open.

```html
<wa-dialog label="Dialog" id="dialog-opening">
  This dialog was opened declaratively — no JavaScript required!
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled" data-dialog="open dialog-opening">Open Dialog</wa-button>
```

Similarly, you can add `data-dialog="close"` to a button _inside_ of a dialog to tell it to close.

```html
<wa-dialog label="Dialog" id="dialog-dismiss">
  Click the button in the footer to close this dialog declaratively.
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled" data-dialog="open dialog-dismiss">Open Dialog</wa-button>
```

### Custom Width

Just use the `--width` custom property to set the dialog's width.

```html
<wa-dialog label="Dialog" class="dialog-width" style="--width: 50vw;">
  This dialog is wider than the default — handy when you need more room for content.
  <wa-button appearance="filled" slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-width');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

### Scrolling

By design, a dialog's height will never exceed that of the viewport. As such, dialogs will not scroll with the page ensuring the header and footer are always accessible to the user.

```html
<wa-dialog label="Dialog" class="dialog-scrolling">
  <div style="height: 150vh; border: dashed 2px var(--wa-color-surface-border); padding: 0 1rem;">
    <p>Scroll down and give it a try! 👇</p>
  </div>
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-scrolling');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

### Header Actions

The header shows a functional close button by default. You can use the `header-actions` slot to add additional [buttons](https://webawesome.com/docs/components/button) if needed.

```html
<wa-dialog label="Dialog" class="dialog-header-actions">
  <wa-button class="new-window" slot="header-actions" appearance="plain">
    <wa-icon name="arrow-up-right-from-square" variant="solid" label="Open in new window"></wa-icon>
  </wa-button>
  You can add custom actions to the header, like the icon button up there!
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-header-actions');
  const openButton = dialog.nextElementSibling;
  const newWindowButton = dialog.querySelector('.new-window');

  openButton.addEventListener('click', () => (dialog.open = true));
  newWindowButton.addEventListener('click', () => window.open(location.href));
</script>
```

### Light Dismissal

If you want the dialog to close when the user clicks on the overlay, add the `light-dismiss` attribute.

```html
<wa-dialog label="Dialog" light-dismiss class="dialog-light-dismiss">
  This dialog will close when you click on the overlay.
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-light-dismiss');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

### Preventing the Dialog from Closing

By default, dialogs will close when the user clicks the close button or presses the Escape key. In most cases, the default behavior is the best behavior in terms of UX. However, there are situations where this may be undesirable, such as when data loss will occur.

To keep the dialog open in such cases, you can cancel the `wa-hide` event. When canceled, the dialog will remain open and pulse briefly to draw the user's attention to it.

You can use `event.detail.source` to determine which element triggered the request to close. This example prevents the dialog from closing unless a specific button is clicked.

```html
<wa-dialog label="Dialog" class="dialog-deny-close">
  This dialog will only close when you click the button below.
  <wa-button slot="footer" variant="brand" data-dialog="close">Only this button will close it</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-deny-close');
  const openButton = dialog.nextElementSibling;
  const closeButton = dialog.querySelector('wa-button[slot="footer"]');

  openButton.addEventListener('click', () => (dialog.open = true));

  // Prevent the dialog from closing unless the close button was clicked
  dialog.addEventListener('wa-hide', event => {
    if (event.detail.source !== closeButton) {
      event.preventDefault();
    }
  });
</script>
```

### Setting Initial Focus

To give focus to a specific element when the dialog opens, use the `autofocus` attribute.

```html
<wa-dialog label="Dialog" class="dialog-focus">
  <wa-input autofocus placeholder="I will have focus when the dialog is opened"></wa-input>
  <wa-button slot="footer" variant="brand" data-dialog="close">Close</wa-button>
</wa-dialog>

<wa-button appearance="filled">Open Dialog</wa-button>

<script>
  const dialog = document.querySelector('.dialog-focus');
  const input = dialog.querySelector('wa-input');
  const openButton = dialog.nextElementSibling;

  openButton.addEventListener('click', () => (dialog.open = true));
</script>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/dialog/dialog.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaDialog from '@awesome.me/webawesome/dist/react/dialog';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The dialog's main content. |
| \`footer\` | The dialog's footer, usually one or more buttons representing various options. |
| \`header-actions\` | \`\` Optional actions to add to the header. Works best with . |
| \`label\` | \`label\` The dialog's . Alternatively, you can use the label attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`label\` label | \`label\` The dialog's as displayed in the header. You should always include a relevant label, as it is required for proper accessibility. If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`lightDismiss\` light-dismiss | \`boolean\` When enabled, the dialog will be closed when the user clicks outside of it. Type Default false | | |
| \`open\` open | \`boolean\` Indicates whether or not the dialog is open. Toggle this attribute to show and hide the dialog. Type Default false | | |
| \`withFooter\` with-footer | \`true\` Only required for SSR. Set to if you're slotting in a footer element so the server-rendered markup includes the footer before the component hydrates on the client. Type boolean Default false | | |
| \`withoutHeader\` without-header | \`boolean\` Disables the header. This will also remove the default close button. Type Default false | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-after-hide\` | Emitted after the dialog closes and all animations are complete. |
| \`wa-after-show\` | Emitted after the dialog opens and all animations are complete. |
| \`wa-hide\` | \`event.preventDefault()\` Emitted when the dialog is requested to close. Calling will prevent the dialog from closing. You can inspect event.detail.source to see which element caused the dialog to close. If the source is the dialog element itself, the user has pressed Escape or the dialog has been closed programmatically. Avoid using this unless closing the dialog will result in destructive behavior such as data loss. |
| \`wa-show\` | Emitted when the dialog opens. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--hide-duration\` | \`200ms\` The animation duration when hiding the dialog. Default |
| \`--show-duration\` | \`200ms\` The animation duration when showing the dialog. Default |
| \`--spacing\` | The amount of space around and between the dialog's content. |
| \`--width\` | The preferred width of the dialog. Note that the dialog will shrink to accommodate smaller screens. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`body\` | The dialog's body. | \`::part(body)\` |
| \`close-button\` | \`\` The close button, a . | \`::part(close-button)\` |
| \`close-button\_\_base\` | \`base\` The close button's exported part. | \`::part(close-button\_\_base)\` |
| \`dialog\` | \`\` The dialog's internal element. | \`::part(dialog)\` |
| \`footer\` | The dialog's footer. | \`::part(footer)\` |
| \`header\` | The dialog's header. This element wraps the title and header actions. | \`::part(header)\` |
| \`header-actions\` | \`\` Optional actions to add to the header. Works best with . | \`::part(header-actions)\` |
| \`title\` | The dialog's title. | \`::part(title)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)

**Need a hand?** Report a bug Ask for help