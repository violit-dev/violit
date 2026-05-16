import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import violit as vl


app = vl.App(title="GitHub Issue 25 - Styling Over Multiple Columns")


ROWS = [
	("Dataset", ["Sales", "Marketing", "Operations"]),
	("Granularity", ["Daily", "Weekly", "Monthly"]),
	("Region", ["Global", "EMEA", "APAC"]),
]


def label_pill(label: str) -> str:
	return f"""
	<div style="
		display: inline-flex;
		align-items: center;
		padding: 0.7rem 0.9rem;
		border-radius: 999px;
		border: 1px solid var(--vl-border);
		background: color-mix(in srgb, var(--vl-bg-card) 82%, white 18%);
		font-weight: 600;
		white-space: nowrap;
	">
		{label}
	</div>
	"""


FRAME_STYLE = (
	"min-height: 8.5rem; padding: 0.9rem; border: 1px dashed var(--vl-border); "
	"border-radius: 0.85rem; background: color-mix(in srgb, var(--vl-primary) 4%, var(--vl-bg-card) 96%);"
)


def render_min_height_frame(content) -> None:
	with app.container(style=FRAME_STYLE, fill_height=True):
		content()


def render_default_row(index: int, label: str, options: list[str]) -> None:
	left, right = app.columns([1, 2], gap="medium")
	with left:
		app.text(label, style="margin: 0; font-weight: 600;")
	with right:
		app.selectbox("Select value", options, key=f"issue25_default_{index}")


def render_column_justify_row(index: int, label: str, options: list[str]) -> None:
	left, right = app.columns([1, 2], gap="medium", justify="center")
	with left:
		app.text(label, style="margin: 0; font-weight: 600;")
	with right:
		app.selectbox(
			"Select value",
			options,
			key=f"issue25_column_justify_{index}",
			label_visibility="collapsed",
			help="The left text becomes the visible label while the select keeps an accessible name.",
		)


def render_container_justify_row(index: int, label: str, options: list[str]) -> None:
	left, right = app.columns([1, 2], gap="medium", equal_height=True)
	with left:
		with app.container(fill_height=True, justify="center"):
			app.text(label, style="margin: 0; font-weight: 600;")
	with right:
		app.selectbox(
			"Select value",
			options,
			key=f"issue25_container_justify_{index}",
			label_visibility="collapsed",
		)


def render_container_local_showcase(position: str, label: str, options: list[str]) -> None:
	with app.container(border=True, style="min-height: 10rem;"):
		left, right = app.columns([1, 2], gap="medium", equal_height=True)
		with left:
			def render_left():
				with app.container(fill_height=True, justify=position):
					app.html(label_pill(f"{position.title()} only"))

			render_min_height_frame(render_left)
		with right:
			def render_right():
				app.selectbox(
					label,
					options,
					key=f"issue25_container_local_{position}",
					label_visibility="collapsed",
					style="width: 14rem;",
				)

			render_min_height_frame(render_right)


def render_justify_showcase(position: str, label: str, options: list[str]) -> None:
	with app.container(border=True, style="min-height: 10rem;"):
		left, right = app.columns([1, 2], gap="medium", equal_height=True)
		with left:
			def render_left():
				with app.container(fill_height=True, justify=position):
					app.html(label_pill(f"{position.title()} text"))

			render_min_height_frame(render_left)
		with right:
			def render_right():
				with app.container(fill_height=True, justify=position):
					app.selectbox(
						label,
						options,
						key=f"issue25_justify_{position}",
						label_visibility="collapsed",
						style="width: 14rem;",
					)

			render_min_height_frame(render_right)


def render_align_showcase(alignment: str, label: str, options: list[str]) -> None:
	left, right = app.columns(
		[1, 2],
		gap="medium",
		border=True,
		equal_height=True,
		align=alignment,
		justify="center",
	)
	with left:
		app.html(label_pill(f"align={alignment}"))
	with right:
		app.selectbox(
			label,
			options,
			key=f"issue25_align_{alignment}",
			label_visibility="collapsed",
			style="width: 14rem;",
		)


def render_label_visibility_demo() -> None:
	app.selectbox(
		"Visible label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_visible",
		label_visibility="visible",
	)
	app.selectbox(
		"Hidden label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_hidden",
		label_visibility="hidden",
		help="The label text is invisible, but its space remains reserved.",
	)
	app.selectbox(
		"Collapsed label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_collapsed",
		label_visibility="collapsed",
		help="The label row is removed entirely.",
	)


def render_label_position_demo() -> None:
	app.selectbox(
		"Top label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_pos_top",
		label_position="top",
	)
	app.selectbox(
		"Left label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_pos_left",
		label_position="left",
	)
	app.selectbox(
		"Right label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_pos_right",
		label_position="right",
	)
	app.selectbox(
		"Bottom label",
		["Sales", "Marketing", "Operations"],
		key="issue25_label_pos_bottom",
		label_position="bottom",
	)


def render_cls_offset_panel(
	badge: str,
	key: str,
	options: list[str],
	*,
	cls: str = "",
	style: str = "width: 14rem;",
) -> None:
	app.html(label_pill(badge))
	with app.container(
		style=(
			"min-height: 9.5rem; margin-top: 0.75rem; padding: 1rem; "
			"border: 1px dashed var(--vl-border); border-radius: 0.85rem; overflow: visible;"
		)
	):
		app.selectbox(
			"Select value",
			options,
			key=key,
			label_visibility="collapsed",
			cls=cls,
			style=style,
		)


def render_cls_offset_showcase(
	index: int,
	title: str,
	options: list[str],
	*,
	tuned_cls: str,
	baseline_style: str = "width: 14rem;",
	tuned_style: str = "width: 14rem;",
) -> None:
	app.markdown(f"**{index}. {title}**")
	baseline, tuned = app.columns([1, 1], gap="medium", border=True, equal_height=True)
	with baseline:
		app.caption("Baseline")
		render_cls_offset_panel(
			"No cls",
			f"issue25_cls_baseline_{index}",
			options,
			style=baseline_style,
		)
	with tuned:
		app.caption(f"Tailwind tuned: cls=\"{tuned_cls}\"")
		render_cls_offset_panel(
			"cls applied",
			f"issue25_cls_tuned_{index}",
			options,
			cls=tuned_cls,
			style=tuned_style,
		)


def render_cls_offset_demo() -> None:
	render_cls_offset_showcase(
		1,
		'margin-top using cls="mt-6"',
		["Sales", "Marketing", "Operations"],
		tuned_cls="mt-6",
	)
	render_cls_offset_showcase(
		2,
		'translateY using cls="translate-y-[12px]"',
		["Sales", "Marketing", "Operations"],
		tuned_cls="translate-y-[12px]",
	)
	render_cls_offset_showcase(
		3,
		'relative offset using cls="relative top-[10px]"',
		["Sales", "Marketing", "Operations"],
		tuned_cls="relative top-[10px]",
	)
	render_cls_offset_showcase(
		4,
		'percent-based horizontal shift using cls="ml-[8%] w-[82%]"',
		["Sales", "Marketing", "Operations"],
		tuned_cls="ml-[8%] w-[82%]",
		baseline_style="width: 82%;",
		tuned_style="",
	)


app.header("Issue 25 - styling text and selectbox across columns")
app.write(
	"This page is tuned to make the alignment behavior visually obvious. "
	"It compares the default mismatch, selectbox label_position, label_visibility, columns justify, columns align, and a local container override."
)

app.subheader("1. Default rendering")
app.caption(
	"The left text stays at the top of its column, while the selectbox includes its own label row above the field. "
	"That is why the two sides do not feel aligned by default."
)
for row_index, (row_label, row_options) in enumerate(ROWS):
	render_default_row(row_index, row_label, row_options)

app.subheader("2. selectbox label_position without columns")
app.caption(
	"The selectbox can now place its own label on top, left, right, or bottom. "
	"That means simple form-like layouts no longer need columns at all."
)
render_label_position_demo()

app.subheader("3. selectbox label_visibility")
app.caption(
	"visible shows the label, hidden keeps the label area but makes it invisible, and collapsed removes the label row. "
	"Collapsed is the mode that helps most when the left column text acts as the row label."
)
render_label_visibility_demo()

app.subheader("4. cls-based fine tuning with Tailwind utilities")
app.caption(
	"Each row compares a baseline column against a Tailwind-tuned column with a dashed outline frame. "
	"That makes small vertical and horizontal shifts easier to see."
)
render_cls_offset_demo()

app.subheader("5. columns(..., justify=...) for both columns")
app.caption(
	"These rows use a min-height outer container and two dashed inner frames instead of a separate anchor column. "
	"The left text and right selectbox are both positioned by justify inside that shared vertical space."
)
render_justify_showcase("top", "Select value", ROWS[0][1])
render_justify_showcase("center", "Select value", ROWS[1][1])
render_justify_showcase("bottom", "Select value", ROWS[2][1])

app.subheader("6. columns(..., align=...) for horizontal placement")
app.caption(
	"align controls horizontal placement inside each column. The selectbox width is intentionally narrow here so start, center, and end stand out."
)
render_align_showcase("start", "Select value", ROWS[0][1])
render_align_showcase("center", "Select value", ROWS[1][1])
render_align_showcase("end", "Select value", ROWS[2][1])

app.subheader("7. container(justify=...) for one side only")
app.caption(
	"These rows also use a min-height outer container, but only the left dashed frame applies container(justify=...). "
	"The right selectbox stays fixed so the local override remains obvious without an anchor column."
)
render_container_local_showcase("top", "Select value", ROWS[0][1])
render_container_local_showcase("center", "Select value", ROWS[1][1])
render_container_local_showcase("bottom", "Select value", ROWS[2][1])


if __name__ == "__main__":
	port = 18525
	if "--port" in sys.argv:
		port_index = sys.argv.index("--port")
		if port_index + 1 < len(sys.argv):
			port = int(sys.argv[port_index + 1])
	app.run(port=port)
