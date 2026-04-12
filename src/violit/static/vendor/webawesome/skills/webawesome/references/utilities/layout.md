# Layout Utilities

**Full documentation:** https://webawesome.com/docs/utilities

## Stack

Use `wa-stack` to arrange elements in the block direction with even spacing.

```html
<div class="wa-stack">
  <div></div>
  <div></div>
  <div></div>
</div>
```

## Examples

Stacks are well suited for forms, text, and ensuring consistent spacing between elements in the document flow.

```html
<div class="wa-stack">
  <wa-input label="Email">
    <wa-icon slot="start" name="envelope" variant="regular"></wa-icon>
  </wa-input>
  <wa-input label="Password" type="password">
    <wa-icon slot="start" name="lock" variant="regular"></wa-icon>
  </wa-input>
  <wa-checkbox>Remember me on this device</wa-checkbox>
  <wa-button appearance="filled">Log In</wa-button>
</div>
```

```html
<div class="wa-stack wa-gap-2xl">
  <h3>Aragorn's Squash</h3>
  <p>
    Altogether unleash weasel mainly well-protected hiding Farthing excuse. Falling pits oil em Hasufel levels weight
    rides vagabonds? Gamgee hard-won thunder merrier forests treasury. Past birthday lasts lowly there'd woe Woodland pa
    sun's slaying most handling.
  </p>
  <p>
    Even the smallest person can change the course of the future. They tempted completely other caves cloven wisest
    draught scrumptious cook Undómiel friends. Dory crunchy huge sleepless. Unmade took nerves liquor defeated Arathorn.
  </p>
</div>
```

## Align Items

By default, items stretch to fill the inline size of the `wa-stack` container. You can add any of the following [`wa-align-items-*`](https://webawesome.com/docs/utilities/align-items) classes to an element with `wa-stack` to specify how items are aligned in the inline direction:

-   `wa-align-items-start`
-   `wa-align-items-end`
-   `wa-align-items-center`
-   `wa-align-items-stretch`
-   `wa-align-items-baseline`

```html
<div class="wa-grid">
  <div class="wa-stack wa-align-items-start">
    <div style="min-inline-size: 4rem;"></div>
    <div style="min-inline-size: 8rem;"></div>
    <div style="min-inline-size: 6rem;"></div>
  </div>
  <div class="wa-stack wa-align-items-center">
    <div style="min-inline-size: 4rem;"></div>
    <div style="min-inline-size: 8rem;"></div>
    <div style="min-inline-size: 6rem;"></div>
  </div>
  <div class="wa-stack wa-align-items-end">
    <div style="min-inline-size: 4rem;"></div>
    <div style="min-inline-size: 8rem;"></div>
    <div style="min-inline-size: 6rem;"></div>
  </div>
</div>
```

## Gap

By default, the gap between stack items uses `--wa-space-m` from your theme. You can add any of the following [`wa-gap-*`](https://webawesome.com/docs/utilities/gap) classes to an element with `wa-stack` to specify the gap between items:

-   `wa-gap-0`
-   `wa-gap-3xs`
-   `wa-gap-2xs`
-   `wa-gap-xs`
-   `wa-gap-s`
-   `wa-gap-m`
-   `wa-gap-l`
-   `wa-gap-xl`
-   `wa-gap-2xl`
-   `wa-gap-3xl`
-   `wa-gap-4xl`
-   `wa-gap-5xl`

```html
<div class="wa-grid">
  <div class="wa-stack wa-gap-2xs">
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-stack wa-gap-2xl">
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>
```

---

## Cluster

Use the `wa-cluster` class to arrange elements inline with even spacing, allowing items to wrap when space is limited.

```html
<div class="wa-cluster">
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
</div>

<!-- We'll vary the div sizes to show the flow of cluster elements -->
<style>
  .wa-cluster div:empty:nth-child(3n) {
    min-inline-size: 6rem;
  }
  .wa-cluster div:empty:nth-child(3n + 2) {
    min-inline-size: 8rem;
  }
</style>
```

## Examples

Clusters are great for inline lists and aligning items of varying sizes.

```html
<div class="wa-cluster">
  <wa-icon name="web-awesome"></wa-icon>
  <a href="#">Components</a>
  <a href="#">Layout</a>
  <a href="#">Patterns</a>
  <a href="#">Theming</a>
</div>
```

```html
<div class="wa-stack">
  <h3 class="wa-heading-2xl">Withywindle Pub and Eatery</h3>
  <div class="wa-cluster wa-gap-xs">
    <wa-rating value="4.6" read-only></wa-rating>
    <strong>4.6</strong>
    <span>(419 reviews)</span>
  </div>
  <div class="wa-cluster wa-gap-xs">
    <div class="wa-cluster wa-gap-3xs">
      <wa-icon name="dollar" style="color: var(--wa-color-green-60);"></wa-icon>
      <wa-icon name="dollar" style="color: var(--wa-color-green-60);"></wa-icon>
      <wa-icon name="dollar" style="color: var(--wa-color-green-60);"></wa-icon>
    </div>
    <span class="wa-caption-s">&bull;</span>
    <wa-tag size="small">Comfort Food</wa-tag>
    <wa-tag size="small">Gastropub</wa-tag>
    <wa-tag size="small">Cocktail Bar</wa-tag>
    <wa-tag size="small">Vegetarian</wa-tag>
    <wa-tag size="small">Gluten Free</wa-tag>
  </div>
</div>
```

## Align Items

By default, items are centered in the block direction of the `wa-cluster` container. You can add any of the following [`wa-align-items-*`](https://webawesome.com/docs/utilities/align-items) classes to an element with `wa-cluster` to specify how items are aligned in the block direction:

-   `wa-align-items-start`
-   `wa-align-items-end`
-   `wa-align-items-center`
-   `wa-align-items-stretch`
-   `wa-align-items-baseline`

```html
<div class="wa-stack">
  <div class="wa-cluster wa-align-items-start" style="min-height: 8rem;">
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-cluster wa-align-items-end" style="min-height: 8rem;">
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-cluster wa-align-items-center" style="min-height: 8rem;">
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-cluster wa-align-items-stretch" style="min-height: 8rem;">
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>
```

## Gap

By default, the gap between cluster items uses `--wa-space-m` from your theme. You can add any of the following [`wa-gap-*`](https://webawesome.com/docs/utilities/gap) classes to an element with `wa-cluster` to specify the gap between items:

-   `wa-gap-0`
-   `wa-gap-3xs`
-   `wa-gap-2xs`
-   `wa-gap-xs`
-   `wa-gap-s`
-   `wa-gap-m`
-   `wa-gap-l`
-   `wa-gap-xl`
-   `wa-gap-2xl`
-   `wa-gap-3xl`
-   `wa-gap-4xl`
-   `wa-gap-5xl`

```html
<div class="wa-stack">
  <div class="wa-cluster wa-gap-2xs">
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-cluster wa-gap-2xl">
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>
```

---

## Grid

Use the `wa-grid` class to arrange elements into rows and columns that automatically adapt to the available space.

```html
<div class="wa-grid">
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
</div>
```

## Examples

Grids work especially well for card lists and content designed for browsing.

```html
<div class="wa-grid">
  <div class="wa-stack wa-gap-s">
    <div class="wa-frame wa-border-radius-l">
      <img src="https://images.unsplash.com/photo-1520763185298-1b434c919102?q=20" alt="" />
    </div>
    <h3 class="wa-heading-m">Tulip</h3>
    <em>Tulipa gesneriana</em>
  </div>
  <div class="wa-stack wa-gap-s">
    <div class="wa-frame wa-border-radius-l">
      <img src="https://images.unsplash.com/photo-1591767134492-338e62f7b5a2?q=20" alt="" />
    </div>
    <h3 class="wa-heading-m">Peony</h3>
    <em>Paeonia officinalis</em>
  </div>
  <div class="wa-stack wa-gap-s">
    <div class="wa-frame wa-border-radius-l">
      <img src="https://images.unsplash.com/photo-1590872000386-4348c6393115?q=20" alt="" />
    </div>
    <h3 class="wa-heading-m">Poppy</h3>
    <em>Papaver rhoeas</em>
  </div>
  <div class="wa-stack wa-gap-s">
    <div class="wa-frame wa-border-radius-l">
      <img src="https://images.unsplash.com/photo-1516723338795-324c7c33f700?q=20" alt="" />
    </div>
    <h3 class="wa-heading-m">Sunflower</h3>
    <em>Helianthus annuus</em>
  </div>
  <div class="wa-stack wa-gap-s">
    <div class="wa-frame wa-border-radius-l">
      <img src="https://images.unsplash.com/photo-1563601841845-74a0a8ab7c8a?q=20" alt="" />
    </div>
    <h3 class="wa-heading-m">Daisy</h3>
    <em>Bellis perennis</em>
  </div>
</div>
```

```html
<div class="wa-grid" style="--min-column-size: 30ch;">
  <wa-card>
    <div class="wa-flank">
      <wa-avatar shape="rounded">
        <wa-icon slot="icon" name="globe"></wa-icon>
      </wa-avatar>
      <div class="wa-stack wa-gap-3xs">
        <span class="wa-caption-xs">Population (Zion)</span>
        <span class="wa-cluster wa-gap-xs">
          <span class="wa-heading-2xl">251,999</span>
          <wa-badge variant="danger">-3%&nbsp;<wa-icon name="arrow-trend-down"></wa-icon></wa-badge>
        </span>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-flank">
      <wa-avatar shape="rounded">
        <wa-icon slot="icon" name="brain-circuit"></wa-icon>
      </wa-avatar>
      <div class="wa-stack wa-gap-3xs">
        <span class="wa-caption-xs">Minds Freed</span>
        <span class="wa-cluster wa-gap-xs">
          <span class="wa-heading-2xl">0.36%</span>
          <wa-badge variant="success">+0.03%&nbsp;<wa-icon name="arrow-trend-up"></wa-icon></wa-badge>
        </span>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-flank">
      <wa-avatar shape="rounded">
        <wa-icon slot="icon" name="robot"></wa-icon>
      </wa-avatar>
      <div class="wa-stack wa-gap-3xs">
        <span class="wa-caption-xs">Agents Discovered</span>
        <span class="wa-cluster wa-gap-xs">
          <span class="wa-heading-2xl">3</span>
          <wa-badge variant="neutral">±0%&nbsp;<wa-icon name="wave-triangle"></wa-icon></wa-badge>
        </span>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-flank">
      <wa-avatar shape="rounded">
        <wa-icon slot="icon" name="spaghetti-monster-flying"></wa-icon>
      </wa-avatar>
      <div class="wa-stack wa-gap-3xs">
        <span class="wa-caption-xs">Sentinels Controlled</span>
        <span class="wa-cluster wa-gap-xs">
          <span class="wa-heading-2xl">208</span>
          <wa-badge variant="success">+1%&nbsp;<wa-icon name="arrow-trend-up"></wa-icon></wa-badge>
        </span>
      </div>
    </div>
  </wa-card>
</div>

<style>
  wa-badge > wa-icon {
    color: color-mix(in oklab, currentColor, transparent 40%);
  }
</style>
```

## Sizing

By default, grid items will wrap when the grid's column size is less than `20ch`, but you can set a custom minimum column size using the `--min-column-size` property.

```html
<div class="wa-stack">
  <div class="wa-grid" style="--min-column-size: 200px;">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-grid" style="--min-column-size: 6rem;">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>
```

## Gap

By default, the gap between grid items uses `--wa-space-m` from your theme. You can add any of the following [`wa-gap-*`](https://webawesome.com/docs/utilities/gap) classes to an element with `wa-grid` to specify the gap between items:

-   `wa-gap-0`
-   `wa-gap-3xs`
-   `wa-gap-2xs`
-   `wa-gap-xs`
-   `wa-gap-s`
-   `wa-gap-m`
-   `wa-gap-l`
-   `wa-gap-xl`
-   `wa-gap-2xl`
-   `wa-gap-3xl`

```html
<div class="wa-stack">
  <div class="wa-grid wa-gap-2xs">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div class="wa-grid wa-gap-2xl">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>
```

## Span Grid

You can add `wa-span-grid` to any grid item to allow it to span all grid columns. With this, the grid item occupies its own grid row.

```html
<div class="wa-grid">
  <div></div>
  <div></div>
  <div class="wa-span-grid"></div>
  <div></div>
  <div></div>
</div>
```

---

## Split

Use the `wa-split` class to distribute two or more items evenly across available space, either in a row or a column.

```html
<div class="wa-split">
  <div></div>
  <div></div>
</div>
```

## Examples

Splits are especially helpful for navigation, header, and footer layouts.

```html
<div class="wa-flank">
  <div class="wa-split:column">
    <div class="wa-stack">
      <wa-button appearance="plain">
        <wa-icon name="house" label="Home"></wa-icon>
      </wa-button>
      <wa-button appearance="plain">
        <wa-icon name="calendar" label="Calendar"></wa-icon>
      </wa-button>
      <wa-button appearance="plain">
        <wa-icon name="envelope" label="Mail"></wa-icon>
      </wa-button>
    </div>
    <div class="wa-stack">
      <wa-divider></wa-divider>
      <wa-button appearance="plain">
        <wa-icon name="right-from-bracket" label="Sign Out"></wa-icon>
      </wa-button>
    </div>
  </div>
  <div class="placeholder"></div>
</div>

<style>
  .placeholder {
    min-block-size: 300px;
    background-color: var(--wa-color-neutral-fill-quiet);
    border: dashed var(--wa-border-width-s) var(--wa-color-neutral-border-normal);
    border-radius: var(--wa-border-radius-l);
  }
</style>
```

```html
<div class="wa-stack">
  <div class="wa-split">
    <wa-icon name="web-awesome" label="Web Awesome" class="wa-font-size-xl"></wa-icon>
    <div class="wa-cluster">
      <wa-button appearance="filled">Sign Up</wa-button>
      <wa-button appearance="outlined">Log In</wa-button>
    </div>
  </div>
  <div class="placeholder"></div>
</div>

<style>
  .placeholder {
    min-block-size: 300px;
    background-color: var(--wa-color-neutral-fill-quiet);
    border: dashed var(--wa-border-width-s) var(--wa-color-neutral-border-normal);
    border-radius: var(--wa-border-radius-l);
  }
</style>
```

## Direction

Items can be split across a row or a column by appending `:row` or `:column` to the `wa-split` class.

```html
<div class="wa-flank wa-align-items-start" style="block-size: 16rem;">
  <div class="wa-split:column">
    <div></div>
    <div></div>
  </div>
  <div class="wa-split:row">
    <div></div>
    <div></div>
  </div>
</div>
```

## Align Items

By default, items are centered on the cross axis of the `wa-split` container. You can add any of the following [`wa-align-items-*`](https://webawesome.com/docs/utilities/align-items) classes to an element with `wa-split` to specify how items are aligned:

-   `wa-align-items-start`
-   `wa-align-items-end`
-   `wa-align-items-center`
-   `wa-align-items-stretch`
-   `wa-align-items-baseline`

These modifiers specify how items are aligned in the block direction for `wa-split:row` and in the inline direction for `wa-split:column`.

```html
<div class="wa-stack">
  <div class="wa-split wa-align-items-start" style="height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-split wa-align-items-end" style="height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-split wa-align-items-center" style="height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-split wa-align-items-stretch" style="height: 8rem;">
    <div></div>
    <div></div>
  </div>
</div>
```

## Gap

A split's gap determines how close items can be before they wrap. By default, the gap between split items uses `--wa-space-m` from your theme. You can add any of the following [`wa-gap-*`](https://webawesome.com/docs/utilities/gap) classes to an element with `wa-split` to specify the gap between items:

-   `wa-gap-0`
-   `wa-gap-3xs`
-   `wa-gap-2xs`
-   `wa-gap-xs`
-   `wa-gap-s`
-   `wa-gap-m`
-   `wa-gap-l`
-   `wa-gap-xl`
-   `wa-gap-2xl`
-   `wa-gap-3xl`

```html
<div class="wa-stack">
  <div class="wa-split wa-gap-3xs">
    <div></div>
    <div></div>
  </div>
  <div class="wa-split wa-gap-3xl">
    <div></div>
    <div></div>
  </div>
</div>
```

---

## Flank

Use the `wa-flank` class to position two items side-by-side, with one item positioned alongside, or _flanking_, content that stretches to fill the available space. When space is limited, the items wrap.

```html
<div class="wa-flank">
  <div></div>
  <div></div>
</div>
```

## Examples

Flanks work especially well for asides, inputs with adjacent buttons, and rich description lists.

```html
<div class="wa-flank:end wa-gap-xs">
  <wa-input>
    <wa-icon slot="start" name="magnifying-glass"></wa-icon>
  </wa-input>
  <wa-button appearance="filled">Search</wa-button>
</div>
```

```html
<div class="wa-stack wa-gap-xl">
  <div class="wa-flank wa-align-items-start">
    <wa-avatar
      image="https://images.unsplash.com/photo-1553284966-19b8815c7817?q=20"
      label="Gandalf's avatar"
    ></wa-avatar>
    <div class="wa-stack wa-gap-3xs">
      <strong>Gandalf</strong>
      <p class="wa-body-s">
        All we have to decide is what to do with the time that is given to us. There are other forces at work in this
        world, Frodo, besides the will of evil.
      </p>
    </div>
  </div>
  <div class="wa-flank wa-align-items-start">
    <wa-avatar
      image="https://images.unsplash.com/photo-1542403764-c26462c4697e?q=20"
      label="Boromir's avatar"
    ></wa-avatar>
    <div class="wa-stack wa-gap-3xs">
      <strong>Boromir</strong>
      <p class="wa-body-s">
        One does not simply walk into Mordor. Its Black Gates are guarded by more than just Orcs. There is evil there
        that does not sleep, and the Great Eye is ever watchful.
      </p>
    </div>
  </div>
  <div class="wa-flank wa-align-items-start">
    <wa-avatar
      image="https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=20"
      label="Galadriel's avatar"
    ></wa-avatar>
    <div class="wa-stack wa-gap-3xs">
      <strong>Galadriel</strong>
      <p class="wa-body-s">
        The world is changed. I feel it in the water. I feel it in the earth. I smell it in the air. Much that once was
        is lost, for none now live who remember it.
      </p>
    </div>
  </div>
</div>
```

## Position

By default, the first item in the `wa-flank` container will flank the other content. You can specify whether the first or last item will flank the remaining content by appending `:start` or `:end` to the `wa-flank` class.

```html
<div class="wa-stack">
  <div class="wa-flank:start">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank:end">
    <div></div>
    <div></div>
  </div>
</div>
```

## Sizing

The flank's inline size is determined by the size of its content, but you can set a target size using the `--flank-size` property. When the flank wraps, it stretches to fill the inline size of the container.

```html
<div class="wa-stack">
  <div class="wa-flank" style="--flank-size: 200px;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank" style="--flank-size: 6rem;">
    <div></div>
    <div></div>
  </div>
</div>
```

The main content fills the remaining inline space of the container. By default, the items wrap when the main content is less than 50% of the container. You can change the minimum size of the main content with the `--content-percentage` property.

```html
<div class="wa-stack">
  <div class="wa-flank" style="--content-percentage: 70%;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank" style="--content-percentage: 85%;">
    <div></div>
    <div></div>
  </div>
</div>
```

## Align Items

By default, items are centered in the block direction of the `wa-flank` container. You can add any of the following [`wa-align-items-*`](https://webawesome.com/docs/utilities/align-items) classes to an element with `wa-flank` to specify how items are aligned in the block direction:

-   `wa-align-items-start`
-   `wa-align-items-end`
-   `wa-align-items-center`
-   `wa-align-items-stretch`
-   `wa-align-items-baseline`

```html
<div class="wa-stack">
  <div class="wa-flank wa-align-items-start" style="min-height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank wa-align-items-end" style="min-height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank wa-align-items-center" style="min-height: 8rem;">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank wa-align-items-stretch" style="min-height: 8rem;">
    <div></div>
    <div></div>
  </div>
</div>
```

## Gap

By default, the gap between flank items uses `--wa-space-m` from your theme. You can add any of the following [`wa-gap-*`](https://webawesome.com/docs/utilities/gap) classes to an element with `wa-flank` to specify the gap between items:

-   `wa-gap-0`
-   `wa-gap-3xs`
-   `wa-gap-2xs`
-   `wa-gap-xs`
-   `wa-gap-s`
-   `wa-gap-m`
-   `wa-gap-l`
-   `wa-gap-xl`
-   `wa-gap-2xl`
-   `wa-gap-3xl`

```html
<div class="wa-stack">
  <div class="wa-flank wa-gap-2xs">
    <div></div>
    <div></div>
  </div>
  <div class="wa-flank wa-gap-2xl">
    <div></div>
    <div></div>
  </div>
</div>
```

---

## Frame

Use the `wa-frame` class to create a responsive container with consistent proportions to enclose content.

```html
<div class="wa-frame" style="max-inline-size: 20rem;">
  <div></div>
</div>
```

## Examples

Frames are well-suited for images and image placeholders.

```html
<div class="wa-flank" style="--flank-size: 8rem;">
  <div class="wa-frame wa-border-radius-m">
    <img src="https://images.unsplash.com/photo-1523593288094-3ccfb6b2c192?q=20" alt="" />
  </div>
  <div class="wa-flank:end" style="--content-percentage: 70%">
    <div class="wa-stack wa-gap-xs">
      <h3>The Lord of the Rings: The Fellowship of the Ring</h3>
      <span>J.R.R. Tolkien</span>
    </div>
    <wa-button id="options-menu" appearance="plain">
      <wa-icon name="ellipsis" label="Options"></wa-icon>
    </wa-button>
    <wa-tooltip for="options-menu">Options</wa-tooltip>
  </div>
</div>
```

```html
<div class="wa-grid" style="--min-column-size: 25ch;">
  <wa-card>
    <div class="wa-frame:landscape" slot="media">
      <img src="https://images.unsplash.com/photo-1533743983669-94fa5c4338ec?q=20" alt="Grey and white tabby kitten" />
    </div>
    <div class="wa-stack wa-gap-xs">
      <h3 class="wa-heading-m">White-socks</h3>
      <span class="wa-body-s">Kitten &bull; Male</span>
      <div class="wa-flank:end wa-gap-xs">
        <wa-button size="small" appearance="filled" variant="brand">Adopt this pet</wa-button>
        <wa-button id="fav-whitesocks" appearance="plain" size="small">
          <wa-icon name="heart" variant="regular" label="Favorite"></wa-icon>
        </wa-button>
        <wa-tooltip for="fav-whitesocks">Favorite</wa-tooltip>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-frame:landscape" slot="header">
      <div class="wa-stack wa-align-items-center wa-gap-xs wa-caption-s">
        <wa-icon name="paw"></wa-icon>
        <span>Photo coming soon</span>
      </div>
    </div>
    <div class="wa-stack wa-gap-xs">
      <h3 class="wa-heading-m">Bumpkin</h3>
      <span class="wa-body-s">Adult &bull; Male</span>
      <div class="wa-flank:end wa-gap-xs">
        <wa-button size="small" appearance="filled" variant="brand">Adopt this pet</wa-button>
        <wa-button id="fav-bumpkin" appearance="plain" size="small">
          <wa-icon name="heart" variant="regular" label="Favorite"></wa-icon>
        </wa-button>
        <wa-tooltip for="fav-bumpkin">Favorite</wa-tooltip>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-frame:landscape" slot="media">
      <img src="https://images.unsplash.com/photo-1445499348736-29b6cdfc03b9?q=20" alt="Diluted calico kitten" />
    </div>
    <div class="wa-stack wa-gap-xs">
      <h3 class="wa-heading-m">Swish-tail</h3>
      <span class="wa-body-s">Kitten &bull; Female</span>
      <div class="wa-flank:end wa-gap-xs">
        <wa-button size="small" appearance="filled" variant="brand">Adopt this pet</wa-button>
        <wa-button id="fav-swishtail" appearance="plain" size="small">
          <wa-icon name="heart" variant="regular" label="Favorite"></wa-icon>
        </wa-button>
        <wa-tooltip for="fav-swishtail">Favorite</wa-tooltip>
      </div>
    </div>
  </wa-card>
  <wa-card>
    <div class="wa-frame:landscape" slot="media">
      <img src="https://images.unsplash.com/photo-1517451330947-7809dead78d5?q=20" alt="Short-haired tabby cat" />
    </div>
    <div class="wa-stack wa-gap-xs">
      <h3 class="wa-heading-m">Sharp-ears</h3>
      <span class="wa-body-s">Adult &bull; Female</span>
      <div class="wa-flank:end wa-gap-xs">
        <wa-button size="small" appearance="filled" variant="brand">Adopt this pet</wa-button>
        <wa-button id="fav-sharpears" appearance="plain" size="small">
          <wa-icon name="heart" variant="regular" label="Favorite"></wa-icon>
        </wa-button>
        <wa-tooltip for="fav-sharpears">Favorite</wa-tooltip>
      </div>
    </div>
  </wa-card>
</div>
```

## Aspect Ratio

Frames have a square aspect ratio by default. You can append `:square` (1 / 1), `:landscape` (16 / 9), or `:portrait` (9 / 16) to the `wa-frame` class in your markup to specify an aspect ratio for the frame. Alternatively, you can define the `aspect-ratio` property to set a custom proportion.

```html
<div class="wa-grid">
  <div class="wa-frame:landscape">
    <div></div>
  </div>
  <div class="wa-frame:portrait">
    <div></div>
  </div>
  <div class="wa-frame" style="aspect-ratio: 4 / 3;">
    <div></div>
  </div>
</div>
```

## Border Radius

Frames have a square border radius by default. You can add any of the following [`wa-border-radius-*`](https://webawesome.com/docs/utilities/rounding) classes to an element with `wa-frame` to specify the border radius:

-   `wa-border-radius-s`
-   `wa-border-radius-m`
-   `wa-border-radius-l`
-   `wa-border-radius-pill`
-   `wa-border-radius-circle`
-   `wa-border-radius-square`

Alternatively, you can define the `border-radius` property to set custom rounding.

```html
<div class="wa-grid">
  <div class="wa-frame wa-border-radius-l">
    <div></div>
  </div>
  <div class="wa-frame wa-border-radius-circle">
    <div></div>
  </div>
  <div class="wa-frame" style="border-radius: 50% 0%;">
    <div></div>
  </div>
</div>
```

---

## Gap

Web Awesome includes classes to set the `gap` property of flex and grid containers. Use them alone to create a flex container with a gap, or use them alongside other Web Awesome layout utilities, like [cluster](https://webawesome.com/docs/utilities/cluster) and [stack](https://webawesome.com/docs/utilities/stack), to change the space between items.

Besides `wa-gap-0`, which sets `gap` to zero, each class corresponds to one of the [`--wa-space-*`](https://webawesome.com/docs/tokens/space) tokens in your theme.

| Class Name | gap Value |
| --- | --- |
| \`wa-gap-0\` | \`0\` |
| \`wa-gap-3xs\` | \`--wa-space-3xs\` |
| \`wa-gap-2xs\` | \`--wa-space-2xs\` |
| \`wa-gap-xs\` | \`--wa-space-xs\` |
| \`wa-gap-s\` | \`--wa-space-s\` |
| \`wa-gap-m\` | \`--wa-space-m\` |
| \`wa-gap-l\` | \`--wa-space-l\` |
| \`wa-gap-xl\` | \`--wa-space-xl\` |
| \`wa-gap-2xl\` | \`--wa-space-2xl\` |
| \`wa-gap-3xl\` | \`--wa-space-3xl\` |
| \`wa-gap-4xl\` | \`--wa-space-4xl\` |
| \`wa-gap-5xl\` | \`--wa-space-5xl\` |

---

## Align Items

Web Awesome includes classes to set the `align-items` property of flex and grid containers. Use these `wa-align-items-*` classes alongside other Web Awesome layout utilities, like [cluster](https://webawesome.com/docs/utilities/cluster) and [stack](https://webawesome.com/docs/utilities/stack), to align items in a container on the container's [cross axis](#whats-the-cross-axis).

| Class Name | align-items Value |
| --- | --- |
| \`wa-align-items-baseline\` | \`baseline\` |
| \`wa-align-items-center\` | \`center\` |
| \`wa-align-items-end\` | \`flex-end\` |
| \`wa-align-items-start\` | \`flex-start\` |
| \`wa-align-items-stretch\` | \`stretch\` |

## Override with Align Self

When you need a flex or grid item to deviate from the `align-items` property of its container, use the `wa-align-self-*` classes to set the item's `align-self` property and individually change its alignment on the container's [cross axis](#whats-the-cross-axis).

| Class Name | align-self Value |
| --- | --- |
| \`wa-align-self-center\` | \`center\` |
| \`wa-align-self-baseline\` | \`baseline\` |
| \`wa-align-self-end\` | \`flex-end\` |
| \`wa-align-self-start\` | \`flex-start\` |
| \`wa-align-self-stretch\` | \`stretch\` |

## What's the Cross Axis?

The cross axis runs perpendicular to a container's content direction. For containers where `flex-direction` is `row` and content flows in the inline direction, the cross axis runs in the block direction. For containers where `flex-direction` is `column` and content flows in the block direction, the cross axis runs in the inline direction.

---

## Justify Content

Web Awesome includes classes to set the `justify-content` property of flex and grid containers. Use them alongside other Web Awesome layout utilities, like [cluster](https://webawesome.com/docs/utilities/cluster) and [stack](https://webawesome.com/docs/utilities/stack), to distribute space between items along the container's [main axis](#whats-the-main-axis).

| Class Name | justify-content Value |
| --- | --- |
| \`wa-justify-content-start\` | \`flex-start\` |
| \`wa-justify-content-end\` | \`flex-end\` |
| \`wa-justify-content-center\` | \`center\` |
| \`wa-justify-content-space-around\` | \`space-around\` |
| \`wa-justify-content-space-between\` | \`space-between\` |
| \`wa-justify-content-space-evenly\` | \`space-evenly\` |

## What's the Main Axis?

The main axis runs parallel to a container's content direction. For grid containers and flex containers where `flex-direction` is `row`, the main axis runs in the inline direction. For containers where `flex-direction` is `column`, the main axis runs in the block direction.

---