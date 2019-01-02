import os
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plot

from waveSlicer import WaveSlicer

FILE_PATH = "../data/"

def read_directories():
    for root, dirs, file_paths in os.walk(FILE_PATH):
        return [FILE_PATH + dir + "/" for dir in dirs]

def read_samples(directories):
    samples = []
    for directory in directories:
        data = []
        for root, dirs, file_paths in os.walk(directory):
            file_paths.sort()
            for file_path in file_paths:
                file = open(directory + file_path)
                lines = file.readlines()
                for index in range(1, len(lines)):
                    data.append(int(lines[index].replace("\n", "")))
        data = [(index, data[index]) for index in range(len(data))]
        samples.append(data)
    return samples

def analyze(title, waves):
    amplitudes = []
    phases = []
    for wave in waves:
        amplitudes.append(compute_fft_amplitude([y for x, y in wave]))
        phases.append(compute_fft_phase([y for x, y in wave]))
    plot.figure(title)

    plot_time_domain_amplitude(data, peaks, slicing_peaks)
    plot_freq_domain_amplitude(amplitudes)
    plot_freq_domain_phase(phases)

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

def analyze_mean_stdev(waves):
    amplitudes = []
    for wave in waves:
        amplitudes.append(compute_fft_amplitude([y for x, y in wave]))
    for amplitude in amplitudes:
        amplitude.sort()

    means = []
    stdevs = []
    for index in reversed(range(len(amplitudes[0]))):
        means.append(np.mean([amplitude[index] for amplitude in amplitudes]))
        stdevs.append(np.std([amplitude[index] for amplitude in amplitudes]))
    return means, stdevs

def write_file(file, dataset_name, double_waves_base, quadra_waves_base, octa_waves_base):
    file.write(dataset_name + "\n")
    file.write("mean," + str(double_waves_mean) + "\n")
    file.write("stdev," + str(double_waves_stdev) + "\n")
    file.write("coefvar," + str(double_waves_coefvar) + "\n")
    line = ""
    for each in double_waves_base:
        line += str(each) + ","
    line = line[:-1] + "\n"
    file.write(line)
    file.write("mean," + str(quadra_waves_mean) + "\n")
    file.write("stdev," + str(quadra_waves_stdev) + "\n")
    file.write("coefvar," + str(quadra_waves_coefvar) + "\n")
    line = ""
    for each in quadra_waves_base:
        line += str(each) + ","
    line = line[:-1] + "\n"
    file.write(line)
    file.write("mean," + str(octa_waves_mean) + "\n")
    file.write("stdev," + str(octa_waves_stdev) + "\n")
    file.write("coefvar," + str(octa_waves_coefvar) + "\n")
    line = ""
    for each in octa_waves_base:
        line += str(each) + ","
    line = line[:-1] + "\n"
    file.write(line)

if __name__ == "__main__":
    directories = read_directories()
    samples = read_samples(directories)

    file = open("../result.csv", "w", encoding = "utf_8_sig")

    for data in samples:
        dataset_name = directories[samples.index(data)].split("/")[2]

        # data: [(index, amplitude), ...]
        slicer = WaveSlicer()
        slicer.fit(data)

        waves = slicer.get_waves()
        waves = waves[1:]

        # 兩個波
        double_waves = []
        for index in range(len(waves) - 1):
            double_waves.append(waves[index] + waves[index + 1])
        double_waves_base = []
        for wave in double_waves:
            amplitudes = compute_fft_amplitude([y for x, y in wave])
            amplitudes.sort()
            double_waves_base.append(amplitudes[-1])

        # 四個波
        quadra_waves = []
        for index in range(len(waves) - 3):
            quadra_waves.append(waves[index] + waves[index + 1] + waves[index + 2] + waves[index + 3])
        quadra_waves_base = []
        for wave in quadra_waves:
            amplitudes = compute_fft_amplitude([y for x, y in wave])
            amplitudes.sort()
            quadra_waves_base.append(amplitudes[-1])

        # 八個波
        octa_waves = []
        for index in range(len(waves) - 7):
            octa_waves.append(waves[index] + waves[index + 1] + waves[index + 2] + waves[index + 3] + waves[index + 4] + waves[index + 5] + waves[index + 6] + waves[index + 7])
        octa_waves_base = []
        for wave in octa_waves:
            amplitudes = compute_fft_amplitude([y for x, y in wave])
            amplitudes.sort()
            octa_waves_base.append(amplitudes[-1])

        double_waves_mean = np.mean(double_waves_base)
        quadra_waves_mean = np.mean(quadra_waves_base)
        octa_waves_mean = np.mean(octa_waves_base)

        double_waves_stdev = np.std(double_waves_base)
        quadra_waves_stdev = np.std(quadra_waves_base)
        octa_waves_stdev = np.std(octa_waves_base)

        double_waves_coefvar = double_waves_stdev / double_waves_mean
        quadra_waves_coefvar = quadra_waves_stdev / quadra_waves_mean
        octa_waves_coefvar = octa_waves_stdev / octa_waves_mean

        # # 切一個一個波
        # analyze("One wave", waves[1:5])
        # # 切兩個兩個波
        # analyze("Two waves", double_waves[1:5])

        # print(dataset_name)
        # means, stdevs = analyze_mean_stdev(waves)
        # coefvars = [stdev / mean for mean, stdev in zip(means, stdevs)]
        # print("means:", means)
        # print("stdevs:", stdevs)
        # print("coefvars:", coefvars)
        # print()

        print(dataset_name)
        print(double_waves_base)
        print(quadra_waves_base)
        print(octa_waves_base)
        write_file(file, dataset_name, double_waves_base, quadra_waves_base, octa_waves_base)

        # plot.show()
