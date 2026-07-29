import streamlit as st
import pandas as pd

# home page formatting
title = st.title("Forecasting 311 Call Volume by Chicago Neighborhood\n")
title_mark = st.markdown("Powered by UChicago Data Science for Social Impact and the City of Chicago")

# sidebar formatting
tab1, tab2, tab3, tab4 = st.tabs(["Forecasting", "Geospatial Analysis", "Snapshots", "Dataset Breakdown"])
st.container(border=True)
