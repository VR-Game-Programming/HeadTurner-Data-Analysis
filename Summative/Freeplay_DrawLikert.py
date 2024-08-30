import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_rel
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

# Get Comfort Data
ComfortData = dict()
for condition in Conditions:
    ComfortData[condition] = dict()
    for app in Applications:
        ComfortData[condition][app] = [0] * len(Points)
for app in Applications:
    for i, row in df.iterrows():
        ComfortData[row[f"{app}-{"Comfort"}-1"]][app][
            int(row[f"{app}-{"Comfort"}-2"]) - 1
        ] += 1

print(ComfortData)

# Draw Comfort Figure
def DrawComfortFig():
    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, sharey=True)
    fig.tight_layout()

    for i, condition in enumerate(reversed(Conditions)):
        data = np.array(list(ComfortData[condition].values()))
        data_cum = data.cumsum(axis=1)

        axes[i].set_title(condition, color=Colors[(i+1)%2][4])
        axes[i].set_xlim(0, 14)
        axes[i].set_xticks([0, 2, 4, 6, 8, 10, 12, 14])

        for j in range(0, len(Points)):
            widths = data[:, j]
            starts = data_cum[:, j] - widths
            rects = axes[i].barh(
                Applications,
                widths,
                left=starts,
                align="center",
                height=0.4,
                color=Colors[(i+1)%2][j],
            )
            for rect in rects:
                x, y = rect.get_xy()
                w, h = rect.get_width(), rect.get_height()
                if (w == 0 or x == 0):
                    continue
                axes[i].plot([x, x], [y + 0.01, y + h - 0.01], color='black', lw=1)

    axes[0].invert_xaxis()
    axes[0].set_yticks(range(len(Applications)))
    axes[0].set_yticklabels(Applications)
    axes[0].yaxis.tick_left()
    axes[0].tick_params(axis="y")

    plt.ylim(-1, 3)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.suptitle("Comfort", fontsize=16, fontweight="bold")

    figurepath = f"{RootDir}/Result Figure/Summative Freeplay Comfort [BarH].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {ColorText(figurepath, "green")}\n")

# Get Preference Data
PreferenceData = dict()
for condition in Conditions:
    PreferenceData[condition] = dict()
    PreferenceData[condition]["Overall"] = [0] * len(Points)
    for app in Applications:
        PreferenceData[condition][app] = [0] * len(Points)

for app in Applications:
    for i, row in df.iterrows():
        PreferenceData[row[f"{app}-{"Preference"}-1"]][app][
            int(row[f"{app}-{"Preference"}-2"]) - 1
        ] += 1
for i, row in df.iterrows():
    PreferenceData[row["OverallPreference"]]["Overall"][4] += 1

print(PreferenceData)

# Draw Preference Figure
def DrawPreferenceFig():
    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, sharey=True)
    fig.tight_layout()

    for i, condition in enumerate(reversed(Conditions)):
        data = np.array(list(PreferenceData[condition].values()))
        data_cum = data.cumsum(axis=1)

        axes[i].set_title(condition, color=Colors[(i+1)%2][4])
        axes[i].set_xlim(0, 14)
        axes[i].set_xticks([0, 2, 4, 6, 8, 10, 12, 14])

        for j in range(0, len(Points)):
            widths = data[:, j]
            starts = data_cum[:, j] - widths
            rects = axes[i].barh(
                ["Overall"] + Applications,
                widths,
                left=starts,
                align="center",
                height=0.4,
                color=Colors[(i+1)%2][j],
            )
            for rect in rects:
                x, y = rect.get_xy()
                w, h = rect.get_width(), rect.get_height()
                if (w == 0 or x == 0):
                    continue
                axes[i].plot([x, x], [y + 0.01, y + h - 0.01], color='black', lw=1)

    axes[0].invert_xaxis()
    axes[0].set_yticks(range(len(Applications) + 1))
    axes[0].set_yticklabels(["Overall"] + Applications)
    axes[0].yaxis.tick_left()
    axes[0].tick_params(axis="y")

    plt.ylim(-1, 3)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.suptitle("Preference", fontsize=16, fontweight="bold")

    figurepath = f"{RootDir}/Result Figure/Summative Freeplay Preference [BarH].png"
    plt.savefig(figurepath, transparent=False)
    plt.close()

    print(f"Figure saved to {ColorText(figurepath, "green")}\n")


def TTestAnalysis():
    with open(f"{RootDir}/Processed Data/Summative_Freeplay_Likert_pval.txt", "w") as file:
        for app in Applications:
            file.write(f"Application: {app}\n")
            t, p = ttest_rel(ComfortData["ActuatedBed"][app], ComfortData["NormalBed"][app])
            file.write(f"Comfort: t = {t}, p = {p}\n")
            t, p = ttest_rel(PreferenceData["ActuatedBed"][app], PreferenceData["NormalBed"][app])
            file.write(f"Preference: t = {t}, p = {p}\n")
            file.write("\n")

TTestAnalysis()
