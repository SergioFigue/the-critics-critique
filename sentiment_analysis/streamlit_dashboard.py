import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#def run_streamlit(scored_texts_analytics):


def load_data():
    return pd.read_csv('../data/scored_texts_analytics.csv')


#@st.cache
scored_texts_analytics = load_data()
st.beta_set_page_config(layout="centered")
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

    st.markdown("*This is how the real score compares with the stars suggested by the model*")

    from PIL import Image
    img = Image.open("../data/media/Plan Proyecto Sergio.jpg")
    st.image(img, width=450)

    # Sidebar 2 - NLP Stars vs Scores

    st.sidebar.subheader("NLP Stars vs Scores")
    radio_list_down = ["Website", "Platform", "Author", "Company"]
    status = st.sidebar.radio("", radio_list_down, key=2)

    if status == 'Website':

        st.subheader('First look site by site')
        st.markdown('**Mean score deviation** is the difference between score and prediction in % and looks like this')
        st.markdown('·*Positive deviation means sentiment is better than score and vice versa*')

        site_deviation = scored_texts_analytics.groupby('site')[['score', 'stars_mean', 'score_deviation']].mean()
        st.table(site_deviation)

        sites = scored_texts_analytics['site'].unique()
        site = st.selectbox("Select a website", sites)

        df = scored_texts_analytics[scored_texts_analytics['site'].isin([site])]

        fig1, ax = plt.subplots(figsize=(20, 6))
        sns.despine(bottom=True, left=True)
        sns.pointplot(x="site", y="score_deviation", data=df, join=False, palette="dark", markers="d")
        sns.stripplot(x="site", y="score_deviation", hue="score",
                      data=df, dodge=True, alpha=.5, zorder=0.5)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::5], labels[::5], title="Score Deviation(%) per site", title_fontsize=16, frameon=True,
                  bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                  ncol=20, mode="expand", borderaxespad=0., fontsize=8)
        st.pyplot(fig1)

        if st.checkbox("All websites"):
            fig2, ax = plt.subplots(figsize=(20, 6))
            sns.despine(bottom=True, left=True)
            sns.pointplot(x="site", y="score_deviation", data=scored_texts_analytics, join=False, palette="dark",
                          markers="d")

            sns.stripplot(x="site", y="score_deviation", hue="score", data=scored_texts_analytics, dodge=True, alpha=.5,
                          zorder=0.5)

            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[::10], labels[::10], title="Score Deviation(%) per site", title_fontsize=16,
                      frameon=False, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=20, mode="expand",
                      borderaxespad=0., fontsize=8)

            st.pyplot(fig2)

    if status == "Author":

        st.subheader('What they write vs how they score')

        authors = sorted(scored_texts_analytics['author'].unique())
        author = st.selectbox("Who are you looking for?", authors)

        points = scored_texts_analytics[scored_texts_analytics['author'].str.contains(author)]['score'].mean()

        if isinstance(points, float):
            points = points.round(2)

        st.write(author, 'Score average is %s' % points)

        estimated_stars = scored_texts_analytics[scored_texts_analytics['author'].str.contains(author)] \
                              ['stars_mean'].mean() * 2

        if isinstance(estimated_stars, float):
            estimated_stars = estimated_stars.round(2)

        st.write('Model prediction average (adjusted) is %s' % estimated_stars)

        if abs(points - estimated_stars) < 0.5:
            st.success('So close! Such a fair reviewer')
        elif 0.5 <= abs(points - estimated_stars) <= 1.5:
            st.warning('Not bad, better than Doritos')
        else:
            st.error('You better change your career, try on Ironhack!')

        st.subheader('Is it a real problem?')
        st.markdown('**Mean score deviation** is the difference between score and prediction in % and looks like this')
        st.markdown('·*Positive deviation means sentiment is better than score and vice versa*')

        q_authors_filter = scored_texts_analytics.groupby('author').filter(lambda x: len(x) >= 3)
        q_authors = q_authors_filter.groupby('author')['score_deviation'].mean()

        fig3, ax = plt.subplots(figsize=(20, 6))
        N, bins, patches = plt.hist(q_authors, 30)
        cmap = plt.get_cmap('jet')
        low = cmap(0.5)
        medium = cmap(0.2)
        high = cmap(0.7)

        for i in range(0, 3):
            patches[i].set_facecolor(low)
        for i in range(4, 13):
            patches[i].set_facecolor(medium)
        for i in range(14, 30):
            patches[i].set_facecolor(high)

        plt.xlabel("Mean score deviation", fontsize=16)
        plt.ylabel("Authors count", fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig3)

    if status == "Company":

        st.subheader('Names matter more than quality?')
        st.markdown('**Mean score deviation** is the difference between score and prediction in % and looks like this')
        st.markdown('·*Positive deviation means sentiment is better than score and vice versa*')

        q_companies_filter = scored_texts_analytics.groupby('company').filter(lambda x: len(x) >= 20)
        q_companies = q_companies_filter.groupby('company')['score_deviation'].mean()

        col1, col2 = st.beta_columns(2)
        col1.header("Come off well scored")
        site_deviation_pos = q_companies.sort_values().head(10)
        col1.table(site_deviation_pos)

        col2.header("Come off poorly scored")
        site_deviation_neg = q_companies.sort_values(ascending=False).head(10)
        col2.table(site_deviation_neg)

        st.subheader('Tendency: shower with compliments')
        st.markdown('There is a clear correlation between score and pretty words')

        c_companies = q_companies_filter.groupby('company')[['game']].count().reset_index()
        s_companies = q_companies_filter.groupby('company')[['score_deviation', 'score']].mean().reset_index()
        companies_df = pd.merge(c_companies, s_companies, on="company")
        companies_df.drop(companies_df[companies_df['company'] == 'None'].index, inplace=True)

        fig4 = px.scatter(companies_df, x="score", y="score_deviation", color="company", size='game')
        fig4.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        st.plotly_chart(fig4, use_container_width=True)


if status == "Conclusions":
    st.subheader('There are a few conclusions right from the get go')
    st.markdown('- uno / - dos')
