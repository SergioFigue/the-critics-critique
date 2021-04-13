import requests
from bs4 import BeautifulSoup
import pandas as pd

'''New Links retriever v2 with a break to skip duplicates.
3 steps: retrieve old and new links, compare and produce new dataframe'''


# vandal updater
def vandal_latest_links(data):
    all_sites = pd.read_csv(data)
    filtered_df = all_sites[all_sites['site'] == 'Vandal']
    return filtered_df['url_link'].tolist()


def vandal_link_retrieve(pages, data):
    links = []
    titles = []
    old_links = vandal_latest_links(data)
    repeated = False

    # pages parser
    for i in range(pages):
        if repeated:
            break

        url = f"https://vandal.elespanol.com/analisis/videojuegos/inicio/{i * 45}"

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('div', {'class': 'caja300 afterclearer'})

        # links & game titles retrieve. New: checking if old to stop adding rows.
        for a in articles:
            link = a.find('a')['href']

            if link not in old_links:
                links.append(link)
                titles.append(a.find('a')['title'])
            else:
                print(f'{len(titles)} new games found on Vandal.')
                repeated = True
                break

    return links, titles


# gamereactor updater
def gamereactor_latest_games(data):
    all_sites = pd.read_csv(data)
    filtered_df = all_sites[all_sites['site'] == 'Gamereactor']

    return filtered_df['game'].tolist()


def gamereactor_link_retrieve(pages, data):
    links = []
    titles = []
    old_games = gamereactor_latest_games(data)
    repeated = False

    # pages parser
    for i in range(pages):
        if repeated:
            break

        url = f'https://www.gamereactor.es/analisis/?page={i + 1}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find('section', {'id': 'textlist'}).find_all('article')

        # links & game titles retrieve. New: checking if old to stop adding rows.
        for article in articles:
            game = article.find('h3').text

            if game not in old_games:
                links.append(f"https://www.gamereactor.es{article.find_all('a')[1]['href']}")
                titles.append(game)
            else:
                print(f'{len(titles)} new games found on Gamereactor.')
                repeated = True
                break

    return links, titles


# revogamers updater
def revogamers_latest_links(data):
    all_sites = pd.read_csv(data)
    filtered_df = all_sites[all_sites['site'] == 'revogamers']
    return filtered_df['url_link'].tolist()


def revogamers_link_retrieve(pages, data):
    links = []
    titles = []
    old_links = revogamers_latest_links(data)
    repeated = False

    # pages parser
    for i in range(pages):
        if repeated:
            break

        url = f'https://www.revogamers.net/analisis-w/page/{i + 1}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        # links retrieve
        for a in articles:
            link = a.find('a')['href']

            if link not in old_links:
                links.append(link)
                titles.append(a.find('a')['title'])
            else:
                print(f'{len(titles)} new games found on Revogamers.')
                repeated = True
                break

    # Deleting non review links
    for link in links:
        if 'analisis' not in link:
            links.remove(link)

    return links, titles


# meristation updater
def meristation_latest_links(data):
    all_sites = pd.read_csv(data)
    filtered_df = all_sites[all_sites['site'] == 'meristation']
    return filtered_df['url_link'].tolist()


def meristation_link_retrieve(pages, data):
    links = []
    old_links = meristation_latest_links(data)
    repeated = False

    # pages parser
    for i in range(pages):
        if repeated:
            break

        url = f'https://as.com/meristation/analisis/{337 - i}'

        # building soup
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('h2')

        # links & game titles retrieve. New: checking if old to stop adding rows.
        for a in articles:

            if a.find('a') is None:
                pass
            else:
                link = a.find('a')['href']

                if link not in old_links:
                    links.append(link)
                else:
                    repeated = True
                    break

    # Deleting non review links
    for link in links:
        if 'analisis' not in link:
            links.remove(link)

    print(f'{len(links)} new games found on Meristation.')
    return links




