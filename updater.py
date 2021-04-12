import argparse
import pandas as pd

import scraping.Gamereactor as gam
import scraping.revogamers as rev
import scraping.meristation as mer
import scraping.Vandal as van
import scraping.new_links_retriever as ret


def argument_parser():
    parser = argparse.ArgumentParser(description='Select number of pages')
    parser.add_argument("-p", "--pages", type=int, dest='pages', required=True,
                        help="'Enter the number of pages to retrieve per site. "
                             "Every site export a different number of articles per page")
    parser.add_argument("-d", "--data", type=str, dest='data', required=True,
                        help="Rute to the dataframe you want to test, produced with scraping script")
    args = parser.parse_args()
    return args


def main(pages, data):
    # import dataframes site by site (3D Juegos ditched scores in Dec 2020)
    links_gamereactor, titles_gamereactor = ret.gamereactor_link_retrieve(pages, data)
    gamereactor_df = gam.gamereactor_dataframe(links_gamereactor, titles_gamereactor)

    links_revogamers, titles_revogamers = ret.revogamers_link_retrieve(pages, data)
    revogamers_df = rev.revogamers_dataframe(links_revogamers, titles_revogamers)

    links_meristation = ret.meristation_link_retrieve(pages, data)
    meristation_df = mer.meristation_dataframe(links_meristation)

    links_vandal, titles_vandal = ret.vandal_link_retrieve(pages, data)
    vandal_df = van.vandal_dataframe(links_vandal, titles_vandal)

    # merge and export all reviews together
    old_data = pd.read_csv(data)
    all_sites = pd.concat([old_data, vandal_df, gamereactor_df, revogamers_df, meristation_df],
                          ignore_index=True, sort=False)
    all_sites.dropna(inplace=True)
    all_sites.reset_index(drop=True, inplace=True)
    all_sites.to_csv('./data/up_to_date_all.csv', index=False)
    print(f'Your dataframe is now up to date!')


if __name__ == '__main__':
    arguments = argument_parser()
    print(arguments.pages)
    main(arguments.pages, arguments.data)
