# WS 0
import numpy
from matplotlib import pyplot as plt

# --- exercise: make some noise!

# sampling rate of the signal (in Hz: samples per second)
samplerate = 200

# duration of the signal (in seconds)
duration = 1
signal_length = samplerate * duration

# create a time axis (array of time points)
time = numpy.linspace(start=0, stop=duration, num=signal_length)  # start, stop, number of steps

# generate a noisy signal (array of random values)
noise = numpy.random.rand(signal_length)

# plot noise on the y-axis against time on the x-axis
plt.plot(time, noise)
plt.xlabel('Time (s)')  # label the time axis with a string

# --- exercise: making waves

# parameters of the sine wave:
amplitude = 1
frequency = 4
phi = numpy.sin(0)  # phase angle offset 0-360°

# create a wave:
wave = amplitude * numpy.sin(2 * numpy.pi * frequency * time + phi)

plt.plot(time, wave)
plt.xlabel('Time (s)')

# add our noise to the wave:
noisy_wave = wave + noise
plt.plot(time, noisy_wave)

# add some sine waves together
frequencies = [2, 4]  # different frequencies
sine_waves = []
for freq in frequencies:
    x = amplitude * numpy.sin(2 * numpy.pi * freq * time + phi)
    sine_waves.append(x)
sum = numpy.sum(sine_waves, axis=0)

# --- exercise: load eeg data

# --- exercise: select data by time interval

# --- exercise: plot data

# --- exercise: sum and average across time slices

