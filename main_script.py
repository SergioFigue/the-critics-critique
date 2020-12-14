import argparse
import sentiment_analysis.model as mod
import sentiment_analysis.wrangling as wra
from streamlit import bootstrap


def argument_parser():
    parser = argparse.ArgumentParser(description='Select a dataframe')
    parser.add_argument("-d", "--data", type=str, dest='data', required=True,
                        help="Rute to the dataframe you want to test, produced with scraping script")
    args = parser.parse_args()
    return args


def main(data):
    all_sites = mod.acquire(data)
    scored_texts = mod.final_dataframe(all_sites)
    wra.score_deviation_func(scored_texts)
    real_script = 'sentiment_analysis/streamlit_dashboard.py'
    bootstrap.run(real_script, f'run.py {real_script}', [])


if __name__ == '__main__':
    arguments = argument_parser()
    print(f'you choosed: {arguments.data}')
    main(arguments.data)
