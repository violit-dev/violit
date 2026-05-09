import json
import urllib.request
from typing import Any, cast

from _local_violit_bootstrap import bootstrap_local_violit

bootstrap_local_violit()

import violit as vl


MODEL = "gpt-4o-mini"

app = vl.App(title="Simple OpenAI Chat", theme="violit_light_jewel", container_width="760px")
messages = app.state([
    {"role": "assistant", "content": "Hello. Ask ChatGPT anything."}
], key="demo_openai_messages")
api_key = app.state("", key="demo_openai_api_key")
busy = app.state(False, key="demo_openai_busy")


def _reply_non_streaming(payload: dict, key: str) -> str:
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))

    text = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
    if not text:
        raise RuntimeError("OpenAI returned an empty response.")
    return text


def _reply_streaming(payload: dict, key: str):
    def stream():
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                data_line = line[5:].strip()
                if not data_line or data_line == "[DONE]":
                    continue

                event = json.loads(data_line)
                choice = (event.get("choices") or [{}])[0]
                delta = choice.get("delta") or {}
                text = delta.get("content")
                if isinstance(text, str) and text:
                    yield text

    return stream()


def reply(_prompt: str):
    key = api_key.value.strip()
    if not key:
        raise RuntimeError("Paste your OpenAI API key above.")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": item.get("role", "user"), "content": item.get("content", "")}
            for item in messages.value
            if item.get("content")
        ],
        "temperature": 0.4,
        "stream": True,
    }

    return _reply_streaming(payload, key)


def append_message(message: dict[str, Any]) -> None:
    messages.set([*messages.value, dict(message)])


def replace_last_message(message: dict[str, Any]) -> None:
    items = [dict(item) for item in messages.value]
    if not items:
        messages.set([dict(message)])
        return
    items[-1] = dict(message)
    messages.set(items)


def run_reply(prompt: str) -> None:
    result = reply(prompt)
    if isinstance(result, str):
        replace_last_message({"role": "assistant", "content": result})
        return

    chunks: list[str] = []
    for chunk in cast(Any, result):
        text = chunk if isinstance(chunk, str) else str(chunk)
        if not text:
            continue
        chunks.append(text)
        replace_last_message({"role": "assistant", "content": "".join(chunks)})

    final_text = "".join(chunks).strip()
    if not final_text:
        raise RuntimeError("OpenAI returned an empty response.")
    replace_last_message({"role": "assistant", "content": final_text})


def fail_reply(exc: Exception) -> None:
    replace_last_message({
        "role": "assistant",
        "content": f"Error:\n\n```text\n{exc}\n```",
    })
    busy.set(False)


def submit_prompt(prompt: str) -> None:
    cleaned = str(prompt or "").strip()
    if not cleaned or busy.value:
        return

    append_message({"role": "user", "content": cleaned})
    append_message({"role": "assistant", "content": ""})
    busy.set(True)

    app.background(
        lambda prompt=cleaned: run_reply(prompt),
        on_complete=lambda: busy.set(False),
        on_error=fail_reply,
    ).start()


reactivity = cast(Any, app.reactivity)

app.title("Simple OpenAI Chat")
app.caption("A small text-only Violit chat example.")
app.text_input("OPENAI_API_KEY", value=api_key.value, key="demo_openai_api_key", type="password")


@reactivity
def render_chat():
    with app.chat_thread(height="60vh"):
        for message in messages.value:
            with app.chat_message(message.get("role", "assistant")):
                app.render_chat_message_body(message)


render_chat()
app.chat_input(
    "Ask ChatGPT",
    on_submit=submit_prompt,
    disabled=bool(busy.value),
)


app.run()