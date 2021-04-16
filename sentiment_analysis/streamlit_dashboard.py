import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


st.beta_set_page_config(layout="centered")


@st.cache(show_spinner=False)
def load_data():
    return pd.read_csv('./data/wrangled_data/scored_texts.csv')


scored_texts_analytics = load_data()

st.title('The Critics Critique App')


# NLP Model
@st.cache(show_spinner=False)
def model_function():
    nlp_model = 'nlptown/bert-base-multilingual-uncased-sentiment'
    tokenizer = AutoTokenizer.from_pretrained(nlp_model)
    model = AutoModelForSequenceClassification.from_pretrained(nlp_model)
    classifier = pipeline(
        'sentiment-analysis',
        model=model,
        tokenizer=tokenizer)

    return classifier


classifier = model_function()


@st.cache(show_spinner=False)
def split_and_classification(review):
    n = 1500
    func_points = []
    review_splitted = [(review[i:i + n]) for i in range(0, len(review), n)]
    global_stars = (classifier(review_splitted))

    for classification in global_stars:
        grade = int(classification['label'].split(' ')[0])
        func_points.append(grade)
    func_stars_mean = round(np.mean(func_points), 2)

    return func_stars_mean


@st.cache(show_spinner=False)
def insert_img():
    from PIL import Image

    return Image.open("./data/media/stadia_platforms.jpg")


img = insert_img()

# Sidebar 1
st.sidebar.header("The Critics Critique")

st.sidebar.subheader("Do you trust critics?")
radio_list_up = ["Know the app", "Take a sample", "How critics score", "Conclusions"]
status = st.sidebar.radio("", radio_list_up, key=1)

if status == "Know the app":
    # st.success("RG data")

    st.markdown("*Would you trust this guy?*")

    my_slot1 = st.empty()

    vid_file = open("./data/media/xcloud_gamereactor.mp4", "rb").read()
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

    st.image(img, width=450)

    if st.checkbox("Take a look at the DataFrame"):
        st.markdown("*This is how the real score compares with the stars suggested by the model*")
        st.write(scored_texts_analytics)

    st.subheader('Run the code')
    st.markdown("* Push the button to start scraping the website and criticize the critic. Just a few seconds.")

    col1, col2, col3, col4, col5 = st.beta_columns(5)


    @st.cache(show_spinner=False)
    def revogamers_link_retrieve():
        url = f'https://www.revogamers.net/analisis-w/page/2'
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find('h2')

        func_link = article.find('a')['href']
        func_title = article.find('a')['title']

        return func_link, func_title


    @st.cache(show_spinner=False)
    def revogamers_streamlit_sentiment_analysis(func_link):
        review_html = requests.get(func_link).content
        soup = BeautifulSoup(review_html, 'lxml')

        func_author = soup.find('span', {'class': 'gp-post-meta gp-meta-author'}).find('a').text

        article = soup.find('div', {'class': 'gp-entry-content'}).find_all('p')
        func_review = [tag.text for tag in article]
        func_review = ' '.join(func_review)

        func_score = soup.find('div', {'class': 'gp-rating-score'}).text.strip()
        func_score = float(func_score)
        func_score_adj = func_score / 2

        return func_author, func_score, func_score_adj, func_review


    if col1.button("revogamers"):
        link, title = revogamers_link_retrieve()
        author, score, score_adj, func_review = revogamers_streamlit_sentiment_analysis(link)
        stars_mean = split_and_classification(func_review)
        st.write(title)
        st.write(author, "'s score is", score)
        st.write("Model's stars score is", stars_mean)


    @st.cache(show_spinner=False)
    def gamereactor_link_retrieve():
        url = f'https://www.gamereactor.es/analisis/'
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find('section', {'id': 'textlist'}).find('article')

        func_link = f"https://www.gamereactor.es{article.find('a')['href']}"
        func_title = article.find('h3').text

        return func_link, func_title

    @st.cache(show_spinner=False)
    def gamereactor_streamlit_sentiment_analysis(func_link):
        review_html = requests.get(func_link).content
        soup = BeautifulSoup(review_html, 'lxml')

        func_author = soup.find('li', {'class': 'publishAuthor bullet'}).text

        article = soup.find('div', {'class': 'breadtext'}).find('div', {'id': 'page0'})
        p_tags = article.find_all('p')
        func_review = [tag.text for tag in p_tags]
        func_review = ' '.join(func_review)

        func_score = soup.find('div', {'class': 'bigScoreWrapper'}).find('img')['alt']
        func_score = float(func_score)
        func_score_adj = func_score / 2

        return func_author, func_score, func_score_adj, func_review


    if col2.button("Gamereactor"):
        link, title = gamereactor_link_retrieve()
        author, score, score_adj, func_review = gamereactor_streamlit_sentiment_analysis(link)
        stars_mean = split_and_classification(func_review)
        st.write(title)
        st.write(author, "'s score is", score)
        st.write("Model's stars score is", stars_mean)

    #@Deprecated: 3D Juegos stop scoring reviews on December 15, 2020.
    @st.cache(show_spinner=False)
    def tdjuegos_link_retrieve():
        url = f"https://www.3djuegos.com/novedades/analisis/juegos/0f0f0f0/fecha/"

        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find('h2')

        func_link = article.find('a')['href']
        func_title = article.find('a')['title']

        return func_link, func_title


    @st.cache(show_spinner=False)
    def tdjuegos_streamlit_sentiment_analysis(func_link):
        review_html = requests.get(link).content
        soup = BeautifulSoup(review_html, 'lxml')

        func_author = soup.find('a', {'class': 'c7 n'}).text

        p_tags = p_tags = soup.find('div', {'class': 'lh27 url_lineas article_body0 mar_temp_0'}).find_all('p')
        review = [tag.text for tag in p_tags]
        func_review = ' '.join(review)

        try:
            score = soup.find('div', {'class': 'nota_ana_3 fftext b nota_interior2'}).text
            score = score.replace(',', '.')

        except AttributeError:
            pass

        func_score = float(score)
        func_score_adj = func_score / 2

        return func_author, func_score, func_score_adj, func_review


    if col3.button("3D Juegos"):
        link, title = tdjuegos_link_retrieve()
        author, score, score_adj, func_review = tdjuegos_streamlit_sentiment_analysis(link)
        stars_mean = split_and_classification(func_review)
        st.write(title)
        st.write(author, "'s score is", score)
        st.write("Model's stars score is", stars_mean)


    @st.cache(show_spinner=False)
    def meristation_link_retrieve():
        url = f'https://as.com/meristation/analisis/'
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        for a in articles:
            if a.find('a') == None:
                pass
            else:
                func_link = a.find('a')['href']

        return func_link


    @st.cache(show_spinner=False)
    def meristation_streamlit_sentiment_analysis(func_link):
        review_html = requests.get(link).content
        soup = BeautifulSoup(review_html, 'lxml')

        title = soup.find('div', {'class': 'ga-h-tl'}).text.strip('\n')

        func_author = 'None'

        try:
            func_author = soup.find('p', {'class': 'art-aut-wr'}).find('a').text.strip('\n')
        except AttributeError:
            pass
        try:
            func_author = soup.find('li', {'class': 'art-aut-wr'}).text.strip('\n')
        except AttributeError:
            pass

        p_tags = soup.find('div', {'class': 'art-body'}).find_all('p')
        review = [tag.text for tag in p_tags]
        func_review = ' '.join(review)

        try:
            score = soup.find('span', {'class': 'rv-sc sc-h'}).text
        except AttributeError:
            pass
        try:
            score = soup.find('span', {'class': 'rv-sc sc-m'}).text
        except AttributeError:
            pass
        try:
            score = soup.find('span', {'class': 'rv-sc sc-l'}).text
        except AttributeError:
            pass

        func_score = float(score)
        func_score_adj = func_score / 2

        return title, func_author, func_score, func_score_adj, func_review

    if col4.button("meristation"):
        link = meristation_link_retrieve()
        title, author, score, score_adj, func_review = meristation_streamlit_sentiment_analysis(link)
        stars_mean = split_and_classification(func_review)
        st.write(title)
        st.write(author, "'s score is", score)
        st.write("Model's stars score is", stars_mean)

    @st.cache(show_spinner=False)
    def vandal_link_retrieve():
        url = f"https://vandal.elespanol.com/analisis/videojuegos"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find('div', {'class': 'caja300 afterclearer'})
        func_link = article.find('a')['href']
        func_title = article.find('a')['title']

        return func_link, func_title


    @st.cache(show_spinner=False)
    def vandal_streamlit_sentiment_analysis(func_link):
        review_html = requests.get(link).content
        soup = BeautifulSoup(review_html, 'lxml')

        func_author = soup.find('span', {'class': 'reviewer'}).text

        p_tags = soup.find('div', {'class': 'textart'}).find_all('p')
        review = [tag.text for tag in p_tags]
        func_review = ' '.join(review).strip()

        score = soup.find('div', {'class': 'fichajuego mt03 tleft'}).text
        func_score = float(score)
        func_score_adj = func_score / 2

        return func_author, func_score, func_score_adj, func_review


    if col5.button("Vandal"):
        link, title = vandal_link_retrieve()
        author, score, score_adj, func_review = vandal_streamlit_sentiment_analysis(link)
        stars_mean = split_and_classification(func_review)
        st.write(title)
        st.write(author, "'s score is", score)
        st.write("Model's stars score is", stars_mean)


if status == "How critics score":

    st.markdown("*This is how the real score compares with the stars suggested by the model*")

    st.image(img, width=450)

    # Sidebar 2 - NLP Stars vs Scores

    st.sidebar.subheader("NLP Stars vs Scores")
    radio_list_down = ["Website", "Author", "Company", "Platform"]
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

        fig4 = px.scatter(companies_df, x="score", y="score_deviation", color="company", size='game',
                          template="simple_white")
        st.plotly_chart(fig4, use_container_width=True)

    if status == 'Platform':

        st.subheader('Focusing on the last console generation and PC')
        st.markdown('*Left value: real score, right value: NLP prediction*')

        switch_df = scored_texts_analytics[scored_texts_analytics['platform'].str.contains("Switch")]
        switch_plot = switch_df[['score', 'stars_mean']].mean()
        ps4_df = scored_texts_analytics[scored_texts_analytics['platform'].str.contains("PS4")]
        ps4_plot = ps4_df[['score', 'stars_mean']].mean()
        xbox_df = scored_texts_analytics[scored_texts_analytics['platform'].str.contains("Xbox One")]
        xbox_plot = xbox_df[['score', 'stars_mean']].mean()
        pc_df = scored_texts_analytics[scored_texts_analytics['platform'].str.contains("PC")]
        pc_plot = pc_df[['score', 'stars_mean']].mean()

        platform_plot = ps4_plot.to_frame(name='PS4').join(switch_plot.to_frame(name='Switch')).join(
            xbox_plot.to_frame(name='Xbox One')).join(pc_plot.to_frame(name='PC'))

        fig5 = px.line(platform_plot, labels={"variable": "Platform", "index": "", "value": "Score"},
                       template="simple_white")
        st.plotly_chart(fig5, use_container_width=True)

if status == "Conclusions":
    st.image(img, width=450)
    st.subheader('More than 15,500 review later, this model uncovered the truth:')
    st.markdown('- In 4 out of 5 outlets, human score is frequently better than NLP score')
    st.markdown('- Human scores tent towards extreme opinions, the model is more moderate')
    st.markdown('- Authors make no distinction between platforms')
    st.markdown('**In conclusion: Spanish reviewers inflate video games scores, only when the score is fat**')
    st.text("")
    st.button("Download and Try your self for free!")


