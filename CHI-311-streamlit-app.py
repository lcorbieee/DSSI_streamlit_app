import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="CHI 311 PLACEHOLDER TITLE", 
    page_icon="https://pbs.twimg.com/profile_images/1229828517526851584/4yqr6QTK_400x400.png", 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
    'About': 'This dashboard was created by four students in the UChicago Data Science for Social Impact Summer Program.'
    }
    )

@st.cache_data
def load_entire_df():
    return pd.read_csv("data/request_counts_by_community_area_year_month.csv")

@st.cache_data
def load_geojson():
    with open("data/community_area_boundaries.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

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

# home page formatting
title = st.title("CHI 311 PLACEHOLDER TITLE\n")
title_mark = st.markdown("Powered by UChicago Data Science for Social Impact and the City of Chicago")

# tab formatting
tab_forecast, tab_geospastial, tab_snapshot, tab_breakdown = st.container(border=True).tabs(
    ["Forecasting 🔮", "Geospatial Analysis 🗺️", "Snapshots 📸", "Dataset Breakdown 🧐"]
)
# sidebar formatting
st.sidebar.write("Navigate CHI 311")

# tab_forecast formatting
with tab_forecast:
    st.subheader("Forecasting 311 Call Volume by Chicago Neighborhood.  Models were trained on monthly Chicago 311 requests from 2019-2025.")
# tab_geospastial formatting
with tab_geospastial:
    st.subheader("Below is an interactive map of Chicago's 77 community areas.  Hover and see how different neighborhoods are using 311!")
    # --- Aggregate to one row per community area -------------------------------
    # Drop COMMUNITY_AREA == 0 (that's your citywide total row, not a real area)
    # and sum however many months/columns you want represented on the map.
    areas_only = total_requests[total_requests["COMMUNITY_AREA"] != 0]

    request_type_cols = [c for c in total_requests.columns if c not in ("YEAR_MONTH", "COMMUNITY_AREA")]
    by_area = areas_only.groupby("COMMUNITY_AREA")[request_type_cols].sum().sum(axis=1).reset_index()
    by_area.columns = ["COMMUNITY_AREA", "value"]

    # --- Build the choropleth ----------------------------------------------------
    fig_map = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=by_area["COMMUNITY_AREA"],       # values to match against featureidkey
            featureidkey="properties.area_numbe",       # the property in your geojson holding the area number
            z=by_area["value"],                          # the color-scale variable
            zmin=by_area["value"].min(),
            zmax=by_area["value"].quantile(0.90),        # 90th percentile, not max — keeps one huge outlier area
                                                        # from washing out color contrast on every other area
            colorscale="Purples",
            marker_line_color="white",
            marker_line_width=0.5,
            colorbar_title="Requests",
        )
    )

    fig_map.update_geos(fitbounds="locations", visible=False)  # zooms to just your boundaries, hides base map
    fig_map.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=0))

    # --- Render it, with click-to-select enabled ---------------------------------
    map_event = st.plotly_chart(
        fig_map,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
        key="choropleth_map",
    )

    if map_event.selection.points:
        clicked_area = map_event.selection.points[0].get("location")
        st.success(f"Selected community area: {clicked_area}")
        st.session_state["selected_area"] = clicked_area
# tab_snapshot formatting
with tab_snapshot:
    st.subheader("Enjoy some bite-sized analyses of our data.")
    st.dataframe(response_times, use_container_width=True)
# tab_breakdown formatting
with tab_breakdown:
    st.subheader("Learn more about our dataset and research methods.")
    st.dataframe(total_requests, use_container_width=True)
