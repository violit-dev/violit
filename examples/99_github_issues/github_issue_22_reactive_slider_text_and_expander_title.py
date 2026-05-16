import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import violit as vl


app = vl.App(title="GitHub Issue 22 - Reactive Slider Text and Expander Title")


fetch_count = app.session_state(50, "issue22_fetch_count")


def fetch_count_changed(value):
	fetch_count.set(value)


def main_page():
	app.header("Issue 22 - reactive slider text and expander title")
	app.write("This page contrasts static text with reactive text and expander titles.")

	app.subheader("1. Static snapshot")
	app.text("This line is evaluated immediately, so it does not live-update:")
	app.text(f"Static snapshot: {fetch_count}")

	app.subheader("2. Reactive text")
	app.text("These lines re-evaluate when the slider changes:")
	app.text(fetch_count)
	app.text(lambda: f"Reactive lambda text: {fetch_count.value}")

	app.slider(
		"Fetch top emails",
		10,
		100,
		fetch_count.value,
		10,
		key="issue22_slider_value",
		live_update=True,
		on_change=fetch_count_changed,
	)

	app.subheader("3. Expander title")
	app.text("The first expander uses a static title snapshot. The second uses a reactive label.")

	with app.expander(f"Static expander title: {fetch_count}", expanded=True):
		app.text("This title will stay frozen until a full rerender happens.")
		app.text(lambda: f"Inner reactive text still updates: {fetch_count.value}")

	with app.expander(lambda: f"Reactive expander title: {fetch_count.value}", expanded=True):
		app.text("After the framework fix, this title updates while dragging the slider.")
		app.text(lambda: f"Current fetch_count: {fetch_count.value}")


app.navigation([main_page])


if __name__ == "__main__":
	app.run()
