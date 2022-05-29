import pandas
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, plot_confusion_matrix
from python.dami import riona
from python.dami.sources import data
from python.dami.plots import plot
from pretty_confusion_matrix import pp_matrix_from_data


def run_experiment(dataset, clazz_name, test_size=0.2, k=1, draw_plot=False):
    learn_data, test_data = train_test_split(dataset, test_size=test_size)

    if k == 'max':
        k = math.ceil(math.sqrt(len(learn_data)))

    # Uncomment if you want test specific example
    # learn_data = dataset
    # test_data = pandas.DataFrame(data={'height': [170], 'weight': [60], 'gender': [2]})

    if draw_plot:
        if len(dataset.columns) - 1 == 2:
            plot.draw(learn_data, clazz_name)
        else:
            print("You can not draw 2D chart. Vector contains {} dimensions".format(len(dataset.columns) - 1))

    minimum_values, maximum_values = data.find_minimum_and_maximum_values(learn_data)

    grouped_global_data = learn_data.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))

    results = pandas.DataFrame()
    for index, test_instance in test_data.iterrows():
        distance_to_k_element = riona.distance_to_k_element(test_instance, learn_data, clazz_name, k=k)

        closest_objects = data.find_elements_by_distance_less_than(learn_data, test_instance, distance_to_k_element,
                                                                   clazz_name, minimum_values, maximum_values)
        closest_objects = closest_objects.astype(learn_data.dtypes)
        if draw_plot:
            if len(dataset.columns) - 1 == 2:
                plot.draw_closest_point(learn_data, closest_objects, 'gender', test_instance, minimum_values,
                                        maximum_values, k=k)

        subset_decision, global_decision = riona.predict(closest_objects, test_instance, clazz_name,
                                                         grouped_global_data)

        results = results.append(pandas.DataFrame(
            data={'true_value': [test_instance[clazz_name]], 'subset_prediction': [int(subset_decision)],
                  'global_decision': [int(global_decision)]}))

    accuracy = accuracy_score(results['true_value'], results['subset_prediction'])
    print('Confusion matrix with subset, k = {}, accuracy: {:.2f}%'.format(k, 100 * accuracy))
    print(confusion_matrix(results['true_value'], results['subset_prediction']))
    # pp_matrix_from_data(results['true_value'], results['subset_prediction'], cmap='PuRd', fz=24, figsize=[5, 5])

    accuracy = accuracy_score(results['true_value'], results['global_decision'])
    print('Confusion matrix with global decision, k = {}, accuracy: {:.2f}%'.format(k, 100 * accuracy))
    print(confusion_matrix(results['true_value'], results['global_decision']))
    # pp_matrix_from_data(results['true_value'], results['global_decision'], cmap='PuRd', fz=24, figsize=[5, 5])
