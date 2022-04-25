import math

from dami.files import loader
from dami import knn
from dami.plots import plot
from dami.sources import data


def aaa(point, data_in_class, distance):
    number_of_vectors = 0

    for row in data_in_class:
        calculated_distance = 0
        for i in range(len(point)):
            calculated_distance = calculated_distance + math.pow(row[i] - point[i], 2)

        if math.sqrt(calculated_distance) <= distance:
            number_of_vectors = number_of_vectors + 1
    return number_of_vectors


if __name__ == '__main__':
    # print("Init project")
    # loader.load_txt()

    grouped_data = knn.knn(data.data, 2)

    # plot.draw_classified_2d_data(grouped_data)

    plot.draw_classified_2d_data_with_test(grouped_data, 170, 60, 12)

    print("Number of elements in class 1: {}".format(len(grouped_data[0])))
    print("Number of elements in class 2: {} \n".format(len(grouped_data[1])))

    print("Number of elements in circle in class 1: {}".format(aaa([170, 60], grouped_data[0], 12)))
    print("Number of elements in circle in class 2: {} \n".format(aaa([170, 60], grouped_data[1], 12)))

    print("end of algorithm")
