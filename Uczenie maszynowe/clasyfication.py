from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC



def nb_01(df, labels):
    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2,
                                                        shuffle=True)

    pipe_mnnb = Pipeline(steps=[
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('mnnb', MultinomialNB())])
    pgrid_mnnb = {
        "vect__max_df": (0.5, 0.75),
        'vect__ngram_range': [(1, 1), (1, 2)],
        'tfidf__use_idf': [True, False],
        'tfidf__smooth_idf': [True, False],
        'tfidf__sublinear_tf': [True, False],
        'mnnb__alpha': [0.01, 0.005, 0.001]
    }

    gs_mnnb = GridSearchCV(pipe_mnnb, pgrid_mnnb, cv=5, n_jobs=-1, verbose=10)
    classifier = gs_mnnb.fit(X_train, y_train)
    print("Train", gs_mnnb.score(X_train, y_train))
    print("Test", gs_mnnb.score(X_test, y_test))
    print(gs_mnnb.best_params_)
    preds_mnnb = gs_mnnb.predict(X_test)

    print(classification_report(y_test, preds_mnnb, target_names=labels))

    titles_options = [
        ("Confusion matrix, without normalization", None),
        ("Normalized confusion matrix", "true"),
    ]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            classifier,
            X_test,
            y_test,
            display_labels=labels,
            cmap=plt.cm.Blues,
            normalize=normalize,
        )
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)
    plt.show()


def svm_01(df, labels):
    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2,
                                                        shuffle=True)
    pipe_svm = Pipeline(steps=[
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('SVM', SVC())])
    pgrid_svm = {
        "SVM__C": [0.001, 0.1, 10, 100, 10e5],
        "SVM__gamma": [0.1, 0.01]
    }

    gs_svm = GridSearchCV(pipe_svm, pgrid_svm, cv=5, n_jobs=-1, verbose=10)
    classifier = gs_svm.fit(X_train, y_train)
    print("Train", gs_svm.score(X_train, y_train))
    print("Test", gs_svm.score(X_test, y_test))
    print(gs_svm.best_params_)
    preds_svm = gs_svm.predict(X_test)

    print(classification_report(y_test, preds_svm, target_names=labels))

    titles_options = [
        ("Confusion matrix, without normalization", None),
        ("Normalized confusion matrix", "true"),
    ]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            classifier,
            X_test,
            y_test,
            display_labels=labels,
            cmap=plt.cm.Blues,
            normalize=normalize,
        )
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)
    plt.show()
