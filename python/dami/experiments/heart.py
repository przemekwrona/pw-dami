from python.dami.sources import data
from python.dami.experiments import expoeriment


def run_experiment(k=1, mode='STAND'):
    print("Run experiment with HEART data in mode {}".format(mode))

    expoeriment.run_experiment(dataset=data.load_heart(), clazz_name='presence of heart disease', test_size=0.2, k=k,
                               dataset_name='heart', mode=mode, draw_plot=False)
