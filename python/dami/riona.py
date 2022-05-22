import numpy
import pandas

from python.dami.sources import data


def distance(v1, v2, types, class_name, minimum_values, maximum_values):
    s = 0.0

    for name, value in v1.items():
        if name == class_name:
            continue

        a = v2[name] - v1[name]
        d = maximum_values[name] - minimum_values[name]

        if types[name] == float:
            a = v2[name] - v1[name]
            d = maximum_values[name] - minimum_values[name]
            s += abs(a / d)

        if types[name] == int:
            if v1[name] - v2[name] == 0:
                s += 1
            else:
                s += 0

    return s


def distance_to_k_element(point, vectors, class_name, k=1):
    riona_distances = []
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(vectors)

    for index, vector in vectors.iterrows():
        riona_distances.append(distance(point, vector, vectors.dtypes, class_name, minimum_values, maximum_values))
    riona_distances.sort()

    return riona_distances[k - 1]


def predict(subset, point, clazz_name, grouped_global_data):
    rules = pandas.DataFrame()
    consistent2 = pandas.DataFrame()

    for index, row in subset.iterrows():
        rule = get_rule(point, row, clazz_name)
        rules = rules.append(rule)
        consistent = get_consistent(rule, subset, clazz_name)
        consistent2 = consistent2.append(consistent)

    grouped_subset_data = subset.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))
    grouped_consistency_data = consistent2.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))

    decision_matrix = pandas.DataFrame()
    decision_matrix['subset'] = grouped_consistency_data / grouped_subset_data
    decision_matrix['global'] = grouped_consistency_data / grouped_global_data

    return decision_matrix['subset'].idxmax(), decision_matrix['global'].idxmax()


def get_rule(v1, v2, clazz_name):
    rule = pandas.DataFrame()
    for name, column in v2.items():
        if name == clazz_name:
            rule[name] = [v2[name], v2[name]]
        elif v2[name].dtype == float and v1[name] > v2[name]:
            rule[name] = [v2[name], v1[name]]
        elif v2[name].dtype == float and v1[name] <= v2[name]:
            rule[name] = [v1[name], v2[name]]
        elif v2[name].dtype == int and v1[name] == v2[name]:
            rule[name] = [v1[name], v2[name]]
        elif v2[name].dtype == int and v1[name] != v2[name]:
            rule[name] = [0, float('inf')]

    return rule


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
