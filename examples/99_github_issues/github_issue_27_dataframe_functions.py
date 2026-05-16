import sys
from typing import Any

import pandas as pd
import violit as vl


app = vl.App(title="GitHub Issue 27 - DataFrame Functions")


page_size = app.session_state(20, key="issue27_page_size")
editor_event = app.session_state("No edit events yet.", key="issue27_editor_event")
row_click_event = app.session_state("No row clicked yet.", key="issue27_row_click_event")


regions = ["Global", "EMEA", "APAC", "Americas"]
teams = ["Platform", "Growth", "Operations", "Analytics"]
statuses = ["Healthy", "Watch", "At Risk"]

rows = []
for index in range(1, 121):
    rows.append(
        {
            "account_id": f"ACC-{index:03d}",
            "team": teams[index % len(teams)],
            "region": regions[index % len(regions)],
            "status": statuses[index % len(statuses)],
            "mrr": 1200 + index * 37,
            "active_users": 10 + (index * 3) % 90,
            "nps": 25 + (index * 7) % 55,
        }
    )

df = pd.DataFrame(rows)


def shared_grid_options():
    return {
        "pagination": True,
        "paginationPageSize": int(page_size.value),
        "paginationPageSizeSelector": [10, 20, 50, 100],
        "animateRows": False,
    }


def dataframe_column_config():
    return {
        "account_id": {"label": "Account ID", "pinned": "left", "minWidth": 140},
        "team": {"label": "Team", "minWidth": 130},
        "region": {"label": "Region", "minWidth": 120},
        "status": {"label": "Health", "minWidth": 120},
        "mrr": {"label": "MRR", "minWidth": 120},
        "active_users": {"label": "Active Users", "minWidth": 140},
        "nps": {"label": "NPS", "maxWidth": 100},
    }


def data_editor_column_config():
    return {
        "account_id": {"label": "Account ID", "readonly": True, "pinned": "left", "minWidth": 140},
        "team": {"label": "Team", "type": "select", "options": teams},
        "region": {"label": "Region", "type": "select", "options": regions},
        "status": {"label": "Health", "type": "select", "options": statuses},
        "mrr": {"label": "MRR", "type": "number", "min": 0, "step": 50},
        "active_users": {"label": "Active Users", "type": "number", "min": 0, "step": 1},
        "nps": {"label": "NPS", "type": "number", "min": 0, "max": 100, "step": 1},
    }


def editor_toolbar_config():
    return {
        "search": True,
        "export_csv": True,
        "fullscreen": True,
        "search_placeholder": "Search editable rows...",
        "csv_file_name": "github_issue_27_data_editor.csv",
    }


def validate_editor(payload, candidate_df):
    if "nps" in candidate_df.columns:
        normalized_nps = pd.to_numeric(candidate_df["nps"], errors="coerce")
        candidate_df["nps"] = normalized_nps
        if ((normalized_nps < 0) | (normalized_nps > 100)).fillna(False).any():
            return {"ok": False, "message": "NPS must stay between 0 and 100."}

    if "mrr" in candidate_df.columns:
        candidate_df["mrr"] = pd.to_numeric(candidate_df["mrr"], errors="coerce")

    if "active_users" in candidate_df.columns:
        normalized_active_users = pd.to_numeric(candidate_df["active_users"], errors="coerce")
        candidate_df["active_users"] = normalized_active_users
        if (normalized_active_users < 0).fillna(False).any():
            return {"ok": False, "message": "active_users cannot be negative."}

    return {"ok": True, "df": candidate_df}


def handle_editor_change(updated_df, payload):
    editor_event.set(
        f"event={payload.get('eventType', '-')}, row={payload.get('rowIndex', '-')}, "
        f"field={payload.get('field', '-')}, rows={len(updated_df)}"
    )


def handle_row_click(row_data, payload):
    row_click_event.set(
        f"clicked row={payload.get('rowIndex', '-')}, account={row_data.get('account_id', '-')}, "
        f"status={row_data.get('status', '-')}"
    )


def preview_rows(records, limit=5):
    return records[:limit] if isinstance(records, list) else []


def editor_records(value):
    if isinstance(value, pd.DataFrame):
        return value.to_dict("records")
    if isinstance(value, list):
        return value
    return []


def editor_row_count(value):
    if isinstance(value, pd.DataFrame):
        return len(value.index)
    if isinstance(value, list):
        return len(value)
    return 0


app.header("Issue 27 - DataFrame feature example")
app.write(
    "This example now covers the shared AG Grid toolbar, pagination, width handling, and the "
    "official role split: `dataframe` is read-only and `data_editor` is editable."
)

toolbar_enabled = app.checkbox(
    "Enable built-in toolbar",
    value=True,
    key="issue27_toolbar_enabled",
)
hide_index = app.checkbox(
    "Hide dataframe index",
    value=True,
    key="issue27_hide_index",
)
dynamic_rows = app.checkbox(
    "Allow row add in data_editor",
    value=True,
    key="issue27_dynamic_rows",
)

left, middle, right = app.columns([1.1, 1.1, 1.2], gap="medium")
with left:
    app.selectbox(
        "Rows per page",
        [10, 20, 50, 100],
        bind=page_size,
        help="This drives AG Grid pagination in both dataframe and data_editor.",
    )
with middle:
    width_mode = app.selectbox(
        "Width mode",
        ["stretch", "content"],
        index=0,
        key="issue27_width_mode",
        help="stretch = full width, content = fit table content width.",
    )
with right:
    theme_mode = app.selectbox(
        "Theme",
        ["auto", "light", "dark"],
        index=0,
        key="issue27_theme_mode",
        help="Test AG Grid theme styling with the shared surface.",
    )

app.caption(
    "Try the built-in toolbar inside each grid: search, CSV export, and fullscreen now come from "
    "a shared official surface. Pagination still comes from AG Grid `grid_options`."
)

width_value: Any = lambda: str(width_mode.value)
theme_value: Any = lambda: str(theme_mode.value)
hide_index_value: Any = lambda: bool(hide_index.value)
dataframe_toolbar: Any = lambda: (
    {
        "search": True,
        "export_csv": True,
        "fullscreen": True,
        "search_placeholder": "Search read-only rows...",
        "csv_file_name": "github_issue_27_dataframe.csv",
    }
    if toolbar_enabled.value
    else False
)
editor_toolbar: Any = lambda: editor_toolbar_config() if toolbar_enabled.value else False
editor_num_rows: Any = lambda: "dynamic" if dynamic_rows.value else "fixed"

app.subheader("1. dataframe: read-only viewer")
app.caption(
    "Use this surface for exploration only. Sorting, filtering, pagination, toolbar search, CSV export, "
    "and fullscreen are available, but inline editing should move to data_editor."
)

app.dataframe(
    df,
    hide_index=hide_index_value,
    height=360,
    width=width_value,
    toolbar=dataframe_toolbar,
    theme=theme_value,
    column_config=dataframe_column_config,
    grid_options=shared_grid_options,
)

app.html('<div style="height: 1rem;"></div>')

app.subheader("2. data_editor: editable surface")
app.caption(
    "This grid uses the same toolbar surface, but supports inline editing, select editors, numeric validation, "
    "row click callbacks, and optional row addition."
)

edited = app.data_editor(
    df,
    key="issue27_data_editor",
    num_rows=editor_num_rows,
    height=360,
    width=width_value,
    toolbar=editor_toolbar,
    theme=theme_value,
    column_config=data_editor_column_config(),
    validator=validate_editor,
    on_change=handle_editor_change,
    on_row_click=handle_row_click,
    grid_options=shared_grid_options,
)

metric_left, metric_middle, metric_right = app.columns([1, 1, 1], gap="medium")
with metric_left:
    app.metric("Edited rows", lambda: editor_row_count(edited.value))
with metric_middle:
    app.metric(
        "Healthy rows",
        lambda: int(sum(1 for row in editor_records(edited.value) if row.get("status") == "Healthy")),
    )
with metric_right:
    app.metric(
        "Avg NPS",
        lambda: (
            round(
                sum(row.get("nps", 0) for row in editor_records(edited.value))
                / editor_row_count(edited.value),
                1,
            )
            if editor_row_count(edited.value) > 0
            else 0
        ),
    )

app.caption(editor_event)
app.caption(row_click_event)
app.json(
    lambda: {
        "preview_rows": preview_rows(editor_records(edited.value), limit=5),
        "total_rows": editor_row_count(edited.value),
    },
    expanded=False,
)


with app.expander("What this example demonstrates"):
    app.write("1. `app.dataframe(...)` is now the read-only table surface.")
    app.write("2. `app.data_editor(...)` is the editable table surface.")
    app.write("3. Both widgets expose the shared built-in toolbar: search, CSV export, and fullscreen.")
    app.write("4. Pagination is still tested through `grid_options={\"pagination\": True}`.")
    app.write("5. `width=\"stretch\" | \"content\"` can be tested on both widgets.")
    app.write("6. The editor example also tests select editors, numeric validation, callbacks, and row addition.")


if __name__ == "__main__":
    port = 18527
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)