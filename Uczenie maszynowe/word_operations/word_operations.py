

PATH = '..\\data\\category_cleared_description.txt'


def main():
    with open(PATH, encoding='utf-8') as file:
        for line in file.readlines():
            split = line.split()
            category = split[0]
            print(category)


if __name__ == '__main__':
    main()


