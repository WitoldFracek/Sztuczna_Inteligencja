import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

PATH = '..\\data\\category_full_description.txt'
SAVE_PATH = '..\\data\\category_cleared_description_with_stopwords.txt'


def remove_interpunction(description):
    words = nltk.word_tokenize(description)
    ret = [word for word in words if word.isalnum()]
    return ret


def remove_articles(words):
    ret = []
    for word in words:
        if word not in ['the', 'a', 'an']:
            ret.append(word)
    return ret


def remove_stop_words(words):
    ret = []
    for word in words:
        if word not in set(stopwords.words('english')):
            ret.append(word)
    return ret


def remove_pronounces(words):
    ret = []
    for word in words:
        if word not in ['you', 'your', 'yours',
                        'he', 'him', 'his',
                        'she', 'her', 'hers',
                        'we', 'us', 'our',
                        'they', 'them', 'their']:
            ret.append(word)
    return ret


def to_basic_form(words):
    ret = []
    lemmatizer = WordNetLemmatizer()
    for word in words:
        temp = lemmatizer.lemmatize(word, 'v')
        temp = lemmatizer.lemmatize(temp, 'n')
        ret.append(temp)
    return ret


def get_clear_descriptions(path):
    ret = []
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        split = line.split('|')
        category = split[0]
        description = ' '.join(split[1:])
        words = remove_interpunction(description)
        #words = remove_articles(words)
        #words = remove_pronounces(words)
        #words = remove_stop_words(words)
        #words = to_basic_form(words)
        new_description = " ".join(words)
        ret.append((category, new_description))
        if i % 100 == 1:
            print(i / len(lines) * 100)
    return ret


def save_clear_descriptions(path, save_path):
    ret = []
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
    with open(save_path, 'w+', encoding='utf-8') as file:
        for i, line in enumerate(lines):
            split = line.split('|')
            category = split[0]
            description = ' '.join(split[1:])
            words = remove_interpunction(description)
            # words = remove_articles(words)
            # words = remove_pronounces(words)
            # words = remove_stop_words(words)
            words = to_basic_form(words)
            new_description = " ".join(words)
            ret.append((category, new_description))
            if i % 100 == 1:
                print(i / len(lines) * 100)
            line = f'{category}|{new_description}\n'
            file.write(line)


if __name__ == '__main__':
    save_clear_descriptions(PATH, SAVE_PATH)



