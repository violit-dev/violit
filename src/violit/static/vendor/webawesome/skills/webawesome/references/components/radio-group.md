# Radio Group

**Full documentation:** https://webawesome.com/docs/components/radio-group


`<wa-radio-group>` Since 2.0 Stable

Radio groups are used to group multiple [radios](https://webawesome.com/docs/components/radio) so they function as a single form control.

```html
<wa-radio-group label="Select an option" name="a" value="1">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

## Examples

### Checked

Use the `value` attribute on the radio group to set the checked radio.

```html
<wa-radio-group label="Select an option" name="a" value="2">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

To target checked radios with CSS, use the `:state(checked)` selector.

### Hint

Add descriptive hint to a radio group with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-radio-group label="Select an option" hint="Choose the most appropriate option." name="a" value="1">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

### Radio Buttons

Set the `appearance` attribute to `button` on all radios to render a radio button group.

```html
<wa-radio-group
  label="Horizontal options"
  hint="Select an option that makes you proud."
  orientation="horizontal"
  name="a"
  value="1"
>
  <wa-radio appearance="button" value="1">Option 1</wa-radio>
  <wa-radio appearance="button" value="2">Option 2</wa-radio>
  <wa-radio appearance="button" value="3">Option 3</wa-radio>
</wa-radio-group>

<br />

<wa-radio-group
  label="Vertical options"
  hint="Select an option that makes you proud."
  orientation="vertical"
  name="a"
  value="1"
  style="max-width: 300px;"
>
  <wa-radio appearance="button" value="1">Option 1</wa-radio>
  <wa-radio appearance="button" value="2">Option 2</wa-radio>
  <wa-radio appearance="button" value="3">Option 3</wa-radio>
</wa-radio-group>
```

### Disabling

To disable the entire radio group, add the `disabled` attribute to the radio group.

```html
<wa-radio-group label="Select an option" disabled>
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2" disabled>Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

To disable individual options, add the `disabled` attribute to the respective options.

```html
<wa-radio-group label="Select an option">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2" disabled>Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

### Orientation

The default orientation for radio items is `vertical`. Set the `orientation` to `horizontal` to items on the same row.

```html
<wa-radio-group
  label="Select an option"
  hint="Choose the most appropriate option."
  orientation="horizontal"
  name="a"
  value="1"
>
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

### Sizing Options

The size of radios will be determined by the Radio Group's `size` attribute.

```html
<wa-radio-group label="Small options" size="small" value="1">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
<br>
<wa-radio-group label="Medium options" size="medium" value="2">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
<br>
<wa-radio-group label="Large options" size="large" value="3">
  <wa-radio value="1">Option 1</wa-radio>
  <wa-radio value="2">Option 2</wa-radio>
  <wa-radio value="3">Option 3</wa-radio>
</wa-radio-group>
```

If you need to have radios of varying sizes, place the `size` attribute on individual radio items instead.

```html
<wa-radio-group label="Mixed options" value="medium">
  <wa-radio value="1" size="small">Small</wa-radio>
  <wa-radio value="2" size="medium">Medium</wa-radio>
  <wa-radio value="3" size="large">Large</wa-radio>
</wa-radio-group>
```

### Validation

Setting the `required` attribute to make selecting an option mandatory. If a value has not been selected, it will prevent the form from submitting and display an error message.

```html
<form class="validation">
  <wa-radio-group label="Select an option" name="a" required>
    <wa-radio value="1">Option 1</wa-radio>
    <wa-radio value="2">Option 2</wa-radio>
    <wa-radio value="3">Option 3</wa-radio>
  </wa-radio-group>
  <br />
  <wa-button appearance="filled" type="submit" variant="brand">Submit</wa-button>
</form>

<script>
  const form = document.querySelector('.validation');

  // Handle form submit
  form.addEventListener('submit', event => {
    event.preventDefault();
    alert('All fields are valid!');
  });
</script>
```

### Custom Validity

Use the `setCustomValidity()` method to set a custom validation message. This will prevent the form from submitting and make the browser display the error message you provide. To clear the error, call this function with an empty string.

```html
<form class="custom-validity">
  <wa-radio-group label="Select an option" name="a" value="1">
    <wa-radio value="1">Not me</wa-radio>
    <wa-radio value="2">Me neither</wa-radio>
    <wa-radio value="3">Choose me</wa-radio>
  </wa-radio-group>
  <br />
  <wa-button appearance="filled" type="submit" variant="brand">Submit</wa-button>
</form>

<script>
  const form = document.querySelector('.custom-validity');
  const radioGroup = form.querySelector('wa-radio-group');
  const errorMessage = 'You must choose the last option';

  // Set initial validity as soon as the element is defined
  customElements.whenDefined('wa-radio-group').then(() => {
    radioGroup.setCustomValidity(errorMessage);
  });

  // Update validity when a selection is made
  form.addEventListener('change', () => {
    const isValid = radioGroup.value === '3';
    radioGroup.setCustomValidity(isValid ? '' : errorMessage);
  });

  // Handle form submit
  form.addEventListener('submit', event => {
    event.preventDefault();
    alert('All fields are valid!');
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
import '@awesome.me/webawesome/dist/components/radio-group/radio-group.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaRadioGroup from '@awesome.me/webawesome/dist/react/radio-group';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | \`\` The default slot where elements are placed. |
| \`hint\` | \`hint\` Text that describes how to use the radio group. Alternatively, you can use the attribute. |
| \`label\` | \`label\` The radio group's . Required for proper accessibility. Alternatively, you can use the label attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[sizeStyles, formControlStyles, styles\] | | |
| \`defaultValue\` value | \`string \\| null\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the radio group and all child radios. Type Default false | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`hint\` hint | \`hint\` The radio groups's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`label\` label | \`label\` The radio group's . Required for proper accessibility. If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`name\` name | \`string \\| null\` The name of the radio group, submitted as a name/value pair with form data. Type Default null | | |
| \`orientation\` orientation | \`'horizontal' \\| 'vertical'\` The orientation in which to show radio items. Type Default 'vertical' | | |
| \`required\` required | \`boolean\` Ensures a child radio is checked before allowing the containing form to submit. Type Default false | | |
| \`size\` size | \`\` The radio group's size. When present, this size will be applied to all items inside. Type 'small' \\| 'medium' \\| 'large' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` We use the first available radio as the validationTarget similar to native HTML that shows the validation popup on the first radio element. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` | The current value of the radio group, submitted as a name/value pair with form data. | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`focus()\` | Sets focus on the radio group. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`change\` | Emitted when the radio group's selected value changes. |
| \`input\` | Emitted when the radio group receives user input. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`form-control\` | The form control that wraps the label, input, and hint. | \`::part(form-control)\` |
| \`form-control-input\` | The input's wrapper. | \`::part(form-control-input)\` |
| \`form-control-label\` | The label's wrapper. | \`::part(form-control-label)\` |
| \`hint\` | The hint's wrapper. | \`::part(hint)\` |
| \`radios\` | The wrapper than surrounds radio items, styled as a flex container by default. | \`::part(radios)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-radio>`](https://webawesome.com/docs/components/radio)

**Need a hand?** Report a bug Ask for help