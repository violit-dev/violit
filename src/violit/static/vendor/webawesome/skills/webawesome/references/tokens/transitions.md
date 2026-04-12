# Transitions

**Full documentation:** https://webawesome.com/docs/tokens/transitions

Transitions can make interactions more lively and emphasize the relationship between a user's action and its outcome.

### Duration

Web Awesome uses different transition durations to make it easy to track a component's state while minimizing sluggish or distracting movement.

Properties that change between frequent, incidental states, such as hover and focus, generally use faster transitions than properties that change between states that are more intentional and impactful, like checked or open.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-transition-slow\` | \`300ms\` |
| \`--wa-transition-normal\` | \`150ms\` |
| \`--wa-transition-fast\` | \`75ms\` |

### Easing

Easing controls the standard `transition-timing-function` used for transitions throughout Web Awesome.

| Custom Property | Default Value |
| --- | --- |
| \`--wa-transition-easing\` | \`ease\` |