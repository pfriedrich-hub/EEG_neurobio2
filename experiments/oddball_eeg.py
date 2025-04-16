import pandas as pd
import slab
import numpy
import random
import time
import freefield
from pathlib import Path
data_dir = Path.cwd() / 'experiments'
rcx_file = 'oddball.rcx'

# generate standard and deviant stimuli
standard = slab.Binaural.tone(frequency=500, level=60)
deviant_1 = slab.Binaural.tone(frequency=500, level=80)
deviant_2 = slab.Binaural.tone(frequency=800, level=60)
deviant_3 = slab.Binaural.tone(frequency=500, level=60).at_azimuth(45)

# some ideas:
# timbre: create a sound that has the same f0 and amplitude/mean power across frequencies, but different:
# 1 Range between tonal and noiselike character
# 2 Spectral envelope
# 3 Time envelope in terms of rise, duration, and decay (ADSR, which stands for "attack, decay, sustain, release")
# 4 Changes both of spectral envelope (formant-glide) and fundamental frequency (micro-intonation)
# 5 Prefix, or onset of a sound, quite dissimilar to the ensuing lasting vibration

# location (shift itd and ild independently? - ask kirke)

# tradeoff between HRTF and Timbre:
# happens on the spectral envelope level: timbre -> ratio of power across harmonics, hrtf -> ratio of power across bands
# change timbre by playing through known and unknown HRTF?
# behavioral difference? behavioral ratings? unknown HRTF should differ (use jnd timbre differences)
# ask participants to localize first and then rate timbre or reverse or simultaneously
# test spatial instruments for timbre changes

def run_experiment(
        deviant_freq=0.2,
        n_trials=300,
        isi=0.5,
        save_csv_path="mmn_trials.csv"):
    """
    :param deviant_freq: frequency of deviant stimuli
    :param n_trials: number of trials
    :param isi: inter stimulus interval
    :param save_csv_path: path to save trial sequence
    """
    # stimulus codes (0-3) appear in the trial sequence and eeg triggers
    # 0: standard, 1-3: deviants

    # generate Trialsequence # we need ca. 500 trials to get each of the 3 deviants 30 times
    trial_sequence = slab.Trialsequence(conditions = 1, n_reps = n_trials, deviant_freq = deviant_freq)
    trial_sequence.trials = replace_zeros_with_deviants(trial_sequence.trials, deviant_codes=[1,2,3])
    # Save to CSV
    trial_sequence.save(save_csv_path)
    print(f"Trial sequence saved to {save_csv_path}")

    # write stimulus data to buffer
    freefield.write('data_std', standard.data, ['RX81', 'RX82'])
    freefield.write('data_dev_1', deviant_1.data, ['RX81', 'RX82'])
    freefield.write('data_dev_2', deviant_2.data, ['RX81', 'RX82'])
    freefield.write('data_dev_3', deviant_3.data, ['RX81', 'RX82'])
    # for now all stimuli have the same duration
    freefield.write('n_samples', standard.n_samples, ['RX81', 'RX82'])
    # set channel, for now we use fixed locations
    [speaker] = freefield.pick_speakers(23)
    freefield.set_speaker(speaker)

    # Run trials
    print("\nStarting MMN experiment...\n")
    for stim_code in (trial_sequence):
        print(f"Trial {trial_sequence.this_n}, stim code: {trial_sequence.this_trial}")
        freefield.write('stim_code', stim_code, ['RX81', 'RX82'])
        freefield.play('zBusA')
        time.sleep(isi)
    print("\nExperiment complete.")

def replace_zeros_with_deviants(sequence, deviant_codes):
    # Find how many zeros (deviants) there are
    n_deviants = sequence.count(0)
    n_deviant_types = len(deviant_codes)
    n_per_type = n_deviants // n_deviant_types
    # Create evenly distributed list of deviant codes
    deviants = []
    for code in deviant_codes:
        deviants.extend([code] * n_per_type)
    # If there's a remainder, randomly assign extra deviants
    remainder = n_deviants - len(deviants)
    deviants.extend(random.choices(deviant_codes, k=remainder))
    # Shuffle the deviant codes
    random.shuffle(deviants)
    # Replace zeros in the sequence
    new_sequence = []
    deviant_index = 0
    for item in sequence:
        if item == 0:
            new_sequence.append(deviants[deviant_index])
            deviant_index += 1
        else:
            new_sequence.append(item)
    return new_sequence

def init_dsp(rcx_file):
    proc_list = [['RX81', 'RX8', data_dir / 'rcx' / rcx_file],
                 ['RX82', 'RX8', data_dir / 'rcx' / rcx_file]]
    freefield.initialize('dome', device=proc_list, sensor_tracking=True)
    freefield.load_equalization(data_dir / '')

# Example usage
if __name__ == "__main__":
    init_dsp(rcx_file)
    run_experiment(
        deviant_freq=0.2,
        n_trials=300,
        isi=0.5,
        save_csv_path="mmn_trials.csv")
