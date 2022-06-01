import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import GaussianNB, BernoulliNB, ComplementNB, CategoricalNB, MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedShuffleSplit


def model_with_vectorizer(model):
    vectorizer = CountVectorizer(stop_words='english')
    print('Fetching data...')
    data_frame = pd.read_csv("../data/category_cleared_description.csv", encoding="utf-8", sep=';')
    categories = list(data_frame.drop_duplicates('CATEGORY').sort_values('ID')['CATEGORY'].values)
    corpus: pd.Series = data_frame["DESCRIPTION"]
    x_features: csr_matrix = vectorizer.fit_transform(corpus)
    x_features = x_features.toarray()
    for fit in x_features[0]:
        print(fit)

    # y = df['ID']
    # sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=0)
    # sss.get_n_splits(x_features, y)
    # print("Performing split...")
    # train_index, test_index = next(sss.split(x_features, y))
    # X_train, X_test = x_features[train_index], x_features[test_index]
    # y_train, y_test = y[train_index], y[test_index]
    # print("Fitting...")
    # model.fit(X_train, y_train)
    # print("Running test...")
    # prediction = model.predict(X_test)
    # score = accuracy_score(y_test, prediction)
    # print(score)
    # return model, vectorizer, categories


if __name__ == '__main__':
    model_with_vectorizer(GaussianNB())


