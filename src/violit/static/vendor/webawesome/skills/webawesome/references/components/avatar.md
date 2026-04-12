# Avatar

**Full documentation:** https://webawesome.com/docs/components/avatar


`<wa-avatar>` Since 2.0 Stable

Avatars are used to represent a person or object.

By default, a generic icon will be shown. You can personalize avatars by adding custom icons, initials, and images. You should always provide a `label` for assistive devices.

```html
<wa-avatar label="User avatar"></wa-avatar>
```

## Examples

### Images

To use an image for the avatar, set the `image` and `label` attributes. This will take priority and be shown over initials and icons. Avatar images can be lazily loaded by setting the `loading` attribute to `lazy`.

```html
<wa-avatar
  image="https://images.unsplash.com/photo-1529778873920-4da4926a72c2?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"
  label="Avatar of a gray tabby kitten looking down"
></wa-avatar>
<wa-avatar
  image="https://images.unsplash.com/photo-1591871937573-74dbba515c4c?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"
  label="Avatar of a white and grey kitten on grey textile"
  loading="lazy"
></wa-avatar>
```

### Initials

When you don't have an image to use, you can set the `initials` attribute to show something more personalized than an icon.

```html
<wa-avatar initials="WA" label="Avatar with initials: SL"></wa-avatar>
```

### Custom Icons

When no image or initials are set, an icon will be shown. The default avatar shows a generic "user" icon, but you can customize this with the `icon` slot.

```html
<wa-avatar label="Avatar with an image icon">
  <wa-icon slot="icon" name="image" variant="solid"></wa-icon>
</wa-avatar>

<wa-avatar label="Avatar with an archive icon">
  <wa-icon slot="icon" name="archive" variant="solid"></wa-icon>
</wa-avatar>

<wa-avatar label="Avatar with a briefcase icon">
  <wa-icon slot="icon" name="briefcase" variant="solid"></wa-icon>
</wa-avatar>
```

### Shapes

Avatars can be shaped using the `shape` attribute.

```html
<wa-avatar shape="square" label="Square avatar"></wa-avatar>
<wa-avatar shape="rounded" label="Rounded avatar"></wa-avatar>
<wa-avatar shape="circle" label="Circle avatar"></wa-avatar>
```

### Avatar Groups

You can group avatars with a few lines of CSS.

```html
<div class="avatar-group">
  <wa-avatar
    image="https://images.unsplash.com/photo-1490150028299-bf57d78394e0?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80&crop=right"
    label="Avatar 1 of 4"
  ></wa-avatar>

  <wa-avatar
    image="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&crop=left&q=80"
    label="Avatar 2 of 4"
  ></wa-avatar>

  <wa-avatar
    image="https://images.unsplash.com/photo-1456439663599-95b042d50252?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&crop=left&q=80"
    label="Avatar 3 of 4"
  ></wa-avatar>

  <wa-avatar
    image="https://images.unsplash.com/flagged/photo-1554078875-e37cb8b0e27d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&crop=top&q=80"
    label="Avatar 4 of 4"
  ></wa-avatar>
</div>

<style>
  .avatar-group wa-avatar:not(:first-of-type) {
    margin-left: calc(-1 * var(--wa-space-m));
  }

  .avatar-group wa-avatar {
    border: solid 2px var(--wa-color-surface-default);
  }
</style>
```

## Importing

Autoloading components via [projects](https://webawesome.com/docs/#using-a-project) is the recommended way to import components. If you prefer to do it manually, use one of the following code snippets.

\*\*CDN\*\*

Let your project code do the work! [Sign up for free](https://webawesome.com/signup) to use a project with your very own CDN — it's the fastest and easiest way to use Web Awesome.

\*\*npm\*\*

To manually import this component from NPM, use the following code.

```js
import '@awesome.me/webawesome/dist/components/avatar/avatar.js';
```

\*\*React\*\*

To manually import this component from React, use the following code.

```js
import WaAvatar from '@awesome.me/webawesome/dist/react/avatar';
```

## Slots

Learn more about [using slots](https://webawesome.com/docs/usage/#slots).

| Name | Description |
| --- | --- |
| \`icon\` | \`

## Attributes & Properties

Learn more about [attributes and properties](https://webawesome.com/docs/usage/#attributes-and-properties).

| Name | Description | Reflects |
| --- | --- | --- |
| \`css\` | \`CSSResultGroup \\| undefined\` One or more CSSResultGroup to include in the component's shadow root. Host styles are automatically prepended. Type Default styles | | |
| \`image\` image | \`string\` The image source to use for the avatar. Type Default '' | | |
| \`initials\` initials | \`string\` Initials to use as a fallback when no image is available (1-2 characters max recommended). Type Default '' | | |
| \`label\` label | \`string\` A label to use to describe the avatar to assistive devices. Type Default '' | | |
| \`loading\` loading | \`'eager' \\| 'lazy'\` Indicates how the browser should load the image. Type Default 'eager' | | |
| \`shape\` shape | \`'circle' \\| 'square' \\| 'rounded'\` The shape of the avatar. Type Default 'circle' | | |

## Events

Learn more about [events](https://webawesome.com/docs/usage/#events).

| Name | Description |
| --- | --- |
| \`wa-error\` | The image could not be loaded. This may because of an invalid URL, a temporary network condition, or some unknown cause. |

## CSS custom properties

Learn more about [CSS custom properties](https://webawesome.com/docs/customizing/#custom-properties).

| Name | Description |
| --- | --- |
| \`--size\` | The size of the avatar. |

## CSS parts

Learn more about [CSS parts](https://webawesome.com/docs/customizing/#css-parts).

| Name | Description | CSS selector |
| --- | --- | --- |
| \`icon\` | The container that wraps the avatar's icon. | \`::part(icon)\` |
| \`image\` | \`image\` The avatar . Only shown when the image attribute is set. | \`::part(image)\` |
| \`initials\` | The container that wraps the avatar's initials. | \`::part(initials)\` |

## Dependencies

This component automatically imports the following elements. Sub-dependencies, if any exist, will also be included in this list.

-   [`<wa-icon>`](https://webawesome.com/docs/components/icon)

**Need a hand?** Report a bug Ask for help