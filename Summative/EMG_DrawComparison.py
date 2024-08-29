import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
from Constant import Conditions, Applications, Colors, RootDir, ColorText


df = pd.read_csv("Processed Data/Processed MCL Value.csv")


def GetDataFromSheet():
    DataDict = dict()
    for condition in Conditions:
        DataDict[condition] = dict()
        for app in Applications:
            DataDict[condition][app] = \
                df[f"{app}_{condition}"].tolist()

    filepath = \
        f"{RootDir}/Processed Data/Summative_Freeplay_EMG_pval.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["App", "paired-t", "wilcoxon"])
        for app in Applications:
            _, p = ttest_rel(DataDict["ActuatedBed"]
                             [app], DataDict["NormalBed"][app])
            _, wp = wilcoxon(DataDict["ActuatedBed"]
                             [app], DataDict["NormalBed"][app])
            writer.writerow([app, p, wp])

    StdDict = dict()
    for condition in Conditions:
        StdDict[condition] = dict()
        for app in Applications:
            StdDict[condition][app] = stat.stdev(DataDict[condition][app])
            DataDict[condition][app] = stat.fmean(DataDict[condition][app])

    filepath = f"{RootDir}/Processed Data/Summative_Freeplay_EMG.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["App", "Condition", "Mean", "Std"])
        for condition in Conditions:
            for app in Applications:
                writer.writerow(
                    [
                        app,
                        condition,
                        DataDict[condition][app],
                        StdDict[condition][app],
                    ]
                )

    return DataDict, StdDict


def DrawBarChart(FigureTitle, Data, ErrorData, yLimit):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot()

    x = np.arange(len(Applications))
    width = 0.3
    offset = [-width / 2, width / 2]

    for i, group in enumerate(Conditions):
        data = list(Data[group].values())
        std_data = list(ErrorData[group].values())
        ax.bar(
            x + offset[i],
            data,
            width,
            color=Colors[i][4],
            label=group,
            yerr=std_data,
            capsize=3,
        )

    # plt.ylim(0, yLimit)
    ax.set_xlabel("Application")
    ax.set_xticks(x)
    ax.set_xticklabels(Applications)

    plt.legend(loc="best")
    plt.title(FigureTitle, pad=20, color="black", size=16)

    figurepath = f"{RootDir}/Result Figure/Summative {FigureTitle} [Bar].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {ColorText(figurepath, "green")}\n")


EffortData, EffortError = GetDataFromSheet()
DrawBarChart(
    FigureTitle="Freeplay EMG",
    Data=EffortData,
    ErrorData=EffortError,
    yLimit=10,
)
