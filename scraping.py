import argparse
import pandas as pd
from sklearn.utils import shuffle

import scraping.Gamereactor as gam
import scraping.revogamers as rev
import scraping.tdjuegos as tdj
import scraping.meristation as mer
import scraping.Vandal as van


def argument_parser():
    parser = argparse.ArgumentParser(description='Select number of pages')
    parser.add_argument("-p", "--pages", type=int, dest='pages', required=True,
                        help="'Enter the number of pages to retrieve per site. "
                             "Every site export a different number of articles per page")
    args = parser.parse_args()
    return args


def main(pages):

    # import dataframes site by site
    links_gamereactor, titles_gamereactor = gam.gamereactor_link_retrieve(pages)
    gamereactor_df = gam.gamereactor_dataframe(links_gamereactor, titles_gamereactor)

    links_revogamers, titles_revogamers = rev.revogamers_link_retrieve(pages)
    revogamers_df = rev.revogamers_dataframe(links_revogamers, titles_revogamers)

    links_tdjuegos, titles_tdjuegos = tdj.tdjuegos_link_retrieve(pages)
    tdjuegos_df = tdj.tdjuegos_dataframe(links_tdjuegos, titles_tdjuegos)

    links_meristation = mer.meristation_link_retrieve(pages)
    meristation_df = mer.meristation_dataframe(links_meristation)

    links_vandal, titles_vandal = van.vandal_link_retrieve(pages)
    vandal_df = van.vandal_dataframe(links_vandal, titles_vandal)

    # merge, shuffle and export all review together
    sites_dataframes = [gamereactor_df, meristation_df, revogamers_df, vandal_df, tdjuegos_df]
    all_sites = pd.concat(sites_dataframes)
    all_sites.dropna(inplace=True)
    all_sites = shuffle(all_sites)
    all_sites.reset_index(drop=True, inplace=True)
    all_sites.to_csv('./data/test2_2021.csv', index=False)
    print(f'A new dataframe was created!')

if __name__ == '__main__':
    arguments = argument_parser()
    print(arguments.pages)
    main(arguments.pages)
