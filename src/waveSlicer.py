from sklearn import cluster

class WaveSlicer:
    def __init__(self):
        return

    # 找出所有轉折點
    def find_peaks(self):
        peaks = []
        previous_slope = None
        for index in range(1, len(self.data)):
            difference = self.data[index][1] - self.data[index - 1][1]
            if difference == 0:
                continue
            if difference > 0:
                if previous_slope is "negative":
                    peaks.append(self.data[index - 1])
                previous_slope = "positive"
                continue
            if difference < 0:
                if previous_slope is "positive":
                    peaks.append(self.data[index - 1])
                previous_slope = "negative"
                continue
        return peaks

    # 找出cluster_center最大的label(波峰的label)
    def find_largest_cluster_label(self):
        largest_cluster = 0
        largest_center = 0
        for index in range(len(self.cluster_centers)):
            if self.cluster_centers[index][1] > largest_center:
                largest_cluster = index
                largest_center = self.cluster_centers[index][1]
        return largest_cluster

    # 找出波谷的index
    def find_wave_trough_indexes(self):
        wave_trough_indexes = []
        for index in range(1, len(self.cluster_labels)):
            if self.cluster_labels[index - 1] != self.wave_crest_label and self.cluster_labels[index] == self.wave_crest_label:
                wave_trough_indexes.append(index - 1)
        return wave_trough_indexes

    # 找出切割波長的轉折點的index
    def find_slicing_peak_indexes(self):
        slicing_peak_indexes = []
        for index in range(1, len(self.cluster_labels)):
            if self.cluster_labels[index - 1] == self.wave_crest_label and self.cluster_labels[index] != self.wave_crest_label:
                slicing_peak_indexes.append(index)
        return slicing_peak_indexes

    # 找出切割波長的轉折點
    def find_slicing_peaks(self):
        slicing_peaks = []
        for index in range(len(self.peaks)):
            if index in self.slicing_peak_indexes:
                slicing_peaks.append(self.peaks[index])
        return slicing_peaks

    # 根據切割波長的轉折點來切割data
    def slice_data(self):
        waves = []
        slicing_peaks_x = [slicing_peak[0] for slicing_peak in self.slicing_peaks]
        slicing_peaks_x = [-1] + slicing_peaks_x
        for index in range(len(slicing_peaks_x) - 1):
            waves.append(self.data[slicing_peaks_x[index] + 1:slicing_peaks_x[index + 1]])
        return waves

    def fit(self, data):
        # data: [(index, amplitude), ...]
        self.data = data

        # peaks: [(index, amplitude), ...]
        self.peaks = self.find_peaks()

        kmeans = cluster.KMeans(n_clusters = 3).fit([(0, peak[1]) for peak in self.peaks])
        # cluster_labels: [label of peak, ...]
        self.cluster_labels = kmeans.labels_
        self.cluster_centers = kmeans.cluster_centers_

        self.wave_crest_label = self.find_largest_cluster_label()
        # print("wave crest cluster label:", self.wave_crest_label)

        self.slicing_peak_indexes = self.find_wave_trough_indexes()
        # print(self.slicing_peak_indexes)

        self.slicing_peaks = self.find_slicing_peaks()
        # print("slicing peaks:")
        # print(self.slicing_peaks)

        self.waves = self.slice_data()

    def get_waves(self):
        return self.waves

    def get_slicing_peaks(self):
        return self.slicing_peaks
