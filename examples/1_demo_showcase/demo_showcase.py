
import violit as vl
import pandas as pd
import numpy as np
import random
import sys

# Detect mode
mode = 'lite' if '--lite' in sys.argv else 'ws'

# Initialize App
# This will handle --conservative flag internally if passed
# Set container_width='1200px' to display wider with sidebar
app = vl.App(title="Violit Showcase", mode=mode, theme='violit_light_jewel', container_width='1200px')

# --- State Management ---
chat_history = app.state([
    {"role": "assistant", "content": "Welcome to the Violit Showcase! I'm your virtual assistant."}
], key="chat_history")

# Dashboard Data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

# --- Pages ---

def home_page():
    app.header("Violit Showcase")
    
    if getattr(app, 'conservative_mode', False):
         app.info("**Conservative Mode Active**: Navigation and interactions re-run entire reactive scopes (Streamlit-style).")
    else:
         app.success("**Progressive Mode Active**: No top-level fragments. Reactivity is handled via explicit lambdas/callbacks for maximum performance.")

    app.text("Welcome to the comprehensive demo of Violit capabilities.", size="large")
    
    app.divider()
    
    c1, c2 = app.columns(2)
    with c1:
        app.image("https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", caption="Digital Technology (Unsplash)", use_column_width=True)
    with c2:
        app.subheader("Key Features")
        app.success("Fast Development")
        app.info("Reactive Components (Lambda-based)")
        app.warning("Interactive Widgets")
        
        app.text("Violit bridges the gap between simple scripts and complex web apps.")
        
    app.divider()
    app.card(lambda: "<h3>Ready to explore?</h3><p>Use the sidebar navigation to visit different sections.</p>")

def dashboard_page():
    app.header("Interactive Dashboard")
    
    # Metrics
    c1, c2, c3, c4 = app.columns(4)
    with c1: app.metric("Revenue", "$54,230", "+12%")
    with c2: app.metric("Users", "1,234", "+5%")
    with c3: app.metric("Bounce Rate", "45%", "-2%")
    with c4: app.metric("Uptime", "99.9%", "0%")
    
    app.divider()
    
    # Charts
    app.subheader("Analytics")
    
    tab1, tab2 = app.tabs(["Line Chart", "Area Chart"])
    
    with tab1:
        app.line_chart(chart_data)
        
    with tab2:
        app.area_chart(chart_data)
        
    app.subheader("Data Overview")
    app.dataframe(chart_data.head(10), height=300)
    
def components_page():
    app.header("Components Gallery")
    
    app.subheader("Input Widgets")
    
    c1, c2 = app.columns(2)
    with c1:
        name = app.text_input("Username", "Guest")
        volume = app.slider("Volume", 0, 100, 50)
        agreed = app.checkbox("I agree to terms", value=True)
    
    with c2:
        flavor = app.selectbox("Favorite Flavor", ["Vanilla", "Chocolate", "Strawberry"])
        bday = app.date_input("Birthday")
        app.color_picker("Accent Color", "#FF0000")
        
    app.divider()
    app.subheader("Feedback (Reactive via Lambda)")
    
    # Progressive (Lambda) Reactivity
    app.text(lambda: f"User: {name.value}, Volume: {volume.value}, Flavor: {flavor.value}")
    
    app.write(lambda: 
        f'<sl-alert variant="success" open>Terms accepted.</sl-alert>' if agreed.value else 
        f'<sl-alert variant="danger" open>Please accept terms.</sl-alert>'
    )
        
    def gen_random():
        n = random.randint(1, 100)
        app.toast(f"Random Number: {n}", icon="dice-5")
        
    app.button("Generate Random Number", on_click=gen_random)

def chat_page():
    app.header("Chat Interface")
    
    def render_chat_log():
        html = ""
        for msg in chat_history.value:
            bg = "var(--sl-bg-card)" if msg["role"] == "assistant" else "transparent"
            border = "1px solid var(--sl-border)" if msg["role"] == "assistant" else "none"
            html += f"""
            <div style="padding:1rem; margin-bottom:0.5rem; background:{bg}; border:{border}; border-radius:0.5rem; display:flex; gap:0.5rem;">
                <div style="font-weight:bold; min-width:80px;">{msg['role'].title()}:</div>
                <div>{msg['content']}</div>
            </div>
            """
        return html

    app.write(render_chat_log)
            
    # Input
    def on_chat(msg):
        if msg:
            # Append user message
            hist = chat_history.value.copy()
            hist.append({"role": "user", "content": msg})
            
            # Simulate response
            responses = [
                "That's interesting!",
                "Tell me more.",
                "I can help with that.",
                "Could you clarify?",
                "Violit is awesome!"
            ]
            reply = random.choice(responses)
            hist.append({"role": "assistant", "content": reply})
            
            chat_history.set(hist)
    
    # Spacer
    app.html('<div style="height: 20px;"></div>')
    app.chat_input("Say something...", on_submit=on_chat)

def reactive_page():
    app.header("Progressive Reactivity")
    app.text("This page demonstrates **Progressive Mode** reactivity using direct lambdas/callbacks instead of fragments.", size="large")
    app.info("In Progressive Mode, logic runs once. Updates happen precisely where you bind them.")

    # 1. Counter Demo
    count = app.state(0, key="reactive_count")
    
    app.subheader("1. Simple Counter")
    col1, col2 = app.columns([1, 2])
    with col1:
        # Binding directly to state in a metric
        app.metric("Count", lambda: str(count.value))
    with col2:
        def inc(): count.set(count.value + 1)
        def dec(): count.set(count.value - 1)
        c1, c2 = app.columns(2)
        with c1: app.button("Increase", on_click=inc, variant="primary")
        with c2: app.button("Decrease", on_click=dec)

    app.divider()

    # 2. Real-time Calculation Demo
    app.subheader("2. Real-time Calculator")
    app.text("Move the sliders to see the sum update instantly.")
    
    c1, c2 = app.columns(2)
    with c1:
        val_a = app.slider("Value A", 0, 100, 30)
    with c2:
        val_b = app.slider("Value B", 0, 100, 70)
        
    # Lambda captures current values on re-render trigger
    app.card(lambda: f"""
        <div style='text-align: center;'>
            <h2 style='margin:0;'>Total Sum</h2>
            <div style='font-size: 3rem; font-weight: bold; color: var(--sl-primary);'>
                {val_a.value + val_b.value}
            </div>
        </div>
    """)

    app.divider()

    # 3. Dynamic Greeting Demo
    user_name = app.state("Explorer", key="reactive_name")
    
    app.subheader("3. Dynamic UI")
    # Bind text_input to state so it updates when state changes too
    name = app.text_input("Enter your name", value=user_name.value)
    
    # Simple callback to sync input to state if needed, though access via name.value is enough for lambda below
    # But if we want to PERSIST name across page reloads via state:
    name.on_change = lambda v: user_name.set(v.value if hasattr(v, 'value') else v)
        
    app.write(lambda: f"""
        <sl-alert variant="success" open>
            <div style="font-size:1.2rem; font-weight:600;">Hello, {name.value}!</div>
        </sl-alert>
    """)
    app.text("This message update is triggered by the text input above.")

    app.divider()

    # 4. For-Loop List Generation (HTML String Approach)
    item_count = app.state(5, key="reactive_items")

    app.subheader("4. Dynamic List Generation")
    app.text("Generating lists via HTML string builder (Progressive Style).")
    
    n = app.slider("Number of items to generate", 1, 15, item_count.value)
    
    app.write(lambda: 
        '<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">' + 
        "".join([
            f'<div class="card">Item #{i+1}</div>' 
            for i in range(n.value)
        ]) + 
        '</div>'
    )


def settings_page():
    app.header("Settings")
    
    app.subheader("Theme Selection")
    # Important: sort the list first, then find index in the SORTED list
    all_themes = sorted(["dark", "light", "ocean", "sunset", "forest", "cyberpunk"])
    default_theme = "light"
    default_index = all_themes.index(default_theme) if default_theme in all_themes else 0
    
    # Use explicit key to persist selection across page re-renders
    t = app.selectbox("Choose Theme", all_themes, index=default_index, key="settings_theme_select")
    
    def apply_theme():
        selected = t.value
        app.set_theme(selected)
        app.toast(f"Theme changed to {selected}", icon="palette")
        
    app.button("Apply Theme", on_click=apply_theme)
        
    app.subheader("Animation")
    anim = app.radio("Animation Mode", ["soft", "hard"])
    
    def on_anim_change(v):
        app.set_animation_mode(anim.value)
        
    # We can bind explicit on_change, or just check value in a reactive block? 
    # In Progressive, checking value in a reactive block works too, but on_change causes side effects immediately.
    # Existing widgets don't always expose easy 'on_change' hook in constructor (some do).
    # Let's use a reactive watcher button or just bind logic.
    # Or simply:
    app.button("Update Animation", on_click=lambda: app.set_animation_mode(anim.value))

# --- Navigation & Sidebar ---

with app.sidebar:
    app.image("https://via.placeholder.com/150x50?text=Violit", width=150)
    app.text("v1.5.0", size="small", muted=True)
    app.divider()

app.navigation([
    vl.Page(home_page, title="Home", icon="house"),
    vl.Page(dashboard_page, title="Dashboard", icon="graph-up"),
    vl.Page(reactive_page, title="Reactive Logic", icon="lightning"),
    vl.Page(components_page, title="Components", icon="puzzle"),
    vl.Page(chat_page, title="Chat", icon="chat"),
    vl.Page(settings_page, title="Settings", icon="gear")
])

if __name__ == "__main__":
    app.run()
