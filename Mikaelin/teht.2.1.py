from filefifo import Filefifo

#filefifo to read data from a file
data = Filefifo(10, name='capture_250Hz_01.txt', repeat=False)

# variables to store peaks and their indices
peaks = []
previous_sample = None
previous_slope = None

# list to store all samples (for debugging)
samples = []

# read data and find peaks
for i in range(1000):  # read samples
    current_sample = data.get()
    samples.append(current_sample)  # store sample for debugging
    #print(samples)

    if previous_sample is not None:  # ensure we have a valid previous sample
        slope = current_sample - previous_sample  # calculate slope

        # detect a peak (when slope changes from positive to negative)
        if slope < 0 and previous_sample > current_sample:
            if len(peaks) == 0 or (i - peaks[-1] > 1):  # avoid duplicate peaks
                peaks.append(i - 1)  # store peak index
                
        if slope > 0 and previous_sample < current_sample:
            if len(peaks) == 0 or (i + peaks[-1] > 1):
                peaks.append(i - 1)
                
                
                
    previous_sample = current_sample  # update previous sample for next iteration

else:
    for peak in peaks:
        print(f"Sample {peak} with value {samples[peak]}")

# calculate peak-to-peak intervals
peak_intervals = []
for j in range(1, len(samples)):
    interval_samples = samples[j] - samples[j - 1]
    interval_seconds = interval_samples / 250  # convert to seconds (250 Hz sample rate)
    peak_intervals.append((interval_samples, interval_seconds))

# debug print first few data points to check signal shape
#print("First 50 samples:", samples[:50])
print(peaks)

# print the results
if len(peak_intervals) > 0:
    print("\nPeak-to-Peak Intervals:")
    for interval in peak_intervals[:1]:  # prints the number of ppi
        print(f"{interval[0]} peaks, {interval[1]:.3f} seconds")
        
    # calculate the estimated frequency
    avg_interval = sum(interval[0] for interval in peak_intervals) / len(peak_intervals)
    frequency = 250 / avg_interval  # Frequency in Hz
    print(f"\nEstimated Frequency: {frequency:.2f} Hz")
else:
    print("No peaks detected.")