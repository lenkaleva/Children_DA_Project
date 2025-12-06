import streamlit as st

st.title("👥 Project Information & Credits")

# ---- CUSTOM CARD STYLE ----
st.markdown("""
<style>
.card {
    padding: 1.1rem 1.3rem;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.04);
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
}

.card:hover {
    box-shadow: 0px 4px 10px rgba(0,0,0,0.07);
}

.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
    color: #4b5563;
}

.links a {
    text-decoration: none;
    font-size: 0.95rem;
    margin-right: 14px;
}

.linkedin { color: #0A66C2; }
.github { color: #333333; }
</style>
""", unsafe_allow_html=True)


# ---- AUTHOR CARD ----
st.markdown("""
<div class="card">
    <div class="card-title">🟣 Aneta Kantorová</div>
    <div class="links">
        <a class="linkedin" href="https://www.linkedin.com/in/aneta-kantorova-0b8009148/" target="_blank">🔗 LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- AUTHOR CARD ----
st.markdown("""
<div class="card">
    <div class="card-title">🟣 Lenka Levá</div>
    <div class="links">
        <a class="linkedin" href="https://www.linkedin.com/in/lenkaleva/" target="_blank">🔗 LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- DATA SOURCE CARD ----
st.markdown("""
<div class="card">
    <div class="card-title">📚 Data Source</div>
    <div class="links">
        <a class="data" href="https://www.uib.no/en/hbscdata/113290/open-access" target="_blank">🌍 HBSC International Data Portal</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- GITHUB CARD ----
st.markdown("""
<div class="card">
    <div class="card-title">💻 Project Source Code</div>
    <div class="links">
        <a class="github" href="https://github.com/lenkaleva/Children_DA_Project" target="_blank">🐙 GitHub Repository</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- DISCLAIMER ----
st.markdown("""
<br><sub>*The HBSC dataset is used exclusively for educational and research purposes within this project. 
""", unsafe_allow_html=True)

