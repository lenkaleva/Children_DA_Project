import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



#########################################################
# STREAMLIT PAGE SETUP

st.title("Gender Differences in Childhood Overweight")
st.set_page_config(layout="wide")

###########################################################
# LOADING DATA
# already loaded on app.py - using df for convenience
if 'data' not in st.session_state:
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


##############################################################
# FILTERS
# Country, Age

country_list = sorted(df["COUNTRY_NAME"].unique().tolist())

column_country, column_age, column_year = st.columns(3)

# Country filter
with column_country:
    country_options = ["All countries"] + country_list
    selected_country = st.selectbox(
        "Select country",
        options=country_options,
        index=0
    )
    
# Age filter
min_age, max_age = int(df["AGE"].min()), int(df["AGE"].max())

with column_age:
    age_min, age_max = st.slider(
    "Select age",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age),
    step=1
)
    
# Year filter – detail year for KPIs & detail graphs
with column_year:
    year_options = sorted(df["YEAR"].unique().tolist())
    year_labels = ["All years"] + [str(y) for y in year_options]
    selected_year_label = st.selectbox(
        "Select year for KPIs",
        options=year_labels,
        index=0  # default = All years
    )
    if selected_year_label == "All years":
        # detailní rok = nejnovější rok v datech
        DETAIL_YEAR = max(year_options)
    else:
        DETAIL_YEAR = int(selected_year_label)
    

df_filtered = df.copy() 

if selected_country != "All countries":
    df_filtered = df_filtered[df_filtered["COUNTRY_NAME"] == selected_country]

df_filtered = df_filtered[
    (df_filtered["AGE"] >= age_min) &
    (df_filtered["AGE"] <= age_max)
]
    

#######################################################
# DEFINING FACTORS, SCALES

# columns odpovidaji top cca 20 z radom forest modelu 
list_columns = [
    "SWEETS", 
    "TOOTH_BRUSHING", 
    "BREAKFAST_WEEKDAYS", 
    "BREAKFAST_WEEKEND", 
    "SOFT_DRINKS", 
    "PHYS_ACT_60", 
    "NERVOUS", 
    "FRUITS", 
    "VEGETABLES", 
    "TALK_FATHER",
    "TALK_MOTHER", 
    "FRIEND_TALK", 
    "SLEEP_DIF", 
    "TIME_EXE", 
    "FIGHT_YEAR", 
    "HEADACHE", 
    "BUL_BEEN",
    "FAMILY_MEALS_TOGETHER"
]
    
dict_scales = {
    # Symptomy (1=bad → 5=good)
    "HEADACHE": 5,
    "NERVOUS": 5,
    "SLEEP_DIF": 5,
    "FEEL_LOW": 5,
    "STOMACHACHE": 5,
    "DIZZY": 5,
    # Komunikace s rodiči (1=good → 5=bad)
    "TALK_FATHER": 5,
    "TALK_MOTHER": 5,
    "FAMILY_MEALS_TOGETHER": 5,
    # Životní návyky (1=good → max=bad)
    "TIME_EXE": 7,
    "TOOTH_BRUSHING": 5,
    "HEALTH": 4,
    "LIKE_SCHOOL": 4,
    "STUD_TOGETHER": 5,
    # Strava & životní styl
    "FRUITS": 7,
    "VEGETABLES": 7,
    "FRIEND_TALK": 7,
    "BREAKFAST_WEEKDAYS": 5,
    "BREAKFAST_WEEKEND": 3,
    "PHYS_ACT_60": 7,
    "LIFESAT": 10,
    # Rizikové chování
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


########################################################
# KPI BLOCK

if df_filtered.empty:
    st.warning("No data for selected filters.")
else:
    # roky v aktuálním filtru
    years_available = sorted(df_filtered["YEAR"].unique().tolist())
    base_year = years_available[0]

    # data jen pro DETAIL_YEAR – použijeme v KPI 2–4
    df_detail_year = df_filtered[df_filtered["YEAR"] == DETAIL_YEAR].copy()

    # ---------- KPI 1: Overweight change (base_year -> DETAIL_YEAR) ----------
    overall_detail = df_detail_year["OVERWEIGHT"].mean()
    overall_base = df_filtered[df_filtered["YEAR"] == base_year]["OVERWEIGHT"].mean()

    kpi1_label = "OW change"
    if pd.notna(overall_base) and pd.notna(overall_detail):
        diff_pct = (overall_detail - overall_base) * 100
        kpi1_value = f"{diff_pct:+.1f}%"
    else:
        kpi1_value = "N/A"
    # ---------- KPI 2: Gender gap in overweight (DETAIL_YEAR) ----------
    kpi2_label = "Gender gap"
    kpi2_value = "N/A"

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
                kpi2_value = "≈ 0 %"
            elif gap > 0:
                kpi2_value = f"♀️ +{gap:.1f}%"
            else:
                kpi2_value = f"♂️ +{abs(gap):.1f}%"


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
            kpi3_value = f"{best_age} yrs: {best_val:.1f}%"


    # ---------- KPI 4: Gender split among children with overweight (DETAIL_YEAR) ----------
    kpi4_label = "OW boys / girls"
    kpi4_value = "N/A"

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
                kpi4_value = f"♂️ {boys_pct:.0f}% ♀️ {girls_pct:.0f}%"

    # KPI layout
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric(kpi1_label, kpi1_value)
    with kpi_col2:
        st.metric(kpi2_label, kpi2_value)
    with kpi_col3:
        st.metric(kpi3_label, kpi3_value)
    with kpi_col4:
        st.metric(kpi4_label, kpi4_value)


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
        title="Overweight Trend by Gender (2002-2018)", 
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



########################################################
# GRAPH 2
# Overweight vs Non-overweight - risk factors via average difference
# detail year

########################################################
# GRAPH 2
# Overweight vs Non-overweight - risk factors via average difference
# DETAIL_YEAR, all genders together

df_norm_detail = prep_df_normalized_for_year(df_filtered, DETAIL_YEAR)

if not df_norm_detail.empty:
    # bez gender filtru – bereme všechny děti v aktuálních filtrech
    df_fig2 = df_norm_detail.copy()

    df_ow_all  = df_fig2[df_fig2["OVERWEIGHT"] == 1]
    df_non_all = df_fig2[df_fig2["OVERWEIGHT"] == 0]

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

        df_diff["SIDE"] = np.where(
            df_diff["DIFFERENCE"] > 0,
            "Overweight",
            "Non-overweight"
        )

        color_ow = {
            "Overweight": "orangered",
            "Non-overweight": "seagreen"
        }

        fig2 = px.bar(
            df_diff,
            x="DIFFERENCE",
            y="FACTOR",
            orientation="h",
            color="SIDE",
            color_discrete_map=color_ow,
            category_orders={"FACTOR": df_diff["FACTOR"].tolist()},
            title=f"Overweight vs Non-overweight Differences ({DETAIL_YEAR})",
        )

        fig2.update_layout(
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



########################################################
# GRAPH 3 – Top 5 faktorů (podle korelace), rozdíl Boys vs Girls (OW only, 2018)
# KORELACE faktorů s OVERWEIGHT (2018, normované df_2018_normalized)
# prep for Graph 3 (top 5)

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

    fig3 = px.bar(
        sex_means_long,
        x="VALUE",
        y="FACTOR",
        color="SEX_STRING",
        orientation="h",
        barmode="group",
        category_orders={"FACTOR": factor_order_top5},
        color_discrete_map=colors,
        title=f"Top 5 Risk Factors by Gender (Overweight children, {DETAIL_YEAR}, normalized 0-1)"
    )

    fig3.update_layout(
        xaxis_title="Average risk (0-1)",
        yaxis_title="Risk factor",
        legend_title="Gender",
        title=dict(
                text=f"Top 5 Risk Factors by Gender ({DETAIL_YEAR})",
                font=dict(size=24)
            )
    )


##########################################################
# GRAPH 4 – gender gap by factor (Girls − Boys) z df_2018_normalized
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

        fig4 = px.bar(
            df_gap,
            x="FACTOR",
            y="GIRLS_MINUS_BOYS",
            color="SIDE",
            color_discrete_map=color_gap,
            category_orders={"FACTOR": factor_order},
            title=f"Gender Gap Across Risk Factors (Overweight children, ({DETAIL_YEAR})"
        )

        fig4.update_layout(
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
# GRAPH 5 – Overweight by Age and Gender (AGE on X, detail year, ignores age filter)

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

    fig5 = px.line(
        df_age_trend,
        x="AGE",
        y="OVERWEIGHT",
        color="SEX_LABEL",
        markers=True,
        color_discrete_map=colors,
        title=f"Overweight by Age and Gender ({DETAIL_YEAR})"
    )
    fig5.update_layout(
        xaxis_title="Age",
        yaxis_title="Overweight prevalence (0-1)",
        legend_title="Gender",
        title=dict(font=dict(size=24)),
        margin=dict(l=80, r=40, t=60, b=60)
    )


##########################################################
# GRAPH 6 – Risk pyramid by risk count (OW only, detail year)

fig6 = None

df_norm_pyr = prep_df_normalized_for_year(df_filtered, DETAIL_YEAR)
df_norm_pyr = df_norm_pyr[df_norm_pyr["OVERWEIGHT"] == 1]

if not df_norm_pyr.empty:
    threshold = 0.6
    df_norm_pyr = df_norm_pyr.copy()
    df_norm_pyr["RISK_COUNT"] = (df_norm_pyr[list_columns] > threshold).sum(axis=1)

    dist = (
        df_norm_pyr
        .groupby(["SEX", "RISK_COUNT"], observed=True)
        .size()
        .reset_index(name="COUNT")
    )

    if not dist.empty:
        dist["TOTAL"] = dist.groupby("SEX")["COUNT"].transform("sum")
        dist["SHARE"] = dist["COUNT"] / dist["TOTAL"]
        dist["SEX_LABEL"] = dist["SEX"].map({1: "Boys", 2: "Girls"})

        # pro pyramidový efekt: Girls na záporné straně, Boys na kladné
        dist["SHARE_SIGNED"] = np.where(
            dist["SEX_LABEL"] == "Girls",
            -dist["SHARE"],
            dist["SHARE"]
        )

        fig6 = px.bar(
            dist,
            x="SHARE_SIGNED",
            y="RISK_COUNT",
            color="SEX_LABEL",
            orientation="h",
            color_discrete_map={"Boys": "#3b8ee1", "Girls": "#eb8fbd"},
            title=f"Risk Pyramid by Number of Behaviours (Overweight, {DETAIL_YEAR})"
        )

        fig6.update_layout(
            xaxis_title="Share of children (Girls left, Boys right)",
            yaxis_title=f"Number of high-risk behaviours (>{threshold})",
            legend_title="Gender",
            height=500,
            margin=dict(l=80, r=40, t=60, b=60),
            title=dict(font=dict(size=24))
        )

        # x-osa jako procenta (budou s mínusem vlevo, ale popisek to vysvětluje)
        fig6.update_xaxes(tickformat=".0%")


#####################################################
# DASHBOARD LAYOUT

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    if fig1 is not None:
         st.plotly_chart(fig1, use_container_width=True, key="fig1")
    else:
        st.info("Graph 1 not available for current filters.")
with row1_col2:
    if fig2 is not None:
        st.plotly_chart(fig2, use_container_width=True, key="fig2")
    else:
        st.info("Graph 2 not available for current filters.")

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    if fig3 is not None:
        st.plotly_chart(fig3, use_container_width=True, key="fig3")
    else:
        st.info("Graph 3 not available for current filters.")
with row2_col2:
    if fig4 is not None:
        st.plotly_chart(fig4, use_container_width=True, key="fig4")
    else:
        st.info("Graph 4 not available for current filters.")

row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    if fig5 is not None:
        st.plotly_chart(fig5, use_container_width=True, key="fig5")
    else:
        st.info("Graph 5 not available for current filters.")
with row3_col2:
    if fig6 is not None:
        st.plotly_chart(fig6, use_container_width=True, key="fig6")
    else:
        st.info("Graph 6 not available for current filters.")



