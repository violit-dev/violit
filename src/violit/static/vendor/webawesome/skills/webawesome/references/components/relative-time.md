# Relative Time

**Full documentation:** https://webawesome.com/docs/components/relative-time


`<wa-relative-time>` Since 2.0 Stable

Outputs a localized time phrase relative to the current date and time.

Localization is handled by the browser's [`Intl.RelativeTimeFormat` API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat). No language packs are required.

```html
<!-- Shoelace 2 release date 🎉 -->
<wa-relative-time date="2020-07-15T09:17:00-04:00"></wa-relative-time>
```

The `date` attribute determines when the date/time is calculated from. It must be a string that [`Date.parse()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse) can interpret or a [`Date`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) object set via JavaScript.

When using strings, avoid ambiguous dates such as `03/04/2020` which can be interpreted as March 4 or April 3 depending on the user's browser and locale. Instead, always use a valid [ISO 8601 date time string](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse#Date_Time_String_Format) to ensure the date will be parsed properly by all clients.

## Examples

### Keeping Time in Sync

Use the `sync` attribute to update the displayed value automatically as time passes.

```html
<div class="relative-time-sync">
  <wa-relative-time sync></wa-relative-time>
</div>

<script>
  const container = document.querySelector('.relative-time-sync');
  const relativeTime = container.querySelector('wa-relative-time');

  relativeTime.date = new Date(new Date().getTime() - 60000);
</script>
```

### Formatting Styles

You can change how the time is displayed using the `format` attribute. Note that some locales may display the same values for `narrow` and `short` formats.

```html
<wa-relative-time date="2020-07-15T09:17:00-04:00" format="narrow"></wa-relative-time><br />
<wa-relative-time date="2020-07-15T09:17:00-04:00" format="short"></wa-relative-time><br />
<wa-relative-time date="2020-07-15T09:17:00-04:00" format="long"></wa-relative-time>
```

### Localization

Use the `lang` attribute to set the desired locale.

```html
English: <wa-relative-time date="2020-07-15T09:17:00-04:00" lang="en-US"></wa-relative-time><br />
Chinese: <wa-relative-time date="2020-07-15T09:17:00-04:00" lang="zh-CN"></wa-relative-time><br />
German: <wa-relative-time date="2020-07-15T09:17:00-04:00" lang="de"></wa-relative-time><br />
Greek: <wa-relative-time date="2020-07-15T09:17:00-04:00" lang="el"></wa-relative-time><br />
Russian: <wa-relative-time date="2020-07-15T09:17:00-04:00" lang="ru"></wa-relative-time>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/relative-time/relative-time.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaRelativeTime from '@awesome.me/webawesome/dist/react/relative-time';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type | | |
| \`date\` date | \`date.toISOString()\` The date from which to calculate time from. If not set, the current date and time will be used. When passing a string, it's strongly recommended to use the ISO 8601 format to ensure timezones are handled correctly. To convert a date to this format in JavaScript, use . Type Date \\| string Default new Date() | | |
| \`format\` format | \`'long' \\| 'short' \\| 'narrow'\` The formatting style to use. Type Default 'long' | | |
| \`numeric\` numeric | \`auto\` When , values such as "yesterday" and "tomorrow" will be shown when possible. When always, values such as "1 day ago" and "in 1 day" will be shown. Type 'always' \\| 'auto' Default 'auto' | | |
| \`sync\` sync | \`boolean\` Keep the displayed value up to date as time passes. Type Default false | | |

**Need a hand?** Report a bug Ask for help