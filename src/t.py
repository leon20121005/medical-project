from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plot

FILE_PATH = "../data/sample01/001.txt"

# 找出所有轉折點
def find_peaks(data):
    peaks = []
    previous_slope = None

    for index in range(1, len(data)):
        difference = data[index][1] - data[index - 1][1]
        if difference == 0:
            continue
        if difference > 0:
            if previous_slope is "negative":
                peaks.append(data[index - 1])
            previous_slope = "positive"
            continue
        if difference < 0:
            if previous_slope is "positive":
                peaks.append(data[index - 1])
            previous_slope = "negative"
            continue
    return peaks

# 找出最大的cluster的label(波峰的label)
def find_largest_cluster_label(cluster_centers):
    largest_cluster, largest_center = (0, 0)

    for index in range(len(cluster_centers)):
        if cluster_centers[index][1] > largest_center:
            largest_cluster = index
            largest_center = cluster_centers[index][1]
    return largest_cluster

# 找出切割波的轉折點的index
def find_slicing_peak_indexes(cluster_labels, wave_crest_label):
    slicing_peak_indexes = []

    for index in range(1, len(cluster_labels)):
        if cluster_labels[index - 1] == wave_crest_label and cluster_labels[index] != wave_crest_label:
            slicing_peak_indexes.append(index)
    return slicing_peak_indexes

# 找出切割波長的轉折點
def find_slicing_peaks(peaks, slicing_peak_indexes):
    slicing_peaks = []

    for index in range(len(peaks)):
        if index in slicing_peak_indexes:
            slicing_peaks.append(peaks[index])
    return slicing_peaks

# 根據切割波長的轉折點來切割data
def slice_data(data, slicing_peaks):
    waves = []
    slicing_peaks_x = [slicing_peak[0] for slicing_peak in slicing_peaks]
    slicing_peaks_x = [-1] + slicing_peaks_x

    for index in range(len(slicing_peaks_x) - 1):
        waves.append(data[slicing_peaks_x[index] + 1:slicing_peaks_x[index + 1]])
    return waves

def compute_fft_amplitude(data):
    frequency_data = np.fft.fft(data) / len(data)
    return np.abs(frequency_data[1:20])

def compute_fft_phase(data):
    frequency_data = np.fft.fft(data) / len(data)
    return np.angle(frequency_data[1:20], deg = True)

def plot_time_domain_amplitude(data, peaks, slicing_peaks):
    plot.subplot(311)
    plot.xlabel("Time")
    plot.ylabel("Amplitude")
    # plot original data
    plot.plot([each[0] for each in data], [each[1] for each in data], color = "cornflowerblue")
    # plot peaks
    plot.scatter([each[0] for each in peaks], [each[1] for each in peaks], color = "mediumseagreen")
    # plot slicing lines
    for slicing_peak in slicing_peaks:
        plot.axvline(x = slicing_peak[0], color = "grey", linestyle = "--")

def plot_freq_domain_amplitude(amplitudes):
    plot.subplot(312)
    plot.xlabel("Frequency (Hz)")
    plot.ylabel("Amplitude")
    plot.plot(amplitudes[0], label = "wave 1", color = "red")
    plot.plot(amplitudes[1], label = "wave 2", color = "orange")
    plot.plot(amplitudes[2], label = "wave 3", color = "mediumseagreen")
    plot.plot(amplitudes[3], label = "wave 4", color = "cornflowerblue")
    plot.legend(loc = "upper right")

def plot_freq_domain_phase(phases):
    plot.subplot(313)
    plot.xlabel("Frequency (Hz)")
    plot.ylabel("Degree")
    plot.plot(phases[0], label = "wave 1", color = "red")
    plot.plot(phases[1], label = "wave 2", color = "orange")
    plot.plot(phases[2], label = "wave 3", color = "mediumseagreen")
    plot.plot(phases[3], label = "wave 4", color = "cornflowerblue")
    plot.legend(loc = "upper right")

if __name__ == "__main__":
    file = open(FILE_PATH)
    lines = file.readlines()

    data = []
    for index in range(1, len(lines)):
        data.append((index - 1, int(lines[index].replace("\n", ""))))
    # print(data)

    peaks = find_peaks(data)
    # print(peaks)

    kmeans = cluster.KMeans(n_clusters = 3).fit([(0, peak[1]) for peak in peaks])
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    print("cluster labels:")
    print(cluster_labels)
    # print(cluster_centers)

    wave_crest_label = find_largest_cluster_label(cluster_centers)
    print("wave crest cluster:", wave_crest_label)

    slicing_peak_indexes = find_slicing_peak_indexes(cluster_labels, wave_crest_label)
    # print(slicing_peak_indexes)

    slicing_peaks = find_slicing_peaks(peaks, slicing_peak_indexes)
    print("slicing peaks:")
    print(slicing_peaks)

    waves = slice_data(data, slicing_peaks)

    double_waves = []
    bias = 1
    for index in range(len(waves[:4])):
        double_waves.append(waves[index + bias] + waves[index + bias + 1])

    # 切一個一個波
    amplitudes = []
    phases = []
    for wave in waves[:4]:
        amplitudes.append(compute_fft_amplitude([y for x, y in wave]))
        phases.append(compute_fft_phase([y for x, y in wave]))

    plot.figure("One wave")
    plot_time_domain_amplitude(data, peaks, slicing_peaks)
    plot_freq_domain_amplitude(amplitudes)
    plot_freq_domain_phase(phases)

    # 切兩個兩個波
    amplitudes = []
    phases = []
    for wave in double_waves:
        amplitudes.append(compute_fft_amplitude([y for x, y in wave]))
        phases.append(compute_fft_phase([y for x, y in wave]))

    plot.figure("Two waves")
    plot_time_domain_amplitude(data, peaks, slicing_peaks)
    plot_freq_domain_amplitude(amplitudes)
    plot_freq_domain_phase(phases)
    plot.show()