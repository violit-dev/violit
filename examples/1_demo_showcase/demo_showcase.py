import random
import sys

import numpy as np
import pandas as pd

import violit as vl


mode = "lite" if "--lite" in sys.argv else "ws"


app = vl.App(
    title="Violit Showcase",
    mode=mode,
    theme="violit_light_jewel",
    container_width="1200px",
)


chat_history = app.state(
    [
        {
            "role": "assistant",
            "content": (
                "Welcome to the Violit Showcase. This chat demo uses Violit's built-in "
                "chat widgets and only returns pseudo replies, so it is safe to publish "
                "without any real API keys."
            ),
        }
    ],
    key="showcase_chat_history",
)
chat_mode = app.state("streaming", key="showcase_chat_mode")
chat_style = app.state("Builder", key="showcase_chat_style")
dashboard_seed = app.state(0, key="showcase_dashboard_seed")


def _preview_card_html(title: str, mood: str, accent: str, note: str, glow: int) -> str:
    glow_size = 30 + int(glow * 0.55)
    mood_copy = {
        "Soft": "Gentle spacing, softer accents, and a calmer hero feel.",
        "Playful": "Friendly surfaces, lively contrast, and rounded calls to action.",
        "Bold": "Higher contrast, a punchier top border, and a stronger launch card.",
    }
    safe_title = title.strip() or "Violit Studio"
    safe_note = note.strip() or "Reactive widgets, calmer state management, and polished UI surfaces."
    return f"""
    <div style="padding:1.5rem; border-radius:1.8rem; background:linear-gradient(180deg,#FFFFFF 0%, #FAF5FF 100%); border:1px solid #E9D5FF; border-top:8px solid {accent}; box-shadow:0 24px {glow_size}px rgba(109,40,217,0.16);">
      <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin-bottom:1rem;">
        <div>
          <div style="font-size:0.74rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:{accent};">Tailwind-friendly preview</div>
          <h3 style="margin:0.35rem 0 0; font-size:1.45rem; line-height:1.2; color:var(--vl-text);">{safe_title}</h3>
        </div>
        <div style="padding:0.45rem 0.8rem; border-radius:999px; background:{accent}; color:white; font-size:0.78rem; font-weight:700; white-space:nowrap;">{mood}</div>
      </div>
      <p style="margin:0; line-height:1.75; color:var(--vl-text-muted);">{safe_note}</p>
      <div style="margin-top:1rem; padding:1rem; border-radius:1rem; background:white; border:1px dashed #DDD6FE;">
        <div style="font-weight:700; color:var(--vl-text);">Style note</div>
        <div style="margin-top:0.3rem; color:var(--vl-text-muted);">{mood_copy[mood]}</div>
      </div>
    </div>
    """


_HOME_COLORS = {
    "violet":  ("#7C3AED", "#F5F3FF", "#E9D5FF", "Violet"),
    "blue":    ("#2563EB", "#EFF6FF", "#DBEAFE", "Blue"),
    "emerald": ("#059669", "#ECFDF5", "#A7F3D0", "Emerald"),
    "rose":    ("#E11D48", "#FFF1F2", "#FECDD3", "Rose"),
}

_HOME_BUTTON_CLS = {
    "violet": "bg-violet-600 hover:bg-violet-700 shadow-violet-500/30",
    "blue": "bg-blue-600 hover:bg-blue-700 shadow-blue-500/30",
    "emerald": "bg-emerald-600 hover:bg-emerald-700 shadow-emerald-500/30",
    "rose": "bg-rose-600 hover:bg-rose-700 shadow-rose-500/30",
}


def _home_demo_html(count: int, color_key: str, runtime: str) -> str:
    c_hex, c_bg, c_border, c_name = _HOME_COLORS[color_key]
    dots = "".join(
        f'<div style="width:0.65rem;height:0.65rem;border-radius:999px;background:{_HOME_COLORS[k][0]};'
        + (f'transform:scale(1.35);box-shadow:0 0 0 2px white,0 0 0 3.5px {_HOME_COLORS[k][0]};"' if k == color_key else 'opacity:0.28;"')
        + '></div>'
        for k in _HOME_COLORS
    )
    return f"""
    <div style="padding:0.2rem 0;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.1rem;">
        <div style="font-size:0.68rem;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;color:{c_hex};">Live Demo</div>
        <div style="display:flex;gap:0.5rem;align-items:center;">{dots}</div>
      </div>
      <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div style="font-size:5rem;font-weight:900;color:{c_hex};line-height:1;letter-spacing:-0.03em;">{count}</div>
        <div style="color:var(--vl-text-muted);font-size:0.8rem;margin-top:0.45rem;letter-spacing:0.02em;">clicks counted</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-top:0.9rem;">
        <div style="padding:0.7rem;border-radius:0.75rem;background:{c_bg};border:1px solid {c_border};text-align:center;">
          <div style="font-size:0.62rem;font-weight:800;color:{c_hex};text-transform:uppercase;letter-spacing:0.08em;">Color</div>
          <div style="font-weight:700;color:var(--vl-text);margin-top:0.15rem;">{c_name}</div>
        </div>
        <div style="padding:0.7rem;border-radius:0.75rem;background:{c_bg};border:1px solid {c_border};text-align:center;">
          <div style="font-size:0.62rem;font-weight:800;color:{c_hex};text-transform:uppercase;letter-spacing:0.08em;">Runtime</div>
          <div style="font-weight:700;color:var(--vl-text);margin-top:0.15rem;">{"Lite" if runtime == "lite" else "WebSocket"}</div>
        </div>
      </div>
    </div>
    """


def _build_chart_frame(seed: int, points: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 17)
    raw = np.cumsum(
        rng.normal(loc=(1.5, 1.0, 0.45), scale=(0.75, 0.5, 0.25), size=(points, 3)),
        axis=0,
    )
    data = np.round(np.clip(raw + np.array([30, 18, 8]), a_min=0.5, a_max=None), 2)
    return pd.DataFrame(data, columns=["App Launches", "Teams Active", "Engagement Score"])


def _iter_markdown_chunks(text: str):
    paragraphs = text.split("\n\n")
    for paragraph_index, paragraph in enumerate(paragraphs):
        words = paragraph.split()
        for word_index, word in enumerate(words):
            suffix = " " if word_index < len(words) - 1 else ""
            yield word + suffix
        if paragraph_index < len(paragraphs) - 1:
            yield "\n\n"


def _pseudo_chat_reply(prompt: str):
    cleaned = prompt.strip()
    lower = cleaned.lower()
    rng = random.Random(sum(ord(ch) for ch in lower) + len(chat_style.value))
    keyword_notes = [
        ("auth", "Violit already includes built-in auth flows, so you can keep login, sessions, and role checks inside one app."),
        ("orm", "The ORM story starts with vl.App(db='./app.db') and app.db CRUD, which keeps demos short and readable."),
        ("database", "Violit's database helpers let you build simple CRUD screens without adding a second framework."),
        ("lite", "Lite mode uses HTMX and is often a strong choice when you want simpler HTTP transport or higher concurrency."),
        ("theme", "Theme switching stays in Python with app.set_theme(...), and this showcase starts from the bright violit_light_jewel preset."),
        ("tailwind", "Use cls first for utility styling, then add style only when you need precise gradients or shadows."),
        ("chat", "This page shows the recommended built-in chat flow: app.chat_messages(...) plus app.chat_input(messages=..., on_submit=...)."),
        ("reactive", "The reactive sweet spot is direct State passing, lambda bindings, and small @app.reactivity blocks when control flow matters."),
    ]
    matched = [text for keyword, text in keyword_notes if keyword in lower]
    if len(matched) < 3:
        remaining = [text for _, text in keyword_notes if text not in matched]
        matched.extend(rng.sample(remaining, k=3 - len(matched)))

    tone = {
        "Builder": "I will keep this concrete and implementation-focused.",
        "Playful": "I will keep this light, friendly, and demo-oriented.",
        "Bold": "I will keep this punchy and product-focused.",
    }[chat_style.value]

    reply = (
        "This is a pseudo showcase reply. No external API call is made.\n\n"
        f"**Assistant vibe:** {chat_style.value}\n"
        f"{tone}\n\n"
        "Here are the most relevant Violit ideas for that prompt:\n"
        f"- {matched[0]}\n"
        f"- {matched[1]}\n"
        f"- {matched[2]}\n\n"
        "Try the Dashboard, Components, and Settings pages next if you want to see the same ideas as real UI instead of just text."
    )

    if chat_mode.value == "streaming":
        return _iter_markdown_chunks(reply)
    return reply


def _reset_chat():
    chat_history.set(
        [
            {
                "role": "assistant",
                "content": "Chat reset complete. Ask about themes, auth, ORM, Lite mode, or styling.",
            }
        ]
    )


@app.dialog("What's Fresh in This Showcase", width="large")
def whats_new_dialog():
    app.subheader("This refresh focuses on visible, current patterns")
    app.callout_success(
        "The Chat page now uses Violit's built-in chat_messages and chat_input widgets with pseudo replies."
    )
    app.callout_info(
        "The Widgets page now shows a full gallery of input widgets, status feedback, and layout components — all styled with Tailwind cls."
    )
    app.callout_warning(
        "The showcase stays safe to publish because no real AI provider keys or network calls are required for the chat demo."
    )


@app.dialog("Tailwind Notes", width="medium")
def tailwind_notes_dialog():
    app.markdown(
        "- Start with `cls` for utility-first styling.\n"
        "- Add `style` only when you need exact gradients, borders, or shadows.\n"
        "- Use `configure_widget()` later if you want app-wide design defaults."
    )
    app.callout_info("In Violit, styling can stay in Python and still feel deliberate.")


def home_page():
    demo_count = app.state(0, key="home_demo_count")
    demo_color = app.state("violet", key="home_demo_color")

    left, right = app.columns([1.05, 0.95], gap="2rem")
    with left:
        app.badge("Built-in app stack", variant="primary", pill=True)
        app.space("0.7rem")
        app.markdown("## Ship a polished\nPython product")
        app.text(
            "Chat, reactivity, auth, ORM — all from one Python surface.",
            muted=True,
            style="line-height:1.75;font-size:1.02rem;",
        )
        app.space("1.4rem")
        b1, b2 = app.columns([1.1, 0.9], gap="0.8rem")
        with b1:
            app.button(
                "Start With Chat",
                icon="comments",
                on_click=lambda: app.switch_page("Chat"),
                variant="text",
                cls="w-full justify-center rounded-2xl px-5 py-4 font-bold text-white bg-violet-600 hover:bg-violet-700 shadow-xl shadow-violet-500/20",
            )
        with b2:
            app.button(
                "See Widgets",
                icon="puzzle-piece",
                on_click=lambda: app.switch_page("Widgets"),
                variant="text",
                cls="w-full justify-center rounded-2xl px-5 py-4 font-bold border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 shadow-lg shadow-slate-200/50",
            )

        app.space("2.5rem")
        
        with app.card(cls="rounded-2xl border-none shadow-sm bg-slate-50/80 p-2 mb-3"):
            c1, c2 = app.columns([0.1, 0.9], gap="0.3rem")
            with c1:
                app.icon("zap", cls="text-violet-600 text-lg mt-0.5")
            with c2:
                app.text("Fast Iteration", cls="font-bold text-xs")
                app.text("Hot-reload & zero-config setup.", muted=True, cls="text-[10px]")
                
        with app.card(cls="rounded-2xl border-none shadow-sm bg-slate-50/80 p-2 mb-3"):
            c1, c2 = app.columns([0.1, 0.9], gap="0.3rem")
            with c1:
                app.icon("refresh", cls="text-blue-600 text-lg mt-0.5")
            with c2:
                app.text("Reactive State", cls="font-bold text-xs")
                app.text("Auto UI updates across components.", muted=True, cls="text-[10px]")
                
        with app.card(cls="rounded-2xl border-none shadow-sm bg-slate-50/80 p-2"):
            c1, c2 = app.columns([0.1, 0.9], gap="0.3rem")
            with c1:
                app.icon("palette", cls="text-emerald-600 text-lg mt-0.5")
            with c2:
                app.text("Modern UI", cls="font-bold text-xs")
                app.text("Tailwind support via 'cls' parameter.", muted=True, cls="text-[10px]")

    with right:
        app.card(
            lambda: _home_demo_html(demo_count.value, demo_color.value, mode),
            style="background:linear-gradient(180deg,#FAFAFF 0%,white 100%);border:1px solid #E9D5FF;box-shadow:0 24px 56px rgba(109,40,217,0.1);",
        )
        app.space("0.55rem")
        c1, c2, c3, c4 = app.columns(4, gap="0.45rem")
        for col, (key, (c_hex, _, _, c_name)) in zip([c1, c2, c3, c4], _HOME_COLORS.items()):
            with col:
                app.button(
                    c_name,
                    on_click=lambda k=key: demo_color.set(k),
                    variant="text",
                    cls=(
                        "w-full rounded-xl px-3 py-2.5 text-xs font-bold text-white border-0 "
                        "transition-all hover:scale-105 opacity-90 hover:opacity-100 shadow-lg "
                        f"{_HOME_BUTTON_CLS[key]}"
                    ),
                )
        app.space("0.45rem")
        i1, i2, i3 = app.columns(3, gap="0.45rem")
        with i1:
            app.button(
                "+ Click",
                on_click=lambda: demo_count.set(demo_count.value + 1),
                variant="primary",
                cls="w-full rounded-xl font-bold",
            )
        with i2:
            app.button(
                "− Undo",
                on_click=lambda: demo_count.set(max(0, demo_count.value - 1)),
                variant="neutral",
                cls="w-full rounded-xl",
            )
        with i3:
            app.button(
                "Reset",
                on_click=lambda: demo_count.set(0),
                variant="neutral",
                cls="w-full rounded-xl",
            )

    app.divider()

def dashboard_page():
    app.header("Interactive Dashboard")
    app.caption("State-driven metrics and chart tabs without a full app rerun.")

    c1, c2 = app.columns([2, 1])
    with c1:
        window = app.select_slider(
            "Time Window",
            options=[12, 24, 36, 48],
            value=24,
            key="showcase_dashboard_window",
        )
    with c2:
        app.button(
            "Refresh Signals",
            on_click=lambda: dashboard_seed.set(dashboard_seed.value + 1),
            variant="neutral",
        )

    @app.reactivity
    def render_dashboard():
        data = _build_chart_frame(dashboard_seed.value, int(window.value))
        latest = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else latest

        m1, m2, m3, m4 = app.columns(4)
        with m1:
            app.metric("App Launches", f"{int(round(latest['App Launches']))}", f"{int(round(latest['App Launches'] - previous['App Launches'])):+d}")
        with m2:
            app.metric("Teams Active", f"{int(round(latest['Teams Active']))}", f"{int(round(latest['Teams Active'] - previous['Teams Active'])):+d}")
        with m3:
            app.metric("Engagement Score", f"{latest['Engagement Score']:.1f}", f"{latest['Engagement Score'] - previous['Engagement Score']:+.1f}")
        with m4:
            app.metric("Runtime", "Lite" if mode == "lite" else "WebSocket", "active")

        app.divider()
        tab1, tab2 = app.tabs(["Line Chart", "Area Chart"], key="showcase_dashboard_tabs")
        with tab1:
            app.line_chart(data)
        with tab2:
            app.area_chart(data)

        app.subheader("Recent Rows")
        app.dataframe(data.tail(8), height=320)

    render_dashboard()


def widgets_page():
    app.header("Widgets")
    app.caption("A live preview styled in Python, plus a gallery of every built-in Violit widget.")

    left, right = app.columns([1, 1])
    with left:
        title = app.text_input(
            "Launch title",
            value="Violit Studio",
            submit_on_enter=True,
            on_submit=lambda value: app.toast(f"Saved: {value}", variant="success"),
        )
        mood = app.select_slider(
            "Mood",
            options=["Soft", "Playful", "Bold"],
            value="Playful",
            key="showcase_component_mood",
        )
        accent = app.color_picker("Accent", "#7C3AED")
        glow = app.slider("Glow strength", 0, 100, 58, live_update=True)
        note = app.text_area(
            "Mini pitch",
            value="Reactive widgets, calmer state management, and polished UI surfaces.",
            height=5,
        )
        app.download_button(
            "Download starter snippet",
            data=(
                "import violit as vl\n\n"
                "app = vl.App(title='Violit Studio', theme='violit_light_jewel')\n"
                "app.button('Launch', cls='rounded-full shadow-lg')\n"
                "app.run()\n"
            ),
            file_name="violit_starter.py",
            mime="text/x-python",
        )
        app.link_button("Open Documentation", "https://doc.violit.cloud")
        app.button("Tailwind Notes", on_click=tailwind_notes_dialog, variant="neutral")

    with right:
        app.subheader("Live Preview")
        app.card(
            lambda: _preview_card_html(title.value, mood.value, accent.value, note.value, glow.value),
            cls="overflow-hidden",
        )
        app.callout_success("CTA buttons below use cls utilities instead of hand-written HTML.")

        b1, b2 = app.columns(2)
        with b1:
            app.button(
                "Rounded CTA",
                variant="primary",
                cls="w-full rounded-full shadow-lg font-semibold",
            )
        with b2:
            app.button(
                "Soft Outline",
                variant="text",
                cls="w-full rounded-full bg-white border border-violet-200 text-violet-700 font-semibold shadow-sm",
            )

    app.divider()
    app.subheader("Widget Gallery")
    app.caption("All widgets below are live — interact with them freely.")

    t_input, t_status, t_layout = app.tabs(
        ["Input Widgets", "Status & Feedback", "Layout & Display"],
        key="showcase_widget_gallery_tabs",
    )

    with t_input:
        app.space("0.5rem")
        c1, c2 = app.columns(2, gap="1.2rem")
        with c1:
            app.subheader("Selection", divider=False)
            app.checkbox("Enable notifications", value=True, key="wg_chk1")
            app.checkbox("Dark mode preview", value=False, key="wg_chk2")
            app.toggle("Live updates", value=True, key="wg_toggle1")
            app.toggle("Auto-save", value=False, key="wg_toggle2")
            app.space("0.4rem")
            app.radio(
                "Priority",
                options=["Low", "Medium", "High", "Critical"],
                index=1,
                horizontal=True,
                key="wg_radio1",
            )
        with c2:
            app.subheader("Values", divider=False)
            app.number_input("Port", value=8080, min_value=1024, max_value=65535, key="wg_num1")
            app.selectbox(
                "Theme preset",
                ["violit_light_jewel", "ocean", "glass", "editorial", "neo_brutalism", "cyberpunk"],
                key="wg_sel1",
            )
            app.multiselect(
                "Active features",
                options=["Chat", "Auth", "ORM", "Lite mode", "Desktop", "Broadcasting"],
                default=["Chat", "Auth"],
                key="wg_ms1",
            )
            app.date_input("Launch date", key="wg_date1")

    with t_status:
        app.space("0.5rem")
        app.callout_info("Callouts are great for contextual guidance — no custom HTML needed.")
        app.callout_success("Operation completed successfully. State was saved to the database.")
        app.callout_warning("This widget is in beta. Some props may change in future versions.")
        app.callout_danger("Authentication failed. Please check your credentials and try again.")
        app.space("0.5rem")
        app.subheader("Progress & Badges", divider=False)
        c1, c2 = app.columns([1.4, 0.6], gap="1.2rem")
        with c1:
            app.progress(72)
            app.progress(35)
            app.progress(91)
        with c2:
            app.badge("primary", variant="primary", pill=True)
            app.badge("success", variant="success", pill=True)
            app.badge("warning", variant="warning", pill=True)
            app.badge("danger", variant="danger", pill=True)
            app.badge("neutral", variant="neutral", pill=True)
            app.badge("live", variant="primary", pill=True, pulse=True)

    with t_layout:
        app.space("0.5rem")
        with app.expander("What is Violit?", icon="circle-question"):
            app.text(
                "Violit is a Python web framework with built-in reactivity, chat, ORM, and auth.",
                muted=True,
            )
            app.callout_info("No JavaScript required to build polished interactive UIs.")
        with app.expander("Styling approach", icon="palette"):
            app.text(
                "Use cls= for Tailwind utilities. Use style= only for gradients or precise shadows.",
                muted=True,
            )
            app.code("app.button('Launch', cls='rounded-full shadow-lg font-bold')", language="python")
        with app.expander("Deployment options", icon="rocket"):
            app.text("Deploy as a standard Python web app. Supports Uvicorn, Gunicorn, and Docker.", muted=True)
            app.code("violit run app.py --port 8080", language="bash")
        app.space("0.5rem")
        app.subheader("Code snippet", divider=False)
        app.code(
            "app = vl.App(title='My App', theme='violit_light_jewel')\n"
            "count = app.state(0)\n"
            "app.button('Click me', on_click=lambda: count.set(count.value + 1))\n"
            "app.metric('Clicks', lambda: str(count.value))",
            language="python",
        )


def chat_page():
    app.header("Pseudo Chat Studio")
    app.caption("Built with Violit's chat widgets. No real AI provider is called.")

    modes = ["streaming", "instant"]
    current_mode = chat_mode.value if chat_mode.value in modes else "streaming"

    c1, c2, c3 = app.columns([1, 1, 1])
    with c1:
        app.selectbox(
            "Reply mode",
            modes,
            index=modes.index(current_mode),
            key="showcase_chat_mode",
        )
    with c2:
        app.select_slider(
            "Assistant vibe",
            options=["Builder", "Playful", "Bold"],
            value=chat_style.value,
            key="showcase_chat_style",
        )
    with c3:
        app.button("Reset chat", on_click=_reset_chat, variant="neutral")

    app.callout_info(
        "This page demonstrates the real Violit chat surface: chat_messages for the transcript and chat_input for the composer."
    )

    @app.reactivity
    def render_chat():
        app.chat_messages(chat_history, height="62vh", border=True)

    render_chat()

    app.chat_input(
        "Ask about themes, auth, ORM, Lite mode, or styling...",
        messages=chat_history,
        on_submit=_pseudo_chat_reply,
        pinned=False,
        auto_scroll="bottom",
        stream_speed="smooth",
    )


def reactive_page():
    app.header("Reactive Logic")
    app.caption("Small current patterns: direct state, If, For, callbacks, and reactive blocks.")

    count = app.state(0, key="reactive_count")

    app.subheader("1. Counter with a tiny reactive condition")
    c1, c2 = app.columns([1, 2])
    with c1:
        app.metric("Count", lambda: str(count.value))
    with c2:
        btn1, btn2 = app.columns(2)
        with btn1:
            app.button("Increase", on_click=lambda: count.set(count.value + 1), variant="primary")
        with btn2:
            app.button("Decrease", on_click=lambda: count.set(count.value - 1), variant="neutral")

    app.If(
        lambda: count.value >= 5,
        then=lambda: app.callout_success("Counter warmed up. This message appears without a full rerun."),
        else_=lambda: app.callout_info("Tap a few more times to trigger the success state."),
    )

    app.divider()

    app.subheader("2. Real-time calculator")
    v1, v2 = app.columns(2)
    with v1:
        value_a = app.slider("Value A", 0, 100, 30, live_update=True)
    with v2:
        value_b = app.slider("Value B", 0, 100, 70, live_update=True)

    app.card(
        lambda: f"""
        <div style='text-align:center; padding:0.2rem 0;'>
          <div style='font-size:0.8rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#7C3AED;'>Live result</div>
          <div style='margin-top:0.45rem; font-size:3rem; font-weight:800; color:var(--vl-text);'>
            {value_a.value + value_b.value}
          </div>
          <div style='color:var(--vl-text-muted);'>Move the sliders and only this card updates.</div>
        </div>
        """,
        style="background:linear-gradient(180deg,#FFFFFF 0%, #FAF5FF 100%); border:1px solid #E9D5FF; box-shadow:0 18px 40px rgba(109,40,217,0.08);",
    )

    app.divider()

    app.subheader("3. Dynamic greeting")
    name = app.text_input("Enter your name", value="Explorer", key="reactive_name")
    app.If(
        lambda: bool(name.value.strip()),
        then=lambda: app.callout_success(f"Hello, {name.value}. This block is using app.If(...)."),
        else_=lambda: app.callout_warning("Type a name to personalize the greeting."),
    )

    app.divider()

    app.subheader("4. For-driven spotlight list")
    spotlight_count = app.slider("Number of spotlight cards", 1, 6, 3, live_update=True)
    spotlight_items = [
        ("Starter-friendly", "Plain Python authoring with polished built-in widgets.", "#7C3AED"),
        ("Reactive by default", "Use State, lambda bindings, and tiny reactive scopes only where they help.", "#2563EB"),
        ("Theme-ready", "Switch presets quickly and keep the visual direction inside your app code.", "#EA580C"),
        ("Chat-ready", "Modern chat demos can use chat_messages and chat_input without external scaffolding.", "#16A34A"),
        ("Database-friendly", "app.db and built-in auth reduce the need for extra glue in small apps.", "#DB2777"),
        ("Lite included", "HTMX Lite mode is available when you want a different runtime profile.", "#0891B2"),
    ]
    app.For(
        lambda: spotlight_items[: spotlight_count.value],
        render=lambda item, index: app.card(
            f'<div style="display:flex;flex-direction:column;gap:0.4rem;padding:0.1rem 0;">'
            f'<div style="font-size:0.7rem;font-weight:800;letter-spacing:0.09em;text-transform:uppercase;color:{item[2]};">Spotlight {index + 1}</div>'
            f'<div style="font-weight:700;color:var(--vl-text);font-size:1.08rem;">{item[0]}</div>'
            f'<div style="color:var(--vl-text-muted);line-height:1.62;font-size:0.9rem;">{item[1]}</div>'
            f'</div>',
            style=f"margin-bottom:0.75rem;background:white;border:1px solid #E9E5F0;border-left:4px solid {item[2]};box-shadow:0 8px 24px rgba(28,17,39,0.05);",
        ),
    )


def settings_page():
    app.header("Settings")
    app.caption("Switch the look and tune a few runtime-feel controls from one page.")

    theme_options = [
        "violit_light_jewel",
        "light",
        "ocean",
        "glass",
        "editorial",
        "neo_brutalism",
        "violit_dark",
        "cyberpunk",
    ]
    default_theme = "violit_light_jewel"
    default_index = theme_options.index(default_theme)

    theme_choice = app.selectbox(
        "Choose Theme",
        theme_options,
        index=default_index,
        key="settings_theme_select",
    )
    primary = app.color_picker("Primary Accent", "#6D28D9")
    animation = app.radio(
        "Animation Mode",
        ["soft", "hard"],
        index=0,
        horizontal=True,
        key="settings_animation_mode",
    )
    selection = app.toggle("Allow text selection", value=True, key="settings_selection_mode")

    def apply_settings():
        app.set_theme(theme_choice.value)
        app.set_primary_color(primary.value)
        app.set_animation_mode(animation.value)
        app.set_selection_mode(selection.value)
        app.toast(f"Applied {theme_choice.value}", variant="success")

    app.button("Apply Settings", on_click=apply_settings, variant="primary")
    app.callout_info(
        f"This showcase starts in violit_light_jewel. Current runtime: {'Lite (HTMX)' if mode == 'lite' else 'WebSocket'}."
    )


with app.sidebar:
    app.markdown("### Violit Showcase")
    app.caption("Faster than Light, Beautiful as Violet.")
    app.badge(f"runtime: {'lite' if mode == 'lite' else 'ws'}", pill=True, variant="primary")
    app.divider()


app.navigation(
    [
        vl.Page(home_page, title="Home", icon="house"),
        vl.Page(dashboard_page, title="Dashboard", icon="chart-line"),
        vl.Page(reactive_page, title="Reactive Logic", icon="bolt"),
        vl.Page(widgets_page, title="Widgets", icon="puzzle-piece"),
        vl.Page(chat_page, title="Chat", icon="comments"),
        vl.Page(settings_page, title="Settings", icon="gear"),
    ]
)

app.run()
