# 4. Very Simple LLM Chat Application

This folder has three small chat examples:

- `demo_app_gemini.py`
- `demo_app_openai.py`
- `demo_app_gemini_agent.py`

They have the same structure on purpose.

If you understand one file, the other file should feel familiar.

## Files

- `demo_app_gemini.py`: Gemini chat example
- `demo_app_openai.py`: OpenAI chat example
- `demo_app_gemini_agent.py`: Gemini-powered agent example with visible trace and local tools

## Run

### Gemini

```bash
cd examples/4_llm_chat_application
python demo_app_gemini.py
```

### OpenAI

```bash
cd examples/4_llm_chat_application
python demo_app_openai.py
```

### Gemini Agent

```bash
cd examples/4_llm_chat_application
python demo_app_gemini_agent.py
```

## Configure

There is no `.env` file in these examples.

Open the app and paste your API key into the password input.

- `demo_app_gemini.py` asks for `GEMINI_API_KEY`
- `demo_app_gemini_agent.py` asks for `GEMINI_API_KEY`
- `demo_app_openai.py` asks for `OPENAI_API_KEY`

Each app also has a simple `Mode` selectbox:

- `streaming`
- `non-streaming`

That lets you compare the two response styles in the same UI.

## What The App Shows

All three examples follow the same pattern:

- create `app`, `messages`, `api_key`, and `mode`
- show a password input for the API key
- show a mode selectbox
- render chat messages in a reactive block
- keep `app.chat_input(...)` outside the reactive block

This keeps the message list reactive while the input widget stays simple.

## Read The Code In This Order

### 1. Create app state

```python
app = vl.App(...)
messages = app.state([...])
api_key = app.state("")
mode = app.state("streaming")
```

- `messages` stores the chat history
- `api_key` stores the pasted key
- `mode` chooses streaming or non-streaming

### 2. Read the API helpers

Each file now separates the two response paths:

```python
def _reply_non_streaming(...):
    ...

def _reply_streaming(...):
    ...
```

This makes it obvious which code runs in each mode.

### 3. Read `reply()`

```python
def reply(_prompt: str):
    ...
    if mode.value == "streaming":
        return _reply_streaming(...)
    return _reply_non_streaming(...)
```

`reply()` only builds the payload and chooses the correct helper.

### 4. Read the UI

```python
@reactivity
def render_chat():
    app.chat_messages(messages, height="60vh")


render_chat()
app.chat_input(..., messages=messages, on_submit=reply)
```

The reactive part only renders the messages.

## What Is Different Between The Two Files

The overall shape is the same.

The main difference is only the request and response format:

- Gemini uses the Gemini API structure
- OpenAI uses the OpenAI API structure
- Gemini Agent uses Gemini both as planner and final answerer, then maps the run into `status`, `step`, `summary`, `text`, `artifact`, and `done` events

## The Smallest Mental Model

```python
messages = app.state([...])
mode = app.state("streaming")

def reply(prompt):
    if mode.value == "streaming":
        return stream_text_from_api(messages.value)
    return get_text_from_api(messages.value)

app.chat_messages(messages)
app.chat_input(messages=messages, on_submit=reply)
```

That is the whole idea.

Everything else is provider-specific request formatting.
