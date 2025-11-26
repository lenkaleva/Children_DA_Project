import streamlit as st
import pandas as pd
import numpy as np


# Import stránky Lenka
#from pages.lenka import show_lenka_page
#show_lenka_page()


# loading data - to be used na jednotlivych pages
# oprava 2 Belgium na jednotny stat
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('data.csv')
   
df = st.session_state.df











