import numpy
import mne
from pathlib import Path
from matplotlib import pyplot as plt

header_file_path = Path.cwd() / 'resources' / 'EEG_data' / 'blinks.vhdr'
raw = mne.io.read_raw_brainvision(header_file_path, preload=True)

data = raw.copy().pick_channels(['9'])._data[0][:500]  # single channel eeg data
n_samples = len(data)  # length of sequence
times = numpy.arange(0, n_samples) / n_samples  # time points in the data

# take a look at the EEG (time series) data:
fig, ax = plt.subplots(1, 1)
ax.plot(times, data)
ax.set_ylabel('Amplitude (mV)')
ax.set_xlabel('Time (s)')
ax.set_title('Raw signal')


# ---- Step I: Fourier transformation ---- #

samplefrequency = raw.info["sfreq"]         # sampling rate in Hz
nyquist = samplefrequency / 2    # Nyquist frequency -- the highest frequency you can measure in the data
# initialize Fourier output array
fourier = numpy.zeros(n_samples, dtype=complex)
# These are the actual frequencies in Hz that will be returned by the
# Fourier transform. The number of unique frequencies we can measure is
# exactly 1/2 of the number of data points in the time series (plus DC).
frequencies = numpy.linspace(0, nyquist, int(n_samples/2)+1)
# Fourier transform is dot-product between sine wave and data at each frequency
for frequency in range(n_samples):
    sine_wave = numpy.exp(-1j * (2 * numpy.pi * frequency * times))  # complex sine wave
    fourier[frequency] = numpy.sum(sine_wave * data)  # dot productd
fourier = fourier / n_samples  # rescale by signal length

# to obtain the spectrum, disregard the complex part and convert to log power:
# (we keep the fourier transform ('fourier'-variable) to reconstruct the time series data after filtering)
spectrum = numpy.abs(fourier)[:int(n_samples / 2) + 1] ** 2

#  plot the spectrum
fig, ax = plt.subplots(1, 1)
ax.plot(frequencies, spectrum)
ax.set_ylabel('Power (dB)')
ax.set_xlabel('Frequency (Hz)')

# extra: plot a complex sine wave
frequency = 3  # frequency of the sine wave in Hz
fig = plt.figure()
ax = plt.axes(projection='3d')
sine_wave = numpy.exp(-1j * (2 * numpy.pi * frequency * times))  # complex sine wave
ax.plot(times, sine_wave.real, sine_wave.imag)
ax.set_title('%i Hz sine wave' % frequency)



# ---- Step II Construct a band pass filter ----- #

# get variables (these are the same variables as above)
nyquist = samplefrequency / 2  # Nyquist frequency -- the highest frequency you can measure in the data
frequencies = numpy.linspace(0, nyquist, int(n_samples / 2) + 1)

# create an array of zeros with the same length as the frequency array
# filter = numpy.zeros(len(frequencies))  # side note: this filter would just zero out all frequency components!
filter = numpy.zeros(n_samples)  # side note: this filter would just zero out all frequency components!

# select frequencies in the pass-band (the frequency components we want to keep)
low_frequency = ...
high_frequency = ...
passband_indices = numpy.where(numpy.logical_and(frequencies > low_frequency, frequencies < high_frequency))

# Create the filter kernel in the frequency domain: set value at the frequencies that we want to keep to 1, all others remain zero
filter[passband_indices] = 1
# plot the resulting filter
fig, ax = plt.subplots(1, 1)
ax.plot(frequencies, filter[:int(n_samples / 2) + 1])
ax.set_ylabel('Power (dB)')
ax.set_xlabel('Frequency (Hz)')

# Apply the filter to the spectrum (simply multiply the filter with the spectrum) and plot the resulting spectrum
filtered_fourier = fourier * filter

# to obtain the filtered version of the spectrum, disregard the complex part and convert to log power:
filtered_spectrum = numpy.abs(filtered_fourier)[:int(n_samples / 2) + 1] ** 2
fig, ax = plt.subplots(1, 1)
ax.plot(frequencies, filtered_spectrum)
ax.set_ylabel('Power (dB)')
ax.set_xlabel('Frequency (Hz)')
# compare the filtered spectrum to the original spectrum from above


# ---- Step III: Inverse Fourier transformation ---- #

# after we applied the filter to the spectrum of the signal
# we compute the inverse fourier transformation to recover the time series data
reconstructed_data = numpy.zeros(len(data))
for frequency in range(n_samples):
    #  scale sine waves by fourier coefficients
    sine_wave = filtered_fourier[frequency] * numpy.exp(1j * 2 * numpy.pi * (frequency) * times)
    # sine_wave = numpy.exp(-1j * (2 * numpy.pi * frequency * time))  # complex sine wave
    # sum sine waves together (take only real part)
    reconstructed_data = reconstructed_data + numpy.real(sine_wave)

# plot filtered time series
fig, ax = plt.subplots(1, 1)
ax.plot(times, reconstructed_data)
ax.set_ylabel('Amplitude (mV)')
ax.set_xlabel('Time (s)')
ax.set_title('Filtered signal')

raw_filtered = raw.copy().filter(lp=..., hp=...)