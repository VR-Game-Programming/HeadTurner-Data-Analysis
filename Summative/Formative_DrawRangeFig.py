import matplotlib.pyplot as plt
import csv
import statistics as stat
from math import pi
from Constant import *


def CalculateAvgAngle(directions, threshold):
    normal = []
    for value in directions:
        if value > threshold:
            normal.append(value)
    if len(normal) == 0:
        return 0
    else:
        return stat.fmean(normal)


DataDict = dict()
for part in ["Head", "Body"]:
    DataDict[part] = dict()
    for direction in Directions:
        DataDict[part][direction] = dict()
        for condition in Conditions:
            DataDict[part][direction][condition] = list()

# Read raw result
for participant in Participants:
    for condition in Conditions:
        filepath = f"{RootDir}/Raw Data/Summative_T1_P{participant}_{condition}.csv"
        with open(filepath, newline="") as csvfile:
            r = csv.DictReader(csvfile)
            headRangeList = list()
            bodyRangeList = list()
            for row in r:
                direction = row["Direction"]
                tcount = int(row["tCount"])
                headRangeList.append(abs(float(row["MaxViewingRange"])))
                bodyRangeList.append(abs(float(row["MaxBodyRange"])))
                if tcount == 3:
                    DataDict["Head"][direction][condition].append(
                        CalculateAvgAngle(headRangeList, 10)
                    )
                    DataDict["Body"][direction][condition].append(
                        CalculateAvgAngle(bodyRangeList, 0)
                    )
                    headRangeList = list()
                    bodyRangeList = list()

# Calculate AVG & STD
StdDict = dict()
for part in ["Head", "Body"]:
    StdDict[part] = dict()
    for direction in Directions:
        StdDict[part][direction] = dict()
        for condition in Conditions:
            StdDict[part][direction][condition] = stat.stdev(
                DataDict[part][direction][condition]
            )
            DataDict[part][direction][condition] = stat.fmean(
                DataDict[part][direction][condition]
            )

for part in ["Head", "Body"]:
    filepath = f"{RootDir}/Processed Data/Summative_T1_{part}MaximumRange.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Direction", "Condition", "Mean", "Std"])
        for direction in Directions:
            for condition in Conditions:
                writer.writerow(
                    [
                        direction,
                        condition,
                        DataDict[part][direction][condition],
                        StdDict[part][direction][condition],
                    ]
                )


def DrawRangeRadarChart(FigureTitle, FigurePath, LeftData, RightData, Type):
    print(f"Processing with data:\nLeftData: {LeftData}\nRightData: {RightData}")

    plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection="polar")

    N = int(360 / 30)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    begin = pi / 2 if Type == "LR" else 0
    bottom = 4
    hatches = ["\\", None]

    for i, group in enumerate(Conditions):
        leftValue = LeftData[group] / 180 * pi
        rightValue = RightData[group] / 180 * pi
        offset = (leftValue + rightValue) / 2 - rightValue
        ax.bar(
            x=(begin + offset),
            height=(10 - bottom - 0.1),
            width=(leftValue + rightValue),
            bottom=bottom,
            edgecolor=Colors[i][2],
            linewidth=3,
            linestyle="solid",
            fill=False,
            label=group,
            hatch=hatches[i],
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

    print(f"Figure saved to {FigurePath}\n")


# Draw figures
DrawRangeRadarChart(
    FigureTitle="Head Maximum Viewing Range (Yaw)",
    FigurePath=f"{RootDir}/Result Figure/Summative T1 HeadMaximumRange Yaw.png",
    LeftData=DataDict["Head"]["Left"],
    RightData=DataDict["Head"]["Right"],
    Type="LR",
)

DrawRangeRadarChart(
    FigureTitle="Head Maximum Viewing Range (Pitch)",
    FigurePath=f"{RootDir}/Result Figure/Summative T1 HeadMaximumRange Pitch.png",
    LeftData=DataDict["Head"]["Up"],
    RightData=DataDict["Head"]["Down"],
    Type="UD",
)

DrawRangeRadarChart(
    FigureTitle="Body Maximum Viewing Range (Yaw)",
    FigurePath=f"{RootDir}/Result Figure/Summative T1 BodyMaximumRange Yaw.png",
    LeftData=DataDict["Body"]["Left"],
    RightData=DataDict["Body"]["Right"],
    Type="LR",
)

DrawRangeRadarChart(
    FigureTitle="Body Maximum Viewing Range (Pitch)",
    FigurePath=f"{RootDir}/Result Figure/Summative T1 BodyMaximumRange Pitch.png",
    LeftData=DataDict["Body"]["Up"],
    RightData=DataDict["Body"]["Down"],
    Type="UD",
)