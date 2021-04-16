from streamlit import bootstrap


def main():

    analytical_dashboard = 'dashboards/analytical_dashboard.py'
    authors_dashboard = 'dashboards/author_search_app.py'
    bootstrap.run(analytical_dashboard, f'run.py {analytical_dashboard}', [])
    bootstrap.run(authors_dashboard, f'run.py {authors_dashboard}', [])


if __name__ == '__main__':
    print(f'test')
    main()
