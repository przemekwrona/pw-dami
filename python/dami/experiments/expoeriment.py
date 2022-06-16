import numpy
import pandas
import math
import csv
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, plot_confusion_matrix
from python.dami import riona
from python.dami.sources import data
from python.dami.plots import plot
from pretty_confusion_matrix import pp_matrix_from_data
from sklearn.model_selection import KFold


def run_experiment(dataset, clazz_name, test_size=0.2, k=1, fold=3, dataset_name='unknown', mode='not defined',
                   draw_plot=False):
    start_time = datetime.datetime.now()

    learn_data, test_data = train_test_split(dataset, test_size=test_size)
    minimum_values, maximum_values = data.find_minimum_and_maximum_values(dataset)
    grouped_global_data = learn_data.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))

    if k == 'max':
        k = math.ceil(math.sqrt(len(learn_data)))
        print("k max is equal: {}".format(k))
    elif k == 'optimal':
        k_max = math.ceil(math.sqrt(len(learn_data)))
        k = riona.find_k_optimal(learn_data=learn_data, test_data=test_data, clazz_name=clazz_name,
                                 minimum_values=minimum_values, maximum_values=maximum_values, k_max=k_max,
                                 grouped_global_data=grouped_global_data)
        print("k optimal is equal: {}".format(k))
    else:
        print("k is equal: {}".format(k))

    # Uncomment if you want test specific example
    # learn_data = dataset
    # test_data = pandas.DataFrame(data={'height': [170], 'weight': [60], 'gender': [2]})

    if draw_plot:
        if len(dataset.columns) - 1 == 2:
            plot.draw(dataset, clazz_name)
            plot.draw(learn_data, clazz_name)
            plot.draw(test_data, clazz_name)
        else:
            print("You can not draw 2D chart. Vector contains {} dimensions".format(len(dataset.columns) - 1))

    results = pandas.DataFrame()

    filename = 'results/OUT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}.csv'.format(
        attributes=len(dataset.columns),
        rows=len(learn_data), k=k,
        dataset=dataset_name)

    with open(filename, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)

        header = numpy.array(['original position'])
        header = numpy.concatenate((header, dataset.columns.to_numpy()))
        header = numpy.concatenate((header, numpy.array(['k+NN_i'])))
        header = numpy.concatenate((header, numpy.array(['promising k+NN_i'])))
        header = numpy.concatenate((header, numpy.array(['k+NN_i ids'])))
        header = numpy.concatenate((header, numpy.array(['promising k+NN_i ids'])))
        header = numpy.concatenate((header, numpy.array(['standard d(x)'])))
        header = numpy.concatenate((header, numpy.array(['normalized d(x)'])))
        writer.writerow(header)

        # write a row to the csv file
        for index, test_instance in test_data.iterrows():
            distance_to_k_element = riona.distance_to_k_element(test_instance, learn_data, clazz_name, k=k)

            closest_objects = data.find_elements_by_distance_less_than(learn_data, test_instance, distance_to_k_element,
                                                                       clazz_name, minimum_values, maximum_values)
            closest_objects = closest_objects.astype(learn_data.dtypes)
            if draw_plot:
                if len(dataset.columns) - 1 == 2:
                    plot.draw_closest_point(learn_data, closest_objects, 'gender', test_instance, minimum_values,
                                            maximum_values, k=k)

            k_nearest, promising_k_nearest, k_nearest_ids, promising_k_nearest_ids, standard_decision, global_decision = riona.predict(
                closest_objects, test_instance, clazz_name, grouped_global_data)

            row = numpy.array([index])
            row = numpy.concatenate((row, test_instance.to_numpy()))
            row = numpy.concatenate((row, numpy.array([k_nearest])))
            row = numpy.concatenate((row, numpy.array([promising_k_nearest])))
            row = numpy.concatenate((row, numpy.array(["{}".format(numpy.array(k_nearest_ids))])))
            row = numpy.concatenate((row, numpy.array(["{}".format(numpy.array(promising_k_nearest_ids))])))
            row = numpy.concatenate((row, numpy.array([standard_decision])))
            row = numpy.concatenate((row, numpy.array([global_decision])))
            writer.writerow(row)

            results = results.append(pandas.DataFrame(
                data={'true_value': [test_instance[clazz_name]], 'subset_prediction': [standard_decision],
                      'global_decision': [global_decision]}))

    end_time = datetime.datetime.now()

    total_time = end_time - start_time

    if mode == 'STAND':
        standard_accuracy = accuracy_score(results['true_value'], results['subset_prediction'])
        print('Confusion matrix with subset, k = {}, accuracy: {:.2f}%'.format(k, 100 * standard_accuracy))
        print(confusion_matrix(results['true_value'], results['subset_prediction']))
        # pp_matrix_from_data(results['true_value'], results['subset_prediction'], cmap='PuRd', fz=24, figsize=[5, 5])

        stat_filename_in_standard_mode = 'results/STAT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}_{mode}.txt'.format(
            attributes=len(dataset.columns),
            rows=len(learn_data), k=k, mode=mode.lower(),
            dataset=dataset_name)

        with open(stat_filename_in_standard_mode, 'w', encoding='UTF8', newline='') as statistic_file:
            statistic_file.write(
                'Confusion matrix in standard  mode, k = {}, accuracy: {:.2f}%\n'.format(k, 100 * standard_accuracy))
            statistic_file.write('Program was running for {time} second.\n'.format(time=total_time.seconds))
            confusion_matrix_results = confusion_matrix(results['true_value'], results['subset_prediction'])
            calculate_accuracy(confusion_matrix_results, statistic_file)
            k_fold(dataset, statistic_file, fold=fold)

    if mode == 'NORM':
        normalized_accuracy = accuracy_score(results['true_value'], results['global_decision'])
        print('Confusion matrix with global decision, k = {}, accuracy: {:.2f}%'.format(k, 100 * normalized_accuracy))
        print(confusion_matrix(results['true_value'], results['global_decision']))
        # pp_matrix_from_data(results['true_value'], results['global_decision'], cmap='PuRd', fz=24, figsize=[5, 5])

        stat_filename_in_normalized_mode = 'results/STAT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}_{mode}.txt'.format(
            attributes=len(dataset.columns),
            rows=len(learn_data), k=k, mode=mode.lower(),
            dataset=dataset_name)

        with open(stat_filename_in_normalized_mode, 'w', encoding='UTF8', newline='') as statistic_file:
            statistic_file.write(
                'Confusion matrix in normalized mode, k = {}, accuracy: {:.2f}%\n'.format(k, 100 * normalized_accuracy))
            statistic_file.write('Program was running for {time} second\n.'.format(time=total_time.seconds))
            confusion_matrix_results = confusion_matrix(results['true_value'], results['subset_prediction'])

            calculate_accuracy(confusion_matrix_results, statistic_file)
            k_fold(dataset, statistic_file, fold=fold)


def k_fold(dataset, file, fold):
    kf = KFold(n_splits=fold, shuffle=True)
    kf.get_n_splits(dataset)

    iteration = 1

    for train_index, test_index in kf.split(dataset):
        # file.write("\nKFold iteration: {}".format(iteration))
        # print("TRAIN:", train_index, "\nTEST:", test_index)
        # X_train, X_test = X[train_index], X[test_index]
        # y_train, y_test = y[train_index], y[test_index]
        iteration = iteration + 1


def calculate_accuracy(confusion_matrix_results, statistic_file):
    statistic_file.write(numpy.array2string(confusion_matrix_results))

    for i in range(0, len(confusion_matrix_results)):
        acc = confusion_matrix_results[i][i] / sum(confusion_matrix_results[i]) * 100
        statistic_file.write("Accuracy for class {} is equal {:.2f}%\n\n".format(i, acc))

        print("Accuracy for class {} is equal {:.2f}%\n".format(i, acc))


def run_experiment_with_fold(dataset, clazz_name, test_size=0.2, k=1, dataset_name='unknown', mode='not defined',
                             draw_plot=False):
    start_time = datetime.datetime.now()

    minimum_values, maximum_values = data.find_minimum_and_maximum_values(dataset)

    learn_data, test_data = train_test_split(dataset, test_size=test_size)
    grouped_global_data = learn_data.groupby(by=[clazz_name]).agg(count=(clazz_name, 'count'))

    if k == 'max':
        k = math.ceil(math.sqrt(len(learn_data)))
        print("k max is equal: {}".format(k))
    elif k == 'optimal':
        k_max = math.ceil(math.sqrt(len(learn_data)))
        k = riona.find_k_optimal(learn_data=learn_data, test_data=test_data, clazz_name=clazz_name,
                                 minimum_values=minimum_values, maximum_values=maximum_values, k_max=k_max,
                                 grouped_global_data=grouped_global_data)
        print("k optimal is equal: {}".format(k))
    else:
        print("k is equal: {}".format(k))

    # Uncomment if you want test specific example
    # learn_data = dataset
    # test_data = pandas.DataFrame(data={'height': [170], 'weight': [60], 'gender': [2]})

    if draw_plot:
        if len(dataset.columns) - 1 == 2:
            plot.draw(learn_data, clazz_name)
        else:
            print("You can not draw 2D chart. Vector contains {} dimensions".format(len(dataset.columns) - 1))

    results = pandas.DataFrame()

    filename = 'results/OUT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}.csv'.format(
        attributes=len(dataset.columns),
        rows=len(learn_data), k=k,
        dataset=dataset_name)

    with open(filename, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)

        header = numpy.array(['original position'])
        header = numpy.concatenate((header, dataset.columns.to_numpy()))
        header = numpy.concatenate((header, numpy.array(['k+NN_i'])))
        header = numpy.concatenate((header, numpy.array(['promising k+NN_i'])))
        header = numpy.concatenate((header, numpy.array(['standard d(x)'])))
        header = numpy.concatenate((header, numpy.array(['normalized d(x)'])))
        writer.writerow(header)

        # write a row to the csv file
        for index, test_instance in test_data.iterrows():
            distance_to_k_element = riona.distance_to_k_element(test_instance, learn_data, clazz_name, k=k)

            closest_objects = data.find_elements_by_distance_less_than(learn_data, test_instance, distance_to_k_element,
                                                                       clazz_name, minimum_values, maximum_values)
            closest_objects = closest_objects.astype(learn_data.dtypes)
            if draw_plot:
                if len(dataset.columns) - 1 == 2:
                    plot.draw_closest_point(learn_data, closest_objects, 'gender', test_instance, minimum_values,
                                            maximum_values, k=k)

            k_nearest, promising_k_nearest, standard_decision, global_decision = riona.predict(closest_objects,
                                                                                               test_instance,
                                                                                               clazz_name,
                                                                                               grouped_global_data)

            row = numpy.array([index])
            row = numpy.concatenate((row, test_instance.to_numpy()))
            row = numpy.concatenate((row, numpy.array([k_nearest])))
            row = numpy.concatenate((row, numpy.array([promising_k_nearest])))
            row = numpy.concatenate((row, numpy.array([standard_decision])))
            row = numpy.concatenate((row, numpy.array([global_decision])))
            writer.writerow(row)

            results = results.append(pandas.DataFrame(
                data={'true_value': [test_instance[clazz_name]], 'subset_prediction': [standard_decision],
                      'global_decision': [global_decision]}))

    end_time = datetime.datetime.now()

    total_time = end_time - start_time

    if mode == 'STAND':
        standard_accuracy = accuracy_score(results['true_value'], results['subset_prediction'])
        print('Confusion matrix with subset, k = {}, accuracy: {:.2f}%'.format(k, 100 * standard_accuracy))
        print(confusion_matrix(results['true_value'], results['subset_prediction']))
        # pp_matrix_from_data(results['true_value'], results['subset_prediction'], cmap='PuRd', fz=24, figsize=[5, 5])

        stat_filename_in_standard_mode = 'results/STAT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}_{mode}.txt'.format(
            attributes=len(dataset.columns),
            rows=len(learn_data), k=k, mode=mode.lower(),
            dataset=dataset_name)

        with open(stat_filename_in_standard_mode, 'w', encoding='UTF8', newline='') as statistic_file:
            statistic_file.write(
                'Confusion matrix in standard  mode, k = {}, accuracy: {:.2f}%\n'.format(k, 100 * standard_accuracy))
            statistic_file.write('Program was running for {time} second.\n'.format(time=total_time.seconds))
            statistic_file.write(
                numpy.array2string(confusion_matrix(results['true_value'], results['subset_prediction'])))

    if mode == 'NORM':
        normalized_accuracy = accuracy_score(results['true_value'], results['global_decision'])
        print('Confusion matrix with global decision, k = {}, accuracy: {:.2f}%'.format(k, 100 * normalized_accuracy))
        print(confusion_matrix(results['true_value'], results['global_decision']))
        # pp_matrix_from_data(results['true_value'], results['global_decision'], cmap='PuRd', fz=24, figsize=[5, 5])

        stat_filename_in_normalized_mode = 'results/STAT_NG-RIONA_{dataset}_A{attributes}_R{rows}_k{k}_{mode}.txt'.format(
            attributes=len(dataset.columns),
            rows=len(learn_data), k=k, mode=mode.lower(),
            dataset=dataset_name)

        with open(stat_filename_in_normalized_mode, 'w', encoding='UTF8', newline='') as statistic_file:
            statistic_file.write(
                'Confusion matrix in normalized mode, k = {}, accuracy: {:.2f}%\n'.format(k, 100 * normalized_accuracy))
            statistic_file.write('Program was running for {time} second\n.'.format(time=total_time.seconds))
            statistic_file.write(
                numpy.array2string(confusion_matrix(results['true_value'], results['global_decision'])))
