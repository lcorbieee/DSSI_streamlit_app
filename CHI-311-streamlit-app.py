import streamlit as st
import pandas as pd

@st.cache_data
def load_entire_df():
    return pd.read_csv("data/request_counts_by_community_area_year_month.csv")

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
response_times = load_response_times()
forecasts = load_forecasts()

# home page formatting
title = st.title("Forecasting 311 Call Volume by Chicago Neighborhood\n")
title_mark = st.markdown("Powered by UChicago Data Science for Social Impact and the City of Chicago")

# tab formatting
tab_forecast, tab_geospastial, tab_snapshot, tab_breakdown = st.container(border=True).tabs(["Forecasting 🔮", "Geospatial Analysis 🗺️", "Snapshots 📸", "Dataset Breakdown 🧐"])

# tab_forecast formatting
with tab_forecast:
    st.subheader("Models were trained on monthly Chicago 311 calls from 2019-2025.")
# tab_geospastial formatting
with tab_geospastial:
    st.subheader("Below is an interactive map of Chicago's 77 community areas.  Hover and see how different neighborhoods use 311.")
# tab_snapshot formatting
with tab_snapshot:
    st.subheader("Enjoy some bite-sized analyses of our data.")
    st.dataframe(response_times, use_container_width=True)
# tab_breakdown formatting
with tab_breakdown:
    st.subheader("Learn more about our dataset and research methods.")
