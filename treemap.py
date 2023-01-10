import plotly.express as px
import pandas as pd
import plotly

df = pd.read_excel('cleaned_data_treemap.xlsx')

title = df['title']
year = df['year']
certificate = df['certificate']
duration = df['duration']
genre = df['genre']
rating = df['rating']
description = df['description']
stars = df['stars']
votes = df['votes']


fig = px.treemap(df,
                path=[px.Constant("movies"), 'year', 'title'],
                values=year,
                color=year,
                color_continuous_scale=['yellow', 'green', 'blue'],
                title='Movie releases by year',
                hover_name=title
)

fig.update_layout(
                title_font_size=42,
                title_font_family='Arial'
)
plotly.offline.plot(fig, filename='treemap.html')
