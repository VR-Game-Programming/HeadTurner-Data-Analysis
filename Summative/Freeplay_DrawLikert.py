import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from math import pi
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
            DataDict[condition][app] = [0] * len(Points)
    for app in Applications:
        for i, row in df.iterrows():
            DataDict[row[f"{app}-{metrics}-1"]][app][
                int(row[f"{app}-{metrics}-2"]) - 1
            ] += 1

    return DataDict


def GetOverallPreference():
    OverallPreferenceData = {
        "NormalBed": [0],
        "ActuatedBed": [0],
    }
    for i, row in df.iterrows():
        OverallPreferenceData[row["OverallPreference"]][0] += 1

    return OverallPreferenceData


def DrawHorizontalStackBarChart(FigureTitle, Data):
    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, sharey=True)
    fig.tight_layout()

    for i, condition in enumerate(Conditions):
        data = np.array(list(Data[condition].values()))
        data_cum = data.cumsum(axis=1)

        axes[i].set_title(condition, color=Colors[i][3])
        axes[i].set_xlim(0, 10)
        axes[i].set_xticks([0, 2, 4, 6, 8, 10])

        for j in range(0, len(Points)):
            widths = data[:, j]
            starts = data_cum[:, j] - widths
            rects = axes[i].barh(
                Applications,
                widths,
                left=starts,
                align="center",
                height=0.4,
                color=Colors[i][j],
            )
            # axes[i].bar_label(rects, label_type="center")

    axes[0].invert_xaxis()
    axes[0].set_yticks(range(len(Applications)))
    axes[0].set_yticklabels(Applications)
    axes[0].yaxis.tick_left()
    axes[0].tick_params(axis="y")

    plt.ylim(-1, 2)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.suptitle(FigureTitle, fontsize=16, fontweight="bold")

    figurepath = f"{RootDir}/Result Figure/Summative Freeplay {FigureTitle} [BarH].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {figurepath}\n")


def DrawPreferenceDataChart(Data, FigureTitle="Overall Preference"):
    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, sharey=True)
    fig.tight_layout()

    for i, condition in enumerate(Conditions):

        axes[i].set_title(condition, color=Colors[i][3])
        axes[i].set_xlim(0, 10)
        axes[i].set_xticks([0, 2, 4, 6, 8, 10])

        rects = axes[i].barh(
            "Overall Preference",
            Data[condition],
            align="center",
            color=Colors[i][1],
        )

    axes[0].invert_xaxis()
    axes[0].yaxis.tick_left()
    axes[0].tick_params(axis="y")

    plt.ylim(-2, 2)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.suptitle(FigureTitle, fontsize=16, fontweight="bold")

    figurepath = f"{RootDir}/Result Figure/Summative Freeplay {FigureTitle} [BarH].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {figurepath}\n")


ComfortData = GetDataFromSheet("Comfort")
DrawHorizontalStackBarChart("Comfort", ComfortData)

PreferenceData = GetDataFromSheet("Preference")
DrawHorizontalStackBarChart("Preference", PreferenceData)

OverallPreferenceData = GetOverallPreference()
DrawPreferenceDataChart(OverallPreferenceData)
