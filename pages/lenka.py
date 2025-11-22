import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 1) Seznam všech faktorů (jak jsme definovali)
# ------------------------------------------------------------

list_columns_2 = [
    "FRUITS", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
    "TIME_EXE", "PHYS_ACT_60", "DRUNK_30",
    "FAMILY_MEALS_TOGETHER", "BREAKFAST_WEEKDAYS", "BREAKFAST_WEEKEND",
    "TOOTH_BRUSHING", "STUD_TOGETHER", "BUL_OTHERS", "BUL_BEEN",
    "FIGHT_YEAR", "INJURED_YEAR", "HEADACHE", "FEEL_LOW",
    "NERVOUS", "SLEEP_DIF", "DIZZY",
    "TALK_MOTHER", "TALK_FATHER",
    "LIKE_SCHOOL", "SCHOOL_PRESSURE", "COMPUTER_NO"
]

# ------------------------------------------------------------
# 2) Maximální hodnoty (škály)
# ------------------------------------------------------------

dictionary = {
    "HEADACHE": 5,
    "NERVOUS": 5,
    "SLEEP_DIF": 5,
    "FEEL_LOW": 5,
    "STOMACHACHE": 5,
    "DIZZY": 5,

    "TALK_FATHER": 5,
    "TALK_MOTHER": 5,
    "FAMILY_MEALS_TOGETHER": 6,
    "TIME_EXE": 7,
    "TOOTH_BRUSHING": 5,
    "HEALTH": 4,
    "LIKE_SCHOOL": 4,
    "STUD_TOGETHER": 5,
    "FRUITS": 7, "SOFT_DRINKS": 7, "SWEETS": 7, "VEGETABLES": 7,
    "FRIEND_TALK": 7, "PHYS_ACT_60": 7, "DRUNK_30": 7,
    "LIFESAT": 10, "BREAKFAST_WEEKDAYS": 6, "BREAKFAST_WEEKEND": 3,
    "BUL_OTHERS": 5, "BUL_BEEN": 5,
    "FIGHT_YEAR": 5, "INJURED_YEAR": 5,
    "THINK_BODY": 5, "SCHOOL_PRESSURE": 4,
    "COMPUTER_NO": 4
}

# ------------------------------------------------------------
# 3) Reversed faktory – čím více, tím lepší (musíme otočit)
# ------------------------------------------------------------

reverse_scales = {
    "HEADACHE",
    "NERVOUS",
    "SLEEP_DIF",
    "DIZZY",
    "FEEL_LOW",
    "STOMACHACHE",
    "BREAKFAST_WEEKDAYS",
    "BREAKFAST_WEEKEND",
    "FRIEND_TALK",
    "FRUITS",
    "LIFESAT",
    "PHYS_ACT_60",
    "VEGETABLES"
}


# ------------------------------------------------------------
# Hlavní funkce stránky
# ------------------------------------------------------------
def show_lenka_page():

    st.title("🇪🇺 Analýza obezity dětí v Evropě (HBSC)")
    st.write("Interaktivní analýza prevalence obezity a nejdůležitějších faktorů.")

    # ------------------------------------------------------------
    # LOAD DATA (pouze 1×)
    # ------------------------------------------------------------
    if "df" not in st.session_state:
        df = pd.read_csv("data.csv")

        # sjednocení Belgie
        df["COUNTRY_NAME"] = df["COUNTRY_NAME"].replace({
            "Belgium (Flemish)": "Belgium",
            "Belgium (French)": "Belgium"
        })

        st.session_state.df = df
    else:
        df = st.session_state.df

    # extrahujeme jen 2018
    df_2018 = df[df["YEAR"] == 2018].copy()

    # ------------------------------------------------------------
    # VÝBĚR ZEMÍ – hlavní filtr pro celou stránku
    # ------------------------------------------------------------
    default_country = "Czech Republic"
    all_countries = sorted(df["COUNTRY_NAME"].unique())

    options = ["All countries"] + all_countries
    selected_country = st.selectbox("Vyber druhou zemi k porovnání:", options)

    # logika výběru
    if selected_country == "All countries":
        compare_countries = all_countries
        title_text = "Vývoj prevalence obezity – všechny země (včetně ČR)"
    else:
        compare_countries = [default_country, selected_country]
        title_text = f"Vývoj prevalence obezity ({default_country} vs. {selected_country})"

    # ------------------------------------------------------------
    # 🔥 GRAF 1 — LINE CHART (vývoj obezity)
    # ------------------------------------------------------------

    df_line = (
        df[df["COUNTRY_NAME"].isin(compare_countries)]
        .groupby(["YEAR", "COUNTRY_NAME"], as_index=False)["OVERWEIGHT"]
        .mean()
     )

    fig_line = px.line(
        df_line,
        x="YEAR",
        y="OVERWEIGHT",
        color="COUNTRY_NAME",
        markers=True,
        title=title_text
    )

    # zvýraznění ČR
    fig_line.update_traces(
        selector=dict(name="Czech Republic"),
        line=dict(width=5, color="#ff4d4d")
    )
    fig_line.update_traces(
        selector=lambda tr: tr.name != "Czech Republic",
        line=dict(width=2)
    )

    fig_line.update_layout(
        hovermode="x unified",
        height=450,
        width=1400
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # ------------------------------------------------------------
    # PŘÍPRAVA DAT PRO KORELACE (TOP5 + NEXT10)
    # ------------------------------------------------------------

    df_corr_source = df[
        (df["YEAR"] == 2018) &
        (df["COUNTRY_NAME"].isin(compare_countries))
    ].copy()

    factor_candidates = [c for c in list_columns_2 if c in df_corr_source.columns]

    # normalizace faktorů
    for col in factor_candidates:
        max_val = dictionary[col]
        if col in reverse_scales:
            df_corr_source[col] = (max_val + 1 - df_corr_source[col]) / max_val
        else:
            df_corr_source[col] = df_corr_source[col] / max_val

    # korelace s obezitou (dynamické)
    corr_series = (
        df_corr_source[factor_candidates + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
        .abs()
        .sort_values(ascending=False)
    )

    top5 = corr_series.index[:5].tolist()
    next10 = corr_series.index[5:15].tolist()

    # ------------------------------------------------------------
    # 🔥 GRAF 2 — TOP 5 faktorů (GROUPED BAR CHART)
    # ------------------------------------------------------------

    st.subheader("TOP 5 faktorů souvisejících s obezitou")

    df_top5 = (
        df_2018[df_2018["COUNTRY_NAME"].isin(compare_countries)]
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

    colors_top5 = ["#ff4d4d"] + [None] * (len(compare_countries) - 1)

    fig_top5 = px.bar(
        df_top5_long,
        x="FEATURE",
        y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_sequence=colors_top5,
        title=f"TOP 5 faktorů ({default_country} vs. {selected_country})"
    )

    fig_top5.update_xaxes(tickangle=45)
    fig_top5.update_layout(height=500)

    st.plotly_chart(fig_top5, use_container_width=True)

    # ------------------------------------------------------------
    # 🔥 GRAF 3 — NEXT 10 faktorů (VERTIKÁLNÍ BAR CHART)
    # ------------------------------------------------------------

    st.subheader("Dalších 10 relevantních faktorů ovlivňujících obezitu")

    df_next10 = (
        df_2018[df_2018["COUNTRY_NAME"].isin(compare_countries)]
        .groupby("COUNTRY_NAME")[next10]
        .mean()
        .reset_index()
    )

    df_next10_long = df_next10.melt(
        id_vars="COUNTRY_NAME",
        value_vars=next10,
        var_name="FEATURE",
        value_name="VALUE"
    )

    colors_next10 = ["#ff4d4d"] + [None] * (len(compare_countries) - 1)

    fig_next10 = px.bar(
        df_next10_long,
        x="FEATURE",
        y="VALUE",
        color="COUNTRY_NAME",
        barmode="group",
        color_discrete_sequence=colors_next10,
        title=f"Dalších 10 faktorů ({default_country} vs. {selected_country})"
    )

    fig_next10.update_xaxes(tickangle=45)
    fig_next10.update_layout(height=600)

    st.plotly_chart(fig_next10, use_container_width=True)


# ------------------------------------------------------------
# Spuštění stránky
# ------------------------------------------------------------
show_lenka_page()
