import numpy
import numpy as np
import pandas
from sklearn.metrics import confusion_matrix, accuracy_score, plot_confusion_matrix

from python.dami.sources import data


def distance(v1, v2, types, class_name, minimum_values, maximum_values):
    s = 0.0

    for name, value in v1.items():
        if name == class_name:
            continue

        if types[name] == float:
            a = v2[name] - v1[name]
            d = maximum_values[name] - minimum_values[name]
            s += abs(a / d)

        if types[name] == int:
            if int(v1[name] - v2[name]) == 0:
                s += 0
            else:
                s += 1

    return s


def distance_to_k_element(point, vectors, class_name, k=1):
    riona_distances = []
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(vectors)

    for index, vector in vectors.iterrows():
        riona_distances.append(distance(point, vector, vectors.dtypes, class_name, minimum_values, maximum_values))
    riona_distances.sort()

    return riona_distances[k - 1]


def predict(k_nearest_subset, point, clazz_name, grouped_global_data):
    # rules = pandas.DataFrame()
    # consistent_dataset = pandas.DataFrame()
    consistent_dataset = k_nearest_subset.copy()

    for index, row in k_nearest_subset.iterrows():
        # row = row.astype(subset.dtypes)
        rule = get_rule(point, row, k_nearest_subset.dtypes, clazz_name)
        # rules = rules.append(rule)
        # consistent = get_consistent(rule, subset, clazz_name)
        # consistent_dataset = consistent_dataset.append(consistent)
        consistent_dataset = remove_inconsistent(rule, consistent_dataset, clazz_name)

    grouped_subset_data = k_nearest_subset.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))
    grouped_consistency_data = consistent_dataset.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))

    decision_matrix = pandas.DataFrame()
    decision_matrix['subset'] = grouped_consistency_data / grouped_subset_data
    decision_matrix['global'] = grouped_consistency_data / grouped_global_data

    return len(k_nearest_subset), len(consistent_dataset), k_nearest_subset.index, consistent_dataset.index, \
           decision_matrix['subset'].idxmax(), decision_matrix['global'].idxmax()


def get_rule(v1, v2, dtypes, clazz_name):
    rule = pandas.DataFrame()
    for name, column in v2.items():
        if name == clazz_name:
            rule[name] = [v2[name], v2[name]]
        elif dtypes[name] == float and v1[name] > v2[name]:
            rule[name] = [v2[name], v1[name]]
        elif dtypes[name] == float and v1[name] <= v2[name]:
            rule[name] = [v1[name], v2[name]]
        elif dtypes[name] == int and v1[name] == v2[name]:
            rule[name] = [v1[name], v2[name]]
        elif dtypes[name] == int and v1[name] != v2[name]:
            rule[name] = [0, float('inf')]

    return rule


def is_consistent(rule, subset, clazz_name):
    for i, row in subset.iterrows():
        for name, column in rule.items():
            if name == clazz_name:
                continue
            if rule[clazz_name][0] == row[clazz_name]:
                continue
            if not rule[name][0] <= row[name] <= rule[name][1]:
                return False

        return True


def get_consistent(rule, subset, clazz_name):
    consistent = pandas.DataFrame()
    for index, row in subset.iterrows():
        is_consistent = True
        for name, column in rule.items():
            if name == clazz_name:
                continue
            if not rule[name][0] <= row[name] <= rule[name][1]:
                is_consistent = False
                break

        if is_consistent:
            consistent = consistent.append(row)

    return consistent


def remove_inconsistent(rule, consistent_dataset, clazz_name):
    for index, row in consistent_dataset.iterrows():
        is_consistent = True
        if rule[clazz_name][0] != row[clazz_name]:

            for name, column in rule.items():
                if name == clazz_name:
                    continue
                if not rule[name][0] <= row[name] <= rule[name][1]:
                    is_consistent = False
                    break
            if is_consistent:
                consistent_dataset = consistent_dataset.drop(index)

    return consistent_dataset


def get_classification_vector(dataset, clazz_name, grouped_global_data, k_max, minimum_values, maximum_values):
    A = {}
    for r, row in dataset.iterrows():
        A[r] = {}
        for k in range(1, k_max + 1):
            A[r][k] = -1

    decision = {}
    for k in range(1, k_max + 1):
        decision[k] = {}
        for r, row in grouped_global_data.iterrows():
            decision[k][r] = 0

    number_of_class = len(grouped_global_data)
    current_decision = grouped_global_data.idxmax().iloc[0]

    for k in range(1, k_max + 1):
        for r, row in dataset.iterrows():

            d = distance_to_k_element(row, dataset, clazz_name, k)
            k_nearest = data.find_elements_by_distance_less_than(dataset, row, d, clazz_name, minimum_values,
                                                                 maximum_values)

            for n, near in k_nearest.iterrows():
                rule = get_rule(row, near, k_nearest.dtypes, clazz_name)
                has_consistency = is_consistent(rule, k_nearest, clazz_name)

                if has_consistency:
                    v = row[clazz_name]
                    decision[k][v] = decision[k][v] + 1
                    if decision[k][v] > decision[k][current_decision]:
                        current_decision = v

                A[r][k] = current_decision
    return A


def find_k_optimal(dataset, test_data, learn_data, clazz_name, minimum_values, maximum_values, grouped_global_data,
                   k_max):
    k_optimal = -1
    maximal_set_power = 0
    A = get_classification_vector(dataset=dataset, clazz_name=clazz_name, grouped_global_data=grouped_global_data,
                                  k_max=k_max, minimum_values=minimum_values, maximum_values=maximum_values)
    for k in range(1, k_max + 1):
        current_set_power = 0
        for r, row in dataset.iterrows():
            if A[r][k] == row[clazz_name]:
                current_set_power += 1
        if current_set_power > maximal_set_power:
            maximal_set_power = current_set_power
            k_optimal = k

    return k_optimal

    # for k in range(k_max):
    #     results = pandas.DataFrame()
    #
    #     print("k = {}".format(k))
    #
    #     for index, test_instance in test_data.iterrows():
    #         d = distance_to_k_element(test_instance, learn_data, clazz_name, k=k)
    #         closest_objects = data.find_elements_by_distance_less_than(learn_data, test_instance, d, clazz_name,
    #                                                                    minimum_values, maximum_values)
    #         closest_objects = closest_objects.astype(learn_data.dtypes)
    #
    #         k_nearest, promising_k_nearest, k_nearest_ids, k_promising_ids, standard_decision, global_decision = predict(
    #             closest_objects, test_instance,
    #             clazz_name,
    #             grouped_global_data)
    #         results = results.append(pandas.DataFrame(
    #             data={'true_value': [test_instance[clazz_name]], 'subset_prediction': [standard_decision],
    #                   'global_decision': [global_decision]}))
    #
    #     try:
    #         accuracy[k] = accuracy_score(results['true_value'], results['subset_prediction'])
    #     except:
    #         print("An exception occurred")
    #
    #     print("Accuracy: {:.2f}".format(accuracy[k]))
    #
    # accuracy_max = numpy.argmax(accuracy) + 1
    #
    # return accuracy_max
