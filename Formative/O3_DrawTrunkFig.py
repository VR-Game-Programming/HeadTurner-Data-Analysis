import pandas as pd
from Constant import *
from DrawFigFunction import *

# Data Prepare
df = pd.read_csv(f"{RootDir}/Result Processed/O3_MaxTrunkRotation.csv")

range_data = dict()
for dir in ["Right", "Left"]:
    range_data[dir] = dict()
    for pos in Postures:
        data_row = (
            df.loc[df["Type"] == "TrunkYaw"]
            .loc[df["Direction"] == dir]
            .loc[df["Posture"] == pos]
        )
        range_data[dir][pos] = data_row["TrunkRotation"].values[0]

for dir in ["Up", "Down"]:
    range_data[dir] = dict()
    for pos in Postures:
        data_row = (
            df.loc[df["Type"] == "TrunkPitch"]
            .loc[df["Direction"] == dir]
            .loc[df["Posture"] == pos]
        )
        range_data[dir][pos] = data_row["TrunkRotation"].values[0]

# Draw Figure
DrawRangeRadarChart(
    FigureTitle="Trunk Maximum Viewing Range (Yaw)",
    FigurePath=f"{RootDir}/Result Figure/Formative T2 TrunkMaximumRange Yaw.png",
    LeftData=range_data["Left"],
    RightData=range_data["Right"],
    Type="LR",
)

DrawRangeRadarChart(
    FigureTitle="Trunk Maximum Viewing Range (Pitch)",
    FigurePath=f"{RootDir}/Result Figure/Formative T2 TrunkMaximumRange Pitch.png",
    LeftData=range_data["Up"],
    RightData=range_data["Down"],
    Type="UD",
)
