import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "vscode"
px.defaults.template = "plotly"
import plotly.graph_objects as go


#########################################################
# STREAMLIT PAGE SETUP

st.set_page_config(
    page_title="Gender Dashboard",  
    layout="wide",  
)

st.title("Gender Dashboard")


###########################################################
# LOADING DATA
# already loaded on app.py - using df for convenience

if "data" not in st.session_state:
    st.session_state.data = pd.read_csv('data.csv')

df = st.session_state.data



##############################################################
# FILTERS at SIDEBAR
# Country, Year, Age

country_list = sorted(df["COUNTRY_NAME"].unique().tolist())
years_list = sorted(df['YEAR'].unique().tolist())
age_list = sorted(df["AGE"].unique().tolist())


# defining sidebar via context manager with st.sidebar
# # st.selectbox (label , options= to choose from, index=..) 
with st.sidebar:
    st.sidebar.title("📚 Menu")
    selected_country = st.selectbox(
        'Select Country', 
        options = ['All'] + country_list
    )
    selected_years = st.multiselect(
        'Select years', 
        options = years_list, 
        default = years_list
    )
    selected_age = st.multiselect(
        'Select age',
        options = age_list,
        default = age_list
    )

filters = {
    "COUNTRY_NAME": None if selected_country == 'All' else selected_country,
    "YEAR": None if set(selected_years) == set(years_list) else selected_years,
    "AGE": None if set(selected_age) == set(age_list) else selected_age
}
    

###############################################




# columns odpovidaji top cca 20 z radom forest modelu + talk_mother pridan jako protipol talk_father
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

# ty factors kde vyssi hodnota = zdravejsi (5 nikdy headache, 6 snidane kazdy den, 7 hodne sportuje -> reverse aby max nejhorsi/nejmene zdravy)
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

# Normalizace 0-1:
    # - výsledek 0 (min) = nejlepší (zdravější)
    # - výsledek 1 (max) = nejhorší (rizikovost)

def make_df_2018_norm(df_in):
    # Vrátí DF jen pro rok 2018 + normalizované faktory 0-1,
    # kde 0 ~ nejzdravější, 1 ~ nejrizikovější.
    df_2018 = df_in[df_in["YEAR"] == 2018].copy()
    for col in list_columns:
        df_2018[col] = df_2018[col] / dict_scales[col]
        if col in reverse_scales:
            df_2018[col] = 1 - df_2018[col]
    return df_2018

df_2018_norm = make_df_2018_norm(st.session_state.data)





# GRAPH 1 - Overweight overview in time - Boys vs Girls

df_trend = st.session_state.data.groupby(["YEAR", "SEX"], as_index=False)["OVERWEIGHT"].mean()

df_trend['SEX'] = df_trend['SEX'].map({2: 'Girls', 1: 'Boys'})
colors = {'Girls': "#eb8fbd", # pink
'Boys': "#3b8ee1"} # blue

fig1 = px.line(df_trend, y="OVERWEIGHT", x="YEAR", title="Overweight in Time", color="SEX", color_discrete_map=colors)
fig1.update_yaxes(range=[0, 0.5])
fig1.update_xaxes(tickvals=[2002, 2006, 2010, 2014, 2018])
fig1.update_traces(fill="tozeroy")

fig1.update_layout(
    xaxis_title="Year",
    yaxis_title="Overweight (0-1)",
    legend_title="Gender"
)


# -----------------------------------------
# GRAPH 2
# korelace faktorů s OVERWEIGHT (2018, normované df_2018_norm)
corr_series = (
    df_2018_norm[list_columns + ["OVERWEIGHT"]]
    .corr()["OVERWEIGHT"]
    .drop("OVERWEIGHT")
)

corr_abs = corr_series.abs()

top5_corr = corr_abs.sort_values(ascending=False).head(5).index.tolist()
print("TOP 5 podle |korelace s OW|:", top5_corr)


# -----------------------------------------
# GRAPH 3 – gender gap by factor (Girls − Boys)
# seřazeno od "nejvíc holky" po "nejvíc kluci"
# -----------------------------------------

# faktory, které NEJSOU v grafu 2
remaining_factors = [f for f in list_columns if f not in top5_corr]

# jen overweight děti
df_ow_2018 = df_2018_norm[df_2018_norm["OVERWEIGHT"] == 1].copy()

# průměry podle pohlaví
sex_means_all = (
    df_ow_2018
    .groupby("SEX", as_index=False)[remaining_factors]
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
    .groupby(["FACTOR", "SEX_STRING"])["VALUE"]
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

fig3 = px.bar(
    df_gap,
    x="FACTOR",
    y="GIRLS_MINUS_BOYS",
    color="SIDE",
    color_discrete_map=color_gap,
    category_orders={"FACTOR": factor_order},
    title="Gender Gap by Risk Factor"
)

fig3.update_layout(
    xaxis_title="Risk factor",
    yaxis_title="Gender gap (Girls − Boys, scaled 0–1)",
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


### SETTING DASHBOARD STUCTURE

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
# Violin Plot
with col2:
    st.plotly_chart(fig3, use_container_width=True)

