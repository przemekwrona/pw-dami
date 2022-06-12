from python.dami.experiments import gender_v1
from python.dami.experiments import gender
from python.dami.experiments import heart
from python.dami.experiments import lymphography
from python.dami.experiments import spambase

if __name__ == '__main__':
    # gender.run_experiment(k=1, mode='STAND')
    # gender.run_experiment(k=3, mode='STAND')
    # gender.run_experiment(k='optimal', mode='STAND')
    # gender.run_experiment(k='max', mode='STAND')
    #
    # heart.run_experiment(k=1, mode='STAND')
    # heart.run_experiment(k=3, mode='STAND')
    # heart.run_experiment(k='optimal', mode='STAND')
    # heart.run_experiment(k='max', mode='STAND')
    #
    # heart.run_experiment(k=1, mode='NORM')
    # heart.run_experiment(k=3, mode='NORM')
    # heart.run_experiment(k='optimal', mode='NORM')
    # heart.run_experiment(k='max', mode='NORM')

    # lymphography.run_experiment(k=1, mode='STAND')
    # lymphography.run_experiment(k=3, mode='STAND')
    # lymphography.run_experiment(k='optimal', mode='STAND')
    # lymphography.run_experiment(k='max', mode='STAND')
    #
    # lymphography.run_experiment(k=1, mode='NORM')
    # lymphography.run_experiment(k=3, mode='NORM')
    # lymphography.run_experiment(k='optimal', mode='NORM')
    # lymphography.run_experiment(k='max', mode='NORM')

    spambase.run_experiment(k=1, mode='STAND')
    spambase.run_experiment(k=3, mode='STAND')
    spambase.run_experiment(k='optimal', mode='STAND')
    spambase.run_experiment(k='max', mode='STAND')

    spambase.run_experiment(k=1, mode='NORM')
    spambase.run_experiment(k=3, mode='NORM')
    spambase.run_experiment(k='optimal', mode='NORM')
    spambase.run_experiment(k='max', mode='NORM')
