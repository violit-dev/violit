# Color

**Full documentation:** https://webawesome.com/docs/tokens/color

Web Awesome's color system is made up of CSS custom properties to help with consistent color use throughout your project.

Color is organized by three main categories:

-   [Color scales](#color-scales) that gives you a full spectrum of hues to work with
-   [Foundational colors](#foundational-colors) that lay the groundwork for your theme
-   [Semantic colors](#semantic-colors) that draw attention and convey meaning

## Color Scales

Color scales are determined by your [color palette](https://webawesome.com/docs/color-palettes) and are made up of the lowest level color tokens in your theme. Each token is identified by a name, like red or gray, and numerical tint based on the color's lightness. On this scale, 100 is equal to pure white and 0 is equal to pure black.

You can use these tints to ensure accessible color contrast per [WCAG 2.1 success criteria](https://www.w3.org/TR/WCAG21/#contrast-minimum):

-   A difference of 40 ensures a minimum 3:1 contrast ratio, suitable for large text and icons (AA)
-   A difference of 50 ensures a minimum 4.5:1 contrast ratio, suitable for normal text (AA) and large text (AAA)
-   A difference of 60 ensures a minimum 7:1 contrast ratio, suitable for all text (AAA)

You have several hand-crafted [color palettes](https://webawesome.com/docs/color-palettes) to choose from. Each palette defines 10 hues each with a scale of 11 tints using the format `--wa-color-{hue}-{tint}`.

Red

\`--wa-color-red-95\`, \`--wa-color-red-90\`, \`--wa-color-red-80\`, \`--wa-color-red-70\`, \`--wa-color-red-60\`, \`--wa-color-red-50\`, \`--wa-color-red-40\`, \`--wa-color-red-30\`, \`--wa-color-red-20\`, \`--wa-color-red-10\`, \`--wa-color-red-05\`

Orange

\`--wa-color-orange-95\`, \`--wa-color-orange-90\`, \`--wa-color-orange-80\`, \`--wa-color-orange-70\`, \`--wa-color-orange-60\`, \`--wa-color-orange-50\`, \`--wa-color-orange-40\`, \`--wa-color-orange-30\`, \`--wa-color-orange-20\`, \`--wa-color-orange-10\`, \`--wa-color-orange-05\`

Yellow

\`--wa-color-yellow-95\`, \`--wa-color-yellow-90\`, \`--wa-color-yellow-80\`, \`--wa-color-yellow-70\`, \`--wa-color-yellow-60\`, \`--wa-color-yellow-50\`, \`--wa-color-yellow-40\`, \`--wa-color-yellow-30\`, \`--wa-color-yellow-20\`, \`--wa-color-yellow-10\`, \`--wa-color-yellow-05\`

Green

\`--wa-color-green-95\`, \`--wa-color-green-90\`, \`--wa-color-green-80\`, \`--wa-color-green-70\`, \`--wa-color-green-60\`, \`--wa-color-green-50\`, \`--wa-color-green-40\`, \`--wa-color-green-30\`, \`--wa-color-green-20\`, \`--wa-color-green-10\`, \`--wa-color-green-05\`

Cyan

\`--wa-color-cyan-95\`, \`--wa-color-cyan-90\`, \`--wa-color-cyan-80\`, \`--wa-color-cyan-70\`, \`--wa-color-cyan-60\`, \`--wa-color-cyan-50\`, \`--wa-color-cyan-40\`, \`--wa-color-cyan-30\`, \`--wa-color-cyan-20\`, \`--wa-color-cyan-10\`, \`--wa-color-cyan-05\`

Blue

\`--wa-color-blue-95\`, \`--wa-color-blue-90\`, \`--wa-color-blue-80\`, \`--wa-color-blue-70\`, \`--wa-color-blue-60\`, \`--wa-color-blue-50\`, \`--wa-color-blue-40\`, \`--wa-color-blue-30\`, \`--wa-color-blue-20\`, \`--wa-color-blue-10\`, \`--wa-color-blue-05\`

Indigo

\`--wa-color-indigo-95\`, \`--wa-color-indigo-90\`, \`--wa-color-indigo-80\`, \`--wa-color-indigo-70\`, \`--wa-color-indigo-60\`, \`--wa-color-indigo-50\`, \`--wa-color-indigo-40\`, \`--wa-color-indigo-30\`, \`--wa-color-indigo-20\`, \`--wa-color-indigo-10\`, \`--wa-color-indigo-05\`

Purple

\`--wa-color-purple-95\`, \`--wa-color-purple-90\`, \`--wa-color-purple-80\`, \`--wa-color-purple-70\`, \`--wa-color-purple-60\`, \`--wa-color-purple-50\`, \`--wa-color-purple-40\`, \`--wa-color-purple-30\`, \`--wa-color-purple-20\`, \`--wa-color-purple-10\`, \`--wa-color-purple-05\`

Pink

\`--wa-color-pink-95\`, \`--wa-color-pink-90\`, \`--wa-color-pink-80\`, \`--wa-color-pink-70\`, \`--wa-color-pink-60\`, \`--wa-color-pink-50\`, \`--wa-color-pink-40\`, \`--wa-color-pink-30\`, \`--wa-color-pink-20\`, \`--wa-color-pink-10\`, \`--wa-color-pink-05\`

Gray

\`--wa-color-gray-95\`, \`--wa-color-gray-90\`, \`--wa-color-gray-80\`, \`--wa-color-gray-70\`, \`--wa-color-gray-60\`, \`--wa-color-gray-50\`, \`--wa-color-gray-40\`, \`--wa-color-gray-30\`, \`--wa-color-gray-20\`, \`--wa-color-gray-10\`, \`--wa-color-gray-05\`

### Semantic Scales

Any hue can be mapped to `brand`, `neutral`, `success`, `warning`, and `danger` scales. Like the tokens in a color scale, each token is identified by its semantic group and a numerical tint using the format `--wa-color-{group}-{tint}`.

Brand

\`--wa-color-brand-95\`, \`--wa-color-brand-90\`, \`--wa-color-brand-80\`, \`--wa-color-brand-70\`, \`--wa-color-brand-60\`, \`--wa-color-brand-50\`, \`--wa-color-brand-40\`, \`--wa-color-brand-30\`, \`--wa-color-brand-20\`, \`--wa-color-brand-10\`, \`--wa-color-brand-05\`

Neutral

\`--wa-color-neutral-95\`, \`--wa-color-neutral-90\`, \`--wa-color-neutral-80\`, \`--wa-color-neutral-70\`, \`--wa-color-neutral-60\`, \`--wa-color-neutral-50\`, \`--wa-color-neutral-40\`, \`--wa-color-neutral-30\`, \`--wa-color-neutral-20\`, \`--wa-color-neutral-10\`, \`--wa-color-neutral-05\`

Success

\`--wa-color-success-95\`, \`--wa-color-success-90\`, \`--wa-color-success-80\`, \`--wa-color-success-70\`, \`--wa-color-success-60\`, \`--wa-color-success-50\`, \`--wa-color-success-40\`, \`--wa-color-success-30\`, \`--wa-color-success-20\`, \`--wa-color-success-10\`, \`--wa-color-success-05\`

Warning

\`--wa-color-warning-95\`, \`--wa-color-warning-90\`, \`--wa-color-warning-80\`, \`--wa-color-warning-70\`, \`--wa-color-warning-60\`, \`--wa-color-warning-50\`, \`--wa-color-warning-40\`, \`--wa-color-warning-30\`, \`--wa-color-warning-20\`, \`--wa-color-warning-10\`, \`--wa-color-warning-05\`

Danger

\`--wa-color-danger-95\`, \`--wa-color-danger-90\`, \`--wa-color-danger-80\`, \`--wa-color-danger-70\`, \`--wa-color-danger-60\`, \`--wa-color-danger-50\`, \`--wa-color-danger-40\`, \`--wa-color-danger-30\`, \`--wa-color-danger-20\`, \`--wa-color-danger-10\`, \`--wa-color-danger-05\`

## Foundational Colors

Foundational colors lay the groundwork for the content and structure of your project. These colors are named according to their role in your theme.

### Surfaces

Surfaces are background layers that other content rests on. Surface colors help convey hierarchy through a sense of elevation, where `--wa-color-surface-raised` is the closest to the user (e.g., dialogs and popup menus) and `--wa-color-surface-lowered` is the farthest away (e.g., wells).

| Custom Property |
| --- |
| \`--wa-color-surface-raised\` |
| \`--wa-color-surface-default\` |
| \`--wa-color-surface-lowered\` |
| \`--wa-color-surface-border\` |

### Text

Text colors are used for standard text elements. We recommend a minimum 4.5:1 contrast ratio between text colors and surface colors.

| Custom Property |
| --- |
| \`--wa-color-text-normal\` |
| \`--wa-color-text-quiet\` |
| \`--wa-color-text-link\` |

### Overlays

Overlays provide a backdrop to isolate content, often allowing background context to show through.

| Custom Property |
| --- |
| \`--wa-color-overlay-modal\` |
| \`--wa-color-overlay-inline\` |

### Shadow

Web Awesome uses a single color for all shadows. This is used alongside other [shadow tokens](https://webawesome.com/docs/tokens/shadows) to construct your theme's shadows.

| Custom Property |
| --- |
| \`--wa-color-shadow\` |

### Interactions

#### Focus

Web Awesome uses a single focus color for predictable keyboard navigation. This is used alongside other [focus tokens](https://webawesome.com/docs/tokens/focus) to construct `--wa-focus-ring`. We recommend a minimum 3:1 contrast ratio against surface colors and background colors wherever possible.

| Custom Property |
| --- |
| \`--wa-color-focus\` |

#### Hover and Active

Web Awesome leverages `color-mix()` to achieve consistent hover and active states across components without the need for untold numbers of handpicked colors. Through `color-mix()`, these custom properties contextually generate hover and active colors based on the color of the component.

| Custom Property |
| --- |
| \`--wa-color-mix-hover\` |
| \`--wa-color-mix-active\` |

## Semantic Colors

Semantic colors reinforce a specific message, intended usage, or expected results through familiar, meaningful hues. Each color is identified by its semantic group, role, and attention using the format `--wa-color-{group}-{role}-{attention}`. There are five groups of semantic colors:

-   **Brand** to emphasize your brand color
-   **Success** for validity or confirmation
-   **Neutral** for ordinary or inactive content
-   **Warning** for caution or uncertainty
-   **Danger** for errors or risk

Each group defines colors for specific roles so that colors can be easily assembled with predictable results and readable contrast. There are three roles:

-   **Fill** for background colors or areas larger than a few pixels
-   **Border** for borders, dividers, and other stroke-width elements
-   **On** for content displayed on a fill (e.g., pair `--wa-color-danger-on-loud` with `--wa-color-danger-fill-loud`)

Finally, each color is named according to how much attention it draws. Here, we use noise as an analogy: a loud noise draws more attention than a quiet one. There are three levels of attention:

-   **Quiet** draws the least attention
-   **Normal** draws some attention
-   **Loud** draws the most attention

| Custom Property | brand | success | neutral | warning | danger |
| --- | --- | --- | --- | --- | --- |