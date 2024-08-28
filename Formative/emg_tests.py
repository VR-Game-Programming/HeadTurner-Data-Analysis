from scipy.stats import ttest_rel, wilcoxon
import json
import pandas as pd
from Constant import Directions_num

data = pd.read_csv('Result Processed/MCL Value.csv')
data = data.set_index(['Participant', 'Posture']).T.to_dict()

lying_values = []
standing_values = []
for posture in ['Lying', 'Standing']:
    for angle in Directions_num:
        values = [data[(i, posture)][angle] for i in range(1, 17)]
        if posture == 'Lying':
            lying_values.append(values)
        else:
            standing_values.append(values)

ttest_results = []
wilcoxon_results = []

for i in range(8):
    ttest_result = ttest_rel(lying_values[i], standing_values[i])
    wilcoxon_result = wilcoxon(lying_values[i], standing_values[i])
    ttest_results.append(ttest_result)
    wilcoxon_results.append(wilcoxon_result)

# print("T-Test Results:")
# for i, result in enumerate(ttest_results):
#     print(f"Angle {i*45}: p-value = {result.pvalue:.4f}")

print("\nWilcoxon Results:")
for i, result in enumerate(wilcoxon_results):
    print(f"Angle {i*45}: p-value = {result.pvalue:.4f}")
