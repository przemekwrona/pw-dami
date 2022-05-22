import pandas
from python.dami.experiments import expoeriment

from python.dami.sources import data


def run_experiment(k=1):
    print("Run experiment with GENDER data")

    expoeriment.run_experiment(dataset=data.load_gender(), clazz_name='gender',
                               test_size=0.3, k=k, draw_plot=True)
