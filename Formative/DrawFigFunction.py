import matplotlib.pyplot as plt
import numpy as np
from math import pi
from Constant import *

def DrawRadarChart(
    FigureTitle,
    Data,
    StdData,
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
    labels = np.arange(0, 180, 30)
    plt.yticks(labels, color="grey", size=0)
    plt.ylim(0, 180)

    # Plot the data
    for i, group in enumerate(Postures):
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

    figurepath = f"{RootDir}/Result Figure/Formative {FigureTitle}"
    figurepath += " [Radar]"
    if std:
        figurepath += " [STD]"
    if annotate:
        figurepath += " [Annotate]"
    figurepath += ".png"

    plt.savefig(figurepath, transparent=False)
    plt.close()
    print(f"Figure saved to {ColorText(figurepath, "green")}\n")

def DrawRangeRadarChart(FigureTitle, FigurePath, LeftData, RightData, Type):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection="polar")

    N = int(360 / 30)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    begin = pi / 2 if Type == "LR" else 0
    bottom = 4

    for i, group in enumerate(Postures):
        leftValue = LeftData[group] / 180 * pi
        rightValue = RightData[group] / 180 * pi
        offset = (leftValue + rightValue) / 2 - rightValue
        ax.bar(
            x=(begin + offset),
            height=(10 - bottom),
            width=(leftValue + rightValue),
            bottom=bottom,
            color=Colors[i][4] + "32",
            edgecolor=Colors[i][4],
            linewidth=3,
            linestyle="solid",
            label=group,
        )

    # Draw x axis
    plt.xticks(angles, RangeRadarChartAngleLabels[Type], color="black", size=10)
    ax.tick_params(axis="x", which="major", pad=20)

    # Draw y axis
    plt.yticks([0, 10], color="grey", size=0)
    plt.ylim(0, 10)

    plt.legend(loc="best", bbox_to_anchor=(0, 0))
    plt.title(FigureTitle, pad=20, color="black", size=16)
    plt.savefig(FigurePath, transparent=False)
    plt.close()

    print(f"Figure saved to {ColorText(FigurePath, "green")}\n")
