from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline
from model_training import train_model
from sklearn.feature_selection import SelectKBest

CLEAR_PATH = '../data/category_cleared_description.csv'
STOPWORDS_PATH = '../data/category_cleared_description_with_stopwords.csv'

NAIVE_BAYES = Pipeline(steps=[
        ('select', SelectKBest()),
        ('vectorizer', CountVectorizer()),
        ('transformer', TfidfTransformer()),
        ('model', MultinomialNB())
    ])

NAIVE_BAYES_GRID = {
        'select__k': (5, 10, 20, "all"),  # Ile cech będzie brane pod uwagę
        'vectorizer__max_df': (0.5, 0.75),  #
        'vectorizer__ngram_range': [(1, 1), (1, 2)],
        'transformer__use_idf': [True, False],  # enable inverse document frequency reweighting
        'transformer__smooth_idf': [True, False],  # zapobiega dzieleniu przez 0, dodaje 1 do każdego wystąpinia,
        'transformer__sublinear_tf': [True, False],  # apply sublinear tf scaling, ładogzi wystąpienia słów (zamiast 20 dla 20 słów podawana jest wartość 1 + lg(20))
        'model__alpha': [0.01, 0.005, 0.001]  # 0 for no smoothing. Zapobiega zerowaniu prawdopodobieństwa jeśli jakieś słowo nigdy nie wystąpiło
    }


def main():
    train_model(NAIVE_BAYES, NAIVE_BAYES_GRID)


if __name__ == '__main__':
    main()

