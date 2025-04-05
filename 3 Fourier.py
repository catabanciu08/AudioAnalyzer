import sys
sys.path.append("C:/Users/Catalin/AppData/Local/Programs/Python/Python313/Lib/site-packages")
import librosa
# print(librosa.__version__)

import matplotlib.pyplot as plt
import numpy as np

import csv

# Load the audio file
audio_path = "GigiBecali.mp3"  # Replace with your actual file
audio, sr = librosa.load(audio_path, sr=None)  # Use the correct sampling rate

# Apply Short-Time Fourier Transform (STFT) to get the Fourier Transform
D = librosa.stft(audio)

# Convert the complex-valued result into magnitude
magnitude, phase = librosa.magphase(D)

# Plot the magnitude of the Fourier Transform
# plt.figure(figsize=(10, 6))
# librosa.display.specshow(librosa.amplitude_to_db(magnitude, ref=np.max), y_axis='log', x_axis='time', sr=sr)
# plt.colorbar(format='%+2.0f dB')
# plt.title('Magnitude Spectrogram (STFT)')
# plt.xlabel('Time (s)')
# plt.ylabel('Frequency (Hz)')
# plt.show()

# Get the frequency values corresponding to each row in the STFT
frequencies = librosa.fft_frequencies(sr=sr)

# Find the index corresponding to 8192 Hz
freq_index = np.abs(frequencies - 8192).argmin()

# Extract the magnitude at 8192 Hz for each time frame (i.e., for each column)
magnitude_8192 = magnitude[freq_index, :]

# Create the time array corresponding to each frame
time = librosa.times_like(magnitude_8192, sr=sr)

# Plot the evolution of the magnitude at 8192 Hz
# plt.figure(figsize=(10, 6))
# plt.plot(time, magnitude_8192, label="Magnitude at 8192 Hz", color="blue")
# plt.title("Magnitude Evolution at 8192 Hz")
# plt.xlabel("Time (seconds)")
# plt.ylabel("Magnitude")
# plt.legend()
# plt.show()

# Apply a moving average filter to smooth the magnitude curve
window_size = 1000  # Adjust the window size for the moving average
moving_avg = 5 * np.convolve(magnitude_8192, np.ones(window_size)/window_size, mode='same')

# Plot the original and smoothed magnitude curves
# plt.figure(figsize=(10, 6))
# plt.plot(time, magnitude_8192, label="Magnitude at 8192 Hz (Original)", color="blue", alpha=0.6)
# plt.plot(time, moving_avg, label="Smoothed Magnitude (Moving Average)", color="red", linewidth=2)
# plt.title("Magnitude Evolution at 8192 Hz with Moving Average")
# plt.xlabel("Time (seconds)")
# plt.ylabel("Magnitude")
# plt.legend(loc="upper right")
# plt.show()

# Compute the mean of moving average filter of the curve at f = 8192 Hz
mean_avg_filter = np.mean(moving_avg)

# Define the threshold (three times the mean)
threshold = 3 * mean_avg_filter

# Find indices where the absolute signal exceeds three times the mean of the envelope
above_threshold = moving_avg > threshold

# Find the intervals where the signal is above the threshold
intervals = []
start = None
for i in range(1, len(above_threshold)):
    if above_threshold[i] and not above_threshold[i-1]:
        start = i  # Start of a new interval
    elif not above_threshold[i] and above_threshold[i-1]:
        end = i  # End of the interval
        intervals.append((start, end))  # Store the interval

# Convert the sample indices to seconds based on the STFT's hop length (default 512)
intervals_in_seconds = [
    ((start * 512) // sr, (end * 512) // sr) for start, end in intervals
]

print (intervals_in_seconds)

# Express the intervals in min:sec format
min_sec_intervals = []

for start_sec, end_sec in intervals_in_seconds:
    start_min = str(start_sec // 60)
    start_sec = str(start_sec % 60)

    end_min = str(end_sec // 60)
    end_sec = str(end_sec % 60)

    interval_string = start_min + ":" + start_sec + "-" + end_min + ":" + end_sec

    min_sec_intervals.append(interval_string)

print(min_sec_intervals)

# Export the sections in CSV format
if min_sec_intervals:
    with open('time_ranges3.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Time Range"])

        # Write each time range as a separate row
        for time_range in min_sec_intervals:
             writer.writerow([time_range])

    print("Data has been saved to 'time_ranges3.csv'")
else:
    print("No loudness intervals were identified in this audio")




