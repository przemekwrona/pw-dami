from python.dami.sources import data
from python.dami.experiments import expoeriment


def run_experiment(k=1):
    print("Run experiment with HEART data")

    expoeriment.run_experiment(dataset=data.load_heart(), test_size=0.2, k=5, draw_plot=False)
