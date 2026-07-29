import streamlit as st
import pandas as pd

# home page formatting
title = st.title("CHI 311 Data Snapshot: 2019-2025\n")
title_mark = st.markdown("Powered by the City of Chicago and UChicago DSSI")

# sidebar formatting
tab1, tab2, tab3, tab4 = st.tabs(["Data Snapshots", "Dataset Breakdown", "Geospatial Analysis", "Forecasting"])
