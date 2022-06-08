

PATH = '../data/category_cleared_description.txt'
CSV_PATH = '../data/category_cleared_description.csv'
ID_DICT = {
    "children's literature": 0,
    "science fiction": 1,
    "novel": 2,
    "fantasy": 3
}


def convert_to_csv(input_path, output_path):
    with open(input_path, encoding='utf-8') as file:
        lines = file.readlines()
    file = open(output_path, 'w+', encoding='utf-8')
    file.write('ID;CATEGORY;DESCRIPTION')
    for line in lines:
        split = line.split('|')
        category, description = split[0], split[1]
        description = " ".join([word for word in description.split() if not has_numbers(word)])
        cat_id = ID_DICT[category]
        save_line = f'\n{cat_id};{category};{description}'
        if description != '':
            file.write(save_line)
    file.close()


def has_numbers(word):
    for letter in word:
        if letter in '1234567890':
            return True
    return False


def main():
    print(has_numbers('propaganda1'))
    convert_to_csv(PATH, CSV_PATH)


if __name__ == '__main__':
    main()


