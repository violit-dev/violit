import sys

import pandas as pd
import violit as vl


app = vl.App(title="GitHub Issue 27 - DataFrame Functions")


search_query = app.session_state("", key="issue27_search_query")
page_size = app.session_state(20, key="issue27_page_size")


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
csv_data = df.to_csv(index=False)


def dataframe_grid_options():
    return {
        "pagination": True,
        "paginationPageSize": int(page_size.value),
        "paginationPageSizeSelector": [10, 20, 50, 100],
        "quickFilterText": str(search_query.value or ""),
        "animateRows": False,
    }


app.header("Issue 27 - DataFrame feature example")
app.write(
    "This example shows the current Violit approach: built-in AG Grid pagination via "
    "`grid_options`, plus app-level search and CSV export controls."
)

left, middle, right = app.columns([2.2, 1.1, 1.2], gap="medium")
with left:
    app.text_input(
        "Global search",
        bind=search_query,
        placeholder="Search any visible cell value...",
        help="This updates AG Grid quick filtering through grid_options.",
    )
with middle:
    app.selectbox(
        "Rows per page",
        [10, 20, 50, 100],
        bind=page_size,
        help="This uses AG Grid pagination instead of manually slicing the DataFrame.",
    )
with right:
    app.download_button(
        "Export CSV",
        data=csv_data,
        file_name="github_issue_27_dataframe.csv",
        mime="text/csv",
        type="secondary",
        use_container_width=True,
    )

app.caption(
    "Pagination is already available through AG Grid options. Streamlit-style built-in "
    "default toolbar actions such as one-line fullscreen/search/export are not yet exposed "
    "as an official single-API surface."
)

app.dataframe(
    df,
    hide_index=True,
    height=430,
    grid_options=dataframe_grid_options,
)


with app.expander("What this example demonstrates"):
    app.write("1. `grid_options={\"pagination\": True}` enables official grid pagination.")
    app.write("2. `quickFilterText` can be driven from a normal Violit text input.")
    app.write("3. CSV export can be added today with `app.download_button(...)`.")
    app.write("4. Fullscreen is not wrapped yet as a dedicated Violit dataframe convenience API.")


if __name__ == "__main__":
    port = 18527
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port")
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    app.run(port=port)