# QR Code

**Full documentation:** https://webawesome.com/docs/components/qr-code


`<wa-qr-code>` Since 2.0 Stable

Generates a [QR code](https://www.qrcode.com/) and renders it using the [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API).

QR codes are useful for providing small pieces of information to users who can quickly scan them with a smartphone. Most smartphones have built-in QR code scanners, so simply pointing the camera at a QR code will decode it and allow the user to visit a website, dial a phone number, read a message, etc.

```html
<div class="qr-overview">
  <wa-qr-code value="https://shoelace.style/" label="Scan this code to visit Web Awesome on the web!"></wa-qr-code>
  <br />

  <wa-input maxlength="255" with-clear label="Value">
    <wa-icon slot="start" name="link"></wa-icon>
  </wa-input>
</div>

<script>
  const container = document.querySelector('.qr-overview');
  const qrCode = container.querySelector('wa-qr-code');
  const input = container.querySelector('wa-input');

  customElements.whenDefined('wa-qr-code').then(() => {
    input.value = qrCode.value;
    input.addEventListener('input', () => (qrCode.value = input.value));
  });
</script>

<style>
  .qr-overview {
    max-width: 256px;
  }

  .qr-overview wa-input {
    margin-top: 1rem;
  }
</style>
```

## Examples

### Size

Use the `size` attribute to change the size of the QR code.

```html
<wa-qr-code value="https://shoelace.style/" size="64"></wa-qr-code>
```

### Colors

The QR code's fill color is determined by the current text color. To change it, set the CSS `color` property on the host element or an ancestor element.

The canvas is always transparent, so use the `background` or `background-color` CSS property on the host element to set a background color.

A _quiet zone_ is the blank space around a QR code that helps scanners detect it more reliably. Use the `padding` CSS property on the host element to add one.

```html
<wa-qr-code
  value="https://shoelace.style/"
  style="
    color: var(--wa-color-indigo-20);
    background-color: var(--wa-color-indigo-90);
    border-radius: var(--wa-border-radius-m);
    padding: 1rem;
  "
></wa-qr-code>
```

### Radius

Create a rounded effect with the `radius` attribute.

```html
<wa-qr-code value="https://shoelace.style/" radius="0.5"></wa-qr-code>
```

### Error Correction

QR codes can be rendered with various levels of [error correction](https://www.qrcode.com/en/about/error_correction.html) that can be set using the `error-correction` attribute. This example generates four codes with the same value using different error correction levels.

```html
<div class="qr-error-correction">
  <wa-qr-code value="https://shoelace.style/" error-correction="L"></wa-qr-code>
  <wa-qr-code value="https://shoelace.style/" error-correction="M"></wa-qr-code>
  <wa-qr-code value="https://shoelace.style/" error-correction="Q"></wa-qr-code>
  <wa-qr-code value="https://shoelace.style/" error-correction="H"></wa-qr-code>
</div>

<style>
  .qr-error-correction {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
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
import '@awesome.me/webawesome/dist/components/qr-code/qr-code.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaQrCode from '@awesome.me/webawesome/dist/react/qr-code';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`background\` background | \`transparent\` The background color. This can be any valid CSS color or . It cannot be a CSS custom property. Type string Default '' | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`errorCorrection\` error-correction | \`'L' \\| 'M' \\| 'Q' \\| 'H'\` The level of error correction to use. Learn more Type Default 'H' | | |
| \`fill\` fill | \`string\` The fill color. This can be any valid CSS color, but not a CSS custom property. Type Default '' | | |
| \`label\` label | \`string\` The label for assistive devices to announce. If unspecified, the value will be used instead. Type Default '' | | |
| \`radius\` radius | \`number\` The edge radius of each module. Must be between 0 and 0.5. Type Default 0 | | |
| \`size\` size | \`number\` The size of the QR code, in pixels. Type Default 128 | | |
| \`value\` value | \`string\` The QR code's value. Type Default '' | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

**Need a hand?** Report a bug Ask for help