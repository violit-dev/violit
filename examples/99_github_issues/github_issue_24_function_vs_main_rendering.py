import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import violit as vl


app = vl.App(title="GitHub Issue 24 - Function vs Main Rendering")


data = app.session_state(
	[{"text": "text"}, {"text": "another text"}],
	key="issue24_data",
)


app.header("Issue 24 - render difference inside function vs main")
app.write("This page compares the same text + selectbox pattern in normal code and in an @app.reactivity function.")


app.subheader("1. Rendered directly in main")
app.caption("Expected: both rows should render here.")
main_left, main_right = app.columns(2)
for index, item in enumerate(data.value):
	with main_left:
		app.text(item["text"])
	with main_right:
		app.selectbox("value", ["test"], key=f"issue24_main_select_{index}")


app.subheader("2. Rendered inside @app.reactivity function")
app.caption("Expected: after the framework fix, both rows should also render here.")


@app.reactivity
def render_from_function():
	func_left, func_right = app.columns(2)
	for index, item in enumerate(data.value):
		with func_left:
			app.text(item["text"])
		with func_right:
			app.selectbox("value", ["test"], key=f"issue24_func_select_{index}")


render_from_function()


if __name__ == "__main__":
	port = 18524
	if "--port" in sys.argv:
		port_index = sys.argv.index("--port")
		if port_index + 1 < len(sys.argv):
			port = int(sys.argv[port_index + 1])
	app.run(port=port)