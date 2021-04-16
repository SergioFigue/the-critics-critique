from streamlit import bootstrap


def main():

    real_script = 'dashboards/analytical_dashboard.py'
    bootstrap.run(real_script, f'run.py {real_script}', [])


if __name__ == '__main__':
    print(f'test')
    main()
