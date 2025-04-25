import slab
import numpy
import random
import time
import freefield
from pathlib import Path
fs = 48828
slab.set_default_samplerate(fs)
data_dir = Path.cwd() / 'experiments'
rcx_file = 'oddball.rcx'

# generate standard
f0 = 500
n_harmonics = 3
duration = 0.075
level = 75

standard = slab.Sound.tone(f0, duration, level=level)
standard += slab.Sound.tone(f0*2, duration, level=level-3)
standard += slab.Sound.tone(f0*3, duration, level=level-6)
standard.ramp(duration=.005)

# generate deviant 1 - frequency deviant
dev_f0 = 550
deviant_1 = slab.Sound.tone(dev_f0, duration, level=level)
deviant_1 += slab.Sound.tone(dev_f0*2, duration, level=level-3)
deviant_1 += slab.Sound.tone(dev_f0*3, duration, level=level-6)
deviant_1.ramp(duration=.005)

# generate deviant 2 - loudness deviant
dev_level = 85
deviant_2 = slab.Sound.tone(f0, duration, level=dev_level)
deviant_2 += slab.Sound.tone(f0*2, duration, level=dev_level-3)
deviant_2 += slab.Sound.tone(f0*3, duration, level=dev_level-6)
deviant_2.ramp(duration=.005)

# generate deviant 3 - duration deviant
dev_duration = 0.025
deviant_3 = slab.Sound.tone(f0, dev_duration, level=level)
deviant_3 += slab.Sound.tone(f0*2, dev_duration, level=level-3)
deviant_3 += slab.Sound.tone(f0*3, dev_duration, level=level-6)
deviant_3.ramp(duration=.005)
silence = slab.Sound.silence(duration=.05)
deviant_3 = slab.Sound.sequence(deviant_3, silence)

#  deviant 4 - location deviant
# handle in rcx

# (SOA) of 500 ms in three 5 min sequences
def run_experiment(
        n_trials=1845,
        soa = 0.5,
        save_csv_path=Path.cwd() / 'data' / 'mmn_trials.csv'):

    # stimulus codes (0 - 4) appear in the trial sequence and eeg triggers
    # 0: standard, 1 - 4: deviants

    # generate trial sequence
    sequence = generate_mmn_sequence(n_trials)
    print(sequence)
    trial_sequence = slab.Trialsequence(conditions=sequence)
    trial_sequence.trials = numpy.arange(n_trials).tolist()
    trial_sequence.save_csv(save_csv_path)    # Save to CSV

    # write stimulus data to buffers
    freefield.write('data_std', standard.data, ['RX81', 'RX82'])
    freefield.write('data_dev_1', deviant_1.data, ['RX81', 'RX82'])
    freefield.write('data_dev_2', deviant_2.data, ['RX81', 'RX82'])
    freefield.write('data_dev_3', deviant_3.data, ['RX81', 'RX82'])
    freefield.write('data_dev_4', standard.data, ['RX81', 'RX82'])
    freefield.write('n_samples', standard.n_samples, ['RX81', 'RX82'])
    [speaker] = freefield.pick_speakers(23)
    freefield.set_speaker(speaker)

    # Run trials
    print("\nStarting MMN experiment...\n")
    for stim_code in (trial_sequence):
        print(f"Trial {trial_sequence.this_n}, stim code: {trial_sequence.this_trial}")
        freefield.write('stim_code', stim_code, ['RX81', 'RX82'])
        if stim_code == 4:
            freefield.set_speaker(44)  # play at 52.5° azimuth

        freefield.play('zBusA')
        time.sleep(soa - standard.duration)
    print("\nExperiment complete.")

def init_dsp(rcx_file):
    proc_list = [['RX81', 'RX8', data_dir / 'rcx' / rcx_file],
                 ['RX82', 'RX8', data_dir / 'rcx' / rcx_file]]
    freefield.initialize('dome', device=proc_list, sensor_tracking=False)
    # freefield.load_equalization(data_dir / '')

def generate_deviant_groups(total_deviants, last_deviant=None):
    deviant_types = [1, 2, 3, 4]
    groups = []
    while len(groups) * 5 < total_deviants:
        group = deviant_types.copy()
        # Choose a 5th deviant that's not same as previous group's last deviant
        extra_choices = [d for d in deviant_types if d != last_deviant]
        group.append(random.choice(extra_choices))
        # Shuffle group until no adjacent duplicates with previous group's end
        for _ in range(1000):
            random.shuffle(group)
            if last_deviant is None or group[0] != last_deviant:
                if all(group[i] != group[i+1] for i in range(len(group)-1)):
                    break
        else:
            raise RuntimeError("Failed to build a valid deviant group.")
        groups.append(group)
        last_deviant = group[-1]
    # Flatten list of groups
    return [d for group in groups for d in group]

def generate_mmn_sequence(n_trials, leading_standards=15):
    if n_trials <= leading_standards or (n_trials - leading_standards) % 2 != 0:
        raise ValueError("Total length must allow alternation after leading standards.")
    sequence = [0] * leading_standards
    num_deviants = (n_trials - leading_standards) // 2
    deviant_list = generate_deviant_groups(num_deviants)
    # Interleave with standards
    for deviant in deviant_list:
        sequence.append(deviant)  # odd index
        sequence.append(0)        # even index
    return sequence[:n_trials]


# # Example usage
# if __name__ == "__main__":
#     init_dsp(rcx_file)
#     run_experiment(
#         deviant_freq=0.8,
#         n_trials=300,
#         isi=0.5,
#         save_csv_path="mmn_trials.csv")



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