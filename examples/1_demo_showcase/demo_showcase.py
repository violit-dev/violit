from __future__ import annotations

import json
import sys
from typing import Any

import pandas as pd
import plotly.graph_objects as go

import violit as vl
from violit.state import get_session_store
from violit.theme import Theme


mode = 'lite' if '--lite' in sys.argv else 'ws'

SHOWCASE_THEME_OPTIONS = list(Theme.PRESETS.keys())

app = vl.App(
    title='Northstar Foundry',
    mode=mode,
    theme='violit_cloud_foundry',
    container_width='1240px',
    widget_gap='1rem',
)
app.configure_sidebar(width=312, min_width=272, max_width=384, resizable=True)
app.configure_widget('button', part_cls={'base': 'font-medium'})


def badge_chip(text: str, *, variant: str = 'neutral') -> None:
    app.badge(text, variant=variant, pill=True)


def money(value: int) -> str:
    return f'${value:,}'


def compact_label(text: str) -> None:
    app.caption(text)


def theme_badge_label(theme_name: str) -> str:
    return f"{theme_name.removeprefix('violit_').replace('_', ' ').title()} Theme"


months = pd.date_range('2025-01-01', periods=12, freq='ME').strftime('%b')

pipeline_df = pd.DataFrame(
    {
        'month': months,
        'net_new_arr': [188, 194, 201, 209, 218, 226, 223, 234, 243, 252, 264, 278],
        'expansion_arr': [92, 95, 98, 102, 107, 111, 114, 118, 123, 129, 136, 144],
        'inbound_tickets': [126, 131, 137, 143, 149, 154, 158, 163, 167, 171, 175, 179],
        'tickets_closed': [118, 123, 128, 134, 139, 145, 149, 154, 159, 164, 169, 174],
        'sla_hit_rate': [93, 93, 92, 92, 91, 90, 91, 92, 92, 93, 94, 95],
        'nps': [54, 55, 56, 57, 58, 59, 60, 62, 63, 64, 66, 68],
    }
)
pipeline_df['total_arr'] = pipeline_df['net_new_arr'] + pipeline_df['expansion_arr']

customer_df = pd.DataFrame(
    [
        {'company': 'Helio Bank', 'segment': 'Enterprise', 'plan': 'Scale', 'health': 'Strong', 'mrr': 84000, 'seats': 124, 'region': 'US', 'last_seen': '2h ago', 'owner': 'Ari'},
        {'company': 'Baseline AI', 'segment': 'Growth', 'plan': 'Growth', 'health': 'Watch', 'mrr': 18200, 'seats': 34, 'region': 'EU', 'last_seen': '5h ago', 'owner': 'Noa'},
        {'company': 'Aster Retail', 'segment': 'SMB', 'plan': 'Starter', 'health': 'Strong', 'mrr': 6400, 'seats': 12, 'region': 'APAC', 'last_seen': '18m ago', 'owner': 'June'},
        {'company': 'Northwind Ops', 'segment': 'Enterprise', 'plan': 'Scale', 'health': 'At Risk', 'mrr': 67300, 'seats': 97, 'region': 'US', 'last_seen': '1d ago', 'owner': 'Ira'},
        {'company': 'Tidal Labs', 'segment': 'Growth', 'plan': 'Growth', 'health': 'Strong', 'mrr': 24100, 'seats': 42, 'region': 'US', 'last_seen': '3h ago', 'owner': 'Mina'},
        {'company': 'Signal Forge', 'segment': 'Enterprise', 'plan': 'Enterprise', 'health': 'Watch', 'mrr': 91300, 'seats': 156, 'region': 'EU', 'last_seen': '8h ago', 'owner': 'Ari'},
        {'company': 'Cinder Health', 'segment': 'Growth', 'plan': 'Growth', 'health': 'At Risk', 'mrr': 28600, 'seats': 38, 'region': 'US', 'last_seen': '2d ago', 'owner': 'June'},
        {'company': 'Mapline Fleet', 'segment': 'SMB', 'plan': 'Starter', 'health': 'Strong', 'mrr': 5100, 'seats': 9, 'region': 'LATAM', 'last_seen': '44m ago', 'owner': 'Noa'},
    ]
)

rollout_seed = pd.DataFrame(
    [
        {'cohort': 'Design partners', 'traffic_pct': 5, 'status': 'ready', 'owner': 'Mina', 'region': 'US-East', 'latency_ms': 128},
        {'cohort': 'Self-serve teams', 'traffic_pct': 15, 'status': 'warming', 'owner': 'Ira', 'region': 'US-West', 'latency_ms': 142},
        {'cohort': 'Enterprise accounts', 'traffic_pct': 35, 'status': 'staged', 'owner': 'Ari', 'region': 'EU', 'latency_ms': 167},
        {'cohort': 'Support inbox', 'traffic_pct': 20, 'status': 'ready', 'owner': 'June', 'region': 'APAC', 'latency_ms': 151},
    ]
)

launch_events_df = pd.DataFrame(
    [
        {'time': '08:45', 'event': 'Canary checks passed', 'owner': 'Ops'},
        {'time': '09:10', 'event': 'Billing connector stabilized', 'owner': 'Platform'},
        {'time': '09:36', 'event': 'Support macros synced', 'owner': 'CX'},
        {'time': '10:05', 'event': 'Customer-facing banner scheduled', 'owner': 'PMM'},
    ]
)

workflow_templates = [
    'Expansion playbook',
    'Renewal rescue workflow',
    'Escalation routing',
    'VIP onboarding sequence',
]

selected_customer = app.state({}, key='u0_new_demo_selected_customer')
customer_query = app.state('', key='u0_new_demo_customer_query')
customer_segment = app.state('All', key='u0_new_demo_customer_segment')
customer_priority_only = app.state(False, key='u0_new_demo_customer_priority_only')
rollout_rows = app.state(rollout_seed.copy(), key='u0_new_demo_rollout_rows')
workflow_spec = app.state(
    {
        'name': 'Executive expansion signal',
        'trigger': 'MRR drops 10% week-over-week',
        'channel': 'Slack + inbox',
        'priority': 'High',
        'notes': 'Create an owner task, attach usage context, and ping the CSM lead.',
        'notify_exec': True,
    },
    key='u0_new_demo_workflow_spec',
)
support_messages = app.state([], key='u0_new_demo_support_messages')
pulse_tick = app.state(0, key='u0_new_demo_pulse_tick')
pulse_running = app.state(False, key='u0_new_demo_pulse_running')
pulse_handle = app.state(None, key='u0_new_demo_pulse_handle')
active_theme_name = app.state('violit_cloud_foundry', key='u0_new_demo_active_theme_name')

session_theme_name = get_session_store()['theme'].preset_name
if active_theme_name.value != session_theme_name:
    active_theme_name.set(session_theme_name)


def support_boot_messages() -> list[dict[str, Any]]:
    return [
        {
            'role': 'assistant',
            'content': 'Northstar Copilot is ready. Ask about customers, rollout plans, workflow automation, or the current launch surface.',
            'summary': 'This is a local pseudo-agent that uses agent_history and managed_chat_input.',
            'trace': [
                {'kind': 'status', 'title': 'Boot', 'text': 'Workspace context loaded.'},
                {'kind': 'observation', 'title': 'Coverage', 'text': 'Overview, customers, operations, workflow studio, and settings are mapped.'},
            ],
            'artifacts': [
                {'kind': 'guide', 'title': 'Suggested prompts', 'text': 'Try: summarize at-risk customers / explain the rollout cohorts / draft a workflow rule'},
            ],
            'status_text': 'Waiting for a prompt.',
        }
    ]


support_messages.set(support_boot_messages())


def prompt_text(prompt: Any) -> str:
    if isinstance(prompt, dict):
        return str(prompt.get('text') or '').strip()
    return str(prompt or '').strip()


def prompt_files(prompt: Any) -> list[str]:
    if not isinstance(prompt, dict):
        return []
    results = []
    for item in prompt.get('files') or []:
        name = getattr(item, 'name', None)
        if not name and isinstance(item, dict):
            name = item.get('name')
        if name:
            results.append(str(name))
    return results


def prompt_has_audio(prompt: Any) -> bool:
    return isinstance(prompt, dict) and bool(prompt.get('audio'))


def reply_chunks(text: str):
    parts = [part.strip() for part in text.split('\n\n') if part.strip()]
    for index, part in enumerate(parts):
        yield part + ('\n\n' if index < len(parts) - 1 else '')


def support_plan(text: str) -> dict[str, Any]:
    normalized = (text or '').lower()
    if any(token in normalized for token in ['customer', 'account', 'health', 'mrr']):
        return {
            'intent': 'Customer intelligence',
            'summary': 'The request maps to customer filtering, risk review, and account detail flows.',
            'trace': [
                {'kind': 'tool_call', 'title': 'scan-customers', 'text': 'Reviewed the Customer Radar page and the selected-customer detail panel.'},
                {'kind': 'observation', 'title': 'filters', 'text': 'The page supports live search, segment filters, and a risk-only toggle.'},
                {'kind': 'observation', 'title': 'detail flow', 'text': 'Clicking a dataframe cell fills a right-side account detail summary and metadata panel.'},
            ],
            'artifacts': [
                {'kind': 'pattern', 'title': 'Review flow', 'text': 'filter -> click table cell -> inspect account detail -> trigger playbook'},
            ],
            'answer': 'Open Customer Radar for the most realistic account-review flow. Search and segment filters narrow the list, and any clicked row opens a compact detail view with ownership and risk context.',
        }
    if any(token in normalized for token in ['rollout', 'launch', 'latency', 'deploy', 'cohort']):
        return {
            'intent': 'Rollout operations',
            'summary': 'The request maps to phased launch operations and editable rollout cohorts.',
            'trace': [
                {'kind': 'tool_call', 'title': 'scan-operations', 'text': 'Reviewed launch status, confirm dialog, data editor cohorts, and launch timeline.'},
                {'kind': 'observation', 'title': 'cohorts', 'text': 'Rollout cohorts are editable in-place and update the preview summary immediately.'},
                {'kind': 'observation', 'title': 'status surface', 'text': 'The page combines progress, status, toast actions, and plotly launch telemetry.'},
            ],
            'artifacts': [
                {'kind': 'checklist', 'title': 'Ops surface', 'text': 'status, progress, dialog, data_editor, plotly_chart, launch event table'},
            ],
            'answer': 'Operations is the launch control page. It is where you can validate cohort weights, review latency trends, and kick off a launch via a dialog-confirmed action rather than a static marketing card.',
        }
    if any(token in normalized for token in ['workflow', 'studio', 'form', 'automation']):
        return {
            'intent': 'Workflow studio',
            'summary': 'The request maps to form-driven automation setup and JSON export.',
            'trace': [
                {'kind': 'tool_call', 'title': 'scan-studio', 'text': 'Reviewed the playbook form, template popover, and JSON export card.'},
                {'kind': 'observation', 'title': 'form flow', 'text': 'The studio uses a real form submit action and keeps a current workflow spec preview.'},
                {'kind': 'observation', 'title': 'handoff', 'text': 'The resulting configuration can be downloaded as a JSON payload.'},
            ],
            'artifacts': [
                {'kind': 'guide', 'title': 'Studio flow', 'text': 'choose trigger -> capture owner notes -> submit -> inspect preview -> export JSON'},
            ],
            'answer': 'Workflow Studio is built like an internal operations tool rather than a showcase toy. The form composes a realistic automation spec and the preview panel lets users verify what would actually be shipped.',
        }
    return {
        'intent': 'Workspace tour',
        'summary': 'The request maps to a cross-page tour of the whole product-style demo.',
        'trace': [
            {'kind': 'tool_call', 'title': 'scan-workspace', 'text': 'Reviewed the overview, customers, operations, copilot, studio, and settings pages.'},
            {'kind': 'observation', 'title': 'curation', 'text': 'The sidebar is intentionally limited to six pages so the app feels like a real product, not a wall of unrelated widgets.'},
            {'kind': 'observation', 'title': 'design', 'text': 'The theme mixes atmospheric hero treatment with restrained card borders and product-style panels.'},
        ],
        'artifacts': [
            {'kind': 'guide', 'title': 'Recommended path', 'text': 'Overview -> Customer Radar -> Operations -> Copilot -> Workflow Studio -> Settings'},
        ],
        'answer': 'Start on Overview for the narrative, move to Customer Radar and Operations for hands-on testing, then finish in Copilot and Workflow Studio to see the newest high-level chat and form-driven workflows in a realistic app shell.',
    }


def build_support_reply(prompt: Any, *, persona: str, reply_mode: str):
    message = prompt_text(prompt)
    files = prompt_files(prompt)
    has_audio = prompt_has_audio(prompt)
    if not message and not files and not has_audio:
        raise RuntimeError('Please send a message, file, or audio input.')

    plan = support_plan(message)
    persona_line = {
        'Guide': 'Guide mode keeps the answer practical and page-oriented.',
        'Architect': 'Architect mode emphasizes surface composition and API choices.',
        'Debugger': 'Debugger mode emphasizes edge cases, state transitions, and testable flows.',
    }.get(persona, f'{persona} mode is active.')

    answer = f"{persona_line}\n\n{plan['answer']}"
    context_lines = []
    if message:
        context_lines.append(f'Prompt: {message}')
    if files:
        context_lines.append('Files: ' + ', '.join(files))
    if has_audio:
        context_lines.append('Audio was attached.')
    if context_lines:
        answer += '\n\nInput context\n- ' + '\n- '.join(context_lines)

    def stream():
        yield {'type': 'status', 'text': f'{persona} copilot is classifying the request.'}
        yield {'type': 'step', 'kind': 'status', 'title': 'Intent', 'text': plan['intent']}
        for item in plan['trace']:
            yield {'type': 'step', **item}
        yield {'type': 'summary', 'text': plan['summary']}
        if str(reply_mode).lower().strip() == 'streaming':
            yield {'type': 'status', 'text': 'Streaming the response.'}
            for chunk in reply_chunks(answer):
                yield {'type': 'text', 'text': chunk}
        else:
            yield {'type': 'text', 'text': answer, 'stream': False}
        for artifact in plan['artifacts']:
            yield {'type': 'artifact', 'artifact': artifact}
        yield {'type': 'done'}

    return stream()


def filtered_customers() -> pd.DataFrame:
    df = customer_df.copy()
    query = customer_query.value.strip().lower()
    segment = customer_segment.value
    if query:
        mask = df.apply(lambda row: query in row['company'].lower() or query in row['owner'].lower() or query in row['region'].lower(), axis=1)
        df = df[mask]
    if segment != 'All':
        df = df[df['segment'] == segment]
    if customer_priority_only.value:
        df = df[df['health'].isin(['At Risk', 'Watch'])]
    return df.reset_index(drop=True)


def launch_latency_figure() -> go.Figure:
    current = rollout_rows.value.copy()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=current['cohort'],
            y=current['traffic_pct'],
            name='Traffic %',
            marker=dict(color='#5b7cff'),
            opacity=0.85,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=current['cohort'],
            y=current['latency_ms'],
            name='Latency (ms)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='#171717', width=3),
            marker=dict(size=8),
        )
    )
    fig.update_layout(
        height=360,
        margin=dict(l=16, r=16, t=28, b=16),
        legend=dict(orientation='h', y=1.08),
        yaxis=dict(title='Traffic %'),
        yaxis2=dict(title='Latency (ms)', overlaying='y', side='right'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def arr_momentum_figure() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=pipeline_df['month'],
            y=pipeline_df['net_new_arr'],
            name='Net new ARR',
            marker=dict(color='#5b7cff'),
            opacity=0.92,
        )
    )
    fig.add_trace(
        go.Bar(
            x=pipeline_df['month'],
            y=pipeline_df['expansion_arr'],
            name='Expansion ARR',
            marker=dict(color='#91a8ff'),
            opacity=0.88,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pipeline_df['month'],
            y=pipeline_df['total_arr'],
            name='Total ARR',
            mode='lines+markers',
            line=dict(color='#111827', width=3),
            marker=dict(size=7, color='#111827'),
        )
    )
    fig.update_layout(
        height=340,
        margin=dict(l=16, r=16, t=12, b=16),
        barmode='group',
        hovermode='x unified',
        legend=dict(orientation='h', y=1.08),
        xaxis=dict(title=None, type='category', showgrid=False),
        yaxis=dict(title='ARR ($k)', gridcolor='rgba(148,163,184,0.18)', zeroline=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def service_load_figure() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pipeline_df['month'],
            y=pipeline_df['inbound_tickets'],
            name='Inbound tickets',
            mode='lines+markers',
            line=dict(color='#7c93ff', width=2.5),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(124,147,255,0.16)',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pipeline_df['month'],
            y=pipeline_df['tickets_closed'],
            name='Resolved tickets',
            mode='lines+markers',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=6),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pipeline_df['month'],
            y=pipeline_df['sla_hit_rate'],
            name='SLA hit rate',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='#0f172a', width=2, dash='dash'),
            marker=dict(size=5),
        )
    )
    fig.update_layout(
        height=340,
        margin=dict(l=16, r=16, t=12, b=16),
        hovermode='x unified',
        legend=dict(orientation='h', y=1.08),
        xaxis=dict(title=None, type='category', showgrid=False),
        yaxis=dict(title='Tickets', gridcolor='rgba(148,163,184,0.18)', zeroline=False),
        yaxis2=dict(title='SLA %', overlaying='y', side='right', range=[84, 100], showgrid=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def overview_page() -> None:
    app.header('Northstar Foundry')
    app.caption('A product-style showcase for growth, rollout, support, and automation operations.')

    top = app.columns([1.15, 1], gap='large', vertical_alignment='center')
    with top[0]:
        with app.container(border=True, cls='rounded-[32px] bg-white/85 p-7 shadow-[0_32px_90px_-52px_rgba(15,23,42,0.28)]'):
            badge_chip('New Experience', variant='success')
            app.title('A modern customer operations workspace built with real Violit widgets.')
            app.text(
                'The design is intentionally product-like: atmospheric but restrained, with launch metrics, customer intelligence, editable operations, a support copilot, and a workflow studio split into focused pages.',
                muted=True,
            )
            ctas = app.columns(3, gap='small')
            with ctas[0]:
                app.button('Open Operations', on_click=lambda: app.switch_page('Operations'), cls='w-full')
            with ctas[1]:
                app.button('Review Customers', on_click=lambda: app.switch_page('Customer Radar'), variant='neutral', cls='w-full')
            with ctas[2]:
                app.button('Try Copilot', on_click=lambda: app.switch_page('Copilot'), variant='neutral', cls='w-full')
            app.space('0.75rem')
            compact_label('Inspired by the product-marketing rhythm of Stripe, Vercel, Mintlify, and Linear.')

    with top[1]:
        with app.container(border=True, cls='rounded-[30px] bg-white/92 p-5 shadow-[0_24px_72px_-46px_rgba(15,23,42,0.26)]'):
            compact_label('LIVE PREVIEW')
            app.subheader('Launch snapshot')
            metrics = app.columns(3, gap='small')
            with metrics[0]:
                app.metric('ARR', money(int(pipeline_df['total_arr'].sum()) * 1000), '+12%')
            with metrics[1]:
                app.metric('NPS', str(int(pipeline_df['nps'].iloc[-1])), '+4')
            with metrics[2]:
                app.metric('Open risks', '3', '-1')
            app.space('0.5rem')
            app.dataframe(customer_df[['company', 'health', 'mrr']].head(4), height=210, hide_index=True, use_container_width=True)

    app.space('0.75rem')
    kpis = app.columns(4, gap='large')
    metrics_data = [
        ('Expansion ARR', money(int(pipeline_df['expansion_arr'].sum()) * 1000), '+9%'),
        ('Tickets closed', str(int(pipeline_df['tickets_closed'].sum())), '+15%'),
        ('Active cohorts', str(len(rollout_rows.value)), 'editable'),
        ('Automation rules', '14', '4 live'),
    ]
    for column, (label, value, delta) in zip(kpis, metrics_data):
        with column:
            app.metric(label, value, delta)

    app.divider()
    charts = app.columns(2, gap='large', vertical_alignment='top')
    with charts[0]:
        app.subheader('ARR momentum')
        app.plotly_chart(arr_momentum_figure(), use_container_width=True)
    with charts[1]:
        app.subheader('Service load')
        app.plotly_chart(service_load_figure(), use_container_width=True)

    app.divider()
    next_steps = app.columns(3, gap='large', equal_height=True)
    cards = [
        ('Customer Radar', 'Search live accounts, filter the roster, and inspect at-risk details from an interactive dataframe.', 'Customer Radar'),
        ('Operations', 'Adjust rollout cohorts, watch launch status, and confirm a release from a realistic control plane.', 'Operations'),
        ('Workflow Studio', 'Compose a handoff-ready automation rule and export its spec as JSON.', 'Workflow Studio'),
    ]
    for column, (title, text, target) in zip(next_steps, cards):
        with column:
            with app.container(border=True, cls='rounded-[26px] bg-white/82 p-5 shadow-[0_18px_48px_-34px_rgba(15,23,42,0.16)] h-full'):
                compact_label('PAGE')
                app.subheader(title)
                app.text(text, muted=True)
                app.button(f'Open {title}', on_click=lambda target=target: app.switch_page(target), variant='neutral')


def customer_radar_page() -> None:
    app.header('Customer Radar')
    app.caption('A realistic account-review workspace built around live filters and table-driven detail inspection.')

    segment_options = ['All', 'Enterprise', 'Growth', 'SMB']
    visible_customers = filtered_customers()
    selected_company = str(selected_customer.value.get('company') or '').strip() if isinstance(selected_customer.value, dict) else ''
    current_segment_index = segment_options.index(customer_segment.value) if customer_segment.value in segment_options else 0

    if visible_customers.empty:
        if selected_customer.value:
            selected_customer.set({})
    else:
        visible_rows = visible_customers.to_dict('records')
        matching_row = next((row for row in visible_rows if row.get('company') == selected_company), None)
        target_row = matching_row or visible_rows[0]
        if selected_customer.value != target_row:
            selected_customer.set(target_row)

    controls = app.columns([1.2, 1, 0.8], gap='small')
    with controls[0]:
        app.text_input(
            'Search customers',
            value=customer_query.value,
            key='u0_new_demo_customer_query_input',
            on_change=lambda value: customer_query.set(value),
            on_submit=lambda value: customer_query.set(value),
            live_update=True,
        )
    with controls[1]:
        app.selectbox('Segment', segment_options, index=current_segment_index, key='u0_new_demo_customer_segment_input', on_change=lambda value: customer_segment.set(value))
    with controls[2]:
        app.toggle('Priority only', value=customer_priority_only.value, key='u0_new_demo_customer_priority_only_input', on_change=lambda value: customer_priority_only.set(value))

    def on_customer_cell(cell: Any) -> None:
        if isinstance(cell, dict):
            selected_customer.set(cell.get('rowData') or {})

    @app.reactivity
    def render_customer_radar_results() -> None:
        visible_customers = filtered_customers()
        selected_company = str(selected_customer.value.get('company') or '').strip() if isinstance(selected_customer.value, dict) else ''

        if visible_customers.empty:
            if selected_customer.value:
                selected_customer.set({})
        else:
            visible_rows = visible_customers.to_dict('records')
            matching_row = next((row for row in visible_rows if row.get('company') == selected_company), None)
            target_row = matching_row or visible_rows[0]
            if selected_customer.value != target_row:
                selected_customer.set(target_row)

        selected_panel, table_panel = app.columns([0.92, 1.4], gap='large', vertical_alignment='top')

        with table_panel:
            app.dataframe(
                visible_customers,
                height=420,
                hide_index=True,
                use_container_width=True,
                on_cell_clicked=on_customer_cell,
            )
            compact_label(f'{len(visible_customers)} accounts match the current filters.')

        with selected_panel:
            if selected_customer.value:
                current = selected_customer.value
                with app.container(border=True, cls='rounded-[28px] bg-white/90 p-5 shadow-[0_18px_48px_-34px_rgba(15,23,42,0.18)]'):
                    badge_chip(current.get('health', 'Unknown'), variant='warning' if current.get('health') in {'Watch', 'At Risk'} else 'success')
                    app.subheader(current.get('company', 'Account detail'))
                    app.text(f"Owner: {current.get('owner', '-')} · Region: {current.get('region', '-')} · Last seen: {current.get('last_seen', '-')}", muted=True)
                    detail_cols = app.columns(2, gap='small')
                    with detail_cols[0]:
                        app.metric('MRR', money(int(current.get('mrr', 0))), current.get('plan', '-'))
                    with detail_cols[1]:
                        app.metric('Seats', str(current.get('seats', 0)), current.get('segment', '-'))
                    app.divider()
                    with app.popover('Recommended playbooks', use_container_width=True):
                        app.text('1. Trigger success-plan review')
                        app.text('2. Schedule executive check-in')
                        app.text('3. Attach deployment telemetry to the next outreach')
                    app.space('0.5rem')
                    app.json(current, expanded=False)
            else:
                app.callout(
                    'Click any row in the table to inspect a customer record and recommended next actions.',
                    title='Select an account',
                    variant='info',
                )

    render_customer_radar_results()


def operations_page() -> None:
    app.header('Operations')
    app.caption('Phased launch control with status, confirmation dialog, editable cohorts, and telemetry.')

    @app.dialog('Start rollout')
    def launch_dialog() -> None:
        app.text('Kick off the next rollout window for the selected cohorts?')
        app.warning('This demo does not call external systems, but it exercises the real dialog and toast flow.')
        row = app.columns(2, gap='small')
        with row[0]:
            app.button('Cancel', on_click=launch_dialog.close, variant='neutral', use_container_width=True)
        with row[1]:
            app.button(
                'Start launch',
                on_click=lambda: (app.toast('Rollout window started', icon='rocket', variant='success'), launch_dialog.close()),
                variant='success',
                use_container_width=True,
            )

    status_row = app.columns([1.2, 0.9, 0.9], gap='small')
    with status_row[0]:
        launch_state = app.radio('Launch state', ['running', 'complete', 'error'], horizontal=True)
    with status_row[1]:
        app.button('Confirm rollout', on_click=launch_dialog.open, cls='w-full')
    with status_row[2]:
        app.button('Save cohorts', on_click=lambda: app.toast('Cohorts saved', icon='circle-check', variant='success'), variant='neutral', cls='w-full')

    app.status(lambda: f'Foundry release state = {launch_state.value}', state=launch_state, expanded=True)
    app.progress(lambda: int(sum(rollout_rows.value['traffic_pct']) % 100))

    tabs = app.tabs(['Cohorts', 'Telemetry', 'Launch log'])
    with tabs[0]:
        app.data_editor(
            rollout_rows.value,
            num_rows='dynamic',
            height=320,
            hide_index=True,
            use_container_width=True,
            on_change=lambda new_df: rollout_rows.set(new_df),
        )
        app.text(lambda: f'Current cohorts: {len(rollout_rows.value)}', muted=True, size='small')
    with tabs[1]:
        app.plotly_chart(launch_latency_figure(), use_container_width=True)
    with tabs[2]:
        app.table(launch_events_df)


def copilot_page() -> None:
    app.header('Copilot')
    app.caption('High-level chat surface using agent_history plus managed_chat_input.')

    app.callout(
        'This pseudo-agent is local-only, but it exercises the same event schema used by the current production chat surface.',
        title='Northstar Copilot',
        variant='info',
    )

    ctl = app.columns([1.2, 1, 1, 1], gap='small')
    with ctl[0]:
        persona = app.selectbox('Persona', ['Guide', 'Architect', 'Debugger'], value='Guide', key='u0_new_demo_persona_select')
    with ctl[1]:
        reply_mode = app.selectbox('Reply mode', ['streaming', 'instant'], value='streaming', key='u0_new_demo_reply_mode_select')
    with ctl[2]:
        show_trace = app.toggle('Show trace', value=True, key='u0_new_demo_show_trace_toggle')
    with ctl[3]:
        show_artifacts = app.toggle('Show artifacts', value=True, key='u0_new_demo_show_artifacts_toggle')

    app.button('Reset chat', on_click=lambda: support_messages.set(support_boot_messages()), variant='neutral', icon='arrow-rotate-left')
    compact_label('Prompt ideas: summarize at-risk customers / explain rollout cohorts / draft a workflow rule')

    @app.reactivity
    def render_chat() -> None:
        app.agent_history(
            support_messages,
            height='62vh',
            border=True,
            show_trace=show_trace.value,
            show_artifacts=show_artifacts.value,
            show_summary=True,
            show_status=True,
        )

    render_chat()
    app.managed_chat_input(
        'Ask Northstar Copilot...',
        messages=support_messages,
        on_submit=lambda prompt: build_support_reply(prompt, persona=persona.value, reply_mode=reply_mode.value),
        pinned=False,
        auto_scroll='bottom',
        stream_speed='smooth',
        accept_file='multiple',
        accept_audio=True,
        audio_sample_rate=16000,
        max_chars=1000,
    )


def workflow_studio_page() -> None:
    app.header('Workflow Studio')
    app.caption('A compact internal tool for authoring automation rules and exporting the resulting spec.')

    left, right = app.columns([1.05, 0.95], gap='large', vertical_alignment='top')
    with left:
        with app.container(border=True, cls='rounded-[28px] bg-white/90 p-5 shadow-[0_18px_48px_-34px_rgba(15,23,42,0.16)]'):
            with app.popover('Recommended templates', use_container_width=True):
                for template in workflow_templates:
                    app.text(f'- {template}')

            with app.form(key='u0_new_demo_workflow_form', clear_on_submit=False, enter_to_submit=True):
                flow_name = app.text_input('Workflow name', value=workflow_spec.value['name'])
                trigger = app.selectbox('Trigger', ['MRR drops 10% week-over-week', 'Health flips to At Risk', 'Support queue breaches SLA', 'Expansion opportunity detected'], value=workflow_spec.value['trigger'])
                channel = app.selectbox('Routing channel', ['Slack + inbox', 'Email only', 'In-app task', 'Pager rotation'], value=workflow_spec.value['channel'])
                priority = app.select_slider('Priority', options=['Low', 'Medium', 'High', 'Urgent'], value=workflow_spec.value['priority'])
                notes = app.text_area('Operational notes', value=workflow_spec.value['notes'], height=120)
                notify_exec = app.checkbox('Notify executive sponsor', value=workflow_spec.value['notify_exec'])

                def submit_workflow() -> None:
                    workflow_spec.set(
                        {
                            'name': flow_name.value,
                            'trigger': trigger.value,
                            'channel': channel.value,
                            'priority': priority.value,
                            'notes': notes.value,
                            'notify_exec': notify_exec.value,
                        }
                    )
                    app.toast('Workflow spec updated', icon='wand-magic-sparkles', variant='success')

                app.form_submit_button('Update workflow', on_click=submit_workflow, type='primary', use_container_width=True, icon='wand-magic-sparkles')

    with right:
        with app.container(border=True, cls='rounded-[28px] bg-white/90 p-5 shadow-[0_18px_48px_-34px_rgba(15,23,42,0.16)]'):
            compact_label('CURRENT SPEC')
            app.subheader(workflow_spec.value['name'])
            app.text(f"Trigger: {workflow_spec.value['trigger']}", muted=True)
            app.text(f"Channel: {workflow_spec.value['channel']} · Priority: {workflow_spec.value['priority']}", muted=True)
            app.callout(workflow_spec.value['notes'], title='Notes', variant='info')
            if workflow_spec.value['notify_exec']:
                badge_chip('Exec sponsor notified', variant='success')
            else:
                badge_chip('Exec sponsor not notified', variant='neutral')
            app.space('0.75rem')
            app.json(workflow_spec.value, expanded=False)
            app.space('0.75rem')
            app.download_button(
                'Download JSON',
                data=json.dumps(workflow_spec.value, ensure_ascii=False, indent=2),
                file_name='northstar_workflow_spec.json',
                mime='application/json',
                icon='file-code',
                variant='neutral',
            )


def settings_page() -> None:
    app.header('Settings')
    app.caption('Theme controls, animation behavior, live status, and an interval-driven pulse.')

    current_theme_index = SHOWCASE_THEME_OPTIONS.index(active_theme_name.value) if active_theme_name.value in SHOWCASE_THEME_OPTIONS else 0
    controls = app.columns(2, gap='large')
    with controls[0]:
        theme_choice = app.selectbox('Theme', SHOWCASE_THEME_OPTIONS, index=current_theme_index, key='u0_new_demo_theme_choice')
        app.button(
            'Apply theme',
            on_click=lambda: (
                active_theme_name.set(theme_choice.value),
                app.set_theme(theme_choice.value),
                app.toast(f'Theme changed to {theme_choice.value}', icon='palette', variant='success'),
            ),
        )
    with controls[1]:
        animation_mode = app.radio('Animation mode', ['soft', 'hard'], horizontal=True)
        app.button(
            'Update animation',
            on_click=lambda: (app.set_animation_mode(animation_mode.value), app.toast(f'Animation mode set to {animation_mode.value}', icon='sparkles', variant='neutral')),
            variant='neutral',
        )

    app.divider()
    deploy_state = app.radio('Deployment state', ['running', 'complete', 'error'], horizontal=True)
    app.status(lambda: f'Workspace deployment is {deploy_state.value}', state=deploy_state, expanded=True)

    app.divider()

    def start_pulse() -> None:
        if pulse_running.value:
            return
        handle = app.interval(lambda: pulse_tick.set(pulse_tick.value + 1), ms=1000)
        pulse_handle.set(handle)
        pulse_running.set(True)

    def stop_pulse() -> None:
        if pulse_running.value and pulse_handle.value:
            pulse_handle.value.stop()
            pulse_running.set(False)

    pulse_row = app.columns(3, gap='small')
    with pulse_row[0]:
        app.button('Start pulse', on_click=start_pulse, variant='success', cls='w-full')
    with pulse_row[1]:
        app.button('Stop pulse', on_click=stop_pulse, variant='warning', cls='w-full')
    with pulse_row[2]:
        app.button('Reset pulse', on_click=lambda: pulse_tick.set(0), variant='neutral', cls='w-full')

    app.metric('Pulse count', pulse_tick)
    app.progress(lambda: int(pulse_tick.value % 100))
    app.json(
        lambda: {
            'theme': theme_choice.value,
            'animation_mode': animation_mode.value,
            'deployment_state': deploy_state.value,
            'pulse_running': pulse_running.value,
            'pulse_tick': pulse_tick.value,
        },
        expanded=False,
    )


with app.sidebar:
    with app.container(border=True, cls='rounded-[28px] bg-white/82 p-5 shadow-[0_20px_56px_-38px_rgba(15,23,42,0.18)]'):
        compact_label('NORTHSTAR FOUNDRY')
        app.text('Customer operations workspace', size='large', cls='font-semibold')
        app.text('Curated pages, real widget flows, and a modern product-marketing tone.', muted=True, size='small')
        app.space('0.5rem')
        badge_chip(lambda: theme_badge_label(active_theme_name.value), variant='success')
    app.divider()
    compact_label('FOCUSED MENU')
    app.text('Each page owns a clear job so the app feels like a believable product rather than a widget dump.', muted=True, size='small')


app.navigation(
    [
        vl.Page(overview_page, title='Overview', icon='house', url_path='overview'),
        vl.Page(customer_radar_page, title='Customer Radar', icon='users', url_path='customers'),
        vl.Page(operations_page, title='Operations', icon='tower-broadcast', url_path='operations'),
        vl.Page(copilot_page, title='Copilot', icon='comment-dots', url_path='copilot'),
        vl.Page(workflow_studio_page, title='Workflow Studio', icon='wand-magic-sparkles', url_path='studio'),
        vl.Page(settings_page, title='Settings', icon='gear', url_path='settings'),
    ]
)


if __name__ == '__main__':
    app.run()