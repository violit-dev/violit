import sys

import pandas as pd
import violit as vl


app = vl.App(title="GitHub Issue 30 - Expander Open State on Dataframe Update")


EMAIL_POOL = [
    {"id": 1, "subject": "Quarterly planning notes", "sender": "Ava", "label": "inbox"},
    {"id": 2, "subject": "New onboarding checklist", "sender": "Noah", "label": "important"},
    {"id": 3, "subject": "Customer feedback summary", "sender": "Mia", "label": "follow up"},
    {"id": 4, "subject": "Design review recording", "sender": "Liam", "label": "read later"},
    {"id": 5, "subject": "Release status update", "sender": "Emma", "label": "important"},
    {"id": 6, "subject": "Support handoff", "sender": "Olivia", "label": "follow up"},
    {"id": 7, "subject": "Meeting agenda", "sender": "James", "label": "inbox"},
    {"id": 8, "subject": "Docs cleanup", "sender": "Sophia", "label": "read later"},
]


context_emails = app.session_state(EMAIL_POOL[:3], key="issue30_context_emails")
decorator_emails = app.session_state(EMAIL_POOL[:3], key="issue30_decorator_emails")
context_fetches = app.state(0, key="issue30_context_fetches")
decorator_fetches = app.state(0, key="issue30_decorator_fetches")
status_text = app.state(
    "Open each expander, then click its fetch button to compare the update behavior.",
    key="issue30_status_text",
)


def _append_batch(existing_rows: list[dict], prefix: str, batch_size: int = 2) -> list[dict]:
    next_rows = list(existing_rows)
    start = len(next_rows)
    for offset in range(batch_size):
        template = EMAIL_POOL[(start + offset) % len(EMAIL_POOL)].copy()
        template["id"] = len(next_rows) + 1
        template["subject"] = f"{template['subject']} ({prefix}-{template['id']})"
        next_rows.append(template)
    return next_rows


def _emails_to_df(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["id", "subject", "sender", "label"])


def fetch_more_context_emails():
    context_emails.set(_append_batch(context_emails.value, "ctx"))
    context_fetches.set(context_fetches.value + 1)
    status_text.set(
        "Section A fetched more rows. This uses `with app.reactivity()` and mirrors the original report pattern."
    )


def fetch_more_decorator_emails():
    decorator_emails.set(_append_batch(decorator_emails.value, "decorator"))
    decorator_fetches.set(decorator_fetches.value + 1)
    status_text.set(
        "Section B fetched more rows. This uses `@app.reactivity`, which is the supported partial-rerender pattern."
    )


@app.reactivity
def render_decorator_dataframe():
    app.dataframe(
        lambda: _emails_to_df(decorator_emails.value),
        height=260,
        hide_index=True,
        toolbar=False,
        grid_options={"animateRows": False},
        column_order=["id", "subject", "sender", "label"],
    )


def main_page():
    app.header("Issue 30 - expander open state while email rows update")
    app.write(
        "This page gives the reporter a direct way to test the Issue #30 scenario: clicking a fetch button inside an expander "
        "after the email list changes."
    )
    app.callout_info(
        "Section A mirrors the reported `with app.reactivity():` pattern. Section B shows the recommended `@app.reactivity` "
        "workaround so only the inner table fragment rerenders."
    )
    app.text(status_text)

    with app.expander("A. Original pattern from the report: `with app.reactivity()`", expanded=True):
        app.write(
            "Open this expander, click the fetch button, and watch whether the expander itself is recreated. "
            "This path follows the context-manager rerender behavior."
        )
        app.caption("If this section or the section below closes after the click, that is the behavior under test, not a dead button.")
        app.text(lambda: f"Rows: {len(context_emails.value)} | Fetches: {context_fetches.value}")

        with app.reactivity():
            app.dataframe(
                lambda: _emails_to_df(context_emails.value),
                height=260,
                hide_index=True,
                toolbar=False,
                grid_options={"animateRows": False},
                column_order=["id", "subject", "sender", "label"],
            )

        app.button("Fetch more emails in section A", on_click=fetch_more_context_emails)

    with app.expander("B. Supported workaround: `@app.reactivity` inside the expander", expanded=True):
        app.write(
            "Open this expander, click the fetch button, and verify that only the table updates while the expander stays open. "
            "This is the recommended pattern for the Issue #30 use case."
        )
        app.caption("This button should keep working even after repeated clicks. If A causes B to close, reopen B and test again.")
        app.text(lambda: f"Rows: {len(decorator_emails.value)} | Fetches: {decorator_fetches.value}")

        render_decorator_dataframe()

        app.button("Fetch more emails in section B", on_click=fetch_more_decorator_emails)

    with app.expander("Equivalent code pattern for the supported section"):
        app.code(
            'email_list = app.session_state(seed_rows, key="email_list")\n\n'
            '@app.reactivity\n'
            'def render_email_table():\n'
            '    app.dataframe(\n'
            '        lambda: pd.DataFrame(email_list.value),\n'
            '        grid_options={"animateRows": False},\n'
            '    )\n\n'
            'with app.expander("Emails", expanded=True):\n'
            '    render_email_table()\n'
            '    app.button("Fetch more emails", on_click=fetch_emails)\n',
            language="python",
            copy_button=True,
        )


app.navigation([main_page])


if __name__ == "__main__":
    port = 18630
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)