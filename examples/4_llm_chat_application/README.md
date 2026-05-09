# 4. Very Simple LLM Chat Application

This folder contains small chat examples:

- `demo_app_gemini.py`
- `demo_app_openai.py`
- `demo_app_gemini_agent.py`
- `demo_app_compare_violit_agent.py`
- `demo_app_compare_streamlit_agent.py`

They intentionally share the same overall shape, so once you understand one file, the others should feel familiar.

## Files

- `demo_app_gemini.py`: Gemini chat example
- `demo_app_openai.py`: OpenAI chat example
- `demo_app_gemini_agent.py`: Gemini-powered agent example with visible trace and local workspace tools
- `demo_app_compare_violit_agent.py`: small Violit agent-chat example for 1:1 comparison with Streamlit
- `demo_app_compare_streamlit_agent.py`: functionally similar Streamlit version of the same fake-agent flow

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

### Compare: Violit

```bash
cd examples/4_llm_chat_application
python demo_app_compare_violit_agent.py
```

### Compare: Streamlit

```bash
cd examples/4_llm_chat_application
streamlit run demo_app_compare_streamlit_agent.py
```

## Configure

These examples do not rely on a local `.env` file.

Open the app and paste your API key into the password input.
All three examples start with an empty key field, so the credential is entered manually at runtime.

- `demo_app_gemini.py` asks for `GEMINI_API_KEY`
- `demo_app_gemini_agent.py` asks for `GEMINI_API_KEY`
- `demo_app_openai.py` asks for `OPENAI_API_KEY`

For Git safety, keep real keys out of source files, screenshots, and committed config files.

Each app also has a simple `Mode` selectbox:

- `streaming`
- `non-streaming`

This lets you compare the two response styles in the same UI.

## Violit vs Streamlit Comparison Pair

The two `demo_app_compare_*` files intentionally implement nearly the same agent-chat behavior:

- a shared `fake_agent_stream(...)`
- a user message followed by an assistant placeholder
- visible running / done / failed status
- incremental text streaming
- reset button

The difference is the framework model:

- Violit uses `app.state(...)`, a small `@reactivity` block for the transcript, and `app.chat_input(..., on_submit=...)` outside the reactive block
- Streamlit uses reruns plus `st.session_state`, and handles the chat turn inline with `if prompt := st.chat_input(...)`

This pair is useful when you want to compare framework shape rather than model/provider integration.

## What The App Shows

The three provider-backed Violit examples follow the same pattern:

- create `app`, `messages`, `api_key`, and `mode`
- show a password input for the API key
- show a mode selectbox
- render chat messages in a reactive block
- keep `app.managed_chat_input(...)` outside the reactive block

This keeps the message list reactive while the input widget stays simple and stable.

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

`reply()` mainly builds the payload and chooses the correct helper.

### 4. Read the UI

```python
@reactivity
def render_chat():
    app.chat_history(messages, height="60vh")


render_chat()
app.managed_chat_input(..., messages=messages, on_submit=reply)
```

The reactive part only renders the messages.
The input stays outside that block so it does not get rebuilt with every message update.

## What Is Different Between The Files

The overall shape is the same.

The main differences are the provider-specific request format and, in the agent example, the event schema:

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

app.chat_history(messages)
app.managed_chat_input(messages=messages, on_submit=reply)
```

That is the whole idea.

Everything else is provider-specific request formatting or, for the agent example, event generation and tool orchestration.
