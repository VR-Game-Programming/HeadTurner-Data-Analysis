import json
import numpy as np
import matplotlib.pyplot as plt
from emg_single import get_result
from Constant import Colors, Directions, Postures
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


# Draw Plot
# 設置長條的X軸位置
x = np.arange(len(Directions))
width = 0.35  # 長條的寬度

# 繪製長條圖
fig, ax = plt.subplots(figsize=(15, 10))
bars1 = ax.bar(
    x - width / 2,
    average[Postures[0]],
    width,
    label=Postures[0],
    yerr=standard_deviation[Postures[0]],
    capsize=3,
    color=Colors["Standing"][1],
)
bars2 = ax.bar(
    x + width / 2,
    average[Postures[1]],
    width,
    label=Postures[1],
    yerr=standard_deviation[Postures[1]],
    capsize=3,
    color=Colors["Lying"][1],
)

# 添加一些文本標籤
ax.set_xlabel("Directions")
ax.set_ylabel("MCL Value")
ax.set_title("MCL Value with different postures and directions")
ax.set_xticks(x)
ax.set_xticklabels(Directions)
ax.legend()

plt.savefig("Result Figure/" + "T2_MCL.png", transparent=False)
plt.show()
