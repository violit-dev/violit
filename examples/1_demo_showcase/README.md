# 1. Violit Showcase Demo

This example is the broad, polished tour of Violit.

It is not the smallest example in the repository.
It is the example to open when you want to feel what a modern multi-page Violit app can look like with charts, reactive UI, built-in chat widgets, styling helpers, and runtime theme switching in one file.

## File

- `demo_showcase.py`: a multi-page showcase app

## Run

```bash
cd examples/1_demo_showcase
violit run demo_showcase.py
```

By default, the app runs in WebSocket mode and starts with the bright `violit_light_jewel` theme.

You can also run it in Lite mode:

```bash
violit run demo_showcase.py --lite
```

Lite mode uses HTMX and is a good way to preview the same demo in Violit's lighter HTTP runtime.

## What This Example Shows

This app includes several pages in one sidebar navigation:

- `Home`: a more visual landing page with feature cards, quickstart actions, and a curated first impression
- `Dashboard`: metrics, chart tabs, a dataframe, and a small `@app.reactivity` block
- `Reactive Logic`: `State`, `app.If(...)`, `app.For(...)`, live sliders, and partial updates
- `Widgets`: a live preview panel, `download_button`, `link_button`, dialogs, and a broader widget gallery
- `Chat`: Violit's built-in `chat_messages(...)` and `chat_input(...)` with safe pseudo replies instead of a real AI API
- `Settings`: curated theme presets plus runtime controls for primary color, animation mode, and selection mode

There is no database setup and no API key needed.

## Read The Code In This Order

### 1. Mode detection and app setup

```python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
if SRC_ROOT.exists():
    sys.path.insert(0, str(SRC_ROOT))

mode = "lite" if "--lite" in sys.argv else "ws"

app = vl.App(
    title="Violit Showcase",
    mode=mode,
    theme="violit_light_jewel",
    container_width="1200px",
)
```

The example chooses `ws` by default, switches to `lite` when you pass `--lite`, and makes sure the local repository version of Violit is imported during development.

### 2. Shared state

```python
chat_history = app.state([...], key="showcase_chat_history")
chat_mode = app.state("streaming", key="showcase_chat_mode")
chat_style = app.state("Builder", key="showcase_chat_style")
dashboard_seed = app.state(0, key="showcase_dashboard_seed")
```

This state is shared across pages for the pseudo chat demo and dashboard refreshes.

### 3. Page functions

Each page is still a normal Python function:

```python
def home_page():
    ...

def dashboard_page():
    ...

def chat_page():
    ...
```

This keeps the app easy to scan even though it covers a lot of surface area.

### 4. Built-in chat widgets

The `Chat` page now demonstrates the recommended Violit chat pattern:

```python
@app.reactivity
def render_chat():
    app.chat_messages(chat_history, height="62vh", border=True)

render_chat()

app.chat_input(
    "Ask about themes, auth, ORM, Lite mode, or styling...",
    messages=chat_history,
    on_submit=_pseudo_chat_reply,
)
```

The reply function only returns pseudo content.
It does not call OpenAI, Gemini, or any external LLM API.

### 5. Reactive bindings and helpers

This showcase demonstrates several current Violit patterns in one place:

```python
app.card(lambda: ...)
app.If(lambda: ..., then=..., else_=...)
app.For(lambda: items[:count.value], render=...)
```

The `Reactive Logic` page is the clearest place to study these patterns.

### 6. Styling and dialogs

The `Widgets` page mixes input widgets with styling-oriented examples:

```python
app.button("Rounded CTA", cls="w-full rounded-full shadow-lg font-semibold")
app.download_button(...)
app.link_button(...)

@app.dialog("Tailwind Notes")
def tailwind_notes_dialog():
    ...
```

This is a good page to inspect if you want examples of `cls`, visual cards, helper widgets, and a larger built-in widget gallery.

### 7. Sidebar navigation

```python
app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(dashboard_page, title="Dashboard", icon="chart-line"),
    ...
])
```

The example uses Violit's built-in sidebar and page navigation to turn one file into a small showcase app.

## Good Pages To Explore First

If you only want a quick feel for the updated showcase, start here:

- `Home` for the overall visual direction and quickstart actions
- `Chat` for the built-in chat widget flow with pseudo replies
- `Widgets` for Tailwind-friendly button styling, helper widgets, and dialog usage
- `Reactive Logic` for clear examples of partial UI updates without full reruns

## Notes

- The `Chat` page is safe for GitHub and docs because it does not require any secret or external API.
- The `Widgets` page includes a tiny Tailwind-friendly preview and `cls`-based buttons to show how styling can stay in Python.
- The `Settings` page changes theme, primary color, animation mode, and text selection behavior at runtime.
- The `Home` page uses only in-app markup and stateful controls for the hero area.
- This example is meant to feel wide and attractive rather than minimal.

If you want the smallest examples, check the other folders in `examples/`.
