import type { DefineComponent } from "vue";

import type { WaIcon } from "../../components/icon/icon.js";
import type { WaCheckbox, Event } from "../../components/checkbox/checkbox.js";
import type { WaSpinner } from "../../components/spinner/spinner.js";
import type { WaTreeItem } from "../../components/tree-item/tree-item.js";
import type { WaCarouselItem } from "../../components/carousel-item/carousel-item.js";
import type { WaButton } from "../../components/button/button.js";
import type { WaAnimatedImage } from "../../components/animated-image/animated-image.js";
import type { WaAnimation } from "../../components/animation/animation.js";
import type { WaAvatar } from "../../components/avatar/avatar.js";
import type { WaBadge } from "../../components/badge/badge.js";
import type { WaBreadcrumbItem } from "../../components/breadcrumb-item/breadcrumb-item.js";
import type { WaBreadcrumb } from "../../components/breadcrumb/breadcrumb.js";
import type { WaButtonGroup } from "../../components/button-group/button-group.js";
import type { WaCallout } from "../../components/callout/callout.js";
import type { WaCard } from "../../components/card/card.js";
import type { WaCarousel } from "../../components/carousel/carousel.js";
import type { WaInput, InputEvent, Event } from "../../components/input/input.js";
import type { WaPopup } from "../../components/popup/popup.js";
import type { WaColorPicker, Event, InputEvent, CustomEvent } from "../../components/color-picker/color-picker.js";
import type { WaComparison, Event } from "../../components/comparison/comparison.js";
import type { WaTooltip } from "../../components/tooltip/tooltip.js";
import type { WaCopyButton } from "../../components/copy-button/copy-button.js";
import type { WaDetails } from "../../components/details/details.js";
import type { WaDialog } from "../../components/dialog/dialog.js";
import type { WaDivider } from "../../components/divider/divider.js";
import type { WaDrawer } from "../../components/drawer/drawer.js";
import type { WaDropdownItem } from "../../components/dropdown-item/dropdown-item.js";
import type { WaDropdown } from "../../components/dropdown/dropdown.js";
import type { WaFormatBytes } from "../../components/format-bytes/format-bytes.js";
import type { WaFormatDate } from "../../components/format-date/format-date.js";
import type { WaFormatNumber } from "../../components/format-number/format-number.js";
import type { WaInclude } from "../../components/include/include.js";
import type { WaIntersectionObserver } from "../../components/intersection-observer/intersection-observer.js";
import type { WaMutationObserver } from "../../components/mutation-observer/mutation-observer.js";
import type { WaNumberInput, InputEvent, Event } from "../../components/number-input/number-input.js";
import type { WaTag } from "../../components/tag/tag.js";
import type { WaOption } from "../../components/option/option.js";
import type { WaSelect, InputEvent, Event } from "../../components/select/select.js";
import type { WaPopover } from "../../components/popover/popover.js";
import type { WaProgressBar } from "../../components/progress-bar/progress-bar.js";
import type { WaProgressRing } from "../../components/progress-ring/progress-ring.js";
import type { WaQrCode } from "../../components/qr-code/qr-code.js";
import type { WaRadio } from "../../components/radio/radio.js";
import type { WaRadioGroup, InputEvent, Event } from "../../components/radio-group/radio-group.js";
import type { WaRating } from "../../components/rating/rating.js";
import type { WaRelativeTime } from "../../components/relative-time/relative-time.js";
import type { WaScroller } from "../../components/scroller/scroller.js";
import type { WaResizeObserver } from "../../components/resize-observer/resize-observer.js";
import type { WaSkeleton } from "../../components/skeleton/skeleton.js";
import type { WaSlider, Event, FocusEvent, InputEvent } from "../../components/slider/slider.js";
import type { WaSwitch, Event, InputEvent } from "../../components/switch/switch.js";
import type { WaTab } from "../../components/tab/tab.js";
import type { WaSplitPanel } from "../../components/split-panel/split-panel.js";
import type { WaTabPanel } from "../../components/tab-panel/tab-panel.js";
import type { WaTabGroup } from "../../components/tab-group/tab-group.js";
import type { WaTextarea } from "../../components/textarea/textarea.js";
import type { WaTree } from "../../components/tree/tree.js";
import type { WaZoomableFrame, Event } from "../../components/zoomable-frame/zoomable-frame.js";
import type { WaMarkdown } from "../../components/markdown/markdown.js";
import type { WaPage } from "../../components/page/page.js";

type WaIconProps = {
  /** The name of the icon to draw. Available names depend on the icon library being used. */
  name?: WaIcon["name"];
  /** The family of icons to choose from. For Font Awesome Free, valid options include `classic` and `brands`. For
Font Awesome Pro subscribers, valid options include, `classic`, `sharp`, `duotone`, `sharp-duotone`, and `brands`.
A valid kit code must be present to show pro icons via CDN. You can set `<html data-fa-kit-code="...">` to provide
one. */
  family?: WaIcon["family"];
  /** The name of the icon's variant. For Font Awesome, valid options include `thin`, `light`, `regular`, and `solid` for
the `classic` and `sharp` families. Some variants require a Font Awesome Pro subscription. Custom icon libraries
may or may not use this property. */
  variant?: WaIcon["variant"];
  /** Sets the width of the icon to match the cropped SVG viewBox. This operates like the Font `fa-width-auto` class. */
  "auto-width"?: WaIcon["autoWidth"];
  /** Swaps the opacity of duotone icons. */
  "swap-opacity"?: WaIcon["swapOpacity"];
  /** An external URL of an SVG file. Be sure you trust the content you are including, as it will be executed as code and
can result in XSS attacks. */
  src?: WaIcon["src"];
  /** An alternate description to use for assistive devices. If omitted, the icon will be considered presentational and
ignored by assistive devices. */
  label?: WaIcon["label"];
  /** The name of a registered custom icon library. */
  library?: WaIcon["library"];
  /** Sets the rotation degree of the icon */
  rotate?: WaIcon["rotate"];
  /** Sets the flip direction of the icon along the 'x' (horizontal), 'y' (vertical), or 'both' axes. */
  flip?: WaIcon["flip"];
  /** Sets the animation for the icon */
  animation?: WaIcon["animation"];
  /**  */
  dir?: WaIcon["dir"];
  /**  */
  lang?: WaIcon["lang"];
  /**  */
  "did-ssr"?: WaIcon["didSSR"];
  /**  */
  initialReflectedProperties?: WaIcon["initialReflectedProperties"];
  /**  */
  internals?: WaIcon["internals"];
  /** Emitted when the icon has loaded. When using `spriteSheet: true` this will not emit. */
  "onwa-load"?: (e: CustomEvent<never>) => void;
  /** Emitted when the icon fails to load due to an error. When using `spriteSheet: true` this will not emit. */
  "onwa-error"?: (e: CustomEvent<never>) => void;
};

type WaCheckboxProps = {
  /**  */
  title?: WaCheckbox["title"];
  /** The name of the checkbox, submitted as a name/value pair with form data. */
  name?: WaCheckbox["name"];
  /** The value of the checkbox, submitted as a name/value pair with form data. */
  value?: WaCheckbox["value"];
  /** The checkbox's size. */
  size?: WaCheckbox["size"];
  /** Disables the checkbox. */
  disabled?: WaCheckbox["disabled"];
  /** Draws the checkbox in an indeterminate state. This is usually applied to checkboxes that represents a "select
all/none" behavior when associated checkboxes have a mix of checked and unchecked states. */
  indeterminate?: WaCheckbox["indeterminate"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  checked?: WaCheckbox["defaultChecked"];
  /** Makes the checkbox a required field. */
  required?: WaCheckbox["required"];
  /** The checkbox's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaCheckbox["hint"];
  /**  */
  "custom-error"?: WaCheckbox["customError"];
  /**  */
  dir?: WaCheckbox["dir"];
  /**  */
  lang?: WaCheckbox["lang"];
  /**  */
  "did-ssr"?: WaCheckbox["didSSR"];
  /**  */
  input?: WaCheckbox["input"];
  /**  */
  _checked?: WaCheckbox["_checked"];
  /** Draws the checkbox in a checked state. */
  checked?: WaCheckbox["checked"];
  /**  */
  assumeInteractionOn?: WaCheckbox["assumeInteractionOn"];
  /**  */
  valueHasChanged?: WaCheckbox["valueHasChanged"];
  /**  */
  hasInteracted?: WaCheckbox["hasInteracted"];
  /**  */
  states?: WaCheckbox["states"];
  /**  */
  emitInvalid?: WaCheckbox["emitInvalid"];
  /**  */
  labels?: WaCheckbox["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaCheckbox["form"];
  /**  */
  validity?: WaCheckbox["validity"];
  /**  */
  willValidate?: WaCheckbox["willValidate"];
  /**  */
  validationMessage?: WaCheckbox["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaCheckbox["validationTarget"];
  /**  */
  allValidators?: WaCheckbox["allValidators"];
  /**  */
  initialReflectedProperties?: WaCheckbox["initialReflectedProperties"];
  /**  */
  internals?: WaCheckbox["internals"];
  /** Emitted when the checked state changes. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the checkbox loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the checkbox gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the checkbox receives input. */
  oninput?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaSpinnerProps = {
  /**  */
  dir?: WaSpinner["dir"];
  /**  */
  lang?: WaSpinner["lang"];
  /**  */
  "did-ssr"?: WaSpinner["didSSR"];
  /**  */
  initialReflectedProperties?: WaSpinner["initialReflectedProperties"];
  /**  */
  internals?: WaSpinner["internals"];
};

type WaTreeItemProps = {
  /** Expands the tree item. */
  expanded?: WaTreeItem["expanded"];
  /** Draws the tree item in a selected state. */
  selected?: WaTreeItem["selected"];
  /** Disables the tree item. */
  disabled?: WaTreeItem["disabled"];
  /** Enables lazy loading behavior. */
  lazy?: WaTreeItem["lazy"];
  /**  */
  dir?: WaTreeItem["dir"];
  /**  */
  lang?: WaTreeItem["lang"];
  /**  */
  "did-ssr"?: WaTreeItem["didSSR"];
  /**  */
  indeterminate?: WaTreeItem["indeterminate"];
  /**  */
  isLeaf?: WaTreeItem["isLeaf"];
  /**  */
  loading?: WaTreeItem["loading"];
  /**  */
  selectable?: WaTreeItem["selectable"];
  /**  */
  defaultSlot?: WaTreeItem["defaultSlot"];
  /**  */
  childrenSlot?: WaTreeItem["childrenSlot"];
  /**  */
  itemElement?: WaTreeItem["itemElement"];
  /**  */
  childrenContainer?: WaTreeItem["childrenContainer"];
  /**  */
  expandButtonSlot?: WaTreeItem["expandButtonSlot"];
  /**  */
  initialReflectedProperties?: WaTreeItem["initialReflectedProperties"];
  /**  */
  internals?: WaTreeItem["internals"];
  /** Emitted when the tree item expands. */
  "onwa-expand"?: (e: CustomEvent<never>) => void;
  /** Emitted after the tree item expands and all animations are complete. */
  "onwa-after-expand"?: (e: CustomEvent<never>) => void;
  /** Emitted when the tree item collapses. */
  "onwa-collapse"?: (e: CustomEvent<never>) => void;
  /** Emitted after the tree item collapses and all animations are complete. */
  "onwa-after-collapse"?: (e: CustomEvent<never>) => void;
  /** Emitted when the tree item's lazy state changes. */
  "onwa-lazy-change"?: (e: CustomEvent<never>) => void;
  /** Emitted when a lazy item is selected. Use this event to asynchronously load data and append items to the tree before expanding. After appending new items, remove the `lazy` attribute to remove the loading state and update the tree. */
  "onwa-lazy-load"?: (e: CustomEvent<never>) => void;
};

type WaCarouselItemProps = {
  /**  */
  dir?: WaCarouselItem["dir"];
  /**  */
  lang?: WaCarouselItem["lang"];
  /**  */
  "did-ssr"?: WaCarouselItem["didSSR"];
  /**  */
  initialReflectedProperties?: WaCarouselItem["initialReflectedProperties"];
  /**  */
  internals?: WaCarouselItem["internals"];
};

type WaButtonProps = {
  /**  */
  title?: WaButton["title"];
  /** The button's theme variant. Defaults to `neutral` if not within another element with a variant. */
  variant?: WaButton["variant"];
  /** The button's visual appearance. */
  appearance?: WaButton["appearance"];
  /** The button's size. */
  size?: WaButton["size"];
  /** Draws the button with a caret. Used to indicate that the button triggers a dropdown menu or similar behavior. */
  "with-caret"?: WaButton["withCaret"];
  /** Only required for SSR. Set to `true` if you're slotting in a `start` element so the server-rendered markup
includes the start slot before the component hydrates on the client. */
  "with-start"?: WaButton["withStart"];
  /** Only required for SSR. Set to `true` if you're slotting in an `end` element so the server-rendered markup
includes the end slot before the component hydrates on the client. */
  "with-end"?: WaButton["withEnd"];
  /** Disables the button. */
  disabled?: WaButton["disabled"];
  /** Draws the button in a loading state. */
  loading?: WaButton["loading"];
  /** Draws a pill-style button with rounded edges. */
  pill?: WaButton["pill"];
  /** The type of button. Note that the default value is `button` instead of `submit`, which is opposite of how native
`<button>` elements behave. When the type is `submit`, the button will submit the surrounding form. */
  type?: WaButton["type"];
  /** The name of the button, submitted as a name/value pair with form data, but only when this button is the submitter.
This attribute is ignored when `href` is present. */
  name?: WaButton["name"];
  /** The value of the button, submitted as a pair with the button's name as part of the form data, but only when this
button is the submitter. This attribute is ignored when `href` is present. */
  value?: WaButton["value"];
  /** When set, the underlying button will be rendered as an `<a>` with this `href` instead of a `<button>`. */
  href?: WaButton["href"];
  /** Tells the browser where to open the link. Only used when `href` is present. */
  target?: WaButton["target"];
  /** When using `href`, this attribute will map to the underlying link's `rel` attribute. */
  rel?: WaButton["rel"];
  /** Tells the browser to download the linked file as this filename. Only used when `href` is present. */
  download?: WaButton["download"];
  /** Used to override the form owner's `action` attribute. */
  formaction?: WaButton["formAction"];
  /** Used to override the form owner's `enctype` attribute. */
  formenctype?: WaButton["formEnctype"];
  /** Used to override the form owner's `method` attribute. */
  formmethod?: WaButton["formMethod"];
  /** Used to override the form owner's `novalidate` attribute. */
  formnovalidate?: WaButton["formNoValidate"];
  /** Used to override the form owner's `target` attribute. */
  formtarget?: WaButton["formTarget"];
  /**  */
  "custom-error"?: WaButton["customError"];
  /**  */
  dir?: WaButton["dir"];
  /**  */
  lang?: WaButton["lang"];
  /**  */
  "did-ssr"?: WaButton["didSSR"];
  /**  */
  assumeInteractionOn?: WaButton["assumeInteractionOn"];
  /**  */
  button?: WaButton["button"];
  /**  */
  labelSlot?: WaButton["labelSlot"];
  /**  */
  invalid?: WaButton["invalid"];
  /**  */
  isIconButton?: WaButton["isIconButton"];
  /**  */
  required?: WaButton["required"];
  /**  */
  input?: WaButton["input"];
  /**  */
  valueHasChanged?: WaButton["valueHasChanged"];
  /**  */
  hasInteracted?: WaButton["hasInteracted"];
  /**  */
  states?: WaButton["states"];
  /**  */
  emitInvalid?: WaButton["emitInvalid"];
  /**  */
  labels?: WaButton["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaButton["form"];
  /**  */
  validity?: WaButton["validity"];
  /**  */
  willValidate?: WaButton["willValidate"];
  /**  */
  validationMessage?: WaButton["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaButton["validationTarget"];
  /**  */
  allValidators?: WaButton["allValidators"];
  /**  */
  initialReflectedProperties?: WaButton["initialReflectedProperties"];
  /**  */
  internals?: WaButton["internals"];
  /** Emitted when the button loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the button gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaAnimatedImageProps = {
  /** The path to the image to load. */
  src?: WaAnimatedImage["src"];
  /** A description of the image used by assistive devices. */
  alt?: WaAnimatedImage["alt"];
  /** Plays the animation. When this attribute is remove, the animation will pause. */
  play?: WaAnimatedImage["play"];
  /**  */
  dir?: WaAnimatedImage["dir"];
  /**  */
  lang?: WaAnimatedImage["lang"];
  /**  */
  "did-ssr"?: WaAnimatedImage["didSSR"];
  /**  */
  animatedImage?: WaAnimatedImage["animatedImage"];
  /**  */
  frozenFrame?: WaAnimatedImage["frozenFrame"];
  /**  */
  isLoaded?: WaAnimatedImage["isLoaded"];
  /**  */
  initialReflectedProperties?: WaAnimatedImage["initialReflectedProperties"];
  /**  */
  internals?: WaAnimatedImage["internals"];
  /** Emitted when the image loads successfully. */
  "onwa-load"?: (e: CustomEvent<never>) => void;
  /** Emitted when the image fails to load. */
  "onwa-error"?: (e: CustomEvent<never>) => void;
};

type WaAnimationProps = {
  /** The name of the built-in animation to use. For custom animations, use the `keyframes` prop. */
  name?: WaAnimation["name"];
  /** Plays the animation. When omitted, the animation will be paused. This attribute will be automatically removed when
the animation finishes or gets canceled. */
  play?: WaAnimation["play"];
  /** The number of milliseconds to delay the start of the animation. */
  delay?: WaAnimation["delay"];
  /** Determines the direction of playback as well as the behavior when reaching the end of an iteration.
[Learn more](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-direction) */
  direction?: WaAnimation["direction"];
  /** The number of milliseconds each iteration of the animation takes to complete. */
  duration?: WaAnimation["duration"];
  /** The easing function to use for the animation. This can be a Web Awesome easing function or a custom easing function
such as `cubic-bezier(0, 1, .76, 1.14)`. */
  easing?: WaAnimation["easing"];
  /** The number of milliseconds to delay after the active period of an animation sequence. */
  "end-delay"?: WaAnimation["endDelay"];
  /** Sets how the animation applies styles to its target before and after its execution. */
  fill?: WaAnimation["fill"];
  /** The number of iterations to run before the animation completes. Defaults to `Infinity`, which loops. */
  iterations?: WaAnimation["iterations"];
  /** The offset at which to start the animation, usually between 0 (start) and 1 (end). */
  "iteration-start"?: WaAnimation["iterationStart"];
  /** Sets the animation's playback rate. The default is `1`, which plays the animation at a normal speed. Setting this
to `2`, for example, will double the animation's speed. A negative value can be used to reverse the animation. This
value can be changed without causing the animation to restart. */
  "playback-rate"?: WaAnimation["playbackRate"];
  /**  */
  dir?: WaAnimation["dir"];
  /**  */
  lang?: WaAnimation["lang"];
  /**  */
  "did-ssr"?: WaAnimation["didSSR"];
  /**  */
  defaultSlot?: WaAnimation["defaultSlot"];
  /** The keyframes to use for the animation. If this is set, `name` will be ignored. */
  keyframes?: WaAnimation["keyframes"];
  /** Gets and sets the current animation time. */
  currentTime?: WaAnimation["currentTime"];
  /**  */
  initialReflectedProperties?: WaAnimation["initialReflectedProperties"];
  /**  */
  internals?: WaAnimation["internals"];
  /** Emitted when the animation is canceled. */
  "onwa-cancel"?: (e: CustomEvent<never>) => void;
  /** Emitted when the animation finishes. */
  "onwa-finish"?: (e: CustomEvent<never>) => void;
  /** Emitted when the animation starts or restarts. */
  "onwa-start"?: (e: CustomEvent<never>) => void;
};

type WaAvatarProps = {
  /** The image source to use for the avatar. */
  image?: WaAvatar["image"];
  /** A label to use to describe the avatar to assistive devices. */
  label?: WaAvatar["label"];
  /** Initials to use as a fallback when no image is available (1-2 characters max recommended). */
  initials?: WaAvatar["initials"];
  /** Indicates how the browser should load the image. */
  loading?: WaAvatar["loading"];
  /** The shape of the avatar. */
  shape?: WaAvatar["shape"];
  /**  */
  dir?: WaAvatar["dir"];
  /**  */
  lang?: WaAvatar["lang"];
  /**  */
  "did-ssr"?: WaAvatar["didSSR"];
  /**  */
  initialReflectedProperties?: WaAvatar["initialReflectedProperties"];
  /**  */
  internals?: WaAvatar["internals"];
  /** The image could not be loaded. This may because of an invalid URL, a temporary network condition, or some unknown cause. */
  "onwa-error"?: (e: CustomEvent<never>) => void;
};

type WaBadgeProps = {
  /** The badge's theme variant. Defaults to `brand` if not within another element with a variant. */
  variant?: WaBadge["variant"];
  /** The badge's visual appearance. */
  appearance?: WaBadge["appearance"];
  /** Draws a pill-style badge with rounded edges. */
  pill?: WaBadge["pill"];
  /** Adds an animation to draw attention to the badge. */
  attention?: WaBadge["attention"];
  /**  */
  dir?: WaBadge["dir"];
  /**  */
  lang?: WaBadge["lang"];
  /**  */
  "did-ssr"?: WaBadge["didSSR"];
  /**  */
  initialReflectedProperties?: WaBadge["initialReflectedProperties"];
  /**  */
  internals?: WaBadge["internals"];
};

type WaBreadcrumbItemProps = {
  /** Optional URL to direct the user to when the breadcrumb item is activated. When set, a link will be rendered
internally. When unset, a button will be rendered instead. */
  href?: WaBreadcrumbItem["href"];
  /** Tells the browser where to open the link. Only used when `href` is set. */
  target?: WaBreadcrumbItem["target"];
  /** The `rel` attribute to use on the link. Only used when `href` is set. */
  rel?: WaBreadcrumbItem["rel"];
  /**  */
  dir?: WaBreadcrumbItem["dir"];
  /**  */
  lang?: WaBreadcrumbItem["lang"];
  /**  */
  "did-ssr"?: WaBreadcrumbItem["didSSR"];
  /**  */
  defaultSlot?: WaBreadcrumbItem["defaultSlot"];
  /**  */
  initialReflectedProperties?: WaBreadcrumbItem["initialReflectedProperties"];
  /**  */
  internals?: WaBreadcrumbItem["internals"];
};

type WaBreadcrumbProps = {
  /** The label to use for the breadcrumb control. This will not be shown on the screen, but it will be announced by
screen readers and other assistive devices to provide more context for users. */
  label?: WaBreadcrumb["label"];
  /**  */
  dir?: WaBreadcrumb["dir"];
  /**  */
  lang?: WaBreadcrumb["lang"];
  /**  */
  "did-ssr"?: WaBreadcrumb["didSSR"];
  /**  */
  defaultSlot?: WaBreadcrumb["defaultSlot"];
  /**  */
  separatorSlot?: WaBreadcrumb["separatorSlot"];
  /**  */
  initialReflectedProperties?: WaBreadcrumb["initialReflectedProperties"];
  /**  */
  internals?: WaBreadcrumb["internals"];
};

type WaButtonGroupProps = {
  /** A label to use for the button group. This won't be displayed on the screen, but it will be announced by assistive
devices when interacting with the control and is strongly recommended. */
  label?: WaButtonGroup["label"];
  /** The button group's orientation. */
  orientation?: WaButtonGroup["orientation"];
  /**  */
  dir?: WaButtonGroup["dir"];
  /**  */
  lang?: WaButtonGroup["lang"];
  /**  */
  "did-ssr"?: WaButtonGroup["didSSR"];
  /**  */
  defaultSlot?: WaButtonGroup["defaultSlot"];
  /**  */
  disableRole?: WaButtonGroup["disableRole"];
  /**  */
  hasOutlined?: WaButtonGroup["hasOutlined"];
  /**  */
  initialReflectedProperties?: WaButtonGroup["initialReflectedProperties"];
  /**  */
  internals?: WaButtonGroup["internals"];
};

type WaCalloutProps = {
  /** The callout's theme variant. Defaults to `brand` if not within another element with a variant. */
  variant?: WaCallout["variant"];
  /** The callout's visual appearance. */
  appearance?: WaCallout["appearance"];
  /** The callout's size. */
  size?: WaCallout["size"];
  /**  */
  dir?: WaCallout["dir"];
  /**  */
  lang?: WaCallout["lang"];
  /**  */
  "did-ssr"?: WaCallout["didSSR"];
  /**  */
  initialReflectedProperties?: WaCallout["initialReflectedProperties"];
  /**  */
  internals?: WaCallout["internals"];
};

type WaCardProps = {
  /** The card's visual appearance. */
  appearance?: WaCard["appearance"];
  /** Only required for SSR. Set to `true` if you're slotting in a `header` element so the server-rendered markup
includes the header before the component hydrates on the client. */
  "with-header"?: WaCard["withHeader"];
  /** Only required for SSR. Set to `true` if you're slotting in a `media` element so the server-rendered markup
includes the media before the component hydrates on the client. */
  "with-media"?: WaCard["withMedia"];
  /** Only required for SSR. Set to `true` if you're slotting in a `footer` element so the server-rendered markup
includes the footer before the component hydrates on the client. */
  "with-footer"?: WaCard["withFooter"];
  /** Renders the card's orientation * */
  orientation?: WaCard["orientation"];
  /**  */
  dir?: WaCard["dir"];
  /**  */
  lang?: WaCard["lang"];
  /**  */
  "did-ssr"?: WaCard["didSSR"];
  /**  */
  initialReflectedProperties?: WaCard["initialReflectedProperties"];
  /**  */
  internals?: WaCard["internals"];
};

type WaCarouselProps = {
  /** When set, allows the user to navigate the carousel in the same direction indefinitely. */
  loop?: WaCarousel["loop"];
  /**  */
  slides?: WaCarousel["slides"];
  /**  */
  currentSlide?: WaCarousel["currentSlide"];
  /** When set, show the carousel's navigation. */
  navigation?: WaCarousel["navigation"];
  /** When set, show the carousel's pagination indicators. */
  pagination?: WaCarousel["pagination"];
  /** When set, the slides will scroll automatically when the user is not interacting with them. */
  autoplay?: WaCarousel["autoplay"];
  /** Specifies the amount of time, in milliseconds, between each automatic scroll. */
  "autoplay-interval"?: WaCarousel["autoplayInterval"];
  /** Specifies how many slides should be shown at a given time. */
  "slides-per-page"?: WaCarousel["slidesPerPage"];
  /** Specifies the number of slides the carousel will advance when scrolling, useful when specifying a `slides-per-page`
greater than one. It can't be higher than `slides-per-page`. */
  "slides-per-move"?: WaCarousel["slidesPerMove"];
  /** Specifies the orientation in which the carousel will lay out. */
  orientation?: WaCarousel["orientation"];
  /** When set, it is possible to scroll through the slides by dragging them with the mouse. */
  "mouse-dragging"?: WaCarousel["mouseDragging"];
  /**  */
  dir?: WaCarousel["dir"];
  /**  */
  lang?: WaCarousel["lang"];
  /**  */
  "did-ssr"?: WaCarousel["didSSR"];
  /**  */
  scrollContainer?: WaCarousel["scrollContainer"];
  /**  */
  paginationContainer?: WaCarousel["paginationContainer"];
  /**  */
  activeSlide?: WaCarousel["activeSlide"];
  /**  */
  scrolling?: WaCarousel["scrolling"];
  /**  */
  dragging?: WaCarousel["dragging"];
  /**  */
  initialReflectedProperties?: WaCarousel["initialReflectedProperties"];
  /**  */
  internals?: WaCarousel["internals"];
  /** Emitted when the active slide changes. */
  "onwa-slide-change"?: (e: CustomEvent<{ index: number; slide: WaCarouselItem }>) => void;
};

type WaInputProps = {
  /**  */
  title?: WaInput["title"];
  /** The type of input. Works the same as a native `<input>` element, but only a subset of types are supported. Defaults
to `text`. */
  type?: WaInput["type"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaInput["defaultValue"];
  /** The input's size. */
  size?: WaInput["size"];
  /** The input's visual appearance. */
  appearance?: WaInput["appearance"];
  /** Draws a pill-style input with rounded edges. */
  pill?: WaInput["pill"];
  /** The input's label. If you need to display HTML, use the `label` slot instead. */
  label?: WaInput["label"];
  /** The input's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaInput["hint"];
  /** Adds a clear button when the input is not empty. */
  "with-clear"?: WaInput["withClear"];
  /** Placeholder text to show as a hint when the input is empty. */
  placeholder?: WaInput["placeholder"];
  /** Makes the input readonly. */
  readonly?: WaInput["readonly"];
  /** Adds a button to toggle the password's visibility. Only applies to password types. */
  "password-toggle"?: WaInput["passwordToggle"];
  /** Determines whether or not the password is currently visible. Only applies to password input types. */
  "password-visible"?: WaInput["passwordVisible"];
  /** Hides the browser's built-in increment/decrement spin buttons for number inputs. */
  "without-spin-buttons"?: WaInput["withoutSpinButtons"];
  /** Makes the input a required field. */
  required?: WaInput["required"];
  /** A regular expression pattern to validate input against. */
  pattern?: WaInput["pattern"];
  /** The minimum length of input that will be considered valid. */
  minlength?: WaInput["minlength"];
  /** The maximum length of input that will be considered valid. */
  maxlength?: WaInput["maxlength"];
  /** The input's minimum value. Only applies to date and number input types. */
  min?: WaInput["min"];
  /** The input's maximum value. Only applies to date and number input types. */
  max?: WaInput["max"];
  /** Specifies the granularity that the value must adhere to, or the special value `any` which means no stepping is
implied, allowing any numeric value. Only applies to date and number input types. */
  step?: WaInput["step"];
  /** Controls whether and how text input is automatically capitalized as it is entered by the user. */
  autocapitalize?: WaInput["autocapitalize"];
  /** Indicates whether the browser's autocorrect feature is on or off. When set as an attribute, use `"off"` or `"on"`.
When set as a property, use `true` or `false`. */
  autocorrect?: WaInput["autocorrect"];
  /** Specifies what permission the browser has to provide assistance in filling out form field values. Refer to
[this page on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for available values. */
  autocomplete?: WaInput["autocomplete"];
  /** Indicates that the input should receive focus on page load. */
  autofocus?: WaInput["autofocus"];
  /** Used to customize the label or icon of the Enter key on virtual keyboards. */
  enterkeyhint?: WaInput["enterkeyhint"];
  /** Enables spell checking on the input. */
  spellcheck?: WaInput["spellcheck"];
  /** Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual
keyboard on supportive devices. */
  inputmode?: WaInput["inputmode"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaInput["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaInput["withHint"];
  /** The name of the input, submitted as a name/value pair with form data. */
  name?: WaInput["name"];
  /** Disables the form control. */
  disabled?: WaInput["disabled"];
  /**  */
  "custom-error"?: WaInput["customError"];
  /**  */
  dir?: WaInput["dir"];
  /**  */
  lang?: WaInput["lang"];
  /**  */
  "did-ssr"?: WaInput["didSSR"];
  /**  */
  assumeInteractionOn?: WaInput["assumeInteractionOn"];
  /**  */
  input?: WaInput["input"];
  /** The current value of the input, submitted as a name/value pair with form data. */
  value?: WaInput["value"];
  /**  */
  valueHasChanged?: WaInput["valueHasChanged"];
  /**  */
  hasInteracted?: WaInput["hasInteracted"];
  /**  */
  states?: WaInput["states"];
  /**  */
  emitInvalid?: WaInput["emitInvalid"];
  /**  */
  labels?: WaInput["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaInput["form"];
  /**  */
  validity?: WaInput["validity"];
  /**  */
  willValidate?: WaInput["willValidate"];
  /**  */
  validationMessage?: WaInput["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaInput["validationTarget"];
  /**  */
  allValidators?: WaInput["allValidators"];
  /**  */
  initialReflectedProperties?: WaInput["initialReflectedProperties"];
  /**  */
  internals?: WaInput["internals"];
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when an alteration to the control's value is committed by the user. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the clear button is activated. */
  "onwa-clear"?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaPopupProps = {
  /** The element the popup will be anchored to. If the anchor lives outside of the popup, you can provide the anchor
element `id`, a DOM element reference, or a `VirtualElement`. If the anchor lives inside the popup, use the
`anchor` slot instead. */
  anchor?: WaPopup["anchor"];
  /** Activates the positioning logic and shows the popup. When this attribute is removed, the positioning logic is torn
down and the popup will be hidden. */
  active?: WaPopup["active"];
  /** The preferred placement of the popup. Note that the actual placement will vary as configured to keep the
panel inside of the viewport. */
  placement?: WaPopup["placement"];
  /** The bounding box to use for flipping, shifting, and auto-sizing. */
  boundary?: WaPopup["boundary"];
  /** The distance in pixels from which to offset the panel away from its anchor. */
  distance?: WaPopup["distance"];
  /** The distance in pixels from which to offset the panel along its anchor. */
  skidding?: WaPopup["skidding"];
  /** Attaches an arrow to the popup. The arrow's size and color can be customized using the `--arrow-size` and
`--arrow-color` custom properties. For additional customizations, you can also target the arrow using
`::part(arrow)` in your stylesheet. */
  arrow?: WaPopup["arrow"];
  /** The placement of the arrow. The default is `anchor`, which will align the arrow as close to the center of the
anchor as possible, considering available space and `arrow-padding`. A value of `start`, `end`, or `center` will
align the arrow to the start, end, or center of the popover instead. */
  "arrow-placement"?: WaPopup["arrowPlacement"];
  /** The amount of padding between the arrow and the edges of the popup. If the popup has a border-radius, for example,
this will prevent it from overflowing the corners. */
  "arrow-padding"?: WaPopup["arrowPadding"];
  /** When set, placement of the popup will flip to the opposite site to keep it in view. You can use
`flipFallbackPlacements` to further configure how the fallback placement is determined. */
  flip?: WaPopup["flip"];
  /** If the preferred placement doesn't fit, popup will be tested in these fallback placements until one fits. Must be a
string of any number of placements separated by a space, e.g. "top bottom left". If no placement fits, the flip
fallback strategy will be used instead. */
  "flip-fallback-placements"?: WaPopup["flipFallbackPlacements"];
  /** When neither the preferred placement nor the fallback placements fit, this value will be used to determine whether
the popup should be positioned using the best available fit based on available space or as it was initially
preferred. */
  "flip-fallback-strategy"?: WaPopup["flipFallbackStrategy"];
  /** The flip boundary describes clipping element(s) that overflow will be checked relative to when flipping. By
default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can
change the boundary by passing a reference to one or more elements to this property. */
  flipBoundary?: WaPopup["flipBoundary"];
  /** The amount of padding, in pixels, to exceed before the flip behavior will occur. */
  "flip-padding"?: WaPopup["flipPadding"];
  /** Moves the popup along the axis to keep it in view when clipped. */
  shift?: WaPopup["shift"];
  /** The shift boundary describes clipping element(s) that overflow will be checked relative to when shifting. By
default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can
change the boundary by passing a reference to one or more elements to this property. */
  shiftBoundary?: WaPopup["shiftBoundary"];
  /** The amount of padding, in pixels, to exceed before the shift behavior will occur. */
  "shift-padding"?: WaPopup["shiftPadding"];
  /** When set, this will cause the popup to automatically resize itself to prevent it from overflowing. */
  "auto-size"?: WaPopup["autoSize"];
  /** Syncs the popup's width or height to that of the anchor element. */
  sync?: WaPopup["sync"];
  /** The auto-size boundary describes clipping element(s) that overflow will be checked relative to when resizing. By
default, the boundary includes overflow ancestors that will cause the element to be clipped. If needed, you can
change the boundary by passing a reference to one or more elements to this property. */
  autoSizeBoundary?: WaPopup["autoSizeBoundary"];
  /** The amount of padding, in pixels, to exceed before the auto-size behavior will occur. */
  "auto-size-padding"?: WaPopup["autoSizePadding"];
  /** When a gap exists between the anchor and the popup element, this option will add a "hover bridge" that fills the
gap using an invisible element. This makes listening for events such as `mouseenter` and `mouseleave` more sane
because the pointer never technically leaves the element. The hover bridge will only be drawn when the popover is
active. */
  "hover-bridge"?: WaPopup["hoverBridge"];
  /**  */
  dir?: WaPopup["dir"];
  /**  */
  lang?: WaPopup["lang"];
  /**  */
  "did-ssr"?: WaPopup["didSSR"];
  /** A reference to the internal popup container. Useful for animating and styling the popup with JavaScript. */
  popup?: WaPopup["popup"];
  /**  */
  initialReflectedProperties?: WaPopup["initialReflectedProperties"];
  /**  */
  internals?: WaPopup["internals"];
  /** Emitted when the popup is repositioned. This event can fire a lot, so avoid putting expensive operations in your listener or consider debouncing it. */
  "onwa-reposition"?: (e: CustomEvent<never>) => void;
};

type WaColorPickerProps = {
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaColorPicker["defaultValue"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaColorPicker["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaColorPicker["withHint"];
  /** The color picker's label. This will not be displayed, but it will be announced by assistive devices. If you need to
display HTML, you can use the `label` slot` instead. */
  label?: WaColorPicker["label"];
  /** The color picker's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaColorPicker["hint"];
  /** The format to use. If opacity is enabled, these will translate to HEXA, RGBA, HSLA, and HSVA respectively. The color
picker will accept user input in any format (including CSS color names) and convert it to the desired format. */
  format?: WaColorPicker["format"];
  /** Determines the size of the color picker's trigger */
  size?: WaColorPicker["size"];
  /** The preferred placement of the color picker's popup. Note that the actual placement will vary as configured to
keep the panel inside of the viewport. */
  placement?: WaColorPicker["placement"];
  /** Removes the button that lets users toggle between format. */
  "without-format-toggle"?: WaColorPicker["withoutFormatToggle"];
  /** The name of the form control, submitted as a name/value pair with form data. */
  name?: WaColorPicker["name"];
  /** Disables the color picker. */
  disabled?: WaColorPicker["disabled"];
  /** Indicates whether or not the popup is open. You can toggle this attribute to show and hide the popup, or you
can use the `show()` and `hide()` methods and this attribute will reflect the popup's open state. */
  open?: WaColorPicker["open"];
  /** Shows the opacity slider. Enabling this will cause the formatted value to be HEXA, RGBA, or HSLA. */
  opacity?: WaColorPicker["opacity"];
  /** By default, values are lowercase. With this attribute, values will be uppercase instead. */
  uppercase?: WaColorPicker["uppercase"];
  /** One or more predefined color swatches to display as presets in the color picker. Can include any format the color
picker can parse, including HEX(A), RGB(A), HSL(A), HSV(A), and CSS color names. Each color must be separated by a
semicolon (`;`). Alternatively, you can pass an array of color values or an array of `{ color, label }` objects to
this property using JavaScript. When using objects with labels, the label will be used for the swatch's accessible
name instead of the raw color value. */
  swatches?: WaColorPicker["swatches"];
  /** Makes the color picker a required field. */
  required?: WaColorPicker["required"];
  /**  */
  "custom-error"?: WaColorPicker["customError"];
  /**  */
  dir?: WaColorPicker["dir"];
  /**  */
  lang?: WaColorPicker["lang"];
  /**  */
  "did-ssr"?: WaColorPicker["didSSR"];
  /**  */
  base?: WaColorPicker["base"];
  /**  */
  input?: WaColorPicker["input"];
  /**  */
  triggerLabel?: WaColorPicker["triggerLabel"];
  /**  */
  triggerButton?: WaColorPicker["triggerButton"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaColorPicker["validationTarget"];
  /**  */
  popup?: WaColorPicker["popup"];
  /**  */
  previewButton?: WaColorPicker["previewButton"];
  /**  */
  trigger?: WaColorPicker["trigger"];
  /** The current value of the color picker. The value's format will vary based the `format` attribute. To get the value
in a specific format, use the `getFormattedValue()` method. The value is submitted as a name/value pair with form
data. */
  value?: WaColorPicker["value"];
  /**  */
  assumeInteractionOn?: WaColorPicker["assumeInteractionOn"];
  /**  */
  valueHasChanged?: WaColorPicker["valueHasChanged"];
  /**  */
  hasInteracted?: WaColorPicker["hasInteracted"];
  /**  */
  states?: WaColorPicker["states"];
  /**  */
  emitInvalid?: WaColorPicker["emitInvalid"];
  /**  */
  labels?: WaColorPicker["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaColorPicker["form"];
  /**  */
  validity?: WaColorPicker["validity"];
  /**  */
  willValidate?: WaColorPicker["willValidate"];
  /**  */
  validationMessage?: WaColorPicker["validationMessage"];
  /**  */
  allValidators?: WaColorPicker["allValidators"];
  /**  */
  initialReflectedProperties?: WaColorPicker["initialReflectedProperties"];
  /**  */
  internals?: WaColorPicker["internals"];
  /** Emitted when the color picker's value changes. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the color picker receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /**  */
  "onwa-show"?: (e: CustomEvent<CustomEvent>) => void;
  /**  */
  "onwa-after-show"?: (e: CustomEvent<CustomEvent>) => void;
  /**  */
  "onwa-hide"?: (e: CustomEvent<CustomEvent>) => void;
  /**  */
  "onwa-after-hide"?: (e: CustomEvent<CustomEvent>) => void;
  /** Emitted when the color picker loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the color picker receives focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaComparisonProps = {
  /** The position of the divider as a percentage. */
  position?: WaComparison["position"];
  /**  */
  dir?: WaComparison["dir"];
  /**  */
  lang?: WaComparison["lang"];
  /**  */
  "did-ssr"?: WaComparison["didSSR"];
  /**  */
  handle?: WaComparison["handle"];
  /**  */
  initialReflectedProperties?: WaComparison["initialReflectedProperties"];
  /**  */
  internals?: WaComparison["internals"];
  /** Emitted when the position changes. */
  onchange?: (e: CustomEvent<Event>) => void;
};

type WaTooltipProps = {
  /** The preferred placement of the tooltip. Note that the actual placement may vary as needed to keep the tooltip
inside of the viewport. */
  placement?: WaTooltip["placement"];
  /** Disables the tooltip so it won't show when triggered. */
  disabled?: WaTooltip["disabled"];
  /** The distance in pixels from which to offset the tooltip away from its target. */
  distance?: WaTooltip["distance"];
  /** Indicates whether or not the tooltip is open. You can use this in lieu of the show/hide methods. */
  open?: WaTooltip["open"];
  /** The distance in pixels from which to offset the tooltip along its target. */
  skidding?: WaTooltip["skidding"];
  /** The amount of time to wait before showing the tooltip when the user mouses in. */
  "show-delay"?: WaTooltip["showDelay"];
  /** The amount of time to wait before hiding the tooltip when the user mouses out. */
  "hide-delay"?: WaTooltip["hideDelay"];
  /** Controls how the tooltip is activated. Possible options include `click`, `hover`, `focus`, and `manual`. Multiple
options can be passed by separating them with a space. When manual is used, the tooltip must be activated
programmatically. */
  trigger?: WaTooltip["trigger"];
  /** Removes the arrow from the tooltip. */
  "without-arrow"?: WaTooltip["withoutArrow"];
  /**  */
  for?: WaTooltip["for"];
  /**  */
  dir?: WaTooltip["dir"];
  /**  */
  lang?: WaTooltip["lang"];
  /**  */
  "did-ssr"?: WaTooltip["didSSR"];
  /**  */
  defaultSlot?: WaTooltip["defaultSlot"];
  /**  */
  body?: WaTooltip["body"];
  /**  */
  popup?: WaTooltip["popup"];
  /**  */
  anchor?: WaTooltip["anchor"];
  /**  */
  initialReflectedProperties?: WaTooltip["initialReflectedProperties"];
  /**  */
  internals?: WaTooltip["internals"];
  /** Emitted when the tooltip begins to show. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the tooltip has shown and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the tooltip begins to hide. */
  "onwa-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted after the tooltip has hidden and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
};

type WaCopyButtonProps = {
  /** The text value to copy. */
  value?: WaCopyButton["value"];
  /** An id that references an element in the same document from which data will be copied. If both this and `value` are
present, this value will take precedence. By default, the target element's `textContent` will be copied. To copy an
attribute, append the attribute name wrapped in square brackets, e.g. `from="el[value]"`. To copy a property,
append a dot and the property name, e.g. `from="el.value"`. */
  from?: WaCopyButton["from"];
  /** Disables the copy button. */
  disabled?: WaCopyButton["disabled"];
  /** A custom label to show in the tooltip. */
  "copy-label"?: WaCopyButton["copyLabel"];
  /** A custom label to show in the tooltip after copying. */
  "success-label"?: WaCopyButton["successLabel"];
  /** A custom label to show in the tooltip when a copy error occurs. */
  "error-label"?: WaCopyButton["errorLabel"];
  /** The length of time to show feedback before restoring the default trigger. */
  "feedback-duration"?: WaCopyButton["feedbackDuration"];
  /** The preferred placement of the tooltip. */
  "tooltip-placement"?: WaCopyButton["tooltipPlacement"];
  /**  */
  dir?: WaCopyButton["dir"];
  /**  */
  lang?: WaCopyButton["lang"];
  /**  */
  "did-ssr"?: WaCopyButton["didSSR"];
  /**  */
  copyIcon?: WaCopyButton["copyIcon"];
  /**  */
  successIcon?: WaCopyButton["successIcon"];
  /**  */
  errorIcon?: WaCopyButton["errorIcon"];
  /**  */
  tooltip?: WaCopyButton["tooltip"];
  /**  */
  isCopying?: WaCopyButton["isCopying"];
  /**  */
  status?: WaCopyButton["status"];
  /**  */
  initialReflectedProperties?: WaCopyButton["initialReflectedProperties"];
  /**  */
  internals?: WaCopyButton["internals"];
  /** Emitted when the data has been copied. */
  "onwa-copy"?: (e: CustomEvent<never>) => void;
  /** Emitted when the data could not be copied. */
  "onwa-error"?: (e: CustomEvent<never>) => void;
};

type WaDetailsProps = {
  /** Indicates whether or not the details is open. You can toggle this attribute to show and hide the details, or you
can use the `show()` and `hide()` methods and this attribute will reflect the details' open state. */
  open?: WaDetails["open"];
  /** The summary to show in the header. If you need to display HTML, use the `summary` slot instead. */
  summary?: WaDetails["summary"];
  /** Groups related details elements. When one opens, others with the same name will close. */
  name?: WaDetails["name"];
  /** Disables the details so it can't be toggled. */
  disabled?: WaDetails["disabled"];
  /** The element's visual appearance. */
  appearance?: WaDetails["appearance"];
  /** The location of the expand/collapse icon. */
  "icon-placement"?: WaDetails["iconPlacement"];
  /**  */
  dir?: WaDetails["dir"];
  /**  */
  lang?: WaDetails["lang"];
  /**  */
  "did-ssr"?: WaDetails["didSSR"];
  /**  */
  details?: WaDetails["details"];
  /**  */
  header?: WaDetails["header"];
  /**  */
  body?: WaDetails["body"];
  /**  */
  expandIconSlot?: WaDetails["expandIconSlot"];
  /**  */
  isAnimating?: WaDetails["isAnimating"];
  /**  */
  initialReflectedProperties?: WaDetails["initialReflectedProperties"];
  /**  */
  internals?: WaDetails["internals"];
  /** Emitted when the details opens. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the details opens and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the details closes. */
  "onwa-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted after the details closes and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
};

type WaDialogProps = {
  /** Indicates whether or not the dialog is open. Toggle this attribute to show and hide the dialog. */
  open?: WaDialog["open"];
  /** The dialog's label as displayed in the header. You should always include a relevant label, as it is required for
proper accessibility. If you need to display HTML, use the `label` slot instead. */
  label?: WaDialog["label"];
  /** Disables the header. This will also remove the default close button. */
  "without-header"?: WaDialog["withoutHeader"];
  /** When enabled, the dialog will be closed when the user clicks outside of it. */
  "light-dismiss"?: WaDialog["lightDismiss"];
  /** Only required for SSR. Set to `true` if you're slotting in a `footer` element so the server-rendered markup
includes the footer before the component hydrates on the client. */
  "with-footer"?: WaDialog["withFooter"];
  /**  */
  dir?: WaDialog["dir"];
  /**  */
  lang?: WaDialog["lang"];
  /**  */
  "did-ssr"?: WaDialog["didSSR"];
  /**  */
  dialog?: WaDialog["dialog"];
  /**  */
  initialReflectedProperties?: WaDialog["initialReflectedProperties"];
  /**  */
  internals?: WaDialog["internals"];
  /** Emitted when the dialog opens. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the dialog opens and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the dialog is requested to close. Calling `event.preventDefault()` will prevent the dialog from closing. You can inspect `event.detail.source` to see which element caused the dialog to close. If the source is the dialog element itself, the user has pressed [[Escape]] or the dialog has been closed programmatically. Avoid using this unless closing the dialog will result in destructive behavior such as data loss. */
  "onwa-hide"?: (e: CustomEvent<{ source: Element }>) => void;
  /** Emitted after the dialog closes and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
};

type WaDividerProps = {
  /** Sets the divider's orientation. */
  orientation?: WaDivider["orientation"];
  /**  */
  dir?: WaDivider["dir"];
  /**  */
  lang?: WaDivider["lang"];
  /**  */
  "did-ssr"?: WaDivider["didSSR"];
  /**  */
  initialReflectedProperties?: WaDivider["initialReflectedProperties"];
  /**  */
  internals?: WaDivider["internals"];
};

type WaDrawerProps = {
  /** Indicates whether or not the drawer is open. Toggle this attribute to show and hide the drawer. */
  open?: WaDrawer["open"];
  /** The drawer's label as displayed in the header. You should always include a relevant label, as it is required for
proper accessibility. If you need to display HTML, use the `label` slot instead. */
  label?: WaDrawer["label"];
  /** The direction from which the drawer will open. */
  placement?: WaDrawer["placement"];
  /** Disables the header. This will also remove the default close button. */
  "without-header"?: WaDrawer["withoutHeader"];
  /** When enabled, the drawer will be closed when the user clicks outside of it. */
  "light-dismiss"?: WaDrawer["lightDismiss"];
  /** Only required for SSR. Set to `true` if you're slotting in a `footer` element so the server-rendered markup
includes the footer before the component hydrates on the client. */
  "with-footer"?: WaDrawer["withFooter"];
  /**  */
  dir?: WaDrawer["dir"];
  /**  */
  lang?: WaDrawer["lang"];
  /**  */
  "did-ssr"?: WaDrawer["didSSR"];
  /**  */
  drawer?: WaDrawer["drawer"];
  /** Exposes the internal modal utility that controls focus trapping. To temporarily disable focus trapping and allow third-party modals spawned from an active Shoelace modal, call `modal.activateExternal()` when the third-party modal opens. Upon closing, call `modal.deactivateExternal()` to restore Shoelace's focus trapping. */
  modal?: WaDrawer["modal"];
  /**  */
  initialReflectedProperties?: WaDrawer["initialReflectedProperties"];
  /**  */
  internals?: WaDrawer["internals"];
  /** Emitted when the drawer opens. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the drawer opens and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the drawer is requesting to close. Calling `event.preventDefault()` will prevent the drawer from closing. You can inspect `event.detail.source` to see which element caused the drawer to close. If the source is the drawer element itself, the user has pressed [[Escape]] or the drawer has been closed programmatically. Avoid using this unless closing the drawer will result in destructive behavior such as data loss. */
  "onwa-hide"?: (e: CustomEvent<{ source: Element }>) => void;
  /** Emitted after the drawer closes and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
};

type WaDropdownItemProps = {
  /** The type of menu item to render. */
  variant?: WaDropdownItem["variant"];
  /** An optional value for the menu item. This is useful for determining which item was selected when listening to the
dropdown's `wa-select` event. */
  value?: WaDropdownItem["value"];
  /** Set to `checkbox` to make the item a checkbox. */
  type?: WaDropdownItem["type"];
  /** Set to true to check the dropdown item. Only valid when `type` is `checkbox`. */
  checked?: WaDropdownItem["checked"];
  /** Disables the dropdown item. */
  disabled?: WaDropdownItem["disabled"];
  /** Whether the submenu is currently open. */
  submenuOpen?: WaDropdownItem["submenuOpen"];
  /**  */
  dir?: WaDropdownItem["dir"];
  /**  */
  lang?: WaDropdownItem["lang"];
  /**  */
  "did-ssr"?: WaDropdownItem["didSSR"];
  /**  */
  submenuElement?: WaDropdownItem["submenuElement"];
  /**  */
  initialReflectedProperties?: WaDropdownItem["initialReflectedProperties"];
  /**  */
  internals?: WaDropdownItem["internals"];
  /** Emitted when the dropdown item loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the dropdown item gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
};

type WaDropdownProps = {
  /** Opens or closes the dropdown. */
  open?: WaDropdown["open"];
  /** The dropdown's size. */
  size?: WaDropdown["size"];
  /** The placement of the dropdown menu in reference to the trigger. The menu will shift to a more optimal location if
the preferred placement doesn't have enough room. */
  placement?: WaDropdown["placement"];
  /** The distance of the dropdown menu from its trigger. */
  distance?: WaDropdown["distance"];
  /** The offset of the dropdown menu along its trigger. */
  skidding?: WaDropdown["skidding"];
  /**  */
  dir?: WaDropdown["dir"];
  /**  */
  lang?: WaDropdown["lang"];
  /**  */
  "did-ssr"?: WaDropdown["didSSR"];
  /**  */
  defaultSlot?: WaDropdown["defaultSlot"];
  /**  */
  initialReflectedProperties?: WaDropdown["initialReflectedProperties"];
  /**  */
  internals?: WaDropdown["internals"];
  /** Emitted when the dropdown is about to show. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the dropdown has been shown. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the dropdown is about to hide. */
  "onwa-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted after the dropdown has been hidden. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted when an item in the dropdown is selected. */
  "onwa-select"?: (e: CustomEvent<never>) => void;
};

type WaFormatBytesProps = {
  /** The number to format in bytes. */
  value?: WaFormatBytes["value"];
  /** The type of unit to display. */
  unit?: WaFormatBytes["unit"];
  /** Determines how to display the result, e.g. "100 bytes", "100 b", or "100b". */
  display?: WaFormatBytes["display"];
  /**  */
  dir?: WaFormatBytes["dir"];
  /**  */
  lang?: WaFormatBytes["lang"];
  /**  */
  "did-ssr"?: WaFormatBytes["didSSR"];
  /**  */
  initialReflectedProperties?: WaFormatBytes["initialReflectedProperties"];
  /**  */
  internals?: WaFormatBytes["internals"];
};

type WaFormatDateProps = {
  /** The date/time to format. If not set, the current date and time will be used. When passing a string, it's strongly
recommended to use the ISO 8601 format to ensure timezones are handled correctly. To convert a date to this format
in JavaScript, use [`date.toISOString()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString). */
  date?: WaFormatDate["date"];
  /** The format for displaying the weekday. */
  weekday?: WaFormatDate["weekday"];
  /** The format for displaying the era. */
  era?: WaFormatDate["era"];
  /** The format for displaying the year. */
  year?: WaFormatDate["year"];
  /** The format for displaying the month. */
  month?: WaFormatDate["month"];
  /** The format for displaying the day. */
  day?: WaFormatDate["day"];
  /** The format for displaying the hour. */
  hour?: WaFormatDate["hour"];
  /** The format for displaying the minute. */
  minute?: WaFormatDate["minute"];
  /** The format for displaying the second. */
  second?: WaFormatDate["second"];
  /** The format for displaying the time. */
  "time-zone-name"?: WaFormatDate["timeZoneName"];
  /** The time zone to express the time in. */
  "time-zone"?: WaFormatDate["timeZone"];
  /** The format for displaying the hour. */
  "hour-format"?: WaFormatDate["hourFormat"];
  /**  */
  dir?: WaFormatDate["dir"];
  /**  */
  lang?: WaFormatDate["lang"];
  /**  */
  "did-ssr"?: WaFormatDate["didSSR"];
  /**  */
  initialReflectedProperties?: WaFormatDate["initialReflectedProperties"];
  /**  */
  internals?: WaFormatDate["internals"];
};

type WaFormatNumberProps = {
  /** The number to format. */
  value?: WaFormatNumber["value"];
  /** The formatting style to use. */
  type?: WaFormatNumber["type"];
  /** Turns off grouping separators. */
  "without-grouping"?: WaFormatNumber["withoutGrouping"];
  /** The [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency code to use when formatting. */
  currency?: WaFormatNumber["currency"];
  /** How to display the currency. */
  "currency-display"?: WaFormatNumber["currencyDisplay"];
  /** The minimum number of integer digits to use. Possible values are 1-21. */
  "minimum-integer-digits"?: WaFormatNumber["minimumIntegerDigits"];
  /** The minimum number of fraction digits to use. Possible values are 0-100. */
  "minimum-fraction-digits"?: WaFormatNumber["minimumFractionDigits"];
  /** The maximum number of fraction digits to use. Possible values are 0-100. */
  "maximum-fraction-digits"?: WaFormatNumber["maximumFractionDigits"];
  /** The minimum number of significant digits to use. Possible values are 1-21. */
  "minimum-significant-digits"?: WaFormatNumber["minimumSignificantDigits"];
  /** The maximum number of significant digits to use,. Possible values are 1-21. */
  "maximum-significant-digits"?: WaFormatNumber["maximumSignificantDigits"];
  /**  */
  dir?: WaFormatNumber["dir"];
  /**  */
  lang?: WaFormatNumber["lang"];
  /**  */
  "did-ssr"?: WaFormatNumber["didSSR"];
  /**  */
  initialReflectedProperties?: WaFormatNumber["initialReflectedProperties"];
  /**  */
  internals?: WaFormatNumber["internals"];
};

type WaIncludeProps = {
  /** The location of the HTML file to include. Be sure you trust the content you are including as it will be executed as
code and can result in XSS attacks. */
  src?: WaInclude["src"];
  /** The fetch mode to use. */
  mode?: WaInclude["mode"];
  /** Allows included scripts to be executed. Be sure you trust the content you are including as it will be executed as
code and can result in XSS attacks. */
  "allow-scripts"?: WaInclude["allowScripts"];
  /**  */
  dir?: WaInclude["dir"];
  /**  */
  lang?: WaInclude["lang"];
  /**  */
  "did-ssr"?: WaInclude["didSSR"];
  /**  */
  initialReflectedProperties?: WaInclude["initialReflectedProperties"];
  /**  */
  internals?: WaInclude["internals"];
  /** Emitted when the included file is loaded. */
  "onwa-load"?: (e: CustomEvent<never>) => void;
  /** Emitted when the included file fails to load due to an error. */
  "onwa-include-error"?: (e: CustomEvent<{ status: number }>) => void;
};

type WaIntersectionObserverProps = {
  /** Element ID to define the viewport boundaries for tracked targets. */
  root?: WaIntersectionObserver["root"];
  /** Offset space around the root boundary. Accepts values like CSS margin syntax. */
  "root-margin"?: WaIntersectionObserver["rootMargin"];
  /** One or more space-separated values representing visibility percentages that trigger the observer callback. */
  threshold?: WaIntersectionObserver["threshold"];
  /** CSS class applied to elements during intersection. Automatically removed when elements leave
the viewport, enabling pure CSS styling based on visibility state. */
  "intersect-class"?: WaIntersectionObserver["intersectClass"];
  /** If enabled, observation ceases after initial intersection. */
  once?: WaIntersectionObserver["once"];
  /** Deactivates the intersection observer functionality. */
  disabled?: WaIntersectionObserver["disabled"];
  /**  */
  dir?: WaIntersectionObserver["dir"];
  /**  */
  lang?: WaIntersectionObserver["lang"];
  /**  */
  "did-ssr"?: WaIntersectionObserver["didSSR"];
  /**  */
  initialReflectedProperties?: WaIntersectionObserver["initialReflectedProperties"];
  /**  */
  internals?: WaIntersectionObserver["internals"];
  /** Fired when a tracked element begins or ceases intersecting. */
  "onwa-intersect"?: (e: CustomEvent<{ entry: IntersectionObserverEntry }>) => void;
};

type WaMutationObserverProps = {
  /** Watches for changes to attributes. To watch only specific attributes, separate them by a space, e.g.
`attr="class id title"`. To watch all attributes, use `*`. */
  attr?: WaMutationObserver["attr"];
  /** Indicates whether or not the attribute's previous value should be recorded when monitoring changes. */
  "attr-old-value"?: WaMutationObserver["attrOldValue"];
  /** Watches for changes to the character data contained within the node. */
  "char-data"?: WaMutationObserver["charData"];
  /** Indicates whether or not the previous value of the node's text should be recorded. */
  "char-data-old-value"?: WaMutationObserver["charDataOldValue"];
  /** Watches for the addition or removal of new child nodes. */
  "child-list"?: WaMutationObserver["childList"];
  /** Disables the observer. */
  disabled?: WaMutationObserver["disabled"];
  /**  */
  dir?: WaMutationObserver["dir"];
  /**  */
  lang?: WaMutationObserver["lang"];
  /**  */
  "did-ssr"?: WaMutationObserver["didSSR"];
  /**  */
  initialReflectedProperties?: WaMutationObserver["initialReflectedProperties"];
  /**  */
  internals?: WaMutationObserver["internals"];
  /** Emitted when a mutation occurs. */
  "onwa-mutation"?: (e: CustomEvent<{ mutationList: MutationRecord[] }>) => void;
};

type WaNumberInputProps = {
  /**  */
  title?: WaNumberInput["title"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaNumberInput["defaultValue"];
  /** The input's size. */
  size?: WaNumberInput["size"];
  /** The input's visual appearance. */
  appearance?: WaNumberInput["appearance"];
  /** Draws a pill-style input with rounded edges. */
  pill?: WaNumberInput["pill"];
  /** The input's label. If you need to display HTML, use the `label` slot instead. */
  label?: WaNumberInput["label"];
  /** The input's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaNumberInput["hint"];
  /** Placeholder text to show as a hint when the input is empty. */
  placeholder?: WaNumberInput["placeholder"];
  /** Makes the input readonly. */
  readonly?: WaNumberInput["readonly"];
  /** Makes the input a required field. */
  required?: WaNumberInput["required"];
  /** The input's minimum value. */
  min?: WaNumberInput["min"];
  /** The input's maximum value. */
  max?: WaNumberInput["max"];
  /** Specifies the granularity that the value must adhere to, or the special value `any` which means no stepping is
implied, allowing any numeric value. */
  step?: WaNumberInput["step"];
  /** Hides the increment/decrement stepper buttons. */
  "without-steppers"?: WaNumberInput["withoutSteppers"];
  /** Specifies what permission the browser has to provide assistance in filling out form field values. Refer to
[this page on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for available values. */
  autocomplete?: WaNumberInput["autocomplete"];
  /** Indicates that the input should receive focus on page load. */
  autofocus?: WaNumberInput["autofocus"];
  /** Used to customize the label or icon of the Enter key on virtual keyboards. */
  enterkeyhint?: WaNumberInput["enterkeyhint"];
  /** Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual
keyboard on supportive devices. */
  inputmode?: WaNumberInput["inputmode"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaNumberInput["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaNumberInput["withHint"];
  /** The name of the input, submitted as a name/value pair with form data. */
  name?: WaNumberInput["name"];
  /** Disables the form control. */
  disabled?: WaNumberInput["disabled"];
  /**  */
  "custom-error"?: WaNumberInput["customError"];
  /**  */
  dir?: WaNumberInput["dir"];
  /**  */
  lang?: WaNumberInput["lang"];
  /**  */
  "did-ssr"?: WaNumberInput["didSSR"];
  /**  */
  assumeInteractionOn?: WaNumberInput["assumeInteractionOn"];
  /**  */
  input?: WaNumberInput["input"];
  /** The current value of the input, submitted as a name/value pair with form data. */
  value?: WaNumberInput["value"];
  /**  */
  valueHasChanged?: WaNumberInput["valueHasChanged"];
  /**  */
  hasInteracted?: WaNumberInput["hasInteracted"];
  /**  */
  states?: WaNumberInput["states"];
  /**  */
  emitInvalid?: WaNumberInput["emitInvalid"];
  /**  */
  labels?: WaNumberInput["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaNumberInput["form"];
  /**  */
  validity?: WaNumberInput["validity"];
  /**  */
  willValidate?: WaNumberInput["willValidate"];
  /**  */
  validationMessage?: WaNumberInput["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaNumberInput["validationTarget"];
  /**  */
  allValidators?: WaNumberInput["allValidators"];
  /**  */
  initialReflectedProperties?: WaNumberInput["initialReflectedProperties"];
  /**  */
  internals?: WaNumberInput["internals"];
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when an alteration to the control's value is committed by the user. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaTagProps = {
  /** The tag's theme variant. Defaults to `neutral` if not within another element with a variant. */
  variant?: WaTag["variant"];
  /** The tag's visual appearance. */
  appearance?: WaTag["appearance"];
  /** The tag's size. */
  size?: WaTag["size"];
  /** Draws a pill-style tag with rounded edges. */
  pill?: WaTag["pill"];
  /** Makes the tag removable and shows a remove button. */
  "with-remove"?: WaTag["withRemove"];
  /**  */
  dir?: WaTag["dir"];
  /**  */
  lang?: WaTag["lang"];
  /**  */
  "did-ssr"?: WaTag["didSSR"];
  /**  */
  initialReflectedProperties?: WaTag["initialReflectedProperties"];
  /**  */
  internals?: WaTag["internals"];
  /** Emitted when the remove button is activated. */
  "onwa-remove"?: (e: CustomEvent<never>) => void;
};

type WaOptionProps = {
  /** The option's value. When selected, the containing form control will receive this value. The value must be unique
from other options in the same group. Values may not contain spaces, as spaces are used as delimiters when listing
multiple values. */
  value?: WaOption["value"];
  /** Draws the option in a disabled state, preventing selection. */
  disabled?: WaOption["disabled"];
  /** Selects an option initially. */
  selected?: WaOption["defaultSelected"];
  /** The option’s plain text label.
Usually automatically generated, but can be useful to provide manually for cases involving complex content. */
  label?: WaOption["label"];
  /**  */
  dir?: WaOption["dir"];
  /**  */
  lang?: WaOption["lang"];
  /**  */
  "did-ssr"?: WaOption["didSSR"];
  /**  */
  defaultSlot?: WaOption["defaultSlot"];
  /**  */
  current?: WaOption["current"];
  /**  */
  _label?: WaOption["_label"];
  /** The default label, generated from the element contents. Will be equal to `label` in most cases. */
  defaultLabel?: WaOption["defaultLabel"];
  /**  */
  initialReflectedProperties?: WaOption["initialReflectedProperties"];
  /**  */
  internals?: WaOption["internals"];
};

type WaSelectProps = {
  /** The name of the select, submitted as a name/value pair with form data. */
  name?: WaSelect["name"];
  /** The select's value. This will be a string for single select or an array for multi-select. */
  value?: WaSelect["value"];
  /** The select's size. */
  size?: WaSelect["size"];
  /** Placeholder text to show as a hint when the select is empty. */
  placeholder?: WaSelect["placeholder"];
  /** Allows more than one option to be selected. */
  multiple?: WaSelect["multiple"];
  /** The maximum number of selected options to show when `multiple` is true. After the maximum, "+n" will be shown to
indicate the number of additional items that are selected. Set to 0 to remove the limit. */
  "max-options-visible"?: WaSelect["maxOptionsVisible"];
  /** Disables the select control. */
  disabled?: WaSelect["disabled"];
  /** Adds a clear button when the select is not empty. */
  "with-clear"?: WaSelect["withClear"];
  /** Indicates whether or not the select is open. You can toggle this attribute to show and hide the menu, or you can
use the `show()` and `hide()` methods and this attribute will reflect the select's open state. */
  open?: WaSelect["open"];
  /** The select's visual appearance. */
  appearance?: WaSelect["appearance"];
  /** Draws a pill-style select with rounded edges. */
  pill?: WaSelect["pill"];
  /** The select's label. If you need to display HTML, use the `label` slot instead. */
  label?: WaSelect["label"];
  /** The preferred placement of the select's menu. Note that the actual placement may vary as needed to keep the listbox
inside of the viewport. */
  placement?: WaSelect["placement"];
  /** The select's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaSelect["hint"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaSelect["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaSelect["withHint"];
  /** The select's required attribute. */
  required?: WaSelect["required"];
  /**  */
  "custom-error"?: WaSelect["customError"];
  /**  */
  dir?: WaSelect["dir"];
  /**  */
  lang?: WaSelect["lang"];
  /**  */
  "did-ssr"?: WaSelect["didSSR"];
  /**  */
  assumeInteractionOn?: WaSelect["assumeInteractionOn"];
  /**  */
  popup?: WaSelect["popup"];
  /**  */
  combobox?: WaSelect["combobox"];
  /**  */
  displayInput?: WaSelect["displayInput"];
  /**  */
  valueInput?: WaSelect["valueInput"];
  /**  */
  listbox?: WaSelect["listbox"];
  /** Where to anchor native constraint validation */
  validationTarget?: WaSelect["validationTarget"];
  /**  */
  displayLabel?: WaSelect["displayLabel"];
  /**  */
  currentOption?: WaSelect["currentOption"];
  /**  */
  selectedOptions?: WaSelect["selectedOptions"];
  /**  */
  defaultValue?: WaSelect["defaultValue"];
  /** A function that customizes the tags to be rendered when multiple=true. The first argument is the option, the second
is the current tag's index.  The function should return either a Lit TemplateResult or a string containing trusted
HTML of the symbol to render at the specified value. */
  getTag?: WaSelect["getTag"];
  /**  */
  input?: WaSelect["input"];
  /**  */
  valueHasChanged?: WaSelect["valueHasChanged"];
  /**  */
  hasInteracted?: WaSelect["hasInteracted"];
  /**  */
  states?: WaSelect["states"];
  /**  */
  emitInvalid?: WaSelect["emitInvalid"];
  /**  */
  labels?: WaSelect["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaSelect["form"];
  /**  */
  validity?: WaSelect["validity"];
  /**  */
  willValidate?: WaSelect["willValidate"];
  /**  */
  validationMessage?: WaSelect["validationMessage"];
  /**  */
  allValidators?: WaSelect["allValidators"];
  /**  */
  initialReflectedProperties?: WaSelect["initialReflectedProperties"];
  /**  */
  internals?: WaSelect["internals"];
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when the control's value changes. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the control's value is cleared. */
  "onwa-clear"?: (e: CustomEvent<never>) => void;
  /** Emitted when the select's menu opens. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the select's menu opens and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the select's menu closes. */
  "onwa-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted after the select's menu closes and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaPopoverProps = {
  /** The preferred placement of the popover. Note that the actual placement may vary as needed to keep the popover
inside of the viewport. */
  placement?: WaPopover["placement"];
  /** Shows or hides the popover. */
  open?: WaPopover["open"];
  /** The distance in pixels from which to offset the popover away from its target. */
  distance?: WaPopover["distance"];
  /** The distance in pixels from which to offset the popover along its target. */
  skidding?: WaPopover["skidding"];
  /** The ID of the popover's anchor element. This must be an interactive/focusable element such as a button. */
  for?: WaPopover["for"];
  /** Removes the arrow from the popover. */
  "without-arrow"?: WaPopover["withoutArrow"];
  /**  */
  dir?: WaPopover["dir"];
  /**  */
  lang?: WaPopover["lang"];
  /**  */
  "did-ssr"?: WaPopover["didSSR"];
  /**  */
  dialog?: WaPopover["dialog"];
  /**  */
  body?: WaPopover["body"];
  /**  */
  popup?: WaPopover["popup"];
  /**  */
  anchor?: WaPopover["anchor"];
  /**  */
  initialReflectedProperties?: WaPopover["initialReflectedProperties"];
  /**  */
  internals?: WaPopover["internals"];
  /** Emitted when the popover begins to show. Canceling this event will stop the popover from showing. */
  "onwa-show"?: (e: CustomEvent<never>) => void;
  /** Emitted after the popover has shown and all animations are complete. */
  "onwa-after-show"?: (e: CustomEvent<never>) => void;
  /** Emitted when the popover begins to hide. Canceling this event will stop the popover from hiding. */
  "onwa-hide"?: (e: CustomEvent<never>) => void;
  /** Emitted after the popover has hidden and all animations are complete. */
  "onwa-after-hide"?: (e: CustomEvent<never>) => void;
};

type WaProgressBarProps = {
  /** The current progress as a percentage, 0 to 100. */
  value?: WaProgressBar["value"];
  /** When true, percentage is ignored, the label is hidden, and the progress bar is drawn in an indeterminate state. */
  indeterminate?: WaProgressBar["indeterminate"];
  /** A custom label for assistive devices. */
  label?: WaProgressBar["label"];
  /**  */
  dir?: WaProgressBar["dir"];
  /**  */
  lang?: WaProgressBar["lang"];
  /**  */
  "did-ssr"?: WaProgressBar["didSSR"];
  /**  */
  initialReflectedProperties?: WaProgressBar["initialReflectedProperties"];
  /**  */
  internals?: WaProgressBar["internals"];
};

type WaProgressRingProps = {
  /** The current progress as a percentage, 0 to 100. */
  value?: WaProgressRing["value"];
  /** A custom label for assistive devices. */
  label?: WaProgressRing["label"];
  /**  */
  dir?: WaProgressRing["dir"];
  /**  */
  lang?: WaProgressRing["lang"];
  /**  */
  "did-ssr"?: WaProgressRing["didSSR"];
  /**  */
  indicator?: WaProgressRing["indicator"];
  /**  */
  indicatorOffset?: WaProgressRing["indicatorOffset"];
  /**  */
  initialReflectedProperties?: WaProgressRing["initialReflectedProperties"];
  /**  */
  internals?: WaProgressRing["internals"];
};

type WaQrCodeProps = {
  /** The QR code's value. */
  value?: WaQrCode["value"];
  /** The label for assistive devices to announce. If unspecified, the value will be used instead. */
  label?: WaQrCode["label"];
  /** The size of the QR code, in pixels. */
  size?: WaQrCode["size"];
  /** @deprecated Use the `color` CSS property instead. - The fill color. This can be any valid CSS color, but not a CSS custom property. */
  fill?: WaQrCode["fill"];
  /** @deprecated Use the `background` or `background-color` CSS property on the host element instead. - The background color. This can be any valid CSS color or `transparent`. It cannot be a CSS custom property. */
  background?: WaQrCode["background"];
  /** The edge radius of each module. Must be between 0 and 0.5. */
  radius?: WaQrCode["radius"];
  /** The level of error correction to use. [Learn more](https://www.qrcode.com/en/about/error_correction.html) */
  "error-correction"?: WaQrCode["errorCorrection"];
  /**  */
  dir?: WaQrCode["dir"];
  /**  */
  lang?: WaQrCode["lang"];
  /**  */
  "did-ssr"?: WaQrCode["didSSR"];
  /**  */
  canvas?: WaQrCode["canvas"];
  /**  */
  initialReflectedProperties?: WaQrCode["initialReflectedProperties"];
  /**  */
  internals?: WaQrCode["internals"];
};

type WaRadioProps = {
  /** The radio's value. When selected, the radio group will receive this value. */
  value?: WaRadio["value"];
  /** The radio's visual appearance. */
  appearance?: WaRadio["appearance"];
  /** The radio's size. When used inside a radio group, the size will be determined by the radio group's size, which will
override this attribute. */
  size?: WaRadio["size"];
  /** Disables the radio. */
  disabled?: WaRadio["disabled"];
  /** The name of the input, submitted as a name/value pair with form data. */
  name?: WaRadio["name"];
  /**  */
  "custom-error"?: WaRadio["customError"];
  /**  */
  dir?: WaRadio["dir"];
  /**  */
  lang?: WaRadio["lang"];
  /**  */
  "did-ssr"?: WaRadio["didSSR"];
  /**  */
  checked?: WaRadio["checked"];
  /**  */
  required?: WaRadio["required"];
  /**  */
  assumeInteractionOn?: WaRadio["assumeInteractionOn"];
  /**  */
  input?: WaRadio["input"];
  /**  */
  valueHasChanged?: WaRadio["valueHasChanged"];
  /**  */
  hasInteracted?: WaRadio["hasInteracted"];
  /**  */
  states?: WaRadio["states"];
  /**  */
  emitInvalid?: WaRadio["emitInvalid"];
  /**  */
  labels?: WaRadio["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaRadio["form"];
  /**  */
  validity?: WaRadio["validity"];
  /**  */
  willValidate?: WaRadio["willValidate"];
  /**  */
  validationMessage?: WaRadio["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaRadio["validationTarget"];
  /**  */
  allValidators?: WaRadio["allValidators"];
  /**  */
  initialReflectedProperties?: WaRadio["initialReflectedProperties"];
  /**  */
  internals?: WaRadio["internals"];
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
};

type WaRadioGroupProps = {
  /** The radio group's label. Required for proper accessibility. If you need to display HTML, use the `label` slot
instead. */
  label?: WaRadioGroup["label"];
  /** The radio groups's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaRadioGroup["hint"];
  /** The name of the radio group, submitted as a name/value pair with form data. */
  name?: WaRadioGroup["name"];
  /** Disables the radio group and all child radios. */
  disabled?: WaRadioGroup["disabled"];
  /** The orientation in which to show radio items. */
  orientation?: WaRadioGroup["orientation"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaRadioGroup["defaultValue"];
  /** The radio group's size. When present, this size will be applied to all `<wa-radio>` items inside. */
  size?: WaRadioGroup["size"];
  /** Ensures a child radio is checked before allowing the containing form to submit. */
  required?: WaRadioGroup["required"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaRadioGroup["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaRadioGroup["withHint"];
  /**  */
  "custom-error"?: WaRadioGroup["customError"];
  /**  */
  dir?: WaRadioGroup["dir"];
  /**  */
  lang?: WaRadioGroup["lang"];
  /**  */
  "did-ssr"?: WaRadioGroup["didSSR"];
  /**  */
  defaultSlot?: WaRadioGroup["defaultSlot"];
  /** The current value of the radio group, submitted as a name/value pair with form data. */
  value?: WaRadioGroup["value"];
  /** We use the first available radio as the validationTarget similar to native HTML that shows the validation popup on
the first radio element. */
  validationTarget?: WaRadioGroup["validationTarget"];
  /**  */
  assumeInteractionOn?: WaRadioGroup["assumeInteractionOn"];
  /**  */
  input?: WaRadioGroup["input"];
  /**  */
  valueHasChanged?: WaRadioGroup["valueHasChanged"];
  /**  */
  hasInteracted?: WaRadioGroup["hasInteracted"];
  /**  */
  states?: WaRadioGroup["states"];
  /**  */
  emitInvalid?: WaRadioGroup["emitInvalid"];
  /**  */
  labels?: WaRadioGroup["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaRadioGroup["form"];
  /**  */
  validity?: WaRadioGroup["validity"];
  /**  */
  willValidate?: WaRadioGroup["willValidate"];
  /**  */
  validationMessage?: WaRadioGroup["validationMessage"];
  /**  */
  allValidators?: WaRadioGroup["allValidators"];
  /**  */
  initialReflectedProperties?: WaRadioGroup["initialReflectedProperties"];
  /**  */
  internals?: WaRadioGroup["internals"];
  /** Emitted when the radio group receives user input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when the radio group's selected value changes. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaRatingProps = {
  /** The name of the rating, submitted as a name/value pair with form data. */
  name?: WaRating["name"];
  /** A label that describes the rating to assistive devices. */
  label?: WaRating["label"];
  /** The current rating. */
  value?: WaRating["value"];
  /** The default value of the form control. Used to reset the rating to its initial value. */
  "default-value"?: WaRating["defaultValue"];
  /** The highest rating to show. */
  max?: WaRating["max"];
  /** The precision at which the rating will increase and decrease. For example, to allow half-star ratings, set this
attribute to `0.5`. */
  precision?: WaRating["precision"];
  /** Makes the rating readonly. */
  readonly?: WaRating["readonly"];
  /** Disables the rating. */
  disabled?: WaRating["disabled"];
  /** Makes the rating a required field. */
  required?: WaRating["required"];
  /** A function that customizes the symbol to be rendered. The first and only argument is the rating's current value.
The function should return a string containing trusted HTML of the symbol to render at the specified value. Works
well with `<wa-icon>` elements. */
  getSymbol?: WaRating["getSymbol"];
  /** The component's size. */
  size?: WaRating["size"];
  /**  */
  "custom-error"?: WaRating["customError"];
  /**  */
  dir?: WaRating["dir"];
  /**  */
  lang?: WaRating["lang"];
  /**  */
  "did-ssr"?: WaRating["didSSR"];
  /**  */
  assumeInteractionOn?: WaRating["assumeInteractionOn"];
  /**  */
  input?: WaRating["input"];
  /**  */
  valueHasChanged?: WaRating["valueHasChanged"];
  /**  */
  hasInteracted?: WaRating["hasInteracted"];
  /**  */
  states?: WaRating["states"];
  /**  */
  emitInvalid?: WaRating["emitInvalid"];
  /**  */
  labels?: WaRating["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaRating["form"];
  /**  */
  validity?: WaRating["validity"];
  /**  */
  willValidate?: WaRating["willValidate"];
  /**  */
  validationMessage?: WaRating["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaRating["validationTarget"];
  /**  */
  allValidators?: WaRating["allValidators"];
  /**  */
  initialReflectedProperties?: WaRating["initialReflectedProperties"];
  /**  */
  internals?: WaRating["internals"];
  /** Emitted when the rating's value changes. */
  onchange?: (e: CustomEvent<never>) => void;
  /** Emitted when the user hovers over a value. The `phase` property indicates when hovering starts, moves to a new value, or ends. The `value` property tells what the rating's value would be if the user were to commit to the hovered value. */
  "onwa-hover"?: (e: CustomEvent<{ phase: "start" | "move" | "end"; value: number }>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaRelativeTimeProps = {
  /** The date from which to calculate time from. If not set, the current date and time will be used. When passing a
string, it's strongly recommended to use the ISO 8601 format to ensure timezones are handled correctly. To convert
a date to this format in JavaScript, use [`date.toISOString()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString). */
  date?: WaRelativeTime["date"];
  /** The formatting style to use. */
  format?: WaRelativeTime["format"];
  /** When `auto`, values such as "yesterday" and "tomorrow" will be shown when possible. When `always`, values such as
"1 day ago" and "in 1 day" will be shown. */
  numeric?: WaRelativeTime["numeric"];
  /** Keep the displayed value up to date as time passes. */
  sync?: WaRelativeTime["sync"];
  /**  */
  dir?: WaRelativeTime["dir"];
  /**  */
  lang?: WaRelativeTime["lang"];
  /**  */
  "did-ssr"?: WaRelativeTime["didSSR"];
  /**  */
  initialReflectedProperties?: WaRelativeTime["initialReflectedProperties"];
  /**  */
  internals?: WaRelativeTime["internals"];
};

type WaScrollerProps = {
  /** The scroller's orientation. */
  orientation?: WaScroller["orientation"];
  /** Removes the visible scrollbar. */
  "without-scrollbar"?: WaScroller["withoutScrollbar"];
  /** Removes the shadows. */
  "without-shadow"?: WaScroller["withoutShadow"];
  /**  */
  dir?: WaScroller["dir"];
  /**  */
  lang?: WaScroller["lang"];
  /**  */
  "did-ssr"?: WaScroller["didSSR"];
  /**  */
  content?: WaScroller["content"];
  /**  */
  canScroll?: WaScroller["canScroll"];
  /**  */
  initialReflectedProperties?: WaScroller["initialReflectedProperties"];
  /**  */
  internals?: WaScroller["internals"];
};

type WaResizeObserverProps = {
  /** Disables the observer. */
  disabled?: WaResizeObserver["disabled"];
  /**  */
  dir?: WaResizeObserver["dir"];
  /**  */
  lang?: WaResizeObserver["lang"];
  /**  */
  "did-ssr"?: WaResizeObserver["didSSR"];
  /**  */
  initialReflectedProperties?: WaResizeObserver["initialReflectedProperties"];
  /**  */
  internals?: WaResizeObserver["internals"];
  /** Emitted when the element is resized. */
  "onwa-resize"?: (e: CustomEvent<{ entries: ResizeObserverEntry[] }>) => void;
};

type WaSkeletonProps = {
  /** Determines which effect the skeleton will use. */
  effect?: WaSkeleton["effect"];
  /**  */
  dir?: WaSkeleton["dir"];
  /**  */
  lang?: WaSkeleton["lang"];
  /**  */
  "did-ssr"?: WaSkeleton["didSSR"];
  /**  */
  initialReflectedProperties?: WaSkeleton["initialReflectedProperties"];
  /**  */
  internals?: WaSkeleton["internals"];
};

type WaSliderProps = {
  /** The slider's label. If you need to provide HTML in the label, use the `label` slot instead. */
  label?: WaSlider["label"];
  /** The slider hint. If you need to display HTML, use the hint slot instead. */
  hint?: WaSlider["hint"];
  /** The name of the slider. This will be submitted with the form as a name/value pair. */
  name?: WaSlider["name"];
  /** The minimum value of a range selection. Used only when range attribute is set. */
  "min-value"?: WaSlider["minValue"];
  /** The maximum value of a range selection. Used only when range attribute is set. */
  "max-value"?: WaSlider["maxValue"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaSlider["defaultValue"];
  /** Converts the slider to a range slider with two thumbs. */
  range?: WaSlider["range"];
  /** Disables the slider. */
  disabled?: WaSlider["disabled"];
  /** Makes the slider a read-only field. */
  readonly?: WaSlider["readonly"];
  /** The orientation of the slider. */
  orientation?: WaSlider["orientation"];
  /** The slider's size. */
  size?: WaSlider["size"];
  /** The starting value from which to draw the slider's fill, which is based on its current value. */
  "indicator-offset"?: WaSlider["indicatorOffset"];
  /** The minimum value allowed. */
  min?: WaSlider["min"];
  /** The maximum value allowed. */
  max?: WaSlider["max"];
  /** The granularity the value must adhere to when incrementing and decrementing. */
  step?: WaSlider["step"];
  /** Tells the browser to focus the slider when the page loads or a dialog is shown. */
  autofocus?: WaSlider["autofocus"];
  /** The distance of the tooltip from the slider's thumb. */
  "tooltip-distance"?: WaSlider["tooltipDistance"];
  /** The placement of the tooltip in reference to the slider's thumb. */
  "tooltip-placement"?: WaSlider["tooltipPlacement"];
  /** Draws markers at each step along the slider. */
  "with-markers"?: WaSlider["withMarkers"];
  /** Draws a tooltip above the thumb when the control has focus or is dragged. */
  "with-tooltip"?: WaSlider["withTooltip"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaSlider["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaSlider["withHint"];
  /**  */
  "custom-error"?: WaSlider["customError"];
  /**  */
  dir?: WaSlider["dir"];
  /**  */
  lang?: WaSlider["lang"];
  /**  */
  "did-ssr"?: WaSlider["didSSR"];
  /** Override validation target to point to the focusable element */
  validationTarget?: WaSlider["validationTarget"];
  /**  */
  slider?: WaSlider["slider"];
  /**  */
  thumb?: WaSlider["thumb"];
  /**  */
  thumbMin?: WaSlider["thumbMin"];
  /**  */
  thumbMax?: WaSlider["thumbMax"];
  /**  */
  track?: WaSlider["track"];
  /**  */
  tooltip?: WaSlider["tooltip"];
  /** The current value of the slider, submitted as a name/value pair with form data. */
  value?: WaSlider["value"];
  /** Get if this is a range slider */
  isRange?: WaSlider["isRange"];
  /** A custom formatting function to apply to the value. This will be shown in the tooltip and announced by screen
readers. Must be set with JavaScript. Property only. */
  valueFormatter?: WaSlider["valueFormatter"];
  /**  */
  required?: WaSlider["required"];
  /**  */
  assumeInteractionOn?: WaSlider["assumeInteractionOn"];
  /**  */
  input?: WaSlider["input"];
  /**  */
  valueHasChanged?: WaSlider["valueHasChanged"];
  /**  */
  hasInteracted?: WaSlider["hasInteracted"];
  /**  */
  states?: WaSlider["states"];
  /**  */
  emitInvalid?: WaSlider["emitInvalid"];
  /**  */
  labels?: WaSlider["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaSlider["form"];
  /**  */
  validity?: WaSlider["validity"];
  /**  */
  willValidate?: WaSlider["willValidate"];
  /**  */
  validationMessage?: WaSlider["validationMessage"];
  /**  */
  allValidators?: WaSlider["allValidators"];
  /**  */
  initialReflectedProperties?: WaSlider["initialReflectedProperties"];
  /**  */
  internals?: WaSlider["internals"];
  /** Emitted when an alteration to the control's value is committed by the user. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<FocusEvent>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<FocusEvent>) => void;
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaSwitchProps = {
  /**  */
  title?: WaSwitch["title"];
  /** The name of the switch, submitted as a name/value pair with form data. */
  name?: WaSwitch["name"];
  /** The value of the switch, submitted as a name/value pair with form data. */
  value?: WaSwitch["value"];
  /** The switch's size. */
  size?: WaSwitch["size"];
  /** Disables the switch. */
  disabled?: WaSwitch["disabled"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  checked?: WaSwitch["defaultChecked"];
  /** Makes the switch a required field. */
  required?: WaSwitch["required"];
  /** The switch's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaSwitch["hint"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaSwitch["withHint"];
  /**  */
  "custom-error"?: WaSwitch["customError"];
  /**  */
  dir?: WaSwitch["dir"];
  /**  */
  lang?: WaSwitch["lang"];
  /**  */
  "did-ssr"?: WaSwitch["didSSR"];
  /**  */
  input?: WaSwitch["input"];
  /**  */
  _checked?: WaSwitch["_checked"];
  /** Draws the checkbox in a checked state. */
  checked?: WaSwitch["checked"];
  /**  */
  assumeInteractionOn?: WaSwitch["assumeInteractionOn"];
  /**  */
  valueHasChanged?: WaSwitch["valueHasChanged"];
  /**  */
  hasInteracted?: WaSwitch["hasInteracted"];
  /**  */
  states?: WaSwitch["states"];
  /**  */
  emitInvalid?: WaSwitch["emitInvalid"];
  /**  */
  labels?: WaSwitch["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaSwitch["form"];
  /**  */
  validity?: WaSwitch["validity"];
  /**  */
  willValidate?: WaSwitch["willValidate"];
  /**  */
  validationMessage?: WaSwitch["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaSwitch["validationTarget"];
  /**  */
  allValidators?: WaSwitch["allValidators"];
  /**  */
  initialReflectedProperties?: WaSwitch["initialReflectedProperties"];
  /**  */
  internals?: WaSwitch["internals"];
  /** Emitted when the control's checked state changes. */
  onchange?: (e: CustomEvent<Event>) => void;
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<InputEvent>) => void;
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaTabProps = {
  /** The name of the tab panel this tab is associated with. The panel must be located in the same tab group. */
  panel?: WaTab["panel"];
  /** Disables the tab and prevents selection. */
  disabled?: WaTab["disabled"];
  /**  */
  dir?: WaTab["dir"];
  /**  */
  lang?: WaTab["lang"];
  /**  */
  "did-ssr"?: WaTab["didSSR"];
  /**  */
  tab?: WaTab["tab"];
  /**  */
  initialReflectedProperties?: WaTab["initialReflectedProperties"];
  /**  */
  internals?: WaTab["internals"];
};

type WaSplitPanelProps = {
  /** The current position of the divider from the primary panel's edge as a percentage 0-100. Defaults to 50% of the
container's initial size. */
  position?: WaSplitPanel["position"];
  /** The current position of the divider from the primary panel's edge in pixels. */
  "position-in-pixels"?: WaSplitPanel["positionInPixels"];
  /** Sets the split panel's orientation. */
  orientation?: WaSplitPanel["orientation"];
  /** Disables resizing. Note that the position may still change as a result of resizing the host element. */
  disabled?: WaSplitPanel["disabled"];
  /** If no primary panel is designated, both panels will resize proportionally when the host element is resized. If a
primary panel is designated, it will maintain its size and the other panel will grow or shrink as needed when the
host element is resized. */
  primary?: WaSplitPanel["primary"];
  /** One or more space-separated values at which the divider should snap. Values can be in pixels or percentages, e.g.
`"100px 50%"`. */
  snap?: WaSplitPanel["snap"];
  /** How close the divider must be to a snap point until snapping occurs. */
  "snap-threshold"?: WaSplitPanel["snapThreshold"];
  /**  */
  dir?: WaSplitPanel["dir"];
  /**  */
  lang?: WaSplitPanel["lang"];
  /**  */
  "did-ssr"?: WaSplitPanel["didSSR"];
  /**  */
  divider?: WaSplitPanel["divider"];
  /**  */
  initialReflectedProperties?: WaSplitPanel["initialReflectedProperties"];
  /**  */
  internals?: WaSplitPanel["internals"];
  /** Emitted when the divider's position changes. */
  "onwa-reposition"?: (e: CustomEvent<never>) => void;
};

type WaTabPanelProps = {
  /** The tab panel's name. */
  name?: WaTabPanel["name"];
  /** When true, the tab panel will be shown. */
  active?: WaTabPanel["active"];
  /**  */
  dir?: WaTabPanel["dir"];
  /**  */
  lang?: WaTabPanel["lang"];
  /**  */
  "did-ssr"?: WaTabPanel["didSSR"];
  /**  */
  initialReflectedProperties?: WaTabPanel["initialReflectedProperties"];
  /**  */
  internals?: WaTabPanel["internals"];
};

type WaTabGroupProps = {
  /** Sets the active tab. */
  active?: WaTabGroup["active"];
  /** The placement of the tabs. */
  placement?: WaTabGroup["placement"];
  /** When set to auto, navigating tabs with the arrow keys will instantly show the corresponding tab panel. When set to
manual, the tab will receive focus but will not show until the user presses spacebar or enter. */
  activation?: WaTabGroup["activation"];
  /** Disables the scroll arrows that appear when tabs overflow. */
  "without-scroll-controls"?: WaTabGroup["withoutScrollControls"];
  /**  */
  dir?: WaTabGroup["dir"];
  /**  */
  lang?: WaTabGroup["lang"];
  /**  */
  "did-ssr"?: WaTabGroup["didSSR"];
  /**  */
  tabGroup?: WaTabGroup["tabGroup"];
  /** Default slot for `<wa-tab-panel>` children (inside the `body` part container). */
  defaultSlot?: WaTabGroup["defaultSlot"];
  /**  */
  nav?: WaTabGroup["nav"];
  /**  */
  initialReflectedProperties?: WaTabGroup["initialReflectedProperties"];
  /**  */
  internals?: WaTabGroup["internals"];
  /** Emitted when a tab is shown. */
  "onwa-tab-show"?: (e: CustomEvent<{ name: String }>) => void;
  /** Emitted when a tab is hidden. */
  "onwa-tab-hide"?: (e: CustomEvent<{ name: String }>) => void;
};

type WaTextareaProps = {
  /**  */
  title?: WaTextarea["title"];
  /** The name of the textarea, submitted as a name/value pair with form data. */
  name?: WaTextarea["name"];
  /** The default value of the form control. Primarily used for resetting the form control. */
  value?: WaTextarea["defaultValue"];
  /** The textarea's size. */
  size?: WaTextarea["size"];
  /** The textarea's visual appearance. */
  appearance?: WaTextarea["appearance"];
  /** The textarea's label. If you need to display HTML, use the `label` slot instead. */
  label?: WaTextarea["label"];
  /** The textarea's hint. If you need to display HTML, use the `hint` slot instead. */
  hint?: WaTextarea["hint"];
  /** Placeholder text to show as a hint when the input is empty. */
  placeholder?: WaTextarea["placeholder"];
  /** The number of rows to display by default. */
  rows?: WaTextarea["rows"];
  /** Controls how the textarea can be resized. */
  resize?: WaTextarea["resize"];
  /** Disables the textarea. */
  disabled?: WaTextarea["disabled"];
  /** Makes the textarea readonly. */
  readonly?: WaTextarea["readonly"];
  /** Makes the textarea a required field. */
  required?: WaTextarea["required"];
  /** The minimum length of input that will be considered valid. */
  minlength?: WaTextarea["minlength"];
  /** The maximum length of input that will be considered valid. */
  maxlength?: WaTextarea["maxlength"];
  /** Controls whether and how text input is automatically capitalized as it is entered by the user. */
  autocapitalize?: WaTextarea["autocapitalize"];
  /** Indicates whether the browser's autocorrect feature is on or off. When set as an attribute, use `"off"` or `"on"`.
When set as a property, use `true` or `false`. */
  autocorrect?: WaTextarea["autocorrect"];
  /** Specifies what permission the browser has to provide assistance in filling out form field values. Refer to
[this page on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for available values. */
  autocomplete?: WaTextarea["autocomplete"];
  /** Indicates that the input should receive focus on page load. */
  autofocus?: WaTextarea["autofocus"];
  /** Used to customize the label or icon of the Enter key on virtual keyboards. */
  enterkeyhint?: WaTextarea["enterkeyhint"];
  /** Enables spell checking on the textarea. */
  spellcheck?: WaTextarea["spellcheck"];
  /** Tells the browser what type of data will be entered by the user, allowing it to display the appropriate virtual
keyboard on supportive devices. */
  inputmode?: WaTextarea["inputmode"];
  /** Only required for SSR. Set to `true` if you're slotting in a `label` element so the server-rendered markup
includes the label before the component hydrates on the client. */
  "with-label"?: WaTextarea["withLabel"];
  /** Only required for SSR. Set to `true` if you're slotting in a `hint` element so the server-rendered markup
includes the hint before the component hydrates on the client. */
  "with-hint"?: WaTextarea["withHint"];
  /** Shows a character count below the textarea. When `maxlength` is set, shows remaining characters instead. */
  "with-count"?: WaTextarea["withCount"];
  /**  */
  "custom-error"?: WaTextarea["customError"];
  /**  */
  dir?: WaTextarea["dir"];
  /**  */
  lang?: WaTextarea["lang"];
  /**  */
  "did-ssr"?: WaTextarea["didSSR"];
  /**  */
  assumeInteractionOn?: WaTextarea["assumeInteractionOn"];
  /**  */
  input?: WaTextarea["input"];
  /**  */
  base?: WaTextarea["base"];
  /**  */
  sizeAdjuster?: WaTextarea["sizeAdjuster"];
  /** The current value of the input, submitted as a name/value pair with form data. */
  value?: WaTextarea["value"];
  /**  */
  valueHasChanged?: WaTextarea["valueHasChanged"];
  /**  */
  hasInteracted?: WaTextarea["hasInteracted"];
  /**  */
  states?: WaTextarea["states"];
  /**  */
  emitInvalid?: WaTextarea["emitInvalid"];
  /**  */
  labels?: WaTextarea["labels"];
  /** By default, form controls are associated with the nearest containing `<form>` element. This attribute allows you
to place the form control outside of a form and associate it with the form that has this `id`. The form must be in
the same document or shadow root for this to work. */
  form?: WaTextarea["form"];
  /**  */
  validity?: WaTextarea["validity"];
  /**  */
  willValidate?: WaTextarea["willValidate"];
  /**  */
  validationMessage?: WaTextarea["validationMessage"];
  /** Override this to change where constraint validation popups are anchored. */
  validationTarget?: WaTextarea["validationTarget"];
  /**  */
  allValidators?: WaTextarea["allValidators"];
  /**  */
  initialReflectedProperties?: WaTextarea["initialReflectedProperties"];
  /**  */
  internals?: WaTextarea["internals"];
  /** Emitted when the control loses focus. */
  onblur?: (e: CustomEvent<never>) => void;
  /** Emitted when an alteration to the control's value is committed by the user. */
  onchange?: (e: CustomEvent<never>) => void;
  /** Emitted when the control gains focus. */
  onfocus?: (e: CustomEvent<never>) => void;
  /** Emitted when the control receives input. */
  oninput?: (e: CustomEvent<never>) => void;
  /** Emitted when the form control has been checked for validity and its constraints aren't satisfied. */
  "onwa-invalid"?: (e: CustomEvent<never>) => void;
};

type WaTreeProps = {
  /** The selection behavior of the tree. Single selection allows only one node to be selected at a time. Multiple
displays checkboxes and allows more than one node to be selected. Leaf allows only leaf nodes to be selected. */
  selection?: WaTree["selection"];
  /**  */
  dir?: WaTree["dir"];
  /**  */
  lang?: WaTree["lang"];
  /**  */
  "did-ssr"?: WaTree["didSSR"];
  /**  */
  defaultSlot?: WaTree["defaultSlot"];
  /**  */
  expandedIconSlot?: WaTree["expandedIconSlot"];
  /**  */
  collapsedIconSlot?: WaTree["collapsedIconSlot"];
  /**  */
  initialReflectedProperties?: WaTree["initialReflectedProperties"];
  /**  */
  internals?: WaTree["internals"];
  /** Emitted when a tree item is selected or deselected. */
  "onwa-selection-change"?: (e: CustomEvent<{ selection: WaTreeItem[] }>) => void;
};

type WaZoomableFrameProps = {
  /** The URL of the content to display. */
  src?: WaZoomableFrame["src"];
  /** Inline HTML to display. */
  srcdoc?: WaZoomableFrame["srcdoc"];
  /** Allows fullscreen mode. */
  allowfullscreen?: WaZoomableFrame["allowfullscreen"];
  /** Controls iframe loading behavior. */
  loading?: WaZoomableFrame["loading"];
  /** Controls referrer information. */
  referrerpolicy?: WaZoomableFrame["referrerpolicy"];
  /** Security restrictions for the iframe. */
  sandbox?: WaZoomableFrame["sandbox"];
  /** The current zoom of the frame, e.g. 0 = 0% and 1 = 100%. */
  zoom?: WaZoomableFrame["zoom"];
  /** The zoom levels to step through when using zoom controls. This does not restrict programmatic changes to the zoom. */
  "zoom-levels"?: WaZoomableFrame["zoomLevels"];
  /** Removes the zoom controls. */
  "without-controls"?: WaZoomableFrame["withoutControls"];
  /** Disables interaction when present. */
  "without-interaction"?: WaZoomableFrame["withoutInteraction"];
  /** Enables automatic theme syncing (light/dark mode and theme selector classes) from the host document to the iframe. */
  "with-theme-sync"?: WaZoomableFrame["withThemeSync"];
  /**  */
  dir?: WaZoomableFrame["dir"];
  /**  */
  lang?: WaZoomableFrame["lang"];
  /**  */
  "did-ssr"?: WaZoomableFrame["didSSR"];
  /**  */
  iframe?: WaZoomableFrame["iframe"];
  /** Returns the internal iframe's `window` object. (Readonly property) */
  contentWindow?: WaZoomableFrame["contentWindow"];
  /** Returns the internal iframe's `document` object. (Readonly property) */
  contentDocument?: WaZoomableFrame["contentDocument"];
  /**  */
  initialReflectedProperties?: WaZoomableFrame["initialReflectedProperties"];
  /**  */
  internals?: WaZoomableFrame["internals"];
  /** Emitted when the internal iframe when it finishes loading. */
  onload?: (e: CustomEvent<Event>) => void;
  /** Emitted from the internal iframe when it fails to load. */
  onerror?: (e: CustomEvent<Event>) => void;
};

type WaMarkdownProps = {
  /** The tab stop width used when converting leading tabs to spaces during whitespace normalization. */
  "tab-size"?: WaMarkdown["tabSize"];
  /**  */
  dir?: WaMarkdown["dir"];
  /**  */
  lang?: WaMarkdown["lang"];
  /**  */
  "did-ssr"?: WaMarkdown["didSSR"];
  /** A reference to the shared Marked instance for convenience. Equivalent to `WaMarkdown.getMarked()`. */
  marked?: WaMarkdown["marked"];
  /**  */
  initialReflectedProperties?: WaMarkdown["initialReflectedProperties"];
  /**  */
  internals?: WaMarkdown["internals"];
};

type WaPageProps = {
  /** The view is a reflection of the "mobileBreakpoint", when the page is larger than the `mobile-breakpoint` (768px by
default), it is considered to be a "desktop" view. The view is merely a way to distinguish when to show/hide the
navigation. You can use additional media queries to make other adjustments to content as necessary.
The default is "desktop" because the "mobile navigation drawer" isn't accessible via SSR due to drawer requiring JS. */
  view?: WaPage["view"];
  /** Whether or not the navigation drawer is open. Note, the navigation drawer is only "open" on mobile views. */
  "nav-open"?: WaPage["navOpen"];
  /** At what page width to hide the "navigation" slot and collapse into a hamburger button.
Accepts both numbers (interpreted as px) and CSS lengths (e.g. `50em`), which are resolved based on the root element. */
  "mobile-breakpoint"?: WaPage["mobileBreakpoint"];
  /** Where to place the navigation when in the mobile viewport. */
  "navigation-placement"?: WaPage["navigationPlacement"];
  /** Determines whether or not to hide the default hamburger button.
This will automatically flip to "true" if you add an element with `data-toggle-nav` anywhere in the element light DOM.
Generally this will be set for you and you don't need to do anything, unless you're using SSR, in which case you should set this manually for initial page loads. */
  "disable-navigation-toggle"?: WaPage["disableNavigationToggle"];
  /**  */
  dir?: WaPage["dir"];
  /**  */
  lang?: WaPage["lang"];
  /**  */
  "did-ssr"?: WaPage["didSSR"];
  /**  */
  header?: WaPage["header"];
  /**  */
  menu?: WaPage["menu"];
  /**  */
  main?: WaPage["main"];
  /**  */
  aside?: WaPage["aside"];
  /**  */
  subheader?: WaPage["subheader"];
  /**  */
  footer?: WaPage["footer"];
  /**  */
  banner?: WaPage["banner"];
  /**  */
  navigationDrawer?: WaPage["navigationDrawer"];
  /**  */
  navigationToggleSlot?: WaPage["navigationToggleSlot"];
  /**  */
  pageResizeObserver?: WaPage["pageResizeObserver"];
  /**  */
  updateAsideAndMenuHeights?: WaPage["updateAsideAndMenuHeights"];
  /**  */
  initialReflectedProperties?: WaPage["initialReflectedProperties"];
  /**  */
  internals?: WaPage["internals"];
};

export type CustomElements = {
  /**
   * Icons are symbols that can be used to represent various options within an application.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-load** - Emitted when the icon has loaded. When using `spriteSheet: true` this will not emit.
   * - **wa-error** - Emitted when the icon fails to load due to an error. When using `spriteSheet: true` this will not emit.
   *
   * ### **CSS Properties:**
   *  - **--animation-delay** - Sets when the animation will start. _(default: 0)_
   * - **--animation-direction** - Defines whether or not the animation should play in reverse on alternate cycles. _(default: normal)_
   * - **--animation-duration** - Defines the length of time that an animation takes to complete one cycle. _(default: 1s)_
   * - **--animation-iteration-count** - Defines the number of times an animation cycle is played. _(default: infinite)_
   * - **--animation-timing** - Describes how the animation will progress over one cycle of its duration. _(default: undefined)_
   * - **--beat-fade-opacity** - Set lowest opacity value an icon with `beat-fade` animation will fade to and from. _(default: undefined)_
   * - **--beat-fade-scale** - Set max value that an icon with `beat-fade` animation will scale. _(default: undefined)_
   * - **--beat-scale** - Set max value that an icon with `beat` animation will scale. _(default: undefined)_
   * - **--bounce-height** - Set the max height an icon with `bounce` animation will jump to when bouncing. _(default: undefined)_
   * - **--bounce-jump-scale-x** - Set the icon’s horizontal distortion (“squish”) at the top of the jump. _(default: undefined)_
   * - **--bounce-jump-scale-y** - Set the icon’s vertical distortion (“squish”) at the top of the jump. _(default: undefined)_
   * - **--bounce-land-scale-x** - Set the icon’s horizontal distortion (“squish”) when landing after the jump. _(default: undefined)_
   * - **--bounce-land-scale-y** - Set the icon’s vertical distortion (“squish”) when landing after the jump. _(default: undefined)_
   * - **--bounce-rebound** - Set the amount of rebound an icon with `bounce` animation has when landing after the jump. _(default: undefined)_
   * - **--bounce-start-scale-x** - Set the icon’s horizontal distortion (“squish”) when starting to bounce. _(default: undefined)_
   * - **--bounce-start-scale-y** - Set the icon’s vertical distortion (“squish”) when starting to bounce. _(default: undefined)_
   * - **--fade-opacity** - Set lowest opacity value an icon with `fade` animation will fade to and from. _(default: undefined)_
   * - **--flip-angle** - Set rotation angle of flip for an icon with `flip` animation. A positive angle denotes a clockwise rotation, a negative angle a counter-clockwise one. _(default: undefined)_
   * - **--flip-x** - Set x-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation. _(default: undefined)_
   * - **--flip-y** - Set y-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation. _(default: undefined)_
   * - **--flip-z** - Set z-coordinate of the vector denoting the axis of rotation (between 0 and 1) for an icon with `flip` animation. _(default: undefined)_
   * - **--primary-color** - Sets a duotone icon's primary color. _(default: currentColor)_
   * - **--primary-opacity** - Sets a duotone icon's primary opacity. _(default: 1)_
   * - **--secondary-color** - Sets a duotone icon's secondary color. _(default: currentColor)_
   * - **--secondary-opacity** - Sets a duotone icon's secondary opacity. _(default: 0.4)_
   *
   * ### **CSS Parts:**
   *  - **svg** - The internal SVG element.
   * - **use** - The `<use>` element generated when using `spriteSheet: true`
   */
  "wa-icon": DefineComponent<WaIconProps>;

  /**
   * Checkboxes allow the user to toggle an option on or off.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when the checked state changes.
   * - **blur** - Emitted when the checkbox loses focus.
   * - **focus** - Emitted when the checkbox gains focus.
   * - **input** - Emitted when the checkbox receives input.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **click()** - Simulates a click on the checkbox.
   * - **focus(options: _FocusOptions_)** - Sets focus on the checkbox.
   * - **blur()** - Removes focus from the checkbox.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The checkbox's label.
   * - **hint** - Text that describes how to use the checkbox. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Properties:**
   *  - **--checked-icon-color** - The color of the checked and indeterminate icons. _(default: undefined)_
   * - **--checked-icon-scale** - The size of the checked and indeterminate icons relative to the checkbox. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's label .
   * - **control** - The square container that wraps the checkbox's checked state.
   * - **checked-icon** - The checked icon, a `<wa-icon>` element.
   * - **indeterminate-icon** - The indeterminate icon, a `<wa-icon>` element.
   * - **label** - The container that wraps the checkbox's label.
   * - **hint** - The hint's wrapper.
   */
  "wa-checkbox": DefineComponent<WaCheckboxProps>;

  /**
   * Spinners are used to show the progress of an indeterminate operation.
   * ---
   *
   *
   * ### **CSS Properties:**
   *  - **--track-width** - The width of the track. _(default: undefined)_
   * - **--track-color** - The color of the track. _(default: undefined)_
   * - **--indicator-color** - The color of the spinner's indicator. _(default: undefined)_
   * - **--speed** - The time it takes for the spinner to complete one animation cycle. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-spinner": DefineComponent<WaSpinnerProps>;

  /**
   * A tree item serves as a hierarchical node that lives inside a [tree](/docs/components/tree).
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-expand** - Emitted when the tree item expands.
   * - **wa-after-expand** - Emitted after the tree item expands and all animations are complete.
   * - **wa-collapse** - Emitted when the tree item collapses.
   * - **wa-after-collapse** - Emitted after the tree item collapses and all animations are complete.
   * - **wa-lazy-change** - Emitted when the tree item's lazy state changes.
   * - **wa-lazy-load** - Emitted when a lazy item is selected. Use this event to asynchronously load data and append items to the tree before expanding. After appending new items, remove the `lazy` attribute to remove the loading state and update the tree.
   *
   * ### **Methods:**
   *  - **getChildrenItems({ includeDisabled = true }: _{ includeDisabled?: boolean }_): _WaTreeItem[]_** - Gets all the nested tree items in this node.
   *
   * ### **Slots:**
   *  - _default_ - The default slot.
   * - **expand-icon** - The icon to show when the tree item is expanded.
   * - **collapse-icon** - The icon to show when the tree item is collapsed.
   *
   * ### **CSS Properties:**
   *  - **--show-duration** - The animation duration when expanding tree items. _(default: 200ms)_
   * - **--hide-duration** - The animation duration when collapsing tree items. _(default: 200ms)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **item** - The tree item's container. This element wraps everything except slotted tree item children.
   * - **indentation** - The tree item's indentation container.
   * - **expand-button** - The container that wraps the tree item's expand button and spinner.
   * - **spinner** - The spinner that shows when a lazy tree item is in the loading state.
   * - **spinner__base** - The spinner's base part.
   * - **label** - The tree item's label.
   * - **children** - The container that wraps the tree item's nested children.
   * - **checkbox** - The checkbox that shows when using multiselect.
   * - **checkbox__base** - The checkbox's exported `base` part.
   * - **checkbox__control** - The checkbox's exported `control` part.
   * - **checkbox__checked-icon** - The checkbox's exported `checked-icon` part.
   * - **checkbox__indeterminate-icon** - The checkbox's exported `indeterminate-icon` part.
   * - **checkbox__label** - The checkbox's exported `label` part.
   */
  "wa-tree-item": DefineComponent<WaTreeItemProps>;

  /**
   * A carousel item represent a slide within a carousel.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The carousel item's content..
   *
   * ### **CSS Properties:**
   *  - **--aspect-ratio** - The slide's aspect ratio. Inherited from the carousel by default. _(default: undefined)_
   */
  "wa-carousel-item": DefineComponent<WaCarouselItemProps>;

  /**
   * Buttons represent actions that are available to the user.
   * ---
   *
   *
   * ### **Events:**
   *  - **blur** - Emitted when the button loses focus.
   * - **focus** - Emitted when the button gains focus.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **click()** - Simulates a click on the button.
   * - **focus(options: _FocusOptions_)** - Sets focus on the button.
   * - **blur()** - Removes focus from the button.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The button's label.
   * - **start** - An element, such as `<wa-icon>`, placed before the label.
   * - **end** - An element, such as `<wa-icon>`, placed after the label.
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **start** - The container that wraps the `start` slot.
   * - **label** - The button's label.
   * - **end** - The container that wraps the `end` slot.
   * - **caret** - The button's caret icon, a `<wa-icon>` element.
   * - **spinner** - The spinner that shows when the button is in the loading state.
   */
  "wa-button": DefineComponent<WaButtonProps>;

  /**
   * A component for displaying animated GIFs and WEBPs that play and pause on interaction.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-load** - Emitted when the image loads successfully.
   * - **wa-error** - Emitted when the image fails to load.
   *
   * ### **Slots:**
   *  - **play-icon** - Optional play icon to use instead of the default. Works best with `<wa-icon>`.
   * - **pause-icon** - Optional pause icon to use instead of the default. Works best with `<wa-icon>`.
   *
   * ### **CSS Properties:**
   *  - **--control-box-size** - The size of the icon box. _(default: undefined)_
   * - **--icon-size** - The size of the play/pause icons. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **control-box** - The container that surrounds the pause/play icons and provides their background.
   */
  "wa-animated-image": DefineComponent<WaAnimatedImageProps>;

  /**
   * Animate elements declaratively with nearly 100 baked-in presets, or roll your own with custom keyframes. Powered by the [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API).
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-cancel** - Emitted when the animation is canceled.
   * - **wa-finish** - Emitted when the animation finishes.
   * - **wa-start** - Emitted when the animation starts or restarts.
   *
   * ### **Methods:**
   *  - **cancel()** - Clears all keyframe effects caused by this animation and aborts its playback.
   * - **finish()** - Sets the playback time to the end of the animation corresponding to the current playback direction.
   *
   * ### **Slots:**
   *  - _default_ - The element to animate. Avoid slotting in more than one element, as subsequent ones will be ignored. To animate multiple elements, either wrap them in a single container or use multiple `<wa-animation>` elements.
   */
  "wa-animation": DefineComponent<WaAnimationProps>;

  /**
   * Avatars are used to represent a person or object.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-error** - The image could not be loaded. This may because of an invalid URL, a temporary network condition, or some unknown cause.
   *
   * ### **Slots:**
   *  - **icon** - The default icon to use when no image or initials are present. Works best with `<wa-icon>`.
   *
   * ### **CSS Properties:**
   *  - **--size** - The size of the avatar. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **icon** - The container that wraps the avatar's icon.
   * - **initials** - The container that wraps the avatar's initials.
   * - **image** - The avatar image. Only shown when the `image` attribute is set.
   */
  "wa-avatar": DefineComponent<WaAvatarProps>;

  /**
   * Badges are used to draw attention and display statuses or counts.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The badge's content.
   * - **start** - An element, such as `<wa-icon>`, placed before the label.
   * - **end** - An element, such as `<wa-icon>`, placed after the label.
   *
   * ### **CSS Properties:**
   *  - **--pulse-color** - The color of the badge's pulse effect when using `attention="pulse"`. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **start** - The container that wraps the `start` slot.
   * - **end** - The container that wraps the `end` slot.
   */
  "wa-badge": DefineComponent<WaBadgeProps>;

  /**
   * Breadcrumb Items are used inside breadcrumbs to represent different links.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The breadcrumb item's label.
   * - **start** - An element, such as `<wa-icon>`, placed before the label.
   * - **end** - An element, such as `<wa-icon>`, placed after the label.
   * - **separator** - The separator to use for the breadcrumb item. This will only change the separator for this item. If you want to change it for all items in the group, set the separator on `<wa-breadcrumb>` instead.
   *
   * ### **CSS Parts:**
   *  - **label** - The breadcrumb item's label.
   * - **start** - The container that wraps the `start` slot.
   * - **end** - The container that wraps the `end` slot.
   * - **separator** - The container that wraps the separator.
   */
  "wa-breadcrumb-item": DefineComponent<WaBreadcrumbItemProps>;

  /**
   * Breadcrumbs provide a group of links so users can easily navigate a website's hierarchy.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - One or more breadcrumb items to display.
   * - **separator** - The separator to use between breadcrumb items. Works best with `<wa-icon>`.
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-breadcrumb": DefineComponent<WaBreadcrumbProps>;

  /**
   * Button groups can be used to group related buttons into sections.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - One or more `<wa-button>` elements to display in the button group.
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-button-group": DefineComponent<WaButtonGroupProps>;

  /**
   * Callouts are used to display important messages inline.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The callout's main content.
   * - **icon** - An icon to show in the callout. Works best with `<wa-icon>`.
   *
   * ### **CSS Parts:**
   *  - **icon** - The container that wraps the optional icon.
   * - **message** - The container that wraps the callout's main content.
   */
  "wa-callout": DefineComponent<WaCalloutProps>;

  /**
   * Cards can be used to group related subjects in a container.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The card's main content.
   * - **header** - An optional header for the card.
   * - **footer** - An optional footer for the card.
   * - **media** - An optional media section to render at the start of the card.
   * - **actions** - An optional actions section to render at the end for the horizontal card.
   * - **header-actions** - An optional actions section to render in the header of the vertical card.
   * - **footer-actions** - An optional actions section to render in the footer of the vertical card.
   *
   * ### **CSS Properties:**
   *  - **--spacing** - The amount of space around and between sections of the card. Expects a single value. _(default: var(--wa-space-l))_
   *
   * ### **CSS Parts:**
   *  - **media** - The container that wraps the card's media.
   * - **header** - The container that wraps the card's header.
   * - **body** - The container that wraps the card's main content.
   * - **footer** - The container that wraps the card's footer.
   */
  "wa-card": DefineComponent<WaCardProps>;

  /**
   * Carousels display an arbitrary number of content slides along a horizontal or vertical axis.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-slide-change** - Emitted when the active slide changes.
   *
   * ### **Methods:**
   *  - **previous(behavior: _ScrollBehavior_)** - Move the carousel backward by `slides-per-move` slides.
   * - **next(behavior: _ScrollBehavior_)** - Move the carousel forward by `slides-per-move` slides.
   * - **goToSlide(index: _number_, behavior: _ScrollBehavior_)** - Scrolls the carousel to the slide specified by `index`.
   *
   * ### **Slots:**
   *  - _default_ - The carousel's main content, one or more `<wa-carousel-item>` elements.
   * - **next-icon** - Optional next icon to use instead of the default. Works best with `<wa-icon>`.
   * - **previous-icon** - Optional previous icon to use instead of the default. Works best with `<wa-icon>`.
   *
   * ### **CSS Properties:**
   *  - **--aspect-ratio** - The aspect ratio of each slide. _(default: 16/9)_
   * - **--scroll-hint** - The amount of padding to apply to the scroll area, allowing adjacent slides to become partially visible as a scroll hint. _(default: undefined)_
   * - **--slide-gap** - The space between each slide. _(default: var(--wa-space-m))_
   *
   * ### **CSS Parts:**
   *  - **base** - The carousel's internal wrapper.
   * - **scroll-container** - The scroll container that wraps the slides.
   * - **pagination** - The pagination indicators wrapper.
   * - **pagination-item** - The pagination indicator.
   * - **pagination-item-active** - Applied when the item is active.
   * - **navigation** - The navigation wrapper.
   * - **navigation-button** - The navigation button.
   * - **navigation-button-previous** - Applied to the previous button.
   * - **navigation-button-next** - Applied to the next button.
   */
  "wa-carousel": DefineComponent<WaCarouselProps>;

  /**
   * Inputs collect data from the user.
   * ---
   *
   *
   * ### **Events:**
   *  - **input** - Emitted when the control receives input.
   * - **change** - Emitted when an alteration to the control's value is committed by the user.
   * - **blur** - Emitted when the control loses focus.
   * - **focus** - Emitted when the control gains focus.
   * - **wa-clear** - Emitted when the clear button is activated.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **focus(options: _FocusOptions_)** - Sets focus on the input.
   * - **blur()** - Removes focus from the input.
   * - **select()** - Selects all the text in the input.
   * - **setSelectionRange(selectionStart: _number_, selectionEnd: _number_, selectionDirection: _'forward' | 'backward' | 'none'_)** - Sets the start and end positions of the text selection (0-based).
   * - **setRangeText(replacement: _string_, start: _number_, end: _number_, selectMode: _'select' | 'start' | 'end' | 'preserve'_)** - Replaces a range of text with a new string.
   * - **showPicker()** - Displays the browser picker for an input element (only works if the browser supports it for the input type).
   * - **stepUp()** - Increments the value of a numeric input type by the value of the step attribute.
   * - **stepDown()** - Decrements the value of a numeric input type by the value of the step attribute.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - **label** - The input's label. Alternatively, you can use the `label` attribute.
   * - **start** - An element, such as `<wa-icon>`, placed at the start of the input control.
   * - **end** - An element, such as `<wa-icon>`, placed at the end of the input control.
   * - **clear-icon** - An icon to use in lieu of the default clear icon.
   * - **show-password-icon** - An icon to use in lieu of the default show password icon.
   * - **hide-password-icon** - An icon to use in lieu of the default hide password icon.
   * - **hint** - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Parts:**
   *  - **label** - The label
   * - **hint** - The hint's wrapper.
   * - **base** - The wrapper being rendered as an input
   * - **input** - The internal `<input>` control.
   * - **start** - The container that wraps the `start` slot.
   * - **clear-button** - The clear button.
   * - **password-toggle-button** - The password toggle button.
   * - **end** - The container that wraps the `end` slot.
   */
  "wa-input": DefineComponent<WaInputProps>;

  /**
   * Popup is a utility that lets you declaratively anchor "popup" containers to another element.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-reposition** - Emitted when the popup is repositioned. This event can fire a lot, so avoid putting expensive operations in your listener or consider debouncing it.
   *
   * ### **Methods:**
   *  - **reposition()** - Forces the popup to recalculate and reposition itself.
   *
   * ### **Slots:**
   *  - _default_ - The popup's content.
   * - **anchor** - The element the popup will be anchored to. If the anchor lives outside of the popup, you can use the `anchor` attribute or property instead.
   *
   * ### **CSS Properties:**
   *  - **--arrow-size** - The size of the arrow. Note that an arrow won't be shown unless the `arrow` attribute is used. _(default: 6px)_
   * - **--popup-border-width** - The width of any custom border applied to the popup. This is used to reposition the arrow to overlap to the inside edge of the popup border. _(default: undefined)_
   * - **--arrow-color** - The color of the arrow. _(default: black)_
   * - **--auto-size-available-width** - A read-only custom property that determines the amount of width the popup can be before overflowing. Useful for positioning child elements that need to overflow. This property is only available when using `auto-size`. _(default: undefined)_
   * - **--auto-size-available-height** - A read-only custom property that determines the amount of height the popup can be before overflowing. Useful for positioning child elements that need to overflow. This property is only available when using `auto-size`. _(default: undefined)_
   * - **--show-duration** - The show duration to use when applying built-in animation classes. _(default: 100ms)_
   * - **--hide-duration** - The hide duration to use when applying built-in animation classes. _(default: 100ms)_
   *
   * ### **CSS Parts:**
   *  - **arrow** - The arrow's container. Avoid setting `top|bottom|left|right` properties, as these values are assigned dynamically as the popup moves. This is most useful for applying a background color to match the popup, and maybe a border or box shadow.
   * - **popup** - The popup's container. Useful for setting a background color, box shadow, etc.
   * - **hover-bridge** - The hover bridge element. Only available when the `hover-bridge` option is enabled.
   */
  "wa-popup": DefineComponent<WaPopupProps>;

  /**
   * Color pickers allow the user to select a color.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when the color picker's value changes.
   * - **input** - Emitted when the color picker receives input.
   * - **wa-show**
   * - **wa-after-show**
   * - **wa-hide**
   * - **wa-after-hide**
   * - **blur** - Emitted when the color picker loses focus.
   * - **focus** - Emitted when the color picker receives focus.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **getHexString(hue: _number_, saturation: _number_, brightness: _number_, alpha)** - Generates a hex string from HSV values. Hue must be 0-360. All other arguments must be 0-100.
   * - **focus(options: _FocusOptions_)** - Sets focus on the color picker.
   * - **blur()** - Removes focus from the color picker.
   * - **getFormattedValue(format: _'hex' | 'hexa' | 'rgb' | 'rgba' | 'hsl' | 'hsla' | 'hsv' | 'hsva'_)** - Returns the current value as a string in the specified format.
   * - **reportValidity()** - Checks for validity and shows the browser's validation message if the control is invalid.
   * - **show()** - Shows the color picker panel.
   * - **hide()** - Hides the color picker panel
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - **label** - The color picker's form label. Alternatively, you can use the `label` attribute.
   * - **hint** - The color picker's form hint. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Properties:**
   *  - **--grid-width** - The width of the color grid. _(default: undefined)_
   * - **--grid-height** - The height of the color grid. _(default: undefined)_
   * - **--grid-handle-size** - The size of the color grid's handle. _(default: undefined)_
   * - **--slider-height** - The height of the hue and alpha sliders. _(default: undefined)_
   * - **--slider-handle-size** - The diameter of the slider's handle. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **trigger** - The color picker's dropdown trigger.
   * - **swatches** - The container that holds the swatches.
   * - **swatch** - Each individual swatch.
   * - **grid** - The color grid.
   * - **grid-handle** - The color grid's handle.
   * - **slider** - Hue and opacity sliders.
   * - **slider-handle** - Hue and opacity slider handles.
   * - **hue-slider** - The hue slider.
   * - **hue-slider-handle** - The hue slider's handle.
   * - **opacity-slider** - The opacity slider.
   * - **opacity-slider-handle** - The opacity slider's handle.
   * - **preview** - The preview color.
   * - **input** - The text input.
   * - **eyedropper-button** - The eye dropper button.
   * - **eyedropper-button__base** - The eye dropper button's exported `button` part.
   * - **eyedropper-button__start** - The eye dropper button's exported `start` part.
   * - **eyedropper-button__label** - The eye dropper button's exported `label` part.
   * - **eyedropper-button__end** - The eye dropper button's exported `end` part.
   * - **eyedropper-button__caret** - The eye dropper button's exported `caret` part.
   * - **format-button** - The format button.
   * - **format-button__base** - The format button's exported `button` part.
   * - **format-button__start** - The format button's exported `start` part.
   * - **format-button__label** - The format button's exported `label` part.
   * - **format-button__end** - The format button's exported `end` part.
   * - **format-button__caret** - The format button's exported `caret` part.
   */
  "wa-color-picker": DefineComponent<WaColorPickerProps>;

  /**
   * Compare visual differences between similar content with a sliding panel.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when the position changes.
   *
   * ### **Slots:**
   *  - **before** - The before content, often an `<img>` or `<svg>` element.
   * - **after** - The after content, often an `<img>` or `<svg>` element.
   * - **handle** - The icon used inside the handle.
   *
   * ### **CSS Properties:**
   *  - **--divider-width** - The width of the dividing line. _(default: undefined)_
   * - **--handle-size** - The size of the compare handle. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The container that wraps the before and after content.
   * - **before** - The container that wraps the before content.
   * - **after** - The container that wraps the after content.
   * - **divider** - The divider that separates the before and after content.
   * - **handle** - The handle that the user drags to expose the after content.
   */
  "wa-comparison": DefineComponent<WaComparisonProps>;

  /**
   * Tooltips display additional information based on a specific action.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the tooltip begins to show.
   * - **wa-after-show** - Emitted after the tooltip has shown and all animations are complete.
   * - **wa-hide** - Emitted when the tooltip begins to hide.
   * - **wa-after-hide** - Emitted after the tooltip has hidden and all animations are complete.
   *
   * ### **Methods:**
   *  - **show()** - Shows the tooltip.
   * - **hide()** - Hides the tooltip
   *
   * ### **Slots:**
   *  - _default_ - The tooltip's default slot where any content should live. Interactive content should be avoided.
   *
   * ### **CSS Properties:**
   *  - **--max-width** - The maximum width of the tooltip before its content will wrap. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper, an `<wa-popup>` element.
   * - **base__popup** - The popup's exported `popup` part. Use this to target the tooltip's popup container.
   * - **base__arrow** - The popup's exported `arrow` part. Use this to target the tooltip's arrow.
   * - **body** - The tooltip's body where its content is rendered.
   */
  "wa-tooltip": DefineComponent<WaTooltipProps>;

  /**
   * Copies text data to the clipboard when the user clicks the trigger.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-copy** - Emitted when the data has been copied.
   * - **wa-error** - Emitted when the data could not be copied.
   *
   * ### **Slots:**
   *  - _default_ - The trigger element. By default, a copy icon button is rendered so this is optional. If desired, you can slot in a custom element such as `<wa-button>` or `<button>`.
   * - **copy-icon** - The icon to show in the default copy state. Works best with `<wa-icon>`.
   * - **success-icon** - The icon to show when the content is copied. Works best with `<wa-icon>`.
   * - **error-icon** - The icon to show when a copy error occurs. Works best with `<wa-icon>`.
   *
   * ### **CSS Parts:**
   *  - **button** - The internal `<button>` element.
   * - **copy-icon** - The container that holds the copy icon.
   * - **success-icon** - The container that holds the success icon.
   * - **error-icon** - The container that holds the error icon.
   * - **tooltip__base** - The tooltip's exported `base` part.
   * - **tooltip__base__popup** - The tooltip's exported `popup` part.
   * - **tooltip__base__arrow** - The tooltip's exported `arrow` part.
   * - **tooltip__body** - The tooltip's exported `body` part.
   */
  "wa-copy-button": DefineComponent<WaCopyButtonProps>;

  /**
   * Details show a brief summary and expand to show additional content.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the details opens.
   * - **wa-after-show** - Emitted after the details opens and all animations are complete.
   * - **wa-hide** - Emitted when the details closes.
   * - **wa-after-hide** - Emitted after the details closes and all animations are complete.
   *
   * ### **Methods:**
   *  - **show()** - Shows the details.
   * - **hide()** - Hides the details
   *
   * ### **Slots:**
   *  - _default_ - The details' main content.
   * - **summary** - The details' summary. Alternatively, you can use the `summary` attribute.
   * - **expand-icon** - Optional expand icon to use instead of the default. Works best with `<wa-icon>`.
   * - **collapse-icon** - Optional collapse icon to use instead of the default. Works best with `<wa-icon>`.
   *
   * ### **CSS Properties:**
   *  - **--spacing** - The amount of space around and between the details' content. Expects a single value. _(default: undefined)_
   * - **--show-duration** - The show duration to use when applying built-in animation classes. _(default: 200ms)_
   * - **--hide-duration** - The hide duration to use when applying built-in animation classes. _(default: 200ms)_
   *
   * ### **CSS Parts:**
   *  - **base** - The inner `<details>` element used to render the component. Styles you apply to the component are automatically applied to this part, so you usually don't need to deal with it unless you need to set the `display` property.
   * - **header** - The header that wraps both the summary and the expand/collapse icon.
   * - **summary** - The container that wraps the summary.
   * - **icon** - The container that wraps the expand/collapse icons.
   * - **content** - The details content.
   */
  "wa-details": DefineComponent<WaDetailsProps>;

  /**
   * Dialogs, sometimes called "modals", appear above the page and require the user's immediate attention.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the dialog opens.
   * - **wa-after-show** - Emitted after the dialog opens and all animations are complete.
   * - **wa-hide** - Emitted when the dialog is requested to close. Calling `event.preventDefault()` will prevent the dialog from closing. You can inspect `event.detail.source` to see which element caused the dialog to close. If the source is the dialog element itself, the user has pressed [[Escape]] or the dialog has been closed programmatically. Avoid using this unless closing the dialog will result in destructive behavior such as data loss.
   * - **wa-after-hide** - Emitted after the dialog closes and all animations are complete.
   *
   * ### **Slots:**
   *  - _default_ - The dialog's main content.
   * - **label** - The dialog's label. Alternatively, you can use the `label` attribute.
   * - **header-actions** - Optional actions to add to the header. Works best with `<wa-button>`.
   * - **footer** - The dialog's footer, usually one or more buttons representing various options.
   *
   * ### **CSS Properties:**
   *  - **--spacing** - The amount of space around and between the dialog's content. _(default: undefined)_
   * - **--width** - The preferred width of the dialog. Note that the dialog will shrink to accommodate smaller screens. _(default: undefined)_
   * - **--show-duration** - The animation duration when showing the dialog. _(default: 200ms)_
   * - **--hide-duration** - The animation duration when hiding the dialog. _(default: 200ms)_
   *
   * ### **CSS Parts:**
   *  - **dialog** - The dialog's internal `<dialog>` element.
   * - **header** - The dialog's header. This element wraps the title and header actions.
   * - **header-actions** - Optional actions to add to the header. Works best with `<wa-button>`.
   * - **title** - The dialog's title.
   * - **close-button** - The close button, a `<wa-button>`.
   * - **close-button__base** - The close button's exported `base` part.
   * - **body** - The dialog's body.
   * - **footer** - The dialog's footer.
   */
  "wa-dialog": DefineComponent<WaDialogProps>;

  /**
   * Dividers are used to visually separate or group elements.
   * ---
   *
   *
   * ### **CSS Properties:**
   *  - **--color** - The color of the divider. _(default: undefined)_
   * - **--width** - The width of the divider. _(default: undefined)_
   * - **--spacing** - The spacing of the divider. _(default: undefined)_
   */
  "wa-divider": DefineComponent<WaDividerProps>;

  /**
   * Drawers slide in from a container to expose additional options and information.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the drawer opens.
   * - **wa-after-show** - Emitted after the drawer opens and all animations are complete.
   * - **wa-hide** - Emitted when the drawer is requesting to close. Calling `event.preventDefault()` will prevent the drawer from closing. You can inspect `event.detail.source` to see which element caused the drawer to close. If the source is the drawer element itself, the user has pressed [[Escape]] or the drawer has been closed programmatically. Avoid using this unless closing the drawer will result in destructive behavior such as data loss.
   * - **wa-after-hide** - Emitted after the drawer closes and all animations are complete.
   *
   * ### **Slots:**
   *  - _default_ - The drawer's main content.
   * - **label** - The drawer's label. Alternatively, you can use the `label` attribute.
   * - **header-actions** - Optional actions to add to the header. Works best with `<wa-button>`.
   * - **footer** - The drawer's footer, usually one or more buttons representing various options.
   *
   * ### **CSS Properties:**
   *  - **--spacing** - The amount of space around and between the drawer's content. _(default: undefined)_
   * - **--size** - The preferred size of the drawer. This will be applied to the drawer's width or height depending on its `placement`. Note that the drawer will shrink to accommodate smaller screens. _(default: undefined)_
   * - **--show-duration** - The animation duration when showing the drawer. _(default: 200ms)_
   * - **--hide-duration** - The animation duration when hiding the drawer. _(default: 200ms)_
   *
   * ### **CSS Parts:**
   *  - **dialog** - The drawer's internal `<dialog>` element.
   * - **header** - The drawer's header. This element wraps the title and header actions.
   * - **header-actions** - Optional actions to add to the header. Works best with `<wa-button>`.
   * - **title** - The drawer's title.
   * - **close-button** - The close button, a `<wa-button>`.
   * - **close-button__base** - The close button's exported `base` part.
   * - **body** - The drawer's body.
   * - **footer** - The drawer's footer.
   */
  "wa-drawer": DefineComponent<WaDrawerProps>;

  /**
   * Represents an individual item within a dropdown menu, supporting standard items, checkboxes, and submenus.
   * ---
   *
   *
   * ### **Events:**
   *  - **blur** - Emitted when the dropdown item loses focus.
   * - **focus** - Emitted when the dropdown item gains focus.
   *
   * ### **Methods:**
   *  - **openSubmenu()** - Opens the submenu.
   * - **closeSubmenu()** - Closes the submenu.
   *
   * ### **Slots:**
   *  - _default_ - The dropdown item's label.
   * - **icon** - An optional icon to display before the label.
   * - **details** - Additional content or details to display after the label.
   * - **submenu** - Submenu items, typically `<wa-dropdown-item>` elements, to create a nested menu.
   *
   * ### **CSS Parts:**
   *  - **checkmark** - The checkmark icon (a `<wa-icon>` element) when the item is a checkbox.
   * - **icon** - The container for the icon slot.
   * - **label** - The container for the label slot.
   * - **details** - The container for the details slot.
   * - **submenu-icon** - The submenu indicator icon (a `<wa-icon>` element).
   * - **submenu** - The submenu container.
   */
  "wa-dropdown-item": DefineComponent<WaDropdownItemProps>;

  /**
   * Dropdowns display a list of options that can be triggered by a button or other element. They support
   * keyboard navigation, submenus, and various customization options.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the dropdown is about to show.
   * - **wa-after-show** - Emitted after the dropdown has been shown.
   * - **wa-hide** - Emitted when the dropdown is about to hide.
   * - **wa-after-hide** - Emitted after the dropdown has been hidden.
   * - **wa-select** - Emitted when an item in the dropdown is selected.
   *
   * ### **Slots:**
   *  - _default_ - The dropdown's items, typically `<wa-dropdown-item>` elements.
   * - **trigger** - The element that triggers the dropdown, such as a `<wa-button>` or `<button>`.
   *
   * ### **CSS Properties:**
   *  - **--show-duration** - The duration of the show animation. _(default: undefined)_
   * - **--hide-duration** - The duration of the hide animation. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's host element.
   * - **menu** - The dropdown menu container.
   */
  "wa-dropdown": DefineComponent<WaDropdownProps>;

  /**
   * Formats a number as a human readable bytes value.
   * ---
   *
   */
  "wa-format-bytes": DefineComponent<WaFormatBytesProps>;

  /**
   * Formats a date/time using the specified locale and options.
   * ---
   *
   */
  "wa-format-date": DefineComponent<WaFormatDateProps>;

  /**
   * Formats a number using the specified locale and options.
   * ---
   *
   */
  "wa-format-number": DefineComponent<WaFormatNumberProps>;

  /**
   * Includes give you the power to embed external HTML files into the page.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-load** - Emitted when the included file is loaded.
   * - **wa-include-error** - Emitted when the included file fails to load due to an error.
   */
  "wa-include": DefineComponent<WaIncludeProps>;

  /**
   * Tracks immediate child elements and fires events as they move in and out of view.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-intersect** - Fired when a tracked element begins or ceases intersecting.
   *
   * ### **Slots:**
   *  - _default_ - Elements to track. Only immediate children of the host are monitored.
   */
  "wa-intersection-observer": DefineComponent<WaIntersectionObserverProps>;

  /**
   * The Mutation Observer component offers a thin, declarative interface to the [`MutationObserver API`](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver).
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-mutation** - Emitted when a mutation occurs.
   *
   * ### **Slots:**
   *  - _default_ - The content to watch for mutations.
   */
  "wa-mutation-observer": DefineComponent<WaMutationObserverProps>;

  /**
   * Number inputs allow users to enter and edit numeric values with optional stepper buttons.
   * ---
   *
   *
   * ### **Events:**
   *  - **input** - Emitted when the control receives input.
   * - **change** - Emitted when an alteration to the control's value is committed by the user.
   * - **blur** - Emitted when the control loses focus.
   * - **focus** - Emitted when the control gains focus.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **focus(options: _FocusOptions_)** - Sets focus on the input.
   * - **blur()** - Removes focus from the input.
   * - **select()** - Selects all the text in the input.
   * - **stepUp()** - Increments the value by the step amount.
   * - **stepDown()** - Decrements the value by the step amount.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - **label** - The input's label. Alternatively, you can use the `label` attribute.
   * - **start** - An element, such as `<wa-icon>`, placed at the start of the input control.
   * - **end** - An element, such as `<wa-icon>`, placed at the end of the input control (before steppers).
   * - **increment-icon** - An icon to use in lieu of the default increment icon.
   * - **decrement-icon** - An icon to use in lieu of the default decrement icon.
   * - **hint** - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Parts:**
   *  - **label** - The label element.
   * - **form-control-label** - Alias for the label element.
   * - **hint** - The hint element.
   * - **base** - The wrapper containing the input and steppers.
   * - **input** - The internal `<input>` control.
   * - **start** - The container that wraps the `start` slot.
   * - **end** - The container that wraps the `end` slot.
   * - **stepper** - Both stepper buttons (for shared styling).
   * - **stepper-increment** - The increment (+) button on the end side.
   * - **stepper-decrement** - The decrement (-) button on the start side.
   */
  "wa-number-input": DefineComponent<WaNumberInputProps>;

  /**
   * Tags are used as labels to organize things or to indicate a selection.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-remove** - Emitted when the remove button is activated.
   *
   * ### **Slots:**
   *  - _default_ - The tag's content.
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **content** - The tag's content.
   * - **remove-button** - The tag's remove button, a `<wa-button>`.
   * - **remove-button__base** - The remove button's exported `base` part.
   */
  "wa-tag": DefineComponent<WaTagProps>;

  /**
   * Options define the selectable items within a select component.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The option's label.
   * - **start** - An element, such as `<wa-icon>`, placed before the label.
   * - **end** - An element, such as `<wa-icon>`, placed after the label.
   *
   * ### **CSS Parts:**
   *  - **checked-icon** - The checked icon, a `<wa-icon>` element.
   * - **label** - The option's label.
   * - **start** - The container that wraps the `start` slot.
   * - **end** - The container that wraps the `end` slot.
   */
  "wa-option": DefineComponent<WaOptionProps>;

  /**
   * Selects allow you to choose items from a menu of predefined options.
   * ---
   *
   *
   * ### **Events:**
   *  - **input** - Emitted when the control receives input.
   * - **change** - Emitted when the control's value changes.
   * - **focus** - Emitted when the control gains focus.
   * - **blur** - Emitted when the control loses focus.
   * - **wa-clear** - Emitted when the control's value is cleared.
   * - **wa-show** - Emitted when the select's menu opens.
   * - **wa-after-show** - Emitted after the select's menu opens and all animations are complete.
   * - **wa-hide** - Emitted when the select's menu closes.
   * - **wa-after-hide** - Emitted after the select's menu closes and all animations are complete.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **show()** - Shows the listbox.
   * - **hide()** - Hides the listbox.
   * - **focus(options: _FocusOptions_)** - Sets focus on the control.
   * - **blur()** - Removes focus from the control.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The listbox options. Must be `<wa-option>` elements. You can use `<wa-divider>` to group items visually.
   * - **label** - The input's label. Alternatively, you can use the `label` attribute.
   * - **start** - An element, such as `<wa-icon>`, placed at the start of the combobox.
   * - **end** - An element, such as `<wa-icon>`, placed at the end of the combobox.
   * - **clear-icon** - An icon to use in lieu of the default clear icon.
   * - **expand-icon** - The icon to show when the control is expanded and collapsed. Rotates on open and close.
   * - **hint** - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Properties:**
   *  - **--show-duration** - The duration of the show animation. _(default: 100ms)_
   * - **--hide-duration** - The duration of the hide animation. _(default: 100ms)_
   * - **--tag-max-size** - When using `multiple`, the max size of tags before their content is truncated. _(default: 10ch)_
   *
   * ### **CSS Parts:**
   *  - **form-control** - The form control that wraps the label, input, and hint.
   * - **form-control-label** - The label's wrapper.
   * - **form-control-input** - The select's wrapper.
   * - **hint** - The hint's wrapper.
   * - **combobox** - The container the wraps the start, end, value, clear icon, and expand button.
   * - **start** - The container that wraps the `start` slot.
   * - **end** - The container that wraps the `end` slot.
   * - **display-input** - The element that displays the selected option's label, an `<input>` element.
   * - **listbox** - The listbox container where options are slotted.
   * - **tags** - The container that houses option tags when `multiselect` is used.
   * - **tag** - The individual tags that represent each multiselect option.
   * - **tag__content** - The tag's content part.
   * - **tag__remove-button** - The tag's remove button.
   * - **tag__remove-button__base** - The tag's remove button base part.
   * - **clear-button** - The clear button.
   * - **expand-icon** - The container that wraps the expand icon.
   */
  "wa-select": DefineComponent<WaSelectProps>;

  /**
   * Popovers display contextual content and interactive elements in a floating panel.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-show** - Emitted when the popover begins to show. Canceling this event will stop the popover from showing.
   * - **wa-after-show** - Emitted after the popover has shown and all animations are complete.
   * - **wa-hide** - Emitted when the popover begins to hide. Canceling this event will stop the popover from hiding.
   * - **wa-after-hide** - Emitted after the popover has hidden and all animations are complete.
   *
   * ### **Methods:**
   *  - **show()** - Shows the popover.
   * - **hide()** - Hides the popover.
   *
   * ### **Slots:**
   *  - _default_ - The popover's content. Interactive elements such as buttons and links are supported.
   *
   * ### **CSS Properties:**
   *  - **--arrow-size** - The size of the tiny arrow that points to the popover (set to zero to remove). _(default: 0.375rem)_
   * - **--max-width** - The maximum width of the popover's body content. _(default: 25rem)_
   * - **--show-duration** - The speed of the show animation. _(default: 100ms)_
   * - **--hide-duration** - The speed of the hide animation. _(default: 100ms)_
   *
   * ### **CSS Parts:**
   *  - **dialog** - The native dialog element that contains the popover content.
   * - **body** - The popover's body where its content is rendered.
   * - **popup** - The internal `<wa-popup>` element that positions the popover.
   * - **popup__popup** - The popup's exported `popup` part. Use this to target the popover's popup container.
   * - **popup__arrow** - The popup's exported `arrow` part. Use this to target the popover's arrow.
   */
  "wa-popover": DefineComponent<WaPopoverProps>;

  /**
   * Progress bars are used to show the status of an ongoing operation.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - A label to show inside the progress indicator.
   *
   * ### **CSS Properties:**
   *  - **--track-height** - The color of the track. _(default: 1rem)_
   * - **--track-color** - The color of the track. _(default: var(--wa-color-neutral-fill-normal))_
   * - **--indicator-color** - The color of the indicator. _(default: var(--wa-color-brand-fill-loud))_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **indicator** - The progress bar's indicator.
   * - **label** - The progress bar's label.
   */
  "wa-progress-bar": DefineComponent<WaProgressBarProps>;

  /**
   * Progress rings are used to show the progress of a determinate operation in a circular fashion.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - A label to show inside the ring.
   *
   * ### **CSS Properties:**
   *  - **--size** - The diameter of the progress ring (cannot be a percentage). _(default: undefined)_
   * - **--track-width** - The width of the track. _(default: undefined)_
   * - **--track-color** - The color of the track. _(default: undefined)_
   * - **--indicator-width** - The width of the indicator. Defaults to the track width. _(default: undefined)_
   * - **--indicator-color** - The color of the indicator. _(default: undefined)_
   * - **--indicator-transition-duration** - The duration of the indicator's transition when the value changes. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **label** - The progress ring label.
   * - **track** - The progress ring's track.
   * - **indicator** - The progress ring's indicator.
   */
  "wa-progress-ring": DefineComponent<WaProgressRingProps>;

  /**
   * Generates a [QR code](https://www.qrcode.com/) and renders it using the [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API).
   * ---
   *
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-qr-code": DefineComponent<WaQrCodeProps>;

  /**
   * Radios allow the user to select a single option from a group.
   * ---
   *
   *
   * ### **Events:**
   *  - **blur** - Emitted when the control loses focus.
   * - **focus** - Emitted when the control gains focus.
   *
   * ### **Methods:**
   *  - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The radio's label.
   *
   * ### **CSS Properties:**
   *  - **--checked-icon-color** - The color of the checked icon. _(default: undefined)_
   * - **--checked-icon-scale** - The size of the checked icon relative to the radio. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **control** - The circular container that wraps the radio's checked state.
   * - **checked-icon** - The checked icon.
   * - **label** - The container that wraps the radio's label.
   */
  "wa-radio": DefineComponent<WaRadioProps>;

  /**
   * Radio groups are used to group multiple [radios](/docs/components/radio) so they function as a single form control.
   * ---
   *
   *
   * ### **Events:**
   *  - **input** - Emitted when the radio group receives user input.
   * - **change** - Emitted when the radio group's selected value changes.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **focus(options: _FocusOptions_)** - Sets focus on the radio group.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The default slot where `<wa-radio>` elements are placed.
   * - **label** - The radio group's label. Required for proper accessibility. Alternatively, you can use the `label` attribute.
   * - **hint** - Text that describes how to use the radio group. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Parts:**
   *  - **form-control** - The form control that wraps the label, input, and hint.
   * - **form-control-label** - The label's wrapper.
   * - **form-control-input** - The input's wrapper.
   * - **radios** - The wrapper than surrounds radio items, styled as a flex container by default.
   * - **hint** - The hint's wrapper.
   */
  "wa-radio-group": DefineComponent<WaRadioGroupProps>;

  /**
   * Ratings give users a way to quickly view and provide feedback.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when the rating's value changes.
   * - **wa-hover** - Emitted when the user hovers over a value. The `phase` property indicates when hovering starts, moves to a new value, or ends. The `value` property tells what the rating's value would be if the user were to commit to the hovered value.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **CSS Properties:**
   *  - **--symbol-color** - The inactive color for symbols. _(default: undefined)_
   * - **--symbol-color-active** - The active color for symbols. _(default: undefined)_
   * - **--symbol-spacing** - The spacing to use around symbols. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-rating": DefineComponent<WaRatingProps>;

  /**
   * Outputs a localized time phrase relative to the current date and time.
   * ---
   *
   */
  "wa-relative-time": DefineComponent<WaRelativeTimeProps>;

  /**
   * Scrollers create an accessible container while providing visual cues that help users identify and navigate
   * through content that scrolls.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The content to show inside the scroller.
   *
   * ### **CSS Properties:**
   *  - **--shadow-color** - The base color of the shadow. _(default: var(--wa-color-surface-default))_
   * - **--shadow-size** - The size of the shadow. _(default: 2rem)_
   *
   * ### **CSS Parts:**
   *  - **content** - The container that wraps the slotted content.
   */
  "wa-scroller": DefineComponent<WaScrollerProps>;

  /**
   * The Resize Observer component offers a thin, declarative interface to the [`ResizeObserver API`](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver).
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-resize** - Emitted when the element is resized.
   *
   * ### **Slots:**
   *  - _default_ - One or more elements to watch for resizing.
   */
  "wa-resize-observer": DefineComponent<WaResizeObserverProps>;

  /**
   * Skeletons are used to provide a visual representation of where content will eventually be drawn.
   * ---
   *
   *
   * ### **CSS Properties:**
   *  - **--color** - The color of the skeleton. _(default: undefined)_
   * - **--sheen-color** - The sheen color when the skeleton is in its loading state. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **indicator** - The skeleton's indicator which is responsible for its color and animation.
   */
  "wa-skeleton": DefineComponent<WaSkeletonProps>;

  /**
   * Ranges allow the user to select a single value within a given range using a slider.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when an alteration to the control's value is committed by the user.
   * - **blur** - Emitted when the control loses focus.
   * - **focus** - Emitted when the control gains focus.
   * - **input** - Emitted when the control receives input.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **focus()** - Sets focus to the slider.
   * - **blur()** - Removes focus from the slider.
   * - **stepDown()** - Decreases the slider's value by `step`. This is a programmatic change, so `input` and `change` events will not be
   * emitted when this is called.
   * - **stepUp()** - Increases the slider's value by `step`. This is a programmatic change, so `input` and `change` events will not be
   * emitted when this is called.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - **label** - The slider label. Alternatively, you can use the `label` attribute.
   * - **hint** - Text that describes how to use the input. Alternatively, you can use the `hint` attribute. instead.
   * - **reference** - One or more reference labels to show visually below the slider.
   *
   * ### **CSS Properties:**
   *  - **--track-size** - The height or width of the slider's track. _(default: 0.75em)_
   * - **--marker-width** - The width of each individual marker. _(default: 0.1875em)_
   * - **--marker-height** - The height of each individual marker. _(default: 0.1875em)_
   * - **--thumb-width** - The width of the thumb. _(default: 1.25em)_
   * - **--thumb-height** - The height of the thumb. _(default: 1.25em)_
   *
   * ### **CSS Parts:**
   *  - **label** - The element that contains the sliders's label.
   * - **hint** - The element that contains the slider's description.
   * - **slider** - The focusable element with `role="slider"`. Contains the track and reference slot.
   * - **track** - The slider's track.
   * - **indicator** - The colored indicator that shows from the start of the slider to the current value.
   * - **markers** - The container that holds all the markers when `with-markers` is used.
   * - **marker** - The individual markers that are shown when `with-markers` is used.
   * - **references** - The container that holds references that get slotted in.
   * - **thumb** - The slider's thumb.
   * - **thumb-min** - The min value thumb in a range slider.
   * - **thumb-max** - The max value thumb in a range slider.
   * - **tooltip** - The tooltip, a `<wa-tooltip>` element.
   * - **tooltip__tooltip** - The tooltip's `tooltip` part.
   * - **tooltip__content** - The tooltip's `content` part.
   * - **tooltip__arrow** - The tooltip's `arrow` part.
   */
  "wa-slider": DefineComponent<WaSliderProps>;

  /**
   * Switches allow the user to toggle an option on or off.
   * ---
   *
   *
   * ### **Events:**
   *  - **change** - Emitted when the control's checked state changes.
   * - **input** - Emitted when the control receives input.
   * - **blur** - Emitted when the control loses focus.
   * - **focus** - Emitted when the control gains focus.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **click()** - Simulates a click on the switch.
   * - **focus(options: _FocusOptions_)** - Sets focus on the switch.
   * - **blur()** - Removes focus from the switch.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - _default_ - The switch's label.
   * - **hint** - Text that describes how to use the switch. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Properties:**
   *  - **--width** - The width of the switch. _(default: undefined)_
   * - **--height** - The height of the switch. _(default: undefined)_
   * - **--thumb-size** - The size of the thumb. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **control** - The control that houses the switch's thumb.
   * - **thumb** - The switch's thumb.
   * - **label** - The switch's label.
   * - **hint** - The hint's wrapper.
   */
  "wa-switch": DefineComponent<WaSwitchProps>;

  /**
   * Tabs are used inside [tab groups](/docs/components/tab-group) to represent and activate [tab panels](/docs/components/tab-panel).
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The tab's label.
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-tab": DefineComponent<WaTabProps>;

  /**
   * Split panels display two adjacent panels, allowing the user to reposition them.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-reposition** - Emitted when the divider's position changes.
   *
   * ### **Slots:**
   *  - **start** - Content to place in the start panel.
   * - **end** - Content to place in the end panel.
   * - **divider** - The divider. Useful for slotting in a custom icon that renders as a handle.
   *
   * ### **CSS Properties:**
   *  - **--divider-width** - The width of the visible divider. _(default: 4px)_
   * - **--divider-hit-area** - The invisible region around the divider where dragging can occur. This is usually wider than the divider to facilitate easier dragging. _(default: 12px)_
   * - **--min** - The minimum allowed size of the primary panel. _(default: 0)_
   * - **--max** - The maximum allowed size of the primary panel. _(default: 100%)_
   *
   * ### **CSS Parts:**
   *  - **start** - The start panel.
   * - **end** - The end panel.
   * - **panel** - Targets both the start and end panels.
   * - **divider** - The divider that separates the start and end panels.
   */
  "wa-split-panel": DefineComponent<WaSplitPanelProps>;

  /**
   * Tab panels are used inside [tab groups](/docs/components/tab-group) to display tabbed content.
   * ---
   *
   *
   * ### **Slots:**
   *  - _default_ - The tab panel's content.
   *
   * ### **CSS Properties:**
   *  - **--padding** - The tab panel's padding. _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-tab-panel": DefineComponent<WaTabPanelProps>;

  /**
   * Tab groups organize content into a container that shows one section at a time.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-tab-show** - Emitted when a tab is shown.
   * - **wa-tab-hide** - Emitted when a tab is hidden.
   *
   * ### **Slots:**
   *  - _default_ - Used for grouping tab panels in the tab group. Must be `<wa-tab-panel>` elements.
   * - **nav** - Used for grouping tabs in the tab group. Must be `<wa-tab>` elements. Note that `<wa-tab>` will set this slot on itself automatically.
   *
   * ### **CSS Properties:**
   *  - **--indicator-color** - The color of the active tab indicator. _(default: undefined)_
   * - **--track-color** - The color of the indicator's track (the line that separates tabs from panels). _(default: undefined)_
   * - **--track-width** - The width of the indicator's track (the line that separates tabs from panels). _(default: undefined)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **nav** - The tab group's navigation container where tabs are slotted in.
   * - **tabs** - The container that wraps the tabs.
   * - **body** - The tab group's body where tab panels are slotted in.
   * - **scroll-button** - The previous/next scroll buttons that show when tabs are scrollable, a `<wa-button>`.
   * - **scroll-button-start** - The starting scroll button.
   * - **scroll-button-end** - The ending scroll button.
   * - **scroll-button__base** - The scroll button's exported `base` part.
   */
  "wa-tab-group": DefineComponent<WaTabGroupProps>;

  /**
   * Textareas collect data from the user and allow multiple lines of text.
   * ---
   *
   *
   * ### **Events:**
   *  - **blur** - Emitted when the control loses focus.
   * - **change** - Emitted when an alteration to the control's value is committed by the user.
   * - **focus** - Emitted when the control gains focus.
   * - **input** - Emitted when the control receives input.
   * - **wa-invalid** - Emitted when the form control has been checked for validity and its constraints aren't satisfied.
   *
   * ### **Methods:**
   *  - **focus(options: _FocusOptions_)** - Sets focus on the textarea.
   * - **blur()** - Removes focus from the textarea.
   * - **select()** - Selects all the text in the textarea.
   * - **scrollPosition(position: _{ top?: number; left?: number }_): _{ top: number; left: number } | undefined_** - Gets or sets the textarea's scroll position.
   * - **setSelectionRange(selectionStart: _number_, selectionEnd: _number_, selectionDirection: _'forward' | 'backward' | 'none'_)** - Sets the start and end positions of the text selection (0-based).
   * - **setRangeText(replacement: _string_, start: _number_, end: _number_, selectMode: _'select' | 'start' | 'end' | 'preserve'_)** - Replaces a range of text with a new string.
   * - **setCustomValidity(message: _string_)** - Do not use this when creating a "Validator". This is intended for end users of components.
   * We track manually defined custom errors so we don't clear them on accident in our validators.
   * - **formStateRestoreCallback(state: _string | File | FormData | null_, reason: _'autocomplete' | 'restore'_)** - Called when the browser is trying to restore element’s state to state in which case reason is "restore", or when
   * the browser is trying to fulfill autofill on behalf of user in which case reason is "autocomplete". In the case of
   * "restore", state is a string, File, or FormData object previously set as the second argument to setFormValue.
   * - **resetValidity()** - Reset validity is a way of removing manual custom errors and native validation.
   *
   * ### **Slots:**
   *  - **label** - The textarea's label. Alternatively, you can use the `label` attribute.
   * - **hint** - Text that describes how to use the input. Alternatively, you can use the `hint` attribute.
   *
   * ### **CSS Parts:**
   *  - **label** - The label
   * - **form-control-input** - The input's wrapper.
   * - **hint** - The hint's wrapper.
   * - **textarea** - The internal `<textarea>` control.
   * - **base** - The wrapper around the `<textarea>` control.
   * - **count** - The character count element, rendered when the `with-count` attribute is present.
   */
  "wa-textarea": DefineComponent<WaTextareaProps>;

  /**
   * Trees allow you to display a hierarchical list of selectable [tree items](/docs/components/tree-item). Items with children can be expanded and collapsed as desired by the user.
   * ---
   *
   *
   * ### **Events:**
   *  - **wa-selection-change** - Emitted when a tree item is selected or deselected.
   *
   * ### **Slots:**
   *  - _default_ - The default slot.
   * - **expand-icon** - The icon to show when the tree item is expanded. Works best with `<wa-icon>`.
   * - **collapse-icon** - The icon to show when the tree item is collapsed. Works best with `<wa-icon>`.
   *
   * ### **CSS Properties:**
   *  - **--indent-size** - The size of the indentation for nested items. _(default: var(--wa-space-m))_
   * - **--indent-guide-color** - The color of the indentation line. _(default: var(--wa-color-surface-border))_
   * - **--indent-guide-offset** - The amount of vertical spacing to leave between the top and bottom of the indentation line's starting position. _(default: 0)_
   * - **--indent-guide-style** - The style of the indentation line, e.g. solid, dotted, dashed. _(default: solid)_
   * - **--indent-guide-width** - The width of the indentation line. _(default: 0)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   */
  "wa-tree": DefineComponent<WaTreeProps>;

  /**
   * Zoomable frames render iframe content with zoom and interaction controls.
   * ---
   *
   *
   * ### **Events:**
   *  - **load** - Emitted when the internal iframe when it finishes loading.
   * - **error** - Emitted from the internal iframe when it fails to load.
   *
   * ### **Methods:**
   *  - **zoomIn()** - Zooms in to the next available zoom level.
   * - **zoomOut()** - Zooms out to the previous available zoom level.
   *
   * ### **Slots:**
   *  - **zoom-in-icon** - The slot that contains the zoom in icon.
   * - **zoom-out-icon** - The slot that contains the zoom out icon.
   *
   * ### **CSS Parts:**
   *  - **iframe** - The internal `<iframe>` element.
   * - **controls** - The container that surrounds zoom control buttons.
   * - **zoom-in-button** - The zoom in button.
   * - **zoom-out-button** - The zoom out button.
   */
  "wa-zoomable-frame": DefineComponent<WaZoomableFrameProps>;

  /**
   * Renders markdown content in plain ol' HTML.
   * ---
   *
   *
   * ### **Methods:**
   *  - **getMarked(): _Marked_** - Returns the shared Marked instance used by all `<wa-markdown>` components.
   * - **updateAll(): _void_** - Re-renders all connected `<wa-markdown>` instances. Call this after changing the Marked configuration.
   * - **renderMarkdown()** - Reads the script content, normalizes whitespace, parses markdown, and injects the result.
   */
  "wa-markdown": DefineComponent<WaMarkdownProps>;

  /**
   * Pages offer an easy way to scaffold entire page layouts using minimal markup.
   * ---
   *
   *
   * ### **Methods:**
   *  - **visiblePixelsInViewport(element: _HTMLElement | null_)** - https://stackoverflow.com/a/26831113
   * This prevents awkward gaps when scrolling the page and the aside / menu dont "fill" the gaps.
   * - **showNavigation()** - Shows the mobile navigation drawer
   * - **hideNavigation()** - Hides the mobile navigation drawer
   * - **toggleNavigation()** - Toggles the mobile navigation drawer
   *
   * ### **Slots:**
   *  - _default_ - The page's main content.
   * - **banner** - The banner that gets display above the header. The banner will not be shown if no content is provided.
   * - **header** - The header to display at the top of the page. If a banner is present, the header will appear below the banner. The header will not be shown if there is no content.
   * - **subheader** - A subheader to display below the `header`. This is a good place to put things like breadcrumbs.
   * - **menu** - The left side of the page. If you slot an element in here, you will override the default `navigation` slot and will be handling navigation on your own. This also will not disable the fallback behavior of the navigation button. This section "sticks" to the top as the page scrolls.
   * - **navigation-header** - The header for a navigation area. On mobile this will be the header for `<wa-drawer>`.
   * - **navigation** - The main content to display in the navigation area. This is displayed on the left side of the page, if `menu` is not used. This section "sticks" to the top as the page scrolls.
   * - **navigation-footer** - The footer for a navigation area. On mobile this will be the footer for `<wa-drawer>`.
   * - **navigation-toggle** - Use this slot to slot in your own button + icon for toggling the navigation drawer. By default it is a `<wa-button>` + a 3 bars `<wa-icon>`
   * - **navigation-toggle-icon** - Use this to slot in your own icon for toggling the navigation drawer. By default it is 3 bars `<wa-icon>`.
   * - **main-header** - Header to display inline above the main content.
   * - **main-footer** - Footer to display inline below the main content.
   * - **aside** - Content to be shown on the right side of the page. Typically contains a table of contents, ads, etc. This section "sticks" to the top as the page scrolls.
   * - **skip-to-content** - The "skip to content" slot. You can override this If you would like to override the `Skip to content` button and add additional "Skip to X", they can be inserted here.
   * - **footer** - The content to display in the footer. This is always displayed underneath the viewport so will always make the page "scrollable".
   *
   * ### **CSS Properties:**
   *  - **--menu-width** - The width of the page's "menu" section. _(default: auto)_
   * - **--main-width** - The width of the page's "main" section. _(default: 1fr)_
   * - **--aside-width** - The wide of the page's "aside" section. _(default: auto)_
   * - **--banner-height** - The height of the banner. This gets calculated when the page initializes. If the height is known, you can set it here to prevent shifting when the page loads. _(default: 0px)_
   * - **--header-height** - The height of the header. This gets calculated when the page initializes. If the height is known, you can set it here to prevent shifting when the page loads. _(default: 0px)_
   * - **--subheader-height** - The height of the subheader. This gets calculated when the page initializes. If the height is known, you can set it here to prevent shifting when the page loads. _(default: 0px)_
   *
   * ### **CSS Parts:**
   *  - **base** - The component's base wrapper.
   * - **banner** - The banner to show above header.
   * - **header** - The header, usually for top level navigation / branding.
   * - **subheader** - Shown below the header, usually intended for things like breadcrumbs and other page level navigation.
   * - **body** - The wrapper around menu, main, and aside.
   * - **menu** - The left hand side of the page. Generally intended for navigation.
   * - **navigation** - The `<nav>` that wraps the navigation slots on desktop viewports.
   * - **navigation-header** - The header for a navigation area. On mobile this will be the header for `<wa-drawer>`.
   * - **navigation-footer** - The footer for a navigation area. On mobile this will be the footer for `<wa-drawer>`.
   * - **navigation-toggle** - The default `<wa-button>` that will toggle the `<wa-drawer>` for mobile viewports.
   * - **navigation-toggle-icon** - The default `<wa-icon>` displayed inside of the navigation-toggle button.
   * - **main-header** - The header above main content.
   * - **main-content** - The main content.
   * - **main-footer** - The footer below main content.
   * - **aside** - The right hand side of the page. Used for things like table of contents, ads, etc.
   * - **skip-links** - Wrapper around skip-link
   * - **skip-link** - The "skip to main content" link
   * - **footer** - The footer of the page. This is always below the initial viewport size.
   * - **dialog-wrapper** - A wrapper around elements such as dialogs or other modal-like elements.
   */
  "wa-page": DefineComponent<WaPageProps>;
};

declare module "vue" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface GlobalComponents extends CustomElements {}
}

declare global {
  namespace JSX {
    // eslint-disable-next-line @typescript-eslint/no-empty-interface
    interface IntrinsicElements extends CustomElements {}
  }
}
