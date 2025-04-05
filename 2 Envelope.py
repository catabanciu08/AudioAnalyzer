import sys
sys.path.append("C:/Users/Catalin/AppData/Local/Programs/Python/Python313/Lib/site-packages")
import librosa
# print(librosa.__version__)

import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import hilbert, convolve
from scipy.signal.windows import gaussian

import csv

# Load the audio file
audio_path = "GigiBecali.mp3"
audio, sr = librosa.load(audio_path, sr=None)

# Compute the absolute value of the waveform
audio_abs = np.abs(audio)

# Apply the Hilbert transform to get the analytic signal
analytic_signal = hilbert(audio)
envelope = np.abs(analytic_signal)

# Apply a Gaussian filter to smooth the envelope
window_size = 440000  # Larger window for smoother envelope
sigma = 88000  # Standard deviation for Gaussian filter
gaussian_window = gaussian(window_size, std=sigma)
smoothed_envelope = 5 * convolve(envelope, gaussian_window/gaussian_window.sum(), mode='same')

# Time array for the signal
t = np.linspace(0, len(audio) / sr, len(audio))

"""
# Plot the original signal and its smoother envelope
plt.figure(figsize=(10, 6))
plt.plot(t, audio_abs, label="Original Absolute Signal", color="lightgray")
plt.plot(t, smoothed_envelope, label="Smoothed Envelope (Gaussian Filter)", color="red", linewidth=2)

mean_amplitude = np.mean(np.abs(smoothed_envelope))
double_mean_amplitude = 2 * mean_amplitude

plt.axhline(y=mean_amplitude, color='red', linestyle='--', label="Mean Amplitude")
plt.axhline(y=double_mean_amplitude, color='green', linestyle='--', label="Double Mean Amplitude")
plt.title("Signal and Smoothed Envelope (Gaussian Filter)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend(loc = "upper right")
plt.show()
"""

# Compute the mean of the smoothed envelope
mean_envelope = np.mean(smoothed_envelope)

# Define the threshold (twice the mean)
threshold = 2 * mean_envelope

# Find indices where the absolute signal exceeds twice the mean of the envelope
above_threshold = smoothed_envelope > threshold

# Find the intervals where the signal is above the threshold
intervals = []
start = None
for i in range(1, len(above_threshold)):
    if above_threshold[i] and not above_threshold[i-1]:
        start = i  # Start of a new interval
    elif not above_threshold[i] and above_threshold[i-1]:
        end = i  # End of the interval
        intervals.append((start, end))  # Store the interval

print(intervals)

# Express the intervals in min:sec format
min_sec_intervals = []

if intervals:
    for start, end in intervals:
        start_total_seconds = start // sr
        start_min = str(start_total_seconds // 60)
        start_sec = str(start_total_seconds % 60)

        end_total_seconds = end // sr
        end_min = str(end_total_seconds // 60)
        end_sec = str(end_total_seconds % 60)

        interval_string = start_min + ":" + start_sec + "-" + end_min + ":" + end_sec

        min_sec_intervals.append(interval_string)

print(min_sec_intervals)

# Export the sections in CSV format
if min_sec_intervals:
    with open('time_ranges2.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Time Range"])

        # Write each time range as a separate row
        for time_range in min_sec_intervals:
            writer.writerow([time_range])

    print("Data has been saved to 'time_ranges2.csv'")
else:
    print("No loudness intervals were identified in this audio")
