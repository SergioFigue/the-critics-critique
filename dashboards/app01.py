#https://docs.streamlit.io/en/stable/api.html
#streamlit run app01.py

import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

st.title('The Critics Critique App')
st.header('Introduction')
st.subheader('Steps')
st.text('This is an example')
st.code('if a == 1:\n    print(a)', language='python')
st.markdown("This is **text** with markdown")


def revogamers_link_retrieve():
       
	url = f'https://www.revogamers.net/analisis-w/page/2'
	html = requests.get(url).content
	soup = BeautifulSoup(html, 'lxml')
	article = soup.find('h2')

	link = article.find('a')['href']
	title = article.find('a')['title']
		        
	return link, title

def revogamers_streamlit_test(link, title):
    reviews_dict = {}

    review_html = requests.get(link).content
    soup = BeautifulSoup(review_html, 'lxml')

    author = soup.find('span', {'class': 'gp-post-meta gp-meta-author'}).find('a').text

    article = soup.find('div', {'class': 'gp-entry-content'}).find_all('p')
    review = [tag.text for tag in article]
    review = ' '.join(review)

    score = soup.find('div', {'class': 'gp-rating-score'}).text.strip()
    score = float(score)
    score_adj = score / 2

    return author, review, score, score_adj

def sentiment_analysis_bert_base_multilingual_uncased(review):
    n = 1500
    points = []
    
    review_splitted = [(review[i:i + n]) for i in range(0, len(review), n)]
    global_stars = (classifier(review_splitted))

    for classification in global_stars:
        grade = int(classification['label'].split(' ')[0])
        points.append(grade)
    stars_mean = round(np.mean(points), 2)

    return stars_mean


#Botón Button cliclable

nlp_model = 'nlptown/bert-base-multilingual-uncased-sentiment'
tokenizer = AutoTokenizer.from_pretrained(nlp_model)
model = AutoModelForSequenceClassification.from_pretrained(nlp_model)
classifier = pipeline(
        'sentiment-analysis', 
        model=model, 
        tokenizer=tokenizer)

if st.button("Revogamers"):
	link, title = revogamers_link_retrieve()
	author, review, score, score_adj = revogamers_streamlit_test(link, title)
	stars_mean = sentiment_analysis_bert_base_multilingual_uncased(review)

	st.write(title)
	st.write(author)
	st.write(score)
	st.write(score_adj)
	st.write(stars_mean)


#Error/Colorful Text
st.success("Successful")

st.info("Information!")

st.warning("This is a Warning")

st.error("This is an error")



#Widgets
#Botón Checkbox para activar o desactivar un contenido

if st.checkbox("Show/Hide"):
	st.text("Showing or hiding Widget")
	st.video(vid_file)

#Botón Radio para elegir que se linka a varias alternativas visibles

status = st.radio("Select a website", ("RG", "GR"))

if status == "RG":
	st.success("RG data")

elif status == "GR":
	st.success("GR data")


#Botón Selectbox para escoger variar alternativas en desplegable

occupation = st.selectbox("Your occupation", ["Programmer", "DataScientist", "Human"])
st.write("You selected this option", occupation)


#Botón MultiSelect para elegir varias opiones en desplegable

location = st.multiselect("Select a platform", ["Nintendo Switch", "PS4", "Xbox One", "Nintendo 3DS", "PC"])
st.write("You selected", len(location), "options")

#Botón Slider con pregunta y límites inferior y superior

score = st.slider("Choose a score",1,10) 

if score == 3:
	st.text("Tres")




#Recibe imput primera parte por encima y segunda dentro del cuadro y le ponemos un botón para imputar y un resultado con color verde. Casi igual pero más grande con text_area.


firstname = st.text_input("Enter your name", "Type Here")
if st.button("Submit"):
	result = firstname.title()
	st.success(result)

##############################################

#Sidebars
st.sidebar.header("The Critics Critique")

st.sidebar.subheader("The Frame")
radio_list_up = ["Know the app", "How critics score"]
status = st.sidebar.radio("", (radio_list_up))

if status == "Know the app":
	st.success("RG data")

elif status == "How critics score":
	st.success("GR data")

st.sidebar.subheader("NLP Scores Compared by:")
radio_list_down = ["Website", "Platform", "Author", "Genre"]
status = st.sidebar.radio("", (radio_list_down))





#Decoradores st.progress(), st.spinner(), st.balloons





































