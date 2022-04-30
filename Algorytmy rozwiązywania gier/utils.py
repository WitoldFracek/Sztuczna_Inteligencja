
def first(iterable, condition=lambda x: True):
    return next(elem for elem in iterable if condition(elem))


def first_index(iterable, condition=lambda x: True):
    return next(i for i, elem in enumerate(iterable) if condition(elem))
