from python.dami.sources import data
from python.dami import riona


def run_experiment():
    print("Run experiment with HEART data")

    heart_data = data.load_heart()
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(heart_data)

    point = [44.0, 1.0, 4.0, 110.0, 197.0, 0.0, 2.0, 177.0, 0.0, 0.0, 1.0, 1.0, 3.0]

    distance_to_k_element = riona.distance_to_k_element(point, heart_data, k=5)
