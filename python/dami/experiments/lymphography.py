from python.dami.sources import data
from python.dami.experiments import expoeriment


def run_experiment(k=1):
    print("Run experiment with LYMPHOGRAPHY data")

    expoeriment.run_experiment(dataset=data.load_lymphography(), clazz_name='class', test_size=0.2, k=k,
                               draw_plot=False)
