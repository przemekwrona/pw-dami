from dami import knn
from dami.plots import plot
from dami.sources import data

if __name__ == '__main__':
    number_of_class = 2

    grouped_data = knn.knn(data.data, number_of_class)

    # plot.draw_classified_2d_data(grouped_data)

    R = 12
    point = [170, 60]
    plot.draw_classified_2d_data_with_test(grouped_data, point, R)

    for clazz in range(number_of_class):
        print("Number of elements in class {}: {} - {:.2f}%".format(
            clazz, len(grouped_data[clazz]), len(grouped_data[clazz]) / len(data.data) * 100))

    total_number_of_elements_in_range = data.count_elements_by_distance_less_than(point, data.data, R)
    for clazz in range(number_of_class):
        number_of_elements_in_clazz = knn.count_elements_by_class_and_distance_less_than(point, grouped_data[clazz], R)
        print("Number of elements in circle in class {}: {} - {:.2f}%".format(
            clazz, number_of_elements_in_clazz, number_of_elements_in_clazz / total_number_of_elements_in_range * 100))

    print("\nend of algorithm")