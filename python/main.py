import pandas as pd
import numpy as np

from dami.files import loader
from dami import knn

if __name__ == '__main__':
    print("Init project")
    loader.load_txt()

    data = np.array([
        [150, 50],
        [160, 55],
        [183, 80],
        [200, 99],
        [140, 45],
        [150, 50],
        [186, 74],
        [183, 84],
        [150, 50],
        [178, 77],
        [154, 62]
    ])

    knn.knn(data, 2)
