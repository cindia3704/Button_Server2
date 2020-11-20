import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

path = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(
    path+"/knn_edit.csv")
# print(data)
df_z = np.array(data["style"])
df_xy = data[["place1", "place2", "event1",
              "event2", "people1", "people2", "mood"]]
style_header = ["FORMAL", "SEMI-FORMAL",
                "CASUAL", "FREE-STYLE", "OUTDOOR", "VACANCE"]
data_xy = df_xy.values

# place1 = int(input('Place 1(1~4):'))
# place2 = int(input('Place 2(0~4):'))
# event1 = int(input('Event 1(1~8):'))
# event2 = int(input('Event 2(0~8):'))
# people1 = int(input('People 1(1~3):'))
# people2 = int(input('People 2(0~3):'))
# mood = int(input('mood (1~4):'))
# target = [place1, place2, event1, event2, people1, people2, mood]


def data_set(target):
    size = len(data_xy)
    class_target = np.tile(target, (size, 1))
    class_z = np.array(df_z)
    return df_xy, class_target, class_z


def classify(dataset, class_target, class_categoty, k):

    diffMat = class_target - dataset
    sqDiffMat = diffMat ** 2
    row_sum = sqDiffMat.sum(axis=1)
    distance = np.sqrt(row_sum)

    sortDist = distance.argsort()

    class_result = {}
    for i in range(k):
        c = class_categoty[sortDist[i]]
        class_result[c] = class_result.get(c, 0) + 1

    return class_result


def get_max_key(input_dict):
    max_value = -1
    max_key = None
    for k, v in input_dict.items():
        if v > max_value:
            max_value = v
            max_key = k
    return max_key


def knn_results(place1, place2, event1, event2, people1, people2, mood):
    # data = pd.read_csv("/Users/jisookim/Desktop/pythonProject/knn_edit.csv")

    # df_z = np.array(data["style"])
    # df_xy = data[["place1", "place2", "event1", "event2", "people1", "people2", "mood"]]
    # style_header = ["formal", "semiformal", "casual", "free-style", "outdoor", "vacance"]
    # data_xy = df_xy.values

    target = [place1, place2, event1, event2, people1, people2, mood]
    k = 3
    print(target)
    dataset, class_target, class_z = data_set(target)
    class_result = classify(data_xy, class_target, class_z, k)
    print(get_max_key(class_result))
    return style_header[get_max_key(class_result)-1]


#print(knn_results(1, 0, 1, 0, 1, 0, 1))
#k = int(input('k (1~5):'))
#class_result = classify(data_xy, class_target, class_z, k)
# print(style_header[get_max_key(class_result)-1])
# print(knn_results())
