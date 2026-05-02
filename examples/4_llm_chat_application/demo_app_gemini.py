import json
import urllib.parse
import urllib.request
from typing import Any, cast

import violit as vl


MODEL = "gemini-2.5-flash"

app = vl.App(title="Simple Gemini Chat", theme="violit_light_jewel", container_width="760px")
messages = app.state([
    {"role": "assistant", "content": "Hello. Ask Gemini anything."}
], key="demo_gemini_messages")
api_key = app.state("", key="demo_gemini_api_key")
mode = app.state("streaming", key="demo_gemini_mode")


def _post_json(url: str, payload: dict, *, accept_sse: bool = False):
    return urllib.request.urlopen(
        urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Accept": "text/event-stream"} if accept_sse else {}),
            },
            method="POST",
        ),
        timeout=180,
    )


def _reply_non_streaming(payload: dict, model: str, api_key_value: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key_value}"
    with _post_json(url, payload, accept_sse=False) as response:
        data = json.loads(response.read().decode("utf-8"))

    if data.get("error"):
        raise RuntimeError(str(data["error"]))

    parts = []
    for candidate in data.get("candidates") or []:
        for part in ((candidate.get("content") or {}).get("parts") or []):
            text = part.get("text") if isinstance(part, dict) else ""
            if text:
                parts.append(text)

    reply_text = "".join(parts).strip()
    if not reply_text:
        raise RuntimeError("Gemini returned an empty response.")
    return reply_text


def _reply_streaming(payload: dict, model: str, api_key_value: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key_value}"

    def stream():
        with _post_json(url, payload, accept_sse=True) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                data_line = line[5:].strip()
                if not data_line or data_line == "[DONE]":
                    continue

                event = json.loads(data_line)
                if event.get("error"):
                    raise RuntimeError(str(event["error"]))

                for candidate in event.get("candidates") or []:
                    for part in ((candidate.get("content") or {}).get("parts") or []):
                        text = part.get("text") if isinstance(part, dict) else ""
                        if text:
                            yield text

    return stream()


def reply(_prompt: str):
    key = api_key.value.strip()
    if not key:
        raise RuntimeError("Paste your Gemini API key above.")

    payload = {
        "contents": [
            {
                "role": "model" if item.get("role") == "assistant" else "user",
                "parts": [{"text": item.get("content", "")}],
            }
            for item in messages.value
            if item.get("content")
        ],
        "generationConfig": {"temperature": 0.4},
    }

    model = urllib.parse.quote(MODEL, safe="")
    api_key_value = urllib.parse.quote(key, safe="")
    if mode.value == "streaming":
        return _reply_streaming(payload, model, api_key_value)
    return _reply_non_streaming(payload, model, api_key_value)


reactivity = cast(Any, app.reactivity)

app.title("Simple Gemini Chat")
app.caption("A very small Violit chat example.")
app.text_input("GEMINI_API_KEY", value=api_key.value, key="demo_gemini_api_key", type="password")
app.selectbox("Mode", ["streaming", "non-streaming"], value=mode.value, key="demo_gemini_mode")


@reactivity
def render_chat():
    app.chat_messages(messages, height="60vh")


render_chat()
app.chat_input(
    "Ask Gemini",
    messages=messages,
    on_submit=reply,
    pinned=False,
    auto_scroll="bottom",
    stream_speed="smooth",
)


app.run()