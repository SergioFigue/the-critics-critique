# The-critics-critique
My hypothesis is: spanish reviewers overrate video games.

![The Critics Critique conclusions](https://github.com/SergioFigue/the-critics-critique/blob/master/The-Critics-Critique_conclusions.png)


## What is this for

The Critics Critique is a **NLP based app** consisting in two scripts. In first place, a secondary script fetch five different websites looking for video games reviews. Then, the main script apply a sentiment analysis powered by a pre-treained BERT multilengual model, return a score based on wording and let you visualize results through an interactive dashboard.

The original idea comes from a personal feeling by the author and many others in the video games press industry. But also, from what we see in international review aggregators.

## Technologies

The Critics Critique was develoed on python 3.7 and requires popular libraries: requests and beautiful soup for web scraping; pandas and transformers by hugging face (AutoTokenizer, AutoModelForSequenceClassificationby nlptown) for data manipulation, cleaning and sentiment classification; and seaborn, plotly express and streamlit for visualization and reporting. 

## Instructions

Running the first script requires introducing the number of pages you want to fetch from outlet's reviews page. It returns a clean list with review links and game titles. Then, a second function open those links, scrapt the sites selecting relevant information and, finally, creates and exports a dataframe.

The scraping script was created exclusively to be used on the Spanish outlets: Gamereactor Spain, revogamers, meristation, Vandal and 3D Juegos. Feel free to produce you own in any multi-5 language, but keep the format.

The main script can take any dataframe of any number of lines. You might need to adapta cleaning and wrangling depending on language. Large texts are also good to go, as the script split them avoiding tokenization limits, classify every section separatedly and then merge results as a main stars_score. This app was developed to compare reviews scored 2-10 with sentiment analyses scored 1-5.

Lastly, the dashboard includes easy-to-use options for granular analytics and categorical agreggations.

![Video Games - Scattered scores by outlet](https://github.com/SergioFigue/the-critics-critique/blob/master/Score_site_deviation_all.png)


### Example Data

The main analysis was created from data counting for a total of 15.551 valid reviews. Some texts are 10 years old!

Every raw example includes the following columns: site, url, game name, producer company, genre(s), author, plain text and score in the site. While data calculation let us produce a few syntethic variables, stars_mean is key for the model. Then, put it face to face with the orinal score downscaled to produce the mean score deviation. Positive deviation means sentiment is better than score and vice versa.

### Reporting: the dashboard

The dashboard compares how video games critics score a review versus the sentiment said review conveys to the reader according to a pretrained BERT NLP model. Let users show the whole dataframe or just fragments related to categorical variables. This way, it's really easy to visually find and show different insights from thousands and thousands of texts.

![Video Games - Average game score by company](https://github.com/SergioFigue/the-critics-critique/blob/master/Score_plotted_byCompany.png)

## Conclusions

More than 15,500 review later, this model revealed the truth:

* In 4 out of 5 outlets, human score is frequently better than NLP score
* The better the game, the bigger the score deviation
* Authors make no distinction between platforms

**In conclusion: Spanish reviewers inflate video games scores**

## Special thanks

This project wouldn't been possible without the generous support and assistance of the Ironhack lead and assistante teachers, my pals at Gamereactor and, most importantly, my 24/7 fullstack developer and husband.



