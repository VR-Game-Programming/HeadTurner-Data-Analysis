import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
from Constant import *

# Get dataframe from Google Sheet
# Please replace the service_account_file with your own credentials
# (on local, do not upload to github)
gc = pygsheets.authorize(
    service_account_file="Credentials/headturner-423306-b0e4058416e1.json"
)
sheet_url = "https://docs.google.com/spreadsheets/d/1MrSQfQzZdbkJJIY9JIjD0IgCQh8yLSUKTUrm8LsnZfY"
sh = gc.open_by_url(sheet_url)
wks = sh.sheet1
df = wks.get_as_df()

# Remove pilot data
df = df.loc[df["受試者編號"] > 0]


def GetDataFromSheet(metrics):
    DataDict = dict()
    for condition in Conditions:
        DataDict[condition] = dict()
        for app in Applications:
            DataDict[condition][app] = df[f"{app}-{metrics}-{condition}"].tolist()

    filepath = f"{RootDir}/Processed Data/Summative_Freeplay_{metrics}_pval.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["App", "paired-t", "wilcoxon"])
        for app in Applications:
            _, p = ttest_rel(DataDict["ActuatedBed"][app], DataDict["NormalBed"][app])
            _, wp = wilcoxon(DataDict["ActuatedBed"][app], DataDict["NormalBed"][app])
            writer.writerow([app, p, wp])

    StdDict = dict()
    for condition in Conditions:
        StdDict[condition] = dict()
        for app in Applications:
            StdDict[condition][app] = stat.stdev(DataDict[condition][app])
            DataDict[condition][app] = stat.fmean(DataDict[condition][app])

    filepath = f"{RootDir}/Processed Data/Summative_Freeplay_{metrics}.csv"
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
            color=Colors[i][2],
            label=group,
            yerr=std_data,
            capsize=3,
        )

    plt.ylim(0, yLimit)
    ax.set_xlabel("Application")
    ax.set_xticks(x)
    ax.set_xticklabels(Applications)

    plt.legend(loc="best")
    plt.title(FigureTitle, pad=20, color="black", size=16)

    figurepath = f"{RootDir}/Result Figure/Summative {FigureTitle} [Bar].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {ColorText(figurepath, "green")}\n")


EffortData, EffortError = GetDataFromSheet("Effort")
DrawBarChart(
    FigureTitle="Freeplay Effort",
    Data=EffortData,
    ErrorData=EffortError,
    yLimit=10,
)

DizzinessData, DizzinessError = GetDataFromSheet("Dizziness")
DrawBarChart(
    FigureTitle="Freeplay Dizziness",
    Data=DizzinessData,
    ErrorData=DizzinessError,
    yLimit=10,
)
