import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from scipy.stats import wilcoxon
from math import pi
from Constant import *

# Get Dataframe From Google Sheet
# Please replace the service_account_file with your own credentials
# (on local, do not upload to github)
gc = pygsheets.authorize(
    service_account_file="Credentials/headturner-423306-b0e4058416e1.json"
)
sheet_url = "https://docs.google.com/spreadsheets/d/1boxkhwEWOwFU7Pwfa7lKDw4uZosvswwdWjrWo2g6nN0/"
sh = gc.open_by_url(sheet_url)
wks = sh.sheet1
df = wks.get_as_df()

# Remove Pilot Test Data
df = df.drop(index=0)

# Standardize Scores for Participants
# for i in Participants:
#   scores = list()
#   for p in Postures:
#     for d in Directions:
#       col_name = p + " - " + d
#       scores.append(df[col_name][i])

#   mean = fmean(scores)
#   std_dev = stat.stdev(scores)
#   print(f"Particiapant {i}, mean={mean}, std_dev={std_dev}")
#   n = len(scores)
#   for p in Postures:
#     for d in Directions:
#       col_name = p + " - " + d
#       new_score = (df[col_name][i] - mean) / (std_dev / np.sqrt(n))
#       df.at[i, col_name] = new_score

# Initialize Data
data = dict()
avg_data = dict()
std_data = dict()
for p in Postures:
    data[p] = dict()
    avg_data[p] = list()
    std_data[p] = list()
    for d in Directions_num:
        col_name = "Task2 - " + p + " - " + d
        scores = df[col_name].to_list()
        data[p][d] = scores
        avg_data[p].append(stat.fmean(scores))
        std_data[p].append(stat.stdev(scores))

# with open("Result Processed/" + "T2_Result.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Posture", "Direction", "Mean", "Std"])
#     for p in Postures:
#         for idx, d in enumerate(Directions):
#             writer.writerow([p, d, data[p][idx], std_data[p][idx]])

# Data Analysis
with open(f"{RootDir}/Result Processed/T2_pValue_Result.txt", "w") as text_file:
    for d in Directions_num:
        print(f"For Direction {d}", file=text_file)
        print(
            "=================================================================",
            file=text_file,
        )
        print("Standing:", file=text_file)
        print(data["Standing"][d], file=text_file)
        print("Lying:", file=text_file)
        print(data["Lying"][d], file=text_file)
        print(
            wilcoxon(data["Standing"][d], data["Lying"][d]), file=text_file
        )
        print("\n", file=text_file)


# Draw Figure
def DrawEffortBarChart():
    x = np.arange(len(Directions))
    width = 0.35
    fig, ax = plt.subplots(figsize=(15, 10))

    # Draw
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.bar(
        x - width / 2,
        avg_data["Standing"],
        width,
        color=Colors[0][4],
        label="Standing",
        yerr=std_data["Standing"],
        capsize=3,
    )
    ax.bar(
        x + width / 2,
        avg_data["Lying"],
        width,
        color=Colors[1][4],
        label="Lying",
        yerr=std_data["Lying"],
        capsize=3,
    )

    # plt.ylim(1, 7)

    # Add Text
    ax.set_xlabel("Directions")
    ax.set_ylabel("Effort Scores")
    ax.set_title("Effort scores with different postures and directions")
    ax.set_xticks(x)
    ax.set_xticklabels(Directions)
    ax.legend()

    figurepath = f"{RootDir}/Result Figure/Formative T2 EffortScores.png"

    plt.savefig(
        figurepath, transparent=False
    )
    plt.close()
    print(f"Figure saved to {ColorText(figurepath, "green")}\n")

def DrawEffortRadarChart(
    std=True,
    annotate=False,
):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)

    N = len(Directions)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Draw direction axes
    ax.xaxis.set_label_position("bottom")
    plt.xticks(angles[:-1], Directions, color="black", size=10)
    ax.tick_params(axis="x", which="major", pad=20)

    # Draw range labels
    ax.yaxis.set_label_position("left")
    ax.set_rlabel_position(20)
    labels = np.arange(0, 7, 1)
    plt.yticks(labels, color="grey", size=0)
    plt.ylim(0, 7)

    # Plot the data
    for i, group in enumerate(Postures):
        values = avg_data[group]
        values += values[:1]
        if std:
            std_values = list(std_data[group])
            std_values += std_values[:1]
            ax.errorbar(
                angles,
                values,
                color=Colors[i][3],
                linewidth=2,
                linestyle="solid",
                label=group,
                yerr=std_values,
                ecolor=Colors[i][3],
                capsize=5,
            )
        else:
            ax.plot(
                angles,
                values,
                color=Colors[i][3],
                linewidth=2,
                linestyle="solid",
                label=group,
            )

        ax.fill(angles, values, color=Colors[i][3], alpha=0.1)
        if annotate:
            for a, v in zip(angles, values):
                ax.annotate(
                    "%.2f" % v, (a, v), textcoords="offset points", xytext=(0, 10)
                )

    plt.legend(loc="best", bbox_to_anchor=(1, 0))
    plt.title("Effort Scores", pad=20, color="black", size=16)

    figurepath = f"{RootDir}/Result Figure/Formative T2 EffortScores"
    figurepath += " [Radar]"
    if std:
        figurepath += " [STD]"
    if annotate:
        figurepath += " [Annotate]"
    figurepath += ".png"

    plt.savefig(figurepath, transparent=False)
    plt.close()
    print(f"Figure saved to {ColorText(figurepath, "green")}\n")

# DrawEffortBarChart()
# DrawEffortRadarChart()
