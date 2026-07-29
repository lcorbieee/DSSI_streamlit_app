import streamlit as st
import pandas as pd

# home page formatting
title = st.title("Forecasting 311 Call Volume by Chicago Neighborhood\n")
title_mark = st.markdown("Powered by UChicago Data Science for Social Impact and the City of Chicago")

# sidebar formatting
tab_forecast, tab_geospastial, tab_snapshot, tab_breakdown = st.container(border=True).tabs(["Forecasting 🔮", "Geospatial Analysis 🗺️", "Snapshots 📸", "Dataset Breakdown 🧐"])

