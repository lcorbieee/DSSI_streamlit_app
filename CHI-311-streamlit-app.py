import streamlit as st
import pandas as pd

# home page formatting
title = st.title("Forecasting CHI 311 Call Volume by Neighborhood\n")
title_mark = st.markdown("Powered by the City of Chicago and UChicago DSSI")

# sidebar formatting
tab1, tab2, tab3, tab4 = st.tabs(["Snapshots", "Geospatial Analysis", "Forecasting", "Dataset Breakdown"])
