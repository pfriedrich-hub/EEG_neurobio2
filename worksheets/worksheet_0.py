# WS 0
import numpy
from matplotlib import pyplot as plt

# --- exercise 1: make some noise! --- #

# sampling rate of the signal (in Hz: samples per second)
samplerate = 500

# duration of the signal (in seconds)
duration = 1
signal_length = duration * samplerate

# create a time axis (array of time points)
time = numpy.linspace(start=0, stop=duration, num=signal_length)  # start, stop, number of steps

# generate a noisy signal (array of random values)
noise = numpy.random.rand(signal_length)

# plot noise on the y-axis against time on the x-axis
plt.plot(time, noise)
plt.xlabel('Time (s)')  # label the time axis with a string


# --- exercise 2: de-noising by averaging many signals --- #

# create multiple noisy signals:
n = _  # choose how many signals you want to generate (try different values and compare the outcome)

signals_list = list()  # create an empty list to store some signals
for i in range(n):  # generate n signals and add them to the list
    noise = numpy.random.rand(signal_length)  # create different random noise signals
    signals_list.append(noise)  # add each signal to the signals_list

# generate a figure to plot the noise signals
plt.figure(figsize=(15, 4))
plt.xlabel('Time (s)')

# plot the first 10 noise signals from the matrix for comparison
for i in range(n):
    plt.plot(time, signals_list[i], color='grey')

# average across noise signals
mean_signal = numpy.mean(signals_list, axis=0)
# plot the averaged noise to compare it to the original noise
plt.plot(time, mean_signal, color='black')


# --- exercise 3: making waves

# parameters of the sine wave:
amplitude = 1
frequency = 4
phi = numpy.sin(0)  # phase angle (0°-360°)

# create a wave:
wave = amplitude * numpy.sin(2 * numpy.pi * frequency * time + phi)

plt.plot(time, wave)
plt.xlabel('Time (s)')

# add our noise to the wave:
noisy_wave = wave + noise
plt.plot(time, noisy_wave)

# add some sine waves together
frequencies = [2, 4]  # list of different frequencies
sine_waves = []
for freq in frequencies:
    x = amplitude * numpy.sin(2 * numpy.pi * freq * time + phi)
    sine_waves.append(x)
sum = numpy.sum(sine_waves, axis=0)

# plot spectrum here?

# create a difference wave

# --- exercise: load raw eeg data
import mne
raw = mne.io.read_raw_brainvision('file path')

# --- exercise: select data by time interval

# --- exercise: plot data

# --- exercise: sum and average across time slices

