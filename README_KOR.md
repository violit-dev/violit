<p align="center">
  <img src="./assets/violit_glare_small.png" alt="violit icon">
</p>

# 💜 Violit

> **"Faster than Light, Beautiful as Violet."**
> **Streamlit의 직관성 × React의 퍼포먼스**

**Violit(바이올릿)** 은 Streamlit의 치명적인 단점인 **전체 스크립트 재실행(Full Script Rerun)** 문제를 **O(1) State Architecture**로 완벽하게 해결한 차세대 Python 웹 프레임워크입니다.

가장 우아한 문법으로, 빛의 속도로 반응하는 애플리케이션을 만드세요.

<p align="center">
<img src="https://img.shields.io/pypi/v/violit?color=blueviolet&style=flat-square&ignore=cache" alt="PyPI">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python 3.10+">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
<img src="https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square" alt="FastAPI">
<img src="https://img.shields.io/badge/UI-Shoelace-7C4DFF.svg?style=flat-square" alt="Shoelace">
</p>

---

## ⚡ Why Violit?

### 🎯 Streamlit의 한계를 넘어서다

Violit은 단순히 "빠른 Streamlit"이 아닙니다. **아키텍처 자체가 다릅니다.**

| Feature | Streamlit 🐢 | **Violit 💜** |
| --- | --- | --- |
| **Architecture** | **Full Rerun (O(N))**<br><br>버튼 하나만 눌러도 전체 코드 재실행 | **Zero Rerun (O(1))** ⚡<br><br>변경된 컴포넌트만 정확히 업데이트 |
| **UX/UI** | 반응 느림, 화면 깜빡임 발생 | **React급 반응성**, 깜빡임 없는 부드러움 |
| **Optimization** | `@cache`, `@fragment` 등 복잡한 최적화 필수 | **최적화 코드 불필요** (설계 자체가 최적화됨) |
| **Scalability** | 동시 접속자 처리 제한적 (메모리 과다) | **Lite Mode** 지원으로 대규모 트래픽 대응 🌐 |
| **Deployment** | 웹 브라우저만 지원 | 웹 + **Desktop App Mode** 💻 |
| **Design** | 투박한 기본 디자인 | **30+ 전문가급 테마** 내장 🎨 |

### ⭐ Violit만의 시그니처

1. **Ultra-Fast Speed**: 슬라이더를 0.1초 단위로 움직여도 차트가 끊김 없이 실시간으로 반응합니다.
2. **Streamlit-Like API**: 기존 Streamlit 사용자는 10분이면 적응합니다. 코드는 90% 호환됩니다.
3. **Hybrid Runtime**:
   * **WebSocket Mode**: 초저지연 양방향 통신, 실시간 브로드캐스팅 (Default) ⚡
   * **Lite Mode**: HTTP 기반, 수천 명의 동시 접속자 처리 (대규모 대시보드용)
4. **Desktop Mode**: `--native` 옵션 한 줄로 Electron 없이 완벽한 데스크탑 앱을 만듭니다.

---

## 🔥 왜 다른 프레임워크 대신 Violit인가?

### 📊 주요 Python UI 프레임워크 비교

| 프레임워크 | 아키텍처 | 러닝 커브 | 퍼포먼스 | Desktop 앱 | 실시간 기능 |
|-----------|---------|----------|---------|------------|------------|
| **Streamlit** | Full Rerun (O(N)) | ⭐⭐⭐⭐⭐ 매우 쉬움 | 🐢 느림 | ❌ | ❌ (제한적) |
| **Dash (Plotly)** | Callback 기반 | ⭐⭐⭐ 보통 | ⚡ 빠름 | ❌ | ✅ (복잡) |
| **Panel** | Param 기반 | ⭐⭐ 어려움 | ⚡ 빠름 | ❌ | ✅ |
| **NiceGUI** | Vue 기반 | ⭐⭐⭐⭐ 쉬움 | ⚡ 빠름 | ✅ | ✅ |
| **Reflex** | React 스타일 | ⭐⭐ 어려움 | ⚡ 빠름 | ❌ | ✅ |
| **Violit 💜** | **Zero Rerun (O(1))** | ⭐⭐⭐⭐⭐ **매우 쉬움** | **⚡⚡ 최고속** | **✅** | **✅ Built-in** |

### 🎯 Violit을 선택해야 하는 이유

#### 1️⃣ **vs Streamlit**: 같은 문법, 100배 빠른 속도
```python
# Streamlit처럼 쉽지만, 리렌더링 없이 즉각 반응
app.button("클릭", on_click=lambda: count.set(count.value + 1))
app.write("카운트:", count)  # State 변경 시 이 부분만 업데이트!
```
- Streamlit의 **직관적인 API**는 그대로, **Full Rerun의 고통**은 0%
- 캐싱, Fragment, Rerun 등 복잡한 최적화 불필요

#### 2️⃣ **vs Dash**: Callback 지옥 없는 반응성
```python
# Dash는 복잡한 callback 체인이 필요하지만,
# Violit은 State만 바꾸면 자동으로 모든 의존 컴포넌트 업데이트
count = app.state(0)
app.write(lambda: f"값: {count.value}")  # 자동 추적
```
- Dash의 **`@callback` 보일러플레이트 지옥** 제거
- 더 직관적인 State 기반 반응성

#### 3️⃣ **vs Panel**: 러닝 커브 없는 파워
```python
# Panel의 Param 클래스 없이 간단하게
name = app.state("World")
app.write(lambda: f"Hello, {name.value}!")
```
- Panel의 **복잡한 Param 시스템** 불필요
- Streamlit처럼 쉽지만 Panel처럼 강력

#### 4️⃣ **vs NiceGUI**: Python만으로 Desktop 앱까지
- NiceGUI처럼 **실시간 WebSocket 지원**
- 하지만 Violit은 **30+ 프리미엄 테마**와 **Desktop Mode** 추가
- Vue.js 몰라도 OK, Python만으로 충분

#### 5️⃣ **vs Reflex**: 복잡한 설정 없이 바로 시작
```python
# Reflex는 복잡한 설정과 컴파일 필요, Violit은:
import violit as vl
app = vl.App()
app.title("Hello!")
app.run()  # 끝!
```
- Reflex의 **Node.js 의존성 없음**
- **별도 빌드 스텝 불필요**, Python 파일 하나로 완성

### 💎 Violit의 독보적인 장점

1. **Zero Configuration**: `pip install violit` → 바로 시작
2. **Zero Learning Curve**: Streamlit 아시면 5분이면 끝
3. **Zero Performance Issues**: O(1) 아키텍처로 어떤 규모든 OK
4. **Desktop Mode**: `--native` 한 줄로 Desktop Mode 실행
5. **30+ Premium Themes**: 디자이너 없이도 전문가급 UI
6. **Real-time Broadcasting**: 멀티 유저 실시간 동기화 기본 제공

---

## 🐢 Streamlit vs 🏎️ Violit

### Streamlit 방식 (비효율적)

인터랙션이 발생할 때마다 **코드가 처음부터 끝까지 다시 실행**됩니다. 데이터도 매번 다시 로드합니다.

```python
import streamlit as st

# ⚠️ 버튼을 클릭할 때마다 이 무거운 함수가 계속 실행됨
df = load_huge_dataset() 

if 'count' not in st.session_state:
    st.session_state.count = 0

# ⚠️ 전체 페이지 리로딩으로 인한 깜빡임 발생
if st.button('증가'):
    st.session_state.count += 1 
    
st.write(f"카운트: {st.session_state.count}")
```

### Violit 방식 (우아함)

스크립트는 **최초 1회만 실행**됩니다. 상태(State)가 바뀌면 UI는 자동으로 반응합니다.

```python
import violit as vl

app = vl.App()

# ✅ 최초 1회만 실행! 자원 낭비 0%
df = load_huge_dataset()

# State 선언 (Signal 기반)
count = app.state(0)

# 버튼 클릭 시 count 값만 변경 -> UI 즉시 반영 (No Rerun)
app.button("증가", on_click=lambda: count.set(count.value + 1))

# ✨ State 객체를 직접 넣으면 Auto-Reactive!
app.write("카운트:", count)

app.run()
```

---

## 🧩 The "Zero Rerun" Philosophy

Violit은 개발자를 괴롭히던 **불필요한 복잡함**을 제거했습니다.

### 🚫 더 이상 필요 없는 것들

* ❌ **`@st.cache_data`**: 코드가 한 번만 실행되는데 캐싱이 왜 필요한가요?
* ❌ **`@st.fragment`**: Violit은 모든 위젯이 이미 독립적입니다.
* ❌ **`st.rerun()`**: 강제로 재실행할 필요가 없습니다. 상태만 바꾸세요.
* ❌ **`key="widget_1"`**: 위젯의 상태 보존을 위해 키를 관리할 필요가 없습니다.
* ❌ **복잡한 Callback 체인**: Dash처럼 Input/Output 연결 불필요. State가 모든걸 해결합니다.
* ❌ **Param 클래스 정의**: Panel처럼 복잡한 파라미터 클래스 작성 불필요.

### ✅ Violit의 혁신적인 접근

```python
# 1. State 기반 반응성 (Solid.js Signals 방식)
counter = app.state(0)
app.write(counter)  # counter 변경 시 자동 업데이트!

# 2. Lambda로 동적 콘텐츠
app.write(lambda: f"현재 시각: {time.time()}")  # 의존성 자동 추적

# 3. Callback으로 명확한 액션
app.button("클릭", on_click=lambda: counter.set(counter.value + 1))

```

---

## 🎨 30+ Premium Themes

CSS를 전혀 몰라도 됩니다. Violit은 디자이너가 조율한 30가지 이상의 테마를 제공합니다.

```python
# 테마는 한 줄로 변경 가능
app = vl.App(theme='cyberpunk', title='My App')

# 런타임에도 변경 가능
app.set_theme('ocean')
```

| Theme Family | Examples |
| --- | --- |
| **Dark 🌑** | `dark`, `dracula`, `monokai`, `ocean`, `forest`, `sunset` |
| **Light ☀️** | `light`, `pastel`, `retro`, `nord`, `soft_neu` |
| **Tech 🤖** | `cyberpunk`, `terminal`, `cyber_hud`, `blueprint` |
| **Professional 💼** | `editorial`, `bootstrap`, `ant`, `material`, `lg_innotek` |

**다른 프레임워크와 비교:**
- **Streamlit**: 기본 테마만 제공, 커스터마이징 복잡
- **Dash**: CSS 직접 작성 필요
- **Panel**: 제한적인 테마 옵션
- **Violit**: 30+ 즉시 사용 가능한 전문가급 테마 💜

---

## 🚀 Quick Start

### 1. 설치

PyPI에서 `violit`을 설치하세요. (Python 3.10+ 필요)

```bash
pip install violit

# 또는 개발 버전
pip install git+https://github.com/violit-dev/violit.git
```

### 2. Hello, Violit!

`hello.py` 파일을 작성합니다.

```python
import violit as vl

# Violit 앱 인스턴스 생성
app = vl.App(title="Hello Violit", theme='ocean')

app.title("💜 Hello, Violit!")
app.markdown("Experience the speed of **Zero Rerun**.")

# 상태 정의
count = app.state(0)

col1, col2 = app.columns(2)

with col1:
    # 클릭하면 값만 깔끔하게 변경
    app.button("➕ Plus", on_click=lambda: [count.set(count.value + 1), app.balloons()])

with col2:
    app.button("➖ Minus", on_click=lambda: count.set(count.value - 1))

# 실시간 반응형 메트릭
app.metric("Current Count", count)

app.run()
```

### 3. 실행

웹 브라우저 모드 또는 네이티브 앱 모드로 실행할 수 있습니다.

```bash
# 웹 브라우저 실행 (기본: WebSocket Mode)
python hello.py

# Lite 모드로 실행 (대규모 트래픽 처리시)
python hello.py --mode lite

# 🖥️ 데스크탑 앱 모드 (강력 추천!)
python hello.py --native --splash
```

---

## 📊 Streamlit API Support Matrix

Violit은 Streamlit의 주요 API를 대부분 지원하며, 더 나은 성능을 위해 일부 구조를 개선했습니다.

### 1. Text & Media Elements
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.write` | `app.write` | ✅ | 100% 호환 (Signal/State 자동 감지) |
| `st.markdown` | `app.markdown` | ✅ | Markdown 문법 지원 |
| `st.title`, `st.header` | `app.title`, `app.header` | ✅ | Gradient 효과 자동 적용 |
| `st.subheader`, `st.caption` | `app.subheader`, `app.caption` | ✅ | |
| `st.code` | `app.code` | ✅ | Syntax Highlighting 지원 |
| `st.text` | `app.text` | ✅ | |
| `st.latex` | `app.latex` | ❌ | Markdown 수식 `$..$`으로 대체 권장 |
| `st.divider` | `app.divider` | ✅ | |
| `st.image` | `app.image` | ✅ | URL, Local File, NumPy, PIL 지원 |
| `st.audio`, `st.video` | `app.audio`, `app.video` | ✅ | |

### 2. Data & Charts
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.dataframe` | `app.dataframe` | ✅ | **Ag-Grid Native** (고성능) |
| `st.table` | `app.table` | ✅ | |
| `st.metric` | `app.metric` | ✅ | `delta` 및 자동 색상 지원 |
| `st.json` | `app.json` | ✅ | |
| `st.data_editor` | `app.data_editor` | ✅ | 간소화된 버전 제공 |
| `st.plotly_chart` | `app.plotly_chart` | ✅ | Plotly 완벽 호환 |
| `st.pyplot` | `app.pyplot` | ✅ | Matplotlib 지원 |
| `st.line/bar/area_chart` | `app.line_chart` 등 | ✅ | |
| `st.scatter_chart` | `app.scatter_chart` | ✅ | |
| `st.map` | `app.map` | ❌ | `plotly_chart`의 Mapbox 사용 권장 |

### 3. Input Widgets
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.button` | `app.button` | ✅ | `key` 불필요, `on_click` 권장 |
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
| `st.date/time_input` | `app.date_input` 등 | ✅ | |
| `st.file_uploader` | `app.file_uploader` | ✅ | |
| `st.color_picker` | `app.color_picker` | ✅ | |
| `st.camera_input` | `app.camera_input` | ❌ | 미지원 |

### 4. Layout & Containers
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.columns` | `app.columns` | ✅ | List 비율 지원 (예: `[1, 2, 1]`) |
| `st.container` | `app.container` | ✅ | |
| `st.expander` | `app.expander` | ✅ | |
| `st.tabs` | `app.tabs` | ✅ | |
| `st.empty` | `app.empty` | ✅ | 동적 업데이트용 |
| `st.sidebar` | `app.sidebar` | ✅ | `with app.sidebar:` 문법 사용 |
| `st.dialog` | `app.dialog` | ✅ | Modal Decorator 지원 |
| `st.popover` | `app.popover` | ❌ | `app.dialog` 사용 권장 |

### 5. Chat & Status
| Streamlit | Violit Support | Status | Note |
|---|---|---|---|
| `st.chat_message` | `app.chat_message` | ✅ | Avatar 지원 |
| `st.chat_input` | `app.chat_input` | ✅ | |
| `st.status` | `app.status` | ✅ | |
| `st.spinner` | `app.spinner` | ✅ | |
| `st.progress` | `app.progress` | ✅ | |
| `st.toast` | `app.toast` | ✅ | |
| `st.balloons`, `st.snow` | `app.balloons` 등 | ✅ | |
| `st.success/error/warning` | `app.success` 등 | ✅ | |

### 6. Control Flow (Removed)
| Streamlit | Violit Approach | Note |
|---|---|---|
| `st.rerun` | **Unnecessary** | State 변경 시 즉시 부분 업데이트 (Zero Rerun) |
| `st.stop` | **Unnecessary** | Python 제어문(`return` 등)으로 처리 |
| `st.form` | `app.form` | ✅ 지원 (Batch Input 용도) |

---

## 🔌 Third-Party Library Support

Violit은 Streamlit의 인기 서드파티 라이브러리 기능들을 **Native**로 흡수하고 있습니다.

| Library | Violit Status | Description |
|---|---|---|
| **streamlit-aggrid** | ✅ **Native** | `app.dataframe`이 기본적으로 고성능 AG-Grid를 사용합니다. 별도 설치 불필요. |
| **Plotly** | ✅ **Native** | `app.plotly_chart`로 완벽하게 지원합니다. |
| **streamlit-lottie** | ❌ **Planned** | 현재 미지원 (향후 `app.lottie` 추가 예정). |
| **streamlit-option-menu** | ✅ **Native** | Violit의 내장 Sidebar가 Multi-page Navigation을 완벽 대체합니다. |
| **streamlit-extras** | ⚠️ **Partial** | Metric Cards 등 일부 디자인 요소는 Violit 테마 시스템으로 대체 가능합니다. |
| **streamlit-webrtc** | ⚠️ **Planned** | WebSocket 기반 실시간 통신으로 향후 지원 예정. |

### 🎁 Violit만의 추가 기능

Streamlit에는 없는 Violit만의 독점 기능:
- **Broadcasting API**: 실시간 멀티 유저 동기화 (`app.broadcaster`)
- **Card List**: 동적 리스트 UI 자동 관리 (`app.card_list`)
- **Desktop Mode**: `--native` 플래그로 즉시 데스크탑 앱
- **Hot Reload**: 코드 수정 시 자동 새로고침 (개발 모드)
- **Animation Modes**: 부드러운 페이지 전환 (`animation_mode='soft'`)

---

## 🛠️ Tech Stack

Violit은 현대적인 웹 기술과 파이썬의 강력함을 결합했습니다.

* **Backend**: FastAPI (Async Python) - 고성능 비동기 처리
* **Frontend**: Web Components (Shoelace) - 모던 UI 컴포넌트
* **Protocol**: WebSocket (default) & HTTP/HTMX (lite mode) - 하이브리드 선택 가능
* **State**: Signal-based Reactivity - Solid.js 스타일의 세밀한 반응성
* **Charts**: Plotly.js - 인터랙티브 차트
* **Data Grid**: AG-Grid - 엔터프라이즈급 데이터 테이블
* **Desktop**: pywebview - Electron 없이 가벼운 데스크탑 앱

### 📦 Zero Dependencies Bloat

다른 프레임워크와 달리 Violit은:
- ❌ Node.js 불필요 (Reflex와 다르게)
- ❌ React/Vue 빌드 불필요 (순수 Web Components)
- ❌ 복잡한 컴파일 단계 없음
- ✅ Python과 pip만 있으면 OK!

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

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

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
