# Import MNE python library
import mne

# Define the file path of the header file
header_file_path = "..."

# Read in the raw Brainvision file using the "io" class
raw = ...

# Print the raw object. How many channels are there? How many seconds is the recording?

# Print the list of all individual time points

# Print the "info" object of the raw variable. What is the sampling frequency?

# Print the list of all channel names

# Create a copy of the raw object and store it in a new variable

# Rename the channels on the copy of the raw object (use the electrode map image)

# Plot the raw file

# Select bad channels

# Print the names of the selected bad channels

# Pick all the channels that you would associate with blinking
# or pick all "frontal" channels using a regular expression (regexp)

# Select the time frames of the first five blinks and store these in new variables

# Plot the signals of the first five blinks

# Take the average of the "blinks" and plot it. How is it different from the individual blink plots?

# Extra: Repeat the above steps with the eye movement EEG data

# Repeat the "Noise generation" task from Worksheet 1 using python
