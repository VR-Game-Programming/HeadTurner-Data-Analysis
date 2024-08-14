import csv
import pandas as pd
from Constant import *
from random import shuffle
from itertools import permutations


def generate_latin_square(lst):
    n = len(lst)
    latin_square = []
    for i in range(n):
        row = [lst[(j + i) % n] for j in range(n)]
        latin_square.append(row)
    return latin_square


def generate_formative_order(filename, subConditionName, subConditionList):
    filepath = "./Summative/Materials/" + filename
    data_rows = []

    header = ["Participant", "Condition"]
    for i in range(len(subConditionList)):
        header.append(f"{subConditionName}-" + str(i + 1))

    ConditionGroup = generate_latin_square(Conditions)
    subConditionGroup = generate_latin_square(subConditionList)

    for cList in ConditionGroup:
        for dList in subConditionGroup:
            temp = []
            for c in cList:
                line = [c] + dList
                temp.append(line)
            data_rows.append(temp)

    data_rows *= int(len(Participants) / len(data_rows))

    shuffle(data_rows)

    result = []
    for n in Participants:
        for d in data_rows[n - 1]:
            line = [n] + d
            result.append(line)

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in result:
            writer.writerow(row)

    print(f"Generated {filename} successfully!")


generate_formative_order("Summative_Order_S1.csv", "Direction", Directions)
generate_formative_order("Summative_Order_S2.csv", "Application", Applications)
