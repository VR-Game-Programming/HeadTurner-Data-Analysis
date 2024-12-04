
from scipy.signal import butter, sosfilt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def read_emg_data(file_path) -> dict:
    emg_data = []
    with open(file_path, 'r') as f:
        error_lines = []
        for i, line in enumerate(f.readlines()):
            try:
                cur = line.strip().split(',')[:-1]
                cur = [float(x.strip()) for x in cur]
                assert len(cur) == 5
                emg_data.append(cur)
            except:
                error_lines.append(i)
        print(f"Error lines: {error_lines}")

    good_index = 0
    for i in range(len(emg_data)-1):
        if emg_data[i][0] > emg_data[i+1][0]:
            good_index = i+1
        if emg_data[i][0] == 0:
            good_index = i
    emg_data = np.array(emg_data[good_index:])
    timestamp = emg_data[:, 0]
    emg_data = emg_data[:, 1:]
    emg_data = emg_data - np.mean(emg_data, axis=0)
    return {
        "emg_data": emg_data,
        "timestamp": timestamp
    }
    
def read_timestamp_data(timestamp_filepath, timestamp) -> dict:
    timestamp_data = pd.read_csv(timestamp_filepath)

    posture_range = list(timestamp_data.get('range'))
    posture_range = list(set(posture_range))

    angle_timestamp = {}
    for r in posture_range:
        try:
            start = timestamp_data[timestamp_data['range'] == r].iloc[0]['start']
        except:
            start = timestamp[0]
        try:
            end = timestamp_data[timestamp_data['range'] == r].iloc[-1]['end']
        except:
            end = timestamp[-1]

        angle_timestamp[r] = (start, end)
        
    return angle_timestamp

def read_T1_T2_data(task, user_number) -> dict:
    """
    returns dictionary:
    {
        "ActuatedBed": {
            "emg_data": List of unprocessed EMG data,
            "timestamp_data": List of timestamps,
        },
        "NormalBed": {
            "emg_data": List of unprocessed EMG data,
            "timestamp_data": List of timestamps,
        },
    }
    """
    actuated_dir_path = f"raw data/emg_data/Summative_T{task}_P{user_number}_ActuatedBed/"
    normal_dir_path = f"raw data/emg_data/Summative_T{task}_P{user_number}_NormalBed/"
    
    result = {}
    
    for i, dir_path in enumerate([actuated_dir_path, normal_dir_path]):
        files = os.listdir(dir_path)
        data_file = [file for file in files if 'data' in file][-1]
        timestamp_file = [file for file in files if 'timestamp' in file][-1]
        data_filepath = os.path.join(dir_path, data_file)
        timestamp_filepath = os.path.join(dir_path, timestamp_file)
        print(data_filepath, timestamp_filepath)
        
        cur_result = read_emg_data(data_filepath)
        timestamp_data = read_timestamp_data(timestamp_filepath, cur_result["timestamp"])
        cur_result["timestamp_data"] = timestamp_data
        if i == 0:
            result["ActuatedBed"] = cur_result
        else:
            result["NormalBed"] = cur_result
    return result

def read_timestamp_angle_data(timestamp_filepath, timestamp) -> dict:
    timestamp_data = pd.read_csv(timestamp_filepath)
    filtered_data = timestamp_data[timestamp_data['time'].isin(timestamp)]
    angles = filtered_data['turnedAngle'].values
    return angles
    
def read_freeplay_data(task: str, user_number) -> dict:
    assert (task == "FPS" or task == "Ecosphere")
    actuated_dir_path = f"raw data/{task}/emg_data/P_{user_number}_ActuatedBed/"
    normal_dir_path = f"raw data/{task}/emg_data/P_{user_number}_NormalBed/"
    
    result = {}
    
    for i, dir_path in enumerate([actuated_dir_path, normal_dir_path]):
        files = os.listdir(dir_path)
        data_file = [file for file in files if 'data' in file][-1]
        timestamp_file = [file for file in files if 'timestamp' in file][-1]
        data_filepath = os.path.join(dir_path, data_file)
        timestamp_filepath = os.path.join(dir_path, timestamp_file)
        print(data_filepath, timestamp_filepath)
        
        cur_result = read_emg_data(data_filepath)
        timestamp_angle_data = read_timestamp_angle_data(timestamp_filepath, cur_result["timestamp"])
        cur_result["timestamp_angle_data"] = timestamp_angle_data
        if i == 0:
            result["ActuatedBed"] = cur_result
        else:
            result["NormalBed"] = cur_result
    return result

def process_emg_data(emg_data, timestamp, window_length=100) -> np.array:
    bandpass_freq_low = 20
    bandpass_freq_high = 150
    lowpass_freq = 1
    butterworth_order = 4
    sampling_rate = len(emg_data) / (timestamp[-1] - timestamp[0]) * 1000
    print(f"sampling_rate: {sampling_rate}, timestamp: {timestamp[0]} ~ {timestamp[-1]}")

    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], btype='band', output='sos')
        return sos

    def butter_bandpass_filter(data, lowcut, highcut, sample_rate, order=5):
        sos = butter_bandpass(lowcut, highcut, sample_rate, order=order)
        y = sosfilt(sos, data)
        return y

    low = (2*bandpass_freq_low)/sampling_rate
    high = (2*bandpass_freq_high)/sampling_rate
    for i in range(4):
        emg_data[i, :] = butter_bandpass_filter(
            emg_data[i, :], low, high, sampling_rate, butterworth_order)

    window = np.ones(window_length) / window_length
    # Line 19: Compute the RMS envelope using convolution
    processed_emg = []
    for i in range(4):
        squared_emg = emg_data[:, i] ** 2
        val = np.sqrt(np.convolve(squared_emg, window, mode='same'))
        processed_emg.append(val)
    processed_emg = np.array(processed_emg).T

    def butter_lowpass_sos(cutoff, fs, order=5):
        nyquist = 0.5 * fs  # Nyquist Frequency
        normal_cutoff = cutoff / nyquist
        sos = butter(order, normal_cutoff, btype='low',
                     analog=False, output='sos')
        return sos

    def sos_lowpass_filter(data, cutoff, fs, order=5):
        sos = butter_lowpass_sos(cutoff, fs, order=order)
        y = sosfilt(sos, data)
        return y

    for i in range(4):
        processed_emg[i, :] = sos_lowpass_filter(
            processed_emg[i, :], lowpass_freq, sampling_rate, butterworth_order)

    processed_emg = np.sum(processed_emg, axis=1)
    return processed_emg

def draw_T1T2_figure(timestamp, emg_data, mcl_data, fig_name, timestamp_data=None):
    def transform_timestamp(timestamp_data, single_timestamp=None):
        start = timestamp_data[0]
        if single_timestamp is not None:
            return (single_timestamp - start)/1000
        return [(x - start)/1000 for x in timestamp_data]

    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(121)
    ax1.set_title('EMG Data')
    ax2 = fig.add_subplot(122)
    ax2.set_title('MCL Data')
    for i in range(4):
        ax1.plot(transform_timestamp(timestamp),
                 emg_data[:, i], label=f'channel {i}')
    ax1.legend()

    ax2.plot(transform_timestamp(timestamp), mcl_data)
    
    if timestamp_data is not None:
        for angle, val in timestamp_data.items():
            ax2.axvline(x=transform_timestamp(timestamp, val[0]), color='g')
            ax2.axvline(x=transform_timestamp(timestamp, val[1]), color='r')

    plt.tight_layout()

    os.makedirs('Result Figure/Emg Individual', exist_ok=True)
    fig.savefig(os.path.join('Result Figure/Emg Individual', fig_name))
    plt.close(fig)

def get_T1T2_single_user_MCL_result(task, user_number, create_fig=False, window_length=100):
    data = read_T1_T2_data(task, user_number)
    data["ActuatedBed"]["processed_emg"] = process_emg_data(
        data["ActuatedBed"]["emg_data"], data["ActuatedBed"]["timestamp"], window_length)
    data["NormalBed"]["processed_emg"] = process_emg_data(
        data["NormalBed"]["emg_data"], data["NormalBed"]["timestamp"], window_length)
    all_processed_emg = np.concatenate(
        [data["ActuatedBed"]["processed_emg"], data["NormalBed"]["processed_emg"]])
    average_mcl_value = np.mean(all_processed_emg)
    data["average_mcl_value"] = average_mcl_value
    data["ActuatedBed"]["mcl"] = data["ActuatedBed"]["processed_emg"] / average_mcl_value
    data["NormalBed"]["mcl"] = data["NormalBed"]["processed_emg"] / average_mcl_value

    if create_fig:
        draw_T1T2_figure(
            timestamp = data["ActuatedBed"]["timestamp"], 
            emg_data = data["ActuatedBed"]["emg_data"],
            mcl_data = data["ActuatedBed"]["mcl"], 
            timestamp_data = data["ActuatedBed"]["timestamp_data"], 
            fig_name = f"T{task}_P{user_number}_ActuatedBed.png",
        )
        draw_T1T2_figure(
            timestamp = data["NormalBed"]["timestamp"], 
            emg_data = data["NormalBed"]["emg_data"],
            mcl_data = data["NormalBed"]["mcl"], 
            timestamp_data = data["NormalBed"]["timestamp_data"], 
            fig_name = f"T{task}_P{user_number}_NormalBed.png",
        )
        
    result = {
        "ActuatedBed": {},
        "NormalBed": {},
    }
        
    for r in data["ActuatedBed"]["timestamp_data"]:
        start, end = data["ActuatedBed"]["timestamp_data"][r]
        start_idx = np.where(data["ActuatedBed"]["timestamp"] == start)[0][0]
        end_idx = np.where(data["ActuatedBed"]["timestamp"] == end)[0][0]
        result["ActuatedBed"][r] = np.mean(data["ActuatedBed"]["mcl"][start_idx:end_idx])
        
    for r in data["NormalBed"]["timestamp_data"]:
        start, end = data["NormalBed"]["timestamp_data"][r]
        start_idx = np.where(data["NormalBed"]["timestamp"] == start)[0][0]
        end_idx = np.where(data["NormalBed"]["timestamp"] == end)[0][0]
        result["NormalBed"][r] = np.mean(data["NormalBed"]["mcl"][start_idx:end_idx])
        
    return result

def get_freeplay_single_user_MCL_result(task, user_number, create_fig=False, window_length=100):
    data = read_freeplay_data(task, user_number)
    data["ActuatedBed"]["processed_emg"] = process_emg_data(
        data["ActuatedBed"]["emg_data"], data["ActuatedBed"]["timestamp"], window_length)
    print(data["ActuatedBed"]["processed_emg"].shape)
    data["NormalBed"]["processed_emg"] = process_emg_data(
        data["NormalBed"]["emg_data"], data["NormalBed"]["timestamp"], window_length)
    print(data["NormalBed"]["processed_emg"].shape)
    all_processed_emg = np.concatenate(
        [data["ActuatedBed"]["processed_emg"], data["NormalBed"]["processed_emg"]])
    average_mcl_value = np.mean(all_processed_emg)
    data["average_mcl_value"] = average_mcl_value
    data["ActuatedBed"]["mcl"] = data["ActuatedBed"]["processed_emg"] / average_mcl_value
    data["NormalBed"]["mcl"] = data["NormalBed"]["processed_emg"] / average_mcl_value

    if create_fig:
        draw_T1T2_figure(
            timestamp = data["ActuatedBed"]["timestamp"], 
            emg_data = data["ActuatedBed"]["emg_data"],
            mcl_data = data["ActuatedBed"]["mcl"], 
            fig_name = f"{task}_P{user_number}_ActuatedBed.png",
        )
        draw_T1T2_figure(
            timestamp = data["NormalBed"]["timestamp"], 
            emg_data = data["NormalBed"]["emg_data"],
            mcl_data = data["NormalBed"]["mcl"], 
            fig_name = f"{task}_P{user_number}_NormalBed.png",
        )
        
    def process_freeplay_data(freeplay_data):
        mcls = freeplay_data["mcl"]
        angles = freeplay_data["timestamp_angle_data"]
        print(len(mcls), len(angles))
        print(angles)
        bar_data = [[] for _ in range(36)]
        for mcl, angle in zip(mcls, angles):
            angle_interval = int(abs(angle) // 5)
            bar_data[angle_interval].append(mcl)
        print([len(x) for x in bar_data])
        bar_data = [np.mean(x) for x in bar_data if x != []]
        return bar_data
    
    result = {
        "ActuatedBed": process_freeplay_data(data["ActuatedBed"]),
        "NormalBed": process_freeplay_data(data["NormalBed"]),
    }
    
    return result

if __name__ == '__main__':
    # result = get_T1T2_single_user_MCL_result(task=2, user_number=2, create_fig=True, window_length=50)
    # print(result)
    
    result = get_freeplay_single_user_MCL_result(task="Ecosphere", user_number=9, create_fig=True, window_length=50)
    print("ActuatedBed MCL:",len(result["ActuatedBed"])," | NormalBed MCL", len(result["NormalBed"]))
    print(result)
