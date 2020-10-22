#https://docs.streamlit.io/en/stable/api.html
#streamlit run app01.py

import streamlit as st
import pandas as pd
import numpy as np

st.title('The Critics Critique App')
st.header('Introduction')
st.subheader('Steps')
st.text('This is an example')
st.code('if a == 1:\n    print(a)', language='python')
st.markdown("This is **text** with markdown")


#Error/Colorful Text
st.success("Successful")

st.info("Information!")

st.warning("This is a Warning")

st.error("This is an error")

#Writing Text para poner funciones dentro

st.write(range(10))

#st.write(data_frame)
#st.dataframe(df.style.highlight_max(axis=0))
#st.write(mpl_fig)
#st.pyplot(fig)
#st.write(plotly_fig)
#st.plotly_chart()

#Imagen

from PIL import Image
img = Image.open("../data/media/Plan Proyecto Sergio.jpg")
st.image(img, width=450, caption="nombrecico o lista si son varias")

#Video

vid_file = open("../data/media/xcloud_gamereactor.mp4","rb").read()



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

#Botón Button cliclable

if st.button("Guess score"):
	st.text("function missing")


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


#Funciones, a las que puedes añadir @st.cache para que vaya más rápido.

@st.cache

def load_data():
	scored_texts_analytics = pd.read_csv('../data/scored_texts_analytics.csv')
	return scored_texts_analytics

scored_texts_analytics = load_data()

st.write(scored_texts_analytics)

sergio = scored_texts_analytics[scored_texts_analytics['author'].str.contains('Sergio Figueroa')]['score'].mean().round(2)

st.text('Average score by Sergio is %s points' % sergio)

authors = sorted(scored_texts_analytics['author'].unique())
author = st.selectbox("Select a name", authors)
st.write("You selected", author)

points = scored_texts_analytics[scored_texts_analytics['author'].str.contains(author)]['score'].mean()

if isinstance(points, float):
	points = points.round(2)

st.text('And his reviews score average is %s' % points)


#Decoradores st.progress(), st.spinner(), st.balloons





































