import pandas as pd
import numpy as np
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def acquire(data):
    # The full study is based on data/all_sites.csv
    all_sites = pd.read_csv(data)
    return all_sites


# Select model
nlp_model = 'nlptown/bert-base-multilingual-uncased-sentiment'
tokenizer = AutoTokenizer.from_pretrained(nlp_model)
model = AutoModelForSequenceClassification.from_pretrained(nlp_model)

# Classifier
classifier = pipeline(
        'sentiment-analysis',
        model=model,
        tokenizer=tokenizer)


def sentiment_analysis_bert_base_multilingual_uncased(review):
    # Split large texts in fragments of 1500 words guarantees that you don't override BERT max tokens (512)
    n = 1500

    # Returns a vector with a BERT score per review fragment
    review_splitted = [(review[i:i + n]) for i in range(0, len(review), n)]
    global_stars = (classifier(review_splitted))

    return global_stars


def apply_sentiment_model(all_sites):
    try:
        all_sites['stars'] = all_sites['text'].apply(lambda x: sentiment_analysis_bert_base_multilingual_uncased(x))

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


def create_stars_mean_col(all_sites):
    all_sites['stars_mean'] = all_sites['stars'].apply(lambda x: stars_mean_to_score(x))

    return all_sites


def score_half(all_sites):
    # Score halved column for standardized comparison
    all_sites['score_adj'] = all_sites['score'].apply(lambda x: x/2)

    return all_sites


def final_dataframe(all_sites):
    scored_texts = all_sites[['site', 'author', 'game', 'score', 'score_adj',
                              'stars_mean', 'company', 'platform', 'genre']]

    return scored_texts
