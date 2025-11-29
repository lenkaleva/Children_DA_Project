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

factor_alias = {
    "FRUITS": "No fruit",
    "SOFT_DRINKS": "Soft drinks",
    "SWEETS": "Sweets",
    "VEGETABLES": "No vegetables",
    "FRIEND_TALK": "No friends talk",
    "TIME_EXE": "No exercise",
    "PHYS_ACT_60": "Below 60 min/day",
    "DRUNK_30": "Alcohol",
    "FAMILY_MEALS_TOGETHER": "No family meals",
    "BREAKFAST_WEEKDAYS": "No breakfast (weekdays)",
    "BREAKFAST_WEEKEND": "No breakfast (weekend)",
    "TOOTH_BRUSHING": "Poor teeth care",
    "STUD_TOGETHER": "No friend time",
    "BUL_OTHERS": "Bullies others",
    "BUL_BEEN": "Been bullied",
    "FIGHT_YEAR": "Often fights",
    "INJURED_YEAR": "Often injured",
    "HEADACHE": "Frequent headaches",
    "FEEL_LOW": "Feels low",
    "NERVOUS": "Feels nervous",
    "SLEEP_DIF": "Sleep problems",
    "DIZZY": "Feels dizzy",
    "TALK_MOTHER": "No mom talk",
    "TALK_FATHER": "No dad talk",
    "LIKE_SCHOOL": "Dislikes school",
    "SCHOOL_PRESSURE": "High school pressure",
    "COMPUTER_NO": "Computer/Gaming use"
}


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

   # ⭐ FUNKCE NA ZVĚTŠENÍ TITULKU GRAFŮ
    def title24(fig):
        fig.update_layout(title_font=dict(size=24))
        return fig

    st.markdown("""
    <style>

    .stApp { background-color: #f6f8fb; }
    .kpi-wrapper { margin-bottom: 40px; }

    .kpi-box {
        background: #ffffff;
        padding:16px;
        border-radius:16px;
        border:1px solid #d8e2f5;
        box-shadow:0 2px 6px rgba(0,0,0,0.12);
        text-align:center;

        /* HOVER musí být zde – funguje jen když parent NENÍ overflow:hidden */
        transition: box-shadow 0.18s ease;
    }

    .kpi-box:hover {
        box-shadow: 0 6px 18px rgba(15,23,42,0.18);
    }

    /* 🎯 Nový bezpečný selektor, který nezasáhne KPI */
    div[data-testid="stVerticalBlock"] div[data-testid="stPlotlyChart"] {
        background-color: #ffffff !important;
        padding: 12px !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        margin-bottom: 16px !important;
        overflow: hidden !important; /* funguje a neblokuje KPI hover */
        max-width: 100% !important;
    }

    </style>
    """, unsafe_allow_html=True)


    st.title("Cross-Country Analysis of Childhood Obesity")

    # ------------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------------
    if "df" not in st.session_state:
        df = pd.read_csv("data.csv")
        st.session_state.df = df
    else:
        df = st.session_state.df.copy()

    # ---- ALWAYS RUN NORMALIZATION (Belgium + UK) ----
    df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace({
        "Belgium (Flemish)": "Belgium",
        "Belgium (French)": "Belgium"
    })

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

    # ---- APPLY CORRECTIONS ----
    df.loc[df["BUL_BEEN"] == 999, "BUL_BEEN"] = np.nan



    # ============================================================
    # KPI – TOP BAR (ENGLISH + ALIASES + VALUES IN %)
    # ============================================================
    df_2018 = df[df["YEAR"] == 2018].copy()
    if df_2018.empty:
        cz_over = eu_over = global_over = np.nan
        n_countries_total = 0
        top_factor_pretty = "—"
    else:
        cz_over = df_2018[df_2018["COUNTRY_NAME"] == "Czech Republic"]["OVERWEIGHT"].mean()
        eu_over = df_2018[df_2018["COUNTRY_NAME"].isin(eu_list)]["OVERWEIGHT"].mean()
        global_over = df_2018["OVERWEIGHT"].mean()
        n_countries_total = df_2018["COUNTRY_NAME"].nunique()

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
            top_factor_pretty = factor_alias.get(top_factor_code, top_factor_code)
        else:
            top_factor_pretty = "—"
    # ============================================================
    # KPI BOXES
    # ============================================================
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        val = f"{cz_over * 100:.1f}%" if not np.isnan(cz_over) else "—"
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">
                <img src="https://flagcdn.com/w20/cz.png"
                    style="height:18px; vertical-align:middle; margin-right:6px;">
                Obesity in Czechia
            </div>
            <div class="kpi-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        val = f"{eu_over * 100:.1f}%" if not np.isnan(eu_over) else "—"
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">
                <img src="https://flagcdn.com/w20/eu.png"
                    style="height:18px; vertical-align:middle; margin-right:6px;">
                EU Average
            </div>
            <div class="kpi-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        val = f"{global_over * 100:.1f}%" if not np.isnan(global_over) else "—"
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">🌍 Global Average</div>
            <div class="kpi-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">🌐 Number of Countries (2018)</div>
            <div class="kpi-value">{n_countries_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">🔥 Top Risk Factor</div>
            <div class="kpi-value">{top_factor_pretty}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    # ------------------------------------------------------------
    # GRAF 1 TREND
    # ------------------------------------------------------------
    row1_col1, row1_col2 = st.columns([3, 1])
    default_country = "Czech Republic"
    all_countries = sorted(df["COUNTRY_NAME"].unique())
    options = ["All countries"] + all_countries

    with row1_col2:
        st.subheader("Filters")
        selected_country = st.selectbox("Select country:", options, index=0)
        sex_choice = st.radio("Gender:", ["Both", "Girls", "Boys"], horizontal=True)

    df_current = df.copy()
    if sex_choice == "Girls":
        df_current = df_current[df_current["SEX"] == 2]
    elif sex_choice == "Boys":
        df_current = df_current[df_current["SEX"] == 1]

    df_trend = df_current[(df_current["YEAR"] >= 2002) & (df_current["YEAR"] <= 2018)].copy()

    if selected_country == "All countries":
        compare_countries = all_countries
    else:
        compare_countries = [default_country, selected_country]

    color_map = {
        "Czech Republic": DEFAULT_COLOR_CZ,
        selected_country: DEFAULT_COLOR_OTHER
    }

    df_line = (
        df_trend[df_trend["COUNTRY_NAME"].isin(compare_countries)]
        .groupby(["YEAR", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
        .mean()
    )

    with row1_col1:
        fig_line = px.line(
            df_line, x="YEAR", y="OVERWEIGHT",
            color="COUNTRY_NAME", markers=True,
            color_discrete_map=color_map,
            title="Trend of Childhood Overweight (2002–2018)"
        )
        fig_line.update_layout(
            height=450,
            autosize=True,
            margin=dict(l=20, r=20, t=80, b=40),
            legend=dict(
                title="Country",
                orientation="v",
                x=0.02,
                y=0.98,
                font=dict(size=12)
            )
        )

        st.plotly_chart(title24(fig_line), width='stretch', config={})


    # ------------------------------------------------------------
    # GRAF 2 – TOP 5 (aliasy doplněny)
    # ------------------------------------------------------------
    df_current_2018 = df_current[df_current["YEAR"] == 2018].copy()

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

    df_t5_long["FEATURE"] = df_t5_long["FEATURE"].map(lambda x: factor_alias.get(x, x))

    fig_top5 = px.bar(
        df_t5_long,
        x="FEATURE", y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_map=color_map,
        title="TOP 5 factors associated with obesity"
    )

    # Legenda – podmíněné umístění
    if selected_country == "All countries":
        # původní legenda vpravo
        fig_top5.update_layout(
            legend=dict(
                title="Country",
                orientation="v",
                x=1.20,
                y=1,
                xanchor="left",
                yanchor="top"
            )
        )
    else:
        # legenda nahoře uprostřed
        fig_top5.update_layout(
            margin=dict(t=90),
            legend=dict(
                title="Country",      # ← stejně i zde
                orientation="h",
                x=0.70,
                y=1.18,
                xanchor="center",
                yanchor="bottom"
            )
        )


    # ------------------------------------------------------------
    # GRAF 3 – Overweight podle věku
    # ------------------------------------------------------------
    df_age_plot = (
        df_current[df_current["COUNTRY_NAME"].isin(compare_countries)]
        .groupby(["AGE", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
        .mean()
    )

    fig_age = px.line(
        df_age_plot,
        x="AGE", y="OVERWEIGHT",
        color="COUNTRY_NAME",
        markers=True,
        color_discrete_map=color_map,
        title="Overweight by Age"
    )
    # Legenda – podmíněné umístění (stejně jako u TOP5)
    if selected_country == "All countries":
        fig_age.update_layout(
            legend=dict(
                title="Country",      # ← vždy stejný název legendy
                orientation="v",
                x=1.02,
                y=1,
                xanchor="left",
                yanchor="top"
            )
        )
    else:
        fig_age.update_layout(
            margin=dict(t=90),
            legend=dict(
                title="Country",      # ← stejně i zde
                orientation="h",
                x=0.5,
                y=1.18,
                xanchor="center",
                yanchor="bottom"
            )
        )

    col_g2, col_g3 = st.columns(2)

    with col_g2:
        st.plotly_chart(title24(fig_top5), width='stretch', config={})

    with col_g3:
        st.plotly_chart(title24(fig_age), width='stretch', config={})



    # ------------------------------------------------------------
    # GRAF 4 – TOP X (aliasy doplněny)
    # ------------------------------------------------------------
    top_n = st.slider("Number of factors:", 5, 15, 15)   # ← MAX = 15

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

    df_tX_long["FEATURE"] = df_tX_long["FEATURE"].map(lambda x: factor_alias.get(x, x))

    fig_topX = px.bar(
        df_tX_long,
        x="FEATURE", y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_map=color_map,
        title=f"TOP {top_n} additional factors (normalized)"
    )

    # ⭐ ZMĚNA VELIKOSTI NÁZVU
    fig_topX.update_layout(title_font=dict(size=24))

    # ⭐ STEJNÁ LOGIKA LEGENDY — KOPIE Z PŘEDCHOZÍCH GRAFŮ
    if selected_country == "All countries":
        fig_topX.update_layout(
            legend=dict(
                title="Country",
                orientation="v",
                x=1.20,
                y=1,
                xanchor="left",
                yanchor="top"
            )
        )
    else:
        fig_topX.update_layout(
            margin=dict(t=110),
            legend=dict(
                title="Country",
                orientation="h",
                x=0.70,
                y=1.18,
                xanchor="center",
                yanchor="bottom"
            )
        )

    st.plotly_chart(fig_topX, width='stretch', config={})

    # ------------------------------------------------------------
    # SPODNÍ GRAFY – upravené (menší, stejné, legendy nahoře, vedle sebe)
    # ------------------------------------------------------------
    df_eu_2018 = df[df["YEAR"] == 2018].copy()
    if sex_choice == "Girls":
        df_eu_2018 = df_eu_2018[df_eu_2018["SEX"] == 2]
    elif sex_choice == "Boys":
        df_eu_2018 = df_eu_2018[df_eu_2018["SEX"] == 1]

    df_eu_only = df_eu_2018[df_eu_2018["COUNTRY_NAME"].isin(eu_list)]
    eu_avg = df_eu_only["OVERWEIGHT"].mean()

    df_dev = (
        df_eu_only.groupby("COUNTRY_NAME", as_index=False)["OVERWEIGHT"]
        .mean()
    )
    df_dev["DEVIATION"] = df_dev["OVERWEIGHT"] - eu_avg
    df_dev = df_dev.sort_values("DEVIATION")

    # ---------------- GRAF 1 (EU deviation) ----------------
    fig_dev = px.bar(
        df_dev,
        x="DEVIATION", y="COUNTRY_NAME",
        orientation="h",
        color="DEVIATION",
        color_continuous_scale="RdBu_r",
        title="Deviation from EU Average (2018)",
    )

    fig_dev.add_vline(x=0)

    fig_dev.update_layout(
        height=650,
        margin=dict(l=40, r=40, t=60, b=40),
        title_x=0.0
    )


    # ---------------- GRAF 2 (dumbbell) ----------------
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
        mode="markers", 
        name="", 
        marker=dict(color="hotpink", size=12)
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=df_gender_pivot["Boys"], y=df_gender_pivot["COUNTRY_NAME"],
        mode="markers", 
        name="", 
        marker=dict(color="cornflowerblue", size=12)
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=pd.concat([df_gender_pivot["Girls"], df_gender_pivot["Boys"]]),
        y=pd.concat([df_gender_pivot["COUNTRY_NAME"], df_gender_pivot["COUNTRY_NAME"]]),
        mode="lines",
        showlegend=False,
        line=dict(color="gray", width=1.5)
    ))

    fig_dumbbell.update_layout(
        title="<b>Difference Between ♀️ Girls and ♂️ Boys</b>",
        title_x=0.0,
        height=650,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )


    # ---------------- vykreslení – bez velké mezery ----------------
    col4, col5 = st.columns([1, 1])

    with col4:
        st.plotly_chart(title24(fig_dev), width='stretch', config={})

    with col5:
        st.plotly_chart(title24(fig_dumbbell), width='stretch', config={})


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
show_lenka_page()

