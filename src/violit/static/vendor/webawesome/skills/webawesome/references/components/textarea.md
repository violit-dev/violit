# Textarea

**Full documentation:** https://webawesome.com/docs/components/textarea


`<wa-textarea>` Since 2.0 Stable

Textareas collect data from the user and allow multiple lines of text.

```html
<wa-textarea label="Type somethin', will ya"></wa-textarea>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Labels

Use the `label` attribute to give the textarea an accessible label. For labels that contain HTML, use the `label` slot instead.

```html
<wa-textarea label="Comments"></wa-textarea>
```

### Hint

Add descriptive hint to a textarea with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-textarea label="Feedback" hint="Please tell us what you think."> </wa-textarea>
```

### Rows

Use the `rows` attribute to change the number of text rows that get shown.

```html
<wa-textarea rows="2"></wa-textarea>
```

### Placeholders

Use the `placeholder` attribute to add a placeholder.

```html
<wa-textarea placeholder="Type something"></wa-textarea>
```

### Appearance

Use the `appearance` attribute to change the textarea's visual appearance.

```html
<wa-textarea placeholder="Type something" appearance="filled"></wa-textarea><br />
<wa-textarea placeholder="Type something" appearance="filled-outlined"></wa-textarea><br />
<wa-textarea placeholder="Type something" appearance="outlined"></wa-textarea>
```

### Disabled

Use the `disabled` attribute to disable a textarea.

```html
<wa-textarea placeholder="Textarea" disabled></wa-textarea>
```

### Value

Use the `value` attribute to set an initial value.

```html
<wa-textarea value="Write something awesome!"></wa-textarea>
```

### Sizes

Use the `size` attribute to change a textarea's size.

```html
<wa-textarea placeholder="Small" size="small"></wa-textarea>
<br />
<wa-textarea placeholder="Medium" size="medium"></wa-textarea>
<br />
<wa-textarea placeholder="Large" size="large"></wa-textarea>
```

### Prevent Resizing

By default, textareas can be resized vertically by the user. To prevent resizing, set the `resize` attribute to `none`.

```html
<wa-textarea resize="none"></wa-textarea>
```

### Expand with Content

Textareas will automatically resize to expand to fit their content when `resize` is set to `auto`.

```html
<wa-textarea resize="auto"></wa-textarea>
```

### Resize horizontal

Textareas can be made to resize horizontally when `resize` is set to `"horizontal"`

```html
<wa-textarea resize="horizontal"></wa-textarea>
```

### Resize both

Textareas can be made to resize both vertically and horizontally when `resize` is set to `"both"`

```html
<wa-textarea resize="both"></wa-textarea>
```

### Character Count

Add the `with-count` attribute to show a character count below the textarea. When combined with `maxlength`, the count shows remaining characters instead. The count is exposed to assistive technologies using a live region so screen readers can announce updates as the user types.

```html
<wa-textarea label="Comments" hint="Share your thoughts with us" with-count></wa-textarea>
<br />
<wa-textarea label="Bio" hint="Tell us a little about yourself" with-count maxlength="100"></wa-textarea>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/textarea/textarea.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaTextarea from '@awesome.me/webawesome/dist/react/textarea';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`hint\` | \`hint\` Text that describes how to use the input. Alternatively, you can use the attribute. |
| \`label\` | \`label\` The textarea's . Alternatively, you can use the label attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'filled' \\| 'outlined' \\| 'filled-outlined'\` The textarea's visual appearance. Type Default 'outlined' | | |
| \`autocapitalize\` autocapitalize | \`'off' \\| 'none' \\| 'on' \\| 'sentences' \\| 'words' \\| 'characters'\` Controls whether and how text input is automatically capitalized as it is entered by the user. Type | | |
| \`autocomplete\` autocomplete | \`string\` Specifies what permission the browser has to provide assistance in filling out form field values. Refer to this page on MDN for available values. Type | | |
| \`autocorrect\` autocorrect | \`"off"\` Indicates whether the browser's autocorrect feature is on or off. When set as an attribute, use or "on". When set as a property, use true or false. Type boolean | | |
| \`autofocus\` autofocus | \`boolean\` Indicates that the input should receive focus on page load. Type | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles, formControlStyles, sizeStyles, visuallyHidden\] | | |
| \`defaultValue\` value | \`string\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the textarea. Type Default false | | |
| \`enterkeyhint\` enterkeyhint | \`'enter' \\| 'done' \\| 'go' \\| 'next' \\| 'previous' \\| 'search' \\| 'send'\` Used to customize the label or icon of the Enter key on virtual keyboards. Type | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`hint\` hint | \`hint\` The textarea's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`inputmode\` inputmode | \`'none' \\| 'text' \\| 'decimal' \\| 'numeric' \\| 'tel' \\| 'search' \\| 'email' \\| 'url'\` Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual keyboard on supportive devices. Type | | |
| \`label\` label | \`label\` The textarea's . If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`maxlength\` maxlength | \`number\` The maximum length of input that will be considered valid. Type | | |
| \`minlength\` minlength | \`number\` The minimum length of input that will be considered valid. Type | | |
| \`name\` name | \`string \\| null\` The name of the textarea, submitted as a name/value pair with form data. Type Default null | | |
| \`placeholder\` placeholder | \`string\` Placeholder text to show as a hint when the input is empty. Type Default '' | | |
| \`readonly\` readonly | \`boolean\` Makes the textarea readonly. Type Default false | | |
| \`required\` required | \`boolean\` Makes the textarea a required field. Type Default false | | |
| \`resize\` resize | \`'none' \\| 'vertical' \\| 'horizontal' \\| 'both' \\| 'auto'\` Controls how the textarea can be resized. Type Default 'vertical' | | |
| \`rows\` rows | \`number\` The of rows to display by default. Type number Default 4 | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The textarea's size. Type Default 'medium' | | |
| \`spellcheck\` spellcheck | \`boolean\` Enables spell checking on the textarea. Type Default true | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` | The current value of the input, submitted as a name/value pair with form data. | | |
| \`withCount\` with-count | \`maxlength\` Shows a character count below the textarea. When is set, shows remaining characters instead. Type boolean Default false | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the textarea. | |
| \`focus()\` | Sets focus on the textarea. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`scrollPosition()\` | Gets or sets the textarea's scroll position. | \`position: { top?: number; left?: number }\` |
| \`select()\` | Selects all the text in the textarea. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |
| \`setRangeText()\` | Replaces a range of text with a new string. | \`replacement: string, start: number, end: number, selectMode: 'select' \\| 'start' \\| 'end' \\| 'preserve'\` |
| \`setSelectionRange()\` | Sets the start and end positions of the text selection (0-based). | \`selectionStart: number, selectionEnd: number, selectionDirection: 'forward' \\| 'backward' \\| 'none'\` |

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
| \`blank\` | The textarea is empty. | \`:state(blank)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | \`\` The wrapper around the control. | \`::part(base)\` |
| \`count\` | \`with-count\` The character count element, rendered when the attribute is present. | \`::part(count)\` |
| \`form-control-input\` | The input's wrapper. | \`::part(form-control-input)\` |
| \`hint\` | The hint's wrapper. | \`::part(hint)\` |
| \`label\` | The label | \`::part(label)\` |
| \`textarea\` | \`\` The internal control. | \`::part(textarea)\` |

**Need a hand?** Report a bug Ask for help