![img1](./assets/violit_glare_small.png)

# 💜 Violit

> **"Faster than Light, Beautiful as Violet."**
> **Streamlit's Intuition × React's Performance**

**Violit** is a next-generation Python web framework that perfectly solves Streamlit's critical **Full Script Rerun** issue with **O(1) State Architecture**.

Build applications that react at the speed of light with the most elegant syntax.

<p align="center">
<img src="https://img.shields.io/pypi/v/violit?color=blueviolet&style=flat-square" alt="PyPI">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python 3.10+">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
<img src="https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square" alt="FastAPI">
<img src="https://img.shields.io/badge/UI-Shoelace-7C4DFF.svg?style=flat-square" alt="Shoelace">
</p>

---

## ⚡ Why Violit?

### 🎯 Going Beyond Streamlit's Limits

Violit isn't just "faster Streamlit". **The architecture itself is different.**

| Feature | Streamlit 🐢 | **Violit 💜** |
| --- | --- | --- |
| **Architecture** | **Full Rerun (O(N))**<br><br>Re-executes the entire code on a single button press | **Zero Rerun (O(1))** ⚡<br><br>Updates only the changed components exactly |
| **UX/UI** | Slow response, screen flickering | **React-grade Reactivity**, smooth with no flicker |
| **Optimization** | Complex optimizations like `@cache`, `@fragment` required | **No optimization code needed** (Optimized by design) |
| **Scalability** | Limited concurrent users (High memory usage) | **Lite Mode** supports massive traffic 🌐 |
| **Deployment** | Web browser only | Web + **Desktop App Mode** 💻 |
| **Design** | Basic default design | **30+ Premium Themes** built-in 🎨 |

### ⭐ Violit Signatures

1. **Ultra-Fast Speed**: Charts react in real-time without stutter, even when dragging sliders in 0.1s increments.
2. **Streamlit-Like API**: Existing Streamlit users can adapt in 10 minutes. Code is 90% compatible.
3. **Hybrid Runtime**:
   * **WebSocket Mode**: Ultra-low latency bidirectional communication, real-time broadcasting (Default) ⚡
   * **Lite Mode**: HTTP-based, handles thousands of concurrent users (For large-scale dashboards)
4. **Run as Desktop Mode**: Create a perfect desktop app without Electron using a single `--native` flag.

---

## 🔥 Why Violit Over Others?

### 📊 Python UI Framework Comparison

| Framework | Architecture | Learning Curve | Performance | Desktop App | Real-time |
|-----------|---------|----------|---------|------------|------------|
| **Streamlit** | Full Rerun (O(N)) | ⭐⭐⭐⭐⭐ Very Easy | 🐢 Slow | ❌ | ❌ (Limited) |
| **Dash (Plotly)** | Callback Based | ⭐⭐⭐ Average | ⚡ Fast | ❌ | ✅ (Complex) |
| **Panel** | Param Based | ⭐⭐ Hard | ⚡ Fast | ❌ | ✅ |
| **NiceGUI** | Vue Based | ⭐⭐⭐⭐ Easy | ⚡ Fast | ✅ | ✅ |
| **Reflex** | React Style | ⭐⭐ Hard | ⚡ Fast | ❌ | ✅ |
| **Violit 💜** | **Zero Rerun (O(1))** | ⭐⭐⭐⭐⭐ **Very Easy** | **⚡⚡ Fastest** | **✅** | **✅ Built-in** |

### 🎯 Reasons to Choose Violit

#### 1️⃣ **vs Streamlit**: Same Syntax, 100x Faster
```python
# Easy like Streamlit, but instant reaction without re-rendering
app.button("Click", on_click=lambda: count.set(count.value + 1))
app.write("Count:", count)  # Updates only this part when State changes!
```
- Keeps Streamlit's **intuitive API**, removes **Full Rerun pain** completely.
- No need for complex optimizations like caching, fragments, or reruns.

#### 2️⃣ **vs Dash**: Reactivity Without Callback Hell
```python
# Dash needs complex callback chains, but
# Violit automatically updates dependent components just by changing State
count = app.state(0)
app.write(lambda: f"Value: {count.value}")  # Auto-tracking
```
- Removes Dash's **`@callback` boilerplate hell**.
- More intuitive State-based reactivity.

#### 3️⃣ **vs Panel**: Power Without the Learning Curve
```python
# Simple, without Panel's Param class
name = app.state("World")
app.write(lambda: f"Hello, {name.value}!")
```
- No need for Panel's **complex Param system**.
- Easy like Streamlit, powerful like Panel.

#### 4️⃣ **vs NiceGUI**: Desktop Apps with Python Only
- Supports **real-time WebSocket** like NiceGUI.
- But Violit adds **30+ Premium Themes** and **Desktop Mode**.
- No Vue.js knowledge needed, Python is enough.

#### 5️⃣ **vs Reflex**: Start Immediately Without Config
```python
# Reflex needs complex config and compilation, Violit is:
import violit as vl
app = vl.App()
app.title("Hello!")
app.run()  # Done!
```
- No **Node.js dependency** like Reflex.
- **No separate build step**, complete with a single Python file.

### 💎 Violit's Unique Advantages

1. **Zero Configuration**: `pip install violit` → Start immediately.
2. **Zero Learning Curve**: If you know Streamlit, you're done in 5 minutes.
3. **Zero Performance Issues**: O(1) architecture scales to any size.
4. **Desktop Mode**: Run desktop mode with a single `--native` line.
5. **30+ Premium Themes**: Expert-level UI without a designer.
6. **Real-time Broadcasting**: Multi-user synchronization built-in.

---

## 🐢 Streamlit vs 🏎️ Violit

### Streamlit Way (Inefficient)

The code **re-runs from top to bottom** on every interaction. Data is re-loaded every time.

```python
import streamlit as st

# ⚠️ This heavy function runs repeatedly on every button click
df = load_huge_dataset() 

if 'count' not in st.session_state:
    st.session_state.count = 0

# ⚠️ Screen flickers due to full page reload
if st.button('Increase'):
    st.session_state.count += 1 
    
st.write(f"Count: {st.session_state.count}")
```

### Violit Way (Elegant)

The script **runs only once**. UI automatically reacts when State changes.

```python
import violit as vl

app = vl.App()

# ✅ Runs only once! 0% resource waste
df = load_huge_dataset()

# Declare State (Signal based)
count = app.state(0)

# Changing value on click -> UI reflects instantly (No Rerun)
app.button("Increase", on_click=lambda: count.set(count.value + 1))

# ✨ Auto-Reactive by passing State object directly!
app.write("Count:", count)

app.run()
```

---

## 🧩 The "Zero Rerun" Philosophy

Violit eliminates the **unnecessary complexity** that plagued developers.

### 🚫 What You Don't Need Anymore

* ❌ **`@st.cache_data`**: Why cache when code only runs once?
* ❌ **`@st.fragment`**: All Violit widgets are already independent. (Though `@app.fragment` is supported if you want!)
* ❌ **`st.rerun()`**: No need to force re-execution. Just change the state.
* ❌ **`key="widget_1"`**: No need to manage keys to preserve widget state.
* ❌ **Complex Callback Chains**: No need to link Input/Output like in Dash. State solves everything.
* ❌ **Defining Param Classes**: No need to write complex parameter classes like in Panel.

### ✅ Violit's Innovative Approach

```python
# 1. State-based Reactivity (Solid.js Signals style)
counter = app.state(0)
app.write(counter)  # Auto-update when counter changes!

# 2. Dynamic Content with Lambdas
app.write(lambda: f"Current Time: {time.time()}")  # Auto-dependency tracking

# 3. Clear Actions with Callbacks
app.button("Click", on_click=lambda: counter.set(counter.value + 1))

# 4. Group with Fragment if needed (Streamlit-like)
@app.fragment
def dashboard():
    # This area re-runs when internal State changes
    app.header("Dashboard")
    app.metric("Visitors", visitors.value)
```

---

## 🎨 30+ Premium Themes

You don't need to know CSS at all. Violit provides over 30 designer-tuned themes.

```python
# Change theme with one line
app = vl.App(theme='cyberpunk', title='My App')

# Change at runtime
app.set_theme('ocean')
```

| Theme Family | Examples |
| --- | --- |
| **Dark 🌑** | `dark`, `dracula`, `monokai`, `ocean`, `forest`, `sunset` |
| **Light ☀️** | `light`, `pastel`, `retro`, `nord`, `soft_neu` |
| **Tech 🤖** | `cyberpunk`, `terminal`, `cyber_hud`, `blueprint` |
| **Professional 💼** | `editorial`, `bootstrap`, `ant`, `material`, `lg_innotek` |

**Comparison with others:**
- **Streamlit**: Only basic themes, complex customization.
- **Dash**: Must write CSS manually.
- **Panel**: Limited theme options.
- **Violit**: 30+ ready-to-use expert themes 💜

---

## 🚀 Quick Start

### 1. Installation

Install `violit` from PyPI. (Python 3.10+ required)

```bash
pip install violit

# Or development version
pip install git+https://github.com/yourusername/violit.git
```

### 2. Hello, Violit!

Create a `hello.py` file.

```python
import violit as vl

# Create Violit app instance
app = vl.App(title="Hello Violit", theme='ocean')

app.title("💜 Hello, Violit!")
app.markdown("Experience the speed of **Zero Rerun**.")

# Define State
count = app.state(0)

col1, col2 = app.columns(2)

with col1:
    # Cleanly change value on click
    app.button("➕ Plus", on_click=lambda: [count.set(count.value + 1), app.balloons()])

with col2:
    app.button("➖ Minus", on_click=lambda: count.set(count.value - 1))

# Real-time reactive metric
app.metric("Current Count", count)

app.run()
```

### 3. Run

Run in web browser mode or desktop app mode.

```bash
# Run in Web Browser (Default: WebSocket Mode)
python hello.py

# Run in Lite Mode (For handling massive traffic)
python hello.py --mode lite

# 🖥️ Desktop App Mode (Highly Recommended!)
python hello.py --native --splash
```

---

## 📊 Streamlit API Support Matrix

Violit supports most major Streamlit APIs, improving some structures for better performance.

### 1. Text & Media Elements
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.write` | `app.write` | ✅ | 100% Compatible (Signal/State auto-detect) |
| `st.markdown` | `app.markdown` | ✅ | Markdown syntax supported |
| `st.title`, `st.header` | `app.title`, `app.header` | ✅ | Gradient effects auto-applied |
| `st.subheader`, `st.caption` | `app.subheader`, `app.caption` | ✅ | |
| `st.code` | `app.code` | ✅ | Syntax Highlighting supported |
| `st.text` | `app.text` | ✅ | |
| `st.latex` | `app.latex` | ❌ | Recommend using Markdown math `$..$` |
| `st.divider` | `app.divider` | ✅ | |
| `st.image` | `app.image` | ✅ | URL, Local File, NumPy, PIL supported |
| `st.audio`, `st.video` | `app.audio`, `app.video` | ✅ | |

### 2. Data & Charts
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.dataframe` | `app.dataframe` | ✅ | **Ag-Grid Native** (High Performance) |
| `st.table` | `app.table` | ✅ | |
| `st.metric` | `app.metric` | ✅ | Supports `delta` and auto-color |
| `st.json` | `app.json` | ✅ | |
| `st.data_editor` | `app.data_editor` | ✅ | Simplified version provided |
| `st.plotly_chart` | `app.plotly_chart` | ✅ | Full Plotly compatibility |
| `st.pyplot` | `app.pyplot` | ✅ | Matplotlib supported |
| `st.line/bar/area_chart` | `app.line_chart` etc. | ✅ | |
| `st.scatter_chart` | `app.scatter_chart` | ✅ | |
| `st.map` | `app.map` | ❌ | Recommend Mapbox via `plotly_chart` |

### 3. Input Widgets
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.button` | `app.button` | ✅ | `key` not needed, `on_click` recommended |
| `st.download_button` | `app.download_button` | ✅ | |
| `st.link_button` | `app.link_button` | ✅ | |
| `st.text_input` | `app.text_input` | ✅ | |
| `st.number_input` | `app.number_input` | ✅ | |
| `st.text_area` | `app.text_area` | ✅ | |
| `st.checkbox`, `st.toggle` | `app.checkbox`, `app.toggle` | ✅ | |
| `st.radio` | `app.radio` | ✅ | |
| `st.selectbox` | `app.selectbox` | ✅ | |
| `st.multiselect` | `app.multiselect` | ✅ | |
| `st.slider` | `app.slider` | ✅ | |
| `st.date/time_input` | `app.date_input` etc. | ✅ | |
| `st.file_uploader` | `app.file_uploader` | ✅ | |
| `st.color_picker` | `app.color_picker` | ✅ | |
| `st.camera_input` | `app.camera_input` | ❌ | Not supported |

### 4. Layout & Containers
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.columns` | `app.columns` | ✅ | List ratios supported (e.g., `[1, 2, 1]`) |
| `st.container` | `app.container` | ✅ | |
| `st.expander` | `app.expander` | ✅ | |
| `st.tabs` | `app.tabs` | ✅ | |
| `st.empty` | `app.empty` | ✅ | For dynamic updates |
| `st.sidebar` | `app.sidebar` | ✅ | Use `with app.sidebar:` syntax |
| `st.dialog` | `app.dialog` | ✅ | Modal Decorator supported |
| `st.popover` | `app.popover` | ❌ | Recommend using `app.dialog` |

### 5. Chat & Status
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.chat_message` | `app.chat_message` | ✅ | Avatar supported |
| `st.chat_input` | `app.chat_input` | ✅ | |
| `st.status` | `app.status` | ✅ | |
| `st.spinner` | `app.spinner` | ✅ | |
| `st.progress` | `app.progress` | ✅ | |
| `st.toast` | `app.toast` | ✅ | |
| `st.balloons`, `st.snow` | `app.balloons` etc. | ✅ | |
| `st.success/error/warning` | `app.success` etc. | ✅ | |

### 6. Control Flow (Removed)
| Streamlit | Violit Approach | Note |
|---|---|---|
| `st.rerun` | **Unnecessary** | Instant partial update on State change (Zero Rerun) |
| `st.stop` | **Unnecessary** | Handle with Python flow control (`return`, etc.) |
| `st.form` | `app.form` | ✅ Supported (For batch input) |

---

## 🔌 Third-Party Library Support

Violit is absorbing the features of popular Streamlit third-party libraries **natively**.

| Library | Violit Status | Description |
|---|---|---|
| **streamlit-aggrid** | ✅ **Native** | `app.dataframe` natively uses high-performance AG-Grid. No separate install needed. |
| **Plotly** | ✅ **Native** | Perfectly supported via `app.plotly_chart`. |
| **streamlit-lottie** | ❌ **Planned** | Currently unsupported (Will add `app.lottie`). |
| **streamlit-option-menu** | ✅ **Native** | Built-in Sidebar perfectly replaces Multi-page Navigation. |
| **streamlit-extras** | ⚠️ **Partial** | Some design elements like Metric Cards can be replaced with Violit's theme system. |
| **streamlit-webrtc** | ⚠️ **Planned** | Planned support via WebSocket-based real-time communication. |

### 🎁 Violit Exclusive Features

Unique features found only in Violit, not in Streamlit:
- **Broadcasting API**: Real-time multi-user synchronization (`app.broadcaster`)
- **Card List**: Auto-managed dynamic list UI (`app.card_list`)
- **Desktop Mode**: Instant desktop app via `--native` flag
- **Hot Reload**: Auto-refresh on code change (Dev mode)
- **Animation Modes**: Smooth page transitions (`animation_mode='soft'`)

---

## 🛠️ Tech Stack

Violit combines modern web technologies with the power of Python.

* **Backend**: FastAPI (Async Python) - High-performance async processing
* **Frontend**: Web Components (Shoelace) - Modern UI components
* **Protocol**: WebSocket (default) & HTTP/HTMX (lite mode) - Hybrid choice
* **State**: Signal-based Reactivity - Solid.js style fine-grained reactivity
* **Charts**: Plotly.js - Interactive charts
* **Data Grid**: AG-Grid - Enterprise-grade data tables
* **Desktop**: pywebview - Lightweight desktop apps without Electron

### 📦 Zero Dependencies Bloat

Unlike other frameworks, Violit:
- ❌ No Node.js required (Unlike Reflex)
- ❌ No React/Vue build required (Pure Web Components)
- ❌ No complex compilation steps
- ✅ Just Python and pip!

---

## 📂 Project Structure

```bash
.
├── demo_*.py          # Various demo applications
├── violit/            # Framework source code
│   ├── app.py         # Main App class & entry point
│   ├── broadcast.py   # Real-time WebSocket broadcasting
│   ├── state.py       # Reactive State engine
│   ├── theme.py       # Theme management
│   ├── assets/        # Built-in static files
│   └── widgets/       # Widget implementations
│       ├── input_widgets.py
│       ├── data_widgets.py
│       ├── layout_widgets.py
│       └── ...
└── requirements.txt   # Dependencies
```

---

## 🤝 Contributing

**Violit** is an open-source project. Let's build the future of faster, more beautiful Python UI together.

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📝 License

MIT License

---



<p align="center">
<strong>Made with 💜 by the Violit Team</strong>
<br>
<em>Faster than Light, Beautiful as Violet.</em>
</p>
