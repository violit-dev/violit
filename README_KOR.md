<p align="center">
  <img src="./assets/violit_glare_small.png" alt="Violit™ Logo" width=50%>
</p>

# 💜 Violit

> **"Faster than Light, Beautiful as Violet."**
> **Streamlit의 직관성 × React의 퍼포먼스**

**Violit(바이올릿)** 은 Streamlit의 **전체 스크립트 재실행(Full Script Rerun)** 구조와 달리, **Fine-Grained State Architecture**를 채택하여 즉각적인 반응성을 제공하는 차세대 Python 웹 프레임워크입니다.

가장 우아한 문법으로, 빛의 속도로 반응하는 애플리케이션을 만드세요.

<p align="center">
<img src="https://img.shields.io/pypi/v/violit?color=blueviolet&style=flat-square&ignore=cache" alt="PyPI">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python 3.10+">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
<img src="https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square" alt="FastAPI">
<img src="https://img.shields.io/badge/UI-Web%20Awesome-0F766E.svg?style=flat-square" alt="Web Awesome">
</p>

---

## 📸 Demo

*Violit으로 제작된 대시보드가 실시간으로 작동하는 모습입니다.*

<p align="center">
  <img src="./assets/demo_show_main_small.gif" alt="Violit Showcase Demo" width=50%>
</p>

---

## ⚡ Why Violit?

### Architectural Differences

Violit과 Streamlit은 Python 코드로 UI를 만든다는 점은 같지만, 내부 작동 원리는 근본적으로 다릅니다.

| Feature | Streamlit (Traditional) | **Violit (Reactive)** |
| --- | --- | --- |
| **Execution Model** | **Full Script Rerun**<br>사용자 상호작용마다 전체 스크립트를 재실행합니다. | **Fine-Grained Updates**<br>변경된 State에 연결된 컴포넌트만 정확히 업데이트합니다. |
| **Performance** | 데이터 양이 늘어나면 반응 속도가 저하될 수 있습니다. | 데이터 규모와 상관없이 일관된 반응성을 유지합니다. |
| **Optimization** | `@cache`, `@fragment`와 같은 최적화 데코레이터가 필요합니다. | 별도의 최적화 코드 없이도 설계상 최적화되어 있습니다. |
| **Deployment** | 웹 브라우저 실행에 최적화되어 있습니다. | 웹 브라우저 및 **Desktop Native App** 모드를 모두 지원합니다. |
| **Design** | 기본 UI 제공에 집중합니다. | **20+ 전문가급 테마**를 통해 즉시 사용 가능한 디자인을 제공합니다. |

### Key Features

1.  **Optimization by Design (Streamlit-Like Syntax, No Complexity)**:
    Streamlit의 직관적인 문법은 그대로 유지하면서, 복잡한 최적화 도구를 아키텍처 단계에서 제거했습니다.
    *   ❌ **No `@cache_data`, `@fragment`, `st.rerun`**: Fine-Grained 구조 덕분에 수동 최적화가 필요 없습니다.
    *   ❌ **No `key` Management**: 위젯 상태 관리를 위해 고유 키를 일일이 지정할 필요가 없습니다.
    *   ❌ **No Complex Callbacks**: Dash나 Panel처럼 복잡한 콜백/클래스를 정의할 필요가 없습니다.

2.  **Ultra-Fast Speed**: 슬라이더를 0.1초 단위로 움직여도 차트가 끊김 없이 실시간으로 반응합니다.

3.  **Hybrid Runtime**:
    *   **WebSocket Mode**: 초저지연 양방향 통신 (기본값)
    *   **Lite Mode**: HTTP 기반, 대규모 동시 접속 처리에 유리

4.  **Desktop Mode**: `--native` 옵션으로 Electron 없이 완벽한 데스크탑 애플리케이션으로 실행 가능합니다.

---

## 🎨 Theme Gallery

CSS를 전혀 몰라도 됩니다. Violit은 20가지 이상의 테마를 제공합니다. (곧 사용자가 쉽게 원하는 Cutomized Theme를 추가할 수 있습니다.)

*테마 데모는 곧 업데이트될 예정입니다.*

![Theme Gallery Grid](PLACEHOLDER_FOR_THEME_GALLERY_GRID)

```python
# 초기화 시 설정
app = vl.App(theme='cyberpunk')

# 런타임 변경
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

기존 Full Rerun 방식 대비 Violit의 Fine-Grained 업데이트 방식이 얼마나 효율적인지 보여주는 벤치마크 결과입니다.



*벤치마크 상세 데이터는 곧 업데이트될 예정입니다.*

![Benchmark Chart](PLACEHOLDER_FOR_BENCHMARK_CHART)


---

## 🚀 Comparison

### Python UI Frameworks

| 프레임워크 | 아키텍처 | 러닝 커브 | 퍼포먼스 | Desktop 앱 | 실시간 기능 |
|-----------|---------|----------|---------|------------|------------|
| **Streamlit** | Full Rerun | 매우 쉬움 | 느림 | ❌ | △ |
| **Dash** | Callback | 보통 | 빠름 | ❌ | △ |
| **Panel** | Param | 어려움 | 빠름 | ❌ | ✅ |
| **Reflex** | React (Compile) | 어려움 | 빠름 | ❌ | ✅ |
| **NiceGUI** | Vue | 쉬움 | 빠름 | ✅ | ✅ |
| **Violit** | **Signal** | **매우 쉬움** | **빠름** | **✅** | **✅** |

### Code Comparison

#### **1. vs Streamlit** (Rerun vs Signal)
*Streamlit은 버튼 클릭 시 **전체 스크립트**를 다시 실행하지만, Violit은 **해당 함수**만 실행합니다.*

```python
# Streamlit
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("클릭"):
    st.session_state.count += 1 # Rerun triggers here

st.write(st.session_state.count)
```

```python
# Violit
import violit as vl
app = vl.App()

count = app.state(0)

# 클릭 시 count만 업데이트 (No Rerun)
app.button("클릭", on_click=lambda: count.set(count.value + 1))
app.write(count) 
```

#### **2. vs Dash** (Callback Hell vs Auto-Reactivity)
*Dash는 Input/Output을 연결하는 복잡한 **Callback**이 필요하지만, Violit은 **State** 하나로 충분합니다.*

```python
# Dash
from dash import Dash, html, Input, Output, callback

app = Dash(__name__)
app.layout = html.Div([
    html.Button("클릭", id="btn"),
    html.Div(id="out")
])

@callback(Output("out", "children"), Input("btn", "n_clicks"))
def update(n):
    return f"값: {n}" if n else "값: 0"
```

```python
# Violit
count = app.state(0)

app.button("클릭", on_click=lambda: count.set(count.value + 1))
# State 의존성 자동 추적 -> Callback 불필요
app.write(lambda: f"값: {count.value}")
```

#### **3. vs NiceGUI** (Binding vs Direct State)
*NiceGUI도 훌륭하지만, Violit은 Streamlit 스타일의 **더 간결한 문법**을 제공합니다.*

```python
# NiceGUI
from nicegui import ui

count = {'val': 0}
ui.button('클릭', on_click=lambda: count.update(val=count['val'] + 1))
ui.label().bind_text_from(count, 'val', backward=lambda x: f'값: {x}')
```

```python
# Violit
count = app.state(0)
app.button('클릭', on_click=lambda: count.set(count.value + 1))
app.write(count) # .bind_text 등 복잡한 연결 불필요
```

#### **4. vs Reflex** (Class & Compile vs Pure Python)
*Reflex는 State **클래스 정의**와 **컴파일** 과정이 필요하지만, Violit은 **순수 파이썬** 스크립트입니다.*

```python
# Reflex
import reflex as rx

class State(rx.State):
    count: int = 0
    def increment(self):
        self.count += 1

def index():
    return rx.vstack(
        rx.button("클릭", on_click=State.increment),
        rx.text(State.count)
    )
```

```python
# Violit
# 클래스 정의 불필요, 컴파일 불필요
count = app.state(0)
app.button("클릭", on_click=lambda: count.set(count.value + 1))
app.write(count)
```

---

## 🚀 Quick Start

### 1. 설치

Python 3.10 이상 환경에서 설치할 수 있습니다.

```bash
pip install violit

# 또는 개발 버전
pip install git+https://github.com/violit-dev/violit.git
```


### 2. Hello, Violit!

`hello.py` 파일을 작성합니다.

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

### 3. 실행

```bash
# 기본 실행 (WebSocket Mode)
python hello.py

# 데스크탑 앱 모드 (권장)
python hello.py --native

# 포트 설정
python hello.py --port 8020
```

---

## 📚 Widget Support

Violit은 Streamlit의 핵심 위젯을 지원하며, 일부 기능은 더 효율적인 방식으로 재설계되었습니다.

상세한 호환성 목록과 지원되지 않는 위젯에 대한 정보는 [위젯 지원 현황 (Streamlit API Support Matrix)](./doc/Streamlit API Support Matrix.md) 문서를 참고해주세요.

---

## 🛠️ Tech Stack

*   **Backend**: FastAPI (Async Python)
*   **Frontend**: Web Components (Web Awesome), Plotly.js, AG-Grid
*   **Protocol**: WebSocket & HTTP/HTMX Hybrid
*   **State**: Signal-based Reactivity

---

## 🗺️ Roadmap

Violit은 지속적으로 발전하고 있습니다.

*   ✅ **Core**: Signal State Engine, Theme System
*   ✅ **Widgets**: Plotly, Dataframe, Input Widgets
*   ✅ **Homepage**: 공식 홈페이지 Open 
*   ✅ **Documentation**: 공식 기술 문서 및 API 레퍼런스 업데이트 
*   ⏳ **Custom Components**: User-defined Custom Component 지원 
*   ⏳ **Custom Theme**: User-defined Custom Theme지원 
*   ⏳ **async**: async 처리 지원 
*   ⏳ **More examples**: 더 많은 실제 사용가능한 example code 제공 
*   ⏳ **Violit.Cloud**: 클라우드 환경 배포 서비스
*   ⏳ **Expansion**: 더 많은 서드파티 라이브러리 통합

---

## 📂 Project Structure

```bash
.
├── violit/            # 프레임워크 소스 코드
│   ├── app.py         # 메인 App 클래스 및 진입점
│   ├── broadcast.py   # 실시간 WebSocket 브로드캐스팅
│   ├── state.py       # 반응형 State 엔진
│   ├── theme.py       # 테마 관리
│   ├── assets/        # 내장 정적 파일
│   └── widgets/       # 위젯 구현체
│       ├── input_widgets.py
│       ├── data_widgets.py
│       ├── layout_widgets.py
│       └── ...
└── requirements.txt   # 의존성 목록
```

---

## 🤝 Contributing

**Violit**은 오픈소스 프로젝트입니다. 더 빠르고 아름다운 파이썬 UI의 미래를 함께 만들어가요.

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
