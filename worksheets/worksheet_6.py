# Epochs and Evokeds
import mne
from pathlib import Path
import json
import os
import matplotlib.pyplot as plt

header_file = Path.cwd() / 'resources' / 'EEG_data' / 'blinks.vhdr'
raw = mne.io.read_raw_brainvision(header_file, preload=True)

# Load events
events = mne.events_from_annotations(raw)[0]

# Create epochs based on the events list and define the time points of interest before and after the event
epochs = mne.Epochs(raw, events, tmin=..., tmax=...)

# Create another epochs object but this time reject epochs based on peak-to-peak channel amplitude
epochs_rejected = mne.Epochs(raw, events, tmin=..., tmax=..., reject=..., flat=...)

# Plot the estimation of how many epochs were rejected based on the parameters (search for "drop log")

# Plot joint

# Save the epochs as a new file

# Search for a python package that has an automated approach to bad channel detection and interpolation
# Try to use it!
