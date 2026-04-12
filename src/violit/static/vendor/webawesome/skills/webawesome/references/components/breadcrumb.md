# Breadcrumb

**Full documentation:** https://webawesome.com/docs/components/breadcrumb


`<wa-breadcrumb>` Since 2.0 Stable

Breadcrumbs provide a group of links so users can easily navigate a website's hierarchy.

Breadcrumbs are usually placed before a page's main content with the current page shown last to indicate the user's position in the navigation.

```html
<wa-breadcrumb>
  <wa-breadcrumb-item>Catalog</wa-breadcrumb-item>
  <wa-breadcrumb-item>Clothing</wa-breadcrumb-item>
  <wa-breadcrumb-item>Women's</wa-breadcrumb-item>
  <wa-breadcrumb-item>Shirts &amp; Tops</wa-breadcrumb-item>
</wa-breadcrumb>
```

## Examples

### Breadcrumb Links

By default, breadcrumb items are rendered as buttons so you can use them to navigate single-page applications. In this case, you'll need to add event listeners to handle clicks.

For websites, you'll probably want to use links instead. You can make any breadcrumb item a link by applying an `href` attribute to it. Now, when the user activates it, they'll be taken to the corresponding page — no event listeners required.

```html
<wa-breadcrumb>
  <wa-breadcrumb-item href="https://example.com/home">Homepage</wa-breadcrumb-item>

  <wa-breadcrumb-item href="https://example.com/home/services">Our Services</wa-breadcrumb-item>

  <wa-breadcrumb-item href="https://example.com/home/services/digital">Digital Media</wa-breadcrumb-item>

  <wa-breadcrumb-item href="https://example.com/home/services/digital/web-design">Web Design</wa-breadcrumb-item>
</wa-breadcrumb>
```

### Start & End Decorations

Use the `start` and `end` slots to add presentational elements like `<wa-icon>` next to any breadcrumb item.

```html
<wa-breadcrumb>
  <wa-breadcrumb-item>
    <wa-icon slot="start" name="house"></wa-icon>
    Home
  </wa-breadcrumb-item>
  <wa-breadcrumb-item>Articles</wa-breadcrumb-item>
  <wa-breadcrumb-item>
    <wa-icon slot="end" name="tree-palm"></wa-icon>
    Traveling
  </wa-breadcrumb-item>
</wa-breadcrumb>
```

### Custom Separators

Use the `separator` slot to change the separator that goes between breadcrumb items. Icons work well, but you can also use text or an image.

```html
<wa-breadcrumb>
  <wa-icon slot="separator" name="angles-right" variant="solid"></wa-icon>
  <wa-breadcrumb-item>First</wa-breadcrumb-item>
  <wa-breadcrumb-item>Second</wa-breadcrumb-item>
  <wa-breadcrumb-item>Third</wa-breadcrumb-item>
</wa-breadcrumb>

<br />

<wa-breadcrumb>
  <wa-icon slot="separator" name="arrow-right" variant="solid"></wa-icon>
  <wa-breadcrumb-item>First</wa-breadcrumb-item>
  <wa-breadcrumb-item>Second</wa-breadcrumb-item>
  <wa-breadcrumb-item>Third</wa-breadcrumb-item>
</wa-breadcrumb>

<br />

<wa-breadcrumb>
  <span slot="separator">/</span>
  <wa-breadcrumb-item>First</wa-breadcrumb-item>
  <wa-breadcrumb-item>Second</wa-breadcrumb-item>
  <wa-breadcrumb-item>Third</wa-breadcrumb-item>
</wa-breadcrumb>
```

### Custom Colors

Breadcrumb labels match the color set on `<wa-breadcrumb-item>`. Content in the `start`, `end`, and `separator` slots can be styled using CSS parts.

```html
<style>
  .redcrumbs wa-breadcrumb-item {
    color: firebrick;
  }
  .redcrumbs wa-breadcrumb-item:last-of-type {
    color: crimson;
  }
  .redcrumbs wa-breadcrumb-item::part(separator) {
    color: pink;
  }
  .redcrumbs wa-breadcrumb-item::part(start),
  .redcrumbs wa-breadcrumb-item::part(end) {
    color: currentColor;
  }
</style>
<wa-breadcrumb class="redcrumbs">
  <wa-breadcrumb-item>
    <wa-icon slot="start" name="house" variant="solid"></wa-icon>
    Home
  </wa-breadcrumb-item>
  <wa-breadcrumb-item>Articles</wa-breadcrumb-item>
  <wa-breadcrumb-item>Traveling</wa-breadcrumb-item>
</wa-breadcrumb>
```

### With Dropdowns

Dropdown menus can be placed in the default slot to provide additional options.

```html
<wa-breadcrumb>
  <wa-breadcrumb-item>Homepage</wa-breadcrumb-item>
  <wa-breadcrumb-item>
    <wa-dropdown>
      <wa-button slot="trigger" size="small" appearance="filled" pill>
        <wa-icon label="More options" name="ellipsis" variant="solid"></wa-icon>
      </wa-button>
      <wa-dropdown-item type="checkbox" checked>Web Design</wa-dropdown-item>
      <wa-dropdown-item type="checkbox">Web Development</wa-dropdown-item>
      <wa-dropdown-item type="checkbox">Marketing</wa-dropdown-item>
    </wa-dropdown>
  </wa-breadcrumb-item>
  <wa-breadcrumb-item>Our Services</wa-breadcrumb-item>
  <wa-breadcrumb-item>Digital Media</wa-breadcrumb-item>
</wa-breadcrumb>
```

Alternatively, you can place dropdown menus in a `start` or `end` slot.

```html
<wa-breadcrumb>
  <wa-breadcrumb-item>Homepage</wa-breadcrumb-item>
  <wa-breadcrumb-item>Our Services</wa-breadcrumb-item>
  <wa-breadcrumb-item>Digital Media</wa-breadcrumb-item>
  <wa-breadcrumb-item>
    Web Design
    <wa-dropdown slot="end">
      <wa-button slot="trigger" size="small" appearance="filled" pill>
        <wa-icon label="More options" name="ellipsis" variant="solid"></wa-icon>
      </wa-button>
      <wa-dropdown-item type="checkbox" checked>Web Design</wa-dropdown-item>
      <wa-dropdown-item type="checkbox">Web Development</wa-dropdown-item>
      <wa-dropdown-item type="checkbox">Marketing</wa-dropdown-item>
    </wa-dropdown>
  </wa-breadcrumb-item>
</wa-breadcrumb>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/breadcrumb/breadcrumb.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaBreadcrumb from '@awesome.me/webawesome/dist/react/breadcrumb';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | One or more breadcrumb items to display. |
| \`separator\` | \`

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`label\` label | \`string\` The label to use for the breadcrumb control. This will not be shown on the screen, but it will be announced by screen readers and other assistive devices to provide more context for users. Type Default '' | | |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help