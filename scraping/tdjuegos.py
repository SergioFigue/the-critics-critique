import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def tdjuegos_link_retrieve(pages):
    links = []
    titles = []

    # pages parser
    for i in range(pages):
        if i == 0:
            url = f"https://www.3djuegos.com/novedades/analisis/juegos/0f0f0f0/fecha/"
        else:
            url = f"https://www.3djuegos.com/novedades/analisis/juegos/{i}pf0f0f0/fecha/"

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        # links retrieve
        for a in articles:
            links.append(a.find('a')['href'])
            titles.append(a.find('a')['title'])

    return links, titles


def tdjuegos_platform(soup):
    # This function cover different "cxo" classes founded in the site
    # TODO: THIS LIST IS A ÑAPA TO SKIP POTENTIAL RANGE ERROR
    platform_soup = ["", ""]

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c1o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c2o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c3o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c4o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c5o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c6o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    try:
        platform_soup = soup.find('div', {'class': 'he30 s13 c34o cb mar_t3 mar_l2 d_fl a_n a_cFh fftit'}).find_all(
            'span')

    except AttributeError:
        pass

    finally:

        platform = [plat.contents[0] for plat in platform_soup[2:]]
        platforms = ' '.join(platform)

    return platforms


def tdjuegos_dict(links, titles):
    reviews_dict = {}
    i = 0

    for link, title in zip(links, titles):
        try:

            # Request content - Avoid get banned - Make a Soup
            review_html = requests.get(link).content
            time.sleep(1)
            soup = BeautifulSoup(review_html, 'lxml')

            # Author - From Scraping
            author = soup.find('a', {'class': 'c7 n'}).text

            # Company, Genre & Platform - From Scraping
            genre = 'None'
            company = 'None'
            platform = 'None'

            platform = tdjuegos_platform(soup)

            # Text & Cleaning - From Scraping
            p_tags = p_tags = soup.find('div', {'class': 'lh27 url_lineas article_body0 mar_temp_0'}).find_all('p')
            review = [tag.text for tag in p_tags]
            review = ' '.join(review)

            # Score & Clean & Transform - From Scraping
            # Warning! 3D Juegos stop scoring reviews on Dec 2020. Automatically scored as 0 to be deleted afterwards
            score = 0

            try:
                score = soup.find('div', {'class': 'nota_ana_3 fftext b nota_interior2'}).text
                score = score.replace(',', '.')

            except AttributeError:
                pass

            score = float(score)

            # Add to a dict
            reviews_dict[i] = {'site': '3D Juegos',
                               'url_link': link,
                               'author': author,
                               'game': title,
                               'company': company,
                               'genre': genre,
                               'platform': platform,
                               'text': review,
                               'score': score}

        except AttributeError:
            print('error', i)
            pass

        i = i + 1
        if i % 25 == 0:
            print(i, ': ', link)

    return reviews_dict


def tdjuegos_dataframe(links, titles):
    result_tdjuegos = tdjuegos_dict(links, titles)
    tdjuegos_df = pd.DataFrame.from_dict(result_tdjuegos, orient='index')
    return tdjuegos_df
