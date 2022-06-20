import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import make_pipeline
import seaborn as sns; sns.set()
import matplotlib.pyplot as pyl


def assess_model(model, vectorizer, splits_number=3):
    print('Fetching data...')
    data_frame = pd.read_csv("../data/category_cleared_description.csv", encoding="utf-8", sep=';')
    categories = list(data_frame.drop_duplicates('CATEGORY').sort_values('ID')['CATEGORY'].values)
    corpus: pd.Series = data_frame["DESCRIPTION"]
    x_features: csr_matrix = vectorizer.fit_transform(corpus)
    x_features = x_features.toarray()

    y = data_frame['ID']
    print("Splitting data...")
    split = StratifiedShuffleSplit(n_splits=splits_number, test_size=0.3, random_state=0)
    split.get_n_splits(x_features, y)
    for train_index, test_index in split.split(x_features, y):
        X_train, X_test = x_features[train_index], x_features[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print("Fitting...")
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        score = accuracy_score(y_test, prediction)
        print(f"Score of split: {score}")
        mat = confusion_matrix(y_test, prediction)
        sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=categories, yticklabels=categories)
        pyl.xlabel('true')
        pyl.ylabel('predicted')
        pyl.show()

    return model, categories
