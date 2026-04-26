# Streamlit API Support Matrix

Violit covers most of the Streamlit surface people actually use, but the relationship is not one-to-one.
Some APIs map directly, some are intentionally unnecessary because Violit does not rerun the full script, and some areas are extended beyond Streamlit with Violit-only features such as built-in ORM, auth, background jobs, interval timers, and Tailwind-first styling.

## Quick Read

| Meaning | Status |
| --- | --- |
| Directly supported | ✅ |
| Supported, but with Violit-specific behavior | ⚠️ |
| No direct equivalent or not supported | ❌ |

## 1. Text, Markdown, and Media

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.write` | `app.write` | ✅ | Type-aware output with reactive `State` handling |
| `st.markdown` | `app.markdown` | ✅ | Markdown plus optional HTML |
| `st.title` | `app.title` | ✅ | |
| `st.header` | `app.header` | ✅ | |
| `st.subheader` | `app.subheader` | ✅ | |
| `st.caption` | `app.caption` | ✅ | |
| `st.text` | `app.text` | ✅ | Reactive when passed `State` or lambda |
| `st.code` | `app.code` | ✅ | Supports showcase mode, copy button, line numbers |
| `st.latex` | `app.latex` | ✅ | KaTeX-backed rendering |
| `st.divider` | `app.divider` | ✅ | |
| `st.image` | `app.image` | ✅ | URL, local path, PIL, NumPy |
| `st.audio` | `app.audio` | ✅ | |
| `st.video` | `app.video` | ✅ | |

## 2. Data and Charts

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.dataframe` | `app.dataframe` | ✅ | AG Grid based interactive table |
| `st.table` | `app.table` | ✅ | Static table |
| `st.data_editor` | `app.data_editor` | ✅ | Editable grid surface |
| `st.metric` | `app.metric` | ✅ | Works well with `State` |
| `st.json` | `app.json` | ✅ | JSON tree viewer |
| `st.plotly_chart` | `app.plotly_chart` | ✅ | |
| `st.pyplot` | `app.pyplot` | ✅ | |
| `st.line_chart` | `app.line_chart` | ✅ | |
| `st.bar_chart` | `app.bar_chart` | ✅ | |
| `st.area_chart` | `app.area_chart` | ✅ | |
| `st.scatter_chart` | `app.scatter_chart` | ✅ | |
| `st.map` | — | ❌ | Use Plotly or custom map components instead |

## 3. Inputs and Actions

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.button` | `app.button` | ⚠️ | Use `on_click=`. Buttons do not return booleans |
| `st.download_button` | `app.download_button` | ✅ | |
| `st.link_button` | `app.link_button` | ✅ | |
| `st.text_input` | `app.text_input` | ⚠️ | Returns `State`, not a raw value |
| `st.text_area` | `app.text_area` | ⚠️ | Returns `State` |
| `st.number_input` | `app.number_input` | ⚠️ | Returns `State` |
| `st.slider` | `app.slider` | ⚠️ | Returns `State`; supports `live_update` |
| `st.select_slider` | `app.select_slider` | ✅ | |
| `st.checkbox` | `app.checkbox` | ⚠️ | Returns `State[bool]` |
| `st.toggle` | `app.toggle` | ⚠️ | Returns `State[bool]` |
| `st.radio` | `app.radio` | ⚠️ | Returns `State` |
| `st.selectbox` | `app.selectbox` | ⚠️ | Returns `State` |
| `st.multiselect` | `app.multiselect` | ⚠️ | Returns `State[list]` |
| `st.date_input` | `app.date_input` | ⚠️ | Returns `State` |
| `st.time_input` | `app.time_input` | ⚠️ | Returns `State` |
| `st.file_uploader` | `app.file_uploader` | ⚠️ | Returns `State` |
| `st.color_picker` | `app.color_picker` | ⚠️ | Returns `State` |
| `st.camera_input` | — | ❌ | No built-in equivalent |
| — | `app.datetime_input` | Violit-only | Date + time input |

## 4. Layout and Containers

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.columns` | `app.columns` | ✅ | Integer or ratio list |
| `st.container` | `app.container` | ✅ | |
| `st.expander` | `app.expander` | ✅ | |
| `st.tabs` | `app.tabs` | ✅ | |
| `st.empty` | `app.empty` | ✅ | Useful for dynamic replacement |
| `st.sidebar` | `app.sidebar` | ✅ | Proxy or context-manager style |
| `st.dialog` | `app.dialog` | ✅ | Decorator-based modal |
| `st.popover` | `app.popover` | ✅ | Available in current Violit |
| `st.form` | `app.form` | ✅ | Batch submit workflow |
| `st.form_submit_button` | `app.form_submit_button` | ✅ | |

## 5. Chat and Status

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.chat_message` | `app.chat_message` | ✅ | |
| `st.chat_input` | `app.chat_input` | ✅ | |
| `st.status` | `app.status` | ✅ | |
| `st.spinner` | `app.spinner` | ✅ | |
| `st.progress` | `app.progress` | ✅ | Can consume `State` |
| `st.toast` | `app.toast` | ✅ | |
| `st.success` | `app.success` | ✅ | |
| `st.info` | `app.info` | ✅ | |
| `st.warning` | `app.warning` | ✅ | |
| `st.error` | `app.error` | ✅ | |
| `st.balloons` | `app.balloons` | ✅ | |
| `st.snow` | `app.snow` | ✅ | |

## 6. Control Flow and Execution Model

| Streamlit | Violit | Status | Notes |
| --- | --- | --- | --- |
| `st.rerun` | Usually unnecessary | ⚠️ | Violit updates dependent widgets immediately after `State` changes |
| `st.stop` | Python control flow | ⚠️ | Use `return`, branching, or page logic |
| Python `if` / `for` with rerun expectations | `app.If()` / `app.For()` | ⚠️ | Use these for reactive conditional or iterative rendering |

## 7. Violit-Only Features With No Real Streamlit Equivalent

| Violit feature | API | Why it matters |
| --- | --- | --- |
| Built-in ORM | `vl.App(db=..., migrate=...)`, `app.db.*` | Database-backed apps without bolting on a separate stack |
| Built-in auth | `app.setup_auth(User)`, `app.auth.*` | Session auth, password hashing, role-based page protection |
| Background jobs | `app.background(...)` | Long-running work without blocking the UI |
| Interval timers | `app.interval(...)` | Polling, live dashboards, scheduled callbacks |
| Tailwind-first styling | `cls`, `configure_widget()`, `add_css()`, `part_cls` | Much broader styling control than Streamlit |
| Native desktop mode | `python app.py --native` | Desktop window without Electron |

## Migration Notes For Streamlit Users

- Replace `st.session_state` patterns with `app.state()`.
- Do not write `if app.button(...):`.
- Expect most input widgets to return `State`, not the raw value.
- Pass `State` objects directly to widgets for reactivity.
- Use `lambda:` when formatting `state.value` inside strings.
- Treat Violit as a broader app framework, not only as a Streamlit clone.
