import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(layout="wide")

# ------------------------------------------------------------
# CSS – vzhled stránky
# ------------------------------------------------------------
st.markdown("""
<style>
/* Pozadí celé appky */
.stApp {
    background-color: #f6f8fb;
}

/* Menší mezera pod hlavním titulkem */
h1 {
    margin-bottom: 0.3rem;
}

/* KPI sekce – vytáhnout blíž k title, podobně jako Lenka */
.kpi-wrapper {
    margin-top: -0.3rem;
    margin-bottom: 40px;
}

/* jednotlivé KPI boxy */
.kpi-box {
    background: #ffffff;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid #d8e2f5;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    text-align: center;
}

.kpi-box:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(15,23,42,0.18);
}

.kpi-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #4b5563;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #111827;
}

/* Plotly grafy jako karty */
div[data-testid="stPlotlyChart"] {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* === SLIDER – decentní tmavě modro-šedá barva === */
.stSlider > div > div > div > div {
    background-color: #4c5d73 !important;
}

/* kolečka slideru */
.stSlider div[role="slider"] {
    background-color: #334155 !important;
    border: 2px solid #cbd5f5 !important;
}

/* ČÍSLA NAD SLIDEREM (min/max) – Streamlit/BaseUI */
div[data-baseweb="slider"] span {
    color: #475569 !important;
    font-weight: 500;
}

/* když to Streamlit obaluje ještě víc */
div[data-baseweb="slider"] div {
    color: #475569 !important;
}

/* fallback – kdyby Streamlit generoval inline styl barvy */
div[data-baseweb="slider"] * {
    color: #475569 !important;
}

/* Přepiš všechny prvky, které Streamlit obarví default červenou (#f63366 / rgb(246,51,102)) */
span[style*="rgb(246, 51, 102)"],
span[style*="#f63366"],
div[style*="rgb(246, 51, 102)"],
div[style*="#f63366"] {
    color: #475569 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
st.title("Gender Differences in Childhood Overweight")

# ------------------------------------------------------------
# LOADING DATA
# ------------------------------------------------------------
if 'df' not in st.session_state:
    df = pd.read_csv('data.csv')
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
    st.session_state.df = df
else:
    df = st.session_state.df

df.loc[df["BUL_BEEN"] == 999, "BUL_BEEN"] = np.nan

DETAIL_YEAR = 2018

# ------------------------------------------------------------
# KPI BLOCK
# ------------------------------------------------------------
kpi1_label = "📈 Global Change (2002–2018)"
kpi2_label = f"♀️ Girls Overweight ({DETAIL_YEAR})"
kpi3_label = f"♂️ Boys Overweight ({DETAIL_YEAR})"
kpi4_label = "🧒 Highest-Risk Age (2018)"
kpi5_label = "🚨 Highest Overweight Country (2018)"

if df.empty:
    st.warning("No data for selected filters.")
else:
    years_available = sorted(df["YEAR"].unique().tolist())
    base_year = years_available[0]

    df_detail_year = df[df["YEAR"] == DETAIL_YEAR].copy()

    # KPI 1 – změna prevalence mezi prvním rokem a 2018
    overall_detail = df_detail_year["OVERWEIGHT"].mean()
    overall_base = df[df["YEAR"] == base_year]["OVERWEIGHT"].mean()

    if pd.notna(overall_base) and pd.notna(overall_detail):
        diff_pct = (overall_detail - overall_base) * 100
        kpi1_value = f"{diff_pct:+.1f} %"
    else:
        kpi1_value = "N/A"

    # KPI 2 + 3 – podíl OW dívek a chlapců v roce 2018
    kpi2_value = "N/A"
    kpi3_value = "N/A"

    if not df_detail_year.empty:
        df_ow_only = df_detail_year[df_detail_year["OVERWEIGHT"] == 1].copy()
        if not df_ow_only.empty:
            counts = (
                df_ow_only
                .groupby("SEX", observed=True)
                .size()
                .reset_index(name="COUNT")
            )
            if set(counts["SEX"]) == {1, 2}:
                total = counts["COUNT"].sum()
                boys_count = counts.loc[counts["SEX"] == 1, "COUNT"].iloc[0]
                girls_count = counts.loc[counts["SEX"] == 2, "COUNT"].iloc[0]

                boys_pct = boys_count / total * 100
                girls_pct = girls_count / total * 100

                kpi2_value = f"{girls_pct:.0f} %"
                kpi3_value = f"{boys_pct:.0f} %"

    # KPI 4 – věk s nejvyšší prevalencí OW v roce 2018
    kpi4_value = "N/A"
    if not df_detail_year.empty:
        age_means = (
            df_detail_year
            .groupby("AGE", as_index=False, observed=True)["OVERWEIGHT"]
            .mean()
        )
        if not age_means.empty:
            row_max = age_means.sort_values("OVERWEIGHT", ascending=False).iloc[0]
            best_age = int(row_max["AGE"])
            kpi4_value = f"{best_age}"

    # KPI 5 – země s nejvyšší prevalencí OW v roce 2018
    kpi5_value = "N/A"
    if not df_detail_year.empty:
        country_means = (
            df_detail_year
            .groupby("COUNTRY_NAME", as_index=False)["OVERWEIGHT"]
            .mean()
        )
        if not country_means.empty:
            row_max = country_means.sort_values("OVERWEIGHT", ascending=False).iloc[0]
            fattest_country = row_max["COUNTRY_NAME"]
            fattest_value = row_max["OVERWEIGHT"] * 100
            kpi5_value = f"{fattest_country} ({fattest_value:.0f} %)"

    # KPI layout
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">{kpi1_label}</div>
        <div class="kpi-value">{kpi1_value}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">{kpi2_label}</div>
        <div class="kpi-value">{kpi2_value}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">{kpi3_label}</div>
        <div class="kpi-value">{kpi3_value}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">{kpi4_label}</div>
        <div class="kpi-value">{kpi4_value}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">{kpi5_label}</div>
        <div class="kpi-value">{kpi5_value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# FILTERS – vedle grafu 1
# ------------------------------------------------------------
row1_col1, row1_col2 = st.columns([3, 1])
with row1_col2:
    st.subheader("Filters")

    # Country filter
    country_list = sorted(df["COUNTRY_NAME"].unique().tolist())
    country_options = ["All countries"] + country_list
    selected_country = st.selectbox(
        "Select country",
        options=country_options,
        index=0
    )

    # Age filter
    min_age, max_age = int(df["AGE"].min()), int(df["AGE"].max())
    age_min, age_max = st.slider(
        "Select age",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        step=1
    )

df_filtered = df.copy()

if selected_country != "All countries":
    df_filtered = df_filtered[df_filtered["COUNTRY_NAME"] == selected_country]

df_filtered = df_filtered[
    (df_filtered["AGE"] >= age_min) &
    (df_filtered["AGE"] <= age_max)
]

# ------------------------------------------------------------
# DEFINING FACTORS, SCALES
# ------------------------------------------------------------
list_columns = [
    "FRUITS", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
    "TIME_EXE", "PHYS_ACT_60", "DRUNK_30",
    "FAMILY_MEALS_TOGETHER", "BREAKFAST_WEEKDAYS", "BREAKFAST_WEEKEND",
    "TOOTH_BRUSHING", "STUD_TOGETHER",
    "BUL_OTHERS", "BUL_BEEN", "FIGHT_YEAR", "INJURED_YEAR",
    "HEADACHE", "FEEL_LOW", "NERVOUS", "SLEEP_DIF", "DIZZY",
    "TALK_MOTHER", "TALK_FATHER", "LIKE_SCHOOL",
    "SCHOOL_PRESSURE", "COMPUTER_NO"
]

dict_scales = {
    "HEADACHE": 5,
    "NERVOUS": 5,
    "SLEEP_DIF": 5,
    "FEEL_LOW": 5,
    "STOMACHACHE": 5,
    "DIZZY": 5,
    "TALK_FATHER": 5,
    "TALK_MOTHER": 5,
    "FAMILY_MEALS_TOGETHER": 5,
    "TIME_EXE": 7,
    "TOOTH_BRUSHING": 5,
    "HEALTH": 4,
    "LIKE_SCHOOL": 4,
    "STUD_TOGETHER": 5,
    "FRUITS": 7,
    "VEGETABLES": 7,
    "FRIEND_TALK": 7,
    "BREAKFAST_WEEKDAYS": 5,
    "BREAKFAST_WEEKEND": 3,
    "PHYS_ACT_60": 7,
    "LIFESAT": 10,
    "SWEETS": 7,
    "SOFT_DRINKS": 7,
    "DRUNK_30": 5,
    "BUL_BEEN": 5,
    "BUL_OTHERS": 5,
    "FIGHT_YEAR": 5,
    "INJURED_YEAR": 5,
    "COMPUTER_NO": 4,
    "THINK_BODY": 5,
    "SCHOOL_PRESSURE": 4
}

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
    "TOOTH_BRUSHING": "Poor tooth care",
    "STUD_TOGETHER": "No friend time",
    "BUL_OTHERS": "Bullies others",
    "BUL_BEEN": "Been bullied",
    "FIGHT_YEAR": "Often fights",
    "INJURED_YEAR": "Often injured",
    "HEADACHE": "Headaches",
    "FEEL_LOW": "Feels low",
    "NERVOUS": "Nervous",
    "SLEEP_DIF": "Sleep problems",
    "DIZZY": "Dizzy",
    "TALK_MOTHER": "No mom talk",
    "TALK_FATHER": "No dad talk",
    "LIKE_SCHOOL": "Dislikes school",
    "SCHOOL_PRESSURE": "High school pressure",
    "COMPUTER_NO": "Computer/Gaming use"
}

# ------------------------------------------------------------
# NORMALIZACE 0–1 pro DETAIL_YEAR
# ------------------------------------------------------------
def prep_df_normalized_for_year(df_input, year):
    df_year = df_input[df_input["YEAR"] == year].copy()
    for factor in list_columns:
        df_year[factor] = df_year[factor] / dict_scales[factor]
        if factor in reverse_scales:
            df_year[factor] = 1 - df_year[factor]
    return df_year

df_norm_detail = prep_df_normalized_for_year(df_filtered, DETAIL_YEAR)

# ------------------------------------------------------------
# GRAPH 1 – trend OW v čase podle gender
# ------------------------------------------------------------
fig1 = fig2 = fig3 = fig4 = fig5 = fig6 = None

if not df_filtered.empty:
    df_trend = (
        df_filtered
        .groupby(["YEAR", "SEX"], as_index=False, observed=True)["OVERWEIGHT"]
        .mean()
    )
    df_trend["SEX_LABEL"] = df_trend["SEX"].map({1: "Boys", 2: "Girls"})
    colors = {'Girls': "#eb8fbd", 'Boys': "#3b8ee1"}

    fig1 = px.line(
        df_trend,
        y="OVERWEIGHT",
        x="YEAR",
        color="SEX_LABEL",
        color_discrete_map=colors,
    )

    fig1.update_yaxes(range=[0, 0.5])
    fig1.update_xaxes(tickvals=[2002, 2006, 2010, 2014, 2018])
    fig1.update_traces(fill="tozeroy")

    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Overweight prevalence (0-1)",
        legend_title="Gender",
        title=dict(
            text="Trend in Childhood Overweight by Gender (2002-2018)",
            font=dict(size=24),
            x=0.0,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.15,
            xanchor="right",
            x=1.0,
        ),
        margin=dict(l=60, r=40, t=90, b=60)
    )

with row1_col1:
    if fig1 is not None:
        st.plotly_chart(fig1, width='stretch', key="fig1")
    else:
        st.info("Graph 1 not available for current filters.")

# ------------------------------------------------------------
# GRAPH 2 – Top 5 behaviours (OW děti) – Boys vs Girls
# ------------------------------------------------------------
if not df_norm_detail.empty:
    corr_series = (
        df_norm_detail[list_columns + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
    )

    top5_corr = (
        corr_series
        .abs()
        .sort_values(ascending=False)
        .head(5)
        .index
        .tolist()
    )

    df_ow = df_norm_detail[df_norm_detail["OVERWEIGHT"] == 1].copy()

    if not df_ow.empty:
        sex_means = (
            df_ow
            .groupby("SEX", as_index=False, observed=True)[top5_corr]
            .mean()
        )

        if set(sex_means["SEX"]) == {1, 2}:
            df_long = sex_means.melt(
                id_vars="SEX",
                value_vars=top5_corr,
                var_name="FACTOR",
                value_name="VALUE"
            )

            df_long["SEX_LABEL"] = df_long["SEX"].map({1: "Boys", 2: "Girls"})
            df_long["FACTOR_LABEL"] = df_long["FACTOR"].map(factor_alias)

            order_help = (
                df_long
                .groupby("FACTOR_LABEL")["VALUE"]
                .mean()
                .sort_values(ascending=False)
                .index
                .tolist()
            )

            fig2 = px.bar(
                df_long,
                x="VALUE",
                y="FACTOR_LABEL",
                color="SEX_LABEL",
                orientation="h",
                barmode="group",
                category_orders={"FACTOR_LABEL": order_help},
                color_discrete_map={"Boys": "#3b8ee1", "Girls": "#eb8fbd"},
                title=f"Top 5 Behaviours Linked to Overweight – Boys vs Girls ({DETAIL_YEAR})"
            )

            fig2.update_layout(
                xaxis_title="Average risk (0–1)",
                yaxis_title="Behaviour",
                legend_title="Gender",
                height=500,
                margin=dict(l=80, r=40, t=60, b=60),
                title=dict(font=dict(size=24))
            )

# ------------------------------------------------------------
# GRAPH 3 – Gender gap by factor (OW děti, zbylé faktory)
# ------------------------------------------------------------
if not df_norm_detail.empty and "top5_corr" in locals():
    remaining_factors = [f for f in list_columns if f not in top5_corr]

    df_ow_detail = df_norm_detail[df_norm_detail["OVERWEIGHT"] == 1].copy()

    if not df_ow_detail.empty and remaining_factors:
        sex_means_all = (
            df_ow_detail
            .groupby("SEX", as_index=False, observed=True)[remaining_factors]
            .mean()
        )

        if set(sex_means_all["SEX"]) == {1, 2}:
            sex_long_all = sex_means_all.melt(
                id_vars=["SEX"],
                value_vars=remaining_factors,
                var_name="FACTOR",
                value_name="VALUE"
            )
            sex_long_all["SEX_STRING"] = sex_long_all["SEX"].map({1: "Boys", 2: "Girls"})

            gap_table_rest = (
                sex_long_all
                .groupby(["FACTOR", "SEX_STRING"], observed=True)["VALUE"]
                .mean()
                .unstack("SEX_STRING")
            )

            gap_table_rest["GIRLS_MINUS_BOYS"] = (
                gap_table_rest["Girls"] - gap_table_rest["Boys"]
            )
            df_gap = gap_table_rest.reset_index()

            factor_order = (
                df_gap
                .sort_values("GIRLS_MINUS_BOYS", ascending=False)["FACTOR"]
                .tolist()
            )

            df_gap["FACTOR_LABEL"] = df_gap["FACTOR"].map(factor_alias)
            factor_order_labels = [
                factor_alias.get(f, f) for f in factor_order
            ]

            df_gap["SIDE"] = np.where(
                df_gap["GIRLS_MINUS_BOYS"] > 0,
                "Girls",
                "Boys"
            )

            color_gap = {
                "Girls": "#eb8fbd",
                "Boys": "#3b8ee1"
            }

            fig3 = px.bar(
                df_gap,
                x="FACTOR_LABEL",
                y="GIRLS_MINUS_BOYS",
                color="SIDE",
                color_discrete_map=color_gap,
                category_orders={"FACTOR_LABEL": factor_order_labels},
                title=f"Gender Gap Across Risk Factors (Overweight children, {DETAIL_YEAR})"
            )

            fig3.update_layout(
                xaxis_title="Risk factor",
                yaxis_title="Girls - Boys (difference)",
                legend_title="Group with higher risk",
                xaxis=dict(tickangle=-40),
                yaxis=dict(
                    tickmode="linear",
                    tick0=0,
                    dtick=0.05,
                    showgrid=True,
                    gridcolor="lightgray",
                    gridwidth=1,
                    zeroline=False,
                    showline=False,
                    linewidth=0
                ),
                height=500,
                margin=dict(l=80, r=40, b=120),
                title=dict(
                    text=f"Gender Gap by Risk Factor ({DETAIL_YEAR})",
                    font=dict(size=24)
                )
            )


# ------------------------------------------------------------
# GRAPH 4 – Overweight by Age and Gender (2018)
# ------------------------------------------------------------
df_age_base = df[df["YEAR"] == DETAIL_YEAR].copy()
if selected_country != "All countries":
    df_age_base = df_age_base[df_age_base["COUNTRY_NAME"] == selected_country]

if not df_age_base.empty:
    df_age_trend = (
        df_age_base
        .groupby(["AGE", "SEX"], as_index=False, observed=True)["OVERWEIGHT"]
        .mean()
    )
    df_age_trend["SEX_LABEL"] = df_age_trend["SEX"].map({1: "Boys", 2: "Girls"})

    fig4 = px.line(
        df_age_trend,
        x="AGE",
        y="OVERWEIGHT",
        color="SEX_LABEL",
        markers=True,
        color_discrete_map=colors,
        title=f"Overweight by Age and Gender ({DETAIL_YEAR})"
    )
    fig4.update_layout(
        xaxis_title="Age",
        yaxis_title="Overweight prevalence (0–1)",
        legend_title="Gender",
        title=dict(font=dict(size=24)),
        height=600,
        margin=dict(l=80, r=40, t=60, b=60)
    )

# ------------------------------------------------------------
# GRAPH 5 – OW vs Non-OW – rozdíl faktorů
# ------------------------------------------------------------
if not df_norm_detail.empty:
    df_fig5 = df_norm_detail.copy()

    df_ow_all = df_fig5[df_fig5["OVERWEIGHT"] == 1]
    df_non_all = df_fig5[df_fig5["OVERWEIGHT"] == 0]

    if not df_ow_all.empty and not df_non_all.empty:
        ow_means = df_ow_all[list_columns].mean()
        non_means = df_non_all[list_columns].mean()
        diff = ow_means - non_means

        df_diff = (
            diff.rename("DIFFERENCE")
                .reset_index()
                .rename(columns={"index": "FACTOR"})
        )
        df_diff["DIFFERENCE"] = df_diff["DIFFERENCE"].fillna(0.0)
        df_diff["ABS_DIFF"] = df_diff["DIFFERENCE"].abs()

        df_diff = df_diff.sort_values("ABS_DIFF", ascending=False)

        df_diff["FACTOR_LABEL"] = df_diff["FACTOR"].map(factor_alias)

        df_diff["SIDE"] = np.where(
            df_diff["DIFFERENCE"] > 0,
            "Overweight",
            "Non-Overweight"
        )

        color_ow = {
            "Overweight": "orangered",
            "Non-Overweight": "seagreen"
        }

        fig5 = px.bar(
            df_diff,
            x="DIFFERENCE",
            y="FACTOR_LABEL",
            orientation="h",
            color="SIDE",
            color_discrete_map=color_ow,
            category_orders={"FACTOR_LABEL": df_diff["FACTOR_LABEL"].tolist()},
            title=f"Overweight vs Non-Overweight Differences ({DETAIL_YEAR})",
        )

        fig5.update_layout(
            xaxis_title="Overweight - Non-Overweight (difference)",
            yaxis_title="Risk factor",
            legend_title="Group with higher risk",
            xaxis=dict(
                tickmode="linear",
                tick0=0,
                dtick=0.05,
                showgrid=True,
                gridcolor="lightgray",
                gridwidth=1,
                zeroline=False
            ),
            height=600,
            margin=dict(l=200, r=40, t=60, b=60),
            yaxis=dict(automargin=True),
            title=dict(
                text=f"Overweight vs Non-Overweight Differences ({DETAIL_YEAR})",
                font=dict(size=24)
            )
        )

# ------------------------------------------------------------
# GRAPH 6 – World map: where are girls vs boys more overweight?
# ------------------------------------------------------------
df_map = df[
    (df["YEAR"] == DETAIL_YEAR) &
    (df["AGE"] >= age_min) &
    (df["AGE"] <= age_max)
].copy()

if not df_map.empty:
    df_map["SEX_LABEL"] = df_map["SEX"].map({1: "Boys", 2: "Girls"})

    df_gender = (
        df_map
        .groupby(["COUNTRY_NAME", "SEX_LABEL"], as_index=False, observed=True)["OVERWEIGHT"]
        .mean()
    )

    df_pivot = (
        df_gender
        .pivot(index="COUNTRY_NAME", columns="SEX_LABEL", values="OVERWEIGHT")
        .reset_index()
    )

    df_pivot = df_pivot.dropna(subset=["Boys", "Girls"], how="all")

    df_pivot["GAP_PP"] = (df_pivot["Girls"] - df_pivot["Boys"]) * 100

    max_gap = np.nanmax(np.abs(df_pivot["GAP_PP"]))
    max_range = max(5, np.ceil(max_gap / 5.0) * 5)

    gender_gap_colors = [
        "#08306b",
        "#2171b5",
        "#e5e7eb",
        "#fbb6ce",
        "#be185d",
    ]

    fig6 = px.choropleth(
        df_pivot,
        locations="COUNTRY_NAME",
        locationmode="country names",
        color="GAP_PP",
        color_continuous_scale=gender_gap_colors,
        range_color=(-max_range, max_range),
        title=f"Where Are Girls vs Boys More Overweight? (2018, age {age_min}–{age_max})",
        hover_name="COUNTRY_NAME",
        hover_data={
            "GAP_PP": ":.1f",
            "Boys": ":.1%",
            "Girls": ":.1%",
        },
    )

    fig6.update_coloraxes(
        colorbar_title="Girls − Boys (p.p.)",
        colorbar_tickformat=".1f",
        cmid=0
    )

    fig6.update_geos(
        projection_type="equirectangular",
        showcountries=True,
        showland=True,
        landcolor="white",
        showcoastlines=True,
        showframe=False,
        lataxis_range=[30, 75],
        lonaxis_range=[-120, 80],
    )

    fig6.update_traces(
        marker_line_width=0.6,
        marker_line_color="black",
    )

    fig6.update_layout(
        height=580,
        margin=dict(l=10, r=10, t=40, b=20),
        title=dict(
            font=dict(size=24),
            y=0.93,
        ),
    )

# ------------------------------------------------------------
# FIX LEGEND RIGHT (jen bar grafy + age graf)
# ------------------------------------------------------------
def fix_legend_right(fig, right_margin=160):
    if fig is None:
        return

    fig.update_layout(
        legend=dict(
            x=1.02,
            xanchor="left",
            y=1.0,
            yanchor="top",
            orientation="v",
        ),
        margin=dict(
            l=80,
            r=right_margin,
            t=60,
            b=80,
        ),
    )

for f in [fig2, fig3, fig4, fig5]:
    fix_legend_right(f)

# ------------------------------------------------------------
# DASHBOARD LAYOUT
# ------------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    if fig2 is not None:
        st.plotly_chart(fig2, width='stretch', key="fig2")
    else:
        st.info("Graph 2 not available for current filters.")

with row2_col2:
    if fig3 is not None:
        st.plotly_chart(fig3, width='stretch', key="fig3")
    else:
        st.info("Graph 3 not available for current filters.")

row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    if fig4 is not None:
        st.plotly_chart(fig4, width='stretch', key="fig4")
    else:
        st.info("Graph 4 not available for current filters.")

with row3_col2:
    if fig5 is not None:
        st.plotly_chart(fig5, width='stretch', key="fig5")
    else:
        st.info("Graph 5 not available for current filters.")

# Graph 6 – full width
if 'fig6' in locals() and fig6 is not None:
    st.plotly_chart(fig6, width='stretch', key="fig6")
else:
    st.info("Graph 6 not available for current filters.")
