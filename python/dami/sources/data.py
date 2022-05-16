import numpy as np
import math
import csv
import pandas


# gender_data = pandas.DataFrame(np.array([
#     [159, 45],
#     [172, 61],
#     [180, 65],
#     [151, 64],
#     [145, 55],
#     [150, 74],
#     [150, 50],
#     [160, 55],
#     [183, 80],
#     [200, 99],
#     [140, 45],
#     [170, 71],
#     [150, 50],
#     [186, 74],
#     [183, 84],
#     [150, 50],
#     [178, 77],
#     [154, 62],
#     [159, 60]
# ]), columns=['height', 'weight'])


def load_gender():
    headers = ['height', 'weight', 'gender']
    dtypes = {'height': 'float', 'weight': 'float', 'gender': 'int'}

    return pandas.read_csv('./resources/gender.dat', delimiter=' ', names=headers, dtype=dtypes)


def load_heart():
    headers = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12',
               'col13', 'col14']
    dtypes = {'col1': 'float', 'col2': 'float', 'col3': 'float', 'col4': 'float', 'col5': 'float', 'col6': 'float',
              'col7': 'float', 'col8': 'float', 'col9': 'float', 'col10': 'float', 'col11': 'float', 'col12': 'float',
              'col13': 'float', 'col14': 'float'}

    f = pandas.read_csv('./resources/heart.dat', delimiter=' ', names=headers, dtype=dtypes)

    # with open('./resources/heart.dat', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in spamreader:
    #         data.append(row)

    return f


def count_elements_by_distance_less_than(point, grouped_data, distance):
    number_of_vectors = 0

    for index, vector in grouped_data.iterrows():
        calculated_distance = 0
        for i in range(len(point)):
            calculated_distance = calculated_distance + math.pow(vector[i] - point[i], 2)

        if math.sqrt(calculated_distance) <= distance:
            number_of_vectors = number_of_vectors + 1
    return number_of_vectors


def find_minimum_and_maximum_values(data):
    minimum_values = data.min()
    maximum_values = data.max()

    print("Minimum values {}".format(minimum_values))
    print("Maximum values {}".format(maximum_values))

    return minimum_values, maximum_values
