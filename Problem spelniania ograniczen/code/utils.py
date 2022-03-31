from variable import Variable


def generate_equal_domain_values(size, domain: list) -> list[Variable]:
    ret = []
    counter = 0
    for i in range(size):
        for j in range(size):
            variable = Variable((i, j), domain, counter, empty_value_repr=-1)
            ret.append(variable)
            counter += 1
    return ret
