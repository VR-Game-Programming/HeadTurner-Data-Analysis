
from scipy.signal import butter, sosfilt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from copy import deepcopy


def get_result(dir_path, fig_name, create_fig=False, window_length=100):
    files = os.listdir(dir_path)
    data_file = [file for file in files if 'data' in file][-1]
    timestamp_file = [file for file in files if 'timestamp' in file][-1]
    data_filepath = os.path.join(dir_path, data_file)
    timestamp_filepath = os.path.join(dir_path, timestamp_file)
    print(data_filepath, timestamp_filepath)

    emg_data = []
    with open(data_filepath, 'r') as f:
        for line in f.readlines()[20:-10]:
            try:
                cur = line.strip().split(',')[:-1]
                cur = [float(x.strip()) for x in cur]
                assert len(cur) == 5
                emg_data.append(cur)
            except:
                pass
    emg_data = np.array(emg_data)
    timestamp = emg_data[:, 0]
    emg_data = emg_data[:, 1:]
    fig_emg_data = deepcopy(emg_data)
    emg_data = emg_data - np.mean(emg_data, axis=0)

    fig_timestamp = deepcopy(timestamp)

    bandpass_freq_low = 20
    bandpass_freq_high = 150
    lowpass_freq = 1
    butterworth_order = 4
    sampling_rate = len(emg_data) / (timestamp[-1] - timestamp[0]) * 1000
    sampling_rate

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
    EMG = []
    for i in range(4):
        squared_emg = emg_data[:, i] ** 2
        val = np.sqrt(np.convolve(squared_emg, window, mode='same'))
        EMG.append(val)
    EMG = np.array(EMG).T

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
        EMG[i, :] = sos_lowpass_filter(
            EMG[i, :], lowpass_freq, sampling_rate, butterworth_order)

    np.mean(EMG, axis=0)

    EMG = np.sum(EMG, axis=1)

    timestamp_data = pd.read_csv(timestamp_filepath)

    posture_range = list(timestamp_data.get('range'))

    if "Ecosphere" in dir_path:
        posture_range.append("Ecosphere")
    if "Archery" in dir_path:
        posture_range.append("Archery")

    posture_range = list(set(posture_range))

    result = {}
    angle_timestamp = {}
    for r in posture_range:
        if r == 'EOL':
            continue
        try:
            start = timestamp_data[timestamp_data['range']
                                   == r].iloc[0]['start']
            start_index = np.where(timestamp == start)[0][0]
        except:
            start = timestamp[0]
            start_index = np.where(timestamp == start)[0][0]
        try:
            end = timestamp_data[timestamp_data['range'] == r].iloc[-1]['end']
            end_index = np.where(timestamp == end)[0][0]
        except:
            end = timestamp[-1]
            end_index = np.where(timestamp == end)[0][0]

        emg_avg = np.sum(EMG[start_index:end_index]) / (end - start)
        result[r] = emg_avg
        angle_timestamp[r] = (start, end)

    if create_fig:

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
            ax1.plot(transform_timestamp(fig_timestamp),
                     fig_emg_data[:, i], label=f'channel {i}')
        ax1.legend()

        ax2.plot(transform_timestamp(timestamp), EMG)
        for angle, val in angle_timestamp.items():
            ax2.axvline(x=transform_timestamp(timestamp, val[0]), color='g')
            ax2.axvline(x=transform_timestamp(timestamp, val[1]), color='r')

        plt.tight_layout()

        os.makedirs('Result Figure/Emg Individual', exist_ok=True)
        fig.savefig(os.path.join('Result Figure/Emg Individual', fig_name))
        plt.close(fig)

    return result


if __name__ == '__main__':
    result = get_result(
        dir_path="Raw Data/Archery/emg_data/P_7_ActuatedBed", fig_name="Archery_P7_ActuatedBed.png", create_fig=False)
    print(result)
