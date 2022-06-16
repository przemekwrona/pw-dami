import math
import pandas
from python.dami import riona


def load_gender():
    # Attribute Information:
    # ------------------------
    # -- 1. height
    # -- 2. weight
    # -- 3. sex
    headers = ['height', 'weight', 'gender']
    dtypes = {'height': 'float', 'weight': 'int', 'gender': 'int'}

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

    return pandas.read_csv('./resources/heart.dat', delimiter=' ', names=headers, dtype=dtypes)


def load_lymphography():
    # --- NOTE: All attribute values in the database have been entered as
    #               numeric values corresponding to their index in the list
    #               of attribute values for that attribute domain as given below.
    #     1. class: normal find, metastases, malign lymph, fibrosis
    #     2. lymphatics: normal, arched, deformed, displaced
    #     3. block of affere: no, yes
    #     4. bl. of lymph. c: no, yes
    #     5. bl. of lymph. s: no, yes
    #     6. by pass: no, yes
    #     7. extravasates: no, yes
    #     8. regeneration of: no, yes
    #     9. early uptake in: no, yes
    #    10. lym.nodes dimin: 0-3
    #    11. lym.nodes enlar: 1-4
    #    12. changes in lym.: bean, oval, round
    #    13. defect in node: no, lacunar, lac. marginal, lac. central
    #    14. changes in node: no, lacunar, lac. margin, lac. central
    #    15. changes in stru: no, grainy, drop-like, coarse, diluted, reticular,
    #                         stripped, faint,
    #    16. special forms: no, chalices, vesicles
    #    17. dislocation of: no, yes
    #    18. exclusion of no: no, yes
    #    19. no. of nodes in: 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, >=70

    headers = ['class', 'lymphatics', 'block of affere', 'bl. of lymph. c', 'bl. of lymph. s', 'by pass',
               'extravasates', 'regeneration', 'early uptake in', 'lym.nodes dimin', 'lym.nodes enlar',
               'changes in lym.', 'defect in node', 'changes in node', 'changes in stru', 'special forms',
               'dislocation of', 'exclusion of no', 'no. of nodes in']

    dtypes = {'class': 'int',
              'lymphatics': 'int',
              'block of affere': 'int',
              'bl. of lymph. c': 'int',
              'bl. of lymph. s': 'int',
              'by pass': 'int',
              'extravasates': 'int',
              'regeneration': 'int',
              'early uptake in': 'int',
              'lym.nodes dimin': 'int',
              'lym.nodes enlar': 'int',
              'changes in lym.': 'int',
              'defect in node': 'int',
              'changes in node': 'int',
              'changes in stru': 'int',
              'special forms': 'int',
              'dislocation of': 'int',
              'exclusion of no': 'int',
              'no. of nodes in': 'int'
              }

    return pandas.read_csv('./resources/lymphography.data', delimiter=',', names=headers, dtype=dtypes)


def load_spambase():
    # 1, 0.    | spam, non-spam classes
    #
    # word_freq_make:         continuous.
    # word_freq_address:      continuous.
    # word_freq_all:          continuous.
    # word_freq_3d:           continuous.
    # word_freq_our:          continuous.
    # word_freq_over:         continuous.
    # word_freq_remove:       continuous.
    # word_freq_internet:     continuous.
    # word_freq_order:        continuous.
    # word_freq_mail:         continuous.
    # word_freq_receive:      continuous.
    # word_freq_will:         continuous.
    # word_freq_people:       continuous.
    # word_freq_report:       continuous.
    # word_freq_addresses:    continuous.
    # word_freq_free:         continuous.
    # word_freq_business:     continuous.
    # word_freq_email:        continuous.
    # word_freq_you:          continuous.
    # word_freq_credit:       continuous.
    # word_freq_your:         continuous.
    # word_freq_font:         continuous.
    # word_freq_000:          continuous.
    # word_freq_money:        continuous.
    # word_freq_hp:           continuous.
    # word_freq_hpl:          continuous.
    # word_freq_george:       continuous.
    # word_freq_650:          continuous.
    # word_freq_lab:          continuous.
    # word_freq_labs:         continuous.
    # word_freq_telnet:       continuous.
    # word_freq_857:          continuous.
    # word_freq_data:         continuous.
    # word_freq_415:          continuous.
    # word_freq_85:           continuous.
    # word_freq_technology:   continuous.
    # word_freq_1999:         continuous.
    # word_freq_parts:        continuous.
    # word_freq_pm:           continuous.
    # word_freq_direct:       continuous.
    # word_freq_cs:           continuous.
    # word_freq_meeting:      continuous.
    # word_freq_original:     continuous.
    # word_freq_project:      continuous.
    # word_freq_re:           continuous.
    # word_freq_edu:          continuous.
    # word_freq_table:        continuous.
    # word_freq_conference:   continuous.
    # char_freq_;:            continuous.
    # char_freq_(:            continuous.
    # char_freq_[:            continuous.
    # char_freq_!:            continuous.
    # char_freq_$:            continuous.
    # char_freq_#:            continuous.
    # capital_run_length_average: continuous.
    # capital_run_length_longest: continuous.
    # capital_run_length_total:   continuous.

    headers = ['spam', 'word_freq_make', 'word_freq_address', 'word_freq_all', 'word_freq_3d', 'word_freq_our',
               'word_freq_over', 'word_freq_internet', 'word_freq_order', 'word_freq_mail', 'word_freq_receive',
               'word_freq_will', 'word_freq_people', 'word_freq_report', 'word_freq_addresses', 'word_freq_free',
               'word_freq_business', 'word_freq_email', 'word_freq_you', 'word_freq_credit', 'word_freq_your',
               'word_freq_font', 'word_freq_000', 'word_freq_money', 'word_freq_hp', 'word_freq_hpl',
               'word_freq_george', 'word_freq_650', 'word_freq_lab', 'word_freq_labs', 'word_freq_telnet',
               'word_freq_857', 'word_freq_data', 'word_freq_415', 'word_freq_85', 'word_freq_technology',
               'word_freq_1999', 'word_freq_parts', 'word_freq_pm', 'word_freq_direct', 'word_freq_cs',
               'word_freq_meeting', 'word_freq_original', 'word_freq_project', 'word_freq_re', 'word_freq_edu',
               'word_freq_table', 'word_freq_conference', 'char_freq_;', 'char_freq_(', 'char_freq_[', 'char_freq_!',
               'char_freq_$', 'char_freq_#', 'capital_run_length_average', 'capital_run_length_longest',
               'capital_run_length_total']

    dtypes = {'spam': 'float',
              'word_freq_make': 'float',
              'word_freq_address': 'float',
              'word_freq_all': 'float',
              'word_freq_3d': 'float',
              'word_freq_our': 'float',
              'word_freq_over': 'float',
              'word_freq_internet': 'float',
              'word_freq_order': 'float',
              'word_freq_mail': 'float',
              'word_freq_receive': 'float',
              'word_freq_will': 'float',
              'word_freq_people': 'float',
              'word_freq_report': 'float',
              'word_freq_addresses': 'float',
              'word_freq_free': 'float',
              'word_freq_business': 'float',
              'word_freq_email': 'float',
              'word_freq_you': 'float',
              'word_freq_credit': 'float',
              'word_freq_your': 'float',
              'word_freq_font': 'float',
              'word_freq_000': 'float',
              'word_freq_money': 'float',
              'word_freq_hp': 'float',
              'word_freq_hpl': 'float',
              'word_freq_george': 'float',
              'word_freq_650': 'float',
              'word_freq_lab': 'float',
              'word_freq_labs': 'float',
              'word_freq_telnet': 'float',
              'word_freq_857': 'float',
              'word_freq_data': 'float',
              'word_freq_415': 'float',
              'word_freq_85': 'float',
              'word_freq_technology': 'float',
              'word_freq_1999': 'float',
              'word_freq_parts': 'float',
              'word_freq_pm': 'float',
              'word_freq_direct': 'float',
              'word_freq_cs': 'float',
              'word_freq_meeting': 'float',
              'word_freq_original': 'float',
              'word_freq_project': 'float',
              'word_freq_re': 'float',
              'word_freq_edu': 'float',
              'word_freq_table': 'float',
              'word_freq_conference': 'float',
              'char_freq_;': 'float',
              'char_freq_(': 'float',
              'char_freq_[': 'float',
              'char_freq_!': 'float',
              'char_freq_$': 'float',
              'char_freq_#': 'float',
              'capital_run_length_average': 'float',
              'capital_run_length_longest': 'float',
              'capital_run_length_total': 'float'
              }

    return pandas.read_csv('./resources/spambase.data', delimiter=',', decimal='.', names=headers, dtype=dtypes)


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

    # print("Minimum values {}\n".format(minimum_values))
    # print("Maximum values {}".format(maximum_values))

    return minimum_values, maximum_values


def find_elements_by_distance_less_than(data, point, distance_to_k_element, class_name, minimum_values, maximum_values):
    closest_object = pandas.DataFrame()
    for index, row in data.iterrows():
        if riona.distance(point, row, data.dtypes, class_name, minimum_values,
                          maximum_values) <= distance_to_k_element:
            closest_object = closest_object.append(row)
    return closest_object
