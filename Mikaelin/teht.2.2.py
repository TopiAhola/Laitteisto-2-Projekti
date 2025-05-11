from filefifo import Filefifo

# Initialize Filefifo to read data from the file
data = Filefifo(10, name='capture_250Hz_01.txt')

# Read 2 seconds of data (500 samples) to find min and max values
samples = []
for _ in range(500):
    samples.append(data.get())

# Find the min and max values from the first 500 samples
min_value = min(samples)
max_value = max(samples)

print(f"Minimum value: {min_value}")
print(f"Maximum value: {max_value}")

# Scale the first 500 samples to the range 0 - 100
scaled_samples = [(sample - min_value) / (max_value - min_value) * 100 for sample in samples]


# Read 10 seconds of data (2500 samples) and scale it
samples_10s = []
for _ in range(100):
    samples_10s.append(data.get())

scaled_samples_10s = [(sample - min_value) / (max_value - min_value) * 100 for sample in samples_10s]

# Output the scaled 10 seconds of data for Thonny's Plotter
print("\nScaled values (10 seconds of data):")
for sample in scaled_samples_10s:
    print(sample)


