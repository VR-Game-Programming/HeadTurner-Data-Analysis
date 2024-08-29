import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import csv
from math import pi
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
        col_name = "Task2 - " + p + " - " + d
        scores = df[col_name].to_list()
        data[p].append(stat.fmean(scores))
        std_data[p].append(stat.stdev(scores))

# with open("Result Processed/" + "T2_Result.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Posture", "Direction", "Mean", "Std"])
#     for p in Postures:
#         for idx, d in enumerate(Directions):
#             writer.writerow([p, d, data[p][idx], std_data[p][idx]])

# Draw Figure
# =================================================================
x = np.arange(len(Directions))
width = 0.35
fig, ax = plt.subplots(figsize=(15, 10))

# Draw
fig, ax = plt.subplots(figsize=(15, 10))
ax.bar(
    x + width / 2,
    data["Standing"],
    width,
    color=Colors[0][4],
    label="Standing",
    yerr=std_data["Standing"],
    capsize=3,
)
ax.bar(
    x - width / 2,
    data["Lying"],
    width,
    color=Colors[1][4],
    label="Lying",
    yerr=std_data["Lying"],
    capsize=3,
)

# plt.ylim(1, 7)

# Add Text
ax.set_xlabel("Directions")
ax.set_ylabel("Effort Scores")
ax.set_title("Effort scores with different postures and directions")
ax.set_xticks(x)
ax.set_xticklabels(Directions)
ax.legend()

plt.savefig(f"{RootDir}/Result Figure/Formative T2 EffortScores.png", transparent=False)
plt.close()


# Draw Figure (v2)
# =================================================================
# Set plot
# plt.figure(figsize=(10, 10))
# ax = plt.subplot(111, polar=True)

# N = len(Directions)
# angles = [n / float(N) * 2 * pi for n in range(N)]
# angles += angles[:1]

# # Draw direction axes
# ax.set_xlabel("Direction", labelpad=15, color="black", size=16)
# ax.xaxis.set_label_position("bottom")
# plt.xticks(angles[:-1], Directions, color="black", size=10)
# ax.tick_params(axis="x", which="major", pad=20)

# # Draw range labels
# ax.set_ylabel("Effort Score", labelpad=40, color="grey", size=16)
# ax.yaxis.set_label_position("left")
# ax.set_rlabel_position(20)
# # ax.get_yaxis().set_visible(False)
# plt.yticks([1, 2, 3, 4, 5, 6, 7], color="grey", size=10)
# plt.ylim(1, 7)

# # Plot the data
# i = 0
# colors = ["tab:blue", "tab:red"]
# ecolors = ["black", "grey"]
# ecapsize = [6, 4]
# for pos in Postures:
#     values = data[pos]
#     values += values[:1]
#     std_values = std_data[pos]
#     std_values += std_values[:1]
#     ax.errorbar(
#         angles,
#         values,
#         color=colors[i],
#         linewidth=2,
#         linestyle="solid",
#         label=pos,
#         yerr=std_values,
#         ecolor=ecolors[i],
#         capsize=ecapsize[i],
#     )
#     ax.fill(angles, values, "k", alpha=0.05)
#     i += 1

# plt.legend(loc="best", bbox_to_anchor=(0, 0))
# plt.savefig("Result Figure/" + "T2_EffortScores_v2.png", transparent=False)
# plt.close()
