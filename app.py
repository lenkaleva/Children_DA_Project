import streamlit as st
import pandas as pd
import numpy as np

# Import stránky Lenka
from pages.lenka import show_lenka_page

# (Volitelně) import Anet stránky – až ji vytvoříš
# from pages.anet import show_anet_page


if 'data' not in st.session_state:
    st.session_state.data = pd.read_csv('data.csv')


# ------------------------------------------------------------
# SIDEBAR MENU
# ------------------------------------------------------------
st.sidebar.title("📚 Menu")

page = st.sidebar.selectbox(
    "Vyber stránku:",
    [
        "🏠 Domů",
        "📊 Analýza nadváhy",
        "📊 Anet – Grafy",
        "📈 Lenka – Obezita v Evropě"
    ]
)

# ------------------------------------------------------------
# STRÁNKY
# ------------------------------------------------------------

if page == "🏠 Domů":
    st.title("Vítej v naší aplikaci 👋")
    st.write("Tady můžeš zkoumat data o dětech, obezitě a dalších faktorech.")

elif page == "📊 Analýza nadváhy":
    st.title("📊 Analýza nadváhy")
    st.write("Sem můžeš vložit graf porovnání dětí v ČR a v EU.")

elif page == "📊 Anet – Grafy":
    st.title("📊 Anet – Grafy")
    st.write("Sem přijdou Anetiny grafy. Pokud chceš, udělám ti hotovou Anet stránku.")

elif page == "📈 Lenka – Obezita v Evropě":
    show_lenka_page()
