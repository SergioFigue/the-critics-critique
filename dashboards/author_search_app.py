import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.beta_set_page_config(layout="centered")


st.image(Image.open("./data/media/stadia_platforms.jpg"), width=450)


@st.cache(show_spinner=False)
def load_data():
    return pd.read_csv('./data/scored_texts_analytics.csv')


scored_texts_analytics = load_data()

st.title('The Critics Critique App')

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


