import pandas as pd
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
import matplotlib.pyplot as plt
from Constant import *


max_trunk_dict = dict()
for pos in Postures:
    max_trunk_dict[pos] = dict()
    for dir in Directions:
        max_trunk_dict[pos][dir] = dict()
        for ang in ["TrunkYaw", "TrunkPitch"]:
            max_trunk_dict[pos][dir][ang] = list()


def FindMaximumValue(data_list):
    max = 0
    for value in data_list:
        if abs(value) > max:
            max = value
    return max


# Calculate mean of maximum trunk rotation in 3 tasks
for i in Participants:
    for pos in Postures:
        filepath = (
            "Result Raw (ReCalculate)/O3_Final/" + f"Formative_O3_P{i}_{pos}_Final.csv"
        )
        df = pd.read_csv(filepath)

        for dir in Directions:
            for ang in ["TrunkYaw", "TrunkPitch"]:
                max_list = list()
                for task in range(1, 4):
                    task_df = df.loc[df["Direction"] == dir].loc[df["tCount"] == task]
                    max_list.append(FindMaximumValue(task_df[ang]))
                max_trunk_dict[pos][dir][ang].append(stat.fmean(max_list))

# Calculate p-value: Wilcoxon signed-rank test
for dir in Directions:
    for ang in ["TrunkYaw", "TrunkPitch"]:
        print(f"{dir} {ang}")
        print(
            wilcoxon(
                max_trunk_dict["Lying"][dir][ang], max_trunk_dict["Standing"][dir][ang]
            )
        )

# Calculate mean between participants
for pos in Postures:
    for dir in Directions:
        for ang in ["TrunkYaw", "TrunkPitch"]:
            # Remove outlier
            for value in max_trunk_dict[pos][dir][ang]:
                if abs(value) > 50:
                    max_trunk_dict[pos][dir][ang].remove(value)
            max_trunk_dict[pos][dir][ang] = stat.fmean(max_trunk_dict[pos][dir][ang])

# Write to CSV
with open("Result Processed/O3_MaxTrunkRotation.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Type", "Direction", "Posture", "TrunkRotation"])
    for ang in ["TrunkYaw", "TrunkPitch"]:
        for dir in Directions:
            for pos in Postures:
                writer.writerow([ang, dir, pos, abs(max_trunk_dict[pos][dir][ang])])
