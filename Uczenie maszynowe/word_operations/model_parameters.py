from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline
from model_training import train_model
from sklearn.feature_selection import SelectKBest, chi2

CLEAR_PATH = '../data/category_cleared_description.csv'
STOPWORDS_PATH = '../data/category_cleared_description_with_stopwords.csv'

NAIVE_BAYES = Pipeline(steps=[
    ('vectorizer', CountVectorizer()),
    ('transformer', TfidfTransformer()),
    ('select', SelectKBest(score_func=chi2)),
    ('model', MultinomialNB())
])

NAIVE_BAYES_GRID = {
    'select__k': (1000, 3000, "all"),  # Ile cech będzie brane pod uwagę
    'vectorizer__max_df': (0.5, 0.75),  # Ignoruje słowa o częstowtliwości występowanie większej niż podana
    'vectorizer__ngram_range': [(1, 1), (1, 2)],  # dolna i górna granica ngramów (1, 1) tylko unigramy, (1, 2) uni i bigramy
    'transformer__sublinear_tf': [True, False],  # apply sublinear tf scaling, ładogzi wystąpienia słów (zamiast 20 dla 20 słów podawana jest wartość 1 + lg(20))
    'model__alpha': [0.01, 0.001]  # 0 for no smoothing. Zapobiega zerowaniu prawdopodobieństwa jeśli jakieś słowo nigdy nie wystąpiło
}

TEST_GRID = {
    'select__k': (3000,),  # Ile cech będzie brane pod uwagę
    'vectorizer__max_df': (0.5,),  # Ignoruje słowa o częstowtliwości występowanie większej niż podana
    'vectorizer__ngram_range': [(1, 1)],  # dolna i górna granica ngramów (1, 1) tylko unigramy, (1, 2) uni i bigramy
    'transformer__use_idf': [True],  # enable inverse document frequency reweighting
    'transformer__smooth_idf': [True],  # zapobiega dzieleniu przez 0, dodaje 1 do każdego wystąpinia,
    'transformer__sublinear_tf': [True],  # apply sublinear tf scaling, ładogzi wystąpienia słów (zamiast 20 dla 20 słów podawana jest wartość 1 + lg(20))
    'model__alpha': [0.01]
}

VECTOR_MACHINE = Pipeline(steps=[
    ('vectorizer', CountVectorizer()),
    ('transformer', TfidfTransformer()),
    ('select', SelectKBest(score_func=chi2)),
    ('model', SVC())
])

VECTOR_MACHINE_GRID = {
    'select__k': (1000, 3000, "all"),  # Ile cech będzie brane pod uwagę
    'vectorizer__max_df': (0.5, 0.75),  # Ignoruje słowa o częstowtliwości występowanie większej niż podana
    'vectorizer__ngram_range': [(1, 1), (1, 2)],  # dolna i górna granica ngramów (1, 1) tylko unigramy, (1, 2) uni i bigramy
    'transformer__sublinear_tf': [True, False],  # apply sublinear tf scaling, ładogzi wystąpienia słów (zamiast 20 dla 20 słów podawana jest wartość 1 + lg(20))
    'model__kernel': ['poly'],  # wybór funkcji jądra
    'model__C': [0.1, 0.5, 0.9],  # jak bardzo chcemy uniknąć błędnej klasyfikacji. Duże C - mały margines linii rozdzielającej
    'model__degree': [2, 3]
}


def main():
    #train_model(NAIVE_BAYES, TEST_GRID, STOPWORDS_PATH)
    train_model(VECTOR_MACHINE, VECTOR_MACHINE_GRID, CLEAR_PATH)
    train_model(NAIVE_BAYES, NAIVE_BAYES_GRID, STOPWORDS_PATH)
    train_model(VECTOR_MACHINE, VECTOR_MACHINE_GRID, STOPWORDS_PATH)


if __name__ == '__main__':
    main()

