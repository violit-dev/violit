# Number Input

**Full documentation:** https://webawesome.com/docs/components/number-input


`<wa-number-input>` Since 3.2 Experimental

Number inputs allow users to enter and edit numeric values with optional stepper buttons.

```html
<wa-number-input label="Quantity" value="1" style="max-width: 260px;"></wa-number-input>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Labels

Use the `label` attribute to give the input an accessible label. For labels that contain HTML, use the `label` slot instead.

```html
<wa-number-input label="How many items?" style="max-width: 260px;"></wa-number-input>
```

### Hint

Add descriptive hint to an input with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-number-input label="Order quantity" hint="Enter the number of items you'd like to order" style="max-width: 260px;"></wa-number-input>
```

### Placeholders

Use the `placeholder` attribute to add a placeholder.

```html
<wa-number-input placeholder="Enter a number" style="max-width: 260px;"></wa-number-input>
```

### Setting Min, Max, and Step

Use the `min` and `max` attributes to set a minimum and maximum value. Use the `step` attribute to change the granularity the value must adhere to when using the stepper buttons or arrow keys.

```html
<wa-number-input
  label="Donation amount"
  hint="Amount in dollars (10-100, increments of 5)"
  min="10"
  max="100"
  step="5"
  value="25"
  style="max-width: 260px;"
></wa-number-input>
```

### Appearance

Use the `appearance` attribute to change the input's visual appearance.

```html
<wa-number-input label="Outlined" appearance="outlined" value="42" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Filled" appearance="filled" value="42" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Filled Outlined" appearance="filled-outlined" value="42" style="max-width: 260px;"></wa-number-input>
```

### Disabled

Use the `disabled` attribute to disable an input.

```html
<wa-number-input label="Disabled" value="100" disabled style="max-width: 260px;"></wa-number-input>
```

### Readonly

Use the `readonly` attribute to make the input readonly. The value can still be selected and copied, but it cannot be changed.

```html
<wa-number-input label="Readonly" value="42" readonly style="max-width: 260px;"></wa-number-input>
```

### Sizes

Use the `size` attribute to change an input's size.

```html
<wa-number-input label="Small" size="small" value="10" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Medium" size="medium" value="20" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Large" size="large" value="30" style="max-width: 260px;"></wa-number-input>
```

### Pill

Use the `pill` attribute to give inputs rounded edges.

```html
<wa-number-input label="Small Pill" size="small" pill value="10" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Medium Pill" size="medium" pill value="20" style="max-width: 260px;"></wa-number-input>
<br />
<wa-number-input label="Large Pill" size="large" pill value="30" style="max-width: 260px;"></wa-number-input>
```

### Without Steppers

Add the `without-steppers` attribute to remove the increment/decrement buttons. Users can still modify the value using the keyboard.

```html
<wa-number-input label="No steppers" value="50" without-steppers style="max-width: 260px;"></wa-number-input>
```

When steppers are hidden, users can still use the arrow keys to increment and decrement the value.

### Start & End Decorations

Use the `start` and `end` slots to add presentational elements like `<wa-icon>` within the input.

```html
<wa-number-input label="Price" value="100" style="max-width: 260px;">
  <wa-icon slot="start" name="dollar-sign" family="utility" variant="semibold"></wa-icon>
</wa-number-input>

<br />

<wa-number-input label="Weight (kg)" value="75" style="max-width: 260px;">
  <wa-icon slot="end" name="bag-shopping" family="utility" variant="semibold"></wa-icon>
</wa-number-input>
```

### Custom Stepper Icons

Use the `increment-icon` and `decrement-icon` slots to customize the stepper button icons.

```html
<wa-number-input label="Custom icons" value="5" style="max-width: 260px;">
  <wa-icon slot="increment-icon" name="plus" family="notdog-duo" variant="solid"></wa-icon>
  <wa-icon slot="decrement-icon" name="minus" family="notdog-duo" variant="solid"></wa-icon>
</wa-number-input>
```

### Customizing Label Position

Use [CSS parts](#css-parts) to customize the way form controls are drawn. This example uses CSS grid to position the label to the left of the control, but the possible orientations are nearly endless. The same technique works for inputs, textareas, radio groups, and similar form controls.

```html
<div class="label-on-left">
  <wa-number-input label="Quantity" hint="How many do you need?" value="1"></wa-number-input>
  <wa-number-input label="Price" hint="Cost per unit" value="25"></wa-number-input>
</div>

<style>
  .label-on-left {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: var(--wa-space-l);
    align-items: center;

    wa-number-input {
      grid-column: 1 / -1;
      grid-row-end: span 2;
      display: grid;
      grid-template-columns: subgrid;
      gap: 0 var(--wa-space-l);
      align-items: center;
    }

    ::part(label) {
      text-align: right;
    }

    ::part(hint) {
      grid-column: 2;
    }
  }
</style>
```

### Form Validation

Use the `required` attribute to make the field required. Combine with `min` and `max` for range validation.

```html
<form class="number-input-validation">
  <wa-number-input
    name="quantity"
    label="Quantity"
    hint="Enter a value between 1 and 10"
    min="1"
    max="10"
    required
    style="max-width: 260px;"
  ></wa-number-input>
  <br />
  <wa-number-input
    name="price"
    label="Price"
    hint="Must be a multiple of 0.25"
    min="0"
    step="0.25"
    required
    style="max-width: 260px;"
  ></wa-number-input>
  <br />
  <wa-button appearance="filled" type="submit" variant="brand">Submit</wa-button>
  <wa-button appearance="filled" type="reset" variant="neutral">Reset</wa-button>
</form>

<script type="module">
  const form = document.querySelector('.number-input-validation');

  form.addEventListener('submit', event => {
    event.preventDefault();

    // Log data to the console for the demo
    console.log(...new FormData(form));
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
import '@awesome.me/webawesome/dist/components/number-input/number-input.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaNumberInput from '@awesome.me/webawesome/dist/react/number-input';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`decrement-icon\` | An icon to use in lieu of the default decrement icon. |
| \`end\` | \`\` An element, such as , placed at the start of the input control. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'filled' \\| 'outlined' \\| 'filled-outlined'\` The input's visual appearance. Type Default 'outlined' | | |
| \`autocomplete\` autocomplete | \`string\` Specifies what permission the browser has to provide assistance in filling out form field values. Refer to this page on MDN for available values. Type | | |
| \`autofocus\` autofocus | \`boolean\` Indicates that the input should receive focus on page load. Type | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[sizeStyles, formControlStyles, styles\] | | |
| \`defaultValue\` value | \`string \\| null\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the form control. Type Default false | | |
| \`enterkeyhint\` enterkeyhint | \`'enter' \\| 'done' \\| 'go' \\| 'next' \\| 'previous' \\| 'search' \\| 'send'\` Used to customize the label or icon of the Enter key on virtual keyboards. Type | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`hint\` hint | \`hint\` The input's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`inputmode\` inputmode | \`'numeric' \\| 'decimal'\` Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual keyboard on supportive devices. Type Default 'numeric' | | |
| \`label\` label | \`label\` The input's . If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`max\` max | \`number\` The input's maximum value. Type | | |
| \`min\` min | \`number\` The input's minimum value. Type | | |
| \`name\` name | \`string \\| null\` The name of the input, submitted as a name/value pair with form data. Type Default null | | |
| \`pill\` pill | \`boolean\` Draws a pill-style input with rounded edges. Type Default false | | |
| \`placeholder\` placeholder | \`string\` Placeholder text to show as a hint when the input is empty. Type Default '' | | |
| \`readonly\` readonly | \`boolean\` Makes the input readonly. Type Default false | | |
| \`required\` required | \`boolean\` Makes the input a required field. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The input's size. Type Default 'medium' | | |
| \`step\` step | \`any\` Specifies the granularity that the value must adhere to, or the special value which means no stepping is implied, allowing any numeric value. Type number \\| 'any' Default 1 | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` | The current value of the input, submitted as a name/value pair with form data. | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |
| \`withoutSteppers\` without-steppers | \`boolean\` Hides the increment/decrement stepper buttons. Type Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the input. | |
| \`focus()\` | Sets focus on the input. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`select()\` | Selects all the text in the input. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |
| \`stepDown()\` | Decrements the value by the step amount. | |
| \`stepUp()\` | Increments the value by the step amount. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the control loses focus. |
| \`change\` | Emitted when an alteration to the control's value is committed by the user. |
| \`focus\` | Emitted when the control gains focus. |
| \`input\` | Emitted when the control receives input. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`blank\` | The input is empty. | \`:state(blank)\` |
| \`focused\` | The input has focus. | \`:state(focused)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The wrapper containing the input and steppers. | \`::part(base)\` |
| \`end\` | \`end\` The container that wraps the slot. | \`::part(end)\` |
| \`form-control-label\` | Alias for the label element. | \`::part(form-control-label)\` |
| \`hint\` | The hint element. | \`::part(hint)\` |
| \`input\` | \`\` The internal control. | \`::part(input)\` |
| \`label\` | The label element. | \`::part(label)\` |
| \`start\` | \`start\` The container that wraps the slot. | \`::part(start)\` |
| \`stepper\` | Both stepper buttons (for shared styling). | \`::part(stepper)\` |
| \`stepper-decrement\` | The decrement (-) button on the start side. | \`::part(stepper-decrement)\` |
| \`stepper-increment\` | The increment (+) button on the end side. | \`::part(stepper-increment)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help