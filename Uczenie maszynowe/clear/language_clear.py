import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

PATH = '..\\data\\category_full_description.txt'


def remove_interpunction(description):
    words = nltk.word_tokenize(description)
    ret = [word for word in words if word.isalnum()]
    return ret


def remove_articles(words):
    ret = []
    for word in words:
        if word not in ['the', 'a', 'at']:
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
    for line in lines:
        split = line.split('|')
        category = split[0]
        description = ' '.join(split[1:])
        words = remove_interpunction(description)
        words = remove_articles(words)
        words = remove_pronounces(words)
        words = remove_stop_words(words)
        words = to_basic_form(words)
        new_description = " ".join(words)
        ret.append((category, new_description))
    return ret


if __name__ == '__main__':
    clear = get_clear_descriptions(PATH)
    print(len(clear))
    for cat, des in clear:
        print(cat, ':', des)

    # lemmatizer = WordNetLemmatizer()
    # print(lemmatizer.lemmatize('car\'s', 'v'))
    # print(lemmatizer.lemmatize('car\'s', 'n'))



