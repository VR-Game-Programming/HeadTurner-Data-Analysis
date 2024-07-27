import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
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


print("Linear Regression\n")

data = dict()
for pos in Postures:
    data[pos] = dict()
    for dir in Directions:
        data[pos][dir] = dict()
        for ang in Angles:
            data[pos][dir][ang] = list()

R_data = {
    "Yaw": dict(),
    "Pitch": dict(),
}
for pos in Postures:
    R_data["Yaw"][pos] = list()
    R_data["Pitch"][pos] = list()


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


with open("Result Processed/O3_Regression.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    header = ["Posture", "Direction", "Pair", "Slope", "Intercept", "R^2"]
    writer.writerow(header)

    for pos in Postures:
        for dir in Directions:
            print(f"\nPosture: {pos} | Direction: {dir}")
            print("==================================")

            # Yaw
            print("[1] HeadYaw & TrunkYaw")

            Head = np.array(data[pos][dir]["HeadYaw"])
            Trunk = np.array(data[pos][dir]["TrunkYaw"]).reshape(-1, 1)

            reg = LinearRegression()
            reg.fit(Trunk, Head)

            slope = reg.coef_[0]
            intercept = reg.intercept_
            r_squared = reg.score(Trunk, Head)

            print(f"Slope: {slope} | Intercept: {intercept} | R^2: {r_squared}")

            R_data["Yaw"][pos].append(r_squared)
            writer.writerow([pos, dir, "Yaw", slope, intercept, r_squared])

            # Pitch
            print("[2] HeadPitch & TrunkPitch")

            Head = np.array(data[pos][dir]["HeadPitch"])
            Trunk = np.array(data[pos][dir]["TrunkPitch"]).reshape(-1, 1)

            reg = LinearRegression()
            reg.fit(Trunk, Head)

            slope = reg.coef_[0]
            intercept = reg.intercept_
            r_squared = reg.score(Trunk, Head)
            print(f"Slope: {slope} | Intercept: {intercept} | R^2: {r_squared}")

            R_data["Pitch"][pos].append(r_squared)
            writer.writerow([pos, dir, "Pitch", slope, intercept, r_squared])


def DrawBarChart(pair):
    # 設置長條的X軸位置
    x = np.arange(len(Directions))
    width = 0.35  # 長條的寬度

    # 繪製長條圖
    fig, ax = plt.subplots()
    ax.bar(
        x - width / 2,
        R_data[pair]["Standing"],
        width,
        alpha=0.5,
        label=Postures[0],
    )
    ax.bar(
        x + width / 2,
        R_data[pair]["Lying"],
        width,
        alpha=0.5,
        label=Postures[1],
    )

    # 添加一些文本標籤
    ax.set_xlabel("Directions")
    ax.set_ylabel("R^2")
    ax.set_title(f"Head{pair} & Trunk{pair} with different postures and directions")
    ax.set_xticks(x)
    ax.set_xticklabels(Directions)
    ax.legend()

    plt.savefig("Result Figure/" + f"O3_{pair}_Regression.png", transparent=False)
    plt.close()


DrawBarChart("Yaw")
DrawBarChart("Pitch")
