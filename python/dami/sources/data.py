import math
import pandas


def load_gender():
    headers = ['height', 'weight', 'gender']
    dtypes = {'height': 'float', 'weight': 'float', 'gender': 'int'}

    return pandas.read_csv('./resources/gender.dat', delimiter=' ', names=headers, dtype=dtypes)


def load_heart():
    # Attribute Information:
    # ------------------------
    # -- 1. age
    # -- 2. sex
    # -- 3. chest pain type (4 values)
    # -- 4. resting blood pressure
    # -- 5. serum cholesterol in mg/dl
    # -- 6. fasting blood sugar > 120 mg/dl
    # -- 7. resting electrocardiographic results (values 0,1,2)
    # -- 8. maximum heart rate achieved
    # -- 9. exercise induced angina
    # -- 10. oldpeak = ST depression induced by exercise relative to rest
    # -- 11. the slope of the peak exercise ST segment
    # -- 12. number of major vessels (0-3) colored by flourosopy
    # -- 13. thal: 3 = normal; 6 = fixed defect; 7 = reversable defect

    headers = ['age', 'sex', 'chest pain type', 'resting blood pressure', 'serum cholesterol', 'fasting blood sugar',
               'resting electrocardiographic results', 'maximum heart rate achieved', 'exercise induced angina',
               'oldpeak', 'the slope of the peak exercise ST segment', 'number of major vessels', 'thal',
               'presence of heart disease']
    dtypes = {'age': 'float',
              'sex': 'int',
              'chest pain type': 'int',
              'resting blood pressure': 'float',
              'serum cholesterol': 'float',
              'fasting blood sugar': 'int',  # boolean
              'resting electrocardiographic results': 'int',
              'maximum heart rate achieved': 'float',
              'exercise induced angina': 'int',
              'oldpeak': 'float',
              'the slope of the peak exercise ST segment': 'float',
              'number of major vessels': 'float',
              'thal': 'int',
              'presence of heart disease': 'int'}

    f = pandas.read_csv('./resources/heart.dat', delimiter=' ', names=headers, dtype=dtypes)

    return f


def count_elements_by_distance_less_than(point, grouped_data, distance):
    number_of_vectors = 0

    for index, vector in grouped_data.iterrows():
        calculated_distance = 0
        for i in range(len(point)):
            calculated_distance = calculated_distance + math.pow(vector[i] - point[i], 2)

        if math.sqrt(calculated_distance) <= distance:
            number_of_vectors = number_of_vectors + 1
    return number_of_vectors


def find_minimum_and_maximum_values(data):
    minimum_values = data.min()
    maximum_values = data.max()

    print("Minimum values {}\n".format(minimum_values))
    print("Maximum values {}".format(maximum_values))

    return minimum_values, maximum_values
