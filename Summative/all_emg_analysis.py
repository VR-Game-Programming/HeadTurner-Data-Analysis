import os
from single_emg_anlysis import get_result
import csv
from Constant import Directions

TOTAL_PARTICIPANTS = 16
TASKS = ["Summative_T1", "Summative_T2", "Ecosphere", "Archery"]
BED_STATUS = ["ActuatedBed", "NormalBed"]


def gen_experiment_result_path(task, participant_number, bed_status):
    if "Summative" in task:
        return f"Raw Data/Formative_Metrics/emg_data/{task}_P{participant_number}_{bed_status}/"
    return f"Raw Data/{task}/emg_data/P_{participant_number}_{bed_status}/"


results = {}
for t in TASKS:
    results[t] = {
        "ActuatedBed": [],
        "NormalBed": []
    }

data = [[] for _ in range(TOTAL_PARTICIPANTS)]
header = ['Participant']
for participant_number in range(1, TOTAL_PARTICIPANTS+1):
    for task in TASKS:
        for bed_status in BED_STATUS:
            path = gen_experiment_result_path(
                task, participant_number, bed_status)
            fig_name = f"{task}_P{participant_number}_{bed_status}.png"
            mcl = get_result(dir_path=path, fig_name=fig_name, create_fig=True)
            if "Summative" in task:
                if participant_number == 7 and task == "Summative_T2" and bed_status == "ActuatedBed":
                    print(mcl)
                    mcl_value = mcl[180]
                    data[participant_number-1].append(mcl_value)
                for angle, mcl_value in mcl.items():
                    header.append(
                        f"{task[-2:]}_{Directions[angle//90]}_{bed_status}")
                    data[participant_number-1].append(mcl_value)
            header.append(f"{task}_{bed_status}")
            data[participant_number-1].append(sum([mcl[x] for x in mcl]))
data_length = len(data[0])
header = header[:data_length+1]

os.makedirs('Processed Data', exist_ok=True)
with open('Processed Data/Processed MCL Value.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    # Write the data
    for participant_data in data:
        row = [f"P{data.index(participant_data)+1}"]
        row.extend(participant_data)
        writer.writerow(row)

print("Data has been written to Result Processed/MCL Value.csv")
