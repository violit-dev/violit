# Rating

**Full documentation:** https://webawesome.com/docs/components/rating


`<wa-rating>` Since 2.0 Stable

Ratings give users a way to quickly view and provide feedback.

```html
<wa-rating label="Rating"></wa-rating>
```

This component works with standard `<form>` elements. Please refer to the section on [form controls](https://webawesome.com/docs/form-controls) to learn more about form submission and client-side validation.

## Examples

### Labels

Ratings are commonly identified contextually, so labels aren't displayed. However, you should always provide one for assistive devices using the `label` attribute.

```html
<wa-rating label="Rate this component"></wa-rating>
```

### Maximum Value

Ratings are 0-5 by default. To change the maximum possible value, use the `max` attribute.

```html
<wa-rating label="Rating" max="3"></wa-rating>
```

### Precision

Use the `precision` attribute to let users select fractional ratings.

```html
<wa-rating label="Rating" precision="0.5" value="2.5"></wa-rating>
```

### Sizing

Use the `size` attribute to adjust the size of the rating.

```html
<wa-rating label="Rating" size="small"></wa-rating><br />
<wa-rating label="Rating" size="medium"></wa-rating><br />
<wa-rating label="Rating" size="large"></wa-rating>
```

For more granular sizing, you can use the `font-size` property.

```html
<wa-rating label="Rating" style="font-size: 2rem;"></wa-rating>
```

### Readonly

Use the `readonly` attribute to display a rating that users can't change.

```html
<wa-rating label="Rating" readonly value="3"></wa-rating>
```

### Disabled

Use the `disabled` attribute to disable the rating.

```html
<wa-rating label="Rating" disabled value="3"></wa-rating>
```

### Detecting Hover

Use the `wa-hover` event to detect when the user hovers over (or touch and drag) the rating. This lets you hook into values as the user interacts with the rating, but before they select a value.

The event has a payload with `phase` and `value` properties. The `phase` property tells when hovering starts, moves to a new value, and ends. The `value` property tells what the rating's value would be if the user were to commit to the hovered value.

```html
<div class="detect-hover">
  <wa-rating label="Rating"></wa-rating>
  <span></span>
</div>

<script>
  const rating = document.querySelector('.detect-hover > wa-rating');
  const span = rating.nextElementSibling;
  const terms = ['No rating', 'Terrible', 'Bad', 'OK', 'Good', 'Excellent'];

  rating.addEventListener('wa-hover', event => {
    span.textContent = terms[event.detail.value];

    // Clear feedback when hovering stops
    if (event.detail.phase === 'end') {
      span.textContent = '';
    }
  });
</script>

<style>
  .detect-hover span {
    position: relative;
    top: -4px;
    left: 8px;
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-neutral-fill-loud);
    color: var(--wa-color-neutral-on-loud);
    text-align: center;
    padding: 4px 6px;
  }

  .detect-hover span:empty {
    display: none;
  }
</style>
```

### Custom Icons

You can provide custom icons by passing a function to the `getSymbol` property.

```html
<wa-rating label="Rating" class="rating-hearts" style="--symbol-color-active: #ff4136;"></wa-rating>

<script type="module">
  const rating = document.querySelector('.rating-hearts');

  await customElements.whenDefined('wa-rating');
  await rating.updateComplete;

  rating.getSymbol = () => '<wa-icon name="heart" variant="solid"></wa-icon>';
</script>
```

### Value-based Icons

You can also use the `getSymbol` property to render different icons based on value and/or whether the icon is currently selected.

```html
<wa-rating label="Rating" class="rating-emojis"></wa-rating>

<script type="module">
  const rating = document.querySelector('.rating-emojis');

  await customElements.whenDefined('wa-rating');
  await rating.updateComplete;

  rating.getSymbol = (value, isSelected) => {
    const icons = ['face-angry', 'face-frown', 'face-meh', 'face-smile', 'face-laugh'];
    return `<wa-icon name="${icons[value - 1]}"></wa-icon>`;
  };
</script>
```

### Required

Use the `required` attribute to make the rating mandatory. The form will not submit if the user hasn't selected a value.

```html
<form class="rating-required">
  <wa-rating label="Rating" required></wa-rating>
  <br /><br />
  <wa-button appearance="filled" type="submit">Submit</wa-button>
</form>

<script type="module">
  const form = document.querySelector('.rating-required');

  await Promise.all([
    customElements.whenDefined('wa-button'),
    customElements.whenDefined('wa-rating'),
  ]).then(() => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      alert('All fields are valid!');
    });
  });
</script>
```

### Custom Validity

Use the `setCustomValidity()` method to set a custom validation message. This will prevent the form from submitting and make the browser display the error message you provide. To clear the error, call this function with an empty string.

```html
<form class="rating-custom-validity">
  <wa-rating label="Rating"></wa-rating>
  <br /><br />
  <wa-button appearance="filled" type="submit">Submit</wa-button>
</form>

<script type="module">
  const form = document.querySelector('.rating-custom-validity');
  const rating = form.querySelector('wa-rating');
  const errorMessage = 'Please rate at least 3 stars!';

  customElements.whenDefined('wa-rating').then(async () => {
    await rating.updateComplete;
    rating.setCustomValidity(errorMessage);
  });

  rating.addEventListener('change', () => {
    rating.setCustomValidity(rating.value >= 3 ? '' : errorMessage);
  });

  await Promise.all([
    customElements.whenDefined('wa-button'),
    customElements.whenDefined('wa-rating'),
  ]).then(() => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      alert('All fields are valid!');
    });
  });
</script>
```

### Form Submission

Ratings can be used in forms just like native form controls. The rating's `name` and `value` will be included in the form data when submitted.

```html
<form class="rating-form-submission" action="about:blank" method="get" target="_blank">
  <label style="display: block; margin-bottom: 0.5rem;">How would you rate your experience?</label>
  <wa-rating name="rating" label="Rating" required></wa-rating>
  <br /><br />
  <wa-button type="submit">Submit</wa-button>
  <wa-button appearance="filled" type="reset" variant="neutral">Reset</wa-button>
</form>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/rating/rating.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaRating from '@awesome.me/webawesome/dist/react/rating';
```

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default \[sizeStyles, styles\] | | |
| \`defaultValue\` default-value | \`number\` The default value of the form control. Used to reset the rating to its initial value. Type Default 0 | | |
| \`disabled\` disabled | \`boolean\` Disables the rating. Type Default false | | |
| \`form\` | \`

\` By default, form controls are associated with the nearest containing element. This attribute allows you to place the form control outside of a form and associate it with the form that has this id. The form must be in the same document or shadow root for this to work. Type HTMLFormElement \\| null | | |
| \`getSymbol\` getSymbol | \`\` A function that customizes the symbol to be rendered. The first and only argument is the rating's current value. The function should return a string containing trusted HTML of the symbol to render at the specified value. Works well with elements. Type (value: number, isSelected: boolean) => string | | |
| \`label\` label | \`string\` A label that describes the rating to assistive devices. Type Default '' | | |
| \`max\` max | \`number\` The highest rating to show. Type Default 5 | | |
| \`name\` name | \`string \\| null\` The name of the rating, submitted as a name/value pair with form data. Type Default null | | |
| \`precision\` precision | \`0.5\` The precision at which the rating will increase and decrease. For example, to allow half-star ratings, set this attribute to . Type number Default 1 | | |
| \`readonly\` readonly | \`boolean\` Makes the rating readonly. Type Default false | | |
| \`required\` required | \`boolean\` Makes the rating a required field. Type Default false | | |
| \`size\` size | \`'small' \\| 'medium' \\| 'large'\` The component's size. Type Default 'medium' | | |
| \`validationTarget\` | \`undefined \\| HTMLElement\` Override this to change where constraint validation popups are anchored. Type | | |
| \`validators\` | \`observedAttributes\` Validators are static because they have , essentially attributes to "watch" for changes. Whenever these attributes change, we want to be notified and update the validator. Type Validator\[\] Default \[\] | | |
| \`value\` value | \`number\` The current rating. Type Default 0 | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`formStateRestoreCallback()\` | Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue. | \`state: string \\| File \\| FormData \\| null, reason: 'autocomplete' \\| 'restore'\` |
| \`resetValidity()\` | Reset validity is a way of removing manual custom errors and native validation. | |
| \`setCustomValidity()\` | Do not use this when creating a "Validator". This is intended for end users of components. We track manually defined custom errors so we don't clear them on accident in our validators. | \`message: string\` |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`change\` | Emitted when the rating's value changes. |
| \`wa-hover\` | \`phase\` Emitted when the user hovers over a value. The property indicates when hovering starts, moves to a new value, or ends. The value property tells what the rating's value would be if the user were to commit to the hovered value. |
| \`wa-invalid\` | Emitted when the form control has been checked for validity and its constraints aren't satisfied. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--symbol-color\` | The inactive color for symbols. |
| \`--symbol-color-active\` | The active color for symbols. |
| \`--symbol-spacing\` | The spacing to use around symbols. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help