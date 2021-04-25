

def drop_min_outliers(scored_texts):
    min_score_filter = scored_texts['score'] < 2
    scored_texts.drop(scored_texts[min_score_filter].index, inplace=True)

    return scored_texts


def platform_cleaning(scored_texts):
    scored_texts['platform'] = scored_texts['platform'].replace({'Xbox 360': '360',
                                                                 'XOne': 'Xbox One',
                                                                 'iOS': 'iPhone',
                                                                 '3DS': 'Nintendo 3DS',
                                                                 'WiiU': 'Wii U',
                                                                 'Nintendo Switch': 'Nintendo Switch',
                                                                 '\xa0· ': '',
                                                                 'X360': '360',
                                                                 'XBO': 'Xbox One',
                                                                 'IPH': 'iPhone',
                                                                 'IPD': 'iPad',
                                                                 'AND': 'Android',
                                                                 'NSW': 'Switch',
                                                                 'PSV': 'Vita',
                                                                 'GB': 'Game Boy',
                                                                 'STD': 'Stadia',
                                                                 'OSX': 'Mac',
                                                                 'PSVITA': 'Vita',
                                                                 'NDS': 'DS',
                                                                 'Ipad': 'iPad',
                                                                 'Nintendo DS': 'DS',
                                                                 'Móviles': 'Android'
                                                                 }, regex=True)

    return scored_texts


def game_cleaning(scored_texts):
    scored_texts['game'].replace({' - Análisis': '', 'Análisis de ': ''}, regex=True, inplace=True)

    return scored_texts


def author_cleaning(scored_texts):
    scored_texts['author'] = scored_texts['author'].replace({'(\D+)\\n': '', '(\D+) - @': ''}, regex=True)

    return scored_texts


def company_cleaning(scored_texts):
    scored_texts['company'] = scored_texts['company'].replace({'Bandai Namco Entertainment': 'Bandai Namco',
                                                               'Sony Computer Entertainment': 'Sony',
                                                               'Xbox Game Studios': 'Microsoft',
                                                               'Namco Bandai': 'Bandai Namco',
                                                               'Electronic Arts': 'EA',
                                                               'EA Sports': 'EA',
                                                               'THQ Nordic': 'THQ',
                                                               'Nordic Games': 'THQ',
                                                               'Microsoft Game Studios': 'Microsoft',
                                                               'Microsoft Studios': 'Microsoft',
                                                               'Warner Bros. Interactive Entertainment': 'Warner Bros.',
                                                               'Bethesda Softworks': 'Bethesda',
                                                               'Team 17': 'Team17',
                                                               'Blizzard Entertainment': 'Blizzard',
                                                               '2K Games': 'Take-Two Interactive',
                                                               '2K Sports': 'Take-Two Interactive',
                                                               '2K': 'Take-Two Interactive',
                                                               'Sony Interactive Entertainment': 'Sony',
                                                               'Sony Europe': 'Sony',
                                                               'Square-Enix': 'Square Enix',
                                                               'Koch Media': 'Deep Silver',
                                                               'Tecmo Koei': 'KoeTec',
                                                               'Koei Tecmo': 'KoeTec',
                                                               'Koei': 'KoeTec',
                                                               'Tecmo': 'KoeTec',
                                                               'Tecmo Koei Europe': 'KoeTec',
                                                               'The Pokémon Company': 'Nintendo',
                                                               'Rockstar Games': 'Rockstar',
                                                               'Nacon': 'Bigben Interactive',
                                                               'Sega': 'SEGA',
                                                               'Private Division': 'Take-Two Interactive',
                                                               'Take 2': 'Take-Two Interactive'
                                                               }, regex=True)

    return scored_texts


def score_deviation_func(scored_texts):
    scored_texts['score_deviation'] = (scored_texts['stars_mean'] - scored_texts['score_adj']) \
                                      / scored_texts['score_adj'] * 100

    scored_texts.to_csv('./new_scored_texts.csv', index=False)
    print('Your data is now fully operative. Proceed to analyze with Streamlit in a new browser tab.')

