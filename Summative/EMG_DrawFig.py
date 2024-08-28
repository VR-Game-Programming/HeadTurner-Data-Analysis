import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
from math import pi
from Constant import Colors, Conditions, Directions, RootDir, ColorText

df = pd.read_csv("Processed Data/Processed MCL Value.csv")


def ReturnProcessData(task):
    DataDict = dict()
    for condition in Conditions:
        DataDict[condition] = dict()
        for direction in Directions:
            DataDict[condition][direction] = df[
                f"{task}_{direction}_{condition}"
            ].tolist()

    filepath = f"{RootDir}/Processed Data/Summative_{task}_EMG_pval.csv"
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
            StdDict[condition][direction] = stat.stdev(
                DataDict[condition][direction])
            DataDict[condition][direction] = stat.fmean(
                DataDict[condition][direction])

    filepath = f"{RootDir}/Processed Data/Summative_{task}_EMG.csv"
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
    std=False,
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
    labels = np.arange(0, yLimit, yLimit / 5)
    plt.yticks(labels, color="grey", size=0)
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


T1_EMG_Dict, T1_EMG_StdDict = ReturnProcessData("T1")

DrawRadarChart(
    FigureTitle="T1 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
)
DrawRadarChart(
    FigureTitle="T1 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
    std=True,
)
DrawRadarChart(
    FigureTitle="T1 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
    std=True,
    annotate=True,
)

T1_EMG_Dict, T1_EMG_StdDict = ReturnProcessData("T2")

DrawRadarChart(
    FigureTitle="T2 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
)
DrawRadarChart(
    FigureTitle="T2 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
    std=True,
)
DrawRadarChart(
    FigureTitle="T2 EMG",
    Data=T1_EMG_Dict,
    StdData=T1_EMG_StdDict,
    yLimit=50,
    std=True,
    annotate=True,
)
