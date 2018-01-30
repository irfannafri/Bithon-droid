import numpy as np
from scipy.signal import butter, lfilter, firwin
from scipy.signal import freqz
import tools as st
import time


class Zero_Cross(object):
    """docstring for Zero_Cross"""

    def __init__(self, raw, SAMPLING_RATE=100):
        super(Zero_Cross, self).__init__()
        self.raw = raw
        self.SAMPLING_RATE = SAMPLING_RATE

    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def calc_low_high(self, lowcut, highcut, fs):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        return low, high

    def window_bandpass(self, lowcut, highcut, fs, numtaps):
        f1, f2 = self.calc_low_high(lowcut, highcut, fs)
        taps = firwin(numtaps, [f1, f2], pass_zero=False)
        return taps

    def window_bandpass_filter(self, data, lowcut, highcut, fs, numtaps):
        taps = self.window_bandpass(lowcut, highcut, fs, numtaps)
        y = lfilter(taps, 1.0, data)
        return y

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        low, high = self.calc_low_high(lowcut, highcut, fs)
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def odd_even(self, x):
        if x & 1:
            return -1
        else:
            return 1

    def high_freq_add(self, data, ff=1.0, c=3.0):
        bn = 0.0
        kn = 0.0
        kn1 = 0.0

        # y = []
        # for i in range(0, len(data)):
        #     y.append(0)
        y = np.empty(len(data))

        kn1 = 0.0125

        for i in range(0, len(data)):
            # if i == 0:
            #     kn = kn1
            # else:
            #     kn = ff * kn1 + (1 - ff) * abs(data[i]) * c
            kn = kn1
            bn = self.odd_even(i) * kn  # pow(-1, i) * kn
            y[i] = data[i] + bn
            kn1 = kn

        return y

    def signum(self, data):
        ret = 0
        if (data > 0):
            ret = 1
        elif (data < 0):
            ret = -1

        return ret

    def abs(self, data):

        if (data >= 0):
            return data
        elif (data < 0):
            return data * -1

            # ~ return ret

    def zero_cross_count(self, data, ff=0.85):
        # y = []
        # dn = []

        # for i in range(0, len(data)):
        #     y.append(0)
        #     dn.append(0)

        y = np.empty(len(data))
        dn = np.empty(len(data))

        for i in range(0, len(data)):
            if i == 0:
                dn[i] = 1  # abs(np.sign(data[i]) / 2)
                y[i] = 1  # ff + (1 - ff) * dn[i]
            else:
                dn[i] = self.abs((self.signum(data[i]) - self.signum(data[i - 1])) / 2)
                y[i] = ff * y[i - 1] + (1 - ff) * dn[i]

        return y

    def adaptive_threshold(self, data, ff=0.85):
        # y = []

        # for i in range(0, len(data)):
        #     y.append(0)
        y = np.empty(len(data))

        for i in range(0, len(data)):
            if i == 0:
                y[i] = 1  # ff + (1 - ff) * data[i]
            else:
                y[i] = ff * y[i - 1] + (1 - ff) * data[i]

        return y

    def search_window(self, data, thr):
        y5 = np.empty(len(data))
        starts = []
        ends = []
        last_start = -1
        last_end = -1
        last_status = 0
        cur_status = 0
        timelimit = int(self.SAMPLING_RATE * 0.12)
        # print(timelimit)

        for i in range(0, len(data)):

            if data[i] < thr[i]:
                cur_status = 1
            else:
                cur_status = 0

            if cur_status - last_status == 1:
                if (i > timelimit):
                    if (i - last_end) > timelimit:
                        last_start = i
                        starts.append(i - 2)
                    else:
                        ends.pop()
                else:
                    last_start = i
                    starts.append(i - 2)


            elif cur_status - last_status == -1:
                last_end = i
                ends.append(i)

            last_status = cur_status

            # if y4[i] <= thr[i]:
            #     y5[i] = 0.5
            # else:
            #     y5[i] = -0.5

        if (len(starts) > len(ends)):
            # print('starts ', starts)
            # print('ends   ', ends)

            ends.append(len(data))

        return starts, ends

    def temporal_localization(self, data, starts, ends):
        peaks = np.empty(len(starts))
        # print("temp loc", len(starts), len(ends))

        for i in range(len(starts)):
            maxpeak_val = 0
            maxpeak_loc = -1

            minpeak_val = 0
            minpeak_loc = -1
            # print("temp loc", starts[i], " - ", ends[i])

            for j in range(starts[i], ends[i]):
                if data[j] > maxpeak_val:
                    maxpeak_val = data[j]
                    maxpeak_loc = j

                if data[j] < minpeak_val:
                    minpeak_val = data[j]
                    minpeak_loc = j

            if maxpeak_val > abs(minpeak_val):
                peaks[i] = maxpeak_loc
            else:
                peaks[i] = minpeak_loc

        return peaks

    def calc_time(self, time1, time2):
        return (time2 - time1) * 1000

    def find_QRS(self, lowcut=5, highcut=45, order=3, ff_hf=1.0, c_hf=3, ff_zc=0.8, ff_thr=0.75):
        ## FILTERING
        order = int(0.3 * self.SAMPLING_RATE)
        # y1 = butter_lowpass_filter(raw, highcut, SAMPLING_RATE, order)
        # y1 = butter_highpass_filter(raw, lowcut, SAMPLING_RATE, order)
        # y1 = butter_bandpass_filter(raw, lowcut, highcut, SAMPLING_RATE, order)

        bandpass_time = time.time()
        # filter signal
        self.y1, _, _ = st.filter_signal(signal=self.raw,
                                         ftype='FIR',
                                         band='bandpass',
                                         order=order,
                                         frequency=[lowcut, highcut],
                                         sampling_rate=self.SAMPLING_RATE)
        # self.y1 = self.raw
        # print("findqrs", len(self.y1))

        nonlinear_time = time.time()
        ## NONLINEAR
        self.y2 = np.sign(self.y1) * (self.y1 * self.y1)

        hf_time = time.time()
        ## HIGH-FREQ NOISE ADDING
        self.y3 = self.high_freq_add(self.y2, ff_hf, c_hf)

        zc_time = time.time()
        ## ZERO CROSS COUNT
        self.y4 = self.zero_cross_count(self.y3, ff_zc)

        ed_time = time.time()
        ## EVENT DETECTION
        self.thr = self.adaptive_threshold(self.y4, ff_thr)
        starts, ends = self.search_window(self.y4, self.thr)
        peaks = self.temporal_localization(self.raw, starts, ends)

        end_time = time.time()

        # print("bp: ", self.calc_time(bandpass_time, nonlinear_time),
        #       "nl: ", self.calc_time(nonlinear_time, hf_time),
        #       "hf: ", self.calc_time(hf_time, zc_time),
        #       "zc: ", self.calc_time(zc_time, ed_time),
        #       "ed: ", self.calc_time(ed_time, end_time))

        t1 = self.calc_time(bandpass_time, nonlinear_time)
        t2 = self.calc_time(nonlinear_time, hf_time)
        t3 = self.calc_time(hf_time, zc_time)
        t4 = self.calc_time(zc_time, ed_time)
        t5 = self.calc_time(ed_time, end_time)

        return peaks, starts, ends, t1, t2, t3, t4, t5
