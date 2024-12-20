from config import *
from utils import *

import pprint
import csv
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = f"{ROOT_DIR}/output/freeplay-headrot-cdf"
logger = LOGGER(f"{OUTPUT_DIR}/log.txt")

# d[application][condition] = headrot value list
d = {}

for application in APPLICATIONS:
    for condition in CONDITIONS:
        d.setdefault(application, {})[condition] = []
        for participant in PARTICIPANTS:

            input_file = f"{ROOT_DIR}/raw data/s_converted/{application}/P_{participant}_{condition}_converted.csv"
            try:
                with open(input_file, newline="") as f:
                    reader = csv.DictReader(f)

                    for row in reader:
                        headrot = row["TurnedAngle"]
                        d[application][condition].append(float(headrot))

            except FileNotFoundError:
                logger.PRINT_LOG(
                    "FILE NOT FOUND", bcolors.FAIL, f"{input_file} not found"
                )


# plot CDF
PLOT_CDF = True
if PLOT_CDF:
    bins = np.arange(0, 175 + 1, 1)

    for application in APPLICATIONS:
        plt.figure(figsize=(12, 6))

        value_50 = {}
        value_90 = {}
        for condition in CONDITIONS:
            x = np.sort(d[application][condition])
            hist, bin_edges = np.histogram(x, bins=bins, density=True)

            cdf = np.cumsum(hist * np.diff(bin_edges))

            value_50.setdefault(condition, np.interp(0.5, cdf, bin_edges[:-1]))
            value_90.setdefault(condition, np.interp(0.9, cdf, bin_edges[:-1]))

            plt.plot(
                bin_edges[:-1],
                cdf * 100,
                linestyle="-",
                color=COLORS[condition][DARKEST],
                label=condition,
            )

        plt.xlabel("Head Rotation Angle (°)")
        plt.ylabel("Cumulative Proportion (%)")
        plt.title(
            f"Cumulative Distribution Function of Head Rotation Angles ({application})"
        )
        plt.xticks(np.arange(0, 175 + 25, 25))
        plt.yticks(np.arange(0, 100 + 10, 10))
        plt.legend()
        plt.grid(True)

        # calculate the gap between two CDFs at 50% and 90%

        gap_50 = np.abs(value_50[CONDITIONS[0]] - value_50[CONDITIONS[1]])
        gap_90 = np.abs(value_90[CONDITIONS[0]] - value_90[CONDITIONS[1]])

        logger.PRINT_LOG(
            "INFO",
            bcolors.OKGREEN,
            f"{application}: gap at 50% = {gap_50:.5f}, gap at 90% = {gap_90:.5f}",
        )

        output_file = f"{OUTPUT_DIR}/{application}_headrot_cdf.png"
        plt.savefig(output_file)
        plt.close()

        logger.PRINT_LOG("SAVE PLOT", bcolors.OKBLUE, f"saved {output_file}")

# plot PDF
PLOT_PDF = False
if PLOT_PDF:
    bins = np.arange(0, 90 + 5, 5)

    for application in APPLICATIONS:
        plt.figure(figsize=(12, 6))

        for condition in CONDITIONS:
            x = np.sort(d[application][condition])
            hist, bin_edges = np.histogram(x, bins=bins, density=True)

            plt.plot(
                bin_edges[:-1],
                hist * 100,
                linestyle="-",
                color=COLORS[condition][DARKEST],
                label=condition,
            )

        plt.xlabel("Head Rotation Angle (°)")
        plt.ylabel("Proportion (%)")
        plt.title(
            f"Probability Density Function of Head Rotation Angles ({application})"
        )
        plt.xticks(np.arange(0, 90 + 5, 5))
        plt.yticks(np.arange(0, 10 + 1, 1))
        plt.legend()

        output_file = f"{OUTPUT_DIR}/{application}_headrot_pdf_(anglex).png"
        plt.savefig(output_file)
        plt.close()

        logger.PRINT_LOG("SAVE PLOT", bcolors.OKBLUE, f"saved {output_file}")

# ks test
KS_TEST = False
if KS_TEST:
    from scipy.stats import ks_2samp

    for application in APPLICATIONS:
        x1 = d[application][CONDITIONS[0]]
        x2 = d[application][CONDITIONS[1]]

        ks_stat, ks_pval = ks_2samp(x1, x2)
        logger.PRINT_LOG(
            "INFO",
            bcolors.OKCYAN,
            f"{application}: ks_stat={ks_stat:.5f}, ks_pval={ks_pval:.5f}",
        )
