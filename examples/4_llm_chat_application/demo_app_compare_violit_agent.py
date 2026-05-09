import time
from typing import Any, Iterable, cast

from _local_violit_bootstrap import bootstrap_local_violit

bootstrap_local_violit()

import violit as vl


def fake_agent_stream(prompt: str) -> Iterable[str]:
    steps = [
        "Understanding the request... ",
        "Collecting relevant context... ",
        "Drafting the answer... ",
        f"Done. You asked: {prompt}",
    ]
    for step in steps:
        time.sleep(0.35)
        yield step


def seed_messages() -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": "Hello. This is the Violit primitive version of the same small agent-chat example.",
            "meta": {"label": "Ready", "state": "complete"},
        }
    ]



def make_message(role: str, content: str, *, label: str | None = None, state: str | None = None) -> dict[str, Any]:
    message: dict[str, Any] = {"role": role, "content": content}
    if label is not None and state is not None:
        message["meta"] = {"label": label, "state": state}
    return message


app = vl.App(title="Compare: Violit Agent Chat", container_width="820px")
messages = app.state(seed_messages(), key="compare_violit_agent_messages")
reactivity = cast(Any, app.reactivity)


def reset_chat() -> None:
    messages.set(seed_messages())


def append_message(message: dict[str, Any]) -> None:
    messages.set([*messages.value, message])


def replace_last_message(message: dict[str, Any]) -> None:
    items = list(messages.value)
    if not items:
        messages.set([message])
        return
    items[-1] = message
    messages.set(items)


def run_agent(prompt: str) -> None:
    append_message(make_message("user", prompt))
    append_message(make_message("assistant", "", label="Running agent...", state="running"))

    chunks: list[str] = []
    try:
        for chunk in fake_agent_stream(prompt):
            chunks.append(chunk)
            replace_last_message(make_message("assistant", "".join(chunks), label="Running agent...", state="running"))

        replace_last_message(make_message("assistant", "".join(chunks), label="Done", state="complete"))
    except Exception as exc:
        replace_last_message(make_message("assistant", f"Error: {exc}", label="Failed", state="error"))


def submit_prompt(prompt: str) -> None:
    app.background(lambda prompt=prompt: run_agent(prompt)).start()


app.title("Violit vs Streamlit: Violit Agent Chat")
app.caption("Same fake-agent behavior as the Streamlit example, but rendered with Violit primitive chat_message, status, and chat_input APIs.")
app.button("Reset chat", on_click=reset_chat, variant="neutral")


@reactivity
def render_chat() -> None:
    with app.chat_thread(height="62vh", border=True, cls="rounded-[24px] bg-white/90 p-4"):
        for message in messages.value:
            with app.chat_message(message["role"]):
                meta = message.get("meta")
                if meta:
                    with app.status(meta["label"], state=meta["state"], expanded=False):
                        pass
                if message.get("content"):
                    app.markdown(message["content"])


cast(Any, render_chat)()
app.chat_input("Ask the agent", key="compare_violit_agent_prompt", on_submit=submit_prompt)
app.run()