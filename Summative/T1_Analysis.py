import pandas as pd
import statistics as stat
import csv
from scipy.stats import ttest_rel, wilcoxon
import statsmodels.formula.api as smf
from Constant import *

ProcessedDir = "Result Processed/"


def CalculateAngle(direction, angle):
    if direction == "Right" or direction == "UpRight" or direction == "DownRight":
        return abs(angle) if angle > 0 else 360 + angle

    elif direction == "Left" or direction == "UpLeft" or direction == "DownLeft":
        return abs(angle) if angle < 0 else 360 - angle

    else:
        return abs(angle) if abs(angle) < 180 else 360 - abs(angle)


# Data Prepare
# =================================================================
# Initialize the result dict
range_data = dict()
for p in Postures:
    range_data[p] = dict()
    for d in Directions:
        range_data[p][d] = list()

# Read raw result
df = pd.DataFrame(columns=["Participant", "Posture", "Direction", "Range"])
for p in Postures:
    for i in Participants:
        filepath = (
            "Result Raw (ReCalculate)/T1/" + f"Formative_T1_P{i}_{p}_ReCalculate.csv"
        )
        with open(filepath, newline="") as csvfile:
            r = csv.DictReader(csvfile)
            for row in r:
                d = row["Direction"]
                angle = CalculateAngle(d, float(row["MaxViewingRange"]))

                df = df._append(
                    {
                        "Participant": i,
                        "Posture": p,
                        "Direction": d,
                        "Range": angle,
                    },
                    ignore_index=True,
                )

df.to_csv(ProcessedDir + "T1_RawData.csv", index=False)

# Calculate each participant's mean
df_mean = pd.DataFrame(columns=["Participant", "Posture", "Direction", "Range"])
range_data = dict()

for p in Postures:
    range_data[p] = dict()
    for d in Directions:
        range_data[p][d] = list()
        for i in Participants:
            ranges = list(
                df.loc[df["Posture"] == p]
                .loc[df["Direction"] == d]
                .loc[df["Participant"] == i]["Range"]
            )
            for value in ranges:
                if value < 10:
                    ranges.remove(value)
            mean_angle = stat.fmean(ranges)

            range_data[p][d].append(mean_angle)
            df_mean = df_mean._append(
                {
                    "Participant": i,
                    "Posture": p,
                    "Direction": d,
                    "Range": mean_angle,
                },
                ignore_index=True,
            )

df_mean.to_csv(ProcessedDir + "T1_RawData_Mean.csv", index=False)

# Data Analysis
# =================================================================
# Paired t-Test & Wilcoxon
with open(ProcessedDir + "T1_pValue_Result.txt", "w") as text_file:
    for d in Directions:
        print(f"For Direction {d}", file=text_file)
        print(
            "=================================================================",
            file=text_file,
        )
        print("Standing:", file=text_file)
        print(range_data["Standing"][d], file=text_file)
        print("Lying:", file=text_file)
        print(range_data["Lying"][d], file=text_file)
        print(
            ttest_rel(range_data["Standing"][d], range_data["Lying"][d]), file=text_file
        )
        print(
            wilcoxon(range_data["Standing"][d], range_data["Lying"][d]), file=text_file
        )
        print("\n", file=text_file)

# Model
with open(ProcessedDir + "T1_Model_Summary.txt", "w") as text_file:
    base_posture = "Standing"
    base_direction = "Up"

    df_mean["Posture"] = df_mean["Posture"].astype("category")
    df_mean["Direction"] = df_mean["Direction"].astype("category")
    df_mean["Range"] = df_mean["Range"].apply(pd.to_numeric, errors="coerce")

    df_mean["Posture"] = df_mean["Posture"].cat.reorder_categories(
        [base_posture]
        + [cat for cat in df_mean["Posture"].cat.categories if cat != base_posture],
        ordered=True,
    )
    df_mean["Direction"] = df_mean["Direction"].cat.reorder_categories(
        [base_direction]
        + [cat for cat in df_mean["Direction"].cat.categories if cat != base_direction],
        ordered=True,
    )

    model = smf.mixedlm(
        "Range ~ Posture + Direction", df_mean, groups=df_mean["Participant"]
    )
    result = model.fit()

    print(f"Base: {base_posture}, {base_direction}\n", file=text_file)
    print(result.summary(), file=text_file)
