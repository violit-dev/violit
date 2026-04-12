# Include

**Full documentation:** https://webawesome.com/docs/components/include


`<wa-include>` Since 2.0 Stable

Includes give you the power to embed external HTML files into the page.

Included files are asynchronously requested using `window.fetch()`. Requests are cached, so the same file can be included multiple times, but only one request will be made.

The included content will be inserted into the `<wa-include>` element's default slot so it can be easily accessed and styled through the light DOM.

```html
<wa-include src="https://shoelace.style/assets/examples/include.html"></wa-include>
```

## Examples

### Listening for Events

When an include file loads successfully, the `wa-load` event will be emitted. You can listen for this event to add custom loading logic to your includes.

If the request fails, the `wa-include-error` event will be emitted. In this case, `event.detail.status` will contain the resulting HTTP status code of the request, e.g. 404 (not found).

```html
<wa-include src="https://shoelace.style/assets/examples/include.html"></wa-include>

<script>
  const include = document.querySelector('wa-include');

  include.addEventListener('wa-load', event => {
    if (event.eventPhase === Event.AT_TARGET) {
      console.log('Success');
    }
  });

  include.addEventListener('wa-include-error', event => {
    if (event.eventPhase === Event.AT_TARGET) {
      console.log('Error', event.detail.status);
    }
  });
</script>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/include/include.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaInclude from '@awesome.me/webawesome/dist/react/include';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`allowScripts\` allow-scripts | \`boolean\` Allows included scripts to be executed. Be sure you trust the content you are including as it will be executed as code and can result in XSS attacks. Type Default false | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`mode\` mode | \`'cors' \\| 'no-cors' \\| 'same-origin'\` The fetch mode to use. Type Default 'cors' | | |
| \`src\` src | \`string\` The location of the HTML file to include. Be sure you trust the content you are including as it will be executed as code and can result in XSS attacks. Type | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-include-error\` | Emitted when the included file fails to load due to an error. |
| \`wa-load\` | Emitted when the included file is loaded. |

**Need a hand?** Report a bug Ask for help