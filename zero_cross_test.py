import wfdb
import numpy as np
import pyscript.zero_cross as zcross
import matplotlib.pyplot as plt
import time
import csv

rrs = []

full = ["100", "101", "103", "105", "106", "108",
        "109", "111", "112", "113", "114", "115", "116", "117",
        "118", "119", "121", "122", "123", "124", "200", "201",
        "202", "203", "205", "207", "208", "209", "210", "212",
        "213", "214", "215", "219", "220", "221", "222",
        "223", "228", "230", "231", "232", "233", "234",
        "102", "104", "107", "217"]  # PACED BEAT

test = ["108"]

ds1 = ["101", "106", "108", "109", "112", "114", "115", "116",
       "118", "119", "122", "124", "201", "203", "205", "207",
       "208", "209", "215", "220", "223", "230"]

ds2 = ["100", "103", "105", "111", "113", "117", "121", "123",
       "200", "202", "210", "212", "213", "214", "219", "221",
       "222", "228", "231", "232", "233", "234"]

ds3 = ["101", "106", "108", "109", "112", "114", "115", "116",
       "118", "119", "122", "124", "201", "203", "205", "207",
       "208", "209", "215", "220", "223", "230", "100", "105",
       "113", "121", "200", "210", "213", "219", "222", "231", "233"]

ds4 = ["103", "111", "117", "123", "202", "212", "214", "221",
       "228", "232", "234"]

paced = ["102", "104", "107", "217"]  # PACED BEAT

directory = "../record/json"          # "../mitbih"

files_used = ds1
filename = "test_ds1"

SAMPLING_RATE = 360
WINDOW_SIZE = 60 * SAMPLING_RATE

id_t = []
bp_t = []
nl_t = []
hf_t = []
zc_t = []
ed_t = []
total_t = []

# for i in range(len(files_used)):
#     ecgrecord = wfdb.rdsamp(directory + '/' + files_used[i], sampfrom=0, channels=[0])
#     # p_signal = ecgrecord.dac()
#     print('----- ', files_used[i], ' -----')
#
#     for j in range(ecgrecord.p_signals.size // WINDOW_SIZE):
#         # signal_window = np.empty([WINDOW_SIZE])
#         # signal_window = ecgrecord.p_signals[(j * WINDOW_SIZE):((j+1)*WINDOW_SIZE)]
#         # print(j)
#
#         signal_window = [None] * WINDOW_SIZE
#
#         for k in range(WINDOW_SIZE):
#             signal_window[k] = ecgrecord.p_signals[(j * WINDOW_SIZE) + k][0]
#
#         # start_time = time.time()
#         # peaks = wfdb.processing.gqrs_detect(x=signal_window, fs=SAMPLING_RATE, adcgain=ecgrecord.adcgain[0], adczero=ecgrecord.adczero[0])
#         # print("--- %s miliseconds ---" % ((time.time() - start_time) * 1000))
#
#         # print(peaks)
#
#
#         # ~ print(j, ", ", signal_window)
#
#         qrs = zcross.Zero_Cross(signal_window, SAMPLING_RATE)
#         start_time = time.time()
#         peaks, starts, ends, bp, nl, hf, zc, ed = qrs.find_QRS()
#
#         id_t.append(files_used[i] + ' [' + str(j) + ']')
#         bp_t.append(bp)
#         nl_t.append(nl)
#         hf_t.append(hf)
#         zc_t.append(zc)
#         ed_t.append(ed)
#         # total_t.append(bp + hl + hf + zc + ed)
#
#     # ~ print("--- %s miliseconds ---" % ((time.time() - start_time) * 1000))
#
#     # ~ if (j == 0):
#
#     # ~ indexList = np.arange(0, len(signal_window), 1)
#     # ~ fig, ax = plt.subplots()
#     # ~ for c in peaks:
#     # ~ plt.axvline(x=c, color="r", alpha=0.35)
#
#     # ~ #for c in starts:
#     # ~ #plt.axvline(x=c, color="g", alpha=0.35)
#
#     # ~ #for c in ends:
#     # ~ #plt.axvline(x=c, color="g", alpha=0.35)
#
#     # ~ ##plt.plot(indexList, qrs.y2)
#     # ~ ##plt.plot(indexList, qrs.y3)
#     # ~ #plt.plot(indexList, qrs.y4)
#     # ~ #plt.plot(indexList, qrs.thr)
#
#     # ~ #raw_ = np.array(qrs.raw)
#     # ~ #raw_ = raw_ + 0.2
#     # ~ #plt.plot(indexList, raw_, color="b", alpha=0.35)
#     # ~ plt.show()
#
# # ~ print(total_t, bp_t, hl_t, hf_t, zc_t, ed_t)
#
# print(id_t)
#
# save_file = "../export/test/" + filename + ".csv"
#
# with open(save_file, 'w') as csv_file:
#     wr = csv.writer(csv_file, delimiter=',')
#     wr.writerow(["record [min]", "bandpass", "nonlinear", "high-freq", "zero-cross-count", "event-detection"])
#     for i in range(len(id_t)):
#         wr.writerow([id_t[i], bp_t[i], nl_t[i], hf_t[i], zc_t[i], ed_t[i]])

import json

with open(directory + "/1.json") as json_file:
    data = json.load(json_file)

print(len(data))

signal_window = [None] * len(data)

for k in range(len(data)):
    signal_window[k] = data[k]

qrs = zcross.Zero_Cross(signal_window, 1000)
# start_time = time.time()
peaks, starts, ends, bp, nl, hf, zc, ed = qrs.find_QRS(lowcut=15, highcut=45, order=2)

indexList = np.arange(0, len(signal_window), 1)
fig, ax = plt.subplots()
for c in peaks:
    plt.axvline(x=c, color="r", alpha=0.35)

for c in starts:
    plt.axvline(x=c, color="g", alpha=0.35)

for c in ends:
    plt.axvline(x=c, color="m", alpha=0.35)

plt.plot(indexList, qrs.y2)
plt.plot(indexList, qrs.y3, alpha=0.35)
plt.plot(indexList, qrs.y4, alpha=0.35)
plt.plot(indexList, qrs.thr, alpha=0.35)

raw_ = np.array(qrs.raw)
raw_ = raw_ + 0.2
plt.plot(indexList, raw_, color="b", alpha=0.25)
plt.show()