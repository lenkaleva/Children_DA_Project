import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


###########################################################
# LOADING DATA
# already loaded on app.py - using df for convenience
if 'df' not in st.session_state:
    df = pd.read_csv('data.csv')
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

# ROW: Graph 1 + Filters
col_graph1, col_filters = st.columns([2, 1])

#########################################################
# STREAMLIT PAGE SETUP

st.title("Gender Differences in Childhood Overweight")
st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Pozadí celé appky */
.stApp {
    background-color: #f6f8fb;
}

/* === KPI sekce - mezera pod KPI boxy === */
.kpi-wrapper {
    margin-bottom: 80px; 
}

/* jednotlivé KPI boxy */
.kpi-box {
    background: #ffffff;
    padding:16px;
    border-radius:16px;
    border:1px solid #d8e2f5;
    box-shadow:0 2px 6px rgba(0,0,0,0.12);
    text-align:center;
}

/* mezery mezi grafy */
.plot-box {
    margin-top: 20px;
}

.kpi-box:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(15,23,42,0.18);
}

.kpi-label {
    font-size: 0.9rem;
    font-weight: 500;
    color: #4b5563;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #111827;
}

/* Pidlíky pro kluky/holky v KPI 2 a 4 */
.gender-pill {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    width:1.9rem;
    height:1.9rem;
    border-radius:0.6rem;
    font-size:1.1rem;
    color:white;
    margin-right:0.25rem;
}
.gender-pill.male {
    background:#3b82f6;
}
.gender-pill.female {
    background:#ec4899;
    margin-left:0.6rem;
    margin-right:0.25rem;
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
    background-color: #4c5d73 !important;  /* tmavě šedo-modrá */
}

/* kolečka slideru */
.stSlider div[role="slider"] {
    background-color: #334155 !important;
    border: 2px solid #cbd5f5 !important;
}

/* Barva čísel nad sliderem (min/max) */
div[data-baseweb="slider"] span {
    color: color: #2B6CB0;   /* tmavě šedá/modrošedá */
    font-weight: 500;

/* Slider – barva textu (min/max hodnoty, případně i label) */
.stSlider span {
    color: #4b5563 !important;   /* tmavší šedá/modrošedá */
}

            /* ČÍSLA NAD SLIDEREM (min/max) – Streamlit/BaseUI */
div[data-baseweb="slider"] span {
    color: #475569 !important;   /* tmavě šedo-modrá místo červené */
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
    color: #475569 !important;   /* tvoje tmavě šedá/modrošedá */
} 


</style>
""", unsafe_allow_html=True)


########################################################
# KPI BLOCK
DETAIL_YEAR = 2018
if df.empty:
    st.warning("No data for selected filters.")
else:
    # roky v aktuálním filtru
    years_available = sorted(df["YEAR"].unique().tolist())
    base_year = years_available[0]

    # data jen pro DETAIL_YEAR (2018) – pro KPI 2–4
    df_detail_year = df[df["YEAR"] == DETAIL_YEAR].copy()

    # ---------- KPI 1: Overweight change (base_year -> DETAIL_YEAR) ----------
    overall_detail = df_detail_year["OVERWEIGHT"].mean()
    overall_base = df[df["YEAR"] == base_year]["OVERWEIGHT"].mean()

    kpi1_label = "OW change"
    if pd.notna(overall_base) and pd.notna(overall_detail):
        diff_pct = (overall_detail - overall_base) * 100
        kpi1_value = f"{diff_pct:+.1f} %"
    else:
        kpi1_value = "N/A"

    # ---------- KPI 4 (nově KPI2): Gender split among OW children (DETAIL_YEAR) ----------
    kpi2_label = "OW boys / girls"
    kpi2_value = "N/A"

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
                kpi2_value = f"♂️ {boys_pct:.0f} % ♀️ {girls_pct:.0f} %"

    # ---------- KPI 3: Age with highest overweight (DETAIL_YEAR) ----------
    kpi3_label = "Worst age"
    kpi3_value = "N/A"

    if not df_detail_year.empty:
        age_means = (
            df_detail_year
            .groupby("AGE", as_index=False, observed=True)["OVERWEIGHT"]
            .mean()
        )
        if not age_means.empty:
            row_max = age_means.sort_values("OVERWEIGHT", ascending=False).iloc[0]
            best_age = int(row_max["AGE"])
            best_val = row_max["OVERWEIGHT"] * 100
            kpi3_value = f"{best_age}"

    # ---------- KPI 2 (nově KPI4): Gender gap in overweight (DETAIL_YEAR) ----------
    kpi4_label = "Gender gap"
    kpi4_value = "N/A"

    if not df_detail_year.empty:
        grp = (
            df_detail_year
            .groupby("SEX", as_index=False, observed=True)["OVERWEIGHT"]
            .mean()
        )

        if set(grp["SEX"]) == {1, 2}:
            boys = grp.loc[grp["SEX"] == 1, "OVERWEIGHT"].iloc[0]
            girls = grp.loc[grp["SEX"] == 2, "OVERWEIGHT"].iloc[0]
            gap = (girls - boys) * 100  # v procentech

            if abs(gap) < 0.1:
                kpi4_value = "≈ 0 %"
            elif gap > 0:
                kpi4_value = f"♀️ +{gap:.1f} %"
            else:
                kpi4_value = f"♂️ +{abs(gap):.1f} %"

    # ---------- KPI layout – nové pořadí ----------
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">OW change</div>
            <div class="kpi-value">{kpi1_value}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        # předpokládám, že máš spočítané boys_pct a girls_pct (používáš je v KPI 2)
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">OW boys / girls</div>
            <div class="kpi-value">
                <span class="gender-pill male">♂</span>{boys_pct:.0f} %
                <span class="gender-pill female">♀</span>{girls_pct:.0f} %
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">Worst age</div>
            <div class="kpi-value">{kpi3_value}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">Gender gap</div>
            <div class="kpi-value">{kpi4_value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



##############################################################
# FILTERS – budou v pravém sloupci vedle Grafu 1
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


# default values (overwritten later in UI)
selected_country = "All countries"
min_age, max_age = int(df["AGE"].min()), int(df["AGE"].max())
age_min, age_max = min_age, max_age

country_list = sorted(df["COUNTRY_NAME"].unique().tolist())


#######################################################
# DEFINING FACTORS, SCALES

# columns odpovidaji top cca 20 z radom forest modelu 
list_columns = [
    "FRUITS", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK", "TIME_EXE", "PHYS_ACT_60", "DRUNK_30", 
    "FAMILY_MEALS_TOGETHER", "BREAKFAST_WEEKDAYS", "BREAKFAST_WEEKEND", "TOOTH_BRUSHING", "STUD_TOGETHER", 
    "BUL_OTHERS", "BUL_BEEN", "FIGHT_YEAR", "INJURED_YEAR", "HEADACHE", "FEEL_LOW", "NERVOUS", "SLEEP_DIF", "DIZZY",
    "TALK_MOTHER", "TALK_FATHER", "LIKE_SCHOOL", "SCHOOL_PRESSURE", "COMPUTER_NO"
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

# ty factors kde v source data vyssi hodnota= zdravejsi (5 nikdy headache, 6 snidane kazdy den, 7 hodne sportuje -> reverse aby max= nejhorsi/nejmene zdravy)
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


########################################################
# NORMALIZACE 0-1:
# - výsledek 0 (min) = nejlepší (zdravější)
# - výsledek 1 (max) = nejhorší (rizikovost)

def prep_df_normalized_for_year(df_input, year):
    # Vrátí DF jen pro rok 2018 + normalizované faktory 0-1,
    # kde 0 ~ nejzdravější, 1 ~ nejrizikovější.
    df_year = df_input[df_input["YEAR"] == year].copy()
    for factor in list_columns:
        df_year[factor] = df_year[factor] / dict_scales[factor]
        if factor in reverse_scales:
            df_year[factor] = 1 - df_year[factor]
    return df_year

DETAIL_YEAR = 2018



##########################################################
# GRAPH 1 - Overweight overview in time - Boys vs Girls

fig1 = fig2 = fig3 = fig4 = fig5 = fig6 = None

if not df_filtered.empty:
    df_trend = (
        df_filtered
        .groupby(["YEAR", "SEX"], as_index=False, observed=True)["OVERWEIGHT"]
        .mean()
    )

    df_trend["SEX_LABEL"] = df_trend["SEX"].map({1: 'Boys', 2: 'Girls'})
    colors = {'Girls': "#eb8fbd", 'Boys': "#3b8ee1"}

    fig1 = px.line(
        df_trend, 
        y="OVERWEIGHT", 
        x="YEAR", 
        color="SEX_LABEL", 
        color_discrete_map=colors
    )

    fig1.update_yaxes(range=[0, 0.5])
    fig1.update_xaxes(tickvals=[2002, 2006, 2010, 2014, 2018])
    fig1.update_traces(fill="tozeroy")

    fig1.update_layout(
    xaxis_title="Year",
    yaxis_title="Overweight prevalence (0-1)",
    legend_title="Gender",
    title=dict(
        text="Overweight Trend by Gender (2002-2018)",
        font=dict(size=24)
    ),
    margin=dict(l=80, r=40, t=60, b=60)  
    )

#Layout graph1
with row1_col1:
    if fig1 is not None:
        st.plotly_chart(fig1, use_container_width=True, key="fig1")
    else:
        st.info("Graph 1 not available for current filters.")



########################################################
# GRAPH 2 – Top 5 faktorů (podle korelace), rozdíl Boys vs Girls (OW only, 2018)
# KORELACE faktorů s OVERWEIGHT (2018, normované df_2018_normalized)
# prep for Graph 3 (top 5)
df_norm_detail = prep_df_normalized_for_year(df_filtered, DETAIL_YEAR)

df_filtered = df.copy()

if selected_country != "All countries":
    df_filtered = df_filtered[df_filtered["COUNTRY_NAME"] == selected_country]

df_filtered = df_filtered[
    (df_filtered["AGE"] >= age_min) &
    (df_filtered["AGE"] <= age_max)
]


if not df_norm_detail.empty:
    corr_series = (
        df_norm_detail[list_columns + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
    )

    corr_abs = corr_series.abs()
    top5_corr = corr_abs.sort_values(ascending=False).head(5).index.tolist()

    df_ow_detail = df_norm_detail[df_norm_detail["OVERWEIGHT"] == 1].copy()

    if not df_ow_detail.empty:
        sex_means = (
            df_ow_detail
            .groupby("SEX", as_index=False, observed=True)[top5_corr]
            .mean()
        )

        # long form pro plotly
        sex_means_long = sex_means.melt(
            id_vars=["SEX"],
            value_vars=top5_corr,
            var_name="FACTOR",
            value_name="VALUE"
        )

        sex_means_long["SEX_STRING"] = sex_means_long["SEX"].map({1: "Boys", 2: "Girls"})

        sex_means_long["FACTOR_LABEL"] = sex_means_long["FACTOR"].map(factor_alias)
        factor_order_top5 = [f for f in top5_corr] 
        factor_order_top5_labels = [
            factor_alias.get(f, f) for f in factor_order_top5
        ]


        # tabulka pro výpočet gender gapu (Girls - Boys)
        gap_table = (
            sex_means_long
            .pivot_table(
                index="FACTOR",
                columns="SEX_STRING",
                values="VALUE"
            )
        )

    gap_table["GIRLS_MINUS_BOYS"] = gap_table["Girls"] - gap_table["Boys"]
    factor_order_top5 = top5_corr 

    colors = {"Boys": "#3b8ee1", "Girls": "#eb8fbd"}

    fig2 = px.bar(
        sex_means_long,
        x="VALUE",
        y="FACTOR_LABEL",
        color="SEX_STRING",
        orientation="h",
        barmode="group",
        category_orders={"FACTOR_LABEL": factor_order_top5_labels},
        color_discrete_map=colors,
        title=f"Top 5 Risk Factors by Gender (Overweight children, {DETAIL_YEAR}, normalized 0-1)"
    )

    fig2.update_layout(
        xaxis_title="Average risk (0-1)",
        yaxis_title="Risk factor",
        legend_title="Gender",
        title=dict(
                text=f"Top 5 Risk Factors by Gender ({DETAIL_YEAR})",
                font=dict(size=24)
            )
    )


##########################################################
# GRAPH 3 – gender gap by factor (Girls − Boys) z df_2018_normalized
# seřazeno od "nejvíc holky" po "nejvíc kluci"

if not df_norm_detail.empty and  "top5_corr" in locals():
    remaining_factors = [f for f in list_columns if f not in top5_corr]
    # jen overweight děti
    df_ow_detail = df_ow_detail[df_ow_detail["OVERWEIGHT"] == 1].copy()

    if not df_ow_detail.empty and remaining_factors:
    # průměry podle pohlaví
        sex_means_all = (
            df_ow_detail
            .groupby("SEX", as_index=False, observed=True)[remaining_factors]
            .mean()
        )
        sex_long_all = sex_means_all.melt(
            id_vars=["SEX"],
            value_vars=remaining_factors,
            var_name="FACTOR",
            value_name="VALUE"
        )
        sex_long_all["SEX_STRING"] = sex_long_all["SEX"].map({1: "Boys", 2: "Girls"})
        # tabulka gender gapu
        gap_table_rest = (
            sex_long_all
            .groupby(["FACTOR", "SEX_STRING"], observed=True)["VALUE"]
            .mean()
            .unstack("SEX_STRING")
        )
        gap_table_rest["GIRLS_MINUS_BOYS"] = gap_table_rest["Girls"] - gap_table_rest["Boys"]
        
        df_gap = gap_table_rest.reset_index()
        # pořadí faktorů podle gender gapu:
        # nejdřív holky horší (nejvyšší +), pak až kluci (nejnižší −)
        factor_order = (
            df_gap
            .sort_values("GIRLS_MINUS_BOYS", ascending=False)["FACTOR"]
            .tolist()
        )

        df_gap["FACTOR_LABEL"] = df_gap["FACTOR"].map(factor_alias)
        factor_order_labels = [
            factor_alias.get(f, f) for f in factor_order
            ]

        # kdo má vyšší průměr (jen pro barvu)
        df_gap["SIDE"] = np.where(
            df_gap["GIRLS_MINUS_BOYS"] > 0,
            "Girls",
            "Boys"
        )

        color_gap = {
            "Girls": "#eb8fbd",
            "Boys": "#3b8ee1"
        }

        # pro symetrickou osu si můžeme spočítat min/max
        #y_min = df_gap["GIRLS_MINUS_BOYS"].min()
        #y_max = df_gap["GIRLS_MINUS_BOYS"].max()
        #pad   = 0.05 * max(abs(y_min), abs(y_max))

        fig3 = px.bar(
            df_gap,
            x="FACTOR_LABEL",
            y="GIRLS_MINUS_BOYS",
            color="SIDE",
            color_discrete_map=color_gap,
            category_orders={"FACTOR_LABEL": factor_order_labels},
            title=f"Gender Gap Across Risk Factors (Overweight children, ({DETAIL_YEAR})"
        )

        fig3.update_layout(
            xaxis_title="Risk factor",
            yaxis_title="Girls - Boys (difference)",
            legend_title="Group with higher risk",
            xaxis=dict(tickangle=-40),
            yaxis=dict(
                tickmode="linear",
                tick0=0,
                dtick=0.05,          # krok mezi linkami
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
            
                
        
##########################################################
# GRAPH 4 – Overweight by Age and Gender (AGE on X, detail year, ignores age filter)

# data jen podle země + detailní rok
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
        yaxis_title="Overweight prevalence (0-1)",
        legend_title="Gender",
        title=dict(font=dict(size=24)),
        margin=dict(l=80, r=40, t=60, b=60)
    )

#######################################################
# GRAPH 5
# Overweight vs Non-overweight - risk factors via average difference
# DETAIL_YEAR, all genders together


if not df_norm_detail.empty:
    # bez gender filtru – bereme všechny děti v aktuálních filtrech
    df_fig5 = df_norm_detail.copy()

    df_ow_all  = df_fig5[df_fig5["OVERWEIGHT"] == 1]
    df_non_all = df_fig5[df_fig5["OVERWEIGHT"] == 0]

    if not df_ow_all.empty and not df_non_all.empty:
        ow_means  = df_ow_all[list_columns].mean()
        non_means = df_non_all[list_columns].mean()
        diff = ow_means - non_means

        df_diff = (
            diff.rename("DIFFERENCE")
                .reset_index()
                .rename(columns={"index": "FACTOR"})
        )
        df_diff["DIFFERENCE"] = df_diff["DIFFERENCE"].fillna(0.0)
        df_diff["ABS_DIFF"] = df_diff["DIFFERENCE"].abs()

        # seřadit podle velikosti rozdílu (největší rozdíl nahoře)
        df_diff = df_diff.sort_values("ABS_DIFF", ascending=False)

        df_diff["FACTOR_LABEL"] = df_diff["FACTOR"].map(factor_alias)

        df_diff["SIDE"] = np.where(
            df_diff["DIFFERENCE"] > 0,
            "Overweight",
            "Non-overweight"
        )

        color_ow = {
            "Overweight": "orangered",
            "Non-overweight": "seagreen"
        }

        fig5 = px.bar(
            df_diff,
            x="DIFFERENCE",
            y="FACTOR_LABEL",
            orientation="h",
            color="SIDE",
            color_discrete_map=color_ow,
            category_orders={"FACTOR_LABEL": df_diff["FACTOR_LABEL"].tolist()},
            title=f"Overweight vs Non-overweight Differences ({DETAIL_YEAR})",
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
            height=450,
            margin=dict(l=140, r=40, t=60, b=60),
            title=dict(
                text=f"Overweight vs Non-overweight Differences ({DETAIL_YEAR})",
                font=dict(size=24)
            )
        )

#####################################################
# DASHBOARD LAYOUT

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    if fig2 is not None:
        st.plotly_chart(fig2, use_container_width=True, key="fig2")
    else:
        st.info("Graph 2 not available for current filters.")
with row2_col2:
    if fig3 is not None:
        st.plotly_chart(fig3, use_container_width=True, key="fig3")
    else:
        st.info("Graph 3 not available for current filters.")



row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    if fig4 is not None:
        st.plotly_chart(fig4, use_container_width=True, key="fig4")
    else:
        st.info("Graph 4 not available for current filters.")
with row3_col2:
    if fig5 is not None:
        st.plotly_chart(fig5, use_container_width=True, key="fig5")
    else:
        st.info("Graph 5 not available for current filters.")





