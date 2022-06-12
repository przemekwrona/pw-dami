import pandas
from python.dami.experiments import expoeriment

from python.dami.sources import data


def run_experiment(k=1, test_size=0.2, mode='not defined'):
    print("Run experiment with GENDER data in mode {}".format(mode))

    expoeriment.run_experiment(dataset=data.load_gender(), clazz_name='gender',
                               test_size=test_size, k=k, dataset_name='gender', mode=mode, draw_plot=True)
