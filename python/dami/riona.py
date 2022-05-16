from python.dami.sources.data import minimum_values, maximum_values


def distance(v1, v2):
    s = 0.0

    for index, column in enumerate(v2):
        a = v2[index] - v1[index]
        d = maximum_values[index] - minimum_values[index]

        s += abs(a / d)

    return s


def distance_to_k_element(point, vectors, k=1):
    riona_distances = []
    for index, vector in enumerate(vectors):
        riona_distances.append(distance(point, vector))
    riona_distances.sort()

    return riona_distances[k - 1]
