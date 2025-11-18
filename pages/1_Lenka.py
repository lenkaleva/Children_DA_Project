import streamlit as st
import pandas as pd
import plotly.express as px


def show_lenka_page():
    # ----------------------------------------------------------------------------
    # LOAD DATA
    # ----------------------------------------------------------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("final_data.csv")
        return df

    df = load_data()

    st.title("Analýza obezity dětí v Evropě")
    st.write("Interaktivní přehled obezity podle zemí, věku a pohlaví.")

    # ----------------------------------------------------------------------------
    # 1) SROVNÁNÍ OBEZITY MEZI ZEMĚMI — ČR ZVÝRAZNĚNA
    # ----------------------------------------------------------------------------
    st.header("📊 Obezita podle evropských zemí (ČR zvýrazněna)")

    country_stats = (
        df.groupby("COUNTRY_NAME")["OVERWEIGHT"]
        .mean()
        .reset_index()
        .sort_values("OVERWEIGHT", ascending=False)
    )

    # Highlight Czech Republic
    country_stats["COLOR"] = country_stats["COUNTRY_NAME"].apply(
        lambda x: "red" if x == "Czech Republic" else "lightgray"
    )

    fig_country = px.bar(
        country_stats,
        x="COUNTRY_NAME",
        y="OVERWEIGHT",
        color="COLOR",
        color_discrete_map={"red": "red", "lightgray": "lightgray"},
        title="Průměrná míra obezity podle země (ČR zvýrazněna)",
        labels={"COUNTRY_NAME": "Země", "OVERWEIGHT": "Obezita (průměr)", "COLOR": ""}
    )

    st.plotly_chart(fig_country, width="stretch")

    # ----------------------------------------------------------------------------
    # 2) KLUKI VS HOLKY — ČR ZVÝRAZNĚNA
    # ----------------------------------------------------------------------------
    st.header("🧑‍🤝‍🧑 Obezita chlapců vs. dívek (ČR zvýrazněna)")

    df["SEX_LABEL"] = df["SEX"].map({1: "Chlapci", 2: "Dívky"})

    gender_stats = (
        df.groupby(["COUNTRY_NAME", "SEX_LABEL"])["OVERWEIGHT"]
        .mean()
        .reset_index()
    )

    def bar_color(row):
        if row["COUNTRY_NAME"] == "Czech Republic" and row["SEX_LABEL"] == "Chlapci":
            return "darkblue"
        if row["COUNTRY_NAME"] == "Czech Republic" and row["SEX_LABEL"] == "Dívky":
            return "deeppink"
        return "lightgray"

    gender_stats["COLOR"] = gender_stats.apply(bar_color, axis=1)

    fig_gender = px.bar(
        gender_stats,
        x="COUNTRY_NAME",
        y="OVERWEIGHT",
        color="COLOR",
        barmode="group",
        color_discrete_map={
            "darkblue": "darkblue",
            "deeppink": "deeppink",
            "lightgray": "lightgray"
        },
        title="Rozdíly v obezitě podle pohlaví a země (ČR zvýrazněna)",
        labels={"COUNTRY_NAME": "Země", "OVERWEIGHT": "Obezita", "COLOR": ""}
    )

    st.plotly_chart(fig_gender, width="stretch")

    # ----------------------------------------------------------------------------
    # 3) DETAILNÍ ANALÝZA ZEMĚ — SELECTBOX
    # ----------------------------------------------------------------------------
    st.header("🔍 Detail podle vybrané země")

    selected_country = st.selectbox(
        "Vyber zemi:",
        sorted(df["COUNTRY_NAME"].unique()),
        index=sorted(df["COUNTRY_NAME"].unique()).index("Czech Republic")
    )

    country_df = df[df["COUNTRY_NAME"] == selected_country]

    country_gender = (
        country_df.groupby("SEX_LABEL")["OVERWEIGHT"]
        .mean()
        .reset_index()
    )

    fig_detail = px.bar(
        country_gender,
        x="SEX_LABEL",
        y="OVERWEIGHT",
        color="SEX_LABEL",
        color_discrete_map={"Chlapci": "blue", "Dívky": "pink"},
        title=f"Obezita chlapců a dívek — {selected_country}",
        labels={"SEX_LABEL": "Pohlaví", "OVERWEIGHT": "Obezita"}
    )

    st.plotly_chart(fig_detail, width="stretch")
