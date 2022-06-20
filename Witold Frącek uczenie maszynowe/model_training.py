import matplotlib.pyplot as pyl
import seaborn as sns; sns.set()
from sklearn.pipeline import make_pipeline, Pipeline
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB, BernoulliNB, ComplementNB, CategoricalNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer


def train_model(model, vectorizer, splits=3):
    print('Fetching data...')
    data_frame = pd.read_csv("../data/category_cleared_description.csv", encoding="utf-8", sep=';')
    categories = list(data_frame.drop_duplicates('CATEGORY').sort_values('ID')['CATEGORY'].values)
    descriptions = list(data_frame['DESCRIPTION'].values)
    split_descriptions = np.asarray([desc.split() for desc in descriptions], dtype=object)
    category_ids = np.asarray([elem for elem in list(data_frame["ID"].values)], dtype=object)

    #pipeline = make_pipeline(vectorizer, model)
    pipeline = Pipeline(steps=[
        ('vect', vectorizer),
        ('trnsform', TfidfTransformer()),
        ('model', model)
    ])

    print("Splitting data...")
    split = StratifiedShuffleSplit(n_splits=splits, test_size=0.3, random_state=0)
    split.get_n_splits(split_descriptions, category_ids)
    for train_index, test_index in split.split(split_descriptions, category_ids):
        x_train = split_descriptions[train_index]
        y_train = category_ids[train_index]
        x_test, y_test = split_descriptions[test_index], category_ids[test_index]
        print("Fitting...")
        print(x_train)
        x_train_v = vectorizer.fit_transform(x_train)
        y_train_v = vectorizer.fit_transform(y_train)
        pipeline.fit(x_train_v, y_train_v)
        predictions = pipeline.predict()
        mat = confusion_matrix(y_test, predictions, normalize=True)
        sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=categories, yticklabels=categories)
        pyl.xlabel('true')
        pyl.ylabel('predicted')
        pyl.show()


if __name__ == '__main__':
    train_model(GaussianNB(), CountVectorizer())


