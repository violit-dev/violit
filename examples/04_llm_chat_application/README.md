# 4. LLM Chat Application Examples

This folder contains six small Violit chat examples that show the same problem at different API levels:

- `demo_app_gemini_primitive.py`
- `demo_app_openai_primitive.py`
- `demo_app_gemini_highlevel.py`
- `demo_app_openai_highlevel.py`
- `demo_app_gemini_agent_primitive.py`
- `demo_app_gemini_agent_highlevel.py`

The set is intentionally split along two axes:

- provider: Gemini or OpenAI
- API level: primitive or high-level

The two Gemini agent examples add a third axis:

- transcript type: plain chat or agent-oriented chat with status, trace, summary, and artifacts

## Before You Run

These examples are written for normal Violit users.
Install Violit first:

```bash
pip install violit
```

Then run whichever example file you want to try.

## Example Matrix

| File | Provider | Level | Main transcript API | Input API | Mode select | Display select | Smooth speed | Attachments/audio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `demo_app_gemini_primitive.py` | Gemini | Primitive | `chat_thread(...)` + `chat_message(...)` + `render_chat_message_body(...)` | `chat_input(...)` | Yes | Yes | Yes | No |
| `demo_app_openai_primitive.py` | OpenAI | Primitive | `chat_thread(...)` + `chat_message(...)` + `render_chat_message_body(...)` | `chat_input(...)` | Yes | Yes | Yes | No |
| `demo_app_gemini_highlevel.py` | Gemini | High-level | `chat_history(...)` | `managed_chat_input(...)` | Yes | Yes | Yes | No |
| `demo_app_openai_highlevel.py` | OpenAI | High-level | `chat_history(...)` | `managed_chat_input(...)` | Yes | Yes | Yes | No |
| `demo_app_gemini_agent_primitive.py` | Gemini | Primitive agent | `chat_thread(...)` + `agent_turn(...)` + `render_chat_message_body(...)` | `chat_input(...)` | Yes | Yes | Yes | Yes |
| `demo_app_gemini_agent_highlevel.py` | Gemini | High-level agent | `agent_history(...)` | `managed_chat_input(...)` | Yes | Yes | Yes | Yes |

## Run

### Gemini Primitive

```bash
python demo_app_gemini_primitive.py
```

### OpenAI Primitive

```bash
python demo_app_openai_primitive.py
```

### Gemini High-level

```bash
python demo_app_gemini_highlevel.py
```

### OpenAI High-level

```bash
python demo_app_openai_highlevel.py
```

### Gemini Agent Primitive

```bash
python demo_app_gemini_agent_primitive.py
```

### Gemini Agent High-level

```bash
python demo_app_gemini_agent_highlevel.py
```

Optional runtime flags also work, for example:

```bash
python demo_app_gemini_highlevel.py --port 8002
python demo_app_gemini_highlevel.py --lite
```

## Runtime Configuration

These examples do not depend on a local `.env` file.

Open the app and paste the API key into the password input at runtime.

- Gemini examples ask for `GEMINI_API_KEY`
- OpenAI examples ask for `OPENAI_API_KEY`

For Git safety, keep real keys out of source files, screenshots, and committed config files.

All six examples expose the same top-level runtime controls:

- `Mode`
- `Display`
- `Smooth speed`

These examples use the recommended external-state pattern for controls:

```python
api_key = app.state("")
mode = app.state("streaming")
display = app.state("smooth")
smooth_speed = app.state(7)

app.text_input("GEMINI_API_KEY", bind=api_key, type="password")
app.selectbox("Mode", ["streaming", "non-streaming"], bind=mode)
app.selectbox("Display", ["smooth", "instant"], bind=display)
app.slider("Smooth speed", 1, 10, bind=smooth_speed, step=1)
```

`key=` remains available for widget identity, but external state binding should use `bind=`.

The `Mode` options are:

- `streaming`
- `non-streaming`

The `Display` options are:

- `smooth`
- `instant`

`Smooth speed` uses a 1 to 10 slider, where 1 is the fastest reveal and 10 is the most gradual.

Only the two Gemini agent examples accept file and audio input.

## What Each Example Teaches

### 1. `demo_app_gemini_primitive.py`

This is the smallest Gemini chat that still feels like a real app.

What to look at:

- provider request helpers for Gemini streaming
- manual state updates with `append_message(...)` and `replace_last_message(...)`
- primitive rendering with `chat_thread(...)`, `chat_message(...)`, and `render_chat_message_body(...)`
- `chat_input(...)` as the primitive submit surface

This file is the right starting point if you want to understand the lowest-level plain chat flow.

### 2. `demo_app_openai_primitive.py`

This is the same primitive pattern, but with OpenAI request formatting.

What changes relative to the Gemini primitive example:

- OpenAI request URL and authorization header
- OpenAI SSE chunk parsing
- same primitive Violit rendering structure

If you already understand the Gemini primitive version, this file mainly shows provider differences.

### 3. `demo_app_gemini_highlevel.py`

This is the smallest Gemini example built on Violit's high-level chat API.

What to look at:

- `chat_history(messages, height="60vh")`
- `managed_chat_input(..., messages=messages, on_submit=reply)`
- `mode` state controlling streaming vs non-streaming

Compared with the primitive example, the input lifecycle and transcript mutations are mostly handled for you.

### 4. `demo_app_openai_highlevel.py`

This is the OpenAI counterpart to the Gemini high-level example.

What changes relative to the Gemini high-level example:

- OpenAI request payload and SSE parsing
- same `chat_history(...)` plus `managed_chat_input(...)` structure

This is the easiest file to compare against the Gemini high-level version when you only want provider-side differences.

### 5. `demo_app_gemini_agent_primitive.py`

This is a real Gemini-powered agent example rendered only with primitive Violit APIs.

What to look at:

- manual agent event generation
- message items carrying `phase`, `status`, `status_text`, `summary`, `trace`, `artifacts`, and `error`
- primitive transcript rendering with `agent_turn(...)`
- `chat_input(...)` configured with `accept_file="multiple"` and `accept_audio=True`

This is the file to read if you want full control over the agent transcript while still using Violit building blocks.

### 6. `demo_app_gemini_agent_highlevel.py`

This is the high-level version of the Gemini agent example.

What to look at:

- `agent_history(...)` for agent-oriented transcript rendering
- `managed_chat_input(...)` for the input lifecycle
- the same event schema as the primitive agent example, but with the rendering concerns mostly delegated to the framework

This is the shortest path to a richer agent UI when you do not need to manually assemble each turn.

## Primitive Vs High-level

Use the primitive examples when you want to control the transcript row by row.

Typical primitive shape:

```python
@reactivity
def render_chat():
    with app.chat_thread(height="60vh"):
        for message in messages.value:
            with app.chat_message(message.get("role", "assistant")):
                app.render_chat_message_body(message)


app.chat_input("Ask...", on_submit=submit_prompt)
```

Use the high-level examples when you want the framework to own most of the chat lifecycle.

Typical high-level shape:

```python
@reactivity
def render_chat():
    app.chat_history(messages, height="60vh")


app.managed_chat_input(
    "Ask...",
    messages=messages,
    on_submit=reply,
)
```

For agent-oriented histories, replace `chat_history(...)` with `agent_history(...)` and, in primitive mode, replace `chat_message(...)` with `agent_turn(...)`.

## Read The Code In This Order

1. Read the top-level state: `app`, `messages`, `api_key`, and sometimes `mode`.
2. Read the provider helper functions: request building, streaming parsing, and non-streaming fallback.
3. Read `reply(...)` or `submit_prompt(...)` to see how each example maps UI input into API work.
4. Read the reactive transcript renderer.
5. Read the final input widget outside the reactive block.

That order keeps the important distinction clear:

- provider code decides what text or events come back
- Violit code decides how those messages are rendered and submitted

## Smallest Mental Models

### Plain primitive chat

```python
messages = app.state([...])

def submit_prompt(prompt):
    append_user_message(prompt)
    append_empty_assistant_message()
    app.background(run_reply).start()

with app.chat_thread():
    for message in messages.value:
        with app.chat_message(message.get("role", "assistant")):
            app.render_chat_message_body(message)

app.chat_input(on_submit=submit_prompt)
```

### Plain high-level chat

```python
messages = app.state([...])

def reply(prompt):
    return provider_reply(messages.value)

app.chat_history(messages)
app.managed_chat_input(messages=messages, on_submit=reply)
```

### Agent primitive chat

```python
with app.chat_thread():
    for message in messages.value:
        with app.agent_turn(...):
            app.render_chat_message_body(message)

app.chat_input(on_submit=submit_prompt, accept_file="multiple", accept_audio=True)
```

### Agent high-level chat

```python
app.agent_history(messages)
app.managed_chat_input(messages=messages, on_submit=reply, accept_file="multiple", accept_audio=True)
```

Everything else in these files is either provider-specific HTTP formatting or agent-specific event generation.
