import sys
sys.path.append("C:/Users/Catalin/AppData/Local/Programs/Python/Python313/Lib/site-packages")
import librosa
# print(librosa.__version__)

import librosa.display
import matplotlib.pyplot as plt
import numpy as np

import csv

# Load audio file
file_path = "GigiBecali.mp3"
audio, sr = librosa.load(file_path, sr=None)

# plt.figure(figsize=(14, 5))
# librosa.display.waveshow(audio, sr=sr)
# plt.title("Audio Waveform")
# plt.xlabel("Time (seconds)")
# plt.ylabel("Amplitude")
# plt.show()

# Compute global average amplitude
global_avg_amplitude = np.mean(np.abs(audio))

# Define interval (in seconds)
interval_duration = 10 # seconds
samples_per_interval = sr * interval_duration  # Number of samples per interval
num_intervals = len(audio) // samples_per_interval # Number of intervals

loud_intervals = []

# Define the threshold for loudness (1.5 - 2 recommended)
amplitude_coefficient = 1.6

# Determine the loudness intervals
for i in range(num_intervals):
    start_sample = i * samples_per_interval
    end_sample = (i + 1) * samples_per_interval
    interval_avg_amplitude = np.mean(np.abs(audio[start_sample:end_sample]))

    if interval_avg_amplitude >= amplitude_coefficient * global_avg_amplitude:
        loud_intervals.append(i)  # Store index of loud intervals
if loud_intervals:
    print(loud_intervals)
else:
    print("No loud intervals are present in this audio")

# Determine the sections corresponding to the loud intervals
loud_sections = []

j = 0
while j < num_intervals:
    if j in loud_intervals:
        loudness_interval_beginning = j * interval_duration
        beginning_min = str(loudness_interval_beginning // 60)
        beginning_sec = str(loudness_interval_beginning % 60)
        while j in loud_intervals:
            j += 1
        loudness_interval_ending = j * interval_duration
        ending_min = str(loudness_interval_ending // 60)
        ending_sec = str(loudness_interval_ending % 60)
        section = beginning_min + ":" + beginning_sec + "-" + ending_min + ":" + ending_sec
        loud_sections.append(section)
    else:
        j += 1

# Export the sections in CSV format
if loud_sections:
    with open('time_ranges.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Time Range"])

        # Write each time range as a separate row
        for time_range in loud_sections:
            writer.writerow([time_range])

    print("Data has been saved to 'time_ranges.csv'")
else:
    print("No loud sections were identified in this audio")





