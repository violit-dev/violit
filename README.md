![Violit Logo](https://github.com/user-attachments/assets/f6a56e37-37a5-437c-ae16-13bff7029797)

🎉 **Featured on OpenSourceProjects.dev**: ["Stop Overcomplicating Your Data Dashboards"](https://www.opensourceprojects.dev/post/634ad562-83d4-4a7b-8a74-b61e47ad68aa)

> **"Faster than Light, Beautiful as Violet."** **Structure of Streamlit × Performance of React.**

**Violit** is a Python web framework built on a **fine-grained reactive architecture**. It preserves the highly productive, top-down Python authoring style loved by the Streamlit community, but eliminates the performance bottlenecks of the **full script rerun** model.

It starts naturally from data apps and dashboards, but is not limited to them. With built-in ORM/Auth support and Tailwind-style design primitives, Violit also scales well to more general web applications such as admin tools, internal platforms, CRUD systems, and user-facing product UIs.

<p align="center">
<img src="https://img.shields.io/pypi/v/violit?color=blueviolet&style=flat-square&ignore=cache" alt="PyPI">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python 3.10+">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
<img src="https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square" alt="FastAPI">
<img src="https://img.shields.io/badge/UI-Web%20Awesome-0F766E.svg?style=flat-square" alt="Web Awesome">
<img src="https://img.shields.io/github/stars/violit-dev/violit?style=flat-square&color=f59e0b" alt="Github Stars">
</p>

```bash
pip install violit
```

- **Docs:** <https://doc.violit.cloud>
- **PyPI:** <https://pypi.org/project/violit/>
- **GitHub:** <https://github.com/violit-dev/violit>

## Demo

This demo illustrates the kind of interaction Violit was built for: Python-first UI code with reactive updates that remain snappy and smooth, even as the interface grows more complex.

<p align="center">
[demo_violit_showcase.webm](https://github.com/user-attachments/assets/962fa0e5-c98b-443d-9d35-76e62ccb819f)
</p>

## Why Violit?

Violit is designed for developers who love the immediate productivity of Streamlit but need an architecture that scales gracefully as their applications evolve from tiny dashboards to feature-rich web apps.

- **Streamlit-like Python flow**, but completely free from full script reruns.
- **Fine-grained state updates** ensuring only the dependent widgets update (React-like reactivity).
- **Built-in ORM** ready to use with `vl.App(db=...)`.
- **Tailwind-like styling** via the `cls` parameter.
- **Async friendly** with built-in `app.background(...)` and `app.interval(...)`.
- **Flexible Runtimes**: Runs in the Browser, HTMX Lite mode for higher concurrency, and as Desktop Native apps.
- **Rich ecosystem**: Out-of-the-box support for powerful widgets, themes, and animations.

## Architectural Difference

The fundamental difference lies not just in syntax, but in how the framework handles the DOM after a user interacts (clicks, types, or drags).

| Topic | Streamlit | Violit |
| :--- | :--- | :--- |
| **Update Model** | Full script rerun | Fine-grained reactive updates |
| **Interaction Cost** | The entire script may re-execute | Only explicitly dependent UI components update |
| **Optimization Burden** | Often requires workarounds for rerun constraints | Naturally handled by the signal-based architecture |
| **App Growth Path** | Ideal for quick, simple data views | Designed to scale into richer, stateful app flows |
| **Runtime Modes** | Browser-focused | WebSocket, Lite, Desktop Native |
| **Styling** | Basic theming | Themes + Tailwind-like utility styling |

## Framework Comparison (Feature Matrix)

Every Python UI framework has its own unique philosophy and strengths. This matrix compares the structural capabilities of popular frameworks to help you choose the right tool for your specific use case.

| Framework | No Full Rerun | Pure Python (Zero JS/HTML) | SEO / SSR Ready | Desktop Native (exe/app) |
| :--- | :---: | :---: | :---: | :---: |
| **Streamlit** | ❌ | ✅ | ❌ | ❌ |
| **Dash / Panel** | ✅<br />*(Callbacks)* | ✅ | ❌ | ❌ |
| **NiceGUI** | ✅ | ✅ | ❌ | ✅ |
| **Reflex** | ✅ | ⚠️<br />*(React paradigm)* | ✅ | ❌ |
| **RIO** | ✅<br />*(React-like)* | ✅ | ❌ | ✅<br />*(Local mode)* |
| **Violit** | ✅<br />**(Signals)** | ✅ | ✅ | ✅<br />**(Built-in pywebview)** |

### What This Matrix Means

- **Streamlit** remains the easiest starting point for data scientists, but its full-rerun model can become a bottleneck as interaction complexity grows.
- **Dash & Panel** are robust data tools but often require adopting specific callback structures.
- **NiceGUI** is highly practical and productive, adopting a more object-oriented UI binding style.
- **Reflex** is incredibly powerful and compiles to a React frontend, but introduces a steeper learning curve for developers unfamiliar with React concepts.
- **RIO** is a modern, reactive framework inspired by React and Flutter, offering great component structures, though it requires adopting an opinionated class-based architecture.
- **Violit** aims for the sweet spot: providing the **familiar, script-like readability of Streamlit**, while internally leveraging a **modern, fine-grained reactive engine** and offering built-in full-stack features (ORM, Auth, Desktop compilation).

## Syntax Comparison

The snippets below are intentionally minimal. The goal is to highlight how much structural boilerplate each framework requires to express the exact same tiny interaction.

### Streamlit

```python
import streamlit as st

name = st.text_input("Name", "Violit")
st.write(f"Hello, {name}")
```

- **The Vibe:** Extremely direct and beginner-friendly.
- **The Trade-off:** As the app grows, you find yourself constantly architecting around the full-rerun behavior.

### NiceGUI

```python
from nicegui import ui

name = ui.input("Name", value="Violit")
ui.label().bind_text_from(name, "value", lambda v: f"Hello, {v}")

ui.run()
```

- **The Vibe:** Explicit UI object binding. Excellent for component-driven design.
- **The Trade-off:** Shifts away from the declarative, top-down reading flow that data professionals prefer.

### Reflex

```python
import reflex as rx

class State(rx.State):
    name: str = "Violit"

def app():
    return rx.vstack(
        rx.input(value=State.name, on_change=State.set_name),
        rx.text(State.name),
    )
```

- **The Vibe:** A robust, React-flavored state model.
- **The Trade-off:** Requires defining separate state classes, which can feel heavy for small to medium interactive apps.

### RIO

```python
import rio

class Page(rio.Component):
    name: str = "Violit"

    def build(self) -> rio.Component:
        return rio.Column(
            rio.TextInput("Name", text=self.bind().name),
            rio.Text(f"Hello, {self.name}"),
        )
```

- **The Vibe:** Component-based and reactive, heavily inspired by React and Flutter.
- **The Trade-off:** The class-based component structure is powerful but can feel opinionated and heavier compared to a simple procedural script.

### Violit Syntax

```python
import violit as vl

app = vl.App()

name = app.text_input("Name", value="Violit")
app.text(lambda: f"Hello, {name.value}")

app.run()
```

- **The Vibe:** The top-down simplicity of Streamlit, powered by the reactive performance of modern JS frameworks.
- **The Advantage:** The syntax remains lightweight, but the runtime updates only the necessary DOM nodes seamlessly.

## Quick Start

Experience the core Violit philosophy: declare state, bind widgets, and let the runtime update only what's necessary.

```python
import violit as vl

app = vl.App(title="Hello Violit", theme="violit_light_jewel")

count = app.state(0)
name = app.text_input("Project name", value="Violit")

app.title("Build apps in pure Python")
app.text(lambda: f"Hello, {name.value}")
app.metric("Clicks", count)
app.button("+1", on_click=lambda: count.set(count.value + 1))

app.run()
```

## Very Easy ORM Example

Violit bridges the gap between a quick prototype and a production-ready application by offering built-in persistence.

```python
import violit as vl
from sqlmodel import SQLModel, Field
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

app = vl.App(db="./todo.db")

app.db.add(Todo(title="Ship first Violit app"))
items = app.db.all(Todo)

app.title("Todo List")
app.text(lambda: f"Total items: {len(items)}")

app.run()
```

## Background Work

This is where Violit truly separates itself from simple dashboard tools. You can model long-running tasks directly in your Python code without freezing the user interface.

```python
import time
import violit as vl

app = vl.App()
progress = app.state(0)

def work():
    for step in range(1, 6):
        time.sleep(0.3)
        progress.set(step * 20)

task = app.background(work)

app.button("Run task", on_click=task.start)
app.progress(progress)

app.run()
```

*Tip: If you need periodic polling or refreshing, `app.interval(...)` is also natively supported.*

## Styling

Violit keeps UI customization practical and fast. You can use utility classes without dropping out of Python for every minor CSS adjustment.

```python
app.button(
    "Deploy",
    cls="rounded-full bg-sky-500 px-6 py-3 text-white shadow-lg hover:bg-sky-600",
)
```

## Tech Stack

Under the hood, Violit utilizes a pragmatic, modern stack focused on performance and interactivity.

- **Backend:** FastAPI, Uvicorn
- **Reactivity:** WebSocket runtime, HTMX-based Lite mode
- **Data & DB:** SQLModel + Alembic, pandas, numpy
- **Visualization:** Vega-Lite, Plotly integration
- **Desktop:** pywebview for native executables
- **Assets:** Local bundled assets for offline-friendly deployments

## Roadmap

Violit is evolving rapidly. The core reactive foundation is solid, and several full-stack features are already implemented. Our next steps focus on ecosystem expansion and customization.

- ✅ **Core**: Signal State Engine, Theme System
- ✅ **Widgets**: Plotly, Dataframe, Input Widgets
- ✅ **ORM**: Built-in ORM support with SQLModel and migrations
- ✅ **Auth**: Built-in authentication flow and page protection
- ✅ **Styling**: Tailwind-like utility styling support
- ✅ **Homepage**: Official Website launched
- ✅ **Documentation**: Technical Documentation and API Reference
- ⏳ **Custom Components**: User-defined Custom Component APIs
- ⏳ **Custom Theme**: Advanced theming support
- ⏳ **Examples**: More real-world, production-grade templates
- ⏳ **Violit.Cloud**: One-click cloud deployment service
- ⏳ **Expansion**: Deeper integration with third-party libraries

## Installation

Getting started is as simple as installing the package. The Violit CLI is automatically included.

```bash
pip install violit
# Or to get the latest bleeding-edge version:
pip install git+https://github.com/violit-dev/violit.git
```

## Running Your App

Violit ships with a powerful CLI. The recommended way to run your apps is via `violit run`.

`violit run` forwards the same runtime flags that `app.run()` accepts. If a command works with `python app.py ...`, the same flags work with `violit run app.py ...`.

`--lite` runs the app in HTMX-based HTTP mode instead of the default WebSocket runtime. This is often the better choice when you want to handle more concurrent users or deploy in environments where WebSockets are limited.

```bash
python app.py --reload --localhost
violit run app.py --reload --localhost

violit run app.py --help       # Show runtime flags accepted by app.run()
violit run app.py --reload     # Auto-reload on code changes
violit run app.py --localhost  # Bind to 127.0.0.1 and print localhost URL
violit run app.py --native     # Launch as a Desktop App
violit run app.py --lite       # Run in HTMX-based lite mode for higher concurrency
violit run app.py --port 8020
violit run app.py --make-migration "add_users"
```

You can also scaffold a new project instantly:

```bash
violit create my_app
cd my_app
violit run main.py --reload
```

## Documentation & Resources

Ready to dive deeper? Check out our official guides depending on your needs:

- **Live Docs:** <https://doc.violit.cloud>
- **Streamlit Migration:** [Streamlit API Support Matrix](doc/Streamlit%20API%20Support%20Matrix.md)
- **AI Coding Context:** [llms.txt](doc/llms.txt)

## 📝 License

Violit is released under the **MIT License**.

*Trademark Note: The open-source license applies to the code, while "Violit™" remains a trademark of The Violit Team to ensure clear project identity.*
