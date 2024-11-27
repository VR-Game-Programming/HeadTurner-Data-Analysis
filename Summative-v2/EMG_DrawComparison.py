import pandas as pd
import matplotlib.pyplot as plt
from Constant import Colors

# Read the CSV file
df = pd.read_csv('Processed Data/Processed Freeplay MCL Value.csv')

def plot_data(draw_std=False):    

    for task in ['FPS', 'Ecosphere']:
    # Filter the data for the specific task
        task_data = df[df['Task'] == task]

        # Group by BedStatus and calculate the mean for each degree interval
        actuated_bed_data = task_data[task_data['BedStatus'] == 'ActuatedBed'].iloc[:, 3:]
        normal_bed_data = task_data[task_data['BedStatus'] == 'NormalBed'].iloc[:, 3:]
        
        actuated_bed_mean = actuated_bed_data.mean()
        normal_bed_mean = normal_bed_data.mean()
        
        actuated_bed_std = actuated_bed_data.std()
        normal_bed_std = normal_bed_data.std()

        # Extract the degree intervals from the header
        degree_intervals = df.columns[3:].astype(int)

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(degree_intervals, actuated_bed_mean, label='ActuatedBed', marker='o', color=Colors[0][3])
        plt.plot(degree_intervals, normal_bed_mean, label='NormalBed', marker='o', color=Colors[1][3])
        
        
        if draw_std:
            plt.fill_between(degree_intervals, actuated_bed_mean - actuated_bed_std, actuated_bed_mean + actuated_bed_std, color=Colors[0][3], alpha=0.2)
            plt.fill_between(degree_intervals, normal_bed_mean - normal_bed_std, normal_bed_mean + normal_bed_std, color=Colors[1][3], alpha=0.2)
        
            
        plt.xlabel('Degree Interval')
        plt.ylabel('Mean MCL Value')
        plt.title(f'Mean MCL Value for {task} Task')
        plt.legend()
        plt.grid(True)
        if draw_std:
            plt.savefig(f'Result Figure/Summative_{task}_MCL [STD].png')
        else: 
            plt.savefig(f'Result Figure/Summative_{task}_MCL.png')

plot_data(draw_std=False)
plot_data(draw_std=True)

for task in ['FPS', 'Ecosphere']:
    # Filter the data for the specific task
    task_data = df[df['Task'] == task]

    # Group by BedStatus and calculate the mean and standard deviation for each degree interval
    actuated_bed_data = task_data[task_data['BedStatus'] == 'ActuatedBed'].iloc[:, 3:]
    normal_bed_data = task_data[task_data['BedStatus'] == 'NormalBed'].iloc[:, 3:]

    # Count the number of non-NaN values in each column
    actuated_bed_nan_count = 16 - actuated_bed_data.isna().sum()
    normal_bed_nan_count = 16 - normal_bed_data.isna().sum()

    # Extract the degree intervals from the header
    degree_intervals = df.columns[3:].astype(int)
    
    actuated_bed_nan_count = actuated_bed_nan_count[:35]
    normal_bed_nan_count = normal_bed_nan_count[:35]
    degree_intervals = degree_intervals[:35]

    # Plot the non-NaN counts
    plt.figure(figsize=(10, 6))
    plt.plot(degree_intervals, actuated_bed_nan_count, label='ActuatedBed', marker='o', color=Colors[0][3])
    plt.plot(degree_intervals, normal_bed_nan_count, label='NormalBed', marker='o', color=Colors[1][3])
    plt.xlabel('Degree Interval')
    plt.ylabel('Non-NaN Count')
    plt.title(f'Non-NaN Count for {task} Task')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'Result Figure/Summative_{task}_counts.png')