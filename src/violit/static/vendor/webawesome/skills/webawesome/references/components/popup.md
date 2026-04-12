# Popup

**Full documentation:** https://webawesome.com/docs/components/popup


`<wa-popup>` Since 2.0 Stable

Popup is a utility that lets you declaratively anchor "popup" containers to another element.

This component's name is inspired by [`<popup>`](https://github.com/MicrosoftEdge/MSEdgeExplainers/blob/main/Popup/explainer.md). It uses [Floating UI](https://floating-ui.com/) under the hood to provide a well-tested, lightweight, and fully declarative positioning utility for tooltips, dropdowns, and more.

Popup doesn't provide any styles — just positioning! The popup's preferred placement, distance, and skidding (offset) can be configured using attributes. An arrow that points to the anchor can be shown and customized to your liking. Additional positioning options are available and described in more detail below.

Popup is a low-level utility built specifically for positioning elements. Do not mistake it for a [tooltip](https://webawesome.com/docs/components/tooltip) or similar because _it does not facilitate an accessible experience!_ Almost every correct usage of `<wa-popup>` will involve building other components. It should rarely, if ever, occur directly in your HTML.

```html
<div class="popup-overview">
  <wa-popup placement="top" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <div class="popup-overview-options">
    <wa-combobox label="Placement" name="placement" placeholder="Select placement..." class="popup-overview-select"></wa-combobox>
    <wa-input type="number" name="distance" label="distance" value="0"></wa-input>
    <wa-input type="number" name="skidding" label="Skidding" value="0"></wa-input>
  </div>

  <div class="popup-overview-options">
    <wa-switch name="active" checked>Active</wa-switch>
    <wa-switch name="arrow">Arrow</wa-switch>
  </div>
</div>

<script type="module">
  await customElements.whenDefined('wa-combobox');
  await customElements.whenDefined('wa-option');

  const container = document.querySelector('.popup-overview');
  const popup = container.querySelector('wa-popup');
  const placement = container.querySelector('wa-combobox[name="placement"]');
  const distance = container.querySelector('wa-input[name="distance"]');
  const skidding = container.querySelector('wa-input[name="skidding"]');
  const active = container.querySelector('wa-switch[name="active"]');
  const arrow = container.querySelector('wa-switch[name="arrow"]');

  const placements = ['top', 'top-start', 'top-end', 'bottom', 'bottom-start', 'bottom-end', 'right', 'right-start', 'right-end', 'left', 'left-start', 'left-end'];

  placements.forEach(value => {
    const option = document.createElement('wa-option');
    option.value = value;
    option.textContent = value;
    placement.append(option);
  });

  await placement.updateComplete;

  placement.value = 'top';

  placement.addEventListener('change', () => (popup.placement = placement.value));
  distance.addEventListener('input', () => (popup.distance = distance.value));
  skidding.addEventListener('input', () => (popup.skidding = skidding.value));
  active.addEventListener('change', () => (popup.active = active.checked));
  arrow.addEventListener('change', () => (popup.arrow = arrow.checked));
</script>

<style>
  .popup-overview wa-popup {
    --arrow-color: var(--wa-color-brand-fill-loud);
  }

  .popup-overview span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-overview .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }

  .popup-overview-options {
    display: flex;
    flex-wrap: wrap;
    align-items: end;
    gap: 1rem;
  }

  .popup-overview-options wa-combobox {
    width: 160px;
  }

  .popup-overview-options wa-input {
    width: 100px;
  }

  .popup-overview-options + .popup-overview-options {
    margin-top: 1rem;
  }
</style>
```

A popup's anchor should not be styled with `display: contents` since the coordinates will not be eligible for calculation. However, if the anchor is a `<slot>` element, popup will use the first assigned element as the anchor. This behavior allows other components to pass anchors through more easily via composition.

## Examples

### Activating

Popups are inactive and hidden until the `active` attribute is applied. Removing the attribute will tear down all positioning logic and listeners, meaning you can have many idle popups on the page without affecting performance.

```html
<div class="popup-active">
  <wa-popup placement="top" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <br />
  <wa-switch checked>Active</wa-switch>
</div>

<style>
  .popup-active span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-active .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }
</style>

<script>
  const container = document.querySelector('.popup-active');
  const popup = container.querySelector('wa-popup');
  const active = container.querySelector('wa-switch');

  active.addEventListener('change', () => (popup.active = active.checked));
</script>
```

### External Anchors

By default, anchors are slotted into the popup using the `anchor` slot. If your anchor needs to live outside of the popup, you can pass the anchor's `id` to the `anchor` attribute. Alternatively, you can pass an element reference to the `anchor` property to achieve the same effect without using an `id`.

```html
<span id="external-anchor"></span>

<wa-popup anchor="external-anchor" placement="top" active>
  <div class="box"></div>
</wa-popup>

<style>
  #external-anchor {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px 0 0 50px;
  }

  #external-anchor ~ wa-popup .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }
</style>
```

### Placement

Use the `placement` attribute to tell the popup the preferred placement of the popup. Note that the actual position will vary to ensure the panel remains in the viewport if you're using positioning features such as `flip` and `shift`.

Since placement is preferred when using `flip`, you can observe the popup's current placement when it's active by looking at the `data-current-placement` attribute. This attribute will update as the popup flips to find available space and it will be removed when the popup is deactivated.

```html
<div class="popup-placement">
  <wa-popup placement="top" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <wa-combobox name="placement" label="Placement" placeholder="Select placement..."></wa-combobox>
</div>

<style>
  .popup-placement span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-placement .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }

  .popup-placement wa-combobox {
    max-width: 280px;
  }
</style>

<script type="module">
  await customElements.whenDefined('wa-combobox');
  await customElements.whenDefined('wa-option');

  const container = document.querySelector('.popup-placement');
  const popup = container.querySelector('wa-popup');
  const placement = container.querySelector('wa-combobox');

  const placements = ['top', 'top-start', 'top-end', 'bottom', 'bottom-start', 'bottom-end', 'right', 'right-start', 'right-end', 'left', 'left-start', 'left-end'];

  placements.forEach(value => {
    const option = document.createElement('wa-option');
    option.value = value;
    option.textContent = value;
    placement.append(option);
  });

  await placement.updateComplete;

  placement.value = 'top';

  placement.addEventListener('change', () => (popup.placement = placement.value));
</script>
```

### Distance

Use the `distance` attribute to change the distance between the popup and its anchor. A positive value will move the popup further away and a negative value will move it closer.

```html
<div class="popup-distance">
  <wa-popup placement="top" distance="0" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <wa-slider min="-50" max="50" step="1" value="0" label="Distance"></wa-slider>
</div>

<style>
  .popup-distance span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-distance .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }

  .popup-distance wa-slider {
    max-width: 260px;
  }
</style>

<script>
  const container = document.querySelector('.popup-distance');
  const popup = container.querySelector('wa-popup');
  const distance = container.querySelector('wa-slider');

  distance.addEventListener('input', () => (popup.distance = distance.value));
</script>
```

### Skidding

The `skidding` attribute is similar to `distance`, but instead allows you to offset the popup along the anchor's axis. Both positive and negative values are allowed.

```html
<div class="popup-skidding">
  <wa-popup placement="top" skidding="0" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <wa-slider min="-50" max="50" step="1" value="0" label="Skidding"></wa-slider>
</div>

<style>
  .popup-skidding span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-skidding .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }

  .popup-skidding wa-slider {
    max-width: 260px;
  }
</style>

<script>
  const container = document.querySelector('.popup-skidding');
  const popup = container.querySelector('wa-popup');
  const skidding = container.querySelector('wa-slider');

  skidding.addEventListener('input', () => (popup.skidding = skidding.value));
</script>
```

### Arrows

Add an arrow to your popup with the `arrow` attribute. It's usually a good idea to set a `distance` to make room for the arrow. To adjust the arrow's color and size, use the `--arrow-color` and `--arrow-size` custom properties, respectively. You can also target the `arrow` part to add additional styles such as shadows and borders to match styles applied to rest of the popup element.

By default, the arrow will be aligned as close to the center of the _anchor_ as possible, considering available space and `arrow-padding`. You can use the `arrow-placement` attribute to force the arrow to align to the start, end, or center of the _popup_ instead.

```html
<div class="popup-arrow">
  <wa-popup placement="top" arrow arrow-placement="anchor" distance="8" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <div class="popup-arrow-options">
    <wa-combobox label="Placement" name="placement" placeholder="Select placement..." class="popup-overview-select"></wa-combobox>

    <wa-select label="Arrow Placement" name="arrow-placement" value="anchor">
      <wa-option value="anchor">anchor</wa-option>
      <wa-option value="start">start</wa-option>
      <wa-option value="end">end</wa-option>
      <wa-option value="center">center</wa-option>
    </wa-select>
  </div>

  <div class="popup-arrow-options">
    <wa-switch name="arrow" checked>Arrow</wa-switch>
  </div>

  <style>
    .popup-arrow wa-popup {
      --arrow-color: var(--wa-color-brand-fill-loud);
    }

    .popup-arrow span[slot='anchor'] {
      display: inline-block;
      width: 150px;
      height: 150px;
      border: dashed 2px var(--wa-color-neutral-fill-loud);
      margin: 50px;
    }

    .popup-arrow .box {
      width: 100px;
      height: 50px;
      background: var(--wa-color-brand-fill-loud);
      border-radius: var(--wa-border-radius-m);
    }

    .popup-arrow-options {
      display: flex;
      flex-wrap: wrap;
      align-items: end;
      gap: 1rem;
    }

    .popup-arrow-options wa-combobox,
    .popup-arrow-options wa-select {
      width: 160px;
    }

    .popup-arrow-options + .popup-arrow-options {
      margin-top: 1rem;
    }
  </style>

  <script type="module">
    await customElements.whenDefined('wa-combobox');
    await customElements.whenDefined('wa-option');

    const container = document.querySelector('.popup-arrow');
    const popup = container.querySelector('wa-popup');
    const placement = container.querySelector('wa-combobox[name="placement"]');
    const arrowPlacement = container.querySelector('wa-select[name="arrow-placement"]');
    const arrow = container.querySelector('[name="arrow"]');

    const placements = ['top', 'top-start', 'top-end', 'bottom', 'bottom-start', 'bottom-end', 'right', 'right-start', 'right-end', 'left', 'left-start', 'left-end'];

    placements.forEach(value => {
      const option = document.createElement('wa-option');
      option.value = value;
      option.textContent = value;
      placement.append(option);
    });

    await placement.updateComplete;

    placement.value = 'top';

    placement.addEventListener('change', () => (popup.placement = placement.value));
    arrowPlacement.addEventListener('change', () => (popup.arrowPlacement = arrowPlacement.value));
    arrow.addEventListener('change', () => (popup.arrow = arrow.checked));
  </script>
</div>
```

### Adding a border

Borders can also be added to the popup element by targeting the contents of the `wa-popup` element. This styling can also be extended to the arrow itself by targeting `.arrow` class in the popup.

When adding borders to the popup element which has an arrow, make sure to set the `--popup-border-width` custom property to match the width of the border of the popup. Setting this will allow the arrow to overlap the border of the popup so that they visually appear connected.

```html
<div class="popup-border">
  <wa-popup placement="top" arrow arrow-placement="anchor" distance="8" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>

  <div class="popup-border-options">
    <wa-combobox label="Placement" name="placement" placeholder="Select placement..." class="popup-overview-select"></wa-combobox>
  </div>

  <style>
    
    .popup-border span[slot='anchor'] {
      display: inline-block;
      width: 150px;
      height: 150px;
      border: dashed 2px var(--wa-color-neutral-fill-loud);
      margin: 50px;
    }

    .popup-border .box {
      width: 100px;
      height: 50px;
      background: var(--wa-color-brand-on-loud);
      border-radius: var(--wa-border-radius-m);
      border: var(--wa-panel-border-width) solid var(--wa-color-brand-border-loud);
      border-style: var(--wa-panel-border-style);
      box-shadow: var(--wa-shadow-l);
    }
    
    .popup-border wa-popup {
      --arrow-color: var(--wa-color-brand-on-loud);
      --popup-border-width: var(--wa-panel-border-width);

      &::part(arrow) {
        border-bottom: var(--wa-panel-border-width) var(--wa-panel-border-style) var(--wa-color-brand-border-loud);
        border-right: var(--wa-panel-border-width) var(--wa-panel-border-style) var(--wa-color-brand-border-loud);
      }
    }

    .popup-border-options {
      display: flex;
      flex-wrap: wrap;
      align-items: end;
      gap: 1rem;
    }

    .popup-border-options wa-combobox {
      width: 160px;
    }
  </style>
  
  <script type="module">
    await customElements.whenDefined('wa-combobox');

    const container = document.querySelector('.popup-border');
    const popup = container.querySelector('wa-popup');
    const placement = container.querySelector('wa-combobox[name="placement"]');

    const placements = ['top', 'top-start', 'top-end', 'bottom', 'bottom-start', 'bottom-end', 'right', 'right-start', 'right-end', 'left', 'left-start', 'left-end'];

    placements.forEach(value => {
      const option = document.createElement('wa-option');
      option.value = value;
      option.textContent = value;
      placement.append(option);
    });

    await placement.updateComplete;

    placement.value = 'top';

    placement.addEventListener('change', () => (popup.placement = placement.value));
  </script>
</div>
```

### Flip

When the popup doesn't have enough room in its preferred placement, it can automatically flip to keep it in view and visually connected to its anchor. To enable this, use the `flip` attribute. By default, the popup will flip to the opposite placement, but you can configure preferred fallback placements using `flip-fallback-placement` and `flip-fallback-strategy`. Additional options are available to control the flip behavior's boundary and padding.

By default, flip takes effect when the popup would overflow the viewport. You can use `boundary="scroll"` to make the popup resize when it overflows its nearest scrollable container instead.

Scroll the container to see how the popup flips to prevent clipping.

```html
<div class="popup-flip">
  <div class="overflow">
    <wa-popup placement="top" flip active boundary="scroll">
      <span slot="anchor"></span>
      <div class="box"></div>
    </wa-popup>
  </div>

  <br />
  <wa-switch checked>Flip</wa-switch>
</div>

<style>
  .popup-flip .overflow {
    position: relative;
    height: 300px;
    border: solid 2px var(--wa-color-surface-border);
    overflow: auto;
  }

  .popup-flip span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 150px 50px;
  }

  .popup-flip .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }
</style>

<script>
  const container = document.querySelector('.popup-flip');
  const popup = container.querySelector('wa-popup');
  const flip = container.querySelector('wa-switch');

  flip.addEventListener('change', () => (popup.flip = flip.checked));
</script>
```

### Flip Fallbacks

While using the `flip` attribute, you can customize the placement of the popup when the preferred placement doesn't have room. For this, use `flip-fallback-placements` and `flip-fallback-strategy`.

If the preferred placement doesn't have room, the first suitable placement found in `flip-fallback-placement` will be used. The value of this attribute must be a string including any number of placements separated by a space, e.g. `"right bottom"`.

If no fallback placement works, the final placement will be determined by `flip-fallback-strategy`. This value can be either `initial` (default), where the placement reverts to the position in `placement`, or `best-fit`, where the placement is chosen based on available space.

Scroll the container to see how the popup changes it's fallback placement to prevent clipping.

```html
<div class="popup-flip-fallbacks">
  <div class="overflow">
    <wa-popup
      placement="top"
      flip
      flip-fallback-placements="right bottom"
      flip-fallback-strategy="initial"
      active
      boundary="scroll"
    >
      <span slot="anchor"></span>
      <div class="box"></div>
    </wa-popup>
  </div>
</div>

<style>
  .popup-flip-fallbacks .overflow {
    position: relative;
    height: 300px;
    border: solid 2px var(--wa-color-surface-border);
    overflow: auto;
  }

  .popup-flip-fallbacks span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 250px 50px;
  }

  .popup-flip-fallbacks .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }
</style>
```

### Shift

When a popup is longer than its anchor, it risks overflowing. In this case, use the `shift` attribute to shift the popup along its axis and back into view. You can customize the shift behavior using `shiftBoundary` and `shift-padding`.

By default, auto-size takes effect when the popup would overflow the viewport. You can use `boundary="scroll"` to make the popup resize when it overflows its nearest scrollable container instead.

Toggle the switch to see the difference.

```html
<div class="popup-shift">
  <div class="overflow">
    <wa-popup placement="top" shift shift-padding="10" active boundary="scroll">
      <span slot="anchor"></span>
      <div class="box"></div>
    </wa-popup>
  </div>

  <wa-switch checked>Shift</wa-switch>
</div>

<style>
  .popup-shift .overflow {
    position: relative;
    border: solid 2px var(--wa-color-surface-border);
    overflow: auto;
  }

  .popup-shift span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 60px 0 0 10px;
  }

  .popup-shift .box {
    width: 300px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }
</style>

<script>
  const container = document.querySelector('.popup-shift');
  const popup = container.querySelector('wa-popup');
  const shift = container.querySelector('wa-switch');

  shift.addEventListener('change', () => (popup.shift = shift.checked));
</script>
```

### Auto-size

Use the `auto-size` attribute to tell the popup to resize when necessary to prevent it from overflowing. Possible values are `horizontal`, `vertical`, and `both`. You can use `autoSizeBoundary` and `auto-size-padding` to customize the behavior of this option. Auto-size works well with `flip`, but if you're using `auto-size-padding` make sure `flip-padding` is the same value.

By default, auto-size takes effect when the popup would overflow the viewport. You can use `boundary="scroll"` to make the popup resize when it overflows its nearest scrollable container instead.

When using `auto-size`, one or both of `--auto-size-available-width` and `--auto-size-available-height` will be applied to the host element. These values determine the available space the popover has before clipping will occur. Since they cascade, you can use them to set a max-width/height on your popup's content and easily control its overflow.

Scroll the container to see the popup resize as its available space changes.

```html
<div class="popup-auto-size">
  <div class="overflow">
    <wa-popup placement="top" auto-size="both" auto-size-padding="10" active boundary="scroll">
      <span slot="anchor"></span>
      <div class="box"></div>
    </wa-popup>
  </div>

  <br />
  <wa-switch checked>Auto-size</wa-switch>
</div>

<style>
  .popup-auto-size .overflow {
    position: relative;
    height: 300px;
    border: solid 2px var(--wa-color-surface-border);
    overflow: auto;
  }

  .popup-auto-size span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 250px 50px 100px 50px;
  }

  .popup-auto-size .box {
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);

    /* This sets the preferred size of the popup's content */
    width: 100px;
    height: 200px;

    /* This sets the maximum dimensions and allows scrolling when auto-size kicks in */
    max-width: var(--auto-size-available-width);
    max-height: var(--auto-size-available-height);
    overflow: auto;
  }
</style>

<script>
  const container = document.querySelector('.popup-auto-size');
  const popup = container.querySelector('wa-popup');
  const autoSize = container.querySelector('wa-switch');

  autoSize.addEventListener('change', () => (popup.autoSize = autoSize.checked ? 'both' : ''));
</script>
```

### Hover Bridge

When a gap exists between the anchor and the popup element, this option will add a "hover bridge" that fills the gap using an invisible element. This makes listening for events such as `mouseover` and `mouseout` more sane because the pointer never technically leaves the element. The hover bridge will only be drawn when the popover is active. For demonstration purposes, the bridge in this example is shown in orange.

```html
<div class="popup-hover-bridge">
  <wa-popup placement="top" hover-bridge distance="10" skidding="0" active>
    <span slot="anchor"></span>
    <div class="box"></div>
  </wa-popup>
  <br />
  <wa-switch checked>Hover Bridge</wa-switch><br />
  <wa-slider min="0" max="50" step="1" value="10" label="Distance"></wa-slider>
  <wa-slider min="-50" max="50" step="1" value="0" label="Skidding"></wa-slider>
</div>
<style>
  .popup-hover-bridge span[slot='anchor'] {
    display: inline-block;
    width: 150px;
    height: 150px;
    border: dashed 2px var(--wa-color-neutral-fill-loud);
    margin: 50px;
  }

  .popup-hover-bridge .box {
    width: 100px;
    height: 50px;
    background: var(--wa-color-brand-fill-loud);
    border-radius: var(--wa-border-radius-m);
  }

  .popup-hover-bridge wa-slider {
    max-width: 260px;
    margin-top: 0.5rem;
  }

  .popup-hover-bridge wa-popup::part(hover-bridge) {
    background: tomato;
    opacity: 0.5;
  }
</style>
<script>
  const container = document.querySelector('.popup-hover-bridge');
  const popup = container.querySelector('wa-popup');
  const hoverBridge = container.querySelector('wa-switch');
  const distance = container.querySelector('wa-slider[label="Distance"]');
  const skidding = container.querySelector('wa-slider[label="Skidding"]');
  distance.addEventListener('input', () => (popup.distance = distance.value));
  skidding.addEventListener('input', () => (popup.skidding = skidding.value));
  hoverBridge.addEventListener('change', () => (popup.hoverBridge = hoverBridge.checked));
</script>
```

### Virtual Elements

In most cases, popups are anchored to an actual element. Sometimes, it can be useful to anchor them to a non-element. To do this, you can pass a `VirtualElement` to the anchor property. A virtual element must contain a function called `getBoundingClientRect()` that returns a [`DOMRect`](https://developer.mozilla.org/en-US/docs/Web/API/DOMRect) object as shown below.

```ts
const virtualElement = {
  getBoundingClientRect() {
    // ...
    return { width, height, x, y, top, left, right, bottom };
  },
};
```

This example anchors a popup to the mouse cursor using a virtual element. As such, a mouse is required to properly view it.

```html
<div class="popup-virtual-element">
  <wa-popup placement="right-start">
    <div class="circle"></div>
  </wa-popup>

  <wa-switch>Highlight mouse cursor</wa-switch>
</div>

<script>
  const container = document.querySelector('.popup-virtual-element');
  const popup = container.querySelector('wa-popup');
  const circle = container.querySelector('.circle');
  const enabled = container.querySelector('wa-switch');
  let clientX = 0;
  let clientY = 0;

  // Set the virtual element as a property
  popup.anchor = {
    getBoundingClientRect() {
      return {
        width: 0,
        height: 0,
        x: clientX,
        y: clientY,
        top: clientY,
        left: clientX,
        right: clientX,
        bottom: clientY,
      };
    },
  };

  // Only activate the popup when the switch is checked
  enabled.addEventListener('change', () => {
    popup.active = enabled.checked;
  });

  // Listen for the mouse to move
  document.addEventListener('mousemove', handleMouseMove);

  // Update the virtual element as the mouse moves
  function handleMouseMove(event) {
    clientX = event.clientX;
    clientY = event.clientY;

    // Reposition the popup when the virtual anchor moves
    if (popup.active) {
      popup.reposition();
    }
  }
</script>

<style>
  /* If you need to set a z-index, set it on the popup part like this */
  .popup-virtual-element wa-popup::part(popup) {
    z-index: 1000;
    pointer-events: none;
  }

  .popup-virtual-element .circle {
    width: 100px;
    height: 100px;
    border: solid 4px var(--wa-color-neutral-fill-loud);
    border-radius: 50%;
    translate: -50px -50px;
    animation: 1s virtual-cursor infinite;
  }

  @keyframes virtual-cursor {
    0% {
      scale: 1;
    }
    50% {
      scale: 1.1;
    }
  }
</style>
```

### Built-in Animations

The following classes can be applied to the popup's `popup` part to animate it in or out programmatically. You can control the animation duration with the `--show-duration` and `--hide-duration` custom properties.

-   `show` / `hide` - Shows or hides the popover with a fade
-   `show-with-scale` / `hide-with-scale` - Shows or hides the popover with a fade and subtle scale effect

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/popup/popup.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaPopup from '@awesome.me/webawesome/dist/react/popup';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | The popup's content. |
| \`anchor\` | \`anchor\` The element the popup will be ed to. If the anchor lives outside of the popup, you can use the anchor attribute or property instead. |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`active\` active | \`boolean\` Activates the positioning logic and shows the popup. When this attribute is removed, the positioning logic is torn down and the popup will be hidden. Type Default false | | |
| \`anchor\` anchor | \`id\` The element the popup will be anchored to. If the anchor lives outse of the popup, you can provide the anchor element id, a DOM element reference, or a VirtualElement. If the anchor lives inside the popup, use the anchor slot instead. Type Element \\| string \\| VirtualElement | | |
| \`arrow\` arrow | \`--arrow-size\` Attaches an arrow to the popup. The arrow's size and color can be customized using the and --arrow-color custom properties. For additional customizations, you can also target the arrow using ::part(arrow) in your stylesheet. Type boolean Default false | | |
| \`arrowPadding\` arrow-padding | \`number\` The amount of padding between the arrow and the edges of the popup. If the popup has a border-radius, for example, this will prevent it from overflowing the corners. Type Default 10 | | |
| \`arrowPlacement\` arrow-placement | \`anchor\` The placement of the arrow. The default is , which will align the arrow as close to the center of the anchor as possible, considering available space and arrow-padding. A value of start, end, or center will align the arrow to the start, end, or center of the popover instead. Type 'start' \\| 'end' \\| 'center' \\| 'anchor' Default 'anchor' | | |
| \`autoSize\` auto-size | \`'horizontal' \\| 'vertical' \\| 'both'\` When set, this will cause the popup to automatically resize itself to prevent it from overflowing. Type | | |
| \`autoSizeBoundary\` autoSizeBoundary | \`Element \\| Element\[\]\` The auto-size boundary describes clipping element(s) that overflow will be checked relative to when resizing. By default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can change the boundary by passing a reference to one or more elements to this property. Type | | |
| \`autoSizePadding\` auto-size-padding | \`number\` The amount of padding, in pixels, to exceed before the auto-size behavior will occur. Type Default 0 | | |
| \`boundary\` boundary | \`'viewport' \\| 'scroll'\` The bounding box to use for flipping, shifting, and auto-sizing. Type Default 'viewport' | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`distance\` distance | \`number\` The distance in pixels from which to offset the panel away from its anchor. Type Default 0 | | |
| \`flip\` flip | \`flipFallbackPlacements\` When set, placement of the popup will flip to the opposite site to keep it in view. You can use to further configure how the fallback placement is determined. Type boolean Default false | | |
| \`flipBoundary\` flipBoundary | \`Element \\| Element\[\]\` The flip boundary describes clipping element(s) that overflow will be checked relative to when flipping. By default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can change the boundary by passing a reference to one or more elements to this property. Type | | |
| \`flipFallbackPlacements\` flip-fallback-placements | \`string\` If the preferred placement doesn't fit, popup will be tested in these fallback placements until one fits. Must be a of any number of placements separated by a space, e.g. "top bottom left". If no placement fits, the flip fallback strategy will be used instead. Type string Default '' | | |
| \`flipFallbackStrategy\` flip-fallback-strategy | \`'best-fit' \\| 'initial'\` When neither the preferred placement nor the fallback placements fit, this value will be used to determine whether the popup should be positioned using the best available fit based on available space or as it was initially preferred. Type Default 'best-fit' | | |
| \`flipPadding\` flip-padding | \`number\` The amount of padding, in pixels, to exceed before the flip behavior will occur. Type Default 0 | | |
| \`hoverBridge\` hover-bridge | \`mouseenter\` When a gap exists between the anchor and the popup element, this option will add a "hover bridge" that fills the gap using an invisible element. This makes listening for events such as and mouseleave more sane because the pointer never technically leaves the element. The hover bridge will only be drawn when the popover is active. Type boolean Default false | | |
| \`placement\` placement | \`'top' \\| 'top-start' \\| 'top-end' \\| 'bottom' \\| 'bottom-start' \\| 'bottom-end' \\| 'right' \\| 'right-start' \\| 'right-end' \\| 'left' \\| 'left-start' \\| 'left-end'\` The preferred placement of the popup. Note that the actual placement will vary as configured to keep the panel inside of the viewport. Type Default 'top' | | |
| \`popup\` | \`HTMLElement\` A reference to the internal popup container. Useful for animating and styling the popup with JavaScript. Type | | |
| \`shift\` shift | \`boolean\` Moves the popup along the axis to keep it in view when clipped. Type Default false | | |
| \`shiftBoundary\` shiftBoundary | \`Element \\| Element\[\]\` The shift boundary describes clipping element(s) that overflow will be checked relative to when shifting. By default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can change the boundary by passing a reference to one or more elements to this property. Type | | |
| \`shiftPadding\` shift-padding | \`number\` The amount of padding, in pixels, to exceed before the shift behavior will occur. Type Default 0 | | |
| \`skidding\` skidding | \`number\` The distance in pixels from which to offset the panel along its anchor. Type Default 0 | | |
| \`sync\` sync | \`'width' \\| 'height' \\| 'both'\` Syncs the popup's width or height to that of the anchor element. Type | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`reposition()\` | Forces the popup to recalculate and reposition itself. | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-reposition\` | Emitted when the popup is repositioned. This event can fire a lot, so avoid putting expensive operations in your listener or consider debouncing it. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--arrow-color\` | \`black\` The color of the arrow. Default |
| \`--arrow-size\` | \`arrow\` The size of the . Note that an arrow won't be shown unless the arrow attribute is used. Default 6px |
| \`--auto-size-available-height\` | \`auto-size\` A read-only custom property that determines the amount of height the popup can be before overflowing. Useful for positioning child elements that need to overflow. This property is only available when using . |
| \`--auto-size-available-width\` | \`auto-size\` A read-only custom property that determines the amount of width the popup can be before overflowing. Useful for positioning child elements that need to overflow. This property is only available when using . |
| \`--hide-duration\` | \`100ms\` The hide duration to use when applying built-in animation classes. Default |
| \`--popup-border-width\` | The width of any custom border applied to the popup. This is used to reposition the arrow to overlap to the inside edge of the popup border. |
| \`--show-duration\` | \`100ms\` The show duration to use when applying built-in animation classes. Default |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`arrow\` | \`top\\|bottom\\|left\\|right\` The arrow's container. Avoid setting properties, as these values are assigned dynamically as the popup moves. This is most useful for applying a background color to match the popup, and maybe a border or box shadow. | \`::part(arrow)\` |
| \`hover-bridge\` | \`hover-bridge\` The hover bridge element. Only available when the option is enabled. | \`::part(hover-bridge)\` |
| \`popup\` | The popup's container. Useful for setting a background color, box shadow, etc. | \`::part(popup)\` |

**Need a hand?** Report a bug Ask for help