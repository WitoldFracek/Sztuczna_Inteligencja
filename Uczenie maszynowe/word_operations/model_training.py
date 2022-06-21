import matplotlib.pyplot as pyl
import seaborn as sns; sns.set()
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
from sklearn.metrics import confusion_matrix
from datetime import datetime
from sklearn import preprocessing

REPORT_PATH = '../reports/reports.txt'


def train_model(pipeline: Pipeline, grid, source_path):
    report_message = ''
    training_start = datetime.now()
    report_message += f'\n\nMODEL:   {pipeline["model"].__class__.__name__}\n'
    report_message += f'Started at {training_start}\n\n'
    print('Fetching data...')
    data_frame = pd.read_csv(source_path, encoding="utf-8", sep=';')
    categories = data_frame.drop_duplicates('CATEGORY').sort_values('ID')['CATEGORY'].values
    descriptions = np.array(data_frame['DESCRIPTION'].values)
    category_ids = np.asarray([elem for elem in list(data_frame["ID"].values)], dtype=int)
    step_end = datetime.now()
    report_message += f'Fetching:'.ljust(20) + f'{(step_end - training_start).seconds} s\n'

    print("Splitting data...")
    step_start = datetime.now()
    x_train, x_test, y_train, y_test = train_test_split(descriptions, category_ids, test_size=0.2, stratify=category_ids)
    step_end = datetime.now()
    report_message += f'Splitting:'.ljust(20) + f'{(step_end - step_start).seconds} s\n'

    print("Checking the grid...")
    step_start = datetime.now()
    search = GridSearchCV(pipeline, grid, n_jobs=-1, verbose=2)
    step_end = datetime.now()
    report_message += f'Checking grid:'.ljust(20) + f'{(step_end - step_start).seconds} s\n'

    print('Fitting data...')
    step_start = datetime.now()
    fitted: Pipeline = search.fit(x_train, y_train)
    step_end = datetime.now()
    report_message += f'Fitting:'.ljust(20) + f'{(step_end - step_start).seconds} s\n'

    train_score = fitted.score(x_train, y_train)
    print(f'Train score: {train_score}')
    report_message += f'Train score:'.ljust(20) + f'{train_score}\n'

    test_score = fitted.score(x_test, y_test)
    print(f'Test score: {test_score}')
    report_message += f'Test score:'.ljust(20) + f'{test_score}\n'

    predictions = fitted.predict(x_test)

    training_end = datetime.now()
    report_message += f'Whole process:'.ljust(20) + f'{(training_end - training_start).seconds}s\n'
    report_message += f'\nPARAMS:\n'

    # for key in search.cv_results_:
    #     report_message += f'{key}: {search.cv_results_[key]}\n'

    report_message += f'Mean score:'.ljust(30) + f'{search.cv_results_["mean_test_score"]}\n'
    report_message += f'Mean fit time:'.ljust(30) + f'{search.cv_results_["mean_fit_time"]}\n'

    # for key in search.best_params_:
    #     obj, attr = key.split('__')[0], key.split('__')[1]
    #     report_message += f'{obj} {attr}:'.ljust(30) + f'{search.best_params_[key]}\n'

    mat = confusion_matrix(y_test, predictions, normalize='true')
    sns.heatmap(mat.T, square=True, annot=True, fmt='f', cbar=False, xticklabels=categories, yticklabels=categories)
    pyl.xlabel('true')
    pyl.ylabel('predicted')
    pyl.show()

    with open(REPORT_PATH, 'a', encoding='utf-8') as file:
        file.write(report_message)


