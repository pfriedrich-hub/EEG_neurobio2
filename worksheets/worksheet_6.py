# Epochs and Evokeds
import mne
from pathlib import Path
import json
import os
import matplotlib.pyplot as plt

header_file = Path.cwd() / 'resources' / 'EEG_data' / 'P1_Ears Free_0.vhdr'
raw = mne.io.read_raw_brainvision(header_file, preload=True)

# Load events and the event_id dictionary with the unique event values
events, event_id = mne.events_from_annotations(raw)

# Visualise all events and their types
mne.viz.plot_events(events, sfreq=raw.info["sfreq"], first_samp=raw.first_samp, event_id=event_id)

# Create epochs based on the events list and define the time points of interest before and after the event
t_min = ...
t_max = ...
epochs = mne.Epochs(raw, events, tmin=t_min, tmax=t_max)

# Print the epochs object and notice the names of the event_ids
print(epochs)
print(epochs.event_id)

# Redefine your event_id dictionary to name events for easier referencing later on
event_dict = {
    "elevation_5": 1,
    "voice_1": 2,
    "...": 3,
    "buttonpress": 4
}
epochs = mne.Epochs(raw, events, tmin=t_min, tmax=t_max, event_id=event_dict)
print(epochs.event_id)

# Now it's easy to subselect epochs using square brackets
print(epochs["elevation_5"])
print(epochs[["voice_1", "buttonpress"]])

# Create another epochs object but this time reject epochs based on peak-to-peak channel amplitude
reject_criteria = ...
flat_criteria = ...
epochs = mne.Epochs(raw, events, tmin=t_min, tmax=t_max, event_id=event_dict, reject=reject_criteria, flat=flat_criteria)
# Plot the estimation of how many epochs were rejected based on the parameters (search for "drop log")
epochs.plot...

# Plot the first 10 epochs with the notation
epochs.plot(n_epochs=..., events=True)

# Baseline correction: select the time points in which you want to correct for baseline
# and apply it to the epochs object
epochs.apply_....

# Save the epochs as a new file
# Epochs objects can be saved in the .fif format
# The MNE-Python naming convention for epochs files is that the file basename
# (the part before the .fif or .fif.gz extension) should end with -epo or _epo,
# and a warning will be issued if the filename you provide does not adhere to that convention.
epochs.save("...-epo.fif", overwrite=True)

# Search for a python package that has an automated approach to bad channel detection and interpolation
# Try to use it!

# Evoked objects are the averages of all epochs relating to the same experimental condition (event_id)
conditions = list(event_dict.keys())
evokeds = [epochs[condition].average() for condition in conditions]

# Plot the evoked of each of the conditions
evokeds[0].plot()
evokeds[1].plot()
...

# Plot the evoked of each of the conditions with a topomap view of the most prominent peaks
# Explore other plotting options on the evoked data to see which ones represent your results the best
evokeds[0].plot_joint()
evokeds[1].plot_joint()
...

# Plot the evoked objects to be able to compare conditions
# Plot the global field power (GFP), as well as pick one channel for best representation of your experiment
# What's the difference between the plots?
mne.viz.plot_compare_evokeds(evokeds)

# Get peak amplitude and the time points of the peaks for each condition

# Save the evokeds object as a .fif file
mne.write_evokeds("...-ave.fif", evokeds)
