# Color Picker

**Full documentation:** https://webawesome.com/docs/components/color-picker


`<wa-color-picker>` Since 2.0 Stable

Color pickers allow the user to select a color.

```html
<wa-color-picker label="Select a color"></wa-color-picker>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Initial Value

Use the `value` attribute to set an initial value for the color picker.

```html
<wa-color-picker value="#4a90e2" label="Select a color"></wa-color-picker>
```

### Opacity

Use the `opacity` attribute to enable the opacity slider. When this is enabled, the value will be displayed as HEXA, RGBA, HSLA, or HSVA based on `format`.

```html
<wa-color-picker value="#f5a623ff" opacity label="Select a color"></wa-color-picker>
```

### Formats

Set the color picker's format with the `format` attribute. Valid options include `hex`, `rgb`, `hsl`, and `hsv`. Note that the color picker's input will accept any parsable format (including CSS color names) regardless of this option.

To prevent users from toggling the format themselves, add the `without-format-toggle` attribute.

```html
<div class="wa-grid" style="--min-column-size: 12ch;">
  <wa-color-picker format="hex" value="#4a90e2" label="Pick a hex color"></wa-color-picker>
  <wa-color-picker format="rgb" value="rgb(80, 227, 194)" label="Pick an RGB color"></wa-color-picker>
  <wa-color-picker format="hsl" value="hsl(290, 87%, 47%)" label="Pick an HSL color"></wa-color-picker>
  <wa-color-picker format="hsv" value="hsv(55, 89%, 97%)" label="Pick an HSV color"></wa-color-picker>
</div>
```

### Swatches

Use the `swatches` attribute to add convenient presets to the color picker. Any format the color picker can parse is acceptable (including [CSS color names](https://www.w3schools.com/colors/colors_names.asp)), but each value must be separated by a semicolon (`;`). Alternatively, you can pass an array of color values to this property using JavaScript.

```html
<wa-color-picker
  label="Select a color"
  swatches="
    #d0021b; #f5a623; #f8e71c; #8b572a; #7ed321; #417505; #bd10e0; #9013fe;
    #4a90e2; #50e3c2; #b8e986; #000; #444; #888; #ccc; #fff;
  "
></wa-color-picker>
```

You can also pass an array of objects with `color` and `label` properties using JavaScript. When labels are provided, they will be used as the accessible name for each swatch instead of the raw color value.

```html
<wa-color-picker id="labeled-swatches" label="Select a color"></wa-color-picker>

<script>
  const colorPicker = document.getElementById('labeled-swatches');
  colorPicker.swatches = [
    { color: '#d0021b', label: 'Red' },
    { color: '#f5a623', label: 'Orange' },
    { color: '#f8e71c', label: 'Yellow' },
    { color: '#7ed321', label: 'Green' },
    { color: '#4a90e2', label: 'Blue' },
    { color: '#bd10e0', label: 'Purple' },
    { color: '#000', label: 'Black' },
    { color: '#fff', label: 'White' }
  ];
</script>
```

### Placement

The preferred placement of the dropdown can be set with the `placement` attribute. Note that the actual position may vary to ensure the panel remains in the viewport.

```html
<div class="wa-gap-m wa-align-items-baseline">
  <wa-color-picker placement="top-start" label="Select a color"></wa-color-picker>
  <wa-color-picker placement="bottom-end" label="Select a color"></wa-color-picker>
  <wa-color-picker placement="right" label="Select a color"></wa-color-picker>
  <wa-color-picker placement="left" label="Select a color"></wa-color-picker>
</div>
```

### Sizes

Use the `size` attribute to change the color picker's trigger size.

```html
<div class="wa-gap-m wa-align-items-baseline">
  <wa-color-picker size="small" label="Select a color"></wa-color-picker>
  <wa-color-picker size="medium" label="Select a color"></wa-color-picker>
  <wa-color-picker size="large" label="Select a color"></wa-color-picker>
</div>
```

### Disabled

The color picker can be rendered as disabled.

```html
<wa-color-picker disabled label="Select a color"></wa-color-picker>
```

### Hint

Add descriptive hint to a color picker with the `hint` attribute. For hints that contain HTML, use the `hint` slot instead.

```html
<wa-color-picker label="Select a color" hint="Choose a color with appropriate contrast!"></wa-color-picker>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/color-picker/color-picker.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaColorPicker from '@awesome.me/webawesome/dist/react/color-picker';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`hint\` | \`hint\` The color picker's form . Alternatively, you can use the hint attribute. |
| \`label\` | \`label\` The color picker's form . Alternatively, you can use the label attribute. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[visuallyHidden, sizeStyles, formControlStyles, styles\] | | |
| \`defaultValue\` value | \`string \\| null\` The default value of the form control. Primarily used for resetting the form control. Type | | |
| \`disabled\` disabled | \`boolean\` Disables the color picker. Type Default false | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`format\` format | \`'hex' \\| 'rgb' \\| 'hsl' \\| 'hsv'\` The format to use. If opacity is enabled, these will translate to HEXA, RGBA, HSLA, and HSVA respectively. The color picker will accept user input in any format (including CSS color names) and convert it to the desired format. Type Default 'hex' | | |
| \`hint\` hint | \`hint\` The color picker's . If you need to display HTML, use the hint slot instead. Type string Default '' | | |
| \`label\` label | \`label\` The color picker's . This will not be displayed, but it will be announced by assistive devices. If you need to display HTML, you can use the label slot\` instead. Type string Default '' | | |
| \`name\` name | \`string \\| null\` The name of the form control, submitted as a name/value pair with form data. Type Default null | | |
| \`opacity\` opacity | \`boolean\` Shows the opacity slider. Enabling this will cause the formatted value to be HEXA, RGBA, or HSLA. Type Default false | | |
| \`open\` open | \`show()\` Indicates whether or not the popup is open. You can toggle this attribute to show and hide the popup, or you can use the and hide() methods and this attribute will reflect the popup's open state. Type boolean Default false | | |
| \`placement\` placement | \`'top' \\| 'top-start' \\| 'top-end' \\| 'bottom' \\| 'bottom-start' \\| 'bottom-end' \\| 'right' \\| 'right-start' \\| 'right-end' \\| 'left' \\| 'left-start' \\| 'left-end'\` The preferred placement of the color picker's popup. Note that the actual placement will vary as configured to keep the panel inside of the viewport. Type Default 'bottom-start' | | |
| \`required\` required | \`boolean\` Makes the color picker a required field. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` Determines the size of the color picker's trigger Type Default 'medium' | | |
| \`swatches\` swatches | \`;\` One or more predefined color swatches to display as presets in the color picker. Can include any format the color picker can parse, including HEX(A), RGB(A), HSL(A), HSV(A), and CSS color names. Each color must be separated by a semicolon (). Alternatively, you can pass an array of color values or an array of { color, label } objects to this property using JavaScript. When using objects with labels, the label will be used for the swatch's accessible name instead of the raw color value. Type string \\| string\[\] \\| WaColorPickerSwatch\[\] Default '' | | |
| \`uppercase\` uppercase | \`boolean\` By default, values are lowercase. With this attribute, values will be uppercase instead. Type Default false | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` | \`format\` The current value of the color picker. The value's will vary based the format attribute. To get the value in a specific format, use the getFormattedValue() method. The value is submitted as a name/value pair with form data. | | |
| \`withHint\` with-hint | \`true\` Only required for SSR. Set to if you're slotting in a hint element so the server-rendered markup includes the hint before the component hydrates on the client. Type boolean Default false | | |
| \`withLabel\` with-label | \`true\` Only required for SSR. Set to if you're slotting in a label element so the server-rendered markup includes the label before the component hydrates on the client. Type boolean Default false | | |
| \`withoutFormatToggle\` without-format-toggle | \`boolean\` Removes the button that lets users toggle between format. Type Default false | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`blur()\` | Removes focus from the color picker. | |
| \`focus()\` | Sets focus on the color picker. | \`options: FocusOptions\` |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`getFormattedValue()\` | Returns the current value as a string in the specified format. | \`format: 'hex' \\| 'hexa' \\| 'rgb' \\| 'rgba' \\| 'hsl' \\| 'hsla' \\| 'hsv' \\| 'hsva'\` |
| \`getHexString()\` | Generates a hex string from HSV values. Hue must be 0-360. All other arguments must be 0-100. | \`hue: number, saturation: number, brightness: number, alpha:\` |
| \`hide()\` | Hides the color picker panel | |
| \`reportValidity()\` | Checks for validity and shows the browser's validation message if the control is invalid. | |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |
| \`show()\` | Shows the color picker panel. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`blur\` | Emitted when the color picker loses focus. |
| \`change\` | Emitted when the color picker's value changes. |
| \`focus\` | Emitted when the color picker receives focus. |
| \`input\` | Emitted when the color picker receives input. |
| \`wa-after-hide\` | |
| \`wa-after-show\` | |
| \`wa-hide\` | |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |
| \`wa-show\` | |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--grid-handle-size\` | The size of the color grid's handle. |
| \`--grid-height\` | The height of the color grid. |
| \`--grid-width\` | The width of the color grid. |
| \`--slider-handle-size\` | The diameter of the slider's handle. |
| \`--slider-height\` | The height of the hue and alpha sliders. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |
| \`eyedropper-button\` | The eye dropper button. | \`::part(eyedropper-button)\` |
| \`eyedropper-button\_\_base\` | \`button\` The eye dropper 's exported button part. | \`::part(eyedropper-button\_\_base)\` |
| \`eyedropper-button\_\_caret\` | \`caret\` The eye dropper button's exported part. | \`::part(eyedropper-button\_\_caret)\` |
| \`eyedropper-button\_\_end\` | \`end\` The eye dropper button's exported part. | \`::part(eyedropper-button\_\_end)\` |
| \`eyedropper-button\_\_label\` | \`label\` The eye dropper button's exported part. | \`::part(eyedropper-button\_\_label)\` |
| \`eyedropper-button\_\_start\` | \`start\` The eye dropper button's exported part. | \`::part(eyedropper-button\_\_start)\` |
| \`format-button\` | The format button. | \`::part(format-button)\` |
| \`format-button\_\_base\` | \`button\` The format 's exported button part. | \`::part(format-button\_\_base)\` |
| \`format-button\_\_caret\` | \`caret\` The format button's exported part. | \`::part(format-button\_\_caret)\` |
| \`format-button\_\_end\` | \`end\` The format button's exported part. | \`::part(format-button\_\_end)\` |
| \`format-button\_\_label\` | \`label\` The format button's exported part. | \`::part(format-button\_\_label)\` |
| \`format-button\_\_start\` | \`start\` The format button's exported part. | \`::part(format-button\_\_start)\` |
| \`grid\` | The color grid. | \`::part(grid)\` |
| \`grid-handle\` | The color grid's handle. | \`::part(grid-handle)\` |
| \`hue-slider\` | The hue slider. | \`::part(hue-slider)\` |
| \`hue-slider-handle\` | The hue slider's handle. | \`::part(hue-slider-handle)\` |
| \`input\` | The text input. | \`::part(input)\` |
| \`opacity-slider\` | The opacity slider. | \`::part(opacity-slider)\` |
| \`opacity-slider-handle\` | The opacity slider's handle. | \`::part(opacity-slider-handle)\` |
| \`preview\` | The preview color. | \`::part(preview)\` |
| \`slider\` | Hue and opacity sliders. | \`::part(slider)\` |
| \`slider-handle\` | Hue and opacity slider handles. | \`::part(slider-handle)\` |
| \`swatch\` | Each individual swatch. | \`::part(swatch)\` |
| \`swatches\` | The container that holds the swatches. | \`::part(swatches)\` |
| \`trigger\` | The color picker's dropdown trigger. | \`::part(trigger)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-button-group>`](https://webawesome.com/docs/components/button-group)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-input>`](https://webawesome.com/docs/components/input)
-   [`<wa-popup>`](https://webawesome.com/docs/components/popup)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)
-   [`<wa-visually-hidden>`](https://webawesome.com/docs/components/visually-hidden)

**Need a hand?** Report a bug Ask for help