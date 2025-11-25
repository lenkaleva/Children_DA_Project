import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ------------------------------------------------------------
# KONSTANTY: škály a faktory
# ------------------------------------------------------------
factors = [
    "FRUITS", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
    "TIME_EXE", "PHYS_ACT_60", "DRUNK_30",
    "FAMILY_MEALS_TOGETHER", "BREAKFAST_WEEKDAYS", "BREAKFAST_WEEKEND",
    "TOOTH_BRUSHING", "STUD_TOGETHER", "BUL_OTHERS", "BUL_BEEN",
    "FIGHT_YEAR", "INJURED_YEAR", "HEADACHE", "FEEL_LOW",
    "NERVOUS", "SLEEP_DIF", "DIZZY",
    "TALK_MOTHER", "TALK_FATHER",
    "LIKE_SCHOOL", "SCHOOL_PRESSURE", "COMPUTER_NO"
]

dictionary = {
    "HEADACHE": 5, "NERVOUS": 5, "SLEEP_DIF": 5, "FEEL_LOW": 5,
    "DIZZY": 5, "TALK_FATHER": 5, "TALK_MOTHER": 5,
    "FAMILY_MEALS_TOGETHER": 6, "TIME_EXE": 7,
    "TOOTH_BRUSHING": 5, "LIKE_SCHOOL": 4, "STUD_TOGETHER": 5,
    "FRUITS": 7, "SOFT_DRINKS": 7, "SWEETS": 7, "VEGETABLES": 7,
    "FRIEND_TALK": 7, "PHYS_ACT_60": 7, "DRUNK_30": 7,
    "BREAKFAST_WEEKDAYS": 6, "BREAKFAST_WEEKEND": 3,
    "BUL_OTHERS": 5, "BUL_BEEN": 5,
    "FIGHT_YEAR": 5, "INJURED_YEAR": 5,
    "SCHOOL_PRESSURE": 4, "COMPUTER_NO": 4
}

reverse_scales = {
    "HEADACHE", "NERVOUS", "SLEEP_DIF", "DIZZY", "FEEL_LOW",
    "BREAKFAST_WEEKDAYS", "BREAKFAST_WEEKEND",
    "FRIEND_TALK", "FRUITS", "PHYS_ACT_60", "VEGETABLES"
}

# sjednocené barvy
DEFAULT_COLOR_CZ = "#1f77b4"
DEFAULT_COLOR_OTHER = "#ff7f0e"

eu_list = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Malta",
    "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden", "United Kingdom"
]


# ------------------------------------------------------------
# FUNKCE STRÁNKY
# ------------------------------------------------------------
def show_lenka_page():

    st.set_page_config(page_title="Analýza dětské obezity", layout="wide")

    # Globální styl – světle šedé pozadí + karty
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #f3f3f3;
        }
        .kpi-card {
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #dddddd;
            padding: 14px 16px;
            text-align: center;
        }
        .kpi-title {
            font-size: 0.9rem;
            font-weight: 700;
            color: #555555;
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 900;
            color: #222222;
        }
        .kpi-sub {
            font-size: 0.75rem;
            color: #777777;
        }
        .card {
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #dddddd;
            padding: 16px 18px;
            margin-bottom: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Analýza dětské obezity podle zemí")


    # ------------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------------
    if "df" not in st.session_state:
        df = pd.read_csv("data.csv")

        # Sjednocení Belgie
        df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace({
            "Belgium (Flemish)": "Belgium",
            "Belgium (French)": "Belgium"
        })

        # Sjednocení UK regionů na "United Kingdom"
        uk_map = {
            "England": "United Kingdom",
            "Scotland": "United Kingdom",
            "Wales": "United Kingdom",
            "Northern Ireland": "United Kingdom",
            "Great Britain": "United Kingdom",
            "UK (England)": "United Kingdom",
            "UK (Wales)": "United Kingdom",
            "UK (Scotland)": "United Kingdom"
        }
        df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace(uk_map)

        st.session_state.df = df
    else:
        df = st.session_state.df

    df.loc[df["BUL_BEEN"] == 999, "BUL_BEEN"] = np.nan

    # ============================================================
    # KPI – nahoře, v bílých čtverečcích, vždy z roku 2018
    # ============================================================
    
    df_2018 = df[df["YEAR"] == 2018].copy()

    cz_over = df_2018[df_2018["COUNTRY_NAME"] == "Czech Republic"]["OVERWEIGHT"].mean()
    eu_over = df_2018[df_2018["COUNTRY_NAME"].isin(eu_list)]["OVERWEIGHT"].mean()
    global_over = df_2018["OVERWEIGHT"].mean()
    n_countries_total = df_2018["COUNTRY_NAME"].nunique()

    # Top rizikový faktor za 2018 (globálně)
    df_norm_kpi = df_2018.copy()
    for f in factors:
        maxv = dictionary[f]
        df_norm_kpi[f] = (maxv + 1 - df_norm_kpi[f]) / maxv if f in reverse_scales else df_norm_kpi[f] / maxv

    corr_kpi = (
        df_norm_kpi[factors + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
        .abs()
        .sort_values(ascending=False)
    )

    if not corr_kpi.empty:
        top_factor_code = corr_kpi.index[0]
        top_factor_pretty = top_factor_code.replace("_", " ").title()
    else:
        top_factor_pretty = "—"

    colK1, colK2, colK3, colK4, colK5 = st.columns(5)

    with colK1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🇨🇿 Obezita v ČR</div>
                <div class="kpi-value"><b>{cz_over:.2f}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colK2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🇪🇺 EU průměr</div>
                <div class="kpi-value"><b>{eu_over:.2f}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colK3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🌍 Globální průměr</div>
                <div class="kpi-value"><b>{global_over:.2f}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colK4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">📊 Počet zemí v datasetu</div>
                <div class="kpi-value"><b>{n_countries_total}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with colK5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🔥 Top rizikový faktor</div>
                <div class="kpi-value"><b>{top_factor_pretty}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ============================================================
    # PRVNÍ GRAF + FILTRY VEDLE SEBE (bez filtru věku)
    # ============================================================
    st.subheader("📈 Vývoj prevalence obezity v čase")

    col_graph1, col_filters = st.columns([3, 1])

    default_country = "Czech Republic"
    all_countries = sorted(df["COUNTRY_NAME"].unique())
    options = ["All countries"] + all_countries

    with col_filters:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Filtry**")
        selected_country = st.selectbox("Vyber druhou zemi:", options, index=1)

        sex_choice = st.radio(
            "Pohlaví:",
            ["Vše", "Jen dívky", "Jen chlapce"],
            horizontal=False
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Aplikace filtru pohlaví (už ne filtr věku)
    df_current = df.copy()

    if sex_choice == "Jen dívky":
        df_current = df_current[df_current["SEX"] == 2]
    elif sex_choice == "Jen chlapce":
        df_current = df_current[df_current["SEX"] == 1]

    # Pro grafy pořád pracujeme hlavně s rokem 2018, ale vývoj bere všechny roky
    df_current_2018 = df_current[df_current["YEAR"] == 2018].copy()

    # DEFINICE POROVNÁVANÝCH ZEMÍ
    if selected_country == "All countries":
        compare_countries = all_countries
    else:
        compare_countries = [default_country, selected_country]

    # BARVY PRO GRAFY
    color_map = {
        "Czech Republic": DEFAULT_COLOR_CZ,
        selected_country: DEFAULT_COLOR_OTHER
    }

    with col_graph1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        df_line = (
            df_current[df_current["COUNTRY_NAME"].isin(compare_countries)]
            .groupby(["YEAR", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
            .mean()
        )

        fig_line = px.line(
            df_line, x="YEAR", y="OVERWEIGHT", color="COUNTRY_NAME",
            markers=True, color_discrete_map=color_map,
            title="Vývoj prevalence obezity"
        )
        fig_line.update_layout(height=450)

        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    # GRAF 2 + 3 — TOP 5 + podle věku
    # ============================================================
    st.subheader("📊 TOP 5 faktorů a overweight podle věku (2018)")

    # GRAF 2 — TOP 5
    df_norm = df_current_2018.copy()
    for f in factors:
        maxv = dictionary[f]
        df_norm[f] = (maxv + 1 - df_norm[f]) / maxv if f in reverse_scales else df_norm[f] / maxv

    corr_vals = (
        df_norm[factors + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
        .abs()
        .sort_values(ascending=False)
    )

    top5 = corr_vals.head(5).index.tolist()

    df_t5 = (
        df_norm[df_norm["COUNTRY_NAME"].isin(compare_countries)]
        .groupby("COUNTRY_NAME")[top5]
        .mean()
        .reset_index()
    )

    df_t5_long = df_t5.melt(
        id_vars="COUNTRY_NAME",
        value_vars=top5,
        var_name="FEATURE",
        value_name="VALUE"
    )

    fig_top5 = px.bar(
        df_t5_long,
        x="FEATURE",
        y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_map=color_map,
        title="TOP 5 faktorů souvisejících s obezitou (normalizováno)"
    )
    fig_top5.update_layout(height=450)

    # GRAF 3 — Overweight podle věku
    df_age_plot = (
        df_current[df_current["COUNTRY_NAME"].isin(compare_countries)]
        .groupby(["AGE", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
        .mean()
    )

    fig_age = px.line(
        df_age_plot,
        x="AGE",
        y="OVERWEIGHT",
        color="COUNTRY_NAME",
        markers=True,
        color_discrete_map=color_map,
        title="Overweight podle věku"
    )
    fig_age.update_layout(height=450)

    col_g2, col_g3 = st.columns(2)
    with col_g2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig_top5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    # GRAF 4 — TOP X faktorů (bez TOP 5)
    # ============================================================
    st.subheader("📊 TOP X dalších faktorů (bez TOP 5)")

    top_n = st.slider("Počet faktorů:", 5, 20, 15)

    remaining = corr_vals.index.tolist()[5:]
    topX = remaining[:top_n]

    df_tX = (
        df_norm[df_norm["COUNTRY_NAME"].isin(compare_countries)]
        .groupby("COUNTRY_NAME")[topX]
        .mean()
        .reset_index()
    )

    df_tX_long = df_tX.melt(
        id_vars="COUNTRY_NAME",
        value_vars=topX,
        var_name="FEATURE",
        value_name="VALUE"
    )

    fig_topX = px.bar(
        df_tX_long,
        x="FEATURE",
        y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_map=color_map,
        title=f"TOP {top_n} dalších faktorů (normalizováno)"
    )
    fig_topX.update_layout(height=600, xaxis_tickangle=45)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_topX, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    # SPODNÍ GRAFY – IGNORUJÍ FILTR VĚKU (jako dřív)
    # ============================================================
    st.subheader("📉 EU porovnání (bez věkového filtru)")

    # GRAF 5 — EU deviation
    df_eu_2018 = df[df["YEAR"] == 2018].copy()

    if sex_choice == "Jen dívky":
        df_eu_2018 = df_eu_2018[df_eu_2018["SEX"] == 2]
    elif sex_choice == "Jen chlapce":
        df_eu_2018 = df_eu_2018[df_eu_2018["SEX"] == 1]

    df_eu_only = df_eu_2018[df_eu_2018["COUNTRY_NAME"].isin(eu_list)]
    eu_avg = df_eu_only["OVERWEIGHT"].mean()

    df_dev = (
        df_eu_only.groupby("COUNTRY_NAME", as_index=False)["OVERWEIGHT"]
        .mean()
    )
    df_dev["DEVIATION"] = df_dev["OVERWEIGHT"] - eu_avg
    df_dev = df_dev.sort_values("DEVIATION")

    fig_dev = px.bar(
        df_dev,
        x="DEVIATION",
        y="COUNTRY_NAME",
        orientation="h",
        color="DEVIATION",
        color_continuous_scale="RdBu_r",
        title="Odchylka od EU průměru (2018)"
    )
    fig_dev.add_vline(x=0)
    fig_dev.update_layout(height=750)

    # GRAF 6 — Boys vs Girls
    df_gender = df[df["YEAR"] == 2018].copy()
    df_gender = df_gender[df_gender["COUNTRY_NAME"].isin(eu_list)]
    df_gender["SEX_LABEL"] = df_gender["SEX"].map({1: "Boys", 2: "Girls"})

    df_gender_pivot = (
        df_gender.groupby(["COUNTRY_NAME", "SEX_LABEL"], as_index=False)["OVERWEIGHT"]
        .mean()
        .pivot(index="COUNTRY_NAME", columns="SEX_LABEL", values="OVERWEIGHT")
        .dropna()
        .reset_index()
    )

    df_gender_pivot["DIFF"] = df_gender_pivot["Girls"] - df_gender_pivot["Boys"]
    df_gender_pivot = df_gender_pivot.sort_values("DIFF")

    fig_dumbbell = go.Figure()

    fig_dumbbell.add_trace(go.Scatter(
        x=df_gender_pivot["Girls"], y=df_gender_pivot["COUNTRY_NAME"],
        mode="markers", name="Girls", marker=dict(color="hotpink", size=12)
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=df_gender_pivot["Boys"], y=df_gender_pivot["COUNTRY_NAME"],
        mode="markers", name="Boys", marker=dict(color="cornflowerblue", size=12)
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=pd.concat([df_gender_pivot["Girls"], df_gender_pivot["Boys"]]),
        y=pd.concat([df_gender_pivot["COUNTRY_NAME"], df_gender_pivot["COUNTRY_NAME"]]),
        mode="lines", showlegend=False, line=dict(color="gray", width=1.7)
    ))

    fig_dumbbell.update_layout(height=750, title="Boys vs Girls")

    col4, col5 = st.columns(2)
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig_dev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig_dumbbell, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
show_lenka_page()
