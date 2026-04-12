# Borders

**Full documentation:** https://webawesome.com/docs/tokens/borders

## Style

Border style controls the standard line shape of borders throughout Web Awesome.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-border-style\` | \`solid\` |

## Width

Border widths use `rem` units in order to scale proportionately with the root font size.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-border-width-s\` | \`0.0625rem\` (1px) |
| \`--wa-border-width-m\` | \`0.125rem\` (2px) |
| \`--wa-border-width-l\` | \`0.1875rem\` (3px) |

To scale all borders at once, you can use the `--wa-border-width-scale` property which specifies a multiplier on `border-width`. Values < 1 make all borders uniformly thinner, while values > 1 make them thicker.

## Radius

Border radius controls the corners of Web Awesome components.

Common border radius properties allow you to achieve specific shapes beyond your theme's preferred corner styles.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-border-radius-pill\` | \`9999px\` |
| \`--wa-border-radius-circle\` | \`50%\` |
| \`--wa-border-radius-square\` | \`0px\` |

Size-based border radius properties allow you to customize the overall roundness of Web Awesome components. These use `rem` units in order to scale proportionately with the root font size.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-border-radius-s\` | \`0.1875rem\` (3px) |
| \`--wa-border-radius-m\` | \`0.375rem\` (6px) |
| \`--wa-border-radius-l\` | \`0.75rem\` (12px) |

To scale all border radii at once, you can use the `--wa-border-radius-scale` property which specifies a multiplier on `border-radius`. Values < 1 make corners sharper, while values > 1 make them rounder.