import pandas as pd
import numpy as np
from transformers import pipeline
import torch
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
    n = 1500

    review_splitted = [(review[i:i + n]) for i in range(0, len(review), n)]
    global_stars = (classifier(review_splitted))

    return global_stars


def apply_sentiment_model(all_sites):
    try:
        all_sites['stars'] = all_sites['text'].apply(lambda x: sentiment_analysis_bert_base_multilingual_uncased(x))

    except RuntimeError:
        print(all_sites['game'])
        all_sites['stars'] = all_sites['text'].apply(lambda x: np.nan)

    finally:
        all_sites.to_csv('../data/labeled_texts1.csv', index=False)

    return all_sites


def stars_mean_to_score(review):
    points = []

    for classification in review:
        # Mean of fragment
        grade = int(classification['label'].split(' ')[0])
        points.append(grade)
    score = round(np.mean(points), 2)

    return (score)

all_sites['stars_mean'] = all_sites['stars'].apply(lambda x: stars_mean_to_score(x))

def score_half(score):
    '''Score reduced to compare with stars mean'''
    return score / 2

all_sites1['score_adj'] = all_sites1['score'].apply(lambda x: score_half(x))