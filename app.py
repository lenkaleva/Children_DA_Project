import streamlit as st
import pandas as pd
import numpy as np

# Import stránky Lenka
from pages.lenka import show_lenka_page

# (Volitelně) import Anet stránky – až ji vytvoříš
# from pages.anet import show_anet_page

# loading data - to be used na jednotlivych pages
# oprava 2 Belgium na jednotny stat
if 'data' not in st.session_state:
    df = pd.read_csv('data.csv')
    df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace({
        "Belgium (Flemish)": "Belgium",
        "Belgium (French)": "Belgium"
    })
    st.session_state.data = df


country_list = st.session_state.data['COUNTRY_NAME'].unique().tolist()
years_list = st.session_state.data['YEAR'].unique().tolist()

# ------------------------------------------------------------
# SIDEBAR MENU
# ------------------------------------------------------------
with st.sidebar:
    st.sidebar.title("📚 Menu")
    filters = {}
    selected_country = st.selectbox('Select Country', options = ['All'] + country_list)
    selected_sex = st.multiselect('Select Gender', options = ['Girls', 'Boys'], default = ['Girls', 'Boys'] )
    selected_years = st.multiselect('Select years', options = years_list, default = years_list)


    filters = {
        'COUNTRY_NAME': None if selected_country == 'All' else [selected_country, 'Czech Republic'],
        'YEAR': None if selected_years == years_list else selected_years,
        'SEX': None if selected_sex == ['Girls', 'Boys'] else selected_sex,
}
    

filtered = st.session_state.data.copy()
for col, val in filters.items():
    if val is None:
        continue
    if isinstance(val, (list, tuple, set)):
        filtered = filtered[filtered[col].isin(val)]
    else:
        filtered = filtered[filtered[col] == val]

st.dataframe(filtered[0:100])







