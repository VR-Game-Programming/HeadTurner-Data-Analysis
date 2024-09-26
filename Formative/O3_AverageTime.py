import pandas as pd
import statistics as stat
import csv
from Constant import *


task_time_dict = dict()
for pos in Postures:
    task_time_dict[pos] = dict()
    for dir in Directions:
        task_time_dict[pos][dir] = list()


def CalculateTaskTime(data_list):
    start_time = float(data_list[0])
    end_time = float(data_list[-1])
    return end_time - start_time


for i in Participants:
    for pos in Postures:
        filepath = f"{RootDir}/Result Raw (ReCalculate)/O3_Final/Formative_O3_P{i}_{pos}_Final.csv"
        df = pd.read_csv(filepath)

        for dir in Directions:
            for task in range(1, 4):
                task_df = df.loc[df["Direction"] == dir].loc[df["tCount"] == task]
                task_time = CalculateTaskTime(task_df["Time"].tolist())
                task_time_dict[pos][dir].append(task_time)


def Remove_Outlier(data_list):
    mean = stat.fmean(data_list)
    for data in data_list:
        if abs(data - mean) > 2:
            data_list.remove(data)
    return data_list


def Get_Degree(dir):
    if dir == "Up" or dir == "Down":
        return 30
    elif dir == "Left" or dir == "Right":
        return 50
    else:
        return 40


with open(f"{RootDir}/Result Processed/O3_AverageTime.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Posture", "Direction", "TaskTime", "Degree/Second"])

    for pos in Postures:
        for dir in Directions:
            task_time_dict[pos][dir] = Remove_Outlier(task_time_dict[pos][dir])
            task_time = stat.fmean(task_time_dict[pos][dir])
            degree_sec = Get_Degree(dir) / task_time
            writer.writerow([pos, dir, task_time, degree_sec])
