import math
import json
import numpy as np
import matplotlib.pyplot as plt
from emg_single import get_result
from Constant import ColorText, Colors, Directions, Postures
from emg_single import get_result
from Constant import Directions, Postures
import csv

TOTAL_PARTICIPANTS = 16

results = {
    'Lying': [0] * 8,
    'Standing': [0] * 8
}

mcl_result = {}

for participant_number in range(1, TOTAL_PARTICIPANTS+1):
    for posture in ['Lying', 'Standing']:
        mcl = get_result(participant_number, posture, create_fig=False)
        results[posture] = [sum(x) for x in zip(results[posture], mcl)]
        if participant_number not in mcl_result:
            mcl_result[participant_number] = {}
        mcl_result[participant_number][posture] = mcl

results['Lying'] = [x / TOTAL_PARTICIPANTS for x in results['Lying']]
results['Standing'] = [x / TOTAL_PARTICIPANTS for x in results['Standing']]

data = mcl_result

with open('Result Processed/MCL Value.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    header = ['Participant', 'Posture'] + list(range(0, 360, 45))
    writer.writerow(header)

    # Write the data
    for participant, posture_data in data.items():
        for posture, values in posture_data.items():
            row = [participant, posture] + values
            writer.writerow(row)

print("Data has been written toResult Processed/MCL Value.csv")


average = {
    'Lying': [0] * 8,
    'Standing': [0] * 8
}

standard_deviation = {
    'Lying': [0] * 8,
    'Standing': [0] * 8
}

for posture in ['Lying', 'Standing']:
    for angle in range(8):
        values = [data[key][posture][angle] for key in data]
        average[posture][angle] = sum(values) / len(values)
        standard_deviation[posture][angle] = (
            sum([(x - average[posture][angle]) ** 2 for x in values]) / len(values)) ** 0.5


# # Draw Plot
# # 設置長條的X軸位置
# x = np.arange(len(Directions))
# width = 0.35  # 長條的寬度

# # 繪製長條圖
# fig, ax = plt.subplots(figsize=(15, 10))
# bars1 = ax.bar(
#     x - width / 2,
#     average[Postures[0]],
#     width,
#     label=Postures[0],
#     yerr=standard_deviation[Postures[0]],
#     capsize=3,
#     color=Colors[0][4],
# )
# bars2 = ax.bar(
#     x + width / 2,
#     average[Postures[1]],
#     width,
#     label=Postures[1],
#     yerr=standard_deviation[Postures[1]],
#     capsize=3,
#     color=Colors[1][4],
# )

# # 添加一些文本標籤
# ax.set_xlabel("Directions")
# ax.set_ylabel("MCL Value")
# ax.set_title("MCL Value with different postures and directions")
# ax.set_xticks(x)
# ax.set_xticklabels(Directions)
# ax.legend()

# plt.savefig("Result Figure/" + "T2_MCL.png", transparent=False)
# plt.show()


def DrawRadarChart(
    FigureTitle,
    Data,
    StdData,
    yLimit,
    std=False,
    annotate=False,
):
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)

    N = len(Directions)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    # Draw direction axes
    ax.xaxis.set_label_position("bottom")
    plt.xticks(angles[:-1], Directions, color="black", size=10)
    ax.tick_params(axis="x", which="major", pad=20)

    # Draw range labels
    ax.yaxis.set_label_position("left")
    ax.set_rlabel_position(20)
    labels = np.arange(0, yLimit, yLimit / 5)
    plt.yticks(labels, color="grey", size=0)
    plt.ylim(0, yLimit)

    # Plot the data
    for i, group in enumerate(Postures):
        values = list(Data[group])
        values += values[:1]
        if std:
            std_values = list(StdData[group])
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

    figurepath = f"Result Figure/Formative T2 MCL.png"
    figurepath += " [Radar]"
    if std:
        figurepath += " [STD]"
    if annotate:
        figurepath += " [Annotate]"
    figurepath += ".png"

    plt.savefig(figurepath, transparent=False)
    plt.close()
    print(f"Figure saved to {ColorText(figurepath, "green")}\n")


DrawRadarChart(
    "MCL Value with different postures and directions",
    results,
    standard_deviation,
    50,
    std=False,
    annotate=False,
)
