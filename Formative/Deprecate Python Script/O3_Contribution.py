import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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


data = dict()
for pos in Postures:
    data[pos] = dict()
    for dir in Directions:
        data[pos][dir] = dict()
        for ang in Angles:
            data[pos][dir][ang] = list()

contribution_data = {
    "Standing": {
        "Yaw": {"Head": list(), "Trunk": list()},
        "Pitch": {"Head": list(), "Trunk": list()},
    },
    "Lying": {
        "Yaw": {"Head": list(), "Trunk": list()},
        "Pitch": {"Head": list(), "Trunk": list()},
    },
}

percentage_data = {
    "Standing": {
        "Yaw": {"Head": list(), "Trunk": list()},
        "Pitch": {"Head": list(), "Trunk": list()},
    },
    "Lying": {
        "Yaw": {"Head": list(), "Trunk": list()},
        "Pitch": {"Head": list(), "Trunk": list()},
    },
}


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


# Calculate Contribution
# =============================================================================
def CalculateContribution(pos, dir, type, head_arr, trunk_arr):
    print(f"[1] {type}")

    # Process the data
    head_arr = np.array(head_arr)
    trunk_arr = np.array(trunk_arr)
    same_sign_mask = (head_arr * trunk_arr) > 0
    real_head_arr = np.where(same_sign_mask, head_arr - trunk_arr, head_arr + trunk_arr)

    # Turn to 2d array
    data = np.vstack((real_head_arr, trunk_arr)).T

    # Standardize the data
    std_data = StandardScaler().fit_transform(data)

    # PCA
    # We don't downscale the data because we want to know the contribution of each component
    pca = PCA(n_components=2)
    L = pca.fit_transform(std_data)

    head_contribution = round(pca.explained_variance_ratio_[0] * 100, 2)
    trunk_contribution = round(pca.explained_variance_ratio_[1] * 100, 2)

    print(f"Head Contribution: {head_contribution}%")
    print(f"Trunk Contribution: {trunk_contribution}%")

    contribution_data[pos][type]["Head"].append(head_contribution)
    contribution_data[pos][type]["Trunk"].append(trunk_contribution)

    return head_contribution, trunk_contribution


with open("Result Processed/O3_Contribution.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    header = [
        "Posture",
        "Direction",
        "Type",
        "Head Contribution",
        "Trunk Contribution",
    ]
    writer.writerow(header)

    for pos in Postures:
        for dir in Directions:
            print(f"\nPosture: {pos} | Direction: {dir}")
            print("==================================")

            yaw_head, yaw_trunk = CalculateContribution(
                pos, dir, "Yaw", data[pos][dir]["HeadYaw"], data[pos][dir]["TrunkYaw"]
            )
            pitch_head, pitch_trunk = CalculateContribution(
                pos,
                dir,
                "Pitch",
                data[pos][dir]["HeadPitch"],
                data[pos][dir]["TrunkPitch"],
            )

            writer.writerow([pos, dir, "Yaw", yaw_head, yaw_trunk])
            writer.writerow([pos, dir, "Pitch", pitch_head, pitch_trunk])


# Calculate Percentage
# =============================================================================
# def CalculatePercentage(pos, dir, type, total_arr, trunk_arr):
#     print(f"[1] {type}")

#     total_np_arr = np.array(total_arr)
#     total_np_arr_nz = total_np_arr[total_np_arr != 0]
#     trunk_np_arr = np.array(trunk_arr)
#     trunk_np_arr_nz = trunk_np_arr[total_np_arr != 0]
#     head_np_arr_nz = abs(total_np_arr_nz - trunk_np_arr_nz)

#     head_percentage_arr = abs(head_np_arr_nz / total_np_arr_nz) * 100
#     trunk_percentage_arr = abs(trunk_np_arr_nz / total_np_arr_nz) * 100

#     head_percentage = round(np.mean(head_percentage_arr), 2)
#     trunk_percentage = round(np.mean(trunk_percentage_arr), 2)

#     print(f"Head Percentage: {head_percentage}%")
#     print(f"Trunk Percentage: {trunk_percentage}%")

#     percentage_data[pos][type]["Head"].append(head_percentage)
#     percentage_data[pos][type]["Trunk"].append(trunk_percentage)

#     return head_percentage, trunk_percentage


# with open("Result Processed/O3_Percentage.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)

#     header = [
#         "Posture",
#         "Direction",
#         "Type",
#         "Head Percentage",
#         "Trunk Percentage",
#     ]
#     writer.writerow(header)

#     for pos in Postures:
#         for dir in Directions:
#             print(f"\nPosture: {pos} | Direction: {dir}")
#             print("==================================")

#             yaw_head, yaw_trunk = CalculatePercentage(
#                 pos, dir, "Yaw", data[pos][dir]["HeadYaw"], data[pos][dir]["TrunkYaw"]
#             )
#             pitch_head, pitch_trunk = CalculatePercentage(
#                 pos,
#                 dir,
#                 "Pitch",
#                 data[pos][dir]["HeadPitch"],
#                 data[pos][dir]["TrunkPitch"],
#             )

#             writer.writerow([pos, dir, "Yaw", yaw_head, yaw_trunk])
#             writer.writerow([pos, dir, "Pitch", pitch_head, pitch_trunk])


# Draw Bar Chart
# =============================================================================
def DrawBarChart(type):
    x = np.arange(len(Directions))
    width = 0.3
    s_colors = ["#54bebe", "#98d1d1"]
    l_colors = ["#c80064", "#d7658b"]

    fig, ax = plt.subplots(figsize=(15, 10))
    # plt.figure(figsize=(10, 10))

    bottom = np.zeros(8)
    for i, part in enumerate(["Head", "Trunk"]):
        ax.bar(
            x - width / 2 - 0.02,
            contribution_data["Standing"][type][part],
            width,
            color=s_colors[i],
            label=f"{part} (Standing)",
            bottom=bottom,
        )
        for xpos, ypos, value in zip(
            x, bottom, contribution_data["Standing"][type][part]
        ):
            plt.text(
                x=xpos - width / 2 - 0.2,
                y=ypos + value / 2,
                s=f"{value}%",
                color="black",
                fontsize=10,
            )
        bottom += contribution_data["Standing"][type][part]

    bottom = np.zeros(8)
    for i, part in enumerate(["Head", "Trunk"]):
        ax.bar(
            x + width / 2 + 0.02,
            contribution_data["Lying"][type][part],
            width,
            color=l_colors[i],
            label=f"{part} (Lying)",
            bottom=bottom,
        )
        for xpos, ypos, value in zip(x, bottom, contribution_data["Lying"][type][part]):
            plt.text(
                x=xpos + width / 2 - 0.1,
                y=ypos + value / 2,
                s=f"{value}%",
                color="black",
                fontsize=10,
            )

        bottom += contribution_data["Lying"][type][part]

    ax.set_xticks(x)
    ax.set_xticklabels(Directions)
    plt.ylim(0, 120)
    plt.title(f"Head and Trunk Contributions on {type} Angle")
    plt.legend(loc="upper center", ncol=4)

    plt.savefig(f"Result Figure/O3_{type}_Contribution.png")
    plt.close()


DrawBarChart("Yaw")
DrawBarChart("Pitch")
