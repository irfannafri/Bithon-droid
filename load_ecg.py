import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import butter, lfilter, firwin
from scipy.signal import freqz
global N
#global g



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


def butter_bandpass(lowcut, highcut, fs, order=2):
    low, high = calc_low_high(lowcut, highcut, fs)
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
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


lowcut = 5
highcut = 20


y1 = butter_bandpass_filter(a3s, lowcut, highcut, SAMPLING_RATE, order=7)

y2 = [None] * len(y1)

for i in range(0, len(y1)):
        if i==0 :
                y2[i]= (2*y1[i+1]+y1[i+2])/8
        elif i==1:
                y2[i]= (-2*y1[i-1]+2*y1[i+1]+y1[i+2])/8
        elif i== len(y1)-2:
                 y2[i]= (-y1[i-2]-2*y1[i-1]+2*y1[i+1])/8
        elif i== len(y1)-1:
                y2[i]= (-y1[i-2]-2*y1[i-1])/8
        else :
                y2[i]= (-y1[i-2]-2*y1[i-1]+2*y1[i+1]+y1[i+2])/8
                


        
#y2 = y1 * y1
y3 = []
for i in range(0, len(y1)):
        y3.append(0)

for i in range(0, len(y2)):
        y3[i] = y1[i] * y1[i]


#plt.plot(indexList, y1, indexList, y2)
#plt.show()
        
y4 = []
N=15
y4= [None]*len(y3)
for i in range(0,len(y3)):

    tempVal = y3[i]

    if (i < N):
        for j in range(0, i):
            tempVal = tempVal + y3[i-j]
    else:
        for j in range(0, N):
            tempVal = tempVal + y3[i-j]

    y4[i] = tempVal / N

       
    # if i >= len(y3)-N :
    #     #y4[i]=(y3[i]+ y3[i-1]+ y3[i-2]+ y3[i-3]+ y3[i-4])/N 
    #     y4[i]=(y3[i]+y3[i]-(N-1)+y3[i]-(N-2)+y3[i]-(N-3)+y3[i]-(N-4)+y3[i]-(N-5))/N
    #     #y4[i]= (y3[i-(N-1)]+y3[i-(N-2)]+y3[i-(N-3)]+y3[i-(N-4)]+y3[i-(N-5)]+y3[i-(N-6)])/N
    # else:
    #     pass



plt.plot(indexList, y1, indexList, y4)
plt.show()


