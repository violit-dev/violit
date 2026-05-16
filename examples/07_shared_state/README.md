# 7. Shared State (Multi-user Sync)

This example demonstrates how to build real-time, multi-user collaborative experiences using Violit's `shared_state`.

In Violit, state management is scoped. While `view_state` or `session_state` are private to a single browser tab, `shared_state` allows you to create "rooms" or "boards" where data is synchronized across different users and devices in real-time.

## File

- `shared_state_demo.py`: A simple real-time chat/log board using namespaced shared state.

## Run

To see the synchronization in action:
1. Open a terminal and run the app.
2. Open the URL in **two different browser windows** (or two different devices).
3. Type a message in one window and see it appear instantly in the other.

```bash
cd examples/7_shared_state
python shared_state_demo.py
```

## Conceptual Overview

Violit provides four major state scopes:
1. **View State**: Transient, stays within a single function/component.
2. **Session State**: Tied to a specific browser session (reloading the page preserves it).
3. **App State**: Global singleton for the entire server (useful for global counters/configs).
4. **Shared State**: **Namespaced** global state. It allows different groups of users to share data by using the same `namespace` string (e.g., `room:123`).

## What This Example Shows

- **Real-time Sync**: Using `app.shared_state` to broadcast updates to all connected clients.
- **Namespacing**: Organizing shared data so different "rooms" don't collide.
- **Reactive Rendering**: Using `app.For` to efficiently render list updates without refreshing the whole page.
- **Smart-Updates**: Violit's runtime automatically preserves focus for text inputs even when the surrounding UI updates from another user's message.

## Read The Code In This Order

### 1. Defining Shared State

```python
# Messages are shared across all users using the "demo:lobby" namespace.
messages = app.shared_state([], key="messages", namespace="demo:lobby")
```
By providing a `namespace`, you ensure that only users in the "lobby" see these messages. You could easily create separate chat rooms by changing this string dynamically.

### 2. Updating the State

```python
def post_message(name, text):
    # ... validation logic ...
    next_items = list(messages.value)
    next_items.append({ ... })
    
    # Update the shared state. This broadcasts to EVERYONE in this namespace.
    messages.set(next_items[-20:])
    
    # Clear only the local input box
    message.set("")
```
When `messages.set()` is called, Violit handles the heavy lifting of notifying all connected browser instances.

### 3. Reactive List Rendering

```python
app.For(
    lambda: messages.value,
    render=lambda item, _: app.text(f"[{item['created_at']}] {item['author']}: {item['text']}"),
    empty=lambda: app.caption("No shared messages yet."),
)
```
`app.For` is the recommended way to render lists. It only updates the parts of the DOM that changed, making the multi-user experience smooth and fast.

## Security & Performance Note

`shared_state` in Violit is designed for collaborative UX:
- **TTL**: Shared namespaces are automatically cleared after 6 hours of inactivity.
- **Limits**: Each shared value is capped at 256KB to prevent memory exhaustion (DoS).
- **Sanitization**: Violit automatically sanitizes markdown content to prevent XSS in shared environments.
