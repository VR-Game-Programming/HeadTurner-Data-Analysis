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


def generate_formative_order(filename):
    filepath = "./Summative/Materials/" + filename
    data_rows = []

    header = ["Participant", "Condition"]
    for i in range(len(Directions)):
        header.append(f"Direction-" + str(i + 1))

    ConditionGroup = generate_latin_square(Conditions)
    DirectionGroup = generate_latin_square(Directions)

    for cList in ConditionGroup:
        for dList in DirectionGroup:
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


def find_idx_with_value(lst, value):
    for idx, val in enumerate(lst):
        if val == value:
            return idx
    return -1


def generate_application_order(filename):
    filepath = "./Summative/Materials/" + filename
    data_rows = []

    header = ["Participant", "Condition"]
    for i in range(len(Applications)):
        header.append(f"Application-" + str(i + 1))

    ConditionGroup = generate_latin_square(Conditions)
    ApplicationGroup = generate_latin_square(Applications)
    ClipGroup = generate_latin_square(EcosphereClips)
    ApplicationClipGroup = []

    for aList in ApplicationGroup:
        replaceIdx = find_idx_with_value(aList, "Ecosphere")
        for cList in ClipGroup:
            temp = []
            for c in cList:
                line = aList.copy()
                line[replaceIdx] = c
                temp.append(line)
            ApplicationClipGroup.append(temp)

    for cList in ConditionGroup:
        for aList in ApplicationClipGroup:
            temp = []
            for c, a in zip(cList, aList):
                line = [c] + a
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


# generate_formative_order("Summative_S1_Order.csv", "Direction", Directions)
generate_application_order("Summative_S2_Order.csv")
