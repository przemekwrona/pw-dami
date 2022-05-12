from python.dami.sources.data import minimum_values, maximum_values


def distance(v1, v2):
    s = 0.0

    for index, column in enumerate(v2):
        a = v2[index] - v1[index]
        d = maximum_values[index] - minimum_values[index]

        s += abs(a / d)

    return s
