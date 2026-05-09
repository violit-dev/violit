import json
import urllib.parse
import urllib.request
from typing import Any, cast

from _local_violit_bootstrap import bootstrap_local_violit

bootstrap_local_violit()

import violit as vl


MODEL = "gemini-2.5-flash"

app = vl.App(title="Simple Gemini Chat", theme="violit_light_jewel", container_width="760px")
messages = app.state([
    {"role": "assistant", "content": "Hello. Ask Gemini anything."}
], key="demo_gemini_messages")
api_key = app.state("", key="demo_gemini_api_key")
busy = app.state(False, key="demo_gemini_busy")


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


def _extract_gemini_event_text(event: dict[str, Any]) -> str:
    parts: list[str] = []
    for candidate in event.get("candidates") or []:
        for part in ((candidate.get("content") or {}).get("parts") or []):
            text = part.get("text") if isinstance(part, dict) else ""
            if text:
                parts.append(text)
    return "".join(parts)


def _next_gemini_stream_delta(emitted_text: str, event_text: str) -> tuple[str, str]:
    if not event_text:
        return "", emitted_text
    if not emitted_text:
        return event_text, event_text
    if event_text == emitted_text or event_text in emitted_text:
        return "", emitted_text
    if event_text.startswith(emitted_text):
        delta = event_text[len(emitted_text):]
        return delta, emitted_text + delta

    overlap = 0
    max_overlap = min(len(emitted_text), len(event_text))
    for size in range(max_overlap, 0, -1):
        if emitted_text.endswith(event_text[:size]):
            overlap = size
            break

    delta = event_text[overlap:]
    return delta, emitted_text + delta


def _reply_streaming(payload: dict, model: str, api_key_value: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key_value}"

    def stream():
        emitted_text = ""
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
                text = _extract_gemini_event_text(event)
                if not text:
                    continue
                delta, emitted_text = _next_gemini_stream_delta(emitted_text, text)
                if delta:
                    yield delta

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
    return _reply_streaming(payload, model, api_key_value)


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
        raise RuntimeError("Gemini returned an empty response.")
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

app.title("Simple Gemini Chat")
app.caption("A small text-only Violit chat example.")
app.text_input("GEMINI_API_KEY", value=api_key.value, key="demo_gemini_api_key", type="password")


@reactivity
def render_chat():
    with app.chat_thread(height="60vh"):
        for message in messages.value:
            with app.chat_message(message.get("role", "assistant")):
                app.render_chat_message_body(message)


render_chat()
app.chat_input(
    "Ask Gemini",
    on_submit=submit_prompt,
    disabled=bool(busy.value),
)


app.run()