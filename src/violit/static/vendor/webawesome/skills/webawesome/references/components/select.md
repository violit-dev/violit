# Select

**Full documentation:** https://webawesome.com/docs/components/select


`<wa-select>` Since 2.0 Stable

Selects allow you to choose items from a menu of predefined options.

```html
<wa-select>
  <wa-option value="">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
  <wa-option value="option-4">Option 4</wa-option>
  <wa-option value="option-5">Option 5</wa-option>
  <wa-option value="option-6">Option 6</wa-option>
</wa-select>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Labels

Use the `label` attribute to give the select an accessible label. For labels that contain HTML, use the `label` slot instead.

```html
<wa-select label="Select one">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Hint

Add descriptive hint to a select with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-select label="Experience" hint="Please tell us your skill level.">
  <wa-option value="1">Novice</wa-option>
  <wa-option value="2">Intermediate</wa-option>
  <wa-option value="3">Advanced</wa-option>
</wa-select>
```

### Placeholders

Use the `placeholder` attribute to add a placeholder.

```html
<wa-select placeholder="Select one">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Clearable

Use the `with-clear` attribute to make the control clearable. The clear button only appears when an option is selected.

```html
<wa-select with-clear value="option-1">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Appearance

Use the `appearance` attribute to change the select's visual appearance.

```html
<wa-select appearance="filled">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
<br />
<wa-select appearance="filled-outlined">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
<br />
<wa-select appearance="outlined">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Pill

Use the `pill` attribute to give selects rounded edges.

```html
<wa-select pill>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Disabled

Use the `disabled` attribute to disable a select.

```html
<wa-select placeholder="Disabled" disabled>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Multiple

To allow multiple options to be selected, use the `multiple` attribute. It's a good practice to use `with-clear` when this option is enabled. You can select multiple options by adding the `selected` attribute to individual options.

```html
<wa-select label="Select a Few" multiple with-clear>
  <wa-option value="option-1" selected>Option 1</wa-option>
  <wa-option value="option-2" selected>Option 2</wa-option>
  <wa-option value="option-3" selected>Option 3</wa-option>
  <wa-option value="option-4">Option 4</wa-option>
  <wa-option value="option-5">Option 5</wa-option>
  <wa-option value="option-6">Option 6</wa-option>
</wa-select>
```

Selecting multiple options may result in wrapping, causing the control to expand vertically. You can use the `max-options-visible` attribute to control the maximum number of selected options to show at once.

### Setting Initial Values

Use the `selected` attribute on individual options to set the initial selection, similar to native HTML.

```html
<wa-select>
  <wa-option value="option-1" selected>Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
  <wa-option value="option-4">Option 4</wa-option>
</wa-select>
```

For multiple selections, apply it to all selected options.

```html
<wa-select multiple with-clear>
  <wa-option value="option-1" selected>Option 1</wa-option>
  <wa-option value="option-2" selected>Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
  <wa-option value="option-4">Option 4</wa-option>
</wa-select>
```

Framework users can bind directly to the `value` property for reactive data binding and form state management.

### Grouping Options

Use `<wa-divider>` to group listbox items visually. You can also use `<small>` to provide labels, but they won't be announced by most assistive devices.

```html
<wa-select>
  <small>Section 1</small>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
  <wa-divider></wa-divider>
  <small>Section 2</small>
  <wa-option value="option-4">Option 4</wa-option>
  <wa-option value="option-5">Option 5</wa-option>
  <wa-option value="option-6">Option 6</wa-option>
</wa-select>
```

### Sizes

Use the `size` attribute to change a select's size.

```html
<wa-select placeholder="Small" size="small">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>

<br />

<wa-select placeholder="Medium" size="medium">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>

<br />

<wa-select placeholder="Large" size="large">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Placement

The preferred placement of the select's listbox can be set with the `placement` attribute. Note that the actual position may vary to ensure the panel remains in the viewport. Valid placements are `top` and `bottom`.

```html
<wa-select placement="top">
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Start & End Decorations

Use the `start` and `end` slots to add presentational elements like `<wa-icon>` within the combobox.

```html
<wa-select placeholder="Small" size="small" with-clear>
  <wa-icon slot="start" name="house" variant="solid"></wa-icon>
  <wa-icon slot="end" name="flag-checkered"></wa-icon>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
<br />
<wa-select placeholder="Medium" size="medium" with-clear>
  <wa-icon slot="start" name="house" variant="solid"></wa-icon>
  <wa-icon slot="end" name="flag-checkered"></wa-icon>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
<br />
<wa-select placeholder="Large" size="large" with-clear>
  <wa-icon slot="start" name="house" variant="solid"></wa-icon>
  <wa-icon slot="end" name="flag-checkered"></wa-icon>
  <wa-option value="option-1">Option 1</wa-option>
  <wa-option value="option-2">Option 2</wa-option>
  <wa-option value="option-3">Option 3</wa-option>
</wa-select>
```

### Custom Tags

When multiple options can be selected, you can provide custom tags by passing a function to the `getTag` property. Your function can return a string of HTML, a [Lit Template](https://lit.dev/docs/templates/overview/), or an [`HTMLElement`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement). The `getTag()` function will be called for each option. The first argument is an `<wa-option>` element and the second argument is the tag's index (its position in the tag list).

Remember that custom tags are rendered in a shadow root. To style them, you can use the `style` attribute in your template or you can add your own [parts](https://webawesome.com/docs/customizing/#css-parts) and target them with the [`::part()`](https://developer.mozilla.org/en-US/docs/Web/CSS/::part) selector.

```html
<wa-select placeholder="Select one" multiple with-clear class="custom-tag">
  <wa-option value="email" selected>
    <wa-icon slot="start" name="envelope" variant="solid"></wa-icon>
    Email
  </wa-option>
  <wa-option value="phone" selected>
    <wa-icon slot="start" name="phone" variant="solid"></wa-icon>
    Phone
  </wa-option>
  <wa-option value="chat">
    <wa-icon slot="start" name="comment" variant="solid"></wa-icon>
    Chat
  </wa-option>
</wa-select>

<script type="module">
  await customElements.whenDefined('wa-select');
  const select = document.querySelector('.custom-tag');
  await select.updateComplete;

  select.getTag = (option, index) => {
    // Use the same icon used in wa-option
    const name = option.querySelector('wa-icon[slot="start"]').name;

    // You can return a string, a Lit Template, or an HTMLElement here
    // Important: include data-value so the tag can be removed properly!
    return `
      <wa-tag with-remove data-value="${option.value}">
        <wa-icon name="${name}"></wa-icon>
        ${option.label}
      </wa-tag>
    `;
  };
</script>
```

Be sure you trust the content you are outputting! Passing unsanitized user input to `getTag()` can result in XSS vulnerabilities.

When using custom tags with `with-remove`, you must include the `data-value` attribute set to the option's value. This allows the select to identify which option to deselect when the tag's remove button is clicked.

### Lazy loading options

Lazy loading options works similarly to native `<select>` elements. The select component handles various scenarios intelligently:

#### Basic lazy loading scenarios:

-   **Empty select with value**: If a `<wa-select>` is created without any options but given a `value` attribute, its value will be `""` initially. When options are added later, if any option has a value matching the select's value attribute, the select's value will update to match.
    
-   **Multiple select with partial options**: If a `<wa-select multiple>` has an initial value with multiple options, but only some options are present in the DOM, it will respect only the available options. When additional selected options are loaded later (and the user hasn't changed the selection), those options will be automatically added to the selection.
    

Here's a comprehensive example showing different lazy loading scenarios:

```html
<form id="lazy-options-example">
  <div>
    <wa-select name="select-1" value="foo" label="Single select (with existing options)">
      <wa-option value="bar">Bar</wa-option>
      <wa-option value="baz">Baz</wa-option>
    </wa-select>
    <br />
    <wa-button appearance="filled" type="button">Add "foo" option</wa-button>
  </div>

  <br />

  <div>
    <wa-select name="select-2" value="foo" label="Single select (with no existing options)"> </wa-select>
    <br />
    <wa-button appearance="filled" type="button">Add "foo" option</wa-button>
  </div>

  <br />

  <div>
    <wa-select name="select-3" multiple label="Multiple Select (with existing selected options)">
      <wa-option value="bar" selected>Bar</wa-option>
      <wa-option value="baz" selected>Baz</wa-option>
    </wa-select>
    <br />
    <wa-button appearance="filled" type="button">Add "foo" option (selected)</wa-button>
  </div>

  <br />

  <div>
    <wa-select name="select-4" value="foo" multiple label="Multiple Select (with no existing options)"> </wa-select>
    <br />
    <wa-button appearance="filled" type="button">Add "foo" option</wa-button>
  </div>

  <br /><br />

  <div style="display: flex; gap: 16px;">
    <wa-button appearance="filled" type="reset">Reset</wa-button>
    <wa-button appearance="filled" type="submit" variant="brand">Show FormData</wa-button>
  </div>

  <br />

  <pre hidden><code id="lazy-options-example-form-data"></code></pre>

  <br />
</form>

<script type="module">
  function addFooOption(e) {
    const addFooButton = e.target.closest("wa-button[type='button']");
    if (!addFooButton) {
      return;
    }
    const select = addFooButton.parentElement.querySelector('wa-select');

    if (select.querySelector("wa-option[value='foo']")) {
      // Foo already exists. no-op.
      return;
    }

    const option = document.createElement('wa-option');
    option.setAttribute('value', 'foo');
    option.selected = true;
    option.innerText = 'Foo';

    // For the multiple select with existing selected options, make the new option selected
    if (select.getAttribute('name') === 'select-3') {
      option.selected = true;
    }

    select.append(option);
  }

  function handleLazySubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const codeElement = document.querySelector('#lazy-options-example-form-data');

    const obj = {};
    for (const key of formData.keys()) {
      const val = formData.getAll(key).length > 1 ? formData.getAll(key) : formData.get(key);
      obj[key] = val;
    }

    codeElement.textContent = JSON.stringify(obj, null, 2);

    const preElement = codeElement.parentElement;
    preElement.removeAttribute('hidden');
  }

  const container = document.querySelector('#lazy-options-example');
  container.addEventListener('click', addFooOption);
  container.addEventListener('submit', handleLazySubmit);
</script>
```

The key principle is that the select component prioritizes user interactions and explicit selections over programmatic changes, ensuring a predictable user experience even with dynamically loaded content.

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/select/select.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaSelect from '@awesome.me/webawesome/dist/react/select';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | \`\` The listbox options. Must be elements. You can use to group items visually. |
| \`clear-icon\` | An icon to use in lieu of the default clear icon. |
| \`end\` | \`\` An element, such as , placed at the start of the combobox. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`appearance\` appearance | \`'filled' \\| 'outlined' \\| 'filled-outlined'\` The select's visual appearance. Type Default 'outlined' | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[styles, formControlStyles, sizeStyles\] | | |
| \`disabled\` disabled | \`boolean\` Disables the select control. Type Default false | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`getTag\` | \`(option: WaOption, index: number) => TemplateResult \\| string \\| HTMLElement\` A function that customizes the tags to be rendered when multiple=true. The first argument is the option, the second is the current tag's index. The function should return either a Lit TemplateResult or a string containing trusted HTML of the symbol to render at the specified value. Type | | |
| \`hint\` hint | \`hint\` The select's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`label\` label | \`label\` The select's . If you need to display HTML, use the label slot instead. Type string Default '' | | |
| \`maxOptionsVisible\` max-options-visible | \`multiple\` The maximum number of selected options to show when is true. After the maximum, "+n" will be shown to indicate the number of additional items that are selected. Set to 0 to remove the limit. Type number Default 3 | | |
| \`multiple\` multiple | \`boolean\` Allows more than one option to be selected. Type Default false | | |
| \`name\` name | \`string \\| null\` The name of the select, submitted as a name/value pair with form data. Type Default '' | | |
| \`open\` open | \`show()\` Indicates whether or not the select is open. You can toggle this attribute to show and hide the menu, or you can use the and hide() methods and this attribute will reflect the select's open state. Type boolean Default false | | |
| \`pill\` pill | \`boolean\` Draws a pill-style select with rounded edges. Type Default false | | |
| \`placeholder\` placeholder | \`string\` Placeholder text to show as a hint when the select is empty. Type Default '' | | |
| \`placement\` placement | \`'top' \\| 'bottom'\` The preferred placement of the select's menu. Note that the actual placement may vary as needed to keep the listbox inside of the viewport. Type Default 'bottom' | | |
| \`required\` required | \`boolean\` The select's required attribute. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The select's size. Type Default 'medium' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Where to anchor native constraint validation Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` value | The select's value. This will be a string for single select or an array for multi-select. | | |
| \`withClear\` with-clear | \`boolean\` Adds a clear button when the select is not empty. Type Default false | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the control. | |
| \`focus()\` | Sets focus on the control. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`hide()\` | Hides the listbox. | |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |
| \`show()\` | Shows the listbox. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the control loses focus. |
| \`change\` | Emitted when the control's value changes. |
| \`focus\` | Emitted when the control gains focus. |
| \`input\` | Emitted when the control receives input. |
| \`wa-after-hide\` | Emitted after the select's menu closes and all animations are complete. |
| \`wa-after-show\` | Emitted after the select's menu opens and all animations are complete. |
| \`wa-clear\` | Emitted when the control's value is cleared. |
| \`wa-hide\` | Emitted when the select's menu closes. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |
| \`wa-show\` | Emitted when the select's menu opens. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--hide-duration\` | \`100ms\` The duration of the hide animation. Default |
| \`--show-duration\` | \`100ms\` The duration of the show animation. Default |
| \`--tag-max-size\` | \`multiple\` When using , the max size of tags before their content is truncated. Default 10ch |

## Custom States

Learn more about [custom states](https://webawesome.com/docs/customizing/#custom-states).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`blank\` | The select is empty. | \`:state(blank)\` |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`clear-button\` | The clear button. | \`::part(clear-button)\` |
| \`combobox\` | The container the wraps the start, end, value, clear icon, and expand button. | \`::part(combobox)\` |
| \`display-input\` | \`\` The element that displays the selected option's label, an element. | \`::part(display-input)\` |
| \`end\` | \`end\` The container that wraps the slot. | \`::part(end)\` |
| \`expand-icon\` | The container that wraps the expand icon. | \`::part(expand-icon)\` |
| \`form-control\` | The form control that wraps the label, input, and hint. | \`::part(form-control)\` |
| \`form-control-input\` | The select's wrapper. | \`::part(form-control-input)\` |
| \`form-control-label\` | The label's wrapper. | \`::part(form-control-label)\` |
| \`hint\` | The hint's wrapper. | \`::part(hint)\` |
| \`listbox\` | The listbox container where options are slotted. | \`::part(listbox)\` |
| \`start\` | \`start\` The container that wraps the slot. | \`::part(start)\` |
| \`tag\` | The individual tags that represent each multiselect option. | \`::part(tag)\` |
| \`tag\_\_content\` | The tag's content part. | \`::part(tag\_\_content)\` |
| \`tag\_\_remove-button\` | The tag's remove button. | \`::part(tag\_\_remove-button)\` |
| \`tag\_\_remove-button\_\_base\` | The tag's remove button base part. | \`::part(tag\_\_remove-button\_\_base)\` |
| \`tags\` | \`multiselect\` The container that houses option tags when is used. | \`::part(tags)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-option>`](https://webawesome.com/docs/components/option)
-   [`<wa-popup>`](https://webawesome.com/docs/components/popup)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)
-   [`<wa-tag>`](https://webawesome.com/docs/components/tag)

**Need a hand?** Report a bug Ask for help