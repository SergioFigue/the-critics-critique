import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def revogamers_link_retrieve(pages):
    links = []
    titles = []

    # pages parser
    for i in range(pages):
        url = f'https://www.revogamers.net/analisis-w/page/{i + 51}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        # links retrieve
        for a in articles:
            links.append(a.find('a')['href'])
            titles.append(a.find('a')['title'])

    # Deleting non review links
    for link in links:
        if 'analisis' not in link:
            links.remove(link)

    return links, titles


def revogamers_dict(links, titles):
    reviews_dict = {}
    i = 0

    for link, title in zip(links, titles):
        try:
            # Request content - Avoid get banned - Make a Soup
            review_html = requests.get(link).content
            time.sleep(3)
            soup = BeautifulSoup(review_html, 'lxml')

            # Author - From Scraping
            author = soup.find('span', {'class': 'gp-post-meta gp-meta-author'}).find('a').text

            # Company, Genre & Platform - From Scraping
            genre = 'None'
            company = 'None'
            platform = 'Nintendo Switch'

            elems = soup.find_all('span', {'class': 'gp-hub-field-list'})
            if len(elems) == 3:
                genre, company, platform = [elem.text for elem in elems]

            elif len(elems) != 3:
                div = soup.find_all('div', {'class': 'gp-hub-field'})

                for span in div:

                    if 'Genero:' in span.find('span', {'class': 'gp-hub-field-name'}).text:
                        genre = span.find('span', {'class': 'gp-hub-field-list'}).text

                    if 'Desarrolladora:' in span.find('span', {'class': 'gp-hub-field-name'}).text:
                        company = span.find('span', {'class': 'gp-hub-field-list'}).text

                    if 'Sistema:' in span.find('span', {'class': 'gp-hub-field-name'}).text:
                        platform = span.find('span', {'class': 'gp-hub-field-list'}).text

            # Text & Cleaning - From Scraping
            article = soup.find('div', {'class': 'gp-entry-content'}).find_all('p')
            review = [tag.text for tag in article]
            review = ' '.join(review)

            # Score & Clean & Transform - From Scraping
            score = soup.find('div', {'class': 'gp-rating-score'}).text.strip()
            score = float(score)

            # Add to a dict
            reviews_dict[i] = {'site': 'revogamers',
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
            print(i, ': ', link)

    return reviews_dict


def revogamers_dataframe(links, titles):
    result_revo = revogamers_dict(links, titles)
    revogamers_df = pd.DataFrame.from_dict(result_revo, orient='index')
    return revogamers_df
