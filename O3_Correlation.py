import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import csv
from Constant import *


def ColorText(text, color):
    if color == "green":
        return f"\033[92m{text}\033[0m"
    elif color == "yellow":
        return f"\033[93m{text}\033[0m"
    elif color == "red":
        return f"\033[91m{text}\033[0m"
    else:
        return text


def PrintResult(corr, pval):
    print(
        "correlation coefficient: "
        + ColorText(str(corr), "green" if abs(corr) > 0.7 else "red")
        + " | p-value: "
        + ColorText(str(pval), "green" if abs(pval) < 0.05 else "red")
    )


print("Spearman’s Rank Correlation\n")

data = dict()
for pos in Postures:
    data[pos] = dict()
    for dir in Directions:
        data[pos][dir] = dict()
        for ang in Angles:
            data[pos][dir][ang] = list()

corr_data = {
    "Yaw": dict(),
    "Pitch": dict(),
}
for pos in Postures:
    corr_data["Yaw"][pos] = list()
    corr_data["Pitch"][pos] = list()


for pos in Postures:
    for i in Participants:
        filepath = (
            "Result Raw (ReCalculate)/O3_Final/" + f"Formative_O3_P{i}_{pos}_Final.csv"
        )
        df = pd.read_csv(filepath)

        for dir in Directions:
            dir_df = df.loc[df["Direction"] == dir]
            for ang in Angles:
                data[pos][dir][ang].extend(dir_df[ang].to_list())


with open("Result Processed/O3_Correlation.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    header = ["Posture", "Direction", "Pair", "Corr", "P-value"]
    writer.writerow(header)

    for pos in Postures:
        for dir in Directions:
            print(f"\nPosture: {pos} | Direction: {dir}")
            print("==================================")

            print("[1] HeadYaw & TrunkYaw")
            print(
                "dataset size:",
                len(data[pos][dir]["HeadYaw"]),
                len(data[pos][dir]["TrunkYaw"]),
            )

            corr, pval = stats.spearmanr(
                data[pos][dir]["HeadYaw"], data[pos][dir]["TrunkYaw"]
            )
            corr_data["Yaw"][pos].append(corr)
            writer.writerow([pos, dir, "Yaw", corr, pval])

            PrintResult(corr, pval)

            # plt.scatter(data[pos][dir]["HeadYaw"], data[pos][dir]["TrunkYaw"])
            # plt.xlabel("HeadYaw")
            # plt.ylabel("TrunkYaw")
            # plt.title(f"{pos} {dir} HeadYaw vs. TrunkYaw")
            # plt.savefig("Result Figure/O3_Scatter/" + f"O3_{pos}_{dir}_Yaw_Scatter.png")
            # plt.close()

            print("[2] HeadPitch & TrunkPitch")
            print(
                "dataset size:",
                len(data[pos][dir]["HeadPitch"]),
                len(data[pos][dir]["TrunkPitch"]),
            )

            corr, p = stats.spearmanr(
                data[pos][dir]["HeadPitch"], data[pos][dir]["TrunkPitch"]
            )
            corr_data["Pitch"][pos].append(corr)
            writer.writerow([pos, dir, "Pitch", corr, pval])

            PrintResult(corr, pval)

            # plt.scatter(data[pos][dir]["HeadPitch"], data[pos][dir]["TrunkPitch"])
            # plt.xlabel("HeadPitch")
            # plt.ylabel("TrunkPitch")
            # plt.title(f"{pos} {dir} HeadPitch vs. TrunkPitch")
            # plt.savefig("Result Figure/O3_Scatter/"  + f"O3_{pos}_{dir}_Pitch_Scatter.png")
            # plt.close()


def DrawBarChart(pair):
    # 設置長條的X軸位置
    x = np.arange(len(Directions))
    width = 0.35  # 長條的寬度

    # 繪製長條圖
    fig, ax = plt.subplots()
    ax.bar(
        x - width / 2,
        corr_data[pair]["Standing"],
        width,
        alpha=0.5,
        label=Postures[0],
    )
    ax.bar(
        x + width / 2,
        corr_data[pair]["Lying"],
        width,
        alpha=0.5,
        label=Postures[1],
    )

    # 添加一些文本標籤
    ax.set_xlabel("Directions")
    ax.set_ylabel("Correlation Coefficient")
    ax.set_title(f"Head{pair} & Trunk{pair} with different postures and directions")
    ax.set_xticks(x)
    ax.set_xticklabels(Directions)
    ax.legend()

    plt.savefig("Result Figure/" + f"O3_{pair}_Correlation.png", transparent=False)
    plt.close()


DrawBarChart("Yaw")
DrawBarChart("Pitch")
