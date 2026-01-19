"""
Violit Advanced Blog - Blog with theme settings
Adds user-specific theme save and auto-apply functionality.
"""

import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import violit as vl

# Database setup

DB_NAME = "blog_advanced.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, content TEXT, 
                  author_name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # Advanced: theme settings table
    c.execute('''CREATE TABLE IF NOT EXISTS settings 
                 (user_id INTEGER PRIMARY KEY, theme_name TEXT DEFAULT 'ocean')''')
    conn.commit()
    conn.close()

def db_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return [dict(r) for r in res] if fetch else None

# Advanced: theme-related functions
def get_user_theme(user_id):
    result = db_query("SELECT theme_name FROM settings WHERE user_id = ?", (user_id,), fetch=True)
    return result[0]['theme_name'] if result else 'ocean'

def save_user_theme(user_id, theme_name):
    db_query("INSERT OR REPLACE INTO settings (user_id, theme_name) VALUES (?, ?)", (user_id, theme_name))

# App and session initialization

init_db()
app = vl.App(title="Violit Advanced Blog", theme="ocean", container_width="800px")

session = app.state({
    'is_logged_in': False,
    'user_id': None,
    'username': '',
    'view_mode': 'list',
    'selected_post_id': None
}, key='blog_session')

# Page implementations

def home_page():
    s = session.value
    app.header("Blog Feed")
    
    if s['view_mode'] == 'detail':
        # Detail view
        post_id = s['selected_post_id']
        posts = db_query("SELECT * FROM posts WHERE id = ?", (post_id,), fetch=True)
        
        if not posts:
            app.error("Post not found.")
            def go_back():
                session.set({**s, 'view_mode': 'list'})
            app.button("Back to list", on_click=go_back)
            return
            
        post = posts[0]
        with app.container(border=True, style="padding: 2rem;"):
            app.subheader(post['title'])
            app.caption(f"{post['author_name']} | {post['created_at']}")
            app.divider()
            app.text(post['content'])
            
            app.divider()
            cols = app.columns(4)
            with cols[0]:
                def go_to_list():
                    session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                app.button("Back to list", on_click=go_to_list, variant="neutral")
            
            if s['is_logged_in'] and s['user_id'] == post['user_id']:
                with cols[3]:
                    def delete_post():
                        db_query("DELETE FROM posts WHERE id = ?", (post['id'],))
                        app.toast("Post deleted.")
                        session.set({**s, 'view_mode': 'list', 'selected_post_id': None})
                    app.button("Delete", on_click=delete_post, variant="danger")
    else:
        # List view
        posts = db_query("SELECT * FROM posts ORDER BY created_at DESC", fetch=True)
        
        if not posts:
            app.info("No posts yet. Write the first post!")
        
        for post in posts:
            with app.container(border=True, style="margin-bottom: 1rem;"):
                app.markdown(f"### {post['title']}")
                app.caption(f"By {post['author_name']} on {post['created_at'][:10]}")
                summary = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                app.text(summary)
                
                def make_view_handler(pid):
                    return lambda: session.set({**session.value, 'view_mode': 'detail', 'selected_post_id': pid})
                app.button("Read more", on_click=make_view_handler(post['id']), variant="text")

def write_page():
    s = session.value
    app.header("Write New Post")
    
    if not s['is_logged_in']:
        app.warning("Login required.")
        return

    with app.container():
        title = app.text_input("Title", placeholder="Enter title", key="new_post_title")
        content = app.text_area("Content", placeholder="Tell your story...", rows=10, key="new_post_content")
        
        def save_post():
            if not title.value.strip() or not content.value.strip():
                app.toast("Please enter both title and content.", variant="danger")
                return
            db_query("INSERT INTO posts (user_id, author_name, title, content) VALUES (?, ?, ?, ?)",
                     (s['user_id'], s['username'], title.value, content.value))
            app.toast("Post published successfully!", variant="success")
            title.set("")
            content.set("")
            session.set({**session.value, 'view_mode': 'list'})
        
        app.button("Publish", on_click=save_post, variant="primary", size="large")

def login_page():
    s = session.value
    
    if s['is_logged_in']:
        app.header("My Info")
        app.success(f"Hello, **{s['username']}**!")
        
        def logout():
            session.set({
                'is_logged_in': False, 'user_id': None, 'username': '',
                'view_mode': 'list', 'selected_post_id': None
            })
            app.toast("Logged out.")
        app.button("Logout", on_click=logout, variant="neutral")
        return

    app.header("Login")
    with app.container():
        username = app.text_input("Username", key="login_username")
        password = app.text_input("Password", type="password", key="login_password")
        
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
                # Advanced: auto-apply user theme on login
                user_theme = get_user_theme(user['id'])
                app.set_theme(user_theme)
                app.toast(f"Welcome, {user['username']}!", variant="success")
            else:
                app.toast("Invalid username or password.", variant="danger")
        
        app.button("Login", on_click=do_login, variant="primary")

def register_page():
    app.header("Register")
    
    if session.value['is_logged_in']:
        app.info("Already logged in.")
        return

    with app.container():
        username = app.text_input("Username", key="reg_username")
        password = app.text_input("Password", type="password", key="reg_password")
        
        def do_register():
            if not username.value or not password.value:
                app.toast("Please enter username and password.", variant="danger")
                return
            try:
                db_query("INSERT INTO users (username, password) VALUES (?, ?)", 
                         (username.value, password.value))
                app.toast("Registration successful! Please login.", variant="success")
            except sqlite3.IntegrityError:
                app.toast("Username already exists.", variant="danger")
        
        app.button("Register", on_click=do_register, variant="primary")

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

# Advanced: theme settings page
def settings_page():
    s = session.value
    app.header("Settings")
    
    if not s['is_logged_in']:
        app.warning("Login required.")
        return
    
    with app.container(border=True):
        app.subheader("Change Theme")
        app.text("You can change the blog color theme.")
        
        available_themes = ["light", "dark", "ocean", "sunset", "forest", "cyberpunk"]
        current_theme = get_user_theme(s['user_id'])
        
        theme_select = app.selectbox(
            "Select Theme",
            available_themes,
            index=available_themes.index(current_theme) if current_theme in available_themes else 0,
            key="theme_selector"
        )
        
        def apply_theme():
            selected = theme_select.value
            app.set_theme(selected)
            save_user_theme(s['user_id'], selected)
            app.toast(f"'{selected}' theme applied!", variant="success")
        
        app.button("Apply Theme", on_click=apply_theme, variant="primary", size="large")
        
        app.divider()
        app.caption("Theme will be auto-applied on next login!")

# Sidebar and navigation

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

app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(write_page, title="Write", icon="pencil"),
    vl.Page(my_posts_page, title="My Posts", icon="journal-text"),
    vl.Page(settings_page, title="Settings", icon="gear"),
    vl.Page(login_page, title="Login/Info", icon="person"),
    vl.Page(register_page, title="Register", icon="person-plus"),
])

if __name__ == "__main__":
    print("Violit Advanced Blog server starting...")
    app.run()
