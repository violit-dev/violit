# Violit — AI/LLM Code Generation Reference

> **Violit ≈ Streamlit syntax + Reactive State (no rerun)**
> If you know Streamlit, you already know 90% of Violit.
> This document covers only the differences and Violit-specific patterns.

---

## Quick Mental Model

```
Streamlit: st.xxx()        → Violit: app.xxx()
st.session_state            → app.state()
Full script rerun on change → Only affected widgets update (Zero Rerun)
```

---

## 1. Boilerplate (Streamlit vs Violit)

```python
# ❌ Streamlit
import streamlit as st
st.title("Hello")
st.write("World")

# ✅ Violit
import violit as vl
app = vl.App(title="Hello", theme="ocean")
app.title("Hello")
app.write("World")
app.run()   # REQUIRED at the end
```

**Key differences:**
- `import violit as vl` (not `import streamlit as st`)
- Must create `app = vl.App(...)` instance first
- All widgets are called on `app` (e.g., `app.title()` not `st.title()`)
- Must call `app.run()` at the end of the script

**App constructor options:**
```python
app = vl.App(
    title="My App",             # Browser/window title
    theme="ocean",              # Theme preset (dark, light, ocean, cyberpunk, etc.)
    container_width="800px",    # Content max-width ("none" for full-width)
    mode="ws",                  # "ws" (WebSocket, default) or "lite" (HTMX)
)
```

**Running:**
```bash
python app.py                # Web mode (default)
python app.py --native       # Desktop app mode (pywebview)
python app.py --port 8020    # Custom port
python app.py --reload       # Hot reload on file change
```

---

## 2. State — The Core Difference

Streamlit uses `st.session_state` dict + full rerun. Violit uses reactive `State` objects.

```python
# ❌ Streamlit
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Click"):
    st.session_state.count += 1
st.write(st.session_state.count)

# ✅ Violit
count = app.state(0)
app.button("Click", on_click=lambda: count.set(count.value + 1))
app.write(count)  # Auto-updates when count changes
```

### State API

```python
# Create
count = app.state(0)                    # Auto key (file_line)
name = app.state("", key="user_name")   # Explicit key

# Read
count.value    # → 0
count()        # → 0  (shorthand)

# Write
count.set(5)       # Preferred in callbacks
count.value = 5    # Also works

# ⚠️ NEVER reassign the variable
count = 5  # ❌ WRONG — State object is lost!
```

### Passing State to Widgets (Reactivity)

```python
count = app.state(0)
name = app.state("World")

# ✅ Reactive — auto-updates when state changes
app.text(count)                            # State object directly
app.text(count * 2)                        # Operator overloading → ComputedState
app.text("Hello, " + name + "!")           # String concatenation
app.text(lambda: f"Count: {count.value}")  # Lambda for complex formatting
app.metric("Total", count)                 # State in any widget

# ❌ NOT reactive — value is frozen at call time
app.text(count.value)                      # Just passes int 0
app.text(f"Count: {count.value}")          # Just passes string "Count: 0"
```

**Rule of thumb:**
- Pass State **object** to widgets → reactive
- Pass `state.value` to widgets → frozen (not reactive)
- Use `lambda:` when you need f-string formatting or complex logic
- Use `.value` only in callbacks/calculations, not in widget arguments

---

## 3. Input Widgets — Return State, Not Values

In Streamlit, input widgets return the current value directly.
In Violit, input widgets return a **State object**.

```python
# ❌ Streamlit
name = st.text_input("Name")  # name is str
if st.button("Greet"):
    st.write(f"Hello {name}")

# ✅ Violit
name = app.text_input("Name")  # name is State[str]
app.button("Greet", on_click=lambda: app.toast(f"Hello {name.value}"))
app.text("Hello, " + name)     # Reactive display
```

### All Input Widgets (same names as Streamlit)

```python
name     = app.text_input("Name", value="default")
bio      = app.text_area("Bio", height=5)
age      = app.number_input("Age", value=0, min_value=0, max_value=120, step=1)
score    = app.slider("Score", min_value=0, max_value=100, value=50)
agree    = app.checkbox("I agree", value=False)
dark     = app.toggle("Dark mode", value=False)
size     = app.radio("Size", options=["S", "M", "L"], index=0)
lang     = app.selectbox("Language", options=["Python", "JS"], index=0)
tags     = app.multiselect("Tags", options=["A", "B", "C"], default=["A"])
color    = app.color_picker("Color", value="#ff0000")
date     = app.date_input("Date")
time     = app.time_input("Time")
file     = app.file_uploader("Upload", accept=".csv,.txt", multiple=False)
```

All return `State` objects. Access current value via `.value`.

---

## 4. Button — on_click Pattern (NOT if-block)

```python
# ❌ Streamlit pattern (if-block triggers rerun)
if st.button("Save"):
    save_data()

# ✅ Violit pattern (on_click callback, no rerun)
app.button("Save", on_click=save_data)
app.button("Save", on_click=lambda: save_data())

# Button variants
app.button("OK", variant="primary")       # default
app.button("Cancel", variant="neutral")
app.button("Delete", variant="danger")
app.button("Large", size="large")
```

**Important:** Violit buttons do NOT return a boolean.
Use `on_click=` to define what happens when clicked.

---

## 5. Layout — Same as Streamlit

```python
# Columns
col1, col2 = app.columns(2)
with col1:
    app.text("Left")
with col2:
    app.text("Right")

# Columns with ratio
c1, c2, c3 = app.columns([2, 1, 1])

# Container
with app.container(border=True):
    app.text("Inside a card")

# Tabs
tab1, tab2 = app.tabs(["Tab A", "Tab B"])
with tab1:
    app.text("Content A")
with tab2:
    app.text("Content B")

# Expander
with app.expander("Details", expanded=False):
    app.text("Hidden content")

# Sidebar
app.configure_sidebar(width=320, min_width=240, max_width=520, resizable=True)

with app.sidebar:
    app.text("Sidebar content")
```

---

## 6. Data & Charts — Same as Streamlit

```python
import pandas as pd
import plotly.express as px

df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})

app.dataframe(df)                            # AG Grid (interactive)
app.table(df)                                # Static HTML table
app.metric("Revenue", "$54,230", "+12%")     # Metric card
app.json({"key": "value"})                   # JSON viewer

# Charts
fig = px.line(df, x="x", y="y")
app.plotly_chart(fig)                        # Plotly chart

app.line_chart(df)                           # Quick charts
app.bar_chart(df)
app.area_chart(df)
app.scatter_chart(df)
```

---

## 7. Status & Feedback

```python
app.success("Saved!")
app.info("FYI")
app.warning("Caution")
app.error("Failed")
app.toast("Done!", variant="success")        # Pop-up notification
app.spinner("Loading...")
app.progress(75)                             # Progress bar (0-100)
app.balloons()
app.snow()
```

---

## 8. Chat Interface

```python
# Chat input with callback
def on_chat(msg):
    messages = chat_history.value.copy()
    messages.append({"role": "user", "content": msg})
    messages.append({"role": "assistant", "content": "Reply here"})
    chat_history.set(messages)

chat_history = app.state([])
app.chat_input("Type a message...", on_submit=on_chat)
```

---

## 9. Multi-Page Navigation

```python
import violit as vl
app = vl.App(title="Multi-Page")

def home():
    app.title("Home")
    app.text("Welcome!")

def settings():
    app.title("Settings")
    theme = app.selectbox("Theme", ["light", "dark", "ocean"])
    app.button("Apply", on_click=lambda: app.set_theme(theme.value))

# Sidebar with optional content
with app.sidebar:
    app.markdown("## My App")
    app.divider()

app.navigation([
    vl.Page(home, title="Home", icon="house"),
    vl.Page(settings, title="Settings", icon="gear"),
])

app.run()
```

---

## 10. Theme

```python
# Set at init
app = vl.App(theme="cyberpunk")

# Change at runtime
app.set_theme("ocean")

# Available themes:
# dark, light, ocean, sunset, forest, dracula, monokai, nord,
# cyberpunk, terminal, vaporwave, blueprint, neo_brutalism,
# soft_neu, hand_drawn, win95, bauhaus, editorial, glass,
# pastel, retro, ant, bootstrap, material,
# violit_light, violit_light_jewel, violit_dark, rgb_gamer, ...
```

---

## 11. Styling (cls & style)

Every widget supports `cls` and `style` parameters.

```python
app.text("Big", style="font-size: 2rem; font-weight: 800;")
app.button("Wide", cls="w:100%", variant="primary")
app.card(cls="glass", style="padding: 2rem;")

# Global CSS
app.add_css("""
    .glass {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(16px);
    }
""")

# Widget type defaults
app.configure_widget("button", cls="font:600")
app.configure_widget("card", style="border-radius: 1rem;")
```

---

## 12. Dialog

```python
@app.dialog("Confirm")
def confirm_dialog():
    app.text("Are you sure?")
    app.button("Yes", on_click=do_action)

app.button("Open Dialog", on_click=confirm_dialog)
```

---

## 13. Conditional & Loop Rendering

```python
count = app.state(0)

# Conditional rendering (reactive)
app.If(
    lambda: count.value > 5,
    then=lambda: app.success("Big!"),
    else_=lambda: app.info("Small"),
)

# Loop rendering (reactive)
items = app.state(["Apple", "Banana"])
app.For(
    items,
    render=lambda item: app.text(f"- {item}"),
    empty=lambda: app.info("No items"),
)
```

---

## Common Mistakes to Avoid

```python
# ❌ WRONG: Using Streamlit's if-block pattern for buttons
if app.button("Click"):   # Buttons don't return bool in Violit
    do_something()

# ✅ CORRECT:
app.button("Click", on_click=do_something)

# ❌ WRONG: Forgetting app.run()
app.title("Hello")
# Script ends without app.run()

# ✅ CORRECT:
app.title("Hello")
app.run()

# ❌ WRONG: Passing .value to widgets (not reactive)
app.text(count.value)

# ✅ CORRECT: Pass State object directly
app.text(count)

# ❌ WRONG: Using f-string directly (not reactive)
app.text(f"Count: {count.value}")

# ✅ CORRECT: Use lambda or operator
app.text(lambda: f"Count: {count.value}")
app.text("Count: " + count)

# ❌ WRONG: Reassigning state variable
count = count.value + 1

# ✅ CORRECT:
count.set(count.value + 1)
```

---

## Complete Example: Dashboard

```python
import violit as vl
import pandas as pd
import numpy as np

app = vl.App(title="Dashboard", theme="ocean", container_width="1200px")

# State
data_size = app.state(50)

# Sidebar
with app.sidebar:
    app.markdown("## Dashboard")
    app.divider()
    theme = app.selectbox("Theme", ["ocean", "dark", "cyberpunk"])
    app.button("Apply", on_click=lambda: app.set_theme(theme.value))

# Main content
app.header("Sales Dashboard")

c1, c2, c3 = app.columns(3)
with c1: app.metric("Revenue", "$54,230", "+12%")
with c2: app.metric("Users", "1,234", "+5%")
with c3: app.metric("Uptime", "99.9%", "0%")

app.divider()

n = app.slider("Data points", 10, 200, 50)

app.line_chart(
    lambda: pd.DataFrame(
        np.random.randn(n.value, 3),
        columns=["A", "B", "C"]
    )
)

app.run()
```

---

## API Quick Reference

| Category | Streamlit | Violit | Note |
|----------|-----------|--------|------|
| Import | `import streamlit as st` | `import violit as vl` | |
| App init | (implicit) | `app = vl.App(...)` | Required |
| Run | `streamlit run app.py` | `python app.py` + `app.run()` | |
| State | `st.session_state.x = 0` | `x = app.state(0)` | Returns reactive State |
| Read state | `st.session_state.x` | `x.value` or `x()` | |
| Write state | `st.session_state.x = 5` | `x.set(5)` or `x.value = 5` | |
| Button | `if st.button("X"):` | `app.button("X", on_click=fn)` | Callback, not if-block |
| Input return | `val = st.text_input()` (str) | `val = app.text_input()` (State) | |
| Rerun | `st.rerun()` | Not needed | Auto partial update |
| Cache | `@st.cache_data` | Not needed | No full rerun |
| Fragment | `@st.fragment` | Not needed | Fine-grained reactivity by design |
| Key | `st.button("X", key="k")` | Usually not needed | Auto-generated |
| Sidebar | `st.sidebar.xxx()` | `with app.sidebar: app.xxx()` | Context manager |
| Pages | `st.Page` in `st.navigation` | `vl.Page` in `app.navigation` | |
| Theme | `config.toml` | `app = vl.App(theme="ocean")` | 30+ presets |
| Desktop | Not available | `python app.py --native` | pywebview |
