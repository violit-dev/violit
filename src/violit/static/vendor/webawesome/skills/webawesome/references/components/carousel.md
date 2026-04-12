# Carousel

**Full documentation:** https://webawesome.com/docs/components/carousel


`<wa-carousel>` Since 2.2 Experimental

Carousels display an arbitrary number of content slides along a horizontal or vertical axis.

```html
<wa-carousel pagination navigation mouse-dragging loop>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

## Examples

### Pagination

Use the `pagination` attribute to show the total number of slides and the current slide as a set of interactive dots.

```html
<wa-carousel pagination>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

### Navigation

Use the `navigation` attribute to show previous and next buttons.

```html
<wa-carousel navigation>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

### Looping

By default, the carousel will not advanced beyond the first and last slides. You can change this behavior and force the carousel to "wrap" with the `loop` attribute.

```html
<wa-carousel loop navigation pagination>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

### Autoplay

The carousel will automatically advance when the `autoplay` attribute is used. To change how long a slide is shown before advancing, set `autoplay-interval` to the desired number of milliseconds. For best results, use the `loop` attribute when autoplay is enabled. Note that autoplay will pause while the user interacts with the carousel.

```html
<wa-carousel autoplay loop pagination>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

### Mouse Dragging

The carousel uses [scroll snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap) to position slides at various snap positions. This allows users to scroll through the slides very naturally, especially on touch devices. Unfortunately, desktop users won't be able to click and drag with a mouse, which can feel unnatural. Adding the `mouse-dragging` attribute can help with this.

This example is best demonstrated using a mouse. Try clicking and dragging the slide to move it. Then toggle the switch and try again.

```html
<div class="mouse-dragging">
  <wa-carousel pagination>
    <wa-carousel-item>
      <img
        alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
        src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
      />
    </wa-carousel-item>
    <wa-carousel-item>
      <img
        alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
        src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
      />
    </wa-carousel-item>
    <wa-carousel-item>
      <img
        alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
        src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
      />
    </wa-carousel-item>
    <wa-carousel-item>
      <img
        alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
        src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
      />
    </wa-carousel-item>
    <wa-carousel-item>
      <img
        alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
        src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
      />
    </wa-carousel-item>
  </wa-carousel>

  <wa-divider></wa-divider>

  <wa-switch>Enable mouse dragging</wa-switch>
</div>

<script>
  const container = document.querySelector('.mouse-dragging');
  const carousel = container.querySelector('wa-carousel');
  const toggle = container.querySelector('wa-switch');

  toggle.addEventListener('change', () => {
    carousel.toggleAttribute('mouse-dragging', toggle.checked);
  });
</script>
```

### Multiple Slides Per View

The `slides-per-page` attribute makes it possible to display multiple slides at a time. You can also use the `slides-per-move` attribute to advance more than once slide at a time, if desired.

```html
<wa-carousel navigation pagination slides-per-page="2" slides-per-move="2">
  <wa-carousel-item style="background: red;">Slide 1</wa-carousel-item>
  <wa-carousel-item style="background: orange;">Slide 2</wa-carousel-item>
  <wa-carousel-item style="background: yellow;">Slide 3</wa-carousel-item>
  <wa-carousel-item style="background: green;">Slide 4</wa-carousel-item>
  <wa-carousel-item style="background: blue;">Slide 5</wa-carousel-item>
  <wa-carousel-item style="background: purple;">Slide 6</wa-carousel-item>
</wa-carousel>
```

### Adding and Removing Slides

The content of the carousel can be changed by adding or removing carousel items. The carousel will update itself automatically.

```html
<wa-carousel class="dynamic-carousel" pagination navigation>
  <wa-carousel-item style="background: red">Slide 1</wa-carousel-item>
  <wa-carousel-item style="background: orange">Slide 2</wa-carousel-item>
  <wa-carousel-item style="background: yellow">Slide 3</wa-carousel-item>
</wa-carousel>

<div class="carousel-options">
  <wa-button appearance="filled" id="dynamic-add">Add slide</wa-button>
  <wa-button appearance="filled" id="dynamic-remove">Remove slide</wa-button>
</div>

<style>
  .dynamic-carousel {
    --aspect-ratio: 3 / 2;
  }

  .dynamic-carousel ~ .carousel-options {
    display: flex;
    justify-content: center;
    gap: var(--wa-space-xs);
    margin-top: var(--wa-space-l);
  }

  .dynamic-carousel wa-carousel-item {
    flex: 0 0 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--wa-font-size-2xl);
  }
</style>

<script>
  (() => {
    const dynamicCarousel = document.querySelector('.dynamic-carousel');
    const dynamicAdd = document.querySelector('#dynamic-add');
    const dynamicRemove = document.querySelector('#dynamic-remove');
    const colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple'];
    let colorIndex = 2;

    const addSlide = () => {
      const slide = document.createElement('wa-carousel-item');
      const color = colors[++colorIndex % colors.length];
      slide.innerText = `Slide ${dynamicCarousel.children.length + 1}`;
      slide.style.setProperty('background', color);
      dynamicCarousel.appendChild(slide);
      dynamicRemove.disabled = false;
    };

    const removeSlide = () => {
      const slide = dynamicCarousel.children[dynamicCarousel.children.length - 1];
      const numSlides = dynamicCarousel.querySelectorAll('wa-carousel-item').length;

      if (numSlides > 1) {
        slide.remove();
        colorIndex--;
      }

      dynamicRemove.disabled = numSlides - 1 <= 1;
    };

    dynamicAdd.addEventListener('click', addSlide);
    dynamicRemove.addEventListener('click', removeSlide);
  })();
</script>
```

### Vertical Scrolling

Setting the `orientation` attribute to `vertical` will render the carousel in a vertical layout. If the content of your slides vary in height, you will need to set an explicit `height` or `max-height` on the carousel using CSS.

```html
<wa-carousel class="vertical" pagination orientation="vertical">
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
<style>
  .vertical {
    max-height: 400px;
  }

  .vertical::part(base) {
    grid-template-areas: 'slides slides pagination';
  }

  .vertical::part(pagination) {
    flex-direction: column;
  }

  .vertical::part(navigation) {
    transform: rotate(90deg);
    display: flex;
  }
</style>
```

### Aspect Ratio

Use the `--aspect-ratio` custom property to customize the size of the carousel's viewport from the default value of 16/9.

```html
<wa-carousel class="aspect-ratio" navigation pagination style="--aspect-ratio: 3/2;">
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>

<wa-divider></wa-divider>

<wa-select label="Aspect ratio" name="aspect" value="3/2">
  <wa-option value="1/1">1/1</wa-option>
  <wa-option value="3/2">3/2</wa-option>
  <wa-option value="16/9">16/9</wa-option>
</wa-select>

<script>
  (() => {
    const carousel = document.querySelector('wa-carousel.aspect-ratio');
    const aspectRatio = document.querySelector('wa-select[name="aspect"]');

    aspectRatio.addEventListener('change', () => {
      carousel.style.setProperty('--aspect-ratio', aspectRatio.value);
    });
  })();
</script>
```

### Scroll Hint

Use the `--scroll-hint` custom property to add inline padding in horizontal carousels and block padding in vertical carousels. This will make the closest slides slightly visible, hinting that there are more items in the carousel.

```html
<wa-carousel class="scroll-hint" pagination style="--scroll-hint: 10%;">
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>
```

### Gallery Example

The carousel has a robust API that makes it possible to extend and customize. This example syncs the active slide with a set of thumbnails, effectively creating a gallery-style carousel.

```html
<wa-carousel class="carousel-thumbnails" navigation loop>
  <wa-carousel-item>
    <img
      alt="The sun shines on the mountains and trees (by Adam Kool on Unsplash)"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A river winding through an evergreen forest (by Luca Bravo on Unsplash)"
      src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="The sun is setting over a lavender field (by Leonard Cotte on Unsplash)"
      src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A field of grass with the sun setting in the background (by Sapan Patel on Unsplash)"
      src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10"
    />
  </wa-carousel-item>
  <wa-carousel-item>
    <img
      alt="A scenic view of a mountain with clouds rolling in (by V2osk on Unsplash)"
      src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10"
    />
  </wa-carousel-item>
</wa-carousel>

<div class="thumbnails">
  <div class="scroller">
    <img
      alt="Thumbnail by 1"
      class="image active"
      src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?q=10"
    />
    <img alt="Thumbnail by 2" class="image" src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=10" />
    <img alt="Thumbnail by 3" class="image" src="https://images.unsplash.com/photo-1499002238440-d264edd596ec?q=10" />
    <img alt="Thumbnail by 4" class="image" src="https://images.unsplash.com/photo-1475113548554-5a36f1f523d6?q=10" />
    <img alt="Thumbnail by 5" class="image" src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=10" />
  </div>
</div>

<style>
  .carousel-thumbnails {
    --slide-aspect-ratio: 3 / 2;
  }

  .thumbnails {
    display: flex;
    justify-content: center;
  }

  .scroller {
    display: flex;
    gap: var(--wa-space-s);
    overflow-x: auto;
    scrollbar-width: none;
    scroll-behavior: smooth;
    scroll-padding: var(--wa-space-s);
  }

  .scroller::-webkit-scrollbar {
    display: none;
  }

  .image {
    width: 64px;
    height: 64px;
    object-fit: cover;

    opacity: 0.3;
    will-change: opacity;
    transition: 250ms opacity;

    cursor: pointer;
  }

  .image.active {
    opacity: 1;
  }
</style>

<script>
  {
    const carousel = document.querySelector('.carousel-thumbnails');
    const scroller = document.querySelector('.scroller');
    const thumbnails = document.querySelectorAll('.image');

    scroller.addEventListener('click', e => {
      const target = e.target;

      if (target.matches('.image')) {
        const index = [...thumbnails].indexOf(target);
        carousel.goToSlide(index);
      }
    });

    carousel.addEventListener('wa-slide-change', e => {
      const slideIndex = e.detail.index;

      [...thumbnails].forEach((thumb, i) => {
        thumb.classList.toggle('active', i === slideIndex);
        if (i === slideIndex) {
          thumb.scrollIntoView({
            block: 'nearest',
          });
        }
      });
    });
  }
</script>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/carousel/carousel.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaCarousel from '@awesome.me/webawesome/dist/react/carousel';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| (default) | \`\` The carousel's main content, one or more elements. |
| \`next-icon\` | \`\` Optional previous icon to use instead of the default. Works best with . |

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`autoplay\` autoplay | \`boolean\` When set, the slides will scroll automatically when the user is not interacting with them. Type Default false | | |
| \`autoplayInterval\` autoplay-interval | \`number\` Specifies the amount of time, in milliseconds, between each automatic scroll. Type Default 3000 | | |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`loop\` loop | \`boolean\` When set, allows the user to navigate the carousel in the same direction indefinitely. Type Default false | | |
| \`mouseDragging\` mouse-dragging | \`boolean\` When set, it is possible to scroll through the slides by dragging them with the mouse. Type Default false | | |
| \`navigation\` navigation | \`boolean\` When set, show the carousel's navigation. Type Default false | | |
| \`orientation\` orientation | \`'horizontal' \\| 'vertical'\` Specifies the orientation in which the carousel will lay out. Type Default 'horizontal' | | |
| \`pagination\` pagination | \`boolean\` When set, show the carousel's pagination indicators. Type Default false | | |
| \`slidesPerMove\` slides-per-move | \`slides-per-page\` Specifies the number of slides the carousel will advance when scrolling, useful when specifying a greater than one. It can't be higher than slides-per-page. Type number Default 1 | | |
| \`slidesPerPage\` slides-per-page | \`number\` Specifies how many slides should be shown at a given time. Type Default 1 | | |

## Methods

Learn more about [methods](https://webawesome.com/docs/usage/#methods).

| Name | Description | Arguments |
| --- | --- | --- |
| \`goToSlide()\` | \`index\` Scrolls the carousel to the slide specified by . | \`index: number, behavior: ScrollBehavior\` |
| \`next()\` | \`slides-per-move\` Move the carousel forward by slides. | \`behavior: ScrollBehavior\` |
| \`previous()\` | \`slides-per-move\` Move the carousel backward by slides. | \`behavior: ScrollBehavior\` |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-slide-change\` | Emitted when the active slide changes. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--aspect-ratio\` | \`16/9\` The aspect ratio of each slide. Default |
| \`--scroll-hint\` | The amount of padding to apply to the scroll area, allowing adjacent slides to become partially visible as a scroll hint. |
| \`--slide-gap\` | \`var(--wa-space-m)\` The space between each slide. Default |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`base\` | The carousel's internal wrapper. | \`::part(base)\` |
| \`navigation\` | The navigation wrapper. | \`::part(navigation)\` |
| \`navigation-button\` | The navigation button. | \`::part(navigation-button)\` |
| \`navigation-button-next\` | Applied to the next button. | \`::part(navigation-button-next)\` |
| \`navigation-button-previous\` | Applied to the previous button. | \`::part(navigation-button-previous)\` |
| \`pagination\` | The pagination indicators wrapper. | \`::part(pagination)\` |
| \`pagination-item\` | The pagination indicator. | \`::part(pagination-item)\` |
| \`pagination-item-active\` | Applied when the item is active. | \`::part(pagination-item-active)\` |
| \`scroll-container\` | The scroll container that wraps the slides. | \`::part(scroll-container)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help