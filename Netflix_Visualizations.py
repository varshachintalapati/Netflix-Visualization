import altair as alt
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px # interactive charts
import streamlit as st  #data web app development
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image



cleandata = pd.read_csv('cleaned_data.csv')
cleandata = cleandata.reset_index()
cleandata['genre'] = cleandata['main_genre']
cleandata=cleandata.drop(columns=["right"], axis = 1)
cleandata=cleandata.drop(columns=["middle"], axis = 1)
cleandata=cleandata.drop(columns=["main_genre"], axis = 1)
df = pd.read_excel('cleaned_data_treemap.xlsx')

st.set_page_config(
    page_title='Netflix Data Analysis Dashboard',
    page_icon=":popcorn",
    layout="wide",
)

# dashboard title
title_container = st.container()
col1, col2 = st.columns([1, 20])
image = Image.open('netflixlogo.png')
with title_container:
            with col1:
                st.image(image, width=80)
            with col2:
                st.markdown('<h1 style="color: red;">&nbsp; Netflix Data Analysis Dashboard</h1>',
                            unsafe_allow_html=True)


show_choice = st.multiselect('Which Movie or TV show do you want to display data for?', cleandata['title'].unique())
if show_choice:
    st.success('Yay! 🎉')
else:
    st.warning('No option is selected')
    pass

if show_choice:
    selected_description = cleandata[cleandata['title'] == show_choice[0]]
    st.markdown("Detailed Data View for selected show")
    st.write(selected_description[['title','year','certificate','duration','genre','rating','description','stars','votes']])

# top-level filters
year_filter = st.selectbox("Select the Year", pd.unique(cleandata['year']))

placeholder = st.empty()

cleandata = cleandata[cleandata['year'] == year_filter]

with placeholder.container():
    # create three columns
    k1, k2, k3= st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    k1.metric(
        label="Duration",
        value=str(round(cleandata['duration'].mean())) + ' mins',
        delta = cleandata['duration'].max()
    )

    k2.metric(
        label="Votes Count",
        value=str(int(cleandata['votes'].count())) + ' K'
    )
    k3.metric(
        label="Ratings",
        value=int(cleandata['rating'].max()),
        delta = 9.9
    )

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("Density Heat Map for TV shows Genre and Rating")
        fig1 = px.density_heatmap(
            data_frame=cleandata, y="rating", x="genre"
        )
        st.write(fig1)
    
    with fig_col2:
        st.markdown("Count of TV shows by their certificate type")
        fig2 = px.histogram(data_frame=cleandata, x="genre",y=None,color_discrete_sequence = ['orange']).update_xaxes(categoryorder="total ascending")
        st.write(fig2)


grp_by_certificate = cleandata.groupby("certificate")["title"].count()
grp_by_certificate = grp_by_certificate.reset_index()

fig1, fig2 = st.columns(2)

with fig1:
    bar = alt.Chart(grp_by_certificate).mark_bar().encode(
        x=alt.X('certificate', sort='y'),
        y=alt.Y('title', title = 'count')
        ).properties(height = 400, width = 600
        ).interactive()
    st.write(bar)
with fig2:
    grp_by_certificate
    

# Bar Chart


st.title('Word Cloud showing the most popular stars of Netflix TV shows')
st.set_option('deprecation.showPyplotGlobalUse', False)
wordcloud = WordCloud().generate(str(cleandata['stars']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot()

title = df['title']
year = df['year']
#certificate = df['certificate']
#duration = df['duration']
#genre = df['genre']
#rating = df['rating']
description = df['description']
#stars = df['stars']
#votes = df['votes']


year_df = df[df['year'] == year_filter]
fig = px.treemap(year_df,
                path=[px.Constant("movies"), 'year', 'title','description'],
                values=year_df['year'],
                #color=year_df['year'],
                color_continuous_scale=['yellow', 'green', 'blue'],
                title='TreeMap displaying Movie releases by selected year',
                hover_name=year_df['description'],
                width = 1400,
                height = 800
)

fig.update_layout(
                title_font_size=42,
                title_font_family='Arial'


)

st.plotly_chart(fig)
    
