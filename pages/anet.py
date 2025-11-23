import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



#########################################################
# STREAMLIT PAGE SETUP

st.title("Gender Dashboard")
st.set_page_config(layout="wide")

###########################################################
# LOADING DATA
# already loaded on app.py - using df for convenience

if "data" not in st.session_state:
    st.session_state.data = pd.read_csv('data.csv')

df = st.session_state.data



##############################################################
# FILTERS
# Country, Age

country_list = sorted(df["COUNTRY_NAME"].unique().tolist())
age_list = sorted(df["AGE"].unique().tolist())

st.markdown("### Filters")

column_country, column_age = st.columns(2)

# Country filter
with column_country:
    country_options = ["All countries"] + country_list
    selected_country = st.selectbox(
        "Select country",
        options=country_options,
        index=0
    )
    
# Age filter
with column_age:
    age_options = ["All ages"] + age_list
    selected_age = st.selectbox(
        "Select age",
        options=age_options,
        index=0  # default = All ages
    )

df_filtered = df.copy() 

if selected_country != "All countries":
    df_filtered = df_filtered[df_filtered["COUNTRY_NAME"] == selected_country]

if selected_age != "All ages":
    df_filtered = df_filtered[df_filtered["AGE"] == selected_age]
    
    
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

def prep_df_2018_normalized(df_input):
    # Vrátí DF jen pro rok 2018 + normalizované faktory 0-1,
    # kde 0 ~ nejzdravější, 1 ~ nejrizikovější.
    df_2018 = df_input[df_input["YEAR"] == 2018].copy()
    for factor in list_columns:
        df_2018[factor] = df_2018[factor] / dict_scales[factor]
        if factor in reverse_scales:
            df_2018[factor] = 1 - df_2018[factor]
    return df_2018


##########################################################
# GRAPH 1 - Overweight overview in time - Boys vs Girls

fig1 = fig2 = fig3 = fig4 = None

if df_filtered.empty:
    st.warning("No data for selected filters.")
else:
    df_2018_normalized = prep_df_2018_normalized(df_filtered)
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
        title="Overweight in Time", 
        color="SEX_LABEL", 
        color_discrete_map=colors
    )

    fig1.update_yaxes(range=[0, 0.5])
    fig1.update_xaxes(tickvals=[2002, 2006, 2010, 2014, 2018])
    fig1.update_traces(fill="tozeroy")

    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Overweight (0-1)",
        legend_title="Gender"
    )
#if fig1 is not None:
    #st.plotly_chart(fig1, use_container_width=True)


########################################################
# GRAPH 2
# Overweight vs Non-overweight - risk factors via average difference

fig2 = None 

if df_2018_normalized.empty:
    st.info("No data with selected filters.")
else:
    df_ow_all  = df_2018_normalized[df_2018_normalized["OVERWEIGHT"] == 1]
    df_non_all = df_2018_normalized[df_2018_normalized["OVERWEIGHT"] == 0]

    if df_ow_all.empty or df_non_all.empty:
        st.info("Not enough data for both overweight and non-overweight groups.")
    else:
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
            "Overweight higher",
            "Non-overweight higher"
        )

        color_ow = {
            "Overweight higher": "orangered",
            "Non-overweight higher": "seagreen"
        }

        fig2 = px.bar(
            df_diff,
            x="DIFFERENCE",
            y="FACTOR",
            orientation="h",
            color="SIDE",
            color_discrete_map=color_ow,
            category_orders={"FACTOR": df_diff["FACTOR"].tolist()},
            title="Top behaviour differences (Overweight - Non-overweight, 2002-2018, normalized 0-1)",
        )

        fig2.update_layout(
            xaxis_title="Difference (OW - Non-OW, normalized 0-1; >0 = OW worse)",
            yaxis_title="Factor",
            legend_title="Higher risk in",
            xaxis=dict(
                zeroline=True,
                zerolinecolor="black",
                zerolinewidth=1.5
            ),
            height=450,
            margin=dict(l=140, r=40, t=60, b=60),
        )



########################################################
# GRAPH 3 – Top 5 faktorů (podle korelace), rozdíl Boys vs Girls (OW only, 2018)
# KORELACE faktorů s OVERWEIGHT (2018, normované df_2018_normalized)
# prep for Graph 3 (top 5)

if not df_2018_normalized.empty:
    corr_series = (
        df_2018_normalized[list_columns + ["OVERWEIGHT"]]
        .corr()["OVERWEIGHT"]
        .drop("OVERWEIGHT")
    )

    corr_abs = corr_series.abs()
    top5_corr = corr_abs.sort_values(ascending=False).head(5).index.tolist()

    df_ow_2018 = df_2018_normalized[df_2018_normalized["OVERWEIGHT"] == 1].copy()

    if not df_ow_2018.empty:
        sex_means = (
            df_ow_2018
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
    gap_table["ABS_GAP"] = gap_table["GIRLS_MINUS_BOYS"].abs()

    # pořadí faktorů podle velikosti rozdílu (největší gap nahoře)
    factor_order_top5 = (
        gap_table
        .sort_values("ABS_GAP", ascending=False)
        .index
        .tolist()
    )

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
        title="Top 5 faktorů podle korelace s overweight - Boys vs Girls (OW only, 2018)"
    )

    fig3.update_layout(
        xaxis_title="Average (normalized 0-1, higher = worse)",
        yaxis_title="Risk factor",
        legend_title="Gender"
    )

#st.plotly_chart(fig3, use_container_width=True)


##########################################################
# GRAPH 4 – gender gap by factor (Girls − Boys) z df_2018_normalized
# seřazeno od "nejvíc holky" po "nejvíc kluci"

if not df_2018_normalized.empty and fig3 is not None:
    remaining_factors = [f for f in list_columns if f not in top5_corr]
    # jen overweight děti
    df_ow_2018 = df_2018_normalized[df_2018_normalized["OVERWEIGHT"] == 1].copy()
    if not df_ow_2018.empty and remaining_factors:
    # průměry podle pohlaví
        sex_means_all = (
            df_ow_2018
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
        y_min = df_gap["GIRLS_MINUS_BOYS"].min()
        y_max = df_gap["GIRLS_MINUS_BOYS"].max()
        pad   = 0.05 * max(abs(y_min), abs(y_max))

        fig4 = px.bar(
            df_gap,
            x="FACTOR",
            y="GIRLS_MINUS_BOYS",
            color="SIDE",
            color_discrete_map=color_gap,
            category_orders={"FACTOR": factor_order},
            title="Gender Gap by Risk Factor"
        )

        fig4.update_layout(
            xaxis_title="Risk factor",
            yaxis_title="Gender gap (Girls - Boys, scaled 0-1)",
            legend_title="Higher risk in",
            xaxis=dict(tickangle=-40),
            yaxis=dict(
                zeroline=True,
                zerolinecolor="black",
                zerolinewidth=1.5,
                range=[y_min - pad, y_max + pad]
            ),
            height=500,
            margin=dict(l=80, r=40, b=120)
        )

    #st.plotly_chart(fig4, use_container_width=True)


#####################################################
# DASHBOARD LAYOUT

st.markdown("### Dashboard")

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




