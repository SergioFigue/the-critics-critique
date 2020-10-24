import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns


#def run_streamlit(scored_texts_analytics):


def load_data():
    return pd.read_csv('../data/scored_texts_analytics.csv')


#@st.cache
scored_texts_analytics = load_data()

st.title('The Critics Critique App Presentation')


# Sidebar 1
st.sidebar.header("The Critics Critique")

st.sidebar.subheader("Do you trust critics?")
radio_list_up = ["Know the app", "Take a sample", "How critics score", "Conclusions"]
status = st.sidebar.radio("", radio_list_up, key=1)

if status == "Know the app":
    # st.success("RG data")

    st.markdown("*Would you trust this guy?*")

    my_slot1 = st.empty()

    vid_file = open("../data/media/xcloud_gamereactor.mp4", "rb").read()
    st.video(vid_file)

    time.sleep(5)
    my_slot1.error('Never!')
    st.error('Ever!')

    st.empty()

    st.subheader('What is this?')
    st.markdown("This dashboard compares how video games critics **score** a review versus "
                "the **sentiment** said review conveys to the reader according to a **pretrained BERT NLP model**.")

    st.subheader('Where data comes from?')
    st.markdown("Data was extracted scraping five video game outlets for a total of **15.551 valid reviews**. "
                "Some texts are 10 years old!")

    st.subheader('What are you trying to tell us?')
    st.markdown("My hypothesis is: **spanish reviewers overrate video games**.")

if status == "Take a sample":

    if st.checkbox("Take a look at the DataFrame"):
        st.markdown("*This is how the real score compares with the stars suggested by the model*")
        st.write(scored_texts_analytics)

    st.subheader('Run the code')

if status == "How critics score":

    from PIL import Image

    img = Image.open("../data/media/Plan Proyecto Sergio.jpg")
    st.image(img, width=450)

    st.markdown("*This is how the real score compares with the stars suggested by the model*")

    # Sidebar 2 - NLP Stars vs Scores

    st.sidebar.subheader("NLP Stars vs Scores")
    radio_list_down = ["Website", "Platform", "Author", "Company"]
    status = st.sidebar.radio("", radio_list_down, key=2)

    if status == 'Website':
        site_deviation = scored_texts_analytics.groupby('site')[['score', 'stars_mean', 'score_deviation']].mean()
        st.markdown('*Positive deviation means sentiment is better than score and vice versa*')
        st.table(site_deviation)

        sites = scored_texts_analytics['site'].unique()
        site = st.selectbox("Select a website", sites)

        df = scored_texts_analytics[scored_texts_analytics['site'].isin([site])]

        fig, ax = plt.subplots(figsize=(20, 6))
        sns.despine(bottom=True, left=True)
        sns.pointplot(x="site", y="score_deviation", data=df, join=False, palette="dark", markers="d")
        sns.stripplot(x="site", y="score_deviation", hue="score",
                      data=df, dodge=True, alpha=.5, zorder=0.5)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::5], labels[::5], title="Score Deviation(%) per site", title_fontsize=14, frameon=True,
                  bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                  ncol=20, mode="expand", borderaxespad=0., fontsize=8)
        st.pyplot(fig)

        if st.checkbox("All websites"):
            fig, ax = plt.subplots(figsize=(20, 6))
            sns.despine(bottom=True, left=True)
            sns.pointplot(x="site", y="score_deviation", data=scored_texts_analytics, join=False, palette="dark",
                          markers="d")

            sns.stripplot(x="site", y="score_deviation", hue="score", data=scored_texts_analytics, dodge=True, alpha=.5,
                          zorder=0.5)

            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[::10], labels[::10], title="Score Deviation(%) per site", title_fontsize=14,
                      frameon=False, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=20, mode="expand",
                      borderaxespad=0., fontsize=8)

            st.pyplot(fig)

    if status == "Author":

        authors = sorted(scored_texts_analytics['author'].unique())
        author = st.selectbox("Who are you looking for?", authors)

        points = scored_texts_analytics[scored_texts_analytics['author'].str.contains(author)]['score'].mean()

        if isinstance(points, float):
            points = points.round(2)

        st.write(author, 'Score average is %s' % points)

        estimated_stars = scored_texts_analytics[scored_texts_analytics['author'].str.contains(author)] \
                              ['stars_mean'].mean() * 2

        if isinstance(estimated_stars, float):
            points = points.round(2)

        st.write('Model prediction average (adjusted) is %s' % estimated_stars)

        if abs(points - estimated_stars) < 0.5:
            st.success('So close! Such a fair reviewer')
        elif 0.5 <= abs(points - estimated_stars) <= 1.5:
            st.warning('Not bad, better than Doritos')
        else:
            st.error('You better change your career, try on Ironhack!')

if status == "Conclusions":
    st.subheader('There are a few conclusions right from the get go')
    st.markdown('- uno / - dos')
