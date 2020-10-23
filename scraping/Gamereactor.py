import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def gamereactor_link_retrieve(num_pages):
    links = []
    titles = []

    # pages parser
    for i in range(num_pages):
        url = f'https://www.gamereactor.es/analisis/?page={i + 26}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find('section', {'id': 'textlist'}).find_all('article')

        # links retrieve
        for article in articles:
            links.append(f"https://www.gamereactor.es{article.find_all('a')[1]['href']}")
            titles.append(article.find('h3').text)

    return links, titles


def gamereactor_dict(links, titles):
    reviews_dict = {}
    i = 0

    for link, title in zip(links, titles):
        try:
            # Request content - Avoid get banned - Make a Soup
            review_html = requests.get(link).content
            time.sleep(1)
            soup = BeautifulSoup(review_html, 'lxml')

            # Author - From Scraping
            author = soup.find('li', {'class': 'publishAuthor bullet'}).text

            # Company, Genre & Platform - From Scraping
            genre = 'None'
            company = 'None'
            platform = 'None'

            infobox = soup.find_all('ul', {'class': 'infobox'})[0].contents
            for box in infobox:

                if 'Probado en:' in box.contents[0].text or 'Plataforma:' in box.contents[0].text:
                    platform = box.contents[1]

                if 'Género:' in box.contents[0].text:
                    genre = box.find('a').text

                if 'Editor:' in box.contents[0].text:
                    company = box.find('a').text

            # Text & Cleaning - From Scraping
            article = soup.find('div', {'class': 'breadtext'}).find('div')
            p_tags = article.find_all('p')
            review = [tag.text for tag in p_tags]
            review = ' '.join(review)

            # Score & Clean & Transform - From Scraping
            score = soup.find('div', {'class': 'bigScoreWrapper'}).find('img')['alt']
            score = float(score)

            # Add to a dict
            reviews_dict[i] = {'site': 'Gamereactor',
                               'url_link': link,
                               'author': author,
                               'game': title,
                               'company': company,
                               'genre': genre,
                               'platform': platform,
                               'text': review,
                               'score': score}

        except AttributeError:
            pass

        i = i + 1
        if i % 25 == 0:
            print(i, ':', link)

    return reviews_dict


def gamereactor_dataframe(links, titles):
    result_revo = gamereactor_dict(links, titles)
    gamereactor_df = pd.DataFrame.from_dict(result_revo, orient='index')
    return gamereactor_df

