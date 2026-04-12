# Format Date

**Full documentation:** https://webawesome.com/docs/components/format-date


`<wa-format-date>` Since 2.0 Stable

Formats a date/time using the specified locale and options.

Localization is handled by the browser's [`Intl.DateTimeFormat` API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat). No language packs are required.

```html
<!-- Web Awesome 2 release date 🎉 -->
<wa-format-date date="2020-07-15T09:17:00-04:00"></wa-format-date>
```

The `date` attribute determines the date/time to use when formatting. It must be a string that [`Date.parse()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse) can interpret or a [`Date`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) object set via JavaScript. If omitted, the current date/time will be assumed.

When using strings, avoid ambiguous dates such as `03/04/2020` which can be interpreted as March 4 or April 3 depending on the user's browser and locale. Instead, always use a valid [ISO 8601 date time string](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse#Date_Time_String_Format) to ensure the date will be parsed properly by all clients.

## Examples

### Date & Time Formatting

Formatting options are based on those found in the [`Intl.DateTimeFormat` API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat). When formatting options are provided, the date/time will be formatted according to those values. When no formatting options are provided, a localized, numeric date will be displayed instead.

```html
<!-- Human-readable date -->
<wa-format-date month="long" day="numeric" year="numeric"></wa-format-date><br />

<!-- Time -->
<wa-format-date hour="numeric" minute="numeric"></wa-format-date><br />

<!-- Weekday -->
<wa-format-date weekday="long"></wa-format-date><br />

<!-- Month -->
<wa-format-date month="long"></wa-format-date><br />

<!-- Year -->
<wa-format-date year="numeric"></wa-format-date><br />

<!-- No formatting options -->
<wa-format-date></wa-format-date>
```

### Hour Formatting

By default, the browser will determine whether to use 12-hour or 24-hour time. To force one or the other, set the `hour-format` attribute to `12` or `24`.

```html
<wa-format-date hour="numeric" minute="numeric" hour-format="12"></wa-format-date><br />
<wa-format-date hour="numeric" minute="numeric" hour-format="24"></wa-format-date>
```

### Localization

Use the `lang` attribute to set the date/time formatting locale.

```html
English: <wa-format-date lang="en"></wa-format-date><br />
French: <wa-format-date lang="fr"></wa-format-date><br />
Russian: <wa-format-date lang="ru"></wa-format-date>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/format-date/format-date.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaFormatDate from '@awesome.me/webawesome/dist/react/format-date';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type | | |
| \`date\` date | \`date.toISOString()\` The date/time to format. If not set, the current date and time will be used. When passing a string, it's strongly recommended to use the ISO 8601 format to ensure timezones are handled correctly. To convert a date to this format in JavaScript, use . Type Date \\| string Default new Date() | | |
| \`day\` day | \`'numeric' \\| '2-digit'\` The format for displaying the day. Type | | |
| \`era\` era | \`'narrow' \\| 'short' \\| 'long'\` The format for displaying the era. Type | | |
| \`hour\` hour | \`'numeric' \\| '2-digit'\` The format for displaying the hour. Type | | |
| \`hourFormat\` hour-format | \`'auto' \\| '12' \\| '24'\` The format for displaying the hour. Type Default 'auto' | | |
| \`minute\` minute | \`'numeric' \\| '2-digit'\` The format for displaying the minute. Type | | |
| \`month\` month | \`'numeric' \\| '2-digit' \\| 'narrow' \\| 'short' \\| 'long'\` The format for displaying the month. Type | | |
| \`second\` second | \`'numeric' \\| '2-digit'\` The format for displaying the second. Type | | |
| \`timeZone\` time-zone | \`string\` The time zone to express the time in. Type | | |
| \`timeZoneName\` time-zone-name | \`'short' \\| 'long'\` The format for displaying the time. Type | | |
| \`weekday\` weekday | \`'narrow' \\| 'short' \\| 'long'\` The format for displaying the weekday. Type | | |
| \`year\` year | \`'numeric' \\| '2-digit'\` The format for displaying the year. Type | | |

**Need a hand?** Report a bug Ask for help