import sys

import pandas as pd
import violit as vl


app = vl.App(title="GitHub Issue 30 - Repro vs Minimal Fix")


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


def _append_batch(existing_rows: list[dict], tag: str, batch_size: int = 2) -> list[dict]:
    next_rows = list(existing_rows)
    start = len(next_rows)
    for offset in range(batch_size):
        template = EMAIL_POOL[(start + offset) % len(EMAIL_POOL)].copy()
        template["id"] = len(next_rows) + 1
        template["subject"] = f"{template['subject']} ({tag}-{template['id']})"
        next_rows.append(template)
    return next_rows


def _column_defs(values: list[str]) -> list[dict]:
    return [
        {"field": "subject"},
        {
            "field": "label",
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {
                "values": values,
            },
        },
    ]


repro_email_list = app.session_state(EMAIL_POOL[:3], key="issue30_combo_repro_email_list")
repro_label_values = app.session_state(
    ["inbox", "important", "follow up", "read later"],
    key="issue30_combo_repro_label_values",
)
repro_fetch_count = app.state(0, key="issue30_combo_repro_fetch_count")
repro_status = app.state(
    "Open this expander and click fetch. This mirrors the original report's eager state-read pattern.",
    key="issue30_combo_repro_status",
)

fix_email_list = app.session_state(EMAIL_POOL[:3], key="issue30_combo_fix_email_list")
fix_label_values = app.session_state(
    ["inbox", "important", "follow up", "read later"],
    key="issue30_combo_fix_label_values",
)
fix_fetch_count = app.state(0, key="issue30_combo_fix_fetch_count")
fix_status = app.state(
    "This version changes only one thing: it extracts the table render into @app.reactivity.",
    key="issue30_combo_fix_status",
)


def fetch_repro_emails():
    repro_email_list.set(_append_batch(repro_email_list.value, "repro"))
    repro_fetch_count.set(repro_fetch_count.value + 1)
    repro_status.set(
        "Fetched more rows in the reproduction section. If the expander closes, that matches the original UX complaint. "
        "If it stays open, your current build may already include the expander-state persistence fix."
    )


def fetch_fix_emails():
    fix_email_list.set(_append_batch(fix_email_list.value, "fixed"))
    fix_fetch_count.set(fix_fetch_count.value + 1)
    fix_status.set(
        "Fetched more rows in the minimal-fix section. The expander should stay stable because only the inner reactive function rerenders."
    )


@app.reactivity
def render_fix_email_table():
    df = pd.DataFrame(fix_email_list.value)
    column_defs = _column_defs(fix_label_values.value)
    app.dataframe(
        df,
        height=260,
        hide_index=True,
        toolbar=False,
        grid_options={"animateRows": False},
        column_defs=column_defs,
    )


def main_page():
    app.header("Issue 30 - Original repro vs minimal fix")
    app.write(
        "This page combines the original-report reproduction and the minimal-fix version in one place, so you can compare them "
        "with the same data shape and the same button flow."
    )
    app.callout_info(
        "A uses the original eager state-read pattern inside `with app.reactivity()`. B keeps the overall structure but moves only the table "
        "rendering into an `@app.reactivity` function."
    )

    with app.expander("A. Original report reproduction"):
        app.caption(
            "Starts closed by default, like the original report. Open it manually, then click fetch and watch whether the expander is recreated."
        )
        app.text(repro_status)
        app.text(lambda: f"Rows: {len(repro_email_list.value)} | Fetches: {repro_fetch_count.value}")

        with app.reactivity():
            df = pd.DataFrame(repro_email_list.value)
            column_defs = _column_defs(repro_label_values.value)
            app.dataframe(
                df,
                height=260,
                hide_index=True,
                toolbar=False,
                grid_options={"animateRows": False},
                column_defs=column_defs,
            )

        app.button("Fetch more emails in repro section", on_click=fetch_repro_emails)

    with app.expander("B. Minimal fix with @app.reactivity"):
        app.caption(
            "Also starts closed by default. This version keeps the code very similar, but the inner table rendering is extracted into a decorated "
            "reactive function."
        )
        app.text(fix_status)
        app.text(lambda: f"Rows: {len(fix_email_list.value)} | Fetches: {fix_fetch_count.value}")

        render_fix_email_table()

        app.button("Fetch more emails in fixed section", on_click=fetch_fix_emails)

    with app.expander("Key difference"):
        app.code(
            'A. Reproduction\n'
            'with app.expander("Emails"):\n'
            '    with app.reactivity():\n'
            '        df = pd.DataFrame(email_list.value)\n'
            '        app.dataframe(df, column_defs=column_defs)\n'
            '    app.button("Fetch more emails", on_click=fetch_emails)\n\n'
            'B. Minimal fix\n'
            '@app.reactivity\n'
            'def render_email_table():\n'
            '    df = pd.DataFrame(email_list.value)\n'
            '    app.dataframe(df, column_defs=column_defs)\n\n'
            'with app.expander("Emails"):\n'
            '    render_email_table()\n'
            '    app.button("Fetch more emails", on_click=fetch_emails)\n',
            language="python",
            copy_button=True,
        )


app.navigation([main_page])


if __name__ == "__main__":
    port = 18635
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)