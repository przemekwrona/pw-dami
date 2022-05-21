from sklearn.model_selection import train_test_split
from python.dami import riona
from python.dami.sources import data
from python.dami.plots import plot


def run_experiment(dataset, test_size=0.2, k=5, draw_plot=False):
    learn_data, test_data = train_test_split(dataset, test_size=test_size)

    minimum_values, maximum_values = data.find_minimum_and_maximum_values(learn_data)

    point = [170.0, 60.0, 2]

    # point = pandas.DataFrame(data={'height': [170], 'weight': [60], 'gender': [2]})

    distance_to_k_element = riona.distance_to_k_element(point, learn_data, k=k)

    closest_objects = data.find_elements_by_distance_less_than(learn_data, point, distance_to_k_element,
                                                               minimum_values, maximum_values)

    clazz = riona.assign_class(closest_objects, point)

    if draw_plot:
        if len(dataset.columns) - 1 == 2:
            plot.draw(learn_data, 'gender')
            # plot.draw_with_distance(gender_data, 'gender', point, minimum_values, maximum_values)
            plot.draw_closest_point(learn_data, closest_objects, 'gender', point, minimum_values, maximum_values, k=5)
        else:
            print("You can not draw 2D chart. Vector contains {} dimensions".format(len(dataset.columns) - 1))
