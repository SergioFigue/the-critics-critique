import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def meristation_link_retrieve(pages):
    links = []

    # pages parser
    for i in range(pages):
        url = f'https://as.com/meristation/analisis/{331 - i}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        # links retrieve
        for a in articles:
            if a.find('a') == None:
                pass
            else:
                links.append(a.find('a')['href'])

    # Deleting non review links
    for link in links:
        if 'analisis' not in link:
            links.remove(link)

    return links


def meri_author(soup):
    author = 'None'

    try:
        author = soup.find('p', {'class': 'art-aut-wr'}).find('a').text.strip('\n')

    except AttributeError:
        pass

    try:
        author = soup.find('li', {'class': 'art-aut-wr'}).text.strip('\n')

    except AttributeError:
        pass

    return author


def meri_score(soup):
    # Initialize with most common score
    score = ''

    # 3 different paths for score in Meristation
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

    return score


def meristation_dict(links):
    reviews_dict = {}
    i = 0

    for link in links:
        try:
            # Request content - Avoid get banned - Make a Soup
            review_html = requests.get(link).content
            time.sleep(1)
            soup = BeautifulSoup(review_html, 'lxml')

            # Game - From Scraping
            game = soup.find('div', {'class': 'ga-h-tl'}).text.strip('\n')

            # Author - From Scraping
            author = meri_author(soup)

            # Company, Genre & Platform - From Scraping
            genre = 'None'
            company = 'None'
            platform = 'None'

            infobox = soup.find('ul', {'class': 'li-inl'}).contents
            for box in infobox:

                if (type(box.find('span')) == int) or (box.find('span') == None):
                    pass
                else:
                    # print(box.find('span').text)

                    if 'Plataforma' in box.find('span').text:
                        group = box.find_all('a', {'class': 'rv-inline'})
                        platform = [plat.contents[0].strip('\n') for plat in group]
                        platform = ' '.join(platform).strip('\n')

                    if 'Género' in box.find('span').text:
                        genre = box.find('span', {'class': 'val'}).text.strip('\n')

                    if 'Editor' in box.find('span').text:
                        company = box.find('span', {'class': 'val'}).text.strip('\n')

            # Text & Cleaning - From Scraping
            p_tags = soup.find('div', {'class': 'art-body'}).find_all('p')
            review = [tag.text for tag in p_tags]
            review = ' '.join(review)

            # Score & Clean & Transform - From Scraping
            score = meri_score(soup)

            try:
                score = float(score)

            except ValueError:
                pass

            # Add to a dict
            reviews_dict[i] = {'site': 'meristation',
                               'url_link': link,
                               'author': author,
                               'game': game,
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


def meristation_dataframe(links):
    result_meri = meristation_dict(links)
    meristation_df = pd.DataFrame.from_dict(result_meri, orient='index')
    return meristation_df
