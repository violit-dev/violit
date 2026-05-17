import sys

import violit as vl


app = vl.App(
    title="GitHub Issue 99 - Code Block copy, theme, and syntax highlight",
    theme="ocean",
    spacing="compact",
)


PYTHON_SAMPLE = '''from dataclasses import dataclass


@dataclass
class User:
    name: str
    active: bool = True


def greet(user: User) -> str:
    status = "active" if user.active else "inactive"
    return f"Hello, {user.name} ({status})"


print(greet(User("Violit")))
'''

JSON_SAMPLE = '''{
  "framework": "violit",
  "issue": 99,
  "features": ["copy fallback", "theme auto", "syntax toggle"],
  "stable": true
}
'''

BASH_SAMPLE = '''python -m pip install violit
violit run app.py --port 18699
curl http://127.0.0.1:18699/
'''

PLAIN_SAMPLE = '''Copy fallback should still work even when navigator.clipboard is unavailable.

This block is intentionally rendered without syntax coloring.
'''


sample_code_map = {
    "python": PYTHON_SAMPLE,
    "json": JSON_SAMPLE,
    "bash": BASH_SAMPLE,
    "plain": PLAIN_SAMPLE,
}


app_theme = app.selectbox(
    "App theme",
    ["light", "dark", "ocean", "forest", "vaporwave", "violit_dark"],
    index=2,
    key="issue99_app_theme",
    on_change=lambda value: app.set_theme(value),
    help="The auto code block should adapt to the selected app theme.",
)

sample_kind = app.selectbox(
    "Sample language",
    ["python", "json", "bash", "plain"],
    index=0,
    key="issue99_sample_kind",
)

syntax_enabled = app.checkbox(
    "Enable syntax coloring",
    value=True,
    key="issue99_syntax_enabled",
)

showcase_enabled = app.checkbox(
    "Show showcase title bar",
    value=True,
    key="issue99_showcase_enabled",
)

line_numbers_enabled = app.checkbox(
    "Show line numbers",
    value=True,
    key="issue99_line_numbers_enabled",
)

wrap_lines_enabled = app.checkbox(
    "Wrap long lines",
    value=False,
    key="issue99_wrap_lines_enabled",
)


sample_code = lambda: sample_code_map[sample_kind.value]
sample_language = lambda: None if sample_kind.value == "plain" else sample_kind.value


app.header("Issue 99 - Code block copy and theme validation")
app.write(
    "This example is for validating copy reliability, theme-adaptive backgrounds, and syntax coloring toggle in app.code(...)."
)
app.callout_info(
    "Try the Copy button on each block. The auto block should follow the current app theme, while the light/dark blocks should ignore the app theme."
)

app.caption(
    lambda: (
        f"Current app theme={app_theme.value}, sample={sample_kind.value}, "
        f"syntax_highlighting={syntax_enabled.value}, line_numbers={line_numbers_enabled.value}, wrap_lines={wrap_lines_enabled.value}"
    )
)

left, middle, right = app.columns([1, 1, 1], gap="medium")

with left:
    app.subheader("Auto theme")
    app.caption("Follows the app theme.")
    app.code(
        sample_code,
        language=sample_language,
        syntax_highlighting=lambda: syntax_enabled.value,
        theme="auto",
        title="auto",
        showcase=lambda: showcase_enabled.value,
        copy_button=True,
        line_numbers=lambda: line_numbers_enabled.value,
        wrap_lines=lambda: wrap_lines_enabled.value,
    )

with middle:
    app.subheader("Explicit light")
    app.caption("Ignores the app theme.")
    app.code(
        sample_code,
        language=sample_language,
        syntax_highlighting=lambda: syntax_enabled.value,
        theme="light",
        title="light",
        showcase=lambda: showcase_enabled.value,
        copy_button=True,
        line_numbers=lambda: line_numbers_enabled.value,
        wrap_lines=lambda: wrap_lines_enabled.value,
    )

with right:
    app.subheader("Explicit dark")
    app.caption("Ignores the app theme.")
    app.code(
        sample_code,
        language=sample_language,
        syntax_highlighting=lambda: syntax_enabled.value,
        theme="dark",
        title="dark",
        showcase=lambda: showcase_enabled.value,
        copy_button=True,
        line_numbers=lambda: line_numbers_enabled.value,
        wrap_lines=lambda: wrap_lines_enabled.value,
    )

with app.expander("Expected behavior"):
    app.write(
        "1. Copy should work on localhost pages even if navigator.clipboard is blocked and fallback is needed.\n"
        "2. Auto theme should stop looking like a fixed black block and instead blend with the selected app theme.\n"
        "3. Light and dark code block themes should stay fixed regardless of the app theme.\n"
        "4. Turning syntax coloring off should keep the code readable but remove token coloring."
    )
    app.code(
        "app.code(\n"
        "    sample_code,\n"
        "    language='python',\n"
        "    theme='auto',\n"
        "    syntax_highlighting=True,\n"
        "    copy_button=True,\n"
        ")\n",
        language="python",
        theme="auto",
        syntax_highlighting=True,
        copy_button=True,
        showcase=True,
        title="API summary",
    )


if __name__ == "__main__":
    port = 18699
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)
