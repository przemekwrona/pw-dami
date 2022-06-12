from python.dami.sources import data
from python.dami.experiments import expoeriment


def run_experiment(k=1, mode='STAND'):
    print("Run experiment with SPAMBASE data in mode {}".format(mode))

    expoeriment.run_experiment(dataset=data.load_spambase(), clazz_name='spam', test_size=0.2, k=k,
                               dataset_name='spambase', mode=mode, draw_plot=False)
