import streamlit as st
import pandas as pd

# home page formatting
st.title("CHI 311 Data Snapshot: 2019-2025\n")
st.markdown("Powered by UChicago DSSI")
# sidebar formatting
st.sidebar.write("Select how you want to interpret our data:")
st.sidebar.button("Home")
st.sidebar.button("Dataset Breakdown")
st.sidebar.button("Geospatial analysis")
st.sidebar.button("Forecasting call volume by Chicago neighborhood")
