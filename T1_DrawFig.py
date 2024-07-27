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
        range_data[p][d] = list()

# Read raw result
df = pd.DataFrame(columns=["participant", "posture", "direction", "range"])
for pos in Postures:
    for i in Participants:
        filepath = (
            "Result Raw (ReCalculate)/T1/" + f"Formative_T1_P{i}_{pos}_ReCalculate.csv"
        )
        with open(filepath, newline="") as csvfile:
            r = csv.DictReader(csvfile)
            for row in r:
                d = row["Direction"]
                angle = CalculateAngle(d, float(row["MaxViewingRange"]))

                df = df._append(
                    {
                        "participant": i,
                        "posture": pos,
                        "direction": d,
                        "range": angle,
                    },
                    ignore_index=True,
                )
                range_data[pos][row["Direction"]].append(angle)


df.to_csv(ProcessedDir + "T1_RawData.csv", index=False)

# Data Analysis
# =================================================================
# Paired t-Test & Wilcoxon
with open(ProcessedDir + "T1_pValue_Result.txt", "w") as text_file:
    for d in Directions:
        print(f"For Direction {d}", file=text_file)
        print(
            "=================================================================",
            file=text_file,
        )
        print("Standing:", file=text_file)
        print(range_data["Standing"][d], file=text_file)
        print("Lying:", file=text_file)
        print(range_data["Lying"][d], file=text_file)
        print(
            ttest_rel(range_data["Standing"][d], range_data["Lying"][d]), file=text_file
        )
        print(
            wilcoxon(range_data["Standing"][d], range_data["Lying"][d]), file=text_file
        )
        print("\n", file=text_file)

# Model
base_posture = "Standing"
base_direction = "Up"

df["posture"] = df["posture"].astype("category")
df["direction"] = df["direction"].astype("category")
df["range"] = df["range"].apply(pd.to_numeric, errors="coerce")

df["posture"] = df["posture"].cat.reorder_categories(
    [base_posture]
    + [cat for cat in df["posture"].cat.categories if cat != base_posture],
    ordered=True,
)
df["direction"] = df["direction"].cat.reorder_categories(
    [base_direction]
    + [cat for cat in df["direction"].cat.categories if cat != base_direction],
    ordered=True,
)

model = smf.mixedlm("range ~ posture + direction", df, groups=df["participant"])
# model = smf.glm("range ~ posture + direction", data=df)
result = model.fit()

with open(ProcessedDir + "T1_Model_Summary.txt", "w") as text_file:
    print(f"Base: {base_posture}, {base_direction}\n", file=text_file)
    print(result.summary(), file=text_file)

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

# Draw Figure
# =================================================================
N = len(Directions)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
theta = dict()
offset = {"Standing": pi / 32, "Lying": pi * 7 / 32}
for p in Postures:
    theta[p] = np.linspace(offset[p], (2 * pi) + offset[p], N, endpoint=False)

plt.figure(figsize=(10, 10))
ax = plt.subplot(projection="polar")
width = pi / 16

for p in Postures:
    values = list(range_data[p].values())
    std_values = list(std_data[p].values())
    ax.bar(theta[p], values, width=width, bottom=0, alpha=0.5, label=p)
    ax.errorbar(
        theta[p], values, linewidth=0, yerr=std_values, elinewidth=1, ecolor="k"
    )

plt.xticks(angles[:-1], Directions, color="black", size=10)
ax.tick_params(axis="x", which="major", pad=20)
plt.yticks([0, 30, 60, 90, 120, 150, 180], color="grey", size=10)
plt.ylim(-30, 180)

plt.legend(loc="best", bbox_to_anchor=(0, 0))
plt.savefig("Result Figure/" + "T1_MaxViewingRange.png", transparent=False)
plt.close()


# Draw Figure (v2)
# =================================================================
# Set plot
plt.figure(figsize=(10, 10))
ax = plt.subplot(111, polar=True)

N = len(Directions)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Draw direction axes
ax.set_xlabel("Direction", labelpad=15, color="black", size=16)
ax.xaxis.set_label_position("bottom")
plt.xticks(angles[:-1], Directions, color="black", size=10)
ax.tick_params(axis="x", which="major", pad=20)

# Draw range labels
ax.set_ylabel("Max Viewing Range", labelpad=40, color="grey", size=16)
ax.yaxis.set_label_position("left")
ax.set_rlabel_position(20)
# ax.get_yaxis().set_visible(False)
plt.yticks([30, 60, 90, 120, 150, 180], color="grey", size=10)
plt.ylim(0, 180)

# Plot the data
i = 0
colors = ["tab:blue", "tab:red"]
ecolors = ["black", "grey"]
ecapsize = [6, 4]
for pos in Postures:
    values = list(range_data[pos].values())
    values += values[:1]
    std_values = list(std_data[pos].values())
    std_values += std_values[:1]
    ax.errorbar(
        angles,
        values,
        color=colors[i],
        linewidth=2,
        linestyle="solid",
        label=pos,
        yerr=std_values,
        ecolor=ecolors[i],
        capsize=ecapsize[i],
    )
    ax.fill(angles, values, "k", alpha=0.05)
    i += 1

plt.legend(loc="best", bbox_to_anchor=(0, 0))
plt.savefig("Result Figure/" + "T1_MaxViewingRange_v2.png", transparent=False)
plt.close()
