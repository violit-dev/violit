![Violit Logo](https://github.com/user-attachments/assets/f6a56e37-37a5-437c-ae16-13bff7029797)

🎉 **OpenSourceProjects.dev 선정**: ["Stop Overcomplicating Your Data Dashboards"](https://www.opensourceprojects.dev/post/634ad562-83d4-4a7b-8a74-b61e47ad68aa)

> **"Faster than Light, Beautiful as Violet."** **Streamlit의 구조 × React의 성능**

**Violit**은 **세밀한 반응형 아키텍처(fine-grained reactive architecture)** 위에 구축된 Python 웹 프레임워크입니다. Streamlit 커뮤니티가 사랑하는 생산적인 top-down Python 작성 방식을 유지하면서도, **전체 스크립트 재실행(full script rerun)** 모델의 성능 병목은 제거했습니다.

Violit은 데이터 앱과 대시보드에서 자연스럽게 출발하지만, 그 용도에만 머무르지 않습니다. ORM/Auth 내장 지원과 Tailwind 스타일 디자인 프리미티브를 바탕으로, 관리자 도구, 사내 플랫폼, CRUD 시스템, 사용자 대상 제품 UI 같은 더 일반적인 웹 애플리케이션까지 안정적으로 확장할 수 있습니다.

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

- **문서:** <https://doc.violit.cloud>
- **PyPI:** <https://pypi.org/project/violit/>
- **GitHub:** <https://github.com/violit-dev/violit>

## 데모

이 데모는 Violit이 어떤 상호작용을 위해 만들어졌는지 보여줍니다. Python 중심의 UI 코드로 작성하면서도, 인터페이스가 복잡해져도 반응형 업데이트는 빠르고 부드럽게 유지됩니다.

<p align="center">
    <video 
        src="https://github.com/user-attachments/assets/d2e9297b-bfd6-4eb6-abff-10601bc3e735" 
        poster="https://via.placeholder.com/800x450?text=Violit+Loading..."
        controls 
        loop 
        muted 
        autoplay
        playsinline 
        style="max-width: 100%; height: auto;">
        <a href="https://github.com/user-attachments/assets/d2e9297b-bfd6-4eb6-abff-10601bc3e735">Violit 쇼케이스 데모 보기</a>
    </video>
</p>

## 왜 Violit인가?

Violit은 Streamlit의 즉각적인 생산성을 좋아하지만, 애플리케이션이 작은 대시보드에서 기능이 풍부한 웹 앱으로 성장할 때도 자연스럽게 확장되는 구조를 원하는 개발자를 위해 설계되었습니다.

- **Streamlit 같은 Python 흐름**을 유지하면서도 전체 스크립트 재실행은 완전히 제거했습니다.
- **세밀한 상태 업데이트**로 의존하는 위젯만 갱신합니다. (React와 유사한 반응성)
- **내장 ORM**을 제공하여 `vl.App(db=...)` 형태로 바로 사용할 수 있습니다.
- `cls` 파라미터를 통한 **Tailwind 스타일 스타일링**을 지원합니다.
- `app.background(...)`, `app.interval(...)`을 포함한 **비동기 친화적 구조**를 제공합니다.
- **유연한 런타임**: 브라우저, 더 높은 동시성을 위한 HTMX Lite 모드, Desktop Native 앱 실행을 지원합니다.
- **풍부한 생태계**: 강력한 위젯, 테마, 애니메이션을 기본 제공 수준으로 활용할 수 있습니다.

## 아키텍처 차이

핵심 차이는 문법만이 아니라, 사용자가 클릭하거나 입력하거나 드래그한 뒤 프레임워크가 DOM을 어떻게 처리하느냐에 있습니다.

| 항목 | Streamlit | Violit |
| :--- | :--- | :--- |
| **업데이트 모델** | 전체 스크립트 재실행 | 세밀한 반응형 업데이트 |
| **상호작용 비용** | 전체 스크립트가 다시 실행될 수 있음 | 명시적으로 의존하는 UI 컴포넌트만 업데이트 |
| **최적화 부담** | rerun 제약을 피하기 위한 우회가 자주 필요 | 신호 기반 아키텍처로 자연스럽게 처리 |
| **앱 성장 경로** | 빠르고 단순한 데이터 뷰에 적합 | 더 풍부하고 상태를 많이 가지는 앱 흐름으로 확장되도록 설계 |
| **런타임 모드** | 브라우저 중심 | WebSocket, Lite, Desktop Native |
| **스타일링** | 기본 테마 수준 | 테마 + Tailwind 유틸리티 스타일링 |

## 프레임워크 비교 (기능 매트릭스)

모든 Python UI 프레임워크는 각기 다른 철학과 강점을 갖고 있습니다. 아래 매트릭스는 대표적인 프레임워크들의 구조적 특성을 비교해, 사용 목적에 맞는 도구를 선택하는 데 도움을 주기 위한 것입니다.

| Framework | No Full Rerun | Pure Python (Zero JS/HTML) | SEO / SSR Ready | Desktop Native (exe/app) |
| :--- | :---: | :---: | :---: | :---: |
| **Streamlit** | ❌ | ✅ | ❌ | ❌ |
| **Dash / Panel** | ✅<br />*(Callbacks)* | ✅ | ❌ | ❌ |
| **NiceGUI** | ✅ | ✅ | ❌ | ✅ |
| **Reflex** | ✅ | ⚠️<br />*(React paradigm)* | ✅ | ❌ |
| **RIO** | ✅<br />*(React-like)* | ✅ | ❌ | ✅<br />*(Local mode)* |
| **Violit** | ✅<br />**(Signals)** | ✅ | ✅ | ✅<br />**(Built-in pywebview)** |

### 이 매트릭스가 의미하는 것

- **Streamlit**은 여전히 데이터 과학자에게 가장 쉬운 출발점이지만, 상호작용이 복잡해질수록 full-rerun 모델이 병목이 될 수 있습니다.
- **Dash & Panel**은 강력한 데이터 도구이지만, 프레임워크 고유의 콜백 구조를 받아들여야 하는 경우가 많습니다.
- **NiceGUI**는 매우 실용적이고 생산적이며, 객체 지향적인 UI 바인딩 스타일을 채택합니다.
- **Reflex**는 매우 강력하고 React 프런트엔드로 컴파일되지만, React 개념에 익숙하지 않은 개발자에게는 학습 곡선이 더 가파를 수 있습니다.
- **RIO**는 React와 Flutter에서 영감을 받은 현대적인 반응형 프레임워크로 훌륭한 컴포넌트 구조를 제공하지만, 다소 강한 의견이 담긴 클래스 기반 아키텍처를 요구합니다.
- **Violit**은 그 중간 지점을 목표로 합니다. 즉, **Streamlit의 익숙한 스크립트형 가독성**을 유지하면서, 내부적으로는 **현대적인 세밀 반응형 엔진**을 활용하고 ORM, Auth, Desktop 빌드 같은 풀스택 기능까지 내장합니다.

## 문법 비교

아래 예제는 의도적으로 최소한으로 구성되어 있습니다. 같은 작은 상호작용 하나를 표현하는 데 각 프레임워크가 얼마나 많은 구조적 보일러플레이트를 요구하는지 보여주는 것이 목적입니다.

### Streamlit

```python
import streamlit as st

name = st.text_input("Name", "Violit")
st.write(f"Hello, {name}")
```

- **느낌:** 아주 직관적이고 입문자 친화적입니다.
- **트레이드오프:** 앱이 커질수록 full-rerun 동작을 피하기 위한 구조 고민이 계속 생깁니다.

### NiceGUI

```python
from nicegui import ui

name = ui.input("Name", value="Violit")
ui.label().bind_text_from(name, "value", lambda v: f"Hello, {v}")

ui.run()
```

- **느낌:** UI 객체를 명시적으로 바인딩하는 방식입니다. 컴포넌트 중심 설계에 매우 적합합니다.
- **트레이드오프:** 데이터 실무자가 선호하는 선언적 top-down 읽기 흐름에서는 다소 멀어집니다.

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

- **느낌:** React 감성의 견고한 상태 모델입니다.
- **트레이드오프:** 별도의 상태 클래스를 정의해야 해서, 소형 또는 중형 인터랙티브 앱에는 다소 무겁게 느껴질 수 있습니다.

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

- **느낌:** React와 Flutter에서 강한 영향을 받은 컴포넌트 기반 반응형 구조입니다.
- **트레이드오프:** 클래스 기반 컴포넌트 구조가 강력하긴 하지만, 단순한 절차형 스크립트에 비해 더 의견이 강하고 무겁게 느껴질 수 있습니다.

### Violit 문법

```python
import violit as vl

app = vl.App()

name = app.text_input("Name", value="Violit")
app.text(lambda: f"Hello, {name.value}")

app.run()
```

- **느낌:** Streamlit의 top-down 단순함에 현대적인 JS 프레임워크 수준의 반응형 성능을 결합했습니다.
- **장점:** 문법은 가볍게 유지하면서도, 런타임은 필요한 DOM 노드만 자연스럽게 업데이트합니다.

## 빠른 시작

Violit의 핵심 철학을 바로 경험해보세요. 상태를 선언하고, 위젯에 연결하고, 나머지 업데이트는 런타임에 맡기면 됩니다.

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

## 아주 쉬운 ORM 예제

Violit은 내장 영속성 계층을 통해 빠른 프로토타입과 실제 서비스용 애플리케이션 사이의 간극을 줄여줍니다.

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

## 백그라운드 작업

이 지점에서 Violit은 단순 대시보드 도구와 확실히 구분됩니다. Python 코드 안에서 장시간 실행되는 작업을 직접 모델링하면서도, 사용자 인터페이스를 멈추지 않게 만들 수 있습니다.

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

*팁: 주기적인 폴링이나 새로고침이 필요하다면 `app.interval(...)`도 기본 지원됩니다.*

## 스타일링

Violit은 UI 커스터마이징을 실용적이고 빠르게 유지합니다. 사소한 CSS 조정마다 Python 바깥으로 나갈 필요 없이 유틸리티 클래스를 바로 사용할 수 있습니다.

```python
app.button(
    "Deploy",
    cls="rounded-full bg-sky-500 px-6 py-3 text-white shadow-lg hover:bg-sky-600",
)
```

## 기술 스택

Violit은 성능과 상호작용에 집중한 실용적인 현대 스택 위에서 동작합니다.

- **Backend:** FastAPI, Uvicorn
- **Reactivity:** WebSocket runtime, HTMX-based Lite mode
- **Data & DB:** SQLModel + Alembic, pandas, numpy
- **Visualization:** Vega-Lite, Plotly integration
- **Desktop:** pywebview for native executables
- **Assets:** Local bundled assets for offline-friendly deployments

## 로드맵

Violit은 빠르게 발전하고 있습니다. 핵심 반응형 기반은 이미 견고하며, 여러 풀스택 기능도 구현된 상태입니다. 다음 단계는 생태계 확장과 커스터마이징 강화에 집중하고 있습니다.

- ✅ **Core**: Signal State Engine, Theme System
- ✅ **Widgets**: Plotly, Dataframe, Input Widgets
- ✅ **ORM**: SQLModel 및 migration을 포함한 내장 ORM 지원
- ✅ **Auth**: 내장 인증 플로우와 페이지 보호
- ✅ **Styling**: Tailwind 스타일 유틸리티 스타일링 지원
- ✅ **Homepage**: 공식 웹사이트 공개
- ✅ **Documentation**: 기술 문서 및 API 레퍼런스 제공
- ⏳ **Custom Components**: 사용자 정의 Custom Component API
- ⏳ **Custom Theme**: 고급 테마 커스터마이징 지원
- ⏳ **Examples**: 더 많은 실전형 프로덕션 예제
- ⏳ **Violit.Cloud**: 원클릭 클라우드 배포 서비스
- ⏳ **Expansion**: 서드파티 라이브러리와의 더 깊은 통합

## 설치

시작은 패키지를 설치하는 것만으로 충분합니다. Violit CLI도 함께 설치됩니다.

```bash
pip install violit
# 최신 개발 버전을 설치하려면:
pip install git+https://github.com/violit-dev/violit.git
```

## 앱 실행하기

Violit은 강력한 CLI를 제공합니다. 앱 실행에는 `violit run` 사용을 권장합니다.

`violit run`은 `app.run()`이 받는 런타임 플래그를 그대로 전달합니다. `python app.py ...`로 동작하는 명령은 `violit run app.py ...`로도 같은 플래그를 사용할 수 있습니다.

`--lite`는 기본 WebSocket 런타임 대신 HTMX 기반 HTTP 모드로 앱을 실행합니다. 동시 접속자가 더 많거나 WebSocket 사용이 제한된 환경에서는 이 모드가 더 적합한 경우가 많습니다.

```bash
python app.py --reload --localhost
violit run app.py --reload --localhost

violit run app.py --help       # app.run()이 받는 런타임 플래그 보기
violit run app.py --reload     # 코드 변경 시 자동 재시작
violit run app.py --localhost  # 127.0.0.1에 바인딩하고 localhost URL 출력
violit run app.py --native     # Desktop App으로 실행
violit run app.py --lite       # 더 높은 동시성을 위한 HTMX 기반 lite 모드
violit run app.py --port 8020
violit run app.py --make-migration "add_users"
```

새 프로젝트를 즉시 스캐폴딩할 수도 있습니다.

```bash
violit create my_app
cd my_app
violit run main.py --reload
```

## 문서 및 리소스

더 깊이 살펴보고 싶다면, 목적에 맞는 공식 가이드를 확인하세요.

- **라이브 문서:** <https://doc.violit.cloud>
- **Streamlit 마이그레이션:** [Streamlit API Support Matrix](doc/Streamlit%20API%20Support%20Matrix.md)
- **AI 코딩 컨텍스트:** [llms.txt](doc/llms.txt)

## 📝 라이선스

Violit은 **MIT License**로 배포됩니다.

*상표 고지: 오픈소스 라이선스는 코드에 적용되며, "Violit™"는 프로젝트 정체성을 명확히 유지하기 위한 The Violit Team의 상표입니다.*
