from sklearn.naive_bayes import GaussianNB, BernoulliNB, ComplementNB, CategoricalNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from word_operations import assess_model

# rozpatrywane modele
nb_models = [
    GaussianNB(),
    BernoulliNB(),
    ComplementNB(),
    CategoricalNB(),
    MultinomialNB()
]

svc_models = [
    SVC(C=2),
    SVC(C=3),
    SVC(C=4),
    SVC(kernel='poly', degree=1),  # rbf - radial basis function
    SVC(kernel='poly', degree=2),
    SVC(kernel='poly', degree=3),
    SVC(kernel='poly', degree=4),
    SVC(kernel='poly', degree=5),
    SVC(kernel='poly', degree=6),
]

vectorizers = [
    CountVectorizer(),
    TfidfVectorizer()
]

if __name__ == '__main__':
    assess_model(nb_models[0], vectorizers[0])
    #assess_model(svc_models[0], vectorizers[0])

