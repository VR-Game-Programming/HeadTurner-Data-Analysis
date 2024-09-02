import matplotlib.pyplot as plt
import csv
import statistics as stat
from scipy.stats import ttest_rel, wilcoxon
from math import pi
from Constant import *


def CalculateAvgAngle(values, threshold):
    normal = []
    for value in values:
        if value > threshold:
            normal.append(value)
    if len(normal) == 0:
        return 0
    else:
        return stat.fmean(normal)

def ReadRawRsult():
    DataDict = dict()
    for part in ["Head", "Body"]:
        DataDict[part] = dict()
        for direction in Directions:
            DataDict[part][direction] = dict()
            for condition in Conditions:
                DataDict[part][direction][condition] = dict()
                for participant in Participants:
                    DataDict[part][direction][condition][participant] = -1

    outlierList = list()
    for participant in Participants:
        if participant == 10:
            continue
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
                        haed_avg = CalculateAvgAngle(headRangeList, 10)
                        if (haed_avg == 0):
                            outlierList.append(f"Head_{participant}_{direction}")
                        DataDict["Head"][direction][condition][participant] = haed_avg

                        body_avg = CalculateAvgAngle(bodyRangeList, 0)
                        if (body_avg == 0):
                            outlierList.append(f"Body_{participant}_{direction}")
                        DataDict["Body"][direction][condition][participant] = body_avg

                        headRangeList = list()
                        bodyRangeList = list()

    return DataDict, outlierList

def RemoveOutlier(DataDict, outlierList):
    # Remove outlier
    for outlier in outlierList:
        part, participant, direction = outlier.split("_")
        print(part, participant, direction)
        for condition in Conditions:
            DataDict[part][direction][condition][int(participant)] = -1

    for part in ["Head", "Body"]:
        for direction in Directions:
            for condition in Conditions:
                tmp_list = list()
                for value in list(DataDict[part][direction][condition].values()):
                    if value != -1:
                        tmp_list.append(value)
                DataDict[part][direction][condition] = tmp_list

    return DataDict

def PrintDataDict2CSV(DataDict):
    for part in ["Head", "Body"]:
        filepath = f"{RootDir}/Processed Data/Summative_T1_{part}MaximumRange_Raw.csv"
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Direction", "Condition", "Range"])
            for direction in Directions:
                for condition in Conditions:
                    for value in DataDict[part][direction][condition]:
                        writer.writerow([direction, condition, value])

def CalculatePval(DataDict):
    for part in ["Head", "Body"]:
        filepath = f"{RootDir}/Processed Data/Summative_T1_{part}MaximumRange_pval.csv"
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Direction", "paired-t", "wilcoxon"])

            for direction in Directions:
                _, p = ttest_rel(
                    DataDict[part][direction]["ActuatedBed"],
                    DataDict[part][direction]["NormalBed"],
                )
                _, wp = wilcoxon(
                    DataDict[part][direction]["ActuatedBed"],
                    DataDict[part][direction]["NormalBed"],
                )
                writer.writerow([direction, p, wp])

def CalculateAVGSTD(DataDict):
    AvgDict = dict()
    StdDict = dict()

    for part in ["Head", "Body"]:
        AvgDict[part] = dict()
        StdDict[part] = dict()

        for direction in Directions:
            AvgDict[part][direction] = dict()
            StdDict[part][direction] = dict()

            for condition in Conditions:
                AvgDict[part][direction][condition] = stat.fmean(DataDict[part][direction][condition])
                StdDict[part][direction][condition] = stat.stdev(DataDict[part][direction][condition])

    for part in ["Head", "Body"]:
        filepath = f"{RootDir}/Processed Data/Summative_T1_{part}MaximumRange.csv"
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Direction", "Condition", "Avg", "Std"])
            for direction in Directions:
                for condition in Conditions:
                    writer.writerow(
                        [
                            direction,
                            condition,
                            AvgDict[part][direction][condition],
                            StdDict[part][direction][condition],
                        ]
                    )

    return AvgDict, StdDict

def DrawRangeRadarChart(FigureTitle, FigurePath, LeftData, RightData, Type):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection="polar")

    N = int(360 / 30)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    begin = pi / 2 if Type == "LR" else 0
    bottom = 4

    for i, group in enumerate(Conditions):
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

def DrawAllFigure(DataDict):
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

# Main
DataDict, outlierList = ReadRawRsult()
DataDict = RemoveOutlier(DataDict, outlierList)
PrintDataDict2CSV(DataDict)
CalculatePval(DataDict)
AvgDict, StdDict = CalculateAVGSTD(DataDict)
DrawAllFigure(AvgDict)
