import streamlit as st
import pandas as pd

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
# tab_breakdown formatting
with tab_breakdown:
    st.subheader("Learn more about our dataset and research methods.")
