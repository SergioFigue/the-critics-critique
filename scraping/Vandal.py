import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def vandal_link_retrieve(num_pages):
    links = []
    titles = []

    # pages parser
    for i in range(num_pages):
        url = f"https://vandal.elespanol.com/analisis/videojuegos/inicio/{i * 45}"

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('div', {'class': 'caja300 afterclearer'})

        # links & game titles retrieve
        for a in articles:
            links.append(a.find('a')['href'])
            titles.append(a.find('a')['title'])

    return links, titles


def vandal_platform(soup):
    platform_soup = soup.find('td', {'class': 'tablaplataformas'})
    platform = [img["alt"] for img in platform_soup.select("img[alt]")]
    platform = ' '.join(platform)

    return platform


def vandal_genre(soup):
    genre_soup = soup.find('div', {'class': 'mt1 tcenter t11'}).find_all('a')
    genre = [gs.text for gs in genre_soup]
    genre = ' '.join(genre)

    return genre


def vandal_company(soup):

    infobox = soup.find('ul', {'class': 'mt03 ulficha'})
    for box in infobox:
        if 'Producción: ' in box.contents:
            company = box.find('a').text

            return company


def vandal_dict(links, titles):
    reviews_dict = {}
    i = 0

    for link, title in zip(links, titles):
        try:

            # Request content - Avoid get banned - Make a Soup
            review_html = requests.get(link).content
            time.sleep(1)
            soup = BeautifulSoup(review_html, 'lxml')

            # Author - From Scraping
            author = soup.find('span', {'class': 'reviewer'}).text

            # Company - From Scraping
            company = vandal_company(soup)

            # Genre - From Scraping
            genre = vandal_genre(soup)

            # Platform - From Scraping
            platform = vandal_platform(soup)

            # Text & Cleaning - From Scraping
            p_tags = soup.find('div', {'class': 'textart'}).find_all('p')
            review = [tag.text for tag in p_tags]
            review = ' '.join(review).strip()

            # Score & Clean & Transform - From Scraping
            score = soup.find('div', {'class': 'fichajuego mt03 tleft'}).text
            score = float(score)

            # Add to a dict
            reviews_dict[i] = {'site': 'Vandal',
                               'url_link': link,
                               'author': author,
                               'game': title,
                               'company': company,
                               'genre': genre,
                               'platform': platform,
                               'text': review,
                               'score': score}

        except (ValueError, AttributeError) as e:
            print('error', i)
            pass

        i = i + 1
        if i % 25 == 0:
            print(i, ': ', link)

    return reviews_dict


def vandal_dataframe(links, titles):
    result_vandal = vandal_dict(links, titles)
    vandal_df = pd.DataFrame.from_dict(result_vandal, orient='index')
    return vandal_df
