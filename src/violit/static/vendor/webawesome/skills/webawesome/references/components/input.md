# Input

**Full documentation:** https://webawesome.com/docs/components/input


`<wa-input>` Since 2.0 Stable

Inputs collect data from the user.

```html
<wa-input></wa-input>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Labels

Use the `label` attribute to give the input an accessible label. For labels that contain HTML, use the `label` slot instead.

```html
<wa-input label="What is your name?"></wa-input>
```

### Hint

Add descriptive hint to an input with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-input label="Nickname" hint="What would you like people to call you?"></wa-input>
```

### Placeholders

Use the `placeholder` attribute to add a placeholder.

```html
<wa-input placeholder="Type something"></wa-input>
```

### Clearable

Add the `with-clear` attribute to add a clear button when the input has content.

```html
<wa-input placeholder="Clearable" with-clear></wa-input>
```

### Toggle Password

Add the `password-toggle` attribute to add a toggle button that will show the password when activated.

```html
<wa-input type="password" placeholder="Password Toggle" password-toggle></wa-input>
```

### Appearance

Use the `appearance` attribute to change the input's visual appearance.

```html
<wa-input placeholder="Type something" appearance="filled"></wa-input><br />
<wa-input placeholder="Type something" appearance="filled-outlined"></wa-input><br />
<wa-input placeholder="Type something" appearance="outlined"></wa-input>
```

### Disabled

Use the `disabled` attribute to disable an input.

```html
<wa-input placeholder="Disabled" disabled></wa-input>
```

### Sizes

Use the `size` attribute to change an input's size.

```html
<wa-input placeholder="Small" size="small"></wa-input>
<br />
<wa-input placeholder="Medium" size="medium"></wa-input>
<br />
<wa-input placeholder="Large" size="large"></wa-input>
```

### Pill

Use the `pill` attribute to give inputs rounded edges.

```html
<wa-input placeholder="Small" size="small" pill></wa-input>
<br />
<wa-input placeholder="Medium" size="medium" pill></wa-input>
<br />
<wa-input placeholder="Large" size="large" pill></wa-input>
```

### Input Types

The `type` attribute controls the type of input the browser renders.

```html
<wa-input type="email" placeholder="Email"></wa-input>
<br />
<wa-input type="number" placeholder="Number"></wa-input>
<br />
<wa-input type="date" placeholder="Date"></wa-input>
```

### Start & End Decorations

Use the `start` and `end` slots to add presentational elements like `<wa-icon>` within the input.

```html
<wa-input placeholder="Small" size="small">
  <wa-icon name="house" slot="start"></wa-icon>
  <wa-icon name="comment" slot="end"></wa-icon>
</wa-input>
<br />
<wa-input placeholder="Medium" size="medium">
  <wa-icon name="house" slot="start"></wa-icon>
  <wa-icon name="comment" slot="end"></wa-icon>
</wa-input>
<br />
<wa-input placeholder="Large" size="large">
  <wa-icon name="house" slot="start"></wa-icon>
  <wa-icon name="comment" slot="end"></wa-icon>
</wa-input>
```

### Customizing Label Position

Use [CSS parts](#css-parts) to customize the way form controls are drawn. This example uses CSS grid to position the label to the left of the control, but the possible orientations are nearly endless. The same technique works for inputs, textareas, radio groups, and similar form controls.

```html
<div class="label-on-left">
  <wa-input label="Name" hint="Enter your name"></wa-input>
  <wa-input label="Email" type="email" hint="Enter your email"></wa-input>
  <wa-textarea label="Bio" hint="Tell us something about yourself"></wa-textarea>
</div>

<style>
  .label-on-left {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: var(--wa-space-l);
    align-items: center;

    wa-input,
    wa-textarea {
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

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/input/input.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaInput from '@awesome.me/webawesome/dist/react/input';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`clear-icon\` | An icon to use in lieu of the default clear icon. |
| \`end\` | \`\` An element, such as , placed at the start of the input control. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'filled' \\| 'outlined' \\| 'filled-outlined'\` The input's visual appearance. Type Default 'outlined' | | |
| \`autocapitalize\` autocapitalize | \`'off' \\| 'none' \\| 'on' \\| 'sentences' \\| 'words' \\| 'characters'\` Controls whether and how text input is automatically capitalized as it is entered by the user. Type | | |
| \`autocomplete\` autocomplete | \`string\` Specifies what permission the browser has to provide assistance in filling out form field values. Refer to this page on MDN for available values. Type | | |
| \`autocorrect\` autocorrect | \`"off"\` Indicates whether the browser's autocorrect feature is on or off. When set as an attribute, use or "on". When set as a property, use true or false. Type boolean | | |
| \`autofocus\` autofocus | \`boolean\` Indicates that the input should receive focus on page load. Type | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[sizeStyles, formControlStyles, styles\] | | |
| \`defaultValue\` value | \`string \\| null\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the form control. Type Default false | | |
| \`enterkeyhint\` enterkeyhint | \`'enter' \\| 'done' \\| 'go' \\| 'next' \\| 'previous' \\| 'search' \\| 'send'\` Used to customize the label or icon of the Enter key on virtual keyboards. Type | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`hint\` hint | \`hint\` The input's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`inputmode\` inputmode | \`'none' \\| 'text' \\| 'decimal' \\| 'numeric' \\| 'tel' \\| 'search' \\| 'email' \\| 'url'\` Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual keyboard on supportive devices. Type | | |
| \`label\` label | \`label\` The input's . If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`max\` max | \`number \\| string\` The input's maximum value. Only applies to date and number input types. Type | | |
| \`maxlength\` maxlength | \`number\` The maximum length of input that will be considered valid. Type | | |
| \`min\` min | \`number \\| string\` The input's minimum value. Only applies to date and number input types. Type | | |
| \`minlength\` minlength | \`number\` The minimum length of input that will be considered valid. Type | | |
| \`name\` name | \`string \\| null\` The name of the input, submitted as a name/value pair with form data. Type Default null | | |
| \`passwordToggle\` password-toggle | \`boolean\` Adds a button to toggle the password's visibility. Only applies to password types. Type Default false | | |
| \`passwordVisible\` password-visible | \`boolean\` Determines whether or not the password is currently visible. Only applies to password input types. Type Default false | | |
| \`pattern\` pattern | \`string\` A regular expression pattern to validate input against. Type | | |
| \`pill\` pill | \`boolean\` Draws a pill-style input with rounded edges. Type Default false | | |
| \`placeholder\` placeholder | \`string\` Placeholder text to show as a hint when the input is empty. Type Default '' | | |
| \`readonly\` readonly | \`boolean\` Makes the input readonly. Type Default false | | |
| \`required\` required | \`boolean\` Makes the input a required field. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The input's size. Type Default 'medium' | | |
| \`spellcheck\` spellcheck | \`boolean\` Enables spell checking on the input. Type Default true | | |
| \`step\` step | \`any\` Specifies the granularity that the value must adhere to, or the special value which means no stepping is implied, allowing any numeric value. Only applies to date and number input types. Type number \\| 'any' | | |
| \`type\` type | \`\` The type of input. Works the same as a native element, but only a subset of types are supported. Defaults to text. Type 'date' \\| 'datetime-local' \\| 'email' \\| 'number' \\| 'password' \\| 'search' \\| 'tel' \\| 'text' \\| 'time' \\| 'url' Default 'text' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` | The current value of the input, submitted as a name/value pair with form data. | | |
| \`withClear\` with-clear | \`boolean\` Adds a clear button when the input is not empty. Type Default false | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |
| \`withoutSpinButtons\` without-spin-buttons | \`boolean\` Hides the browser's built-in increment/decrement spin buttons for number inputs. Type Default false | | |

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
| \`setRangeText()\` | Replaces a range of text with a new string. | \`replacement: string, start: number, end: number, selectMode: 'select' \\| 'start' \\| 'end' \\| 'preserve'\` |
| \`setSelectionRange()\` | Sets the start and end positions of the text selection (0-based). | \`selectionStart: number, selectionEnd: number, selectionDirection: 'forward' \\| 'backward' \\| 'none'\` |
| \`showPicker()\` | Displays the browser picker for an input element (only works if the browser supports it for the input type). | |
| \`stepDown()\` | Decrements the value of a numeric input type by the value of the step attribute. | |
| \`stepUp()\` | Increments the value of a numeric input type by the value of the step attribute. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the control loses focus. |
| \`change\` | Emitted when an alteration to the control's value is committed by the user. |
| \`focus\` | Emitted when the control gains focus. |
| \`input\` | Emitted when the control receives input. |
| \`wa-clear\` | Emitted when the clear button is activated. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`blank\` | The input is empty. | \`:state(blank)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The wrapper being rendered as an input | \`::part(base)\` |
| \`clear-button\` | The clear button. | \`::part(clear-button)\` |
| \`end\` | \`end\` The container that wraps the slot. | \`::part(end)\` |
| \`hint\` | The hint's wrapper. | \`::part(hint)\` |
| \`input\` | \`\` The internal control. | \`::part(input)\` |
| \`label\` | The label | \`::part(label)\` |
| \`password-toggle-button\` | The password toggle button. | \`::part(password-toggle-button)\` |
| \`start\` | \`start\` The container that wraps the slot. | \`::part(start)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help