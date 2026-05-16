# 1. Violit Showcase Demo

This example is the main polished, user-facing Violit showcase.

It is the best place to start if you want one file that feels like a small product rather than a widget dump. The app is called `Northstar Foundry` and combines charts, reactive state, editable data, built-in chat widgets, workflow authoring, and live runtime theme switching.

## Files

- `demo_showcase.py`: the current showcase app
- `old_archive_demo_showcase.py`: the previous archived showcase version

## Run

From this folder:

```bash
cd examples/1_demo_showcase
python demo_showcase.py
```

Or with the Violit CLI:

```bash
cd examples/1_demo_showcase
violit run demo_showcase.py
```

By default, the app runs in WebSocket mode and starts with the `violit_cloud_foundry` theme.

You can also run the same example in Lite mode:

```bash
python demo_showcase.py --lite
```

## What This Example Shows

This showcase includes six focused pages in one sidebar app:

- `Overview`: a product-style landing page with launch metrics, curated charts, and next-step cards
- `Customer Radar`: live search, segment filters, risk filtering, dataframe interaction, and account detail sync
- `Operations`: rollout cohorts, editable launch controls, status surfaces, dialogs, and chart telemetry
- `Copilot`: `agent_history(...)` plus `managed_chat_input(...)` with attachments, audio capture, and pseudo-agent replies
- `Workflow Studio`: form-driven workflow authoring with a current-spec preview and JSON download
- `Settings`: runtime theme switching across all registered themes, animation controls, status widgets, and interval-based updates

There is no database setup and no external AI API key required.

## Why It Is Useful

This example is meant for users who want to learn Violit from a realistic multi-page app instead of isolated snippets.

It demonstrates:

- built-in sidebar navigation with `vl.Page(...)`
- `State` shared across pages
- reactive rendering with `@app.reactivity`
- `plotly_chart`, dataframe, data editor, forms, dialogs, and status widgets
- the current high-level chat stack with `agent_history(...)` and `managed_chat_input(...)`
- runtime theme switching, including all themes registered in `Theme.PRESETS`

## Key App Setup

The example chooses WebSocket mode by default and falls back to Lite mode when `--lite` is provided:

```python
mode = 'lite' if '--lite' in sys.argv else 'ws'

app = vl.App(
    title='Northstar Foundry',
    mode=mode,
    theme='violit_cloud_foundry',
    container_width='1240px',
    widget_gap='1rem',
)
```

It also exposes every registered Violit theme in the `Settings` page:

```python
SHOWCASE_THEME_OPTIONS = list(Theme.PRESETS.keys())
```

## Good Pages To Explore First

If you want a quick feel for the current showcase, start here:

- `Overview` for the visual direction, metric cards, and themed Plotly charts
- `Customer Radar` for live filtering and dataframe-driven detail views
- `Copilot` for the built-in chat experience with managed input, file attachment, and audio capture
- `Settings` for trying all available themes and runtime controls

## Notes

- The pseudo-copilot replies are local demo logic, not a real LLM backend.
- The app is intentionally styled to feel like a believable internal product surface.
- If you are studying Violit patterns, this is the most complete single-file example in the repository.
