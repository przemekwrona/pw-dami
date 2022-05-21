import pandas
from python.dami.experiments import expoeriment

from python.dami.sources import data


def run_experiment(k=1):
    print("Run experiment with GENDER data")

    expoeriment.run_experiment(dataset=data.load_gender(), test_size=0.2, k=5, draw_plot=True)
