import numpy as np
import matplotlib.pyplot as plt


def scatter_clazz(data):
    for clazz in data:
        vectors_in_class = np.asarray(clazz)
        x = vectors_in_class[:, 0]
        y = vectors_in_class[:, 1]
        plt.scatter(x, y)


def draw_classified_2d_data(data):
    scatter_clazz(data)

    plt.xlabel("Height")
    plt.ylabel("Weight")
    plt.grid()
    plt.show()


def draw_classified_2d_data_with_test(data, point, r=5):
    scatter_clazz(data)

    x, y = point
    plt.scatter(x, y, color='grey')
    circle = plt.Circle((x, y), r, color='grey', fill=False)
    plt.gca().add_patch(circle)

    plt.xlabel("Height")
    plt.ylabel("Weight")
    plt.grid()
    plt.show()
