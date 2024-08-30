import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import statistics as stat
from math import pi
from scipy.stats import ttest_rel, wilcoxon
import statsmodels.api as sm
import statsmodels.formula.api as smf
from Constant import *
from DrawFigFunction import *

# Data Prepare
# =================================================================
# Initialize the result dict
range_data = dict()
for dir in Directions:
    range_data[dir] = dict()
    for pos in Postures:
        range_data[dir][pos] = [None] * len(Participants)

# Read raw result
filepath = f"{RootDir}/Result Processed/T1_RawData_Mean.csv"
with open(filepath, newline="") as csvfile:
    r = csv.DictReader(csvfile)
    for row in r:
        i = int(row["Participant"])
        pos = row["Posture"]
        dir = row["Direction"]
        angle = float(row["Range"])

        range_data[dir][pos][i - 1] = angle

# Calculate mean & std
std_data = dict()
for dir in Directions:
    std_data[dir] = dict()
    for pos in Postures:
        std_data[dir][pos] = stat.stdev(range_data[dir][pos])
        range_data[dir][pos] = stat.fmean(range_data[dir][pos])

# with open(f"{RootDir}/Result Processed/T1_Result.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Posture", "Direction", "Mean", "Std"])
#     for dir in Directions:
#         for pos in Postures:
#             writer.writerow([pos, dir, range_data[dir][pos], std_data[dir][pos]])

DrawRangeRadarChart(
    FigureTitle="Head Maximum Viewing Range (Yaw)",
    FigurePath=f"{RootDir}/Result Figure/Formative T1 HeadMaximumRange Yaw.png",
    LeftData=range_data["Left"],
    RightData=range_data["Right"],
    Type="LR",
)

DrawRangeRadarChart(
    FigureTitle="Head Maximum Viewing Range (Pitch)",
    FigurePath=f"{RootDir}/Result Figure/Formative T1 HeadMaximumRange Pitch.png",
    LeftData=range_data["Up"],
    RightData=range_data["Down"],
    Type="UD",
)

rev_range_data = dict()
rev_std_data = dict()
for pos in Postures:
    rev_range_data[pos] = dict()
    rev_std_data[pos] = dict()
    for dir in Directions:
        rev_range_data[pos][dir] = range_data[dir][pos]
        rev_std_data[pos][dir] = std_data[dir][pos]

DrawRadarChart(
    FigureTitle="HeadMaximumRange AllDirections",
    Data=rev_range_data,
    StdData=rev_std_data,
)
