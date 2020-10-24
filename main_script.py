import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Select a dataframe')
    parser.add_argument("-d", "--data", type=, dest='pages', required=True,
                        help="Rute to the dataframe you want to test, produced with scraping script")
    args = parser.parse_args()
    return args

def main():
    print('boo')


if __name__ == '__main__':
    #arguments = argument_parser()
    #print(arguments.pages)
    main()
