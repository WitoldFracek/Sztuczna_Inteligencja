import matplotlib.pyplot as pyl
import seaborn as sns; sns.set()
from sklearn.pipeline import make_pipeline, Pipeline
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
from sklearn.feature_selection import SelectFromModel
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB, BernoulliNB, ComplementNB, CategoricalNB, MultinomialNB
from sklearn.datasets import fetch_20newsgroups

from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer


def no_analyzer(doc):
    return doc


def train_model(pipeline, source_path):
    print('Fetching data...')
    data_frame = pd.read_csv("../data/category_cleared_description.csv", encoding="utf-8", sep=';')
    categories = np.array(data_frame.drop_duplicates('CATEGORY').sort_values('ID')['CATEGORY'].values)
    descriptions = np.array(data_frame['DESCRIPTION'].values)
    split_descriptions = np.array([desc.split() for desc in descriptions], dtype=object)
    category_ids = np.array([elem for elem in list(data_frame["ID"].values)], dtype=int)

    #pipeline = make_pipeline(vectorizer, model)
    pipeline = Pipeline(steps=[
        #('select', SelectFromModel(model)),
        ('vect', vectorizer),
        ('tran', transformer),
        ('model', model)
    ])

    print("Splitting data...")
    split = StratifiedShuffleSplit(n_splits=splits, test_size=0.3, random_state=0)
    split.get_n_splits(descriptions, category_ids)
    x_train, x_test, y_train, y_test = train_test_split(descriptions, category_ids, test_size=0.2, stratify=category_ids)
    print("Fitting...")

    fit_pipeline: Pipeline = pipeline.fit(x_train, y_train)
    predictions = fit_pipeline.predict(x_test)

    mat = confusion_matrix(y_test, predictions, normalize='true')
    sns.heatmap(mat.T, square=True, annot=True, fmt='f', cbar=False, xticklabels=categories, yticklabels=categories)
    pyl.xlabel('true')
    pyl.ylabel('predicted')
    pyl.show()

    # twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    #
    # x_train_v = vectorizer.fit_transform(x_train)
    # x_train_t = transformer.fit_transform(x_train_v)
    # print(type(twenty_train.target))
    # print(type(y_train))
    # model.fit(x_train_t, y_train)
    # print(x_train_v.shape)
    # x_train_t = transformer.fit_transform(x_train_v)
    # print(x_train_t.shape)

    # clf = model.fit(x_train, y_train)
    # selector = SelectFromModel(estimator=clf)
    # x_train_v = vectorizer.transform(x_train)
    # print(x_train_v.shape)
    # x_train_t = transformer.transform(x_train_v)
    # print(x_train_t.shape)
    # predicted = clf.predict(x_test)

    # y_train_v = vectorizer.fit_transform(y_train)
    # pipeline.fit(x_train_v, y_train_v)
    # predictions = pipeline.predict()


if __name__ == '__main__':
    train_model(MultinomialNB(), CountVectorizer(), TfidfTransformer())


