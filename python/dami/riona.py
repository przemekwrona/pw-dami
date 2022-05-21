import numpy

from python.dami.sources import data


def distance(v1, v2, types, minimum_values, maximum_values):
    s = 0.0

    for index, column in enumerate(v1):
        a = v2[index] - v1[index]
        d = maximum_values[index] - minimum_values[index]

        if types[index] == float:
            a = v2[index] - v1[index]
            d = maximum_values[index] - minimum_values[index]
            s += abs(a / d)

        if types[index] == int:
            if v1[index] - v2[index] == 0:
                s += 1
            else:
                s += 0

    return s


def distance_to_k_element(point, vectors, k=1):
    riona_distances = []
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(vectors)

    # for index in range(0, len(vectors) + 1):
    #     riona_distances.append(distance(point, vectors[:-1], minimum_values, maximum_values))

    for index, vector in vectors.iterrows():
        riona_distances.append(distance(point, vector, vectors.dtypes, minimum_values, maximum_values))
    riona_distances.sort()

    return riona_distances[k - 1]
