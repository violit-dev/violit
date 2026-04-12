# Button

**Full documentation:** https://webawesome.com/docs/components/button


`<wa-button>` Since 2.0 Stable

Buttons represent actions that are available to the user.

```html
<wa-button>Button</wa-button>
```

## Examples

### Variants

Use the `variant` attribute to set the button's semantic variant.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button variant="neutral">Neutral</wa-button>
  <wa-button variant="brand">Brand</wa-button>
  <wa-button variant="success">Success</wa-button>
  <wa-button variant="warning">Warning</wa-button>
  <wa-button variant="danger">Danger</wa-button>
</div>
```

### Appearance

Use the `appearance` attribute to change the button's visual appearance.

```html
<div class="wa-stack">
  <div class="wa-cluster wa-gap-2xs">
    <wa-button appearance="accent" variant="neutral">Accent</wa-button>
    <wa-button appearance="filled-outlined" variant="neutral">Filled-Outlined</wa-button>
    <wa-button appearance="filled" variant="neutral">Filled</wa-button>
    <wa-button appearance="outlined" variant="neutral">Outlined</wa-button>
    <wa-button appearance="plain" variant="neutral">Plain</wa-button>
  </div>
  <div class="wa-cluster wa-gap-2xs">
    <wa-button appearance="accent" variant="brand">Accent</wa-button>
    <wa-button appearance="filled-outlined" variant="brand">Filled-Outlined</wa-button>
    <wa-button appearance="filled" variant="brand">Filled</wa-button>
    <wa-button appearance="outlined" variant="brand">Outlined</wa-button>
    <wa-button appearance="plain" variant="brand">Plain</wa-button>
  </div>
  <div class="wa-cluster wa-gap-2xs">
    <wa-button appearance="accent" variant="success">Accent</wa-button>
    <wa-button appearance="filled-outlined" variant="success">Filled-Outlined</wa-button>
    <wa-button appearance="filled" variant="success">Filled</wa-button>
    <wa-button appearance="outlined" variant="success">Outlined</wa-button>
    <wa-button appearance="plain" variant="success">Plain</wa-button>
  </div>
  <div class="wa-cluster wa-gap-2xs">
    <wa-button appearance="accent" variant="warning">Accent</wa-button>
    <wa-button appearance="filled-outlined" variant="warning">Filled-Outlined</wa-button>
    <wa-button appearance="filled" variant="warning">Filled</wa-button>
    <wa-button appearance="outlined" variant="warning">Outlined</wa-button>
    <wa-button appearance="plain" variant="warning">Plain</wa-button>
  </div>
  <div class="wa-cluster wa-gap-2xs">
    <wa-button appearance="accent" variant="danger">Accent</wa-button>
    <wa-button appearance="filled-outlined" variant="danger">Filled-Outlined</wa-button>
    <wa-button appearance="filled" variant="danger">Filled</wa-button>
    <wa-button appearance="outlined" variant="danger">Outlined</wa-button>
    <wa-button appearance="plain" variant="danger">Plain</wa-button>
  </div>
</div>
```

### Sizes

Use the `size` attribute to change a button's size.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button size="small">Small</wa-button>
  <wa-button size="medium">Medium</wa-button>
  <wa-button size="large">Large</wa-button>
</div>
```

### Pill Buttons

Use the `pill` attribute to give buttons rounded edges.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button size="small" pill>Small</wa-button>
  <wa-button size="medium" pill>Medium</wa-button>
  <wa-button size="large" pill>Large</wa-button>
</div>
```

### Link Buttons

It's often helpful to have a button that works like a link. This is possible by setting the `href` attribute, which will make the component render an `<a>` under the hood. This gives you all the default link behavior the browser provides (e.g. CMD/CTRL/SHIFT + CLICK) and exposes the `rel`, `target`, and `download` attributes.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button href="https://example.com/">Link</wa-button>
  <wa-button href="https://example.com/" target="_blank">New Window</wa-button>
  <wa-button href="/assets/images/logo.svg" download="shoelace.svg">Download</wa-button>
</div>
```

### Icon Buttons

When only an [icon](https://webawesome.com/docs/components/icon) is slotted into the `label` slot, the button becomes an icon button. In this case, it's important to give the icon a label for users with assistive devices. Icon buttons can use any appearance or variant.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button variant="neutral" appearance="accent"><wa-icon name="house" label="Home"></wa-icon></wa-button>
  <wa-button variant="neutral" appearance="outlined"><wa-icon name="house" label="Home"></wa-icon></wa-button>
  <wa-button variant="neutral" appearance="filled"><wa-icon name="house" label="Home"></wa-icon></wa-button>
  <wa-button variant="neutral" appearance="plain"><wa-icon name="house" label="Home"></wa-icon></wa-button>
</div>
```

### Setting a Custom Width

As expected, buttons can be given a custom width by setting the `width` CSS property. This is useful for making buttons span the full width of their container on smaller screens.

```html
<div class="wa-stack">
  <wa-button size="small" style="width: 100%;">Small</wa-button>
  <wa-button size="medium" style="width: 100%;">Medium</wa-button>
  <wa-button size="large" style="width: 100%;">Large</wa-button>
</div>
```

### Start & End Decorations

Use the `start` and `end` slots to add presentational elements like `<wa-icon>` next to the button label.

```html
<div class="wa-stack">
  <div class="wa-cluster wa-gap-2xs">
    <wa-button size="small">
      <wa-icon slot="start" name="gear"></wa-icon>
      Settings
    </wa-button>

    <wa-button size="small">
      <wa-icon slot="end" name="undo"></wa-icon>
      Refresh
    </wa-button>

    <wa-button size="small">
      <wa-icon slot="start" name="link"></wa-icon>
      <wa-icon slot="end" name="arrow-up-right-from-square"></wa-icon>
      Open
    </wa-button>
  </div>

  <div class="wa-cluster wa-gap-2xs">
    <wa-button>
      <wa-icon slot="start" name="gear"></wa-icon>
      Settings
    </wa-button>

    <wa-button>
      <wa-icon slot="end" name="undo"></wa-icon>
      Refresh
    </wa-button>

    <wa-button>
      <wa-icon slot="start" name="link"></wa-icon>
      <wa-icon slot="end" name="arrow-up-right-from-square"></wa-icon>
      Open
    </wa-button>
  </div>

  <div class="wa-cluster wa-gap-2xs">
    <wa-button size="large">
      <wa-icon slot="start" name="gear"></wa-icon>
      Settings
    </wa-button>

    <wa-button size="large">
      <wa-icon slot="end" name="undo"></wa-icon>
      Refresh
    </wa-button>

    <wa-button size="large">
      <wa-icon slot="start" name="link"></wa-icon>
      <wa-icon slot="end" name="arrow-up-right-from-square"></wa-icon>
      Open
    </wa-button>
  </div>
</div>
```

### Caret

Use the `with-caret` attribute to add a dropdown indicator when a button will trigger a dropdown, menu, or popover.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button size="small" with-caret>
    <wa-icon name="gear" label="Settings"></wa-icon>
  </wa-button>
  <wa-button size="small" with-caret>Small</wa-button>
  <wa-button size="medium" with-caret>Medium</wa-button>
  <wa-button size="large" with-caret>Large</wa-button>
</div>
```

### Loading

Use the `loading` attribute to make a button busy. The width will remain the same as before, preventing adjacent elements from moving around.

```html
<div class="wa-cluster wa-gap-2xs">
  <wa-button variant="brand" loading>Brand</wa-button>
  <wa-button variant="success" loading>Success</wa-button>
  <wa-button variant="neutral" loading>Neutral</wa-button>
  <wa-button variant="warning" loading>Warning</wa-button>
  <wa-button variant="danger" loading>Danger</wa-button>
</div>
```

### Disabled

Use the `disabled` attribute to disable a button.

```html
<wa-button variant="brand" disabled>Brand</wa-button>
<wa-button variant="success" disabled>Success</wa-button>
<wa-button variant="neutral" disabled>Neutral</wa-button>
<wa-button variant="warning" disabled>Warning</wa-button>
<wa-button variant="danger" disabled>Danger</wa-button>

<br /><br />

<wa-button href="https://example.com/" disabled>Link</wa-button>
<wa-button href="https://example.com/" target="_blank" disabled>New Window</wa-button>
<wa-button href="/assets/images/logo.svg" download="shoelace.svg" disabled>Download</wa-button>
```

### Styling Buttons

This example demonstrates how to style buttons using a custom class. This is the recommended approach if you need to add additional variations. To customize an existing variation, modify the selector to target the button's `variant` attribute instead of a class (e.g. `wa-button[variant="brand"]`).

```html
<wa-button class="pink">Pink Button</wa-button>

<style>
  wa-button.pink::part(base) {
    border-radius: 6px;
    border: solid 2px;
    background: #ff1493;
    border-top-color: #ff7ac1;
    border-left-color: #ff7ac1;
    border-bottom-color: #ad005c;
    border-right-color: #ad005c;
    color: white;
    font-size: 1.125rem;
    box-shadow: 0 2px 10px #0002;
    transition: all var(--wa-transition-slow) var(--wa-transition-easing);
  }

  wa-button.pink::part(base):hover {
    transform: scale(1.05);
  }

  wa-button.pink::part(base):active {
    border-top-color: #ad005c;
    border-right-color: #ff7ac1;
    border-bottom-color: #ff7ac1;
    border-left-color: #ad005c;
    transform: translateY(1px);
  }

  wa-button.pink::part(base):focus-visible {
    outline: dashed 2px deeppink;
    outline-offset: 4px;
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
import '@awesome.me/webawesome/dist/components/button/button.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaButton from '@awesome.me/webawesome/dist/react/button';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The button's label. |
| \`end\` | \`\` An element, such as , placed before the label. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'accent' \\| 'filled' \\| 'outlined' \\| 'filled-outlined' \\| 'plain'\` The button's visual appearance. Type Default 'accent' | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles, variantStyles, sizeStyles\] | | |
| \`disabled\` disabled | \`boolean\` Disables the button. Type Default false | | |
| \`download\` download | \`href\` Tells the browser to download the linked file as this filename. Only used when is present. Type string \\| undefined | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`formAction\` formaction | \`action\` Used to override the form owner's attribute. Type string | | |
| \`formEnctype\` formenctype | \`enctype\` Used to override the form owner's attribute. Type 'application/x-www-form-urlencoded' \\| 'multipart/form-data' \\| 'text/plain' | | |
| \`formMethod\` formmethod | \`method\` Used to override the form owner's attribute. Type 'post' \\| 'get' | | |
| \`formNoValidate\` formnovalidate | \`novalidate\` Used to override the form owner's attribute. Type boolean | | |
| \`formTarget\` formtarget | \`target\` Used to override the form owner's attribute. Type '\_self' \\| '\_blank' \\| '\_parent' \\| '\_top' \\| string | | |
| \`href\` href | \`\` When set, the underlying button will be rendered as an with this href instead of a . Type string | | |
| \`loading\` loading | \`boolean\` Draws the button in a loading state. Type Default false | | |
| \`name\` name | \`href\` The name of the button, submitted as a name/value pair with form data, but only when this button is the submitter. This attribute is ignored when is present. Type string \\| null Default null | | |
| \`pill\` pill | \`boolean\` Draws a pill-style button with rounded edges. Type Default false | | |
| \`rel\` rel | \`href\` When using , this attribute will map to the underlying link's rel attribute. Type string \\| undefined | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The button's size. Type Default 'medium' | | |
| \`target\` target | \`href\` Tells the browser where to open the link. Only used when is present. Type '\_blank' \\| '\_parent' \\| '\_self' \\| '\_top' | | |
| \`type\` type | \`button\` The type of . Note that the default value is button instead of submit, which is opposite of how native elements behave. When the type is submit, the button will submit the surrounding form. Type 'button' \\| 'submit' \\| 'reset' Default 'button' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` value | \`href\` The value of the button, submitted as a pair with the button's name as part of the form data, but only when this button is the submitter. This attribute is ignored when is present. Type string | | |
| \`variant\` variant | \`neutral\` The button's theme variant. Defaults to if not within another element with a variant. Type 'neutral' \\| 'brand' \\| 'success' \\| 'warning' \\| 'danger' Default 'neutral' | | |
| \`withCaret\` with-caret | \`boolean\` Draws the button with a caret. Used to indicate that the button triggers a dropdown menu or similar behavior. Type Default false | | |
| \`withEnd\` with-end | \`true\` Only required for SSR. Set to if you're slotting in an end element so the server-rendered markup includes the end slot before the component hydrates on the client. Type boolean Default false | | |
| \`withStart\` with-start | \`true\` Only required for SSR. Set to if you're slotting in a start element so the server-rendered markup includes the start slot before the component hydrates on the client. Type boolean Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the button. | |
| \`click()\` | Simulates a click on the button. | |
| \`focus()\` | Sets focus on the button. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the button loses focus. |
| \`focus\` | Emitted when the button gains focus. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`disabled\` | Applied when the button is disabled. | \`:state(disabled)\` |
| \`icon-button\` | \`

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |
| \`caret\` | \`

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)

**Need a hand?** Report a bug Ask for help