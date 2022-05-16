import numpy as np

from python.dami.sources import data


def distance(v1, v2, minimum_values, maximum_values):
    s = 0.0

    for index, column in enumerate(v1):
        a = v2[index] - v1[index]
        d = maximum_values[index] - minimum_values[index]

        s += abs(a / d)

    return s


def distance_to_k_element(point, vectors, k=1):
    riona_distances = []
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(vectors)
    for index, vector in vectors.iterrows():
        riona_distances.append(distance(point, vector[:-1], minimum_values, maximum_values))
    riona_distances.sort()

    return riona_distances[k - 1]
