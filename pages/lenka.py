import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# 1) Nastavení faktorů + škály
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


# ------------------------------------------------------------
# Hlavní funkce stránky
# ------------------------------------------------------------
def show_lenka_page():

    st.set_page_config(
        page_title="Analýza dětské obezity",
        layout="wide",
    )

    st.title("Analýza dětské obezity podle zemí")
    st.write("Interaktivní analýza obezity a nejdůležitějších faktorů.")

    # ------------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------------
    if "df" not in st.session_state:
        df = pd.read_csv("data.csv")

        df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace({
            "Belgium (Flemish)": "Belgium",
            "Belgium (French)": "Belgium"
        })

        st.session_state.df = df
    else:
        df = st.session_state.df

    df.loc[df["BUL_BEEN"] == 999, "BUL_BEEN"] = np.nan
    df_2018 = df[df["YEAR"] == 2018].copy()

    # ------------------------------------------------------------
    # FILTRY VEDLE SEBE
    # ------------------------------------------------------------
    col_f1, col_f2 = st.columns(2)

    default_country = "Czech Republic"
    all_countries = sorted(df["COUNTRY_NAME"].unique())
    options = ["All countries"] + all_countries

    # 1️⃣ Nejdřív výběr země
    with col_f1:
        selected_country = st.selectbox(
            "Vyber druhou zemi k porovnání:",
            options
        )

    # 2️⃣ Potom výběr pohlaví
    with col_f2:
        sex_choice = st.radio(
            "Zobrazit data pro:",
            ["Vše", "Jen dívky", "Jen chlapce"],
            horizontal=True
        )


    # ------------------------------------------------------------
    # FILTR POHLAVÍ JEN PRO GRAF 1 A 2
    # ------------------------------------------------------------
    df_sex = df.copy()
    df_sex_2018 = df_2018.copy()

    if sex_choice == "Jen dívky":
        df_sex = df_sex[df_sex["SEX"] == 2]
        df_sex_2018 = df_sex_2018[df_sex_2018["SEX"] == 2]

    elif sex_choice == "Jen chlapce":
        df_sex = df_sex[df_sex["SEX"] == 1]
        df_sex_2018 = df_sex_2018[df_sex_2018["SEX"] == 1]

    # ------------------------------------------------------------
    # FILTR ZEMÍ
    # ------------------------------------------------------------
    if selected_country == "All countries":
        compare_countries = all_countries
        title_text = "Vývoj prevalence obezity – všechny země (včetně ČR)"
    else:
        compare_countries = [default_country, selected_country]
        title_text = f"Vývoj prevalence obezity ({default_country} vs. {selected_country})"

    # ------------------------------------------------------------
    # NADPISY PRVNÍCH DVOU GRAFŮ VEDLE SEBE
    # ------------------------------------------------------------
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.subheader("Vývoj prevalence obezity")

    with col_t2:
        st.subheader("TOP 5 faktorů souvisejících s obezitou")

    # ------------------------------------------------------------
    # 🔥 GRAF 1 — LINE CHART (df_sex)
    # ------------------------------------------------------------

    df_line = (
        df_sex[df_sex["COUNTRY_NAME"].isin(compare_countries)]
        .groupby(["YEAR", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
        .mean()
    )

    fig_line = px.line(
        df_line,
        x="YEAR",
        y="OVERWEIGHT",
        color="COUNTRY_NAME",
        markers=True,
        title="",
        color_discrete_map={
            "Czech Republic": "#1F77B4",
            selected_country: "#FF7F0E"
        }
    )

    fig_line.update_layout(hovermode="x unified", height=450)

    # ------------------------------------------------------------
    # 🔥 GRAF 2 — TOP 5 faktorů (df_sex_2018)
    # ------------------------------------------------------------

    df_norm = df_sex_2018.copy()

    for col in factors:
        if col in dictionary:
            max_val = dictionary[col]
            if col in reverse_scales:
                df_norm[col] = (max_val + 1 - df_norm[col]) / max_val
            else:
                df_norm[col] = df_norm[col] / max_val

    corr_series = (
        df_norm[factors + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
        .abs()
        .sort_values(ascending=False)
    )

    top5 = corr_series.head(5).index.tolist()

    df_top5 = (
        df_sex_2018[df_sex_2018["COUNTRY_NAME"].isin(compare_countries)]
        .groupby("COUNTRY_NAME")[top5]
        .mean()
        .reset_index()
    )

    df_top5_long = df_top5.melt(
        id_vars="COUNTRY_NAME",
        value_vars=top5,
        var_name="FEATURE",
        value_name="VALUE"
    )

    fig_top5 = px.bar(
        df_top5_long,
        x="FEATURE",
        y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        title="",
        color_discrete_map={
            "Czech Republic": "#1F77B4",
            selected_country: "#FF7F0E"
        }
    )

    fig_top5.update_layout(height=450)

    # ------------------------------------------------------------
    # GRAFY 1 + 2 VEDLE SEBE
    # ------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.plotly_chart(fig_top5, use_container_width=True)


    # =====================================================================
    # 📌 OD TADY DÁL UŽ NEFILTROVAT POHLAVÍ → PŮVODNÍ df_2018
    # =====================================================================

    # ------------------------------------------------------------
    # 🔵 GRAF 3 — EU deviation
    # ------------------------------------------------------------
    st.subheader("Odchylka zemí od EU průměru (2018)")

    eu = [
        "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
        "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
        "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Malta",
        "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
        "Slovenia", "Spain", "Sweden", "United Kingdom"
    ]

    df_eu = df_2018[df_2018["COUNTRY_NAME"].isin(eu)]
    eu_avg = df_eu["OVERWEIGHT"].mean()

    df_dev = (
        df_eu.groupby("COUNTRY_NAME", as_index=False)["OVERWEIGHT"]
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
        title=f"Odchylka od EU průměru (EU avg = {eu_avg:.3f})"
    )

    fig_dev.update_layout(height=600)
    fig_dev.add_vline(x=0)

    # ------------------------------------------------------------
    # 🔵 GRAF 4 — Boys vs Girls
    # ------------------------------------------------------------
    st.subheader("Overweight – porovnání Boys vs Girls (EU, 2018)")

    df_2018["SEX_LABEL"] = df_2018["SEX"].map({1: "Boys", 2: "Girls"})
    df_eu_gender = df_2018[df_2018["COUNTRY_NAME"].isin(eu)]

    df_gender = (
        df_eu_gender.groupby(["COUNTRY_NAME", "SEX_LABEL"], as_index=False)["OVERWEIGHT"]
        .mean()
        .pivot(index="COUNTRY_NAME", columns="SEX_LABEL", values="OVERWEIGHT")
        .reset_index()
    )

    df_gender = df_gender.dropna()
    df_gender["DIFF"] = df_gender["Girls"] - df_gender["Boys"]
    df_gender = df_gender.sort_values("DIFF")

    fig_dumbbell = go.Figure()

    fig_dumbbell.add_trace(go.Scatter(
        x=df_gender["Girls"], y=df_gender["COUNTRY_NAME"],
        mode="markers", marker=dict(color="hotpink", size=10), name="Girls"
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=df_gender["Boys"], y=df_gender["COUNTRY_NAME"],
        mode="markers", marker=dict(color="cornflowerblue", size=10), name="Boys"
    ))

    fig_dumbbell.add_trace(go.Scatter(
        x=pd.concat([df_gender["Boys"], df_gender["Girls"]]),
        y=pd.concat([df_gender["COUNTRY_NAME"], df_gender["COUNTRY_NAME"]]),
        mode="lines", line=dict(color="gray", width=1.5),
        showlegend=False
    ))

    fig_dumbbell.update_layout(
        height=600,
        title="Overweight Boys vs Girls – EU (2018)"
    )

    # ------------------------------------------------------------
    # GRAFY 3 + 4 VEDLE SEBE
    # ------------------------------------------------------------
    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(fig_dev, use_container_width=True)

    with col4:
        st.plotly_chart(fig_dumbbell, use_container_width=True)


# ------------------------------------------------------------
# Spuštění stránky
# ------------------------------------------------------------
show_lenka_page()
