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


OUTPUT_DIR = f"{ROOT_DIR}/output/formative"

logger = LOGGER(f"{OUTPUT_DIR}/formative.log")


def detect_baddata(lst, variable_name, condition, direction, participant):
    if variable_name == "MaxViewingRange":
        range_threshold = HEAD_RANGE_THRESHOLD
    elif variable_name == "MaxBodyRange":
        range_threshold = BODY_RANGE_THRESHOLD

    logger.PRINT_LOG(
        "INFO", bcolors.ENDC, f"check {lst} @ P{participant} {condition} {direction}"
    )

    # detect exterem values
    o_lst = lst.copy()
    for value in o_lst:
        if (
            value < range_threshold[condition][direction][0]
            or value > range_threshold[condition][direction][1]
        ):
            logger.PRINT_LOG(
                "EXCEED THRESHOLD",
                bcolors.WARNING,
                f"{value:<10}",
            )
            lst.remove(value)

    if len(lst) <= 1:
        return lst

    # detect outliers
    md = stat.median(lst)

    for value in lst:
        if abs(value - md) > OUTLIER_THRESHOLD:
            logger.PRINT_LOG(
                "OUTLIER",
                bcolors.WARNING,
                f"{value:<10}",
            )
            lst.remove(value)

    return lst


def task1_range(variable_name):
    logger.PRINT_LOG("TASK1 RANGE START", bcolors.OKBLUE, f"{variable_name}")
    logger.ADD_LEVEL()

    # read raw data
    # d[direction][condition][participant] = value
    d = {}
    baddatas = []

    for participant in PARTICIPANTS:
        for condition in CONDITIONS:

            input_file = f"{ROOT_DIR}/raw data/formative/task1/Summative_T1_P{participant}_{condition}.csv"
            try:
                with open(input_file, newline="") as f:
                    reader = csv.DictReader(f)
                    lst = []

                    for row in reader:
                        direction = row["Direction"]
                        count = int(row["tCount"])
                        lst.append(abs(float(row[variable_name])))

                        if count == 3:
                            lst = detect_baddata(
                                lst,
                                variable_name,
                                condition,
                                direction,
                                participant,
                            )

                            if len(lst) == 0:
                                x = -1
                                baddatas.append(f"{participant} {direction}")
                            else:
                                x = stat.fmean(lst)

                            d.setdefault(direction, {}).setdefault(condition, {})[
                                participant
                            ] = x
                            lst = []

            except FileNotFoundError:
                logger.PRINT_LOG(
                    "FILE NOT FOUND", bcolors.FAIL, f"{input_file} not found"
                )
    logger.PRINT_LOG("READ RAW DATA", bcolors.OKGREEN, f"read {variable_name} data")

    # remove baddata's condition pairs, if "P4 NormalBed Right" is baddata, remove "P4 ActuatedBed Right"
    for baddata in baddatas:
        participant, direction = baddata.split()
        for condition in CONDITIONS:
            d[direction][condition].pop(int(participant))
            logger.PRINT_LOG(
                "REMOVE BAD DATA",
                bcolors.FAIL,
                f"P{participant} {condition} {direction}",
            )

    # calculate pval
    output_file = f"{OUTPUT_DIR}/summative task1 {variable_name} pval.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DIRECTIONS", "TTEST", "WILCOXON"])

        for direction in DIRECTIONS:
            c1 = list(d[direction][CONDITIONS[0]].values())
            c2 = list(d[direction][CONDITIONS[1]].values())

            _, p = ttest_rel(c1, c2)
            _, wp = wilcoxon(c1, c2)

            writer.writerow([direction, p, wp])
    logger.PRINT_LOG("CALCULATE PVAL", bcolors.OKGREEN, f"save to {output_file}")

    # calculate stat
    mean_d = {}

    output_file = f"{OUTPUT_DIR}/summative task1 {variable_name} stat.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DIRECTIONS", "CONDITIONS", "MEAN", "STD", "MIN", "MAX"])

        for direction in DIRECTIONS:
            for condition in CONDITIONS:
                values = list(d[direction][condition].values())

                mean_ = stat.mean(values)
                mean_d.setdefault(direction, {})[condition] = mean_

                std_ = stat.stdev(values)

                min_ = min(values)
                for p, v in d[direction][condition].items():
                    if v == min_:
                        min_p = p

                max_ = max(values)
                for p, v in d[direction][condition].items():
                    if v == max_:
                        max_p = p

                writer.writerow(
                    [
                        direction,
                        condition,
                        mean_,
                        std_,
                        f"{min_}@P{min_p}",
                        f"{max_}@P{max_p}",
                    ]
                )
    logger.PRINT_LOG("CALCULATE STAT", bcolors.OKGREEN, f"save to {output_file}")

    # draw range figure
    draw_range(variable_name, "YAW", mean_d)
    draw_range(variable_name, "PITCH", mean_d)

    logger.SUB_LEVEL()


def draw_range(variable_name, orientation, d):
    if orientation == "YAW":
        d1 = d["Right"]
        d2 = d["Left"]
        angle_labels = [
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
    elif orientation == "PITCH":
        d1 = d["Up"]
        d2 = d["Down"]
        angle_labels = [
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
    else:
        logger.PRINT_LOG("DRAW RADAR", bcolors.FAIL, "invalid orientation")
        return

    plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection="polar")

    N = int(360 / 30)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    begin = pi / 2 if orientation == "YAW" else 0
    bottom = 4

    for condition in CONDITIONS:
        l_value = d1[condition] / 180 * pi
        r_value = d2[condition] / 180 * pi
        logger.PRINT_LOG("DRAW RADAR", bcolors.ENDC, f"{condition} {l_value} {r_value}")
        offset = (l_value + r_value) / 2 - r_value

        ax.bar(
            x=(begin + offset),
            height=(10 - bottom),
            width=(l_value + r_value),
            bottom=bottom,
            color=COLORS[condition][DARK] + "32",  # make it transparent
            edgecolor=COLORS[condition][DARK],
            linewidth=3,
            linestyle="solid",
            label=condition,
        )

    # Draw x axis
    plt.xticks(angles, angle_labels, color="black", size=10)
    ax.tick_params(axis="x", which="major", pad=20)
    # Draw y axis
    plt.yticks([0, 10], color="grey", size=0)
    plt.ylim(0, 10)

    plt.legend(loc="best", bbox_to_anchor=(0, 0))

    fig_title = f"{variable_name} {orientation}"
    plt.title(fig_title, pad=20, color="black", size=16)

    fig_path = f"{OUTPUT_DIR}/summative {variable_name} {orientation}.png"
    plt.savefig(fig_path, transparent=False)

    plt.close()

    logger.PRINT_LOG("DRAW RADAR", bcolors.OKGREEN, f"save to {fig_path}")


def form_metrics(task_id, variable_name):
    logger.PRINT_LOG(
        "FORM METRICS START", bcolors.OKBLUE, f"task{task_id} {variable_name}"
    )
    logger.ADD_LEVEL()

    # get dataframe from Google Sheet
    # please replace the service_account_file with your own credentials
    # (on local, do not upload to github)
    gc = pygsheets.authorize(
        service_account_file="Credentials/headturner-423306-80a2fe1a0f33.json"
    )
    sheet_url = "https://docs.google.com/spreadsheets/d/1RaLsqFa9m0g6LUvFIRlKljvgqYiR2TWYYIr_orydQkU"
    sh = gc.open_by_url(sheet_url)
    wks = sh.sheet1
    df = wks.get_as_df()

    # remove pilot data
    df = df.loc[df["受試者編號"] > 0]

    # put data into dict
    # d[condition][direction] = [values]
    d = {}
    for condition in CONDITIONS:
        for direction in DIRECTIONS:
            d.setdefault(condition, {}).setdefault(
                direction,
                df[f"Task{task_id}-{variable_name}-{condition}-{direction}"].tolist(),
            )

    # calculate pval
    output_file = f"{OUTPUT_DIR}/summative task{task_id} {variable_name} pval.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DIRECTIONS", "TTEST", "WILCOXON"])

        for direction in DIRECTIONS:
            c1 = d[CONDITIONS[0]][direction]
            c2 = d[CONDITIONS[1]][direction]

            _, p = ttest_rel(c1, c2)
            _, wp = wilcoxon(c1, c2)

            writer.writerow([direction, p, wp])
    logger.PRINT_LOG("CALCULATE PVAL", bcolors.OKGREEN, f"save to {output_file}")

    # calculate stat
    mean_d = {}
    std_d = {}

    output_file = f"{OUTPUT_DIR}/summative task{task_id} {variable_name} stat.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DIRECTIONS", "CONDITIONS", "MEAN", "STD"])

        for condition in CONDITIONS:
            for direction in DIRECTIONS:
                values = d[condition][direction]

                mean_ = stat.mean(values)
                mean_d.setdefault(condition, {})[direction] = mean_

                std_ = stat.stdev(values)
                std_d.setdefault(condition, {})[direction] = std_

                writer.writerow([direction, condition, mean_, std_])
    logger.PRINT_LOG("CALCULATE STAT", bcolors.OKGREEN, f"save to {output_file}")

    # draw metric figure
    draw_metric(task_id, variable_name, mean_d, std_d, y_limit=10, annotate=False)

    logger.SUB_LEVEL()


def draw_metric(task_id, variable_name, mean_d, std_d=None, y_limit=10, annotate=False):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)

    N = len(DIRECTIONS)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Draw direction axes
    ax.xaxis.set_label_position("bottom")
    plt.xticks(angles[:-1], DIRECTIONS, color="black", size=10)
    ax.tick_params(axis="x", which="major", pad=20)

    # Draw range labels
    ax.yaxis.set_label_position("left")
    ax.set_rlabel_position(20)
    labels = np.arange(0, y_limit, y_limit / 5)
    plt.yticks(labels, color="grey", size=0)
    plt.ylim(0, y_limit)

    # Plot the data
    for condition in CONDITIONS:
        values = list(mean_d[condition].values())
        logger.PRINT_LOG("DRAW METRIC", bcolors.ENDC, f"{condition} {values}")
        values += values[:1]

        if std_d is None:
            ax.plot(
                angles,
                values,
                color=COLORS[condition][MEDIUM],
                linewidth=2,
                linestyle="solid",
                label=condition,
            )
        else:
            std_values = list(std_d[condition].values())
            std_values += std_values[:1]
            ax.errorbar(
                angles,
                values,
                color=COLORS[condition][MEDIUM],
                linewidth=2,
                linestyle="solid",
                label=condition,
                yerr=std_values,
                ecolor=COLORS[condition][MEDIUM],
                capsize=5,
            )

        ax.fill(angles, values, color=COLORS[condition][MEDIUM], alpha=0.1)
        if annotate:
            for a, v in zip(angles, values):
                ax.annotate(
                    "%.2f" % v, (a, v), textcoords="offset points", xytext=(0, 10)
                )

    plt.legend(loc="best", bbox_to_anchor=(1, 0))

    fig_title = f"task{task_id} {variable_name}"
    plt.title(fig_title, pad=20, color="black", size=16)

    fig_path = f"{OUTPUT_DIR}/summative task{task_id} {variable_name}"
    if std_d is not None:
        fig_path += " w-std"
    if annotate:
        fig_path += " w-annotate"
    fig_path += ".png"
    plt.savefig(fig_path, transparent=False)

    plt.close()

    logger.PRINT_LOG("DRAW METRIC", bcolors.OKGREEN, f"save to {fig_path}")


task1_range("MaxViewingRange")
task1_range("MaxBodyRange")

# form_metrics(1, "Effort")
# form_metrics(2, "Effort")
# form_metrics(2, "Dizziness")
