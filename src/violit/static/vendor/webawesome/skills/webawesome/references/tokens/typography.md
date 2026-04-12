# Typography

**Full documentation:** https://webawesome.com/docs/tokens/typography

## Font Family

Font families are assigned specific roles — like heading or code — to help keep text styles consistent and easy to customize. By default, these properties use system fonts and generic fallbacks to maximize performance.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-font-family-body\` | \`ui-sans-serif, system-ui, sans-serif\` |
| \`--wa-font-family-heading\` | \`var(--wa-font-family-body)\` |
| \`--wa-font-family-code\` | \`ui-monospace, monospace\` |
| \`--wa-font-family-longform\` | \`ui-serif, serif\` |

## Font Size

Font sizes use a ratio of 1.125 to scale sizes proportionally. Starting with the medium (`m`) font size, smaller sizes (`s` through `3xs`) are 1.125x smaller as the sizes decrease, and larger sizes (`l` through `5xl`) are _twice_ 1.125x larger as sizes increase — here, the ratio is doubled to maximize impact between sizes.

Each value uses `rem` units and is rounded to the nearest whole pixel when rendered with [`round()`](https://developer.mozilla.org/en-US/docs/Web/CSS/round).

You can use `--wa-font-size-scale` to increase or decrease all font sizes at once. By default, this multiplier is `1`.

The calculations for each size and the resulting pixel value (assuming a 16px root font size) are listed below.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-font-size-3xs\` | \`round(calc(var(--wa-font-size-2xs) / 1.125), 1px)\` (10px) |
| \`--wa-font-size-2xs\` | \`round(calc(var(--wa-font-size-xs) / 1.125), 1px)\` (11px) |
| \`--wa-font-size-xs\` | \`round(calc(var(--wa-font-size-s) / 1.125), 1px)\` (12px) |
| \`--wa-font-size-s\` | \`round(calc(var(--wa-font-size-m) / 1.125), 1px)\` (14px) |
| \`--wa-font-size-m\` | \`calc(1rem \* var(--wa-font-size-scale))\` (16px) |
| \`--wa-font-size-l\` | \`round(calc(var(--wa-font-size-m) \* 1.125 \* 1.125), 1px)\` (20px) |
| \`--wa-font-size-xl\` | \`round(calc(var(--wa-font-size-l) \* 1.125 \* 1.125), 1px)\` (25px) |
| \`--wa-font-size-2xl\` | \`round(calc(var(--wa-font-size-xl) \* 1.125 \* 1.125), 1px)\` (32px) |
| \`--wa-font-size-3xl\` | \`round(calc(var(--wa-font-size-2xl) \* 1.125 \* 1.125), 1px)\` (41px) |
| \`--wa-font-size-4xl\` | \`round(calc(var(--wa-font-size-3xl) \* 1.125 \* 1.125), 1px)\` (52px) |
| \`--wa-font-size-5xl\` | \`round(calc(var(--wa-font-size-4xl) \* 1.125 \* 1.125), 1px)\` (66px) |

`3xs` and `2xs` fall below typical legibility. It's best to keep their use to non-essential UI only (e.g. labels, metadata) to maintain accessibility.

You can also use these two custom properties make any font size proportionally smaller or larger to its parent.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-font-size-smaller\` | \`round(calc(1em / 1.125), 1px)\` |
| \`--wa-font-size-larger\` | \`round(calc(1em \* 1.125 \* 1.125), 1px)\` |

## Font Weight

Font weight properties are given common names or assigned specific roles.

Common weights let you easily adjust the full range of weights for your theme.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-font-weight-light\` | \`300\` |
| \`--wa-font-weight-normal\` | \`400\` |
| \`--wa-font-weight-semibold\` | \`500\` |
| \`--wa-font-weight-bold\` | \`600\` |

Role-based weights allow you to uniformly adjust the weight of certain types of text to keep styles consistent.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-font-weight-body\` | \`var(--wa-font-weight-normal)\` |
| \`--wa-font-weight-heading\` | \`var(--wa-font-weight-bold)\` |
| \`--wa-font-weight-code\` | \`var(--wa-font-weight-normal)\` |
| \`--wa-font-weight-longform\` | \`var(--wa-font-weight-normal)\` |
| \`--wa-font-weight-action\` | \`var(--wa-font-weight-semibold)\` |

In Web Awesome, we use `--wa-font-weight-action` for interactive text, such as button labels and tab names. We also recommend using `--wa-font-weight-action` for text that uses color alone to signal interactivity, such as links without text decoration.

## Line Height

Line heights control the distance between lines of text and are unitless to scale proportionately with text size. For readability, `--wa-line-height-normal`, recommended for paragraph text, should be 1.5 or greater.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-line-height-condensed\` | \`1.2\` |
| \`--wa-line-height-normal\` | \`1.6\` |
| \`--wa-line-height-expanded\` | \`2\` |

## Links

Together with [`--wa-color-link`](https://webawesome.com/docs/tokens/color/#text), these tokens add text decoration to `<a>` elements to signal their role as hyperlinks.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-link-decoration-default\` | \`underline color-mix(in oklab, var(--wa-color-text-link) 70%, transparent) dotted\` |
| \`--wa-link-decoration-hover\` | \`underline\` |