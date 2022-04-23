import numpy
import numpy as np


def init_random_centroids(data, number_of_class):
    max_value = np.amax(data, axis=0)
    min_value = np.amin(data, axis=0)

    dimension = len(data[0])

    centroid = []

    for i in range(number_of_class):
        init_centroid = np.random.randint(low=min_value[i], high=max_value[i], size=dimension)
        centroid.append(init_centroid)

    return centroid


def distance_to_centroid(centroid, vector):
    subtract = np.subtract(centroid, vector)
    power = np.power(subtract, 2)
    return np.sqrt(np.sum(np.power(np.subtract(centroid, vector), 2)))


def calculate_centroid(data):
    return np.sum(data, axis=0) / len(data)


def calculate_centroids(grouped_data):
    centroids = []

    for data_in_class in grouped_data:
        centroids.append(calculate_centroid(data_in_class))

    return centroids


def get_last_centroid(centroids):
    return centroids[len(centroids) - 1]


def calculate_max_error(centroids_1, centroids_2):
    sum_of_square_error = numpy.sum(numpy.power(numpy.subtract(centroids_1, centroids_2), 2), axis=0)
    return numpy.max(numpy.sqrt(sum_of_square_error))


def knn(data, number_of_class: int, epsilon=0.005):
    centroids = [init_random_centroids(data, number_of_class)]

    print("Init centroids")
    print(np.array(centroids[0]).tolist())

    while True:

        grouped_data = []
        for i in range(number_of_class):
            grouped_data.append([])

        for vector in data:

            minimal_distance = float('inf')
            assigned_class = None

            for class_id, centroid in enumerate(get_last_centroid(centroids)):
                current_distance = distance_to_centroid(centroid, vector)

                if current_distance < minimal_distance:
                    minimal_distance = current_distance
                    assigned_class = class_id

            grouped_data[assigned_class].append(vector)

        updated_centroid = calculate_centroids(grouped_data)

        centroids.append(updated_centroid)

        error = calculate_max_error(centroids[len(centroids) - 2], centroids[len(centroids) - 1])

        print(np.array(centroids[len(centroids) - 1]).tolist())
        print(error)

        if error <= epsilon:
            break
