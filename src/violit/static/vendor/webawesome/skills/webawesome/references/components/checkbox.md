# Checkbox

**Full documentation:** https://webawesome.com/docs/components/checkbox


`<wa-checkbox>` Since 2.0 Stable

Checkboxes allow the user to toggle an option on or off.

```html
<wa-checkbox>Checkbox</wa-checkbox>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Checked

Use the `checked` attribute to activate the checkbox.

```html
<wa-checkbox checked>Checked</wa-checkbox>
```

The `checked` attribute is the initial value and does not reflect changes, consistent with native checkboxes. To toggle the checked state with JavaScript, use the `checked` property instead. To target checked checkboxes with CSS, use the `:state(checked)` selector.

### Indeterminate

Use the `indeterminate` attribute to make the checkbox indeterminate.

```html
<wa-checkbox indeterminate>Indeterminate</wa-checkbox>
```

### Disabled

Use the `disabled` attribute to disable the checkbox.

```html
<wa-checkbox disabled>Disabled</wa-checkbox>
```

### Sizes

Use the `size` attribute to change a checkbox's size.

```html
<wa-checkbox size="small">Small</wa-checkbox>
<br />
<wa-checkbox size="medium">Medium</wa-checkbox>
<br />
<wa-checkbox size="large">Large</wa-checkbox>
```

### Hint

Add descriptive hint to a switch with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-checkbox hint="What should the user know about the checkbox?">Label</wa-checkbox>
```

### Custom Validity

Use the `setCustomValidity()` method to set a custom validation message. This will prevent the form from submitting and make the browser display the error message you provide. To clear the error, call this function with an empty string.

```html
<form class="custom-validity">
  <wa-checkbox>Check me</wa-checkbox>
  <br />
  <wa-button appearance="filled" type="submit" variant="brand" style="margin-top: 1rem;">Submit</wa-button>
</form>
<script>
  const form = document.querySelector('.custom-validity');
  const checkbox = form.querySelector('wa-checkbox');
  const errorMessage = `Don't forget to check me!`;

  // Set initial validity as soon as the element is defined
  customElements.whenDefined('wa-checkbox').then(async () => {
    await checkbox.updateComplete;
    checkbox.setCustomValidity(errorMessage);
  });

  // Update validity on change
  checkbox.addEventListener('change', () => {
    checkbox.setCustomValidity(checkbox.checked ? '' : errorMessage);
  });

  // Handle submit
  customElements.whenDefined('wa-checkbox').then(() => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      alert('All fields are valid!');
    });
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
import '@awesome.me/webawesome/dist/components/checkbox/checkbox.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaCheckbox from '@awesome.me/webawesome/dist/react/checkbox';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The checkbox's label. |
| \`hint\` | \`hint\` Text that describes how to use the checkbox. Alternatively, you can use the attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`checked\` | Draws the checkbox in a checked state. | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[formControlStyles, sizeStyles, styles\] | | |
| \`defaultChecked\` checked | \`boolean\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the checkbox. Type Default false | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`hint\` hint | \`hint\` The checkbox's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`indeterminate\` indeterminate | \`boolean\` Draws the checkbox in an indeterminate state. This is usually applied to checkboxes that represents a "select all/none" behavior when associated checkboxes have a mix of checked and unchecked states. Type Default false | | |
| \`name\` name | \`string \\| null\` The name of the checkbox, submitted as a name/value pair with form data. Type Default null | | |
| \`required\` required | \`boolean\` Makes the checkbox a required field. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The checkbox's size. Type Default 'medium' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` value | \`string \\| null\` The value of the checkbox, submitted as a name/value pair with form data. Type | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the checkbox. | |
| \`click()\` | Simulates a click on the checkbox. | |
| \`focus()\` | Sets focus on the checkbox. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the checkbox loses focus. |
| \`change\` | Emitted when the checked state changes. |
| \`focus\` | Emitted when the checkbox gains focus. |
| \`input\` | Emitted when the checkbox receives input. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--checked-icon-color\` | The color of the checked and indeterminate icons. |
| \`--checked-icon-scale\` | The size of the checked and indeterminate icons relative to the checkbox. |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`checked\` | Applied when the checkbox is checked. | \`:state(checked)\` |
| \`disabled\` | Applied when the checkbox is disabled. | \`:state(disabled)\` |
| \`indeterminate\` | Applied when the checkbox is in an indeterminate state. | \`:state(indeterminate)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's label . | \`::part(base)\` |
| \`checked-icon\` | \`\` The indeterminate icon, a element. | \`::part(indeterminate-icon)\` |
| \`label\` | The container that wraps the checkbox's label. | \`::part(label)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help