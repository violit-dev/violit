import json
import urllib.request
from typing import Any, cast

import violit as vl


MODEL = "gpt-4o-mini"

app = vl.App(title="Simple OpenAI Chat", theme="violit_light_jewel", container_width="760px")
messages = app.state([
    {"role": "assistant", "content": "Hello. Ask ChatGPT anything."}
], key="demo_openai_messages")
api_key = app.state("", key="demo_openai_api_key")
mode = app.state("streaming", key="demo_openai_mode")


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
        "stream": mode.value == "streaming",
    }

    if mode.value == "streaming":
        return _reply_streaming(payload, key)
    return _reply_non_streaming(payload, key)


reactivity = cast(Any, app.reactivity)

app.title("Simple OpenAI Chat")
app.caption("A very small Violit chat example.")
app.text_input("OPENAI_API_KEY", value=api_key.value, key="demo_openai_api_key", type="password")
app.selectbox("Mode", ["streaming", "non-streaming"], value=mode.value, key="demo_openai_mode")


@reactivity
def render_chat():
    app.chat_messages(messages, height="60vh")


render_chat()
app.chat_input(
    "Ask ChatGPT",
    messages=messages,
    on_submit=reply,
    pinned=False,
    auto_scroll="bottom",
    stream_speed="smooth",
)


app.run()