import streamlit as st
import pandas as pd

# home page formatting
title = st.title("Forecasting 311 Call Volume by Chicago Neighborhood\n")
title_mark = st.markdown("Powered by UChicago Data Science for Social Impact and the City of Chicago")

# tab formatting
tab_forecast, tab_geospastial, tab_snapshot, tab_breakdown = st.container(border=True).tabs(["Forecasting 🔮", "Geospatial Analysis 🗺️", "Snapshots 📸", "Dataset Breakdown 🧐"])

# tab_forecast formatting
# with tab_forecast:
#     st.
# # tab_geospastial formatting
# with tab_geospastial:

# # tab_snapshot formatting
# with tab_snapshot:

# # tab_breakdown formatting
# with tab_breakdown: