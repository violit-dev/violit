import sys

import pandas as pd
import violit as vl


app = vl.App(title="GitHub Issue 28 - Data Editor Edit Results and Row Delete")


label_options = ["bug", "feature", "question", "docs", "done"]

seed_rows = [
    {"id": 1, "text": "Add CSV export", "label": "feature", "owner": "Ava"},
    {"id": 2, "text": "Improve docs", "label": "docs", "owner": "Noah"},
    {"id": 3, "text": "Dropdown edit result", "label": "question", "owner": "Mia"},
]

edited_rows = app.state(pd.DataFrame(seed_rows), key="issue28_edited_rows")
selected_row_text = app.state("No row clicked yet.", key="issue28_selected_row_text")
change_log = app.state("No edits yet.", key="issue28_change_log")


def current_df() -> pd.DataFrame:
    value = edited_rows.value
    if isinstance(value, pd.DataFrame):
        return value.copy()
    if isinstance(value, list):
        return pd.DataFrame(value)
    return pd.DataFrame(seed_rows)


def current_records() -> list[dict]:
    return current_df().to_dict("records")


def handle_change(updated_df: pd.DataFrame, payload: dict):
    event_type = payload.get("eventType", "-")
    if event_type == "delete_selected":
        deleted_rows = payload.get("selectedRows", []) if isinstance(payload, dict) else []
        change_log.set(f"event=delete_selected, deleted_rows={len(deleted_rows)}, total_rows={len(updated_df)}")
        return

    change_log.set(f"event={event_type}, row={payload.get('rowIndex', '-')}, field={payload.get('field', '-')}, total_rows={len(updated_df)}")


def handle_row_click(row_data: dict, payload: dict):
    selected_row_text.set(
        f"Clicked row={payload.get('rowIndex', '-')}, id={row_data.get('id', '-')}, text={row_data.get('text', '-')}, "
        f"label={row_data.get('label', '-')}"
    )


app.header("Issue 28 - How to get edited values back")
app.write(
    "`app.dataframe(...)` is read-only. If you want edit results back, use `app.data_editor(...)`, "
    "which returns a State and can also update one via `bind=`."
)

app.callout_info(
    "This example shows editable dropdown columns, how to read the edited result back, and a built-in multiple row selection + delete flow.",
)

top_left, top_right = app.columns([2, 1], gap="medium")
with top_left:
    app.data_editor(
        current_df,
        key="issue28_data_editor",
        bind=edited_rows,
        height=320,
        num_rows="dynamic",
        toolbar=True,
        row_selection="multiple",
        delete_selected=True,
        on_change=handle_change,
        on_row_click=handle_row_click,
        column_config={
            "id": {"readonly": True, "minWidth": 90},
            "text": {"label": "Text", "minWidth": 240},
            "label": {"label": "Label", "type": "select", "options": label_options},
            "owner": {"label": "Owner", "minWidth": 140},
        },
        grid_options={
            "pagination": True,
            "paginationPageSize": 5,
            "animateRows": False,
        },
    )

with top_right:
    app.metric("Edited rows", lambda: len(current_df()))
    app.caption("Use the row checkboxes, then click Delete Selected in the built-in toolbar.")
    app.caption(selected_row_text)
    app.caption(change_log)

app.subheader("Returned edit result")
app.caption("This is the value you would read in app code, callback logic, or after bind updates.")
app.json(lambda: current_records(), expanded=True)

with app.expander("Equivalent usage pattern"):
    app.code(
        'edited = app.data_editor(\n'
        '    df,\n'
        '    row_selection="multiple",\n'
        '    delete_selected=True,\n'
        '    column_config={\n'
        '        "label": {"type": "select", "options": myvalues.value},\n'
        '    },\n'
        ')\n\n'
        'print(edited.value)\n',
        language="python",
        copy_button=True,
    )


if __name__ == "__main__":
    port = 18528
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)