# Color Variants

**Full documentation:** https://webawesome.com/docs/utilities/color

Some Web Awesome components, like `<wa-button>`, allow you to change the color by using a `variant` attribute:

-   [`<wa-badge>`](https://webawesome.com/docs/components/badge)
-   [`<wa-button>`](https://webawesome.com/docs/components/button)
-   [`<wa-button-group>`](https://webawesome.com/docs/components/button-group)
-   [`<wa-callout>`](https://webawesome.com/docs/components/callout)
-   [`<wa-tag>`](https://webawesome.com/docs/components/tag)

You can create the same effect on any element by using the color variant utility classes:

-   `.wa-brand`
-   `.wa-neutral`
-   `.wa-success`
-   `.wa-warning`
-   `.wa-danger`

Using these classes is a two-way handshake: they do not directly apply styles, but define generic color tokens modeled after our [Semantic Colors](https://webawesome.com/docs/tokens/color/#semantic-colors) but _without_ the group identifier (`neutral`, `brand`, `success`, `warning`, `danger`), defaulting to `neutral`. This means that styles can be written to respond to variants by using e.g. `--wa-color-fill-loud` instead of e.g. `--wa-color-brand-fill-loud`, and all of our [native styles](https://webawesome.com/docs/utilities/native/) do so (where it made sense).

For example, assume we wanted to make a custom `.callout` class with color variants. This is all we need to do:

```html
<p class="callout">This is a callout.</p>
<p class="callout wa-brand">This is a callout.</p>
<p class="callout wa-success">This is a callout.</p>
<p class="callout wa-warning">This is a callout.</p>
<p class="callout wa-danger">This is a callout.</p>

<style>
  .callout {
    background-color: var(--wa-color-fill-quiet);
    border: 1px solid var(--wa-color-border-quiet);
    color: var(--wa-color-on-quiet);
    padding: var(--wa-space-m) var(--wa-space-l);
  }
</style>
```