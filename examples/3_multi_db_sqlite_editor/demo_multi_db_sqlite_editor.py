import os
import re
import sqlite3
import sys
from datetime import date, datetime

import pandas as pd


sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "src",
    )
)

from violit import App


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HR_DB = os.path.join(BASE_DIR, "hr.db")
PROJECT_DB = os.path.join(BASE_DIR, "projects.db")

DEPARTMENT_OPTIONS = ["Engineering", "Sales", "Marketing", "Research", "Operations"]
STATUS_OPTIONS = ["Planning", "In Progress", "Blocked", "Done"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
HR_FIELDS = {"name", "email", "department", "is_active"}
PROJECT_FIELDS = {"project_name", "status", "deadline", "allocation_pct"}


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def reset_demo_databases() -> None:
    with _connect(HR_DB) as conn_hr:
        conn_hr.execute("DROP TABLE IF EXISTS employees")
        conn_hr.execute(
            """
            CREATE TABLE employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conn_hr.executemany(
            "INSERT INTO employees (emp_id, name, email, department, is_active) VALUES (?, ?, ?, ?, ?)",
            [
                (101, "Alice Smith", "alice@company.com", "Engineering", 1),
                (102, "Bob Jones", "bob@company.com", "Sales", 1),
                (103, "Charlie Kim", "charlie@company.com", "Marketing", 0),
            ],
        )

    with _connect(PROJECT_DB) as conn_project:
        conn_project.execute("DROP TABLE IF EXISTS assignments")
        conn_project.execute(
            """
            CREATE TABLE assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER NOT NULL UNIQUE,
                project_name TEXT NOT NULL,
                status TEXT NOT NULL,
                deadline TEXT NOT NULL,
                allocation_pct REAL NOT NULL
            )
            """
        )
        conn_project.executemany(
            """
            INSERT INTO assignments (emp_id, project_name, status, deadline, allocation_pct)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (101, "Alpha Revamp", "In Progress", "2026-05-30", 80.0),
                (102, "Q4 Sales Push", "Planning", "2026-06-15", 55.0),
                (103, "Brand Campaign", "Blocked", "2026-05-10", 35.0),
            ],
        )


def ensure_demo_databases() -> None:
    if not os.path.exists(HR_DB) or not os.path.exists(PROJECT_DB):
        reset_demo_databases()
        return

    try:
        with _connect(HR_DB) as conn_hr:
            hr_columns = {
                row[1] for row in conn_hr.execute("PRAGMA table_info(employees)").fetchall()
            }
        with _connect(PROJECT_DB) as conn_project:
            project_columns = {
                row[1] for row in conn_project.execute("PRAGMA table_info(assignments)").fetchall()
            }

        expected_hr_columns = {"emp_id", "name", "email", "department", "is_active"}
        expected_project_columns = {
            "assignment_id",
            "emp_id",
            "project_name",
            "status",
            "deadline",
            "allocation_pct",
        }

        if hr_columns != expected_hr_columns or project_columns != expected_project_columns:
            reset_demo_databases()
    except sqlite3.Error:
        reset_demo_databases()


def load_hr_data() -> pd.DataFrame:
    with _connect(HR_DB) as conn:
        df = pd.read_sql(
            "SELECT emp_id, name, email, department, is_active FROM employees ORDER BY emp_id",
            conn,
        )
    df["is_active"] = df["is_active"].astype(bool)
    return df


def load_project_data() -> pd.DataFrame:
    with _connect(PROJECT_DB) as conn:
        return pd.read_sql(
            """
            SELECT emp_id, project_name, status, deadline, allocation_pct
            FROM assignments
            ORDER BY emp_id
            """,
            conn,
        )


def load_editor_data() -> pd.DataFrame:
    merged_df = pd.merge(load_hr_data(), load_project_data(), on="emp_id", how="inner")
    merged_df["allocation_pct"] = merged_df["allocation_pct"].astype(float)
    return merged_df[
        [
            "emp_id",
            "name",
            "email",
            "department",
            "is_active",
            "project_name",
            "status",
            "deadline",
            "allocation_pct",
        ]
    ]


def _normalize_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"true", "1", "yes", "y", "on"}


def normalize_row(row: dict) -> dict:
    normalized = dict(row)
    normalized["emp_id"] = int(normalized["emp_id"])
    normalized["name"] = str(normalized["name"]).strip()
    normalized["email"] = str(normalized["email"]).strip().lower()
    normalized["department"] = str(normalized["department"]).strip()
    normalized["is_active"] = _normalize_bool(normalized["is_active"])
    normalized["project_name"] = str(normalized["project_name"]).strip()
    normalized["status"] = str(normalized["status"]).strip()
    normalized["deadline"] = str(normalized["deadline"]).strip()
    normalized["allocation_pct"] = round(float(normalized["allocation_pct"]), 2)
    return normalized


def validate_editor_change(event: dict, candidate_df: pd.DataFrame):
    field = event.get("field")
    if not field:
        return True

    if field == "emp_id":
        return "emp_id is read-only in this demo."

    row = event.get("rowData") or {}
    try:
        normalized_row = normalize_row(row)
    except (TypeError, ValueError) as exc:
        return f"Invalid value: {exc}"

    if not normalized_row["name"]:
        return "name is required."
    if not normalized_row["project_name"]:
        return "project_name is required."
    if normalized_row["department"] not in DEPARTMENT_OPTIONS:
        return f"department must be one of: {', '.join(DEPARTMENT_OPTIONS)}"
    if normalized_row["status"] not in STATUS_OPTIONS:
        return f"status must be one of: {', '.join(STATUS_OPTIONS)}"
    if not EMAIL_RE.match(normalized_row["email"]):
        return "email must be a valid email address."

    try:
        date.fromisoformat(normalized_row["deadline"])
    except ValueError:
        return "deadline must use YYYY-MM-DD format."

    if not 0 <= normalized_row["allocation_pct"] <= 100:
        return "allocation_pct must stay between 0 and 100."

    row_index = event.get("rowIndex")
    if row_index is not None and 0 <= int(row_index) < len(candidate_df.index):
        for key, value in normalized_row.items():
            if key in candidate_df.columns:
                candidate_df.at[int(row_index), key] = value
    else:
        mask = candidate_df["emp_id"] == normalized_row["emp_id"]
        for key, value in normalized_row.items():
            if key in candidate_df.columns:
                candidate_df.loc[mask, key] = value

    return {"ok": True, "df": candidate_df}


def persist_editor_change(event: dict) -> str:
    field = event.get("field")
    if field not in HR_FIELDS | PROJECT_FIELDS:
        raise ValueError(f"Unsupported field: {field}")

    row = normalize_row(event.get("rowData") or {})
    emp_id = row["emp_id"]
    value = row[field]

    if field in HR_FIELDS:
        stored_value = int(value) if field == "is_active" else value
        with _connect(HR_DB) as conn:
            conn.execute(f"UPDATE employees SET {field} = ? WHERE emp_id = ?", (stored_value, emp_id))
        return f"employees.{field} updated for emp_id={emp_id}"

    with _connect(PROJECT_DB) as conn:
        conn.execute(f"UPDATE assignments SET {field} = ? WHERE emp_id = ?", (value, emp_id))
    return f"assignments.{field} updated for emp_id={emp_id}"


ensure_demo_databases()

app = App(title="Violit Multi-DB Editor", theme="violit_light_jewel", container_width="1200px")
app.configure_sidebar(width=320, min_width=240, max_width=520, resizable=True)
hr_table_state = app.state(load_hr_data(), key="official_hr_table_v1")
project_table_state = app.state(load_project_data(), key="official_project_table_v1")
stats_state = app.state({"saved": 0, "rejected": 0, "last": "Ready"}, key="official_stats_v1")
audit_log_state = app.state([], key="official_audit_log_v1")


def refresh_live_tables() -> None:
    hr_table_state.set(load_hr_data())
    project_table_state.set(load_project_data())


def add_audit_log(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    current = list(audit_log_state.value or [])
    current.insert(0, f"[{timestamp}] {message}")
    audit_log_state.set(current[:10])


def bump_stat(counter_name: str, last_message: str) -> None:
    current = dict(stats_state.value)
    current[counter_name] = int(current[counter_name]) + 1
    current["last"] = last_message
    stats_state.set(current)


def validation_message(result) -> str | None:
    if result is True:
        return None
    if isinstance(result, str):
        return result
    if isinstance(result, dict) and not result.get("ok", True):
        return result.get("message") or "Validation failed."
    if isinstance(result, tuple) and result and not result[0]:
        return str(result[1]) if len(result) > 1 else "Validation failed."
    return None


def main() -> None:
    merged_df = load_editor_data()

    app.header("Editable Multi-Database DataFrame")
    app.info(
        "Edit any cell in the merged table. Each valid edit is written to the right SQLite database immediately."
    )
    app.caption(
        "This official example merges two SQLite databases into one editor with validation, immediate persistence, and live table views."
    )

    with app.sidebar:
        app.subheader("What this shows")
        app.markdown(
            """
            - `employees` table lives in `hr.db`
            - `assignments` table lives in `projects.db`
            - the editor shows one merged view
            - updates are validated and persisted per cell
            """
        )
        app.subheader("Column rules")
        app.markdown(
            """
            - `department`: dropdown
            - `status`: dropdown
            - `deadline`: date picker
            - `allocation_pct`: number editor with range validation
            - `is_active`: checkbox
            - `email`: server-side email validation
            """
        )

    app.divider()
    metrics = app.columns(3)
    with metrics[0]:
        app.metric("Saved Cells", lambda: stats_state.value["saved"])
    with metrics[1]:
        app.metric("Rejected Cells", lambda: stats_state.value["rejected"])
    with metrics[2]:
        app.metric("Last Result", lambda: stats_state.value["last"])

    def tracked_validator(event: dict, candidate_df: pd.DataFrame):
        result = validate_editor_change(event, candidate_df)
        message = validation_message(result)
        if message:
            add_audit_log(f"Rejected {event.get('field', 'edit')}: {message}")
            bump_stat("rejected", message)
        return result

    def handle_editor_change(updated_df: pd.DataFrame, event: dict) -> None:
        del updated_df
        message = persist_editor_change(event)
        refresh_live_tables()
        add_audit_log(message)
        bump_stat("saved", message)
        app.toast(message, variant="success", icon="circle-check")

    editor_state = app.data_editor(
        merged_df,
        key="official_multi_db_editor_v1",
        height=360,
        hide_index=True,
        theme="auto",
        validator=tracked_validator,
        on_change=handle_editor_change,
        column_config={
            "emp_id": {"editable": False, "width": 90},
            "name": {"type": "text"},
            "email": {"type": "text", "minWidth": 220},
            "department": {"type": "select", "options": DEPARTMENT_OPTIONS},
            "is_active": {"type": "checkbox", "width": 110},
            "project_name": {"type": "text", "minWidth": 180},
            "status": {"type": "select", "options": STATUS_OPTIONS},
            "deadline": {"type": "date", "minWidth": 140},
            "allocation_pct": {"type": "number", "min": 0, "max": 100, "step": 5},
        },
        grid_options={"animateRows": False},
    )

    def reset_demo() -> None:
        reset_demo_databases()
        editor_state.set(load_editor_data().to_dict("records"))
        refresh_live_tables()
        audit_log_state.set([])
        stats_state.set({"saved": 0, "rejected": 0, "last": "Demo reset"})
        app.toast("Demo databases reset.", variant="primary", icon="arrows-rotate")

    app.button("Reset Demo Data", on_click=reset_demo, variant="default", icon="arrows-rotate")

    app.divider()
    app.subheader("Live SQLite Tables")
    left, right = app.columns(2)
    with left:
        app.markdown("### hr.db / employees")
        app.dataframe(hr_table_state, height=220, theme="auto")
    with right:
        app.markdown("### projects.db / assignments")
        app.dataframe(
            project_table_state,
            height=220,
            theme="auto",
            theme_colors={
                "surface": "color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 6%)",
                "row_hover": "color-mix(in srgb, var(--vl-bg-card), var(--vl-primary) 12%)",
            },
        )

    app.divider()
    app.subheader("Recent Audit Log")
    if audit_log_state.value:
        app.markdown("\n".join(f"- {entry}" for entry in audit_log_state.value))
    else:
        app.caption("No edits yet.")


if __name__ == "__main__":
    main()
    app.run()