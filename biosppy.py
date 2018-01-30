import numpy as np
import biosppy.signals.ecg as ecg

# load raw ECG signal
signal = np.loadtxt('opensignals_2017-05-24_14-07-57.txt')

# process it and plot
out = ecg.ecg(signal=signal, sampling_rate=100., show=True)