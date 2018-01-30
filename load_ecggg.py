import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import butter, lfilter, firwin
from scipy.signal import freqz





def calc_low_high(lowcut, highcut, fs):
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	return low, high

def window_bandpass(lowcut, highcut, fs, numtaps):
	f1, f2 = calc_low_high(lowcut, highcut, fs)
	taps = firwin(numtaps, [f1, f2], pass_zero=False)
	return taps

def window_bandpass_filter(data, lowcut, highcut, fs, numtaps):
	taps = window_bandpass(lowcut, highcut, fs, numtaps)
	y = lfilter(taps, 1.0, data)
	return y


def butter_bandpass(lowcut, highcut, fs, order=5):
    low, high = calc_low_high(lowcut, highcut, fs)
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



SAMPLING_RATE = 100

# load file 
fname = 'opensignals_2017-05-24_14-07-57.txt'

a3s = []

with open(fname,'r') as f:
    next(f) # skip headings
    next(f) # skip headings
    next(f) # skip headings
    reader = csv.reader(f,delimiter='\t')
    for x in reader:
        a3s.append(float(x[5]))

print(len(a3s))

# add x val for plotting
indexList = []
for index in range(len(a3s)):
   indexList.append(index)


# filter signal
# order = int(0.3 * SAMPLING_RATE)
# b, a = signal.butter(1, 0.25)
# zi = signal.lfilter_zi(b, a)
# z, _ = signal.lfilter(b, a, a3s, zi=zi*a3s[0])

lowcut = 18
highcut = 35

# plt.figure(1)
# plt.clf()
# for order in [3, 6, 9]:
# 	b, a = butter_bandpass(lowcut, highcut, SAMPLING_RATE, order=order)
# 	w, h = freqz(b, a, worN=2000)
# 	plt.plot((SAMPLING_RATE * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

# plt.plot([0, 0.5 * SAMPLING_RATE], [np.sqrt(0.5), np.sqrt(0.5)],
#          '--', label='sqrt(0.5)')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain')
# plt.grid(True)
# plt.legend(loc='best')
# plt.show()

# y = butter_bandpass_filter(a3s, lowcut, highcut, SAMPLING_RATE, order=3)
y = window_bandpass_filter(a3s, lowcut, highcut, SAMPLING_RATE, numtaps=27)
plt.plot(indexList, a3s, indexList, y)
plt.show()


# plt.plot(indexList, a3s)
# plt.plot(indexList, z)
# plt.show()
