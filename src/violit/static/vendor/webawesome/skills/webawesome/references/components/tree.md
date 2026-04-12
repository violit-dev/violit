# Tree

**Full documentation:** https://webawesome.com/docs/components/tree


`<wa-tree>` Since 2.0 Stable

Trees allow you to display a hierarchical list of selectable [tree items](https://webawesome.com/docs/components/tree-item). Items with children can be expanded and collapsed as desired by the user.

```html
<wa-tree style="--indent-guide-width: 1px;">
  <wa-tree-item expanded>
    Deciduous
    <wa-tree-item>Birch</wa-tree-item>
    <wa-tree-item expanded>
      Maple
      <wa-tree-item>Field maple</wa-tree-item>
      <wa-tree-item>Red maple</wa-tree-item>
      <wa-tree-item>Sugar maple</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>Oak</wa-tree-item>
    <wa-tree-item>Walnut</wa-tree-item>
  </wa-tree-item>

  <wa-tree-item>
    Coniferous
    <wa-tree-item>Cedar</wa-tree-item>
    <wa-tree-item>
      Pine
      <wa-tree-item>Eastern white pine</wa-tree-item>
      <wa-tree-item>Ponderosa pine</wa-tree-item>
      <wa-tree-item>Scots pine</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>Spruce</wa-tree-item>
    <wa-tree-item>Fir</wa-tree-item>
  </wa-tree-item>

  <wa-tree-item>
    Tropical
    <wa-tree-item>Banyan</wa-tree-item>
    <wa-tree-item>Coconut palm</wa-tree-item>
    <wa-tree-item>Mahogany</wa-tree-item>
    <wa-tree-item>Teak</wa-tree-item>
  </wa-tree-item>
</wa-tree>
```

## Examples

### Selection Modes

The `selection` attribute lets you change the selection behavior of the tree.

-   Use `single` to allow the selection of a single item (default).
-   Use `multiple` to allow the selection of multiple items.
-   Use `leaf` to only allow leaf nodes to be selected.

```html
<wa-select id="selection-mode" value="single" label="Selection">
  <wa-option value="single">Single</wa-option>
  <wa-option value="multiple">Multiple</wa-option>
  <wa-option value="leaf">Leaf</wa-option>
</wa-select>

<br />

<wa-tree class="tree-selectable">
  <wa-tree-item expanded>
    Electronics
    <wa-tree-item expanded>
      Computers
      <wa-tree-item>Laptops</wa-tree-item>
      <wa-tree-item>Desktops</wa-tree-item>
      <wa-tree-item>Tablets</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>
      Phones
      <wa-tree-item>Smartphones</wa-tree-item>
      <wa-tree-item>Accessories</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>
  <wa-tree-item>
    Clothing
    <wa-tree-item>Shirts</wa-tree-item>
    <wa-tree-item>Pants</wa-tree-item>
    <wa-tree-item>Shoes</wa-tree-item>
  </wa-tree-item>
  <wa-tree-item>Books</wa-tree-item>
</wa-tree>

<script>
  const selectionMode = document.querySelector('#selection-mode');
  const tree = document.querySelector('.tree-selectable');

  selectionMode.addEventListener('change', () => {
    tree.querySelectorAll('wa-tree-item').forEach(item => (item.selected = false));
    tree.selection = selectionMode.value;
  });
</script>
```

### Size

Trees inherit their font size by default. You can change the size of a tree and all of its items by setting `font-size` on the `<wa-tree>` element. All internal dimensions, including checkboxes, expand buttons, and labels, scale proportionally.

```html
<wa-tree style="font-size: .75rem;" selection="multiple">
  <wa-tree-item expanded>
    Small
    <wa-tree-item>Newsletters</wa-tree-item>
    <wa-tree-item>
      Promotions
      <wa-tree-item>Weekly deals</wa-tree-item>
      <wa-tree-item>Seasonal sales</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>
</wa-tree>

<br />

<wa-tree selection="multiple">
  <wa-tree-item expanded>
    Default
    <wa-tree-item>Newsletters</wa-tree-item>
    <wa-tree-item>
      Promotions
      <wa-tree-item>Weekly deals</wa-tree-item>
      <wa-tree-item>Seasonal sales</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>
</wa-tree>

<br />

<wa-tree style="font-size: 1.5rem;" selection="multiple">
  <wa-tree-item expanded>
    Large
    <wa-tree-item>Newsletters</wa-tree-item>
    <wa-tree-item>
      Promotions
      <wa-tree-item>Weekly deals</wa-tree-item>
      <wa-tree-item>Seasonal sales</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>
</wa-tree>
```

### Showing Indent Guides

Indent guides can be drawn by setting `--indent-guide-width`. You can also change the color, offset, and style, using `--indent-guide-color`, `--indent-guide-style`, and `--indent-guide-offset`, respectively.

```html
<wa-tree class="tree-with-lines">
  <wa-tree-item expanded>
    Design
    <wa-tree-item expanded>
      Brand
      <wa-tree-item>Colors</wa-tree-item>
      <wa-tree-item>Typography</wa-tree-item>
      <wa-tree-item>Logo</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>
      Components
      <wa-tree-item>Buttons</wa-tree-item>
      <wa-tree-item>Forms</wa-tree-item>
      <wa-tree-item>Navigation</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>

  <wa-tree-item expanded>
    Development
    <wa-tree-item>Frontend</wa-tree-item>
    <wa-tree-item>Backend</wa-tree-item>
    <wa-tree-item>Infrastructure</wa-tree-item>
  </wa-tree-item>

  <wa-tree-item>
    Marketing
    <wa-tree-item>Social Media</wa-tree-item>
    <wa-tree-item>Email Campaigns</wa-tree-item>
    <wa-tree-item>Analytics</wa-tree-item>
  </wa-tree-item>
</wa-tree>

<style>
  .tree-with-lines {
    --indent-guide-width: 1px;
  }
</style>
```

### Lazy Loading

Use the `lazy` attribute on a tree item to indicate that the content is not yet present and will be loaded later. When the user tries to expand the node, the `loading` state is set to `true` and the `wa-lazy-load` event will be emitted to allow you to load data asynchronously. The item will remain in a loading state until its content is changed.

If you want to disable this behavior after the first load, simply remove the `lazy` attribute and, on the next expand, the existing content will be shown instead.

```html
<wa-tree>
  <wa-tree-item lazy>Remote Repositories</wa-tree-item>
</wa-tree>

<script type="module">
  const lazyItem = document.querySelector('wa-tree-item[lazy]');

  lazyItem.addEventListener('wa-lazy-load', () => {
    // Simulate fetching data from a server
    setTimeout(() => {
      const repos = ['design-system', 'marketing-site', 'mobile-app', 'api-gateway'];

      for (const repo of repos) {
        const treeItem = document.createElement('wa-tree-item');
        treeItem.innerText = repo;
        lazyItem.append(treeItem);
      }

      // Disable lazy mode once the content has been loaded
      lazyItem.lazy = false;
    }, 1000);
  });
</script>
```

### Customizing the Expand and Collapse Icons

Use the `expand-icon` and `collapse-icon` slots to change the expand and collapse icons, respectively. To disable the animation, override the `rotate` property on the `expand-button` part as shown below.

```html
<wa-tree class="custom-icons">
  <wa-icon name="square-plus" variant="solid" slot="expand-icon"></wa-icon>
  <wa-icon name="square-minus" variant="solid" slot="collapse-icon"></wa-icon>

  <wa-tree-item expanded>
    Recipes
    <wa-tree-item expanded>
      Breakfast
      <wa-tree-item>Pancakes</wa-tree-item>
      <wa-tree-item>Omelette</wa-tree-item>
      <wa-tree-item>Granola</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>
      Lunch
      <wa-tree-item>Caesar salad</wa-tree-item>
      <wa-tree-item>Grilled chicken wrap</wa-tree-item>
    </wa-tree-item>
    <wa-tree-item>
      Dinner
      <wa-tree-item>Pasta carbonara</wa-tree-item>
      <wa-tree-item>Stir fry</wa-tree-item>
      <wa-tree-item>Roasted salmon</wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>

  <wa-tree-item>
    Desserts
    <wa-tree-item>Chocolate cake</wa-tree-item>
    <wa-tree-item>Tiramisu</wa-tree-item>
    <wa-tree-item>Fruit tart</wa-tree-item>
  </wa-tree-item>
</wa-tree>

<style>
  .custom-icons wa-tree-item::part(expand-button) {
    /* Disable the expand/collapse animation */
    rotate: none;
  }
</style>
```

### With Icons

Decorative icons can be used before labels to provide hints for each node.

```html
<wa-tree class="tree-with-icons">
  <wa-tree-item expanded>
    <wa-icon name="folder" variant="regular"></wa-icon>
    Documents

    <wa-tree-item expanded>
      <wa-icon name="folder" variant="regular"></wa-icon>
      Photos
      <wa-tree-item>
        <wa-icon name="image" variant="regular"></wa-icon>
        vacation.jpg
      </wa-tree-item>
      <wa-tree-item>
        <wa-icon name="image" variant="regular"></wa-icon>
        family-portrait.png
      </wa-tree-item>
      <wa-tree-item>
        <wa-icon name="image" variant="regular"></wa-icon>
        sunset.jpg
      </wa-tree-item>
    </wa-tree-item>

    <wa-tree-item expanded>
      <wa-icon name="folder" variant="regular"></wa-icon>
      Work
      <wa-tree-item>
        <wa-icon name="file-pdf" variant="regular"></wa-icon>
        quarterly-report.pdf
      </wa-tree-item>
      <wa-tree-item>
        <wa-icon name="file-lines" variant="regular"></wa-icon>
        budget.xls
      </wa-tree-item>
      <wa-tree-item>
        <wa-icon name="file" variant="regular"></wa-icon>
        meeting-notes.txt
      </wa-tree-item>
    </wa-tree-item>

    <wa-tree-item>
      <wa-icon name="folder" variant="regular"></wa-icon>
      Personal
      <wa-tree-item>
        <wa-icon name="file" variant="regular"></wa-icon>
        journal.txt
      </wa-tree-item>
      <wa-tree-item>
        <wa-icon name="file-pdf" variant="regular"></wa-icon>
        resume.pdf
      </wa-tree-item>
    </wa-tree-item>
  </wa-tree-item>

  <wa-tree-item>
    <wa-icon name="folder" variant="regular"></wa-icon>
    Downloads
    <wa-tree-item>
      <wa-icon name="file-zipper" variant="regular"></wa-icon>
      archive.zip
    </wa-tree-item>
    <wa-tree-item>
      <wa-icon name="file" variant="regular"></wa-icon>
      readme.txt
    </wa-tree-item>
  </wa-tree-item>
</wa-tree>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/tree/tree.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaTree from '@awesome.me/webawesome/dist/react/tree';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The default slot. |
| \`collapse-icon\` | \`\` The icon to show when the tree item is expanded. Works best with . |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`selection\` selection | \`'single' \\| 'multiple' \\| 'leaf'\` The selection behavior of the tree. Single selection allows only one node to be selected at a time. Multiple displays checkboxes and allows more than one node to be selected. Leaf allows only leaf nodes to be selected. Type Default 'single' | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-selection-change\` | Emitted when a tree item is selected or deselected. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--indent-guide-color\` | \`var(--wa-color-surface-border)\` The color of the indentation line. Default |
| \`--indent-guide-offset\` | \`0\` The amount of vertical spacing to leave between the top and bottom of the indentation line's starting position. Default |
| \`--indent-guide-style\` | \`solid\` The style of the indentation line, e.g. , dotted, dashed. Default solid |
| \`--indent-guide-width\` | \`0\` The width of the indentation line. Default |
| \`--indent-size\` | \`var(--wa-space-m)\` The size of the indentation for nested items. Default |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The component's base wrapper. | \`::part(base)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-checkbox>`](https://webawesome.com/docs/components/checkbox)
-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)
-   [`<wa-spinner>`](https://webawesome.com/docs/components/spinner)
-   [`<wa-tree-item>`](https://webawesome.com/docs/components/tree-item)

**Need a hand?** Report a bug Ask for help