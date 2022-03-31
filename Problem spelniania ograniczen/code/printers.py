

def pretty_binary_print(solution, mockup=None, empty_value_marker=None):
    for i, row in enumerate(solution):
        line = '|'
        for j, value in enumerate(row):
            if mockup is None:
                line = line + f' {" " if value.value is None else value.value} |'
            elif mockup[i, j] is None or mockup[i, j] == empty_value_marker:
                line = line + f' {" " if value.value is None else value.value} |'
            else:
                line = line + f'[{" " if value.value is None else value.value}]|'
        print(line)
