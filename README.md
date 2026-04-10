<p align="center">
  <img src="https://github.com/user-attachments/assets/f6a56e37-37a5-437c-ae16-13bff7029797" alt="Violit Logo" width="100%">
</p>

🎉 **Featured on OpenSourceProjects.dev** : ["Stop Overcomplicating Your Data Dashboards"](https://www.opensourceprojects.dev/post/634ad562-83d4-4a7b-8a74-b61e47ad68aa)


# 💜 Violit

> **"Faster than Light, Beautiful as Violet."**
> **Structure of Streamlit × Performance of React.**

**Violit** is a next-generation Python web framework that adopts a **Fine-Grained State Architecture** for instant reactivity, unlike Streamlit's **Full Script Rerun** structure.

Build applications that react at the speed of light with the most elegant syntax.

<p align="center">
<img src="https://img.shields.io/pypi/v/violit?color=blueviolet&style=flat-square&ignore=cache" alt="PyPI">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python 3.10+">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
<img src="https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square" alt="FastAPI">
<img src="https://img.shields.io/badge/UI-Shoelace-7C4DFF.svg?style=flat-square" alt="Shoelace">
</p>

---

## 📸 Demo

*A dashboard built with Violit running in real-time.*

<p align="center">
  <img src="https://raw.githubusercontent.com/violit-dev/violit/refs/heads/main/assets/demo_show_main_small.gif" alt="Violit Showcase Demo" width=60%>
</p>



---

## ⚡ Why Violit?

### Architectural Differences

Violit and Streamlit are similar in that they build UIs with Python code, but their internal mechanisms are fundamentally different.

| Feature | Streamlit (Traditional) | **Violit (Reactive)** |
| --- | --- | --- |
| **Execution Model** | **Full Script Rerun**<br>Reruns the entire script on every user interaction. | **Fine-Grained Updates**<br>Updates only the components connected to the modified State. |
| **Performance** | Response speed may degrade as data size increases. | Maintains consistent reactivity regardless of data scale. |
| **Optimization** | Requires optimization decorators like `@cache`, `@fragment`. | Optimized by design without extra optimization code. |
| **Deployment** | Optimized for web browser execution. | Supports both Web Browser and **Desktop Native App** modes. |
| **Design** | Focuses on providing basic UI. | Provides ready-to-use designs with **20+ professional themes**. |

### Key Features

1.  **Optimization by Design (Streamlit-Like Syntax, No Complexity)**:
    Streamlit's intuitive syntax is maintained, but complex optimization tools are removed at the architecture level.
    *   ❌ **No `@cache_data`, `@fragment`, `st.rerun`**: Thanks to the fine-grained structure, manual optimization is unnecessary.
    *   ❌ **No `key` Management**: No need to manually specify unique keys for widget state management.
    *   ❌ **No Complex Callbacks**: No need to define complex callbacks/classes like Dash or Panel.

2.  **Ultra-Fast Speed**: Even if you move the slider in 0.1s increments, the chart reacts in real-time without stuttering.

3.  **Hybrid Runtime**:
    *   **WebSocket Mode**: Ultra-low latency bidirectional communication (Default)
    *   **Lite Mode**: HTTP-based, advantageous for handling large-scale concurrent connections

4.  **Desktop Mode**: Can run as a perfect desktop application without Electron using the `--native` option.

---

## 🎨 Theme Gallery

You don't need to know CSS at all. Violit provides over 20 themes. (Soon, users will be able to easily add Custom Themes.)

*Theme demo will be updated soon.*

![Theme Gallery Grid](PLACEHOLDER_FOR_THEME_GALLERY_GRID)

```python
# Configuration at initialization
app = vl.App(theme='cyberpunk')

# Runtime change
app.set_theme('ocean')
```

| Theme Family | Examples |
| --- | --- |
| **Dark 🌑** | `dark`, `dracula`, `monokai`, `ocean`, `forest`, `sunset` |
| **Light ☀️** | `light`, `pastel`, `retro`, `nord`, `soft_neu` |
| **Tech 🤖** | `cyberpunk`, `terminal`, `cyber_hud`, `blueprint` |
| **Professional 💼** | `editorial`, `bootstrap`, `ant`, `material`, `lg_innotek` |

---

## 📈 Benchmarks & Performance

Benchmark results showing how efficient Violit's fine-grained update method is compared to the existing full rerun method.



*Detailed benchmark data will be updated soon.*

![Benchmark Chart](PLACEHOLDER_FOR_BENCHMARK_CHART)


---

## 🚀 Comparison

### Python UI Frameworks

| Framework | Architecture | Learning Curve | Performance | Desktop App | Real-time |
|-----------|---------|----------|---------|------------|------------|
| **Streamlit** | Full Rerun | Very Easy | Slow | ❌ | △ |
| **Dash** | Callback | Medium | Fast | ❌ | △ |
| **Panel** | Param | Hard | Fast | ❌ | ✅ |
| **Reflex** | React (Compile) | Hard | Fast | ❌ | ✅ |
| **NiceGUI** | Vue | Easy | Fast | ✅ | ✅ |
| **Violit** | **Signal** | **Very Easy** | **Fast** | **✅** | **✅** |

### Code Comparison

#### **1. vs Streamlit** (Rerun vs Signal)
*Streamlit re-executes the **entire script** on button click, but Violit executes only **that function**.*

```python
# Streamlit
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Click"):
    st.session_state.count += 1 # Rerun triggers here

st.write(st.session_state.count)
```

```python
# Violit
import violit as vl
app = vl.App()

count = app.state(0)

# Update only count on click (No Rerun)
app.button("Click", on_click=lambda: count.set(count.value + 1))
app.write(count) 
```

#### **2. vs Dash** (Callback Hell vs Auto-Reactivity)
*Dash requires complex **Callbacks** connecting Input/Output, but Violit only needs a single **State**.*

```python
# Dash
from dash import Dash, html, Input, Output, callback

app = Dash(__name__)
app.layout = html.Div([
    html.Button("Click", id="btn"),
    html.Div(id="out")
])

@callback(Output("out", "children"), Input("btn", "n_clicks"))
def update(n):
    return f"Value: {n}" if n else "Value: 0"
```

```python
# Violit
count = app.state(0)

app.button("Click", on_click=lambda: count.set(count.value + 1))
# Automatic state dependency tracking -> No Callback needed
app.write(lambda: f"Value: {count.value}")
```

#### **3. vs NiceGUI** (Binding vs Direct State)
*NiceGUI is also great, but Violit offers a **more concise syntax** in the style of Streamlit.*

```python
# NiceGUI
from nicegui import ui

count = {'val': 0}
ui.button('Click', on_click=lambda: count.update(val=count['val'] + 1))
ui.label().bind_text_from(count, 'val', backward=lambda x: f'Value: {x}')
```

```python
# Violit
count = app.state(0)
app.button('Click', on_click=lambda: count.set(count.value + 1))
app.write(count) # No need for complex connections like .bind_text
```

#### **4. vs Reflex** (Class & Compile vs Pure Python)
*Reflex requires State **class definition** and **compilation**, but Violit is a **pure Python** script.*

```python
# Reflex
import reflex as rx

class State(rx.State):
    count: int = 0
    def increment(self):
        self.count += 1

def index():
    return rx.vstack(
        rx.button("Click", on_click=State.increment),
        rx.text(State.count)
    )
```

```python
# Violit
# No class definition needed, no compilation needed
count = app.state(0)
app.button("Click", on_click=lambda: count.set(count.value + 1))
app.write(count)
```

---

## 🚀 Quick Start

### 1. Installation

Can be installed in Python 3.10+ environments.

```bash
pip install violit

# Or development version
pip install git+https://github.com/violit-dev/violit.git
```


### 2. Hello, Violit!

Create a `hello.py` file.

```python
import violit as vl

app = vl.App(title="Hello Violit", theme='ocean')

app.title("💜 Hello, Violit!")
app.markdown("Experience the speed of **Zero Rerun**.")

count = app.state(0)

col1, col2 = app.columns(2)
with col1:
    app.button("➕ Plus", on_click=lambda: count.set(count.value + 1))
with col2:
    app.button("➖ Minus", on_click=lambda: count.set(count.value - 1))

app.metric("Current Count", count)

app.run()
```

### 3. Execution

```bash
# Basic run (WebSocket Mode)
python hello.py

# Desktop App Mode (Recommended)
python hello.py --native

# Port configuration
python hello.py --port 8020
```

---

## 📚 Widget Support

Violit supports core Streamlit widgets, and some features have been redesigned for greater efficiency.

For a detailed compatibility list and information on unsupported widgets, please refer to the [Streamlit API Support Matrix](./doc/Streamlit%20API%20Support%20Matrix.md) document.

---

## 🛠️ Tech Stack

*   **Backend**: FastAPI (Async Python)
*   **Frontend**: Web Components (Shoelace), Plotly.js, AG-Grid
*   **Protocol**: WebSocket & HTTP/HTMX Hybrid
*   **State**: Signal-based Reactivity

---

## 🗺️ Roadmap

Violit is continuously evolving.

*   ✅ **Core**: Signal State Engine, Theme System
*   ✅ **Widgets**: Plotly, Dataframe, Input Widgets
*   ✅ **Homepage**: Official Homepage Open 
*   ✅ **Documentation**: Official Technical Documentation and API Reference Update 
*   ⏳ **Custom Components**: User-defined Custom Component Support 
*   ⏳ **Custom Theme**: User-defined Custom Theme Support 
*   ⏳ **async**: Async processing support 
*   ⏳ **More examples**: Provide more real-world usable example code 
*   ⏳ **Violit.Cloud**: Cloud deployment service
*   ⏳ **Expansion**: Integration of more third-party libraries

---

## 📂 Project Structure

```bash
.
├── violit/            # Framework source code
│   ├── app.py         # Main App class and entry point
│   ├── broadcast.py   # Real-time WebSocket broadcasting
│   ├── state.py       # Reactive State Engine
│   ├── theme.py       # Theme management
│   ├── assets/        # Built-in static files
│   └── widgets/       # Widget implementations
│       ├── input_widgets.py
│       ├── data_widgets.py
│       ├── layout_widgets.py
│       └── ...
└── requirements.txt   # Dependency list
```

---

## 🤝 Contributing

**Violit** is an open-source project. Let's build the future of faster and more beautiful Python UIs together.

1.  Fork this repository
2.  Create your feature branch
3.  Commit your changes
4.  Push to the branch
5.  Open a Pull Request

---

## 📝 License

MIT License

**Violit™ is a trademark of The Violit Team.**

---

<p align="center">
<strong>Made with 💜 by the Violit Team</strong>
<br>
<em>Faster than Light, Beautiful as Violet.</em>
</p>
