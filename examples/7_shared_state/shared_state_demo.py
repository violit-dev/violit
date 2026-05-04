from __future__ import annotations

from datetime import datetime

import violit as vl


app = vl.App(title="Violit shared_state Quick Demo", theme="violit_light_jewel")

messages = app.shared_state([], key="messages", namespace="demo:lobby")


def post_message(name: str, text: str) -> None:
    author = name.strip() or "guest"
    body = text.strip()
    if not body:
        return

    next_items = list(messages.value)
    next_items.append(
        {
            "author": author,
            "text": body,
            "created_at": datetime.now().strftime("%H:%M:%S"),
        }
    )
    messages.set(next_items[-20:])
    message.set("")


app.title("shared_state Quick Demo")
app.caption("Open this app in two browsers or tabs. Messages are shared through app.shared_state(...).")

name = app.text_input("Name", value="guest", key="quick_demo_name")
message = app.text_input(
    "Message",
    key="quick_demo_message",
    placeholder="Type a short message",
    on_submit=lambda value: post_message(name.value, value),
)

app.button(
    "Send",
    on_click=lambda: post_message(name.value, message.value),
    cls="rounded-2xl font-bold",
)
app.button(
    "Clear shared log",
    on_click=lambda: messages.set([]),
    variant="neutral",
)

app.For(
    lambda: messages.value,
    render=lambda item, _: app.text(f"[{item['created_at']}] {item['author']}: {item['text']}"),
    empty=lambda: app.caption("No shared messages yet. Send the first one."),
)


app.run()