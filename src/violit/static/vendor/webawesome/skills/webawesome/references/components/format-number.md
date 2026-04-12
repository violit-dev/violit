# Format Number

**Full documentation:** https://webawesome.com/docs/components/format-number


`<wa-format-number>` Since 2.0 Stable

Formats a number using the specified locale and options.

Localization is handled by the browser's [`Intl.NumberFormat` API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat). No language packs are required.

```html
<div class="format-number-overview">
  <wa-format-number value="1000"></wa-format-number>
  <br /><br />
  <wa-input type="number" value="1000" label="Number to Format" style="max-width: 180px;"></wa-input>
</div>

<script>
  const container = document.querySelector('.format-number-overview');
  const formatter = container.querySelector('wa-format-number');
  const input = container.querySelector('wa-input');

  input.addEventListener('input', () => (formatter.value = input.value || 0));
</script>
```

## Examples

### Percentages

To get the value as a percent, set the `type` attribute to `percent`.

```html
<wa-format-number type="percent" value="0"></wa-format-number><br />
<wa-format-number type="percent" value="0.25"></wa-format-number><br />
<wa-format-number type="percent" value="0.50"></wa-format-number><br />
<wa-format-number type="percent" value="0.75"></wa-format-number><br />
<wa-format-number type="percent" value="1"></wa-format-number>
```

### Localization

Use the `lang` attribute to set the number formatting locale.

```html
English: <wa-format-number value="2000" lang="en" minimum-fraction-digits="2"></wa-format-number><br />
German: <wa-format-number value="2000" lang="de" minimum-fraction-digits="2"></wa-format-number><br />
Russian: <wa-format-number value="2000" lang="ru" minimum-fraction-digits="2"></wa-format-number>
```

### Currency

To format a number as a monetary value, set the `type` attribute to `currency` and set the `currency` attribute to the desired ISO 4217 currency code. You should also specify `lang` to ensure the the number is formatted correctly for the target locale.

```html
<wa-format-number type="currency" currency="USD" value="2000" lang="en-US"></wa-format-number><br />
<wa-format-number type="currency" currency="GBP" value="2000" lang="en-GB"></wa-format-number><br />
<wa-format-number type="currency" currency="EUR" value="2000" lang="de"></wa-format-number><br />
<wa-format-number type="currency" currency="RUB" value="2000" lang="ru"></wa-format-number><br />
<wa-format-number type="currency" currency="CNY" value="2000" lang="zh-cn"></wa-format-number>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/format-number/format-number.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaFormatNumber from '@awesome.me/webawesome/dist/react/format-number';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type | | |
| \`currency\` currency | \`string\` The ISO 4217 currency code to use when formatting. Type Default 'USD' | | |
| \`currencyDisplay\` currency-display | \`'symbol' \\| 'narrowSymbol' \\| 'code' \\| 'name'\` How to display the currency. Type Default 'symbol' | | |
| \`maximumFractionDigits\` maximum-fraction-digits | \`number\` The maximum of fraction digits to use. Possible values are 0-100. Type number | | |
| \`maximumSignificantDigits\` maximum-significant-digits | \`number\` The maximum of significant digits to use,. Possible values are 1-21. Type number | | |
| \`minimumFractionDigits\` minimum-fraction-digits | \`number\` The minimum of fraction digits to use. Possible values are 0-100. Type number | | |
| \`minimumIntegerDigits\` minimum-integer-digits | \`number\` The minimum of integer digits to use. Possible values are 1-21. Type number | | |
| \`minimumSignificantDigits\` minimum-significant-digits | \`number\` The minimum of significant digits to use. Possible values are 1-21. Type number | | |
| \`type\` type | \`'currency' \\| 'decimal' \\| 'percent'\` The formatting style to use. Type Default 'decimal' | | |
| \`value\` value | \`number\` The to format. Type number Default 0 | | |
| \`withoutGrouping\` without-grouping | \`boolean\` Turns off grouping separators. Type Default false | | |

**Need a hand?** Report a bug Ask for help