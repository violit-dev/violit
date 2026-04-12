---
name: webawesome
description: Web Awesome is a UI component library built with web components. Use when building buttons, inputs, selects, checkboxes, dialogs, modals, drawers, tabs, dropdowns, tooltips, carousels, forms, or using CSS utilities like wa-stack, wa-cluster, wa-grid. Supports React, Vue, Angular, Svelte, and vanilla JS.
license: MIT / Commercial (for Web Awesome Pro)
metadata:
  author: Web Awesome
  version: "3.5.0"
  homepage: https://webawesome.com
  repository: https://github.com/shoelace-style/webawesome
compatibility: Works in modern browsers. Requires no build tools when using CDN. Works with bundlers like Webpack and Vite when installed via npm.
allowed-tools: Read
---

# Web Awesome

Web Awesome is an open source UI component library with a Pro offering that helps sustain the project. It provides 50+ accessible, customizable web components that work with any framework.

**Pro components and features are available to paid users.** [Purchase Pro](https://webawesome.com/purchase)

## Quick Start

### npm Installation

```bash
npm install @awesome.me/webawesome
```

Import styles and components:

```js
import '@awesome.me/webawesome/dist/styles/webawesome.css';
import '@awesome.me/webawesome/dist/components/button/button.js';
```

### CDN / Project Setup

The easiest way to use Web Awesome is with a hosted project. [Create a project](https://webawesome.com) to get a single line of code that loads everything automatically.

For detailed installation options, see [Installation Guide](references/installation.md).

## Core Concepts

Web Awesome components are custom HTML elements. They work like native elements but with enhanced functionality.

- **Attributes & Properties**: Configure components via HTML attributes or JavaScript properties
- **Events**: Listen to custom events prefixed with `wa-` (e.g., `wa-change`, `wa-input`)
- **Methods**: Call methods programmatically (e.g., `element.focus()`)
- **Slots**: Insert content into named slots (e.g., `<wa-icon slot="start">`)
- **CSS Parts**: Style internal elements using `::part()` selectors
- **CSS Custom Properties**: Customize appearance with CSS variables

**Important**: Always use closing tags. Custom elements cannot self-close.

```html
<!-- Correct -->
<wa-input></wa-input>

<!-- Incorrect - will not work -->
<wa-input />
```

For complete usage details, see [Usage Guide](references/usage.md).

## Components

### Free Components

#### Actions

- [`<wa-button>`](references/components/button.md) - Buttons represent actions that are available to the user. ([docs](https://webawesome.com/docs/components/button))
- [`<wa-button-group>`](references/components/button-group.md) - Button groups can be used to group related buttons into sections. ([docs](https://webawesome.com/docs/components/button-group))
- [`<wa-copy-button>`](references/components/copy-button.md) - Copies data to the clipboard when the user clicks the button. ([docs](https://webawesome.com/docs/components/copy-button))
- [`<wa-dropdown>`](references/components/dropdown.md) - Dropdowns expose additional content that "drops down" in a panel. ([docs](https://webawesome.com/docs/components/dropdown))
- [`<wa-dropdown-item>`](references/components/dropdown-item.md) - Provides items to select in a dropdown. ([docs](https://webawesome.com/docs/components/dropdown-item))
- [`<wa-qr-code>`](references/components/qr-code.md) - Generates a QR code and renders it using the Canvas API. ([docs](https://webawesome.com/docs/components/qr-code))

#### Feedback & Status

- [`<wa-badge>`](references/components/badge.md) - Badges are used to draw attention and display statuses or counts. ([docs](https://webawesome.com/docs/components/badge))
- [`<wa-callout>`](references/components/callout.md) - Callouts are used to display important messages inline. ([docs](https://webawesome.com/docs/components/callout))
- [`<wa-progress-bar>`](references/components/progress-bar.md) - Progress bars are used to show the status of an ongoing operation. ([docs](https://webawesome.com/docs/components/progress-bar))
- [`<wa-progress-ring>`](references/components/progress-ring.md) - Progress rings are used to show the progress of a determinate operation in a circular fashion. ([docs](https://webawesome.com/docs/components/progress-ring))
- [`<wa-skeleton>`](references/components/skeleton.md) - Skeletons are used to provide a visual representation of where content will eventually be drawn. ([docs](https://webawesome.com/docs/components/skeleton))
- [`<wa-spinner>`](references/components/spinner.md) - Spinners are used to show the progress of an indeterminate operation. ([docs](https://webawesome.com/docs/components/spinner))
- [`<wa-tag>`](references/components/tag.md) - Tags are used as labels to organize things or to indicate a selection. ([docs](https://webawesome.com/docs/components/tag))
- [`<wa-tooltip>`](references/components/tooltip.md) - Tooltips display additional information based on a specific action. ([docs](https://webawesome.com/docs/components/tooltip))

#### Form Controls

- [`<wa-checkbox>`](references/components/checkbox.md) - Checkboxes allow the user to toggle an option on or off. ([docs](https://webawesome.com/docs/components/checkbox))
- [`<wa-color-picker>`](references/components/color-picker.md) - Color pickers allow the user to select a color. ([docs](https://webawesome.com/docs/components/color-picker))
- [`<wa-input>`](references/components/input.md) - Inputs collect data from the user. ([docs](https://webawesome.com/docs/components/input))
- [`<wa-number-input>`](references/components/number-input.md) - Number inputs allow users to enter and edit numeric values with optional stepper buttons. ([docs](https://webawesome.com/docs/components/number-input))
- [`<wa-option>`](references/components/option.md) - Options define the selectable items within various form controls such as select. ([docs](https://webawesome.com/docs/components/option))
- [`<wa-radio>`](references/components/radio.md) - Radios allow the user to select a single option from a group. ([docs](https://webawesome.com/docs/components/radio))
- [`<wa-radio-group>`](references/components/radio-group.md) - Radio groups are used to group multiple radios so they function as a single form control. ([docs](https://webawesome.com/docs/components/radio-group))
- [`<wa-rating>`](references/components/rating.md) - Ratings give users a way to quickly view and provide feedback. ([docs](https://webawesome.com/docs/components/rating))
- [`<wa-select>`](references/components/select.md) - Selects allow you to choose items from a menu of predefined options. ([docs](https://webawesome.com/docs/components/select))
- [`<wa-slider>`](references/components/slider.md) - Ranges allow the user to select a single value within a given range using a slider. ([docs](https://webawesome.com/docs/components/slider))
- [`<wa-switch>`](references/components/switch.md) - Switches allow the user to toggle an option on or off. ([docs](https://webawesome.com/docs/components/switch))
- [`<wa-textarea>`](references/components/textarea.md) - Textareas collect data from the user and allow multiple lines of text. ([docs](https://webawesome.com/docs/components/textarea))

#### Imagery

- [`<wa-animated-image>`](references/components/animated-image.md) - A component for displaying animated GIFs and WEBPs that play and pause on interaction. ([docs](https://webawesome.com/docs/components/animated-image))
- [`<wa-avatar>`](references/components/avatar.md) - Avatars are used to represent a person or object. ([docs](https://webawesome.com/docs/components/avatar))
- [`<wa-carousel>`](references/components/carousel.md) - Carousels display an arbitrary number of content slides along a horizontal or vertical axis. ([docs](https://webawesome.com/docs/components/carousel))
- [`<wa-carousel-item>`](references/components/carousel-item.md) - A carousel item represent a slide within a carousel. ([docs](https://webawesome.com/docs/components/carousel-item))
- [`<wa-comparison>`](references/components/comparison.md) - Compare visual differences between similar content with a sliding panel. ([docs](https://webawesome.com/docs/components/comparison))
- [`<wa-icon>`](references/components/icon.md) - Icons are symbols that can be used to represent various options within an application. ([docs](https://webawesome.com/docs/components/icon))
- [`<wa-zoomable-frame>`](references/components/zoomable-frame.md) - Zoomable frames render iframe content with zoom and interaction controls. ([docs](https://webawesome.com/docs/components/zoomable-frame))

#### Navigation

- [`<wa-breadcrumb>`](references/components/breadcrumb.md) - Breadcrumbs provide a group of links so users can easily navigate a website's hierarchy. ([docs](https://webawesome.com/docs/components/breadcrumb))
- [`<wa-breadcrumb-item>`](references/components/breadcrumb-item.md) - Breadcrumb Items are used inside breadcrumbs to represent different links. ([docs](https://webawesome.com/docs/components/breadcrumb-item))
- [`<wa-tab>`](references/components/tab.md) - Tabs are used inside tab groups to represent and activate tab panels. ([docs](https://webawesome.com/docs/components/tab))
- [`<wa-tab-group>`](references/components/tab-group.md) - Tab groups organize content into a container that shows one section at a time. ([docs](https://webawesome.com/docs/components/tab-group))
- [`<wa-tab-panel>`](references/components/tab-panel.md) - Tab panels are used inside tab groups to display tabbed content. ([docs](https://webawesome.com/docs/components/tab-panel))
- [`<wa-tree>`](references/components/tree.md) - Trees allow you to display a hierarchical list of selectable tree items. Items with children can be expanded and collapsed as desired by the user. ([docs](https://webawesome.com/docs/components/tree))
- [`<wa-tree-item>`](references/components/tree-item.md) - A tree item serves as a hierarchical node that lives inside a tree. ([docs](https://webawesome.com/docs/components/tree-item))

#### Organization

- [`<wa-card>`](references/components/card.md) - Cards can be used to group related subjects in a container. ([docs](https://webawesome.com/docs/components/card))
- [`<wa-details>`](references/components/details.md) - Details show a brief summary and expand to show additional content. ([docs](https://webawesome.com/docs/components/details))
- [`<wa-dialog>`](references/components/dialog.md) - Dialogs, sometimes called "modals", appear above the page and require the user's immediate attention. ([docs](https://webawesome.com/docs/components/dialog))
- [`<wa-divider>`](references/components/divider.md) - Dividers are used to visually separate or group elements. ([docs](https://webawesome.com/docs/components/divider))
- [`<wa-drawer>`](references/components/drawer.md) - Drawers slide in from a container to expose additional options and information. ([docs](https://webawesome.com/docs/components/drawer))
- [`<wa-page>`](references/components/page.md) - Pages offer an easy way to scaffold entire page layouts using minimal markup. ([docs](https://webawesome.com/docs/components/page))
- [`<wa-scroller>`](references/components/scroller.md) - Scrollers create an accessible container while providing visual cues that help users identify and navigate through content that scrolls. ([docs](https://webawesome.com/docs/components/scroller))
- [`<wa-split-panel>`](references/components/split-panel.md) - Split panels display two adjacent panels, allowing the user to reposition them. ([docs](https://webawesome.com/docs/components/split-panel))

#### Utilities

- [`<wa-animation>`](references/components/animation.md) - Animate elements declaratively with nearly 100 baked-in presets, or roll your own with custom keyframes. ([docs](https://webawesome.com/docs/components/animation))
- [`<wa-format-bytes>`](references/components/format-bytes.md) - Formats a number as a human readable bytes value. ([docs](https://webawesome.com/docs/components/format-bytes))
- [`<wa-format-date>`](references/components/format-date.md) - Formats a date/time using the specified locale and options. ([docs](https://webawesome.com/docs/components/format-date))
- [`<wa-format-number>`](references/components/format-number.md) - Formats a number using the specified locale and options. ([docs](https://webawesome.com/docs/components/format-number))
- [`<wa-include>`](references/components/include.md) - Includes give you the power to embed external HTML files into the page. ([docs](https://webawesome.com/docs/components/include))
- [`<wa-intersection-observer>`](references/components/intersection-observer.md) - Tracks immediate child elements and fires events as they move in and out of view. ([docs](https://webawesome.com/docs/components/intersection-observer))
- [`<wa-markdown>`](references/components/markdown.md) - A declarative utility that renders markdown in plain ol' HTML pages. ([docs](https://webawesome.com/docs/components/markdown))
- [`<wa-mutation-observer>`](references/components/mutation-observer.md) - The Mutation Observer component offers a thin, declarative interface to the MutationObserver API. ([docs](https://webawesome.com/docs/components/mutation-observer))
- [`<wa-popover>`](references/components/popover.md) - Popovers display interactive content when their anchor element is clicked. ([docs](https://webawesome.com/docs/components/popover))
- [`<wa-popup>`](references/components/popup.md) - Popup is a utility that lets you declaratively anchor "popup" containers to another element. ([docs](https://webawesome.com/docs/components/popup))
- [`<wa-relative-time>`](references/components/relative-time.md) - Outputs a localized time phrase relative to the current date and time. ([docs](https://webawesome.com/docs/components/relative-time))
- [`<wa-resize-observer>`](references/components/resize-observer.md) - The Resize Observer component offers a thin, declarative interface to the ResizeObserver API. ([docs](https://webawesome.com/docs/components/resize-observer))


## Themes

Web Awesome includes pre-built themes. Apply a theme by adding its class to the `<html>` element.

### Free Themes
- **Default** - The foundational theme
- **Awesome** - Bright, vibrant color palette
- **Shoelace** - Classic Shoelace styling

### Pro Themes
- **Active** - Green branding with rudimentary palette
- **Brutalist** - Blue branding with default palette
- **Glossy** - Indigo accents with elegant palette
- **Matter** - Purple branding with mild palette
- **Mellow** - Blue branding with natural palette
- **Playful** - Purple branding with rudimentary palette
- **Premium** - Cyan branding with anodized palette
- **Tailspin** - Indigo accents with vogue palette

See [Themes Reference](references/themes.md) for usage details.

## Color Palettes

Each palette provides 10 color hues with 11 tints each.

### Free Palettes
- Default, Bright, Shoelace

### Pro Palettes
- Rudimentary, Elegant, Mild, Natural, Anodized, Vogue

See [Themes Reference](references/themes.md) for palette usage.

## Utilities

Web Awesome provides CSS utilities for common styling tasks:

- **Layout**: `wa-stack`, `wa-cluster`, `wa-grid`, `wa-split`, `wa-flank`, `wa-frame`
- **Spacing**: `wa-gap-*` utilities
- **Text**: Typography utilities
- **Color**: Color variant utilities
- **Rounding**: `wa-border-radius-*` utilities
- **Accessibility**: `wa-visually-hidden` utilities
- **FOUCE Prevention**: `wa-cloak` utility
- **Native Styles**: Enhanced styling for native HTML elements

See [Layout Utilities](references/utilities/layout.md), [Rounding](references/utilities/rounding.md), [Visually Hidden](references/utilities/visually-hidden.md), [FOUCE](references/utilities/fouce.md), and [Native Styles](references/utilities/native.md).

## Design Tokens

Web Awesome uses CSS custom properties (design tokens) for consistent theming:

- **Borders**: `--wa-border-*` for width, radius, style
- **Color**: `--wa-color-*` for surfaces, text, semantic colors
- **Space**: `--wa-space-*` for consistent spacing
- **Typography**: `--wa-font-*` for font families, sizes, weights
- **Shadows**: `--wa-shadow-*` for elevation
- **Focus**: `--wa-focus-*` for focus ring styles
- **Transitions**: `--wa-transition-*` for animation timing

See [Design Tokens](references/tokens/) for full reference.

## Form Controls

Web Awesome form controls are form-associated custom elements supporting native form validation and the Constraint Validation API.

- Use `required`, `pattern`, `minlength`, `maxlength` attributes
- Use `setCustomValidity()` for custom error messages
- Style validation states with `:state(valid)`, `:state(invalid)`, etc.

See [Form Controls Reference](references/form-controls.md) for details.

## Icons

Font Awesome is the default icon library. Use `<wa-icon>` with Font Awesome icon names:

```html
<wa-icon name="house"></wa-icon>
<wa-icon name="gear"></wa-icon>
<wa-icon name="check"></wa-icon>
```

## Framework Integration

Web Awesome works with any framework:

- **React 19+**: Native custom element support with TypeScript types
- **React 18 and below**: Use provided React wrappers
- **Vue**: Works out of the box
- **Angular**: Works out of the box
- **Svelte**: Works out of the box

See framework-specific guides in [references/frameworks/](references/frameworks/).

## Pro Features

[Web Awesome Pro](https://webawesome.com/purchase) includes:

- Pro Components (Data Grid, Date Picker, Rich Text Editor, etc.)
- Pro Themes and Color Palettes
- Theme Builder tool
- Official Figma Design Kit
- Responsive Layout Tools
- Pattern Library
- Priority Support

## Support

- **GitHub Issues**: https://github.com/shoelace-style/webawesome/issues
- **GitHub Discussions**: https://github.com/shoelace-style/webawesome/discussions
- **Discord**: Community chat and support
- **Email**: For account and billing questions

See [Support Reference](references/support.md) for more details.

## Reference Documentation

- [Installation Guide](references/installation.md)
- [Usage Guide](references/usage.md)
- [Form Controls](references/form-controls.md)
- [Customizing](references/customizing.md)
- [Localization](references/localization.md)
- [Themes & Palettes](references/themes.md)
- [Layout Utilities](references/utilities/layout.md)
- [Native Styles](references/utilities/native.md)
- [Design Tokens](references/tokens/) - Borders, Color, Space, Typography, Shadows, Focus, Transitions
- [Framework Guides](references/frameworks/)
