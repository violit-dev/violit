# Shadows

**Full documentation:** https://webawesome.com/docs/tokens/shadows

Shadows indicate elevation and, often, interactivity. Web Awesome offers highly modular shadow properties to easily create custom shadow effects or transform elements based on specific shadow qualities. Together with [`--wa-color-shadow`](https://webawesome.com/docs/tokens/color/#shadow), these tokens create realistic shadows for Web Awesome components.

Shadows are constructed using corresponding offset-x, offset-y, blur, and spread properties, detailed in the sections below. In Web Awesome, shadows use a size-based scale where larger shadows have greater offset and blur values to indicate greater distance from the surface below.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-shadow-s\` | |
| \`--wa-shadow-m\` | |
| \`--wa-shadow-l\` | |

Any shadow may be implemented as an inner box shadow using the `inset` keyword, e.g. `box-shadow: inset var(--wa-shadow-s);`.

## Horizontal Offset (X)

Each offset-x property uses a `calc()` function with `--wa-shadow-offset-x-scale` to uniformly scale horizontal offset values. By default, this multiplier is `0`. The table below lists the result of the calculation.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-shadow-offset-x-s\` | \`0rem\` |
| \`--wa-shadow-offset-x-m\` | \`0rem\` |
| \`--wa-shadow-offset-x-l\` | \`0rem\` |

## Vertical Offset (Y)

Each offset-y property uses a `calc()` function with `--wa-shadow-offset-y-scale` to uniformly scale vertical offset values. By default, this multiplier is `1`. The table below lists the result of the calculation.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-shadow-offset-y-s\` | \`0.125rem\` (2px) |
| \`--wa-shadow-offset-y-m\` | \`0.25rem\` (4px) |
| \`--wa-shadow-offset-y-l\` | \`0.5rem\` (8px) |

## Blur

Each blur property uses a `calc()` function with `--wa-shadow-blur-scale` to uniformly scale blur values. By default, this multiplier is `1`. The table below lists the result of the calculation.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-shadow-blur-s\` | \`0.125rem\` (2px) |
| \`--wa-shadow-blur-m\` | \`0.25rem\` (4px) |
| \`--wa-shadow-blur-l\` | \`0.5rem\` (8px) |

## Spread

Each spread property uses a `calc()` function with `--wa-shadow-spread-scale` to uniformly scale spread values. By default, this multiplier is `-0.5`. The table below lists the result of the calculation.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-shadow-spread-s\` | \`-0.0625rem\` (-1px) |
| \`--wa-shadow-spread-m\` | \`-0.125rem\` (-2px) |
| \`--wa-shadow-spread-l\` | \`-0.25rem\` (-4px) |