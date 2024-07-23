import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from Constant import *

print("Normality Test")
print("==================================")

data = dict()
for pos in Postures:
    data[pos] = dict()
    for dir in Directions:
        data[pos][dir] = dict()
        for ang in Angles:
            data[pos][dir][ang] = list()

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

notNormal = list()
Normal = list()

for pos in Postures:
    print(f"testing posture: {pos}")
    for dir in Directions:
        print(f"testing direction: {dir}")
        for ang in Angles:
            # D’Agostino and Pearson’s test
            _, pval = stats.normaltest(data[pos][dir][ang])
            if pval > 0.05:
                Normal.append(f"{pos}_{dir}_{ang}")
            else:
                notNormal.append(f"{pos}_{dir}_{ang}")
            # isNormal = "Normal" if hp_p > 0.05 else "Not Normal"
            # print(f"p val: {hp_p:.6f} | {isNormal}\n")

            stats.probplot(data[pos][dir][ang], dist="norm", plot=plt)
            plt.title(f"{pos} {dir} {ang}")
            plt.savefig("Result Figure/O3_NormalityTest/" + f"{pos}_{dir}_{ang}_QQ.png")
            plt.close()

print(f"\nNot Normal: {len(notNormal)}")
# for i in notNormal:
#     print(i)

print(f"\nNormal: {len(Normal)}")
# for i in Normal:
#     print(i)
