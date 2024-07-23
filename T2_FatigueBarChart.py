import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from Constant import *

# Get Dataframe From Google Sheet
# Please replace the service_account_file with your own credentials
# (on local, do not upload to github)
gc = pygsheets.authorize(
    service_account_file="Credentials/headturner-423306-b0e4058416e1.json"
)
sheet_url = "https://docs.google.com/spreadsheets/d/1boxkhwEWOwFU7Pwfa7lKDw4uZosvswwdWjrWo2g6nN0/"
sh = gc.open_by_url(sheet_url)
wks = sh.sheet1
df = wks.get_as_df()

# Remove Pilot Test Data
df = df.drop(index=0)

# Standardize Scores for Participants
# for i in Participants:
#   scores = list()
#   for p in Postures:
#     for d in Directions:
#       col_name = p + " - " + d
#       scores.append(df[col_name][i])

#   mean = fmean(scores)
#   std_dev = stat.stdev(scores)
#   print(f"Particiapant {i}, mean={mean}, std_dev={std_dev}")
#   n = len(scores)
#   for p in Postures:
#     for d in Directions:
#       col_name = p + " - " + d
#       new_score = (df[col_name][i] - mean) / (std_dev / np.sqrt(n))
#       df.at[i, col_name] = new_score

# Initialize Data
data = dict()
std_data = dict()
for p in Postures:
    data[p] = list()
    std_data[p] = list()
    for d in Directions_num:
        col_name = p + " - " + d
        scores = df[col_name].to_list()
        data[p].append(stat.fmean(scores))
        std_data[p].append(stat.stdev(scores))

with open("Result Processed/" + "T2_Result.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Posture", "Direction", "Mean", "Std"])
    for p in Postures:
        for idx, d in enumerate(Directions):
            writer.writerow([p, d, data[p][idx], std_data[p][idx]])

# Draw Plot
# 設置長條的X軸位置
x = np.arange(len(Directions))
width = 0.35  # 長條的寬度

# 繪製長條圖
fig, ax = plt.subplots()
bars1 = ax.bar(
    x - width / 2,
    data[Postures[0]],
    width,
    alpha=0.5,
    label=Postures[0],
    yerr=std_data[Postures[0]],
    capsize=3,
)
bars2 = ax.bar(
    x + width / 2,
    data[Postures[1]],
    width,
    alpha=0.5,
    label=Postures[1],
    yerr=std_data[Postures[1]],
    capsize=3,
)

# 添加一些文本標籤
ax.set_xlabel("Directions")
ax.set_ylabel("Fatigue Scores")
ax.set_title("Fatigue scores with different postures and directions")
ax.set_xticks(x)
ax.set_xticklabels(Directions)
ax.legend()

plt.savefig("Result Figure/" + "T2_FatigueScores.png", transparent=False)
plt.show()
