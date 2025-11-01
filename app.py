import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st

# Nastavení menu v postranním panelu
st.sidebar.title("📚 Menu")
page = st.sidebar.selectbox("Vyber stránku:", ["🏠 Domů", "📊 Analýza nadváhy", "😊 Spokojenost", "📊 Graf kluci vs holky"])

# Logika přepínání obsahu
if page == "🏠 Domů":
    st.title("Vítej v naší aplikaci 👋")
    st.write("Tady můžeš zkoumat data o dětech, obezitě a spokojenosti.")

elif page == "📊 Analýza nadváhy":
    st.title("📊 Analýza nadváhy")
    st.write("Tady můžeme dát graf porovnání děti v ČR a ve světě.")
    # Můžeš volat svou funkci, např. show_obesity_analysis()

elif page == "😊 Spokojenost":
    st.title("😊 Spokojenost dětí")
    st.write("Sem přijde analýza spokojenosti s životem (LIFESAT).")

elif page == "📊 Graf kluci vs holky":
    st.title("📊 Graf kluci vs holky")
    st.write("Tady můžeme dát graf porovnání kluků vs holek.")
