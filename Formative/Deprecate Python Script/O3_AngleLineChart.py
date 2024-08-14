import matplotlib.pyplot as plt
import pandas as pd
from Constant import *

for i in Participants:
    for pos in Postures:
        filepath = (
            "Result Raw (ReCalculate)/O3_Final/" + f"Formative_O3_P{i}_{pos}_Final.csv"
        )
        df = pd.read_csv(filepath)

        plt.figure(figsize=(10, 10))
        plt.title(pos)
        for index, row in df.iterrows():
            if (
                row["HeadYaw"] == 0
                and row["HeadPitch"] == 0
                and row["TrunkYaw"] == 0
                and row["TrunkPitch"] == 0
                and row["tCount"] == 1
            ):
                plt.axvline(x=index * 10, color="gray", linestyle="--", linewidth=0.5)
                plt.annotate(
                    row["Direction"],
                    (index * 10, 30),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                )
        plt.plot(df.index * 10, df["HeadYaw"], label="HeadYaw")
        plt.plot(df.index * 10, df["HeadPitch"], label="HeadPitch")
        plt.plot(df.index * 10, df["TrunkYaw"], label="TrunkYaw")
        plt.plot(df.index * 10, df["TrunkPitch"], label="TrunkPitch")
        plt.legend()
        plt.savefig("Result Figure/" + f"Formative_O3_Angle_P{i}_{pos}.png")
        # plt.show()
        plt.close()

        print(f"Participant {i}, {pos} figure done!")
