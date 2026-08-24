import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="CHI 311 Dashboard",
    page_icon="https://pbs.twimg.com/profile_images/1229828517526851584/4yqr6QTK_400x400.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "This dashboard was created by four students in the UChicago Data Science for Social Impact Summer Program."
    },
)

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

st.markdown(
    """
    <style>
    [data-testid="stSidebarNavItems"] {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Data loading (shared across every page, runs once per rerun) ----------
@st.cache_data
def load_entire_df():
    return pd.read_csv("data/request_counts_by_community_area_year_month.csv")

@st.cache_data
def load_geojson():
    with open("data/community_area_boundaries.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_population():
    pop = pd.read_csv("data/ACS_5_Year_Data_by_Community_Area_20260720.csv", thousands=",")
    pop = pop[["Community Area", "Total Population"]].copy()
    pop["Community Area"] = pop["Community Area"].str.strip().str.upper()
    return pop

@st.cache_data
def load_categories():
    return pd.read_csv("data/request_type_categories.csv")

@st.cache_data
def load_response_times():
    return pd.read_csv("data/median_response_time.csv")

@st.cache_data
def load_forecasts():
    return pd.read_csv("data/citywide_forecast_results.csv", parse_dates=["date"])

total_requests = load_entire_df()
categories = load_categories()
geojson = load_geojson()
response_times = load_response_times()
forecasts = load_forecasts()
population = load_population()


# --- Page functions (one per former "tab") ----------------------------------
def forecast_page():
    st.subheader(
        "Forecasting 311 Call Volume by Chicago Neighborhood. "
        "Models were trained on monthly Chicago 311 requests from 2019-2025."
    )

area_id_to_name = {
    int(feat["properties"]["area_numbe"]): feat["properties"]["community"].title()
    for feat in geojson["features"]
}

def geospatial_page():
    st.subheader("Below is an interactive map of Chicago's 77 community areas. Hover to see each neighborhoods' volume of 311 requests.")

    areas_only = total_requests[total_requests["COMMUNITY_AREA"] != 0]
    request_type_cols = [c for c in total_requests.columns if c not in ("YEAR_MONTH", "COMMUNITY_AREA")]
    by_area = areas_only.groupby("COMMUNITY_AREA")[request_type_cols].sum().sum(axis=1).reset_index()
    by_area.columns = ["COMMUNITY_AREA", "value"]

    name_to_area = {
        feat["properties"]["community"].strip().upper(): int(feat["properties"]["area_numbe"])
        for feat in geojson["features"]
    }
    population_by_area = population.copy()
    population_by_area["COMMUNITY_AREA"] = population_by_area["Community Area"].map(name_to_area)

    by_area = by_area.merge(
        population_by_area[["COMMUNITY_AREA", "Total Population"]],
        on="COMMUNITY_AREA",
        how="left",
    )
    by_area["value_per_capita"] = (by_area["value"] / by_area["Total Population"]) * 1000
    by_area["area_name"] = by_area["COMMUNITY_AREA"].map(area_id_to_name)  # <-- new

    metric_mode = st.segmented_control(
        "Metric", options=["Raw count", "Per 1,000 residents"], default="Raw count"
    )
    if metric_mode == "Raw count":
        z_col, colorbar_title = "value", "Requests"
        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Total requests: %{customdata[1]:,.0f}<br>"
            "Population: %{customdata[2]:,.0f}"
            "<extra></extra>"
        )
    else:
        z_col, colorbar_title = "value_per_capita", "Requests per<br>1,000 residents"
        hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            "Total requests: %{customdata[1]:,.0f}<br>"
            "Population: %{customdata[2]:,.0f}<br>"
            "Requests per 1,000 residents: %{z:,.1f}"
            "<extra></extra>"
        )

    fig_map = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=by_area["COMMUNITY_AREA"],
            featureidkey="properties.area_numbe",
            z=by_area[z_col],
            zmin=by_area[z_col].min(),
            zmax=by_area[z_col].quantile(0.90),
            colorscale="Reds",
            marker_line_color="white",
            marker_line_width=0.5,
            colorbar_title=colorbar_title,
            customdata=by_area[["area_name", "value", "Total Population"]],  # name moved to front
            hovertemplate=hovertemplate,
        )
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=0))

    map_event = st.plotly_chart(
        fig_map, use_container_width=True, on_select="rerun", selection_mode="points", key="choropleth_map",
    )

    if map_event.selection.points:
        clicked_area = map_event.selection.points[0].get("location")
        clicked_name = area_id_to_name.get(int(clicked_area), f"Area {clicked_area}")
        st.success(f"Selected: {clicked_name}")
        st.session_state["selected_area"] = clicked_area  # keep storing the number internally


def snapshot_page():
    st.subheader("Enjoy some fast facts derived from our data!")
    st.dataframe(response_times, use_container_width=True)


def breakdown_page():
    st.subheader("Learn more about our dataset and research methods:")

    st.write(
        "Our primary dataset is monthly panel of 311 request counts derived from the City's public data. "
        "Each row is a place-and-month — a community area in a given month (plus "
        "citywide total rows) — with one column per request type giving how many of "
        "that type were created there that month. It covers 2019–2025 for 55 of the "
        "most common request types across Chicago's 77 community areas (stable, "
        "official neighborhood units)."
    )

    st.dataframe(total_requests, use_container_width=True)

    st.download_button(
        label="Download full dataset (.CSV)",
        data=convert_df_to_csv(total_requests),
        file_name="total_requests.csv",
        mime="text/csv",
    )
    


def home_page():
    st.title("CHI 311 Interactive Dashboard")
    st.subheader("Powered by UChicago Data Science for Social Impact and the City of Chicago")
    st.write(
        "Explore Chicago 311 service requests: seasonal predictions, geospatial breakdowns by neighborhood, and forecasts."
    )


# --- Navigation: this is what puts the pages in the sidebar -----------------
pages = [
    st.Page(home_page, title="Home", icon="🏠", default=True),
    st.Page(forecast_page, title="Forecasting", icon="🔮"),
    st.Page(geospatial_page, title="Geospatial Analysis", icon="🗺️"),
    st.Page(snapshot_page, title="Snapshots", icon="📸"),
    st.Page(breakdown_page, title="Dataset Breakdown", icon="🧐"),
]


pg = st.navigation(pages)  # position="sidebar" is default
pg.run()


