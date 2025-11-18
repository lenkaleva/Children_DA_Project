import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "vscode"
px.defaults.template = "plotly"
import plotly.graph_objects as go

df = pd.read_csv("data.csv")

df_filter = df.groupby(["YEAR", "SEX"], as_index=False)["OVERWEIGHT"].mean()

df_filter['SEX'] = df_filter['SEX'].map({2: 'Girls', 1: 'Boys'})
colors = {'Girls': "#eb8fbd", # pink
'Boys': "#3b8ee1"} # blue

fig = px.line(df_filter, y="OVERWEIGHT", x="YEAR", title="Overweight in Time", color="SEX", color_discrete_map=colors)
fig.update_yaxes(range=[0, 0.5])
fig.update_xaxes(tickvals=[2002, 2006, 2010, 2014, 2018])
fig.update_traces(fill="tozeroy")
fig.show()

