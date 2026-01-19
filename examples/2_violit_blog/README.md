# 🚀 Build Your Own Blog in 10 Minutes with Violit!

## 👋 Welcome!

Hello! New to web development? Don't worry. Follow this tutorial and you'll create a **fully functional blog**! 😊

### 🤔 What is a "Framework"?

Think of a framework like a **"LEGO block set"**. Instead of making each brick when building a house, you assemble pre-made blocks.

- **Django, Ruby on Rails**: Famous but complex to set up 😵
- **Violit**: Just know Python and you're good to go! Minimal setup required 🎉

### 🎯 Features We'll Build

By the end of this tutorial, your blog will have:

- ✅ **User Registration**: Create new user accounts
- ✅ **Login/Logout**: Access and exit your account
- ✅ **Write Posts**: Publish posts with title and content
- ✅ **List View**: See all posts at a glance
- ✅ **Detail View**: Click to read full posts
- ✅ **Delete Posts**: Remove only your own posts

It works like a real blog! 🎊

---

## 🏗️ Step 1: Setup (Import Required Tools)

### 📦 What are Libraries?

Libraries are **collections of useful tools made by others**. We don't need to build everything from scratch!

Create a file called `violit_blog.py` and add the following code:

```python
import sys
import os
import sqlite3

# Add Violit library path (if violit is in parent folder)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import violit as vl
```

**🔍 What this code does:**
- `sqlite3`: Database to store data (explained later!)
- `violit as vl`: Our super framework! We'll call it `vl` for short

**💡 Tip:** The `sys.path.append` part tells Python where to find Violit. If you installed Violit via `pip install`, you can skip this line!

---

## 🗄️ Step 2: Create Database (Storage for Posts and Users)

### 📚 What is a Database?

A database is like **an Excel spreadsheet that organizes information**.
- **Users sheet**: User ID, password
- **Posts sheet**: Post title, content, author

We use **SQLite**. It's built into Python, no installation needed! 👍

```python
DB_NAME = "blog_app.db"

def init_db():
    """Initialize database - runs once at startup"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT)''')
    
    # Create posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  title TEXT, 
                  content TEXT, 
                  author_name TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Helper function for easy database queries
def db_query(query, params=(), fetch=False):
    """Query database and get results"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # To use like a dictionary
    c = conn.cursor()
    c.execute(query, params)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return [dict(r) for r in res] if fetch else None
```

**🔍 Code Explanation:**

1. **`CREATE TABLE IF NOT EXISTS`**: Create table if it doesn't exist, otherwise skip
2. **`PRIMARY KEY AUTOINCREMENT`**: Automatically increment ID as 1, 2, 3...
3. **`UNIQUE`**: No duplicate usernames allowed! (Can't register twice with same ID)
4. **`db_query()` function**: Helper function to avoid writing long code repeatedly!

**💬 Understanding with Examples:**
```
users table looks like this:
┌────┬──────────┬──────────┐
│ id │ username │ password │
├────┼──────────┼──────────┤
│ 1  │ alice    │ 1234     │
│ 2  │ bob      │ abcd     │
└────┴──────────┴──────────┘
```

---

## 🎨 Step 3: Create App and Manage State

### 🧠 What is "State"?

State is **what the app remembers**. For example:
- "Who is currently logged in?"
- "Which post are we viewing?"

This information is stored in **memory**!

```python
# Initialize database (runs once)
init_db()

# Create app!
app = vl.App(
    title="Violit Blog",          # Title shown in browser tab
    theme="ocean",                # Ocean theme (blue tones)
    container_width="800px"       # Limit screen width (mobile-like)
)

# Session state: Information managed separately per user
session = app.state({
    'is_logged_in': False,        # Are you logged in? (False initially)
    'user_id': None,              # User ID number
    'username': '',               # Username
    'view_mode': 'list',          # Screen mode: 'list' or 'detail'
    'selected_post_id': None      # ID of currently viewing post
}, key='blog_session')
```

**🔍 Understanding:**
- **`app.state()`**: Violit's magic! When this value changes, the screen automatically updates 🪄
- **`key='blog_session'`**: Uniquely stored per session (won't conflict even with multiple users!)

---

## 🏠 Step 4: Create Main Page (Post List + Detail View)

Now for the important part! Let's create the **home page** users see first.

### 🎭 A Page with Two Faces

The home page has **two modes**:
1. **List mode**: Show all posts as cards
2. **Detail mode**: Display one post in full

```python
def home_page():
    s = session.value  # Get current session info (we'll call it 's' for short)
    
    app.header("Blog Feed")  # Main title
    
    if s['view_mode'] == 'detail':
        # ========== DETAIL VIEW ==========
        post_id = s['selected_post_id']
        posts = db_query("SELECT * FROM posts WHERE id = ?", (post_id,), fetch=True)
        
        if not posts:
            app.error("Post not found.")
            def go_back():
                session.set({**s, 'view_mode': 'list'})
            app.button("Back to list", on_click=go_back)
            return
        
        post = posts[0]
        
        # Display post content in a nice container
        with app.container(border=True, style="padding: 2rem;"):
            app.subheader(post['title'])  # Post title
            app.caption(f"{post['author_name']} | {post['created_at']}")
            app.divider()  # Divider line
            app.text(post['content'])  # Post content
            
            app.divider()
            
            # Arrange buttons horizontally
            cols = app.columns(4)  # Divide into 4 columns
            
            with cols[0]:  # First column
                def go_to_list():
                    # Return to list mode
                    session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                app.button("Back to list", on_click=go_to_list, variant="neutral")
            
            # Show delete button if it's your post
            if s['is_logged_in'] and s['user_id'] == post['user_id']:
                with cols[3]:  # Fourth column (far right)
                    def delete_post():
                        db_query("DELETE FROM posts WHERE id = ?", (post['id'],))
                        app.toast("Post deleted.")
                        session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                    
                    app.button("Delete", on_click=delete_post, variant="danger")
    
    else:
        # ========== LIST VIEW ==========
        posts = db_query("SELECT * FROM posts ORDER BY created_at DESC", fetch=True)
        
        if not posts:
            app.info("No posts yet. Write the first post!")
        
        # Display all posts as cards
        for post in posts:
            with app.container(border=True, style="margin-bottom: 1rem;"):
                app.markdown(f"### {post['title']}")  # Title (large)
                app.caption(f"By {post['author_name']} on {post['created_at'][:10]}")
                
                # Summary (first 100 characters only)
                summary = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                app.text(summary)
                
                # "Read more" button - click to go to detail view!
                def make_view_handler(pid):
                    """Closure pattern: Each button remembers its own post_id"""
                    return lambda: session.set({**session.value, 'view_mode': 'detail', 'selected_post_id': pid})
                
                app.button("Read more", on_click=make_view_handler(post['id']), variant="text")
```

**🔍 Key Concepts:**

1. **`session.value`**: Read current state
2. **`session.set()`**: Change state → Screen automatically updates!
3. **`with app.container()`**: Put content inside a box (clean!)
4. **`app.columns(4)`**: Divide screen into 4 columns (for button layout)
5. **`on_click=function`**: Execute function when button is clicked!

**💬 Why use `make_view_handler`?**

When creating buttons in a loop, each button needs to remember **its own post_id**. So we create an extra function to "capture" the value. (This is called a closure!)

---

## ✍️ Step 5: Create Write Page

Now let's create a page where users can write their posts!

```python
def write_page():
    s = session.value
    app.header("Write New Post")
    
    # Show warning message if not logged in
    if not s['is_logged_in']:
        app.warning("Login required.")
        return  # End function here!
    
    with app.container():
        # Create input form
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
        
        # Function to run when save button is clicked
        def save_post():
            # Validate empty fields
            if not title.value.strip() or not content.value.strip():
                app.toast("Please enter both title and content.", variant="danger")
                return
            
            # Save to database
            db_query(
                "INSERT INTO posts (user_id, author_name, title, content) VALUES (?, ?, ?, ?)",
                (s['user_id'], s['username'], title.value, content.value)
            )
            
            app.toast("Post published successfully!", variant="success")
            
            # Clear input fields
            title.set("")
            content.set("")
            
            # Return to home screen (list)
            session.set({**session.value, 'view_mode': 'list'})
        
        app.button("Publish", on_click=save_post, variant="primary", size="large")
```

**🔍 Key Points:**

1. **`app.text_input()`**: Single-line input (for title)
2. **`app.text_area()`**: Multi-line input (for content)
3. **`key="..."`**: Unique name for each input (must not duplicate!)
4. **`.value`**: Read user's input value
5. **`.set("")`**: Clear input field

**💡 Fun Fact:** `app.toast()` displays a nice notification in the top-right corner, like toast popping up! 🍞

---

## 🔐 Step 6: Login & Registration Pages

### 🚪 Login Page

The door where users enter their account!

```python
def login_page():
    s = session.value
    
    # If already logged in - show my info
    if s['is_logged_in']:
        app.header("My Info")
        app.success(f"Hello, **{s['username']}**!")
        
        def logout():
            # Reset session (logout)
            session.set({
                'is_logged_in': False,
                'user_id': None,
                'username': '',
                'view_mode': 'list',
                'selected_post_id': None
            })
            app.toast("Logged out.")
        
        app.button("Logout", on_click=logout, variant="neutral")
        return  # End here!
    
    # If not logged in - show login form
    app.header("Login")
    
    with app.container():
        username = app.text_input("Username", key="login_username")
        password = app.text_input(
            "Password", 
            type="password",  # Display password as ***
            key="login_password"
        )
        
        def do_login():
            # Find user in database
            users = db_query(
                "SELECT id, username FROM users WHERE username = ? AND password = ?",
                (username.value, password.value),
                fetch=True
            )
            
            if users:
                user = users[0]
                # Login successful! Save info to session
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

**🔍 Explanation:**

- **`type="password"`**: Display entered text as `***` (security!)
- **`**session.value`**: Spread existing session data and modify only parts (Python syntax)

---

### 📝 Registration Page

Where new users create accounts!

```python
def register_page():
    app.header("Register")
    
    # No need to register if already logged in
    if session.value['is_logged_in']:
        app.info("Already logged in.")
        return

    with app.container():
        username = app.text_input("Username", key="reg_username")
        password = app.text_input("Password", type="password", key="reg_password")
        
        def do_register():
            # Check for empty fields
            if not username.value or not password.value:
                app.toast("Please enter username and password.", variant="danger")
                return
            
            try:
                # Add new user to database
                db_query(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username.value, password.value)
                )
                app.toast("Registration successful! Please login.", variant="success")
            except sqlite3.IntegrityError:
                # UNIQUE constraint violation = username already exists
                app.toast("Username already exists.", variant="danger")
        
        app.button("Register", on_click=do_register, variant="primary")
```

**🔍 Key Points:**

- **`try-except`**: Safely execute code that might cause errors
- **`IntegrityError`**: Error that occurs when trying to register with a duplicate username

---

## 👤 Step 7: Create My Posts Page

Create a page where logged-in users can view only their own posts!

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

**🔍 Key Points:**

1. **User filtering**: Get only your posts with `WHERE user_id = ?`
2. **Similar structure to home**: Supports both list and detail views
3. **Post count display**: Show number of posts with `app.success()`
4. **Delete permission**: Can delete all your own posts!

---

## 🎨 Step 8: Sidebar & Navigation (Connect All Pages)

Now let's tie all pages together to complete the app!

### 📱 Create Sidebar

The menu bar on the left side of the screen!

```python
with app.sidebar:
    app.markdown("## Violit Blog")
    app.caption("Simple & Fast")
    app.divider()  # Divider line
    
    # Dynamic login status display
    def render_user_info():
        s = session.value
        if s['is_logged_in']:
            return f"{s['username']}"
        else:
            return "Please login"
    
    app.simple_card(render_user_info)
```

**🔍 Explanation:**
- **`render_user_info()` function**: Returns content to display dynamically based on session state
- **`app.simple_card()`**: Pass a function and it displays it nicely as a card!
- This method automatically updates when session changes (reactive!)

### 🧭 Navigation Setup

Connect pages and display in menu!

```python
app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(write_page, title="Write", icon="pencil"),
    vl.Page(my_posts_page, title="My Posts", icon="journal-text"),
    vl.Page(login_page, title="Login/Info", icon="person"),
    vl.Page(register_page, title="Register", icon="person-plus"),
])
```

**🔍 Explanation:**

- **`vl.Page()`**: Register a page (function, title, icon)
- **`icon="..."`**: Bootstrap icon name (automatically displays nice icons!)
- **My Posts page**: Dedicated page to view only your posts!

---

## 🚀 Step 9: Run the App!

Finally, add code to run the app!

```python
if __name__ == "__main__":
    print("Violit Blog server starting...")
    app.run()
```

**🔍 Explanation:**

- **`if __name__ == "__main__"`**: Only runs when this file is directly executed (won't run if imported from another file)
- **`app.run()`**: Start server! By default runs at `http://localhost:8000`

---

## 🎉 Complete! Let's Run It!

### 💻 How to Run

Open terminal and enter:

```bash
python violit_blog.py
```

### 🌐 Access

Open browser and enter in address bar:

```
http://localhost:8000
```

### 🎊 Congratulations!

Your first blog is complete! Now:

1. Click **Register** button to create an account
2. **Login**
3. **Write** your first post from the Write page
4. Check post list on **Home** page
5. Click **Read more** button to view full content
6. View only your posts on **My Posts** page
7. Try **deleting** your posts

---

## 🎓 What Did We Learn?

Through this tutorial, you learned:

### 💡 Web Development Concepts
- **Frontend**: The screen users see (Violit creates it automatically!)
- **Backend**: Data storage and logic (the Python code we wrote)
- **Database**: Where information is stored (SQLite)

### 🛠️ Core Violit Features
- **`app.state()`**: Reactive state management
- **`app.text_input()`, `app.text_area()`**: Get user input
- **`app.button(on_click=...)`**: Handle click events
- **`app.container()`**: Compose layouts
- **`app.navigation()`**: Create multi-page apps

### 🎯 Python Programming
- Function definition (`def`)
- Conditionals (`if-else`)
- Loops (`for`)
- Exception handling (`try-except`)
- Using SQLite database

---

## 🚀 Next Steps: Level Up

### 💪 Challenge Tasks

1. **Add Comments**: Create `comments` table and add comments to posts
2. **Like Button**: Display like count for each post
3. **Search Feature**: Search posts by title or content
4. **Profile Pictures**: Upload images per user
5. **Password Encryption**: Enhance security with `bcrypt` library (see habit_tracker!)

### 📚 Learn More

- **Violit Official Docs**: Explore other widgets
- **SQL Tutorial**: Learn more complex queries
- **CSS Customization**: Style designs with `style="..."` attribute

---

# 🎓 ADVANCED TUTORIAL: Adding Theme Settings

## 🌈 Now Let's Show You the Real Power!

Once you've completed the basic blog, let's add **per-user UI customization**!

This is where Violit's true power shines. With **just a few lines of code**, you can change the entire blog theme and save it differently per user!

### 🎯 Features to Add

- ⚙️ **Settings Page**: Menu to select themes
- 🎨 **6 Themes**: light, dark, ocean, sunset, forest, cyberpunk
- 💾 **Auto-save**: Save selected theme to DB
- 🔄 **Auto-apply**: Your theme applies automatically on login!

### 🤔 Why is This Amazing?

To add theme features in other frameworks:
- Write multiple CSS files (hundreds of lines)
- Implement theme switching logic in JavaScript
- Complex state management system
- Local storage or DB integration

**In Violit?** → Just one line: `app.set_theme("dark")`! 🎉

---

## 🔨 Step 1: Add Settings Table to Database

Modify the existing `init_db()` function to add a `settings` table.

```python
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Existing tables...
    c.execute('''CREATE TABLE IF NOT EXISTS users ...''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts ...''')
    
    # 🎨 Add settings table!
    c.execute('''CREATE TABLE IF NOT EXISTS settings 
                 (user_id INTEGER PRIMARY KEY, 
                  theme_name TEXT DEFAULT 'ocean')''')
    
    conn.commit()
    conn.close()
```

**🔍 Explanation:**
- `user_id` as PRIMARY KEY (one setting per user)
- Default value 'ocean' for `theme_name`

---

## 🔨 Step 2: Create Theme Save/Load Functions

Add helper functions to communicate with DB.

```python
def get_user_theme(user_id):
    """Get user's saved theme"""
    result = db_query("SELECT theme_name FROM settings WHERE user_id = ?", 
                      (user_id,), fetch=True)
    return result[0]['theme_name'] if result else 'ocean'

def save_user_theme(user_id, theme_name):
    """Save user's theme"""
    # INSERT OR REPLACE: Update if exists, insert if not (UPSERT)
    db_query("INSERT OR REPLACE INTO settings (user_id, theme_name) VALUES (?, ?)", 
             (user_id, theme_name))
```

**🔍 Key Concept:**
- **UPSERT**: Update + Insert combined! Handles it smartly
- Returns default value 'ocean' if not found

---

## 🔨 Step 3: Create Settings Page

Add a completely new page!

```python
def settings_page():
    s = session.value
    app.header("Settings")
    
    # Check login
    if not s['is_logged_in']:
        app.warning("Login required.")
        return
    
    with app.container(border=True):
        app.subheader("Change Theme")
        app.text("You can change the blog color theme.")
        
        # Available themes list
        available_themes = ["light", "dark", "ocean", "sunset", "forest", "cyberpunk"]
        
        # Get currently saved theme
        current_theme = get_user_theme(s['user_id'])
        
        # Dropdown selection box
        theme_select = app.selectbox(
            "Select Theme",
            available_themes,
            index=available_themes.index(current_theme) if current_theme in available_themes else 0,  # Default to current theme
            key="theme_selector"
        )
        
        # Execute when apply button is clicked
        def apply_theme():
            selected = theme_select.value
            app.set_theme(selected)  # 🎨 Change theme instantly!
            save_user_theme(s['user_id'], selected)  # 💾 Save to DB!
            app.toast(f"'{selected}' theme applied!", variant="success")
        
        app.button("Apply Theme", on_click=apply_theme, variant="primary", size="large")
        
        app.divider()
        app.caption("Theme will be auto-applied on next login!")
```

**🔍 Key Points:**

1. **`app.selectbox()`**: Dropdown menu (selection box)
2. **`index=...`**: Display current theme as default selection
3. **`app.set_theme()`**: Change entire UI color with just one line! 🪄
4. **`save_user_theme()`**: Save to DB to persist for next time

---

## 🔨 Step 4: Auto-apply Theme on Login

Modify the `do_login()` function in `login_page()`.

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
        
        # 🎨 Auto-apply user's theme on login! (NEW!)
        user_theme = get_user_theme(user['id'])
        app.set_theme(user_theme)
        
        app.toast(f"Welcome, {user['username']}!", variant="success")
    else:
        app.toast("Invalid username or password.", variant="danger")
```

**🔍 Magical Moment:**

The moment you log in, your saved theme automatically applies! Different users can see different themes. 😎

---

## 🔨 Step 5: Add Settings Page to Navigation

Add "Settings" button to menu.

```python
app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(write_page, title="Write", icon="pencil"),
    vl.Page(my_posts_page, title="My Posts", icon="journal-text"),
    vl.Page(settings_page, title="Settings", icon="gear"),  # 🎨 Added here!
    vl.Page(login_page, title="Login/Info", icon="person"),
    vl.Page(register_page, title="Register", icon="person-plus"),
])
```

---

## 🔨 Step 6: Display Current Theme in Sidebar (Optional)

Let's make the sidebar look even better!

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

**🔍 Changes:**
- Same as basic blog using `render_user_info()` function and `app.simple_card()`
- In Advanced version, you can call `get_user_theme()` inside the function to also display theme info

---

## 🎉 Complete! Run Advanced Version

### 💻 How to Run

```bash
python violit_advanced_blog.py
```

### 🧪 Test It Out

1. Register and login
2. Go to **Settings** page
3. Select a different theme from dropdown (e.g., cyberpunk)
4. Click **"Apply Theme"** button
5. See the screen change instantly! 🎊
6. Logout → Login again
7. Your selected theme applies automatically! 🤩

---

## 🎓 What Did We Learn?

### 💡 Advanced Concepts

1. **UPSERT Pattern**: Smart saving with INSERT OR REPLACE
2. **Per-user Settings Management**: Store different settings per user
3. **Real-time UI Changes**: Change theme without page refresh
4. **Session-based State Persistence**: Auto-apply on login

### 🎨 Violit's Power

```python
# Other frameworks: Hundreds of lines of CSS + JS
# Violit: Just one line!
app.set_theme("dark")
```

This is **the power of frameworks**! Making complex things simple.

---

## 🚀 Going Further

### 💪 Additional Challenges

1. **Font Size Settings**: Adjust text size per user
2. **Layout Mode**: Choose between grid view vs list view
3. **Auto Dark Mode**: Automatically switch theme by time of day
4. **Custom Colors**: Let users input their own color codes

### 🎨 More Violit Features

- **`app.set_primary_color()`**: Change only main color
- **`app.set_animation_mode()`**: Adjust animation speed
- **`app.container(style="...")`**: Apply custom CSS styles

---

## 🌟 Congratulations!

Now you can:

- ✅ Build a basic blog
- ✅ Implement advanced UI customization
- ✅ Manage per-user settings
- ✅ Utilize Violit's powerful features!

**Faster, simpler, and more powerful than Django or RoR, right?** 😎

---

## 🙌 Conclusion

We hope this tutorial was helpful!

Violit is a powerful tool for quickly building web apps without complex setup. You can enjoy the convenience of famous frameworks like Django and Ruby on Rails using just Python!

### 📦 Completed Code

- **Basic Version**: `violit_blog.py` (basic blog)
- **Advanced Version**: `violit_advanced_blog.py` (with theme settings)

Both work perfectly, so compare them while studying!

**Don't hesitate to ask for help if you have questions or problems.**

Happy Coding! 🎉👨‍💻👩‍💻
