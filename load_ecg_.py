import matplotlib.pyplot as plt
import csv
import numpy as np
import zero_cross as zc
import rr_features as rrf



def bitalino_real_units_mv(ecgb, nbits = 10):
    vcc = 3.3
    gecg = 1100
    n = 10
    return (ecgb * vcc / pow(2, n) - vcc / 2) / gecg * 1000



SAMPLING_RATE = 100

# load file 
fname = 'record/opensignals_2017-05-24_09-51-19.txt'

raw = []



with open(fname,'r') as f:
    next(f) # skip headings
    next(f) # skip headings
    next(f) # skip headings
    reader = csv.reader(f,delimiter='\t')
    for x in reader:
        raw.append(bitalino_real_units_mv(float(x[5])))

print(len(raw))

# add x val for plotting

# indexList = []
# for index in range(len(raw)):
#    indexList.append(index)
indexList = np.arange(0, len(raw), 1)

# QRS DETECTION
qrs = zc.Zero_Cross(raw, SAMPLING_RATE)
peaks = qrs.find_QRS(highcut=15)
rr_features = rrf.RR_features(peaks, SAMPLING_RATE)
rr_features.calc_features()



## PLOT

y2_ = qrs.y1 - 1


y2__ = np.array(qrs.y1)


fig, ax = plt.subplots() 
# print(peaks)

for c in peaks:
    plt.axvline(x=c, color="r", alpha=0.35)

# plt.plot(indexList, qrs.y3, indexList, qrs.y4, indexList, qrs.thr) #, indexList, y5, indexList, y2_,
plt.plot(indexList, qrs.y2)

raw_ = np.array(raw)
raw_ = raw_ + 0.2
plt.plot(indexList, raw_, color="b", alpha=0.35)


# for x in starts:
#     plt.axvline(x, color="y")

# for x in ends:
#     plt.axvline(x, color="k")

plt.xlim(0, 500)
plt.ylim(-0.5, 0.5)
plt.show()