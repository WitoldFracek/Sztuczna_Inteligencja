

if __name__ == '__main__':
    with open('../data/category_cleared_description.csv', encoding='utf-8') as file:
        lines = file.readlines()
    desc = [line.split(';')[2][:-1] for line in lines]
    for d in desc:
        #print(d)
        if len(d) < 3:
            print('l ' + str(d))
