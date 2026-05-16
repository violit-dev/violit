# 🚀 Violit으로 10분 만에 나만의 블로그 만들기!

## 👋 환영합니다!

안녕하세요! 웹 개발이 처음이신가요? 걱정하지 마세요. 이 튜토리얼을 따라가면 **진짜로 작동하는 블로그**를 만들 수 있습니다! 😊

### 🤔 "프레임워크"가 뭔가요?

프레임워크는 쉽게 말해 **"레고 블록 세트"** 같은 거예요. 집을 지을 때 벽돌을 하나하나 만드는 대신, 이미 만들어진 블록을 조립하는 거죠. 

- **Django, Ruby on Rails**: 유명하지만 설정이 복잡해요 😵
- **Violit**: 파이썬만 알면 OK! 설정도 거의 없어요 🎉

### 🎯 우리가 만들 블로그의 기능

이 튜토리얼을 마치면 다음과 같은 기능이 있는 블로그가 완성됩니다:

- ✅ **회원가입**: 새로운 사용자 계정 만들기
- ✅ **로그인/로그아웃**: 내 계정으로 들어가고 나가기
- ✅ **글 쓰기**: 제목과 내용을 입력해서 글 발행하기
- ✅ **목록 보기**: 모든 사람이 쓴 글을 한눈에 보기
- ✅ **상세 보기**: 클릭해서 전체 글 읽기
- ✅ **글 삭제**: 내가 쓴 글만 지우기

진짜 블로그처럼 작동합니다! 🎊

---

## 🏗️ 1단계: 준비 작업 (필요한 도구 가져오기)

### 📦 라이브러리란?

라이브러리는 **다른 사람들이 만든 편리한 도구 모음**이에요. 우리가 모든 걸 처음부터 만들 필요가 없죠!

자, 이제 `violit_blog.py` 파일을 만들고 아래 코드를 입력하세요:

```python
import sys
import os
import sqlite3

# Violit 라이브러리 경로 추가 (상위 폴더에 violit이 있는 경우)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import violit as vl
```

**🔍 이 코드가 하는 일:**
- `sqlite3`: 데이터를 저장할 데이터베이스 (나중에 설명!)
- `violit as vl`: 우리의 슈퍼 프레임워크! `vl`이라는 짧은 이름으로 부를 거예요

**💡 팁:** `sys.path.append` 부분은 Violit을 찾을 수 있게 경로를 알려주는 거예요. 만약 Violit을 `pip install`로 설치했다면 이 줄은 생략해도 됩니다!

---

## 🗄️ 2단계: 데이터베이스 만들기 (글과 사용자 정보 저장소)

### 📚 데이터베이스가 뭔가요?

데이터베이스는 **정보를 정리해서 보관하는 엑셀 같은 거**예요. 
- **Users 시트**: 사용자 ID, 비밀번호
- **Posts 시트**: 글 제목, 내용, 작성자

우리는 **SQLite**를 씁니다. 설치 필요 없이 파이썬에 기본으로 들어있어요! 👍

```python
DB_NAME = "blog_app.db"

def init_db():
    """데이터베이스 초기화 - 처음 한 번만 실행"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 사용자 테이블 만들기
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT)''')
    
    # 게시글 테이블 만들기
    c.execute('''CREATE TABLE IF NOT EXISTS posts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  title TEXT, 
                  content TEXT, 
                  author_name TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# DB 조회를 쉽게 해주는 헬퍼 함수
def db_query(query, params=(), fetch=False):
    """데이터베이스에 질문하고 답변 받기"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 딕셔너리처럼 사용하려고
    c = conn.cursor()
    c.execute(query, params)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return [dict(r) for r in res] if fetch else None
```

**🔍 코드 해설:**

1. **`CREATE TABLE IF NOT EXISTS`**: 테이블이 없으면 만들고, 있으면 그냥 넘어가요
2. **`PRIMARY KEY AUTOINCREMENT`**: ID를 자동으로 1, 2, 3... 증가시켜줘요
3. **`UNIQUE`**: 중복된 아이디는 안 돼요! (같은 아이디로 두 번 가입 불가)
4. **`db_query()` 함수**: 매번 긴 코드 쓰기 귀찮으니까 간단하게 만든 도우미 함수!

**💬 예시로 이해하기:**
```
users 테이블은 이렇게 생겼어요:
┌────┬──────────┬──────────┐
│ id │ username │ password │
├────┼──────────┼──────────┤
│ 1  │ alice    │ 1234     │
│ 2  │ bob      │ abcd     │
└────┴──────────┴──────────┘
```

---

## 🎨 3단계: 앱 만들고 상태 관리하기

### 🧠 "상태(State)"가 뭔가요?

상태는 **앱이 기억하는 것**이에요. 예를 들어:
- "지금 로그인한 사람이 누구지?" 
- "어떤 글을 보고 있지?"

이런 정보를 **메모리**에 저장하는 거죠!

```python
# 데이터베이스 초기화 실행 (처음 한 번 실행됨)
init_db()

# 앱 생성! 
app = vl.App(
    title="Violit Blog",          # 브라우저 탭에 보일 제목
    theme="ocean",                # 바다 테마 (파란색 계열)
    container_width="800px"       # 화면 너비 제한 (모바일처럼 보이게)
)

# 세션 상태: 사용자마다 따로 관리되는 정보
session = app.state({
    'is_logged_in': False,        # 로그인 했니? (처음엔 False)
    'user_id': None,              # 사용자 ID 번호
    'username': '',               # 사용자 이름
    'view_mode': 'list',          # 화면 모드: 'list'(목록) or 'detail'(상세)
    'selected_post_id': None      # 지금 보고 있는 글 ID
}, key='blog_session')
```

**🔍 이해하기:**
- **`app.state()`**: Violit의 마법! 이 값이 바뀌면 화면도 자동으로 바뀌어요 🪄
- **`key='session_v1'`**: 세션마다 고유하게 저장 (여러 사용자가 동시에 써도 안 겹쳐요!)

---

## 🏠 4단계: 메인 페이지 만들기 (글 목록 + 상세보기)

이제 진짜 중요한 부분! 사용자가 제일 먼저 보는 **홈 페이지**를 만들어요.

### 🎭 두 얼굴을 가진 페이지

홈 페이지는 **두 가지 모드**가 있어요:
1. **목록 모드**: 모든 글을 카드로 쭉 보여주기
2. **상세 모드**: 글 하나를 크게 펼쳐 보기

```python
def home_page():
    s = session.value  # 현재 세션 정보 가져오기 (짧게 's'라고 부를게요)
    
    app.header("Blog Feed")  # 큰 제목
    
    if s['view_mode'] == 'detail':
        # ========== 상세보기 모드 ==========
        post_id = s['selected_post_id']
        posts = db_query("SELECT * FROM posts WHERE id = ?", (post_id,), fetch=True)
        
        if not posts:
            app.error("Post not found.")
            def go_back():
                session.set({**s, 'view_mode': 'list'})
            app.button("Back to list", on_click=go_back)
            return
        
        post = posts[0]
        
        # 예쁜 컨테이너 안에 글 내용 표시
        with app.container(border=True, style="padding: 2rem;"):
            app.subheader(post['title'])  # 글 제목
            app.caption(f"{post['author_name']} | {post['created_at']}")
            app.divider()  # 구분선
            app.text(post['content'])  # 글 내용
            
            app.divider()
            
            # 버튼들을 가로로 배치하기
            cols = app.columns(4)  # 4개 칸으로 나누기
            
            with cols[0]:  # 첫 번째 칸
                def go_to_list():
                    # 목록 모드로 돌아가기
                    session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                app.button("Back to list", on_click=go_to_list, variant="neutral")
            
            # 내가 쓴 글이면 삭제 버튼 보여주기
            if s['is_logged_in'] and s['user_id'] == post['user_id']:
                with cols[3]:  # 네 번째 칸 (맨 오른쪽)
                    def delete_post():
                        db_query("DELETE FROM posts WHERE id = ?", (post['id'],))
                        app.toast("Post deleted.")
                        session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                    
                    app.button("Delete", on_click=delete_post, variant="danger")
    
    else:
        # ========== 목록 모드 ==========
        posts = db_query("SELECT * FROM posts ORDER BY created_at DESC", fetch=True)
        
        if not posts:
            app.info("No posts yet. Write the first post!")
        
        # 모든 글을 반복해서 카드로 표시
        for post in posts:
            with app.container(border=True, style="margin-bottom: 1rem;"):
                app.markdown(f"### {post['title']}")  # 제목 (크게)
                app.caption(f"By {post['author_name']} on {post['created_at'][:10]}")
                
                # 내용 요약 (처음 100글자만)
                summary = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                app.text(summary)
                
                # "더 읽기" 버튼 - 클릭하면 상세보기로!
                def make_view_handler(pid):
                    """클로저 패턴: 각 버튼마다 다른 post_id를 기억하게"""
                    return lambda: session.set({**session.value, 'view_mode': 'detail', 'selected_post_id': pid})
                
                app.button("Read more", on_click=make_view_handler(post['id']), variant="text")
```

**🔍 중요 개념 설명:**

1. **`session.value`**: 현재 상태를 읽어오기
2. **`session.set()`**: 상태를 바꾸기 → 화면도 자동으로 바뀜!
3. **`with app.container()`**: 박스 안에 내용을 담기 (깔끔!)
4. **`app.columns(4)`**: 화면을 4개 칸으로 나누기 (버튼 배치용)
5. **`on_click=함수`**: 버튼을 클릭하면 함수 실행!

**💬 왜 `make_view_handler`를 쓰나요?**

반복문 안에서 버튼을 만들 때, 각 버튼이 **자기만의 post_id**를 기억해야 해요. 그래서 함수를 하나 더 만들어서 값을 "가둬놓는" 거예요. (이걸 클로저라고 해요!)

---

## ✍️ 5단계: 글쓰기 페이지 만들기

이제 사용자가 직접 글을 쓸 수 있는 페이지를 만들어요!

```python
def write_page():
    s = session.value
    app.header("Write New Post")
    
    # 로그인 안 했으면 경고 메시지만 보여주기
    if not s['is_logged_in']:
        app.warning("Login required.")
        return  # 여기서 함수 종료!
    
    with app.container():
        # 입력 폼 만들기
        title = app.text_input(
            "Title", 
            placeholder="Enter title", 
            key="new_post_title"
        )
        content = app.text_area(
            "Content", 
            placeholder="Tell your story...", 
            rows=10, 
            key="new_post_content"
        )
        
        # 저장 버튼 클릭 시 실행될 함수
        def save_post():
            # 빈 칸 검증
            if not title.value.strip() or not content.value.strip():
                app.toast("Please enter both title and content.", variant="danger")
                return
            
            # 데이터베이스에 저장
            db_query(
                "INSERT INTO posts (user_id, author_name, title, content) VALUES (?, ?, ?, ?)",
                (s['user_id'], s['username'], title.value, content.value)
            )
            
            app.toast("Post published successfully!", variant="success")
            
            # 입력 필드 비우기
            title.set("")
            content.set("")
            
            # 홈 화면(목록)으로 돌아가기
            session.set({**session.value, 'view_mode': 'list'})
        
        app.button("Publish", on_click=save_post, variant="primary", size="large")
```

**🔍 핵심 포인트:**

1. **`app.text_input()`**: 한 줄 입력칸 (제목용)
2. **`app.text_area()`**: 여러 줄 입력칸 (내용용)
3. **`key="..."`**: 각 입력칸의 고유 이름 (중복되면 안 돼요!)
4. **`.value`**: 사용자가 입력한 값 읽기
5. **`.set("")`**: 입력칸 비우기

**💡 재미있는 사실:** `app.toast()`는 화면 오른쪽 위에 예쁜 알림을 띄워줘요. 마치 토스트가 튀어나오듯이! 🍞

---

## 🔐 6단계: 로그인 & 회원가입 페이지

### 🚪 로그인 페이지

사용자가 자기 계정으로 들어오는 문!

```python
def login_page():
    s = session.value
    
    # 이미 로그인한 경우 - 내 정보 보여주기
    if s['is_logged_in']:
        app.header("My Info")
        app.success(f"Hello, **{s['username']}**!")
        
        def logout():
            # 세션 초기화 (로그아웃)
            session.set({
                'is_logged_in': False,
                'user_id': None,
                'username': '',
                'view_mode': 'list',
                'selected_post_id': None
            })
            app.toast("Logged out.")
        
        app.button("Logout", on_click=logout, variant="neutral")
        return  # 여기서 끝!
    
    # 로그인 안 한 경우 - 로그인 폼 보여주기
    app.header("Login")
    
    with app.container():
        username = app.text_input("Username", key="login_username")
        password = app.text_input(
            "Password", 
            type="password",  # 비밀번호는 *** 으로 보이게!
            key="login_password"
        )
        
        def do_login():
            # 데이터베이스에서 사용자 찾기
            users = db_query(
                "SELECT id, username FROM users WHERE username = ? AND password = ?",
                (username.value, password.value),
                fetch=True
            )
            
            if users:
                user = users[0]
                # 로그인 성공! 세션에 정보 저장
                session.set({
                    **session.value,
                    'is_logged_in': True,
                    'user_id': user['id'],
                    'username': user['username']
                })
                app.toast(f"Welcome, {user['username']}!", variant="success")
            else:
                app.toast("Invalid username or password.", variant="danger")
        
        app.button("Login", on_click=do_login, variant="primary")
```

**🔍 설명:**

- **`type="password"`**: 입력한 글자를 `***`로 보이게 (보안!)
- **`**session.value`**: 기존 세션 데이터를 펼쳐놓고, 일부만 수정 (파이썬 문법)

---

### 📝 회원가입 페이지

새로운 사용자가 계정을 만드는 곳!

```python
def register_page():
    app.header("Register")
    
    # 이미 로그인했으면 가입할 필요 없죠
    if session.value['is_logged_in']:
        app.info("Already logged in.")
        return

    with app.container():
        username = app.text_input("Username", key="reg_username")
        password = app.text_input("Password", type="password", key="reg_password")
        
        def do_register():
            # 빈 칸 체크
            if not username.value or not password.value:
                app.toast("Please enter username and password.", variant="danger")
                return
            
            try:
                # 데이터베이스에 새 사용자 추가
                db_query(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username.value, password.value)
                )
                app.toast("Registration successful! Please login.", variant="success")
            except sqlite3.IntegrityError:
                # UNIQUE 제약 위반 = 이미 있는 아이디
                app.toast("Username already exists.", variant="danger")
        
        app.button("Register", on_click=do_register, variant="primary")
```

**🔍 핵심:**

- **`try-except`**: 에러가 날 수도 있는 코드를 안전하게 실행
- **`IntegrityError`**: 중복된 아이디로 가입하려 할 때 발생하는 에러

---

## 👤 7단계: 내 글 목록 페이지 만들기

로그인한 사용자 본인이 쓴 글만 따로 모아볼 수 있는 페이지를 만들어요!

```python
def my_posts_page():
    """My posts list page"""
    s = session.value
    app.header("My Posts")
    
    if not s['is_logged_in']:
        app.warning("Login required.")
        return
    
    if s['view_mode'] == 'detail' and s['selected_post_id']:
        # Detail view
        post_id = s['selected_post_id']
        posts = db_query("SELECT * FROM posts WHERE id = ? AND user_id = ?", 
                        (post_id, s['user_id']), fetch=True)
        
        if not posts:
            app.error("Post not found.")
            def go_back():
                session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
            app.button("Back to list", on_click=go_back)
            return
            
        post = posts[0]
        with app.container(border=True, style="padding: 2rem;"):
            app.subheader(post['title'])
            app.caption(f"{post['created_at']}")
            app.divider()
            app.text(post['content'])
            
            app.divider()
            cols = app.columns(4)
            with cols[0]:
                def go_to_list():
                    session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                app.button("Back to list", on_click=go_to_list, variant="neutral")
            
            with cols[3]:
                def delete_post():
                    db_query("DELETE FROM posts WHERE id = ?", (post['id'],))
                    app.toast("Post deleted.")
                    session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                app.button("Delete", on_click=delete_post, variant="danger")
    else:
        # List view - my posts only
        posts = db_query("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", 
                        (s['user_id'],), fetch=True)
        
        if not posts:
            app.info(f"No posts yet. Write your first post from 'Write' menu!")
        else:
            app.success(f"Total {len(posts)} posts written.")
        
        for post in posts:
            with app.container(border=True, style="margin-bottom: 1rem;"):
                app.markdown(f"### {post['title']}")
                app.caption(f"{post['created_at'][:10]}")
                summary = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                app.text(summary)
                
                def make_view_handler(pid):
                    return lambda: session.set({**session.value, 'view_mode': 'detail', 'selected_post_id': pid})
                app.button("Read more", on_click=make_view_handler(post['id']), variant="text")
```

**🔍 핵심 포인트:**

1. **사용자 필터링**: `WHERE user_id = ?`로 본인 글만 가져오기
2. **홈과 유사한 구조**: 목록/상세 보기 모두 지원
3. **글 개수 표시**: `app.success()`로 작성한 글 개수 보여주기
4. **삭제 권한**: 자기 글이니까 모두 삭제 가능!

---

## 🎨 8단계: 사이드바 & 네비게이션 (모든 페이지 연결하기)

이제 모든 페이지를 하나로 묶어서 앱을 완성해요!

### 📱 사이드바 만들기

화면 왼쪽에 있는 메뉴 바!

```python
with app.sidebar:
    app.markdown("## Violit Blog")
    app.caption("Simple & Fast")
    app.divider()  # 구분선
    
    # Dynamic login status display
    def render_user_info():
        s = session.value
        if s['is_logged_in']:
            return f"{s['username']}"
        else:
            return "Please login"
    
    app.simple_card(render_user_info)
```

**🔍 설명:**
- **`render_user_info()` 함수**: 세션 상태에 따라 동적으로 표시할 내용을 반환
- **`app.simple_card()`**: 함수를 전달하면 자동으로 카드로 예쁘게 보여줘요!
- 이 방식은 세션 변경 시 자동으로 업데이트됩니다 (반응형!)

### 🧭 네비게이션 설정

페이지들을 연결하고 메뉴에 표시!

```python
app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(write_page, title="Write", icon="pencil"),
    vl.Page(my_posts_page, title="My Posts", icon="note-sticky"),
    vl.Page(login_page, title="Login/Info", icon="person"),
    vl.Page(register_page, title="Register", icon="person-plus"),
], reactivity_mode=True)
```

**🔍 설명:**

- **`vl.Page()`**: 페이지를 등록 (함수, 제목, 아이콘)
- **`icon="..."`**: 부트스트랩 아이콘 이름 (자동으로 예쁜 아이콘 표시!)
- **My Posts 페이지**: 내가 쓴 글만 모아보는 전용 페이지 추가!

---

## 🚀 9단계: 앱 실행하기!

마지막으로 앱을 실행하는 코드를 추가해요!

```python
if __name__ == "__main__":
    print("Violit Blog server starting...")
    app.run()
```

**🔍 설명:**

- **`if __name__ == "__main__"`**: 이 파일을 직접 실행할 때만 작동 (다른 파일에서 import 하면 실행 안 됨)
- **`app.run()`**: 서버 시작! 기본적으로 `http://localhost:8000`에서 실행돼요

---

## 🎉 완성! 이제 실행해 보세요!

### 💻 실행 방법

터미널을 열고 다음 명령어를 입력하세요:

```bash
python violit_blog.py
```

### 🌐 접속하기

브라우저를 열고 주소창에 입력:

```
http://localhost:8000
```

### 🎊 축하합니다!

여러분의 첫 블로그가 완성되었습니다! 이제:

1. **회원가입** 버튼을 눌러 계정 만들기
2. **로그인** 하기
3. **글 쓰기** 페이지에서 첫 글 작성
4. **홈** 페이지에서 글 목록 확인
5. **더 읽기** 버튼으로 상세 내용 보기
6. **My Posts** 페이지에서 내 글만 모아보기
7. 내가 쓴 글을 **삭제**해보기

---

## 🎓 무엇을 배웠나요?

이 튜토리얼을 통해 다음을 배웠습니다:

### 💡 웹 개발 개념
- **프론트엔드**: 사용자가 보는 화면 (Violit이 자동으로 만들어줌!)
- **백엔드**: 데이터 저장 및 로직 (우리가 작성한 파이썬 코드)
- **데이터베이스**: 정보를 저장하는 곳 (SQLite)

### 🛠️ Violit 핵심 기능
- **`app.state()`**: 반응형 상태 관리
- **`app.text_input()`, `app.text_area()`**: 입력 받기
- **`app.button(on_click=...)`**: 클릭 이벤트 처리
- **`app.container()`**: 레이아웃 구성
- **`app.navigation()`**: 멀티 페이지 앱 만들기

### 🎯 파이썬 프로그래밍
- 함수 정의 (`def`)
- 조건문 (`if-else`)
- 반복문 (`for`)
- 예외 처리 (`try-except`)
- SQLite 데이터베이스 사용

---

## 🚀 다음 단계: 더 발전시키기

### 💪 도전 과제

1. **댓글 기능 추가**: `comments` 테이블 만들고 글마다 댓글 달기
2. **좋아요 버튼**: 각 글에 좋아요 개수 표시
3. **검색 기능**: 제목이나 내용으로 글 검색
4. **프로필 사진**: 사용자마다 이미지 업로드
5. **비밀번호 암호화**: `bcrypt` 라이브러리로 보안 강화 (habit_tracker 참고!)

### 📚 더 배우기

- **Violit 공식 문서**: 다른 위젯들 탐색하기
- **SQL 튜토리얼**: 더 복잡한 쿼리 작성법
- **CSS 커스터마이징**: `style="..."` 속성으로 디자인 꾸미기

---

# 🎓 ADVANCED TUTORIAL: 테마 설정 기능 추가하기

## 🌈 이제 진짜 강력한 기능을 보여드릴게요!

기본 블로그를 완성했다면, 이제 **사용자별 UI 커스터마이징**을 추가해볼까요? 

Violit의 진짜 힘은 바로 여기에 있습니다. **단 몇 줄의 코드로** 전체 블로그의 테마를 바꾸고, 사용자마다 다르게 저장할 수 있어요!

### 🎯 이번에 추가할 기능

- ⚙️ **설정 페이지**: 테마를 선택할 수 있는 메뉴
- 🎨 **6가지 테마**: light, dark, ocean, sunset, forest, cyberpunk
- 💾 **자동 저장**: 선택한 테마를 DB에 저장
- 🔄 **자동 적용**: 로그인하면 내 테마가 자동으로 적용!

### 🤔 왜 이게 대단한가요?

다른 프레임워크에서 테마 기능을 추가하려면:
- CSS 파일 여러 개 작성 (수백 줄)
- JavaScript로 테마 전환 로직 구현
- 복잡한 상태 관리 시스템
- 로컬스토리지 또는 DB 연동

**Violit에서는?** → `app.set_theme("dark")` 한 줄! 🎉

---

## 🔨 Step 1: 데이터베이스에 설정 테이블 추가

기존 `init_db()` 함수를 수정해서 `settings` 테이블을 추가합니다.

```python
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 기존 테이블들...
    c.execute('''CREATE TABLE IF NOT EXISTS users ...''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts ...''')
    
    # 🎨 설정 테이블 추가!
    c.execute('''CREATE TABLE IF NOT EXISTS settings 
                 (user_id INTEGER PRIMARY KEY, 
                  theme_name TEXT DEFAULT 'ocean')''')
    
    conn.commit()
    conn.close()
```

**🔍 설명:**
- `user_id`를 PRIMARY KEY로 (한 사용자당 하나의 설정)
- `theme_name`에 기본값 'ocean' 설정

---

## 🔨 Step 2: 테마 저장/불러오기 함수 만들기

DB와 통신하는 헬퍼 함수를 추가합니다.

```python
def get_user_theme(user_id):
    """사용자의 저장된 테마 가져오기"""
    result = db_query("SELECT theme_name FROM settings WHERE user_id = ?", 
                      (user_id,), fetch=True)
    return result[0]['theme_name'] if result else 'ocean'

def save_user_theme(user_id, theme_name):
    """사용자의 테마 저장하기"""
    # INSERT OR REPLACE: 있으면 업데이트, 없으면 추가 (UPSERT)
    db_query("INSERT OR REPLACE INTO settings (user_id, theme_name) VALUES (?, ?)", 
             (user_id, theme_name))
```

**🔍 핵심 개념:**
- **UPSERT**: Update + Insert의 합성어! 똑똑하게 처리해줘요
- 없으면 기본값 'ocean' 반환

---

## 🔨 Step 3: 설정 페이지 만들기

완전히 새로운 페이지를 추가합니다!

```python
def settings_page():
    s = session.value
    app.header("Settings")
    
    # 로그인 체크
    if not s['is_logged_in']:
        app.warning("Login required.")
        return
    
    with app.container(border=True):
        app.subheader("Change Theme")
        app.text("You can change the blog color theme.")
        
        # 사용 가능한 테마 목록
        available_themes = ["light", "dark", "ocean", "sunset", "forest", "cyberpunk"]
        
        # 현재 저장된 테마 가져오기
        current_theme = get_user_theme(s['user_id'])
        
        # 드롭다운 선택 상자
        theme_select = app.selectbox(
            "Select Theme",
            available_themes,
            index=available_themes.index(current_theme) if current_theme in available_themes else 0,  # 현재 테마를 기본 선택
            key="theme_selector"
        )
        
        # 적용 버튼 클릭 시 실행
        def apply_theme():
            selected = theme_select.value
            app.set_theme(selected)  # 🎨 테마 즉시 변경!
            save_user_theme(s['user_id'], selected)  # 💾 DB에 저장!
            app.toast(f"'{selected}' theme applied!", variant="success")
        
        app.button("Apply Theme", on_click=apply_theme, variant="primary", size="large")
        
        app.divider()
        app.caption("Theme will be auto-applied on next login!")
```

**🔍 핵심 포인트:**

1. **`app.selectbox()`**: 드롭다운 메뉴 (선택 상자)
2. **`index=...`**: 현재 테마를 기본 선택된 상태로 표시
3. **`app.set_theme()`**: 단 한 줄로 전체 UI 색상 변경! 🪄
4. **`save_user_theme()`**: DB에 저장해서 다음에도 유지

---

## 🔨 Step 4: 로그인 시 테마 자동 적용

`login_page()`의 `do_login()` 함수를 수정합니다.

```python
def do_login():
    users = db_query("SELECT id, username FROM users WHERE username = ? AND password = ?", 
                     (username.value, password.value), fetch=True)
    if users:
        user = users[0]
        session.set({
            **session.value,
            'is_logged_in': True,
            'user_id': user['id'],
            'username': user['username']
        })
        
        # 🎨 로그인 시 사용자의 테마 자동 적용! (NEW!)
        user_theme = get_user_theme(user['id'])
        app.set_theme(user_theme)
        
        app.toast(f"Welcome, {user['username']}!", variant="success")
    else:
        app.toast("Invalid username or password.", variant="danger")
```

**🔍 마법 같은 순간:**

로그인하는 순간, 내가 저장한 테마가 자동으로 적용돼요! 다른 사용자는 다른 테마를 볼 수 있죠. 😎

---

## 🔨 Step 5: 네비게이션에 설정 페이지 추가

메뉴에 "설정" 버튼을 추가합니다.

```python
app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(write_page, title="Write", icon="pencil"),
    vl.Page(my_posts_page, title="My Posts", icon="note-sticky"),
    vl.Page(settings_page, title="Settings", icon="gear"),  # 🎨 여기 추가!
    vl.Page(login_page, title="Login/Info", icon="person"),
    vl.Page(register_page, title="Register", icon="person-plus"),
])
```

---

## 🔨 Step 6: 사이드바에 현재 테마 표시 (선택사항)

사이드바를 좀 더 멋지게 꾸며봅시다!

```python
with app.sidebar:
    app.markdown("## Violit Advanced")
    app.caption("Theme-Enabled Blog")
    app.divider()
    
    # Dynamic login status display
    def render_user_info():
        s = session.value
        if s['is_logged_in']:
            return f"{s['username']}"
        else:
            return "Please login"
    
    app.simple_card(render_user_info)
```

**🔍 변경 사항:**
- 기본 블로그와 동일하게 `render_user_info()` 함수와 `app.simple_card()` 사용
- Advanced 버전에서는 테마 정보까지 표시하려면 함수 내부에서 `get_user_theme()` 호출 가능

---

## 🎉 완성! Advanced 버전 실행하기

### 💻 실행 방법

```bash
python violit_advanced_blog.py
```

### 🧪 테스트해보기

1. 회원가입하고 로그인
2. **설정** 페이지로 이동
3. 드롭다운에서 다른 테마 선택 (예: cyberpunk)
4. **"테마 적용 및 저장"** 버튼 클릭
5. 화면이 즉시 바뀌는 걸 확인! 🎊
6. 로그아웃 → 다시 로그인
7. 내가 선택한 테마가 자동으로 적용됨! 🤩

---

## 🎓 무엇을 배웠나요?

### 💡 Advanced 개념

1. **UPSERT 패턴**: INSERT OR REPLACE로 스마트하게 저장
2. **사용자별 설정 관리**: 각 사용자마다 다른 설정 저장
3. **실시간 UI 변경**: 페이지 새로고침 없이 테마 변경
4. **세션 기반 상태 유지**: 로그인 시 자동 적용

### 🎨 Violit의 강력함

```python
# 다른 프레임워크: 수백 줄의 CSS + JS
# Violit: 단 한 줄!
app.set_theme("dark")
```

이게 바로 **프레임워크의 힘**입니다! 복잡한 것을 간단하게 만들어주죠.

---

## 🚀 더 나아가기

### 💪 추가 도전 과제

1. **폰트 크기 설정**: 사용자마다 글자 크기 조절
2. **레이아웃 모드**: 그리드 뷰 vs 리스트 뷰 선택
3. **다크모드 자동 전환**: 시간대별 자동 테마 변경
4. **커스텀 색상**: 사용자가 직접 색상 코드 입력

### 🎨 더 많은 Violit 기능

- **`app.set_primary_color()`**: 메인 색상만 바꾸기
- **`app.set_animation_mode()`**: 애니메이션 속도 조절
- **`app.container(style="...")`**: 직접 CSS 스타일 적용

---

## 🌟 축하합니다!

이제 여러분은:

- ✅ 기본 블로그를 만들 수 있고
- ✅ 고급 UI 커스터마이징을 구현할 수 있으며
- ✅ 사용자별 설정을 관리할 수 있고
- ✅ Violit의 강력한 기능을 활용할 수 있습니다!

**Django나 RoR보다 빠르고, 간단하고, 강력하죠?** 😎

---

## 🙌 마무리

이 튜토리얼이 도움이 되었기를 바랍니다! 

Violit은 복잡한 설정 없이 빠르게 웹 앱을 만들 수 있는 강력한 도구예요. Django나 Ruby on Rails처럼 유명한 프레임워크의 편리함을, 파이썬만으로 누릴 수 있죠!

### 📦 완성된 코드

- **Basic Version**: `violit_blog.py` (기본 블로그)
- **Advanced Version**: `violit_advanced_blog.py` (테마 설정 포함)

둘 다 완벽하게 작동하니 비교하며 공부해보세요!

**질문이나 문제가 생기면 주저하지 말고 도움을 요청하세요.** 

Happy Coding! 🎉👨‍💻👩‍💻
