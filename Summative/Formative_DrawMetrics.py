import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
from math import pi
from Constant import *

# Get dataframe from Google Sheet
# Please replace the service_account_file with your own credentials
# (on local, do not upload to github)
gc = pygsheets.authorize(
    service_account_file="Credentials/headturner-423306-b0e4058416e1.json"
)
sheet_url = "https://docs.google.com/spreadsheets/d/1wGxgmiH18YDa57GcYY0Fjfzts9VWdkpPf_z4jeDuSYE"
sh = gc.open_by_url(sheet_url)
wks = sh.sheet1
df = wks.get_as_df()

# Remove pilot data
df = df.loc[df["受試者編號"] > 0]


def ReturnProcessData(task, metrics):
    DataDict = dict()
    for condition in Conditions:
        DataDict[condition] = dict()
        for direction in Directions:
            DataDict[condition][direction] = df[
                f"{task}-{metrics}-{condition}-{direction}"
            ].tolist()

    filepath = f"{RootDir}/Processed Data/Summative_{task}_{metrics}_pval.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Direction", "paired-t", "wilcoxon"])
        for direction in Directions:
            _, p = ttest_rel(
                DataDict["ActuatedBed"][direction],
                DataDict["NormalBed"][direction],
            )
            _, wp = wilcoxon(
                DataDict["ActuatedBed"][direction],
                DataDict["NormalBed"][direction],
            )
            writer.writerow([direction, p, wp])

    StdDict = dict()
    for condition in Conditions:
        StdDict[condition] = dict()
        for direction in Directions:
            StdDict[condition][direction] = stat.stdev(DataDict[condition][direction])
            DataDict[condition][direction] = stat.fmean(DataDict[condition][direction])

    filepath = f"{RootDir}/Processed Data/Summative_{task}_{metrics}.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Direction", "Condition", "Mean", "Std"])
        for direction in Directions:
            for condition in Conditions:
                writer.writerow(
                    [
                        direction,
                        condition,
                        DataDict[condition][direction],
                        StdDict[condition][direction],
                    ]
                )

    return DataDict, StdDict

def DrawRadarChart(
    FigureTitle,
    Data,
    StdData,
    yLimit,
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
    labels = np.arange(0, yLimit, yLimit / 4)
    plt.yticks(labels, color="grey", size=10)
    plt.ylim(0, yLimit)

    # Plot the data
    for i, group in enumerate(Conditions):
        values = list(Data[group].values())
        values += values[:1]
        if std:
            std_values = list(StdData[group].values())
            std_values += std_values[:1]
            ax.errorbar(
                angles,
                values,
                color=Colors[i][2],
                linewidth=2,
                linestyle="solid",
                label=group,
                yerr=std_values,
                ecolor=Colors[i][2],
                capsize=5,
            )
        else:
            ax.plot(
                angles,
                values,
                color=Colors[i][2],
                linewidth=2,
                linestyle="solid",
                label=group,
            )

        ax.fill(angles, values, color=Colors[i][2], alpha=0.1)
        if annotate:
            for a, v in zip(angles, values):
                ax.annotate(
                    "%.2f" % v, (a, v), textcoords="offset points", xytext=(0, 10)
                )

    plt.legend(loc="best", bbox_to_anchor=(1, 0))
    plt.title(FigureTitle, pad=20, color="black", size=16)

    figurepath = f"{RootDir}/Result Figure/Summative {FigureTitle}"
    figurepath += " [Radar]"
    if std:
        figurepath += " [STD]"
    if annotate:
        figurepath += " [Annotate]"
    figurepath += ".png"

    plt.savefig(figurepath, transparent=False)
    plt.close()
    print(f"Figure saved to {ColorText(figurepath, "green")}\n")


T1EffortDict, T1EffortStdDict = ReturnProcessData("T1", "Effort")
DrawRadarChart(
    FigureTitle="T1 Effort",
    Data=T1EffortDict,
    StdData=T1EffortStdDict,
    yLimit=8,
)

T2EffortDict, T2EffortStdDict = ReturnProcessData("T2", "Effort")
DrawRadarChart(
    FigureTitle="T2 Effort",
    Data=T2EffortDict,
    StdData=T2EffortStdDict,
    yLimit=8,
)

T2DizzniessDict, T2DizzniessStdDict = ReturnProcessData("T2", "Dizziness")
DrawRadarChart(
    FigureTitle="T2 Dizzniess",
    Data=T2DizzniessDict,
    StdData=T2DizzniessStdDict,
    yLimit=4,
)
