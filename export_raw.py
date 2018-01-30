import wfdb

rrs = []

full = ["100", "101", "103", "105", "106", "108",
        "109", "111", "112", "113", "114", "115", "116", "117",
        "118", "119", "121", "122", "123", "124", "200", "201",
        "202", "203", "205", "207", "208", "209", "210", "212",
        "213", "214", "215", "219", "220", "221", "222",
        "223", "228", "230", "231", "232", "233", "234",
        "102", "104", "107", "217"]  # PACED BEAT

test = ["100"]

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

directory = "mitbih"
file = ds1
filename = "ds1_raw_"

for i in range(len(file)):
    rrs = []
    ann = wfdb.rdann(directory + '/' + file[i], 'atr')
    ecgrecord = wfdb.rdsamp(directory + '/' + file[i], sampfrom=0, channels=[0])

    for x in range(len(ecgrecord.p_signals)):
        rrs.append(ecgrecord.p_signals[x])

    import csv

    save_file = filename + file[i] + ".csv"
    with open(save_file, 'w') as csv_file:
        wr = csv.writer(csv_file)
        for rr in rrs:
            wr.writerow(rr)

# import json

# with open(filename, 'w') as outputfile:
#     json.dump(rrs, outputfile)

from matplotlib import pyplot as plt

plt.plot(rrs)