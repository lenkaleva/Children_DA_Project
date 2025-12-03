import streamlit as st
import pandas as pd




st.markdown("""
<style>
/* zmenší horní padding, aby title neseděl moc nízko */
.block-container {
    padding-top: 1.5rem !important;
}

/* jemně teplejší sidebar (volitelné, můžeš změnit nebo smazat) */
[data-testid="stSidebar"] {
    background-color: #f5f7fb;
}
</style>
""", unsafe_allow_html=True)



if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('data.csv')

df = st.session_state.df




st.title("Childhood Overweight: Country, Behaviour & Lifestyle Factors")
st.subheader("Data Analysis Based on the International HBSC Study (2002–2018)")

st.image("pic.png", use_container_width=True) 


st.markdown("### 🧭 Project Overview")
st.markdown(
    "This app explores how lifestyle, health issues, and behaviour relate to childhood overweight. "
    "Using large-scale data from more than 40 countries, it helps you see patterns, compare groups, "
    "and understand which everyday habits matter most."
)

st.markdown("### 🔎 What You Can Explore")
st.markdown("""
- **Countries:** cross-country trends and how Czechia compares to EU and global averages  
- **Gender:** differences between boys and girls across time and age  
- **Barometer:** an interactive tool that shows how a child’s habits relate to overweight risk  
""")

st.markdown("### 🗃️ Data Sources")
st.markdown("""
The analysis is based on the **HBSC (Health Behaviour in School-aged Children)** study – 
an international survey of students in grades 5, 7, and 9.  
We use five survey runs: **2002, 2006, 2010, 2014, and 2018**, each with roughly **250,000 pupils**
from more than **40 countries**.
""")

st.markdown("### 🤝 Acknowledgements")
st.markdown("""
This project was created as part of our final coursework in the Czechitas Digital Academy: Data.  
We gratefully acknowledge the use of HBSC data, provided for educational and research purposes.
""")
