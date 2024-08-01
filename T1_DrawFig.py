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

ProcessedDir = "Result Processed/"


def CalculateAngle(direction, angle):
    if direction == "Right" or direction == "UpRight" or direction == "DownRight":
        return abs(angle) if angle > 0 else 360 + angle

    elif direction == "Left" or direction == "UpLeft" or direction == "DownLeft":
        return abs(angle) if angle < 0 else 360 - angle

    else:
        return abs(angle) if abs(angle) < 180 else 360 - abs(angle)


# Data Prepare
# =================================================================
# Initialize the result dict
range_data = dict()
for p in Postures:
    range_data[p] = dict()
    for d in Directions:
        range_data[p][d] = [None] * len(Participants)

# Read raw result
filepath = "Result Processed/T1_RawData_Mean.csv"
with open(filepath, newline="") as csvfile:
    r = csv.DictReader(csvfile)
    for row in r:
        i = int(row["Participant"])
        pos = row["Posture"]
        dir = row["Direction"]
        angle = float(row["Range"])

        range_data[pos][dir][i - 1] = angle

# Calculate mean & std
std_data = dict()
for pos in Postures:
    std_data[pos] = dict()
    for d in Directions:
        std_data[pos][d] = stat.stdev(range_data[pos][d])
        range_data[pos][d] = stat.fmean(range_data[pos][d])

with open(ProcessedDir + "T1_Result.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Posture", "Direction", "Mean", "Std"])
    for p in Postures:
        for d in Directions:
            writer.writerow([p, d, range_data[p][d], std_data[p][d]])


# Draw Figure (v3)
# =================================================================
# Left-Right
plt.figure(figsize=(10, 10))
ax = plt.subplot(projection="polar")

N = int(360 / 30)
angles = [n / float(N) * 2 * pi for n in range(N)]
begin = pi / 2
bottom = 4

for p in Postures:
    value = range_data[p]["Left"] / 180 * pi
    offset = begin + value / 2
    ax.bar(
        offset,
        10,
        width=value,
        bottom=bottom,
        color=Colors[p][1],
        alpha=1,
        label=p,
    )
    value = range_data[p]["Right"] / 180 * pi
    offset = begin - value / 2
    ax.bar(
        offset,
        10,
        width=value,
        bottom=bottom,
        color=Colors[p][1],
        alpha=1,
    )

# Draw x axis
angles_label = [
    "Right 90",
    "Right 60",
    "Right 30",
    "Front",
    "Left 30",
    "Left 60",
    "Left 90",
    "Left 120",
    "Left 150",
    "Back",
    "Right 150",
    "Right 120",
]
plt.xticks(angles, angles_label, color="black", size=10)
ax.tick_params(axis="x", which="major", pad=20)

# Draw y axis
plt.yticks([0, 10], color="grey", size=0)
plt.ylim(0, 10)

plt.legend(loc="best", bbox_to_anchor=(0, 0))
plt.title(
    "Yaw Maximum Viewing Range at different posture", pad=20, color="black", size=16
)
plt.savefig("Result Figure/" + "T1_MaxViewingRange_LR_v3.png", transparent=False)
plt.close()

# Up Down
plt.figure(figsize=(10, 10))
ax = plt.subplot(projection="polar")

N = int(360 / 30)
angles = [n / float(N) * 2 * pi for n in range(N)]
begin = 0
bottom = 4

for p in Postures:
    value = range_data[p]["Up"] / 180 * pi
    offset = begin + value / 2
    ax.bar(
        offset,
        10,
        width=value,
        bottom=bottom,
        color=Colors[p][1],
        alpha=1,
        label=p,
    )
    value = range_data[p]["Down"] / 180 * pi
    offset = begin - value / 2
    ax.bar(
        offset,
        10,
        width=value,
        bottom=bottom,
        color=Colors[p][1],
        alpha=1,
    )

# Draw x axis
angles_label = [
    "Front",
    "Up 30",
    "Up 60",
    "Up 90",
    "Up 120",
    "Up 150",
    "Back",
    "Down 150",
    "Down 120",
    "Down 90",
    "Down 60",
    "Down 30",
]
plt.xticks(angles, angles_label, color="black", size=10)
ax.tick_params(axis="x", which="major", pad=20)

# Draw y axis
plt.yticks([0, 10], color="grey", size=0)
plt.ylim(0, 10)

plt.legend(loc="best", bbox_to_anchor=(0, 0))
plt.title(
    "Pitch Maximum Viewing Range at different posture", pad=20, color="black", size=16
)
plt.savefig("Result Figure/" + "T1_MaxViewingRange_UD_v3.png", transparent=False)
plt.close()


# Draw Figure (v2)
# =================================================================
# Set plot
# plt.figure(figsize=(10, 10))
# ax = plt.subplot(111, polar=True)

# N = len(Directions)
# angles = [n / float(N) * 2 * pi for n in range(N)]
# angles += angles[:1]

# # Draw direction axes
# ax.set_xlabel("Direction", labelpad=15, color="black", size=16)
# ax.xaxis.set_label_position("bottom")
# plt.xticks(angles[:-1], Directions, color="black", size=10)
# ax.tick_params(axis="x", which="major", pad=20)

# # Draw range labels
# ax.set_ylabel("Max Viewing Range", labelpad=40, color="grey", size=16)
# ax.yaxis.set_label_position("left")
# ax.set_rlabel_position(20)
# # ax.get_yaxis().set_visible(False)
# plt.yticks([30, 60, 90, 120, 150, 180], color="grey", size=10)
# plt.ylim(0, 180)

# # Plot the data
# i = 0
# colors = ["tab:blue", "tab:red"]
# ecolors = ["black", "grey"]
# ecapsize = [6, 4]
# for pos in Postures:
#     values = list(range_data[pos].values())
#     values += values[:1]
#     std_values = list(std_data[pos].values())
#     std_values += std_values[:1]
#     ax.errorbar(
#         angles,
#         values,
#         color=colors[i],
#         linewidth=2,
#         linestyle="solid",
#         label=pos,
#         yerr=std_values,
#         ecolor=ecolors[i],
#         capsize=ecapsize[i],
#     )
#     ax.fill(angles, values, "k", alpha=0.05)
#     i += 1

# plt.legend(loc="best", bbox_to_anchor=(0, 0))
# plt.savefig("Result Figure/" + "T1_MaxViewingRange_v2.png", transparent=False)
# plt.close()

# Draw Figure
# =================================================================
# N = len(Directions)
# angles = [n / float(N) * 2 * pi for n in range(N)]
# angles += angles[:1]
# theta = dict()
# offset = {"Standing": pi / 32, "Lying": pi * 7 / 32}
# for p in Postures:
#     theta[p] = np.linspace(offset[p], (2 * pi) + offset[p], N, endpoint=False)

# plt.figure(figsize=(10, 10))
# ax = plt.subplot(projection="polar")
# width = pi / 16

# for p in Postures:
#     values = list(range_data[p].values())
#     std_values = list(std_data[p].values())
#     ax.bar(theta[p], values, width=width, bottom=0, alpha=0.5, label=p)
#     ax.errorbar(
#         theta[p], values, linewidth=0, yerr=std_values, elinewidth=1, ecolor="k"
#     )

# plt.xticks(angles[:-1], Directions, color="black", size=10)
# ax.tick_params(axis="x", which="major", pad=20)
# plt.yticks([0, 30, 60, 90, 120, 150, 180], color="grey", size=10)
# plt.ylim(-30, 180)

# plt.legend(loc="best", bbox_to_anchor=(0, 0))
# plt.savefig("Result Figure/" + "T1_MaxViewingRange.png", transparent=False)
# plt.close()
