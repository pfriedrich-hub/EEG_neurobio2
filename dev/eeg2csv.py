# convert brainvision data to a csv file

import mne
import json
import pandas
from pathlib import Path
header_file = Path.cwd() / 'resources' / 'EEG_data' / 'P1_Ears Free_0.vhdr'
electrode_names = json.load(open(Path.cwd() / 'resources' / 'misc' / "electrode_names.json"))

# write data to csv
raw = mne.io.read_raw_brainvision(header_file, preload=True)
# raw = raw.filter(l_freq=.5, h_freq=None)  # remove strong drifts to make the data easier to inspect for a start
start, window_size = 50000, 500  # only use a slice of the raw data

eeg_data = pandas.DataFrame(data=raw._data[:, start:start+window_size])

eeg_data = pandas.DataFrame(data=raw._data[:, start:start+window_size],    # values, convert to µV
            index=electrode_names.keys())    # channel names index
            # columns=raw.times[:window_size])  # timepoints as the column names

eeg_data.to_csv(Path.cwd() / 'resources' / 'EEG_data.csv')

eeg_data = pandas.read_csv(Path.cwd() / 'resources' / 'EEG_data.csv')