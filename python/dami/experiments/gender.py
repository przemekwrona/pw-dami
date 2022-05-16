from python.dami import knn
from python.dami.plots import plot
from python.dami.sources import data
from python.dami import riona

import numpy as np


def run_experiment():
    number_of_class = 2

    grouped_data = knn.knn(data.data, number_of_class)

    # riona.find_minimum_and_maximum_values(data.data)

    # plot.draw_classified_2d_data(grouped_data)

    R = 12
    point = [170, 60]

    plot.draw_classified_2d_data(grouped_data)

    # plot.draw_classified_2d_data_with_test(grouped_data, point, R)

    distance_to_k_element = riona.distance_to_k_element(point, data.data, k=5)

    plot.draw_classified_2d_data_with_metric(grouped_data, point)

    plot.draw_classified_2d_data_with_metric(grouped_data, point, r=distance_to_k_element, k=5)

    for clazz in range(number_of_class):
        print("Number of elements in class {}: {} - {:.2f}%".format(
            clazz, len(grouped_data[clazz]), len(grouped_data[clazz]) / len(data.data) * 100))

    print("")

    for clazz in range(number_of_class):
        number_of_elements_in_clazz = knn.count_elements_by_class_and_distance_less_than(point, grouped_data[clazz], R)
        print("Number of elements in circle in class {} per total number of elements in class: {} - {:.2f}%".format(
            clazz, number_of_elements_in_clazz, number_of_elements_in_clazz / len(grouped_data[clazz]) * 100))

    print("")

    total_number_of_elements_in_range = data.count_elements_by_distance_less_than(point, data.data, R)
    for clazz in range(number_of_class):
        number_of_elements_in_clazz = knn.count_elements_by_class_and_distance_less_than(point, grouped_data[clazz], R)
        print("Number of elements in circle in class {} per total number of elements in circle: {} - {:.2f}%".format(
            clazz, number_of_elements_in_clazz, number_of_elements_in_clazz / total_number_of_elements_in_range * 100))

    print("\nend of algorithm")
