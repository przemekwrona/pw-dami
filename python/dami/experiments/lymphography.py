from python.dami.sources import data
from python.dami.experiments import expoeriment


def run_experiment(k=1, fold=3, mode='STAND'):
    print("Run experiment with LYMPHOGRAPHY data in mode {}".format(mode))

    expoeriment.run_experiment(dataset=data.load_lymphography(), clazz_name='class', test_size=0.2, k=k, fold=3,
                               dataset_name='lymphography', mode=mode, draw_plot=False)
