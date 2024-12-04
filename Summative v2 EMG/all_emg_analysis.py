import os
from single_emg_anlysis import get_T1T2_single_user_MCL_result, get_freeplay_single_user_MCL_result
import csv
from Constant import Directions

TOTAL_PARTICIPANTS = 16
ANGLES = [0, 90, 180, 270]


results = {}

# data = []
# header = ['Participant', "Task", "BedStatus", "0", "90", "180", "270"]
# for participant_number in range(1, TOTAL_PARTICIPANTS+1):
#     if participant_number == 4:
#         continue
#     for task in [1,2]:
#         mcl_result = get_T1T2_single_user_MCL_result(user_number=participant_number, task=task, create_fig=True, window_length=50)
#         for bed_status in ["ActuatedBed", "NormalBed"]:
#             row = [participant_number, task, bed_status]
#             for angle in ANGLES:
#                 try:
#                     row.append(mcl_result[bed_status][angle])
#                 except:
#                     row.append(-1)
#             data.append(row)


# os.makedirs('Processed Data', exist_ok=True)
# with open('Processed Data/Processed T1T2 MCL Value.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(header)
#     for row in data:
#         writer.writerow(row)
# print("Data written")


data = []
header = ['Participant', "Task", "BedStatus"] + [str(degree) for degree in range(0, 360, 5)]
for participant_number in range(1, TOTAL_PARTICIPANTS+1):
    # if participant_number <= 10:
    #     continue
    for task in ["FPS", "Ecosphere"]:
        mcl_result = get_freeplay_single_user_MCL_result(user_number=participant_number, task=task, create_fig=True, window_length=50)
        for bed_status in ["ActuatedBed", "NormalBed"]:
            row = [participant_number, task, bed_status]
            row += list(mcl_result[bed_status])
            data.append(row)
            
os.makedirs('Processed Data', exist_ok=True)
with open('Processed Data/Processed Freeplay MCL Value.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for row in data:
        writer.writerow(row)
print("Data written")