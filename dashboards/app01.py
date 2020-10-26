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

############################33


nlp_model = 'nlptown/bert-base-multilingual-uncased-sentiment'
tokenizer = AutoTokenizer.from_pretrained(nlp_model)
model = AutoModelForSequenceClassification.from_pretrained(nlp_model)
classifier = pipeline(
    'sentiment-analysis',
    model=model,
    tokenizer=tokenizer)

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


col1, col2, col3, col4, col5 = st.beta_columns(5)


def revogamers_link_retrieve():

	url = f'https://www.revogamers.net/analisis-w/page/2'
	html = requests.get(url).content
	soup = BeautifulSoup(html, 'lxml')
	article = soup.find('h2')

	func_link = article.find('a')['href']
	func_title = article.find('a')['title']

	return func_link, func_title

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

if col1.button("Revogamers"):
	link, title = revogamers_link_retrieve()
	author, score, score_adj, func_review = revogamers_streamlit_sentiment_analysis(link)
	stars_mean = split_and_classification(func_review)
	st.write(title)
	st.write(author,"'s score is", score)
	st.write("Model's stars score is", stars_mean)

def gamereactor_link_retrieve():
    url = f'https://www.gamereactor.es/analisis/'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    article = soup.find('section', {'id':'textlist'}).find('article')
    
    func_link = f"https://www.gamereactor.es{article.find('a')['href']}"
    func_title = article.find('h3').text
        
    return func_link, func_title

def gamereactor_streamlit_sentiment_analysis(func_link):

    review_html = requests.get(func_link).content
    soup = BeautifulSoup(review_html, 'lxml')
    
    func_author = soup.find('li', {'class': 'publishAuthor bullet'}).text
    
    article = soup.find('div', {'class': 'breadtext'}).find('div')
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
        st.write(author,"'s score is", score)
        st.write("Model's stars score is", stars_mean)


def tdjuegos_link_retrieve():
        url = f"https://www.3djuegos.com/novedades/analisis/juegos/0f0f0f0/fecha/"

        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find('h2')

        func_link = article.find('a')['href']
        func_title = article.find('a')['title']
    
        return func_link, func_title


def tdjuegos_streamlit_sentiment_analysis(func_link):

    review_html = requests.get(link).content
    soup = BeautifulSoup(review_html, 'lxml')

    func_author = soup.find('a', {'class': 'c7 n'}).text

    p_tags = p_tags = soup.find('div', {'class': 'lh27 url_lineas article_body0 mar_temp_0'}).find_all('p')
    review = [tag.text for tag in p_tags]
    func_review = ' '.join(review)

    try:
        score = soup.find('div', {'class': 'nota_ana_3 fftext b nota_interior2'}).text
        score = score.replace(',','.')
              
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
        st.write(author,"'s score is", score)
        st.write("Model's stars score is", stars_mean)



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
        st.write(author,"'s score is", score)
        st.write("Model's stars score is", stars_mean)


def vandal_link_retrieve():
    url = f"https://vandal.elespanol.com/analisis/videojuegos"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    article = soup.find('div', {'class': 'caja300 afterclearer'})
    func_link = article.find('a')['href'] 
    func_title = article.find('a')['title']
                
    return func_link, func_title


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
        st.write(author,"'s score is", score)
        st.write("Model's stars score is", stars_mean)



#Widgets
#Botón Checkbox para activar o desactivar un contenido

if st.checkbox("Show/Hide"):
	st.text("Showing or hiding Widget")
	st.video(vid_file)

	#Error/Colorful Text
	st.success("Successful")

	st.info("Information!")

	st.warning("This is a Warning")

	st.error("This is an error")

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





































