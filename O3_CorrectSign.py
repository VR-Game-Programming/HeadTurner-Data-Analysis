import pandas as pd
from Constant import *

for i in Participants:
    for pos in Postures:
        print(f"Participant {i}, {pos}")

        # Read the data
        filepath = (
            "Result Raw (ReCalculate)/O3_ReCalculate/"
            + f"Formative_O3_P{i}_{pos}_ReCalculate.csv"
        )
        df = pd.read_csv(filepath)

        # Get the sum of the last row of each task
        HeadYaw = TrunkYaw = 0
        for t in range(1, 4):
            rows = df.loc[df["Direction"] == "Right"].loc[df["tCount"] == t]
            last_row = rows.iloc[-1]
            HeadYaw += float(last_row["HeadYaw"])
            TrunkYaw += float(last_row["TrunkYaw"])

        HeadPitch = TrunkPitch = 0
        for t in range(1, 4):
            rows = df.loc[df["Direction"] == "Down"].loc[df["tCount"] == t]
            last_row = rows.iloc[-1]
            HeadPitch += float(last_row["HeadPitch"])
            TrunkPitch += float(last_row["TrunkPitch"])

        HeadYawSign = 1 if HeadYaw > 0 else -1
        HeadPitchSign = 1 if HeadPitch < 0 else -1
        TrunkYawSign = 1 if TrunkYaw > 0 else -1
        TrunkPitchSign = 1 if TrunkPitch < 0 else -1

        print(
            f"New Sign: {HeadYawSign}, {TrunkYawSign}, {HeadPitchSign}, {TrunkPitchSign}\n"
        )

        for index, row in df.iterrows():
            df.at[index, "HeadYaw"] = row["HeadYaw"] * HeadYawSign
            df.at[index, "HeadPitch"] = row["HeadPitch"] * HeadPitchSign
            df.at[index, "TrunkYaw"] = row["TrunkYaw"] * TrunkYawSign
            df.at[index, "TrunkPitch"] = row["TrunkPitch"] * TrunkPitchSign

        # Save the corrected data
        df.to_csv(
            "Result Raw (ReCalculate)/O3_Final/" + f"Formative_O3_P{i}_{pos}_Final.csv",
            index=False,
        )
