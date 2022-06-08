import json
from clear.books_records import BookRecord


SELECTED_CATEGORIES = ['children\'s literature', 'fantasy', 'science fiction', 'novel']
PATH = '..\\data\\booksummaries.txt'


def convert_to_dict(text):
    json_dict = json.loads(text)
    return json_dict


def get_clear_line(split):
    ret = []
    for elem in split:
        if elem.startswith('{'):
            elem = convert_to_dict(elem)
        ret.append(elem)
    return ret


def load_to_book_object(clear_line) -> BookRecord:
    return BookRecord(
        clear_line[0],
        clear_line[1],
        clear_line[2],
        clear_line[3],
        clear_line[4],
        clear_line[5],
        clear_line[6]
    )


def categories_count(path):
    categories = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        split = line.lower().split('\t')
        clear = get_clear_line(split)
        br = load_to_book_object(clear)
        for category in br.categories:
            categories[category] = categories.setdefault(category, 0) + 1
    return categories


def select_over(count, treshold):
    ret = {}
    for key in count:
        if count[key] >= treshold:
            ret[key] = count[key]
    return ret


def get_book_record_list(path):
    with open(PATH, encoding='utf-8') as file:
        lines = file.readlines()
    br_list = []
    for line in lines:
        split = line.lower().split('\t')
        clear = get_clear_line(split)
        br = load_to_book_object(clear)
        br_list.append(br)
    return br_list


def restrict_categories(book_record_list: list[BookRecord], chosen: list[str]):
    ret = []
    for book_record in book_record_list:
        cat = book_record.categories
        for chosen_category in chosen:
            appended = False
            for category in cat:
                if chosen_category in category:
                    ret.append((chosen_category, book_record.description))
                    appended = True
                    break
            if appended:
                break
    return ret


def count_restricted_pairs(pairs):
    count = {}
    for cat, _ in pairs:
        count[cat] = count.setdefault(cat, 0) + 1
    return count


def restrict_description_length(pairs, longer_than: int):
    ret = []
    for cat, des in pairs:
        if len(des) > longer_than:
            ret.append((cat, des))
    return ret


def save_clear_category_description_pairs(path, pairs):
    with open(path, 'w+', encoding='utf-8') as file:
        for cat, des in pairs:
            line = f'{cat}|{des}'
            file.write(line)


def print_dict(pdict):
    for key in sorted(pdict):
        print(key, ':', pdict[key])


def main():
    # count = categories_count(PATH)
    # print_dict(count)
    br_list = get_book_record_list(PATH)
    pairs = restrict_categories(br_list, SELECTED_CATEGORIES)
    pairs = restrict_description_length(pairs, longer_than=20)
    save_clear_category_description_pairs('..\\data\\category_full_description.txt', pairs)
    # count = count_restricted_pairs(pairs)
    # print(len(pairs))
    # s = 0
    # for key in sorted(count):
    #     s += count[key]
    # for key in sorted(count):
    #     print(key, ":", count[key], count[key] / s * 100)







if __name__ == '__main__':
    main()


