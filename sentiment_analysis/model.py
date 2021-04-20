import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def acquire(data):
    # The full study is based on data/all_sites.csv
    all_sites = pd.read_csv(data)
    all_sites = shuffle(all_sites)
    all_sites.reset_index(drop=True, inplace=True)
    print('Data loaded')
    return all_sites


def model_construction():
    # Select model
    nlp_model = 'nlptown/bert-base-multilingual-uncased-sentiment'
    tokenizer = AutoTokenizer.from_pretrained(nlp_model)
    model = AutoModelForSequenceClassification.from_pretrained(nlp_model)

    # Classifier
    classifier = pipeline(
            'sentiment-analysis',
            model=model,
            tokenizer=tokenizer)
    print('BERT base multilingual model loaded')

    return classifier


def sentiment_analysis_bert_base_multilingual_uncased(review, classifier):
    # Split large texts in fragments of 1500 words guarantees that you don't override BERT max tokens (512)
    n = 1500

    # Returns a vector with a BERT score per review fragment
    review_splitted = [(review[i:i+n]) for i in range(0, len(review), n)]
    global_stars = (classifier(review_splitted))

    return global_stars


def apply_sentiment_model(all_sites, classifier):
    print('Analysing sentiment may take hours depending on your words and rows count. Be patient...')
    try:
        all_sites['stars'] = all_sites['text'].apply(lambda x: sentiment_analysis_bert_base_multilingual_uncased(x, classifier))

    except RuntimeError:
        print(all_sites['game'])
        all_sites['stars'] = all_sites['text'].apply(lambda x: np.nan)

    # Uncomment these lines if you need a checkpoint
    # finally:
    #     all_sites.to_csv('../data/labeled_texts1.csv', index=False)

    return all_sites


def stars_mean_to_score(review):
    # Clean model results extracting only numeric score
    # Glue review fragments to return a unified mean NLP score per review

    points = []

    for classification in review:
        grade = int(classification['label'].split(' ')[0])
        points.append(grade)
    score = round(np.mean(points), 2)

    return score


def final_dataframe(all_sites):
    model = model_construction()
    all_sites = apply_sentiment_model(all_sites, model)
    all_sites['stars_mean'] = all_sites['stars'].apply(lambda x: stars_mean_to_score(x))
    all_sites['score_adj'] = all_sites['score'].apply(lambda x: x / 2)
    all_sites = all_sites[['site', 'author', 'game', 'score', 'score_adj', 'stars_mean', 'company', 'platform', 'genre']]
    print('New dataframe assambled. Proceeding to cleaning and standarizing raws...')

    return all_sites
