import numpy
import math
import mne
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib import colors

# --- Exercise 1: creating a wavelet --- #

# to make a morlet wavelet, create a gaussian and a sine wave and multiply them point by point
# base parameters
samplerate = 500   # sampling rate in Hz
time = numpy.arange(-1, 1, 1 / samplerate)  # time, from -1 to 1 second in steps of 1/sampling-rate

# step 1: create a sine wave
# frequency of the sine wave and of gaussian in Hz = center/peak frequency of resulting wavelet
frequency = 10
# complex sine wave
sine_wave = numpy.exp(2 * numpy.pi * 1j * frequency * time)
# plot the sine wave
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, sine_wave)
ax[0].set_title('Sine wave (signal)')
ax[0].set_ylim(-1.1, 1.1)

# step 2: make a Gaussian
# number of cycles - trade-off between temporal and frequency resolution:
# more cycles will result in higher frequency resolution, but poorer time resolution
n_cycles = 6
# standard deviation of gaussian - this will define how "wide" our wavelet is (= frequency resolution)
sigma = n_cycles / (2 * numpy.pi * frequency)
# amplitude of gaussian
amplitude = 1
gaussian_window = amplitude * numpy.exp(-time ** 2 / (2 * sigma ** 2))
# plot gaussian
ax[1].plot(time, gaussian_window)
ax[1].set_title('Gaussian window')

# step 3: ...and together they make a wavelet!
wavelet = ...
# plot wavelet
ax[2].plot(time, wavelet)
ax[2].set_title('resulting wavelet')


# the morlet wavelet we have just created is actually complex
# plot, including the imaginary part:
fig, ax = plt.subplots(1, 1)
ax = plt.axes(projection='3d')
ax.plot(time, wavelet.real, wavelet.imag)
ax.set_title('%i Hz complex morlet wavelet' % frequency)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('real amplitude')
ax.set_zlabel('imag amplitude')



# --- Exercise 2: convolve EEG signal with a complex morlet wavelet --- #

# load sample data  # todo this could be epochs around an auditory stimulus
header_file = Path.cwd() / 'resources' / 'EEG_data' / 'P1_Ears Free_0.vhdr'
raw = mne.io.read_raw_brainvision(header_file, preload=True)
data = raw.pick_channels(['9'])._data[0][50000:51000]   # single channel eeg data
n_samples = len(data)  # length of the data (time-sequence)
eeg_time = numpy.arange(0, n_samples) / n_samples  # time points in the data

# take a look at the EEG (time series) data:
fig, ax = plt.subplots(1, 1)
ax.plot(eeg_time, data)
ax.set_ylabel('Amplitude (mV)')
ax.set_xlabel('Time (s)')
ax.set_title('Raw signal')


# step 1: define frequency range of the time-frequency-analysis (= wavelet frequencies)
min_freq = 3  # minimum frequency
max_freq = 60  # maximum frequency
n_frequencies = 20  # number of wavelets (frequency resolution)


# step 2: define wavelet parameters
# time points of the wavelet
wavelet_time = numpy.arange(-1, 1, 1 / samplerate)
# frequencies at which we will create the different wavelets (= frequency resolution)
frequencies = numpy.logspace(numpy.log10(min_freq), numpy.log10(max_freq), n_frequencies)
# number of cycles of morlet wavelet (defined by sigma: width of the gaussian bell curve)
# note that we change the number as a function of wavelet frequency (more cycles with increasing wavelet frequency)
sigmas = numpy.logspace(numpy.log10(3), numpy.log10(10), n_frequencies) / (2 * numpy.pi * frequencies)


# convolution parameters
# length of the (zero-padded) wavelet in datapoints
n_wavelet = len(wavelet_time)
# length of the data in datapoints
n_data = len(data)
# length of the convolution result (twice as long due to the imaginary part)
n_convolution = n_wavelet + n_data - 1
# todo
n_conv_pow2 = 2 ** (math.ceil(math.log(n_convolution, 2)))
half_of_wavelet_size = int((n_wavelet - 1) / 2)

# get FFT of data
eeg_fft = numpy.fft.fft(data, n_conv_pow2)
# initialize
eeg_power = numpy.zeros((n_frequencies, n_data))  # frequencies X time
base_idx = [0, 500]  # eeg data used for baseline normalization
# loop through frequencies and compute synchronization
for frequency_index in range(n_frequencies):
    # create morlet wavelets at the different frequencies
    wavelet = (numpy.sqrt(1 / (sigma[frequency_index] * numpy.sqrt(numpy.pi)))
               # complex sine at different frequencies
               * numpy.exp(2 * 1j * numpy.pi * frequencies[frequency_index] * time)
               # gaussian with increasing sigma (=more cycles with increasing wavelet frequency)
               * numpy.exp(-time ** 2 / (2 * (sigmas[frequency_index] ** 2))))

    # apply fourier transformation (move to frequency representation)
    # reminder: multiplication in the frequency domain == convolution in the time domain!
    wavelet_fft = numpy.fft.fft(wavelet, n_conv_pow2)

    # convolve the eeg signal with the wavelet to retrieve time frequency information
    eeg_conv = numpy.fft.ifft(wavelet_fft * eeg_fft)  # convolve and apply inverse fourier transformation
    eeg_conv = eeg_conv[:n_convolution]  # cut result to length of n_convolution
    eeg_conv = eeg_conv[half_of_wavelet_size + 1: n_convolution - half_of_wavelet_size]

    # convert amplitude to power
    temp_power = (numpy.abs(eeg_conv) ** 2)

    # baseline normalization
    eeg_power[frequency_index] = 10 * numpy.log10(temp_power / numpy.mean(temp_power[base_idx[0]:base_idx[1]]))


# plot resulting time frequency representation of the EEG data
x, y = numpy.meshgrid(eeg_time, frequencies)
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
c_ax = ax.contour(x, y, eeg_power, linewidths=0.3, colors="k", norm=colors.Normalize())
c_ax = ax.contourf(x, y, eeg_power, norm=colors.Normalize(), cmap=plt.cm.jet)
cbar = fig.colorbar(c_ax)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Frequency (Hz)')
cbar.set_label('Power (dB)')
plt.show()










# create wavelet
frequency = 6  # in Hz, as usual
time = numpy.arange(-1, 1, 1/samplerate)  # time vector
n_cycles = 4  # number of cycles of gaussian window - remember
sigma = (n_cycles / (2 * numpy.pi * frequency))  
wavelet = numpy.exp(2 * 1j * numpy.pi * frequency * time) * numpy.exp(-time ** 2 / (2 * sigma ** 2) / frequency)

# Fourier parameters
n_wavelet = len(wavelet)
n_data = len(data)
n_convolution = n_wavelet + n_data
half_of_wavelet_size = math.ceil((n_wavelet) / 2)
# FFT of wavelet and EEG data
fft_wavelet = numpy.fft.fft(wavelet, n_convolution)
fft_data = numpy.fft.fft(data, n_convolution)

# convolve and get inverse of fft
convolution_result_fft = numpy.fft.ifft(fft_wavelet * fft_data, n_convolution) * numpy.sqrt(sigma) # scale by root of cycles
# cut off edges
convolution_result_fft = convolution_result_fft[half_of_wavelet_size:n_convolution-half_of_wavelet_size]
# plot for comparison
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, convolution_result_fft.real)
ax[0].set_title('Projection onto real axis is filtered signal at %i Hz.'%frequency)
ax[0].set_xlabel('Time (ms)')
ax[0].set_ylabel('Voltage (\muV)')
ax[1].plot(time, numpy.abs(convolution_result_fft) ** 2)
ax[1].set_title('Magnitude of projection vector squared is power at %i Hz.'%frequency)
ax[1].set_xlabel('Time (ms)')
ax[1].set_ylabel('Voltage (\muV)')
ax[2].plot(time, numpy.angle(convolution_result_fft))
ax[2].set_title('Angle of vector is phase angle time series at %i Hz.'%frequency)
ax[2].set_xlabel('Time (ms)')
ax[2].set_ylabel('Phase angle (rad.)')




