import matplotlib.pyplot as plt
import csv

fname = 'opensignals_2017-05-24_09-26-25.txt'

a3s = []

with open(fname,'r') as f:
    next(f) # skip headings
    next(f) # skip headings
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for x in reader:
        a3s.append(x[5])

print(len(a3s))

indexList = []
for index in range(len(a3s)):
   indexList.append(index)

plt.plot(indexList, a3s)
plt.show()
