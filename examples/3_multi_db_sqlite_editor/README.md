# Multi-DB SQLite Editor

This official Violit example shows how to edit one merged DataFrame backed by two separate SQLite databases.

What it demonstrates:

- immediate per-cell persistence into `hr.db` and `projects.db`
- server-side validation for text, date, number, and boolean fields
- `data_editor` with mixed editor types and live database table views

Run it:

```bash
python demo_multi_db_sqlite_editor.py
```

Optional:

```bash
python demo_multi_db_sqlite_editor.py --port 8014
python demo_multi_db_sqlite_editor.py --native
```

Notes:

- The SQLite files are created automatically on first run.
- Use the `Reset Demo Data` button to restore the initial records.
