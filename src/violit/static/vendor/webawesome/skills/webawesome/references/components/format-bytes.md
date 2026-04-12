# Format Bytes

**Full documentation:** https://webawesome.com/docs/components/format-bytes


`<wa-format-bytes>` Since 2.0 Stable

Formats a number as a human readable bytes value.

```html
<div class="format-bytes-overview">
  The file is <wa-format-bytes value="1000"></wa-format-bytes> in size. <br /><br />
  <wa-input type="number" value="1000" label="Number to Format" style="max-width: 180px;"></wa-input>
</div>

<script>
  const container = document.querySelector('.format-bytes-overview');
  const formatter = container.querySelector('wa-format-bytes');
  const input = container.querySelector('wa-input');

  input.addEventListener('input', () => (formatter.value = input.value || 0));
</script>
```

## Examples

### Formatting Bytes

Set the `value` attribute to a number to get the value in bytes.

```html
<wa-format-bytes value="12"></wa-format-bytes><br />
<wa-format-bytes value="1200"></wa-format-bytes><br />
<wa-format-bytes value="1200000"></wa-format-bytes><br />
<wa-format-bytes value="1200000000"></wa-format-bytes>
```

### Formatting Bits

To get the value in bits, set the `unit` attribute to `bit`.

```html
<wa-format-bytes value="12" unit="bit"></wa-format-bytes><br />
<wa-format-bytes value="1200" unit="bit"></wa-format-bytes><br />
<wa-format-bytes value="1200000" unit="bit"></wa-format-bytes><br />
<wa-format-bytes value="1200000000" unit="bit"></wa-format-bytes>
```

### Localization

Use the `lang` attribute to set the number formatting locale.

```html
<wa-format-bytes value="12" lang="de"></wa-format-bytes><br />
<wa-format-bytes value="1200" lang="de"></wa-format-bytes><br />
<wa-format-bytes value="1200000" lang="de"></wa-format-bytes><br />
<wa-format-bytes value="1200000000" lang="de"></wa-format-bytes>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/format-bytes/format-bytes.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaFormatBytes from '@awesome.me/webawesome/dist/react/format-bytes';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type | | |
| \`display\` display | \`'long' \\| 'short' \\| 'narrow'\` Determines how to display the result, e.g. "100 bytes", "100 b", or "100b". Type Default 'short' | | |
| \`unit\` unit | \`'byte' \\| 'bit'\` The type of unit to display. Type Default 'byte' | | |
| \`value\` value | \`number\` The to format in bytes. Type number Default 0 | | |

**Need a hand?** Report a bug Ask for help