from config import *
from utils import *

import pprint
import csv
import pygsheets
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
from scipy.stats import ttest_rel, wilcoxon
from math import pi


OUTPUT_DIR = f"{ROOT_DIR}/output/freeplay"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-IjhrdKDni0EvxxDpv7XBS_NbntPGaFGrRXMuX55Mzo"
# please replace the service_account_file with your own credentials
# (on local, do not upload to github)
gc = pygsheets.authorize(
    service_account_file="Credentials/headturner-423306-80a2fe1a0f33.json"
)

logger = LOGGER(f"{OUTPUT_DIR}/freeplay.log")


def scale_metrics(variable_name):
    logger.PRINT_LOG("SCALE METRICS START", bcolors.OKBLUE, f"freeplay {variable_name}")
    logger.ADD_LEVEL()

    # get dataframe from Google Sheet
    sh = gc.open_by_url(SHEET_URL)
    wks = sh.sheet1
    df = wks.get_as_df()

    # remove pilot data
    df = df.loc[df["受試者編號"] > 0]

    # put data into dict
    # d[condition][application] = [values]
    d = {}
    for condition in CONDITIONS:
        for app in APPLICATIONS:
            d.setdefault(condition, {}).setdefault(
                app,
                df[f"{app}-{variable_name}-{condition}"].tolist(),
            )

    # calculate pval
    output_file = f"{OUTPUT_DIR}/summative freeplay {variable_name} pval.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["APPLICATIONS", "TTEST", "WILCOXON"])

        for app in APPLICATIONS:
            c1 = d[CONDITIONS[0]][app]
            c2 = d[CONDITIONS[1]][app]

            _, p = ttest_rel(c1, c2)
            _, wp = wilcoxon(c1, c2)

            writer.writerow([app, p, wp])
    logger.PRINT_LOG("CALCULATE PVAL", bcolors.OKGREEN, f"save to {output_file}")

    # calculate stat
    mean_d = {}
    std_d = {}

    output_file = f"{OUTPUT_DIR}/summative freeplay {variable_name} stat.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["APPLICATIONS", "CONDITIONS", "MEAN", "STD"])

        for app in APPLICATIONS:
            for condition in CONDITIONS:
                values = d[condition][app]

                mean_ = stat.mean(values)
                mean_d.setdefault(condition, {})[app] = mean_

                std_ = stat.stdev(values)
                std_d.setdefault(condition, {})[app] = std_

                writer.writerow([app, condition, mean_, std_])
    logger.PRINT_LOG("CALCULATE STAT", bcolors.OKGREEN, f"save to {output_file}")

    # draw metric figure
    draw_scale_metrics(variable_name, mean_d, std_d, 10)

    logger.SUB_LEVEL()


def draw_scale_metrics(variable_name, mean_d, std_d, y_limit=10):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot()

    x = np.arange(len(APPLICATIONS))
    width = 0.3
    offset = [-width / 2, width / 2]

    for i, condition in enumerate(CONDITIONS):
        data = list(mean_d[condition].values())
        std_data = list(std_d[condition].values())
        ax.bar(
            x + offset[i],
            data,
            width,
            color=COLORS[condition][DARK],
            label=condition,
            yerr=std_data,
            capsize=3,
        )

    plt.ylim(0, y_limit)
    ax.set_xlabel("Application")
    ax.set_xticks(x)
    ax.set_xticklabels(APPLICATIONS)

    plt.legend(loc="best")
    fig_title = f"Summative Freeplay {variable_name}"
    plt.title(fig_title, pad=20, color="black", size=16)

    fig_path = f"{OUTPUT_DIR}/summative freeplay scale {variable_name}.png"
    plt.savefig(fig_path, transparent=False)
    plt.close()

    logger.PRINT_LOG("DRAW SCALE METRIC", bcolors.OKGREEN, f"save to {fig_path}")


def likert_metrics(variable_name):
    logger.PRINT_LOG(
        "LIKERT METRICS START", bcolors.OKBLUE, f"freeplay {variable_name}"
    )
    logger.ADD_LEVEL()

    # get dataframe from Google Sheet
    sh = gc.open_by_url(SHEET_URL)
    wks = sh.sheet1
    df = wks.get_as_df()

    # remove pilot data
    df = df.loc[df["受試者編號"] > 0]

    # put data into dict
    # rd[application] = [all voted points]
    # d[condition][application][point] = [num of people voting this point]
    rd = dict()
    d = dict()
    for condition in CONDITIONS:
        for app in APPLICATIONS:
            d.setdefault(condition, {}).setdefault(app, [0] * len(LIKERT_POINT))

    for app in APPLICATIONS:
        for i, row in df.iterrows():
            align = row[f"{app}-{variable_name}-1"]
            if align == "NormalBed":
                point = -int(row[f"{app}-{variable_name}-2"])
            elif align == "ActuatedBed":
                point = int(row[f"{app}-{variable_name}-2"])

            rd.setdefault(app, []).append(point)
            d[align][app][abs(point) - 1] += 1

    if variable_name == "Preference":
        for condition in CONDITIONS:
            d.setdefault(condition, {}).setdefault("Overall", [0] * len(LIKERT_POINT))
        for i, row in df.iterrows():
            align = row[f"Overall-{variable_name}"]
            d[align]["Overall"][len(LIKERT_POINT) - 1] += 1

    pprint.pprint(d)

    # calculate pval
    output_file = f"{OUTPUT_DIR}/summative freeplay {variable_name} pval.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["APPLICATIONS", "WILCOXON"])

        for app in APPLICATIONS:
            _, wp = wilcoxon(rd[app])
            writer.writerow([app, wp])
    logger.PRINT_LOG("CALCULATE PVAL", bcolors.OKGREEN, f"save to {output_file}")

    # draw metric figure
    draw_likert_metrics(variable_name, d)

    logger.SUB_LEVEL()


def draw_likert_metrics(variable_name, d):
    y_group = (
        APPLICATIONS + ["Overall"] if variable_name == "Preference" else APPLICATIONS
    )

    fig, axes = plt.subplots(figsize=(12, 4), ncols=2, sharey=True)
    fig.tight_layout()

    for i, condition in enumerate(reversed(CONDITIONS)):
        data = np.array(list(d[condition].values()))
        data_cum = data.cumsum(axis=1)

        axes[i].set_title(condition, color=COLORS[condition][DARKEST])
        axes[i].set_xlim(0, 14)
        axes[i].set_xticks([0, 2, 4, 6, 8, 10, 12, 14])

        for j in range(0, len(LIKERT_POINT)):
            widths = data[:, j]
            starts = data_cum[:, j] - widths
            rects = axes[i].barh(
                y_group,
                widths,
                left=starts,
                align="center",
                height=0.4,
                color=COLORS[condition][j],
            )
            for rect in rects:
                x, y = rect.get_xy()
                w, h = rect.get_width(), rect.get_height()
                if w == 0 or x == 0:
                    continue
                axes[i].plot([x, x], [y + 0.01, y + h - 0.01], color="black", lw=1)

    axes[0].invert_xaxis()
    axes[0].set_yticks(range(len(y_group)))
    axes[0].set_yticklabels(y_group)
    axes[0].yaxis.tick_left()
    axes[0].tick_params(axis="y")

    plt.ylim(-1, 3)
    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    plt.suptitle("Preference", fontsize=16, fontweight="bold")

    fig_path = f"{OUTPUT_DIR}/summative freeplay likert {variable_name}.png"
    plt.savefig(fig_path, transparent=False)
    plt.close()

    logger.PRINT_LOG("DRAW LIKERT METRIC", bcolors.OKGREEN, f"save to {fig_path}")


# scale_metrics("Effort")
# scale_metrics("Dizziness")
likert_metrics("Comfort")
likert_metrics("Preference")
