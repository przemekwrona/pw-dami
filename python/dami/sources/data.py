import numpy as np
import math

data = np.array([
    [159, 45],
    [172, 61],
    [180, 65],
    [151, 64],
    [145, 55],
    [150, 74],
    [150, 50],
    [160, 55],
    [183, 80],
    [200, 99],
    [140, 45],
    [170, 71],
    [150, 50],
    [186, 74],
    [183, 84],
    [150, 50],
    [178, 77],
    [154, 62],
    [159, 60]
])


def count_elements_by_distance_less_than(point, grouped_data, distance):
    number_of_vectors = 0

    for vector in grouped_data:
        calculated_distance = 0
        for i in range(len(point)):
            calculated_distance = calculated_distance + math.pow(vector[i] - point[i], 2)

        if math.sqrt(calculated_distance) <= distance:
            number_of_vectors = number_of_vectors + 1
    return number_of_vectors
