from python.dami.experiments import gender
from python.dami.experiments import gender_2
from python.dami.experiments import heart

if __name__ == '__main__':
    # gender.run_experiment()

    for k in [5]:
        gender_2.run_experiment(k=k)

        heart.run_experiment(k=k)
