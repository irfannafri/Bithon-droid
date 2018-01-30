import wfdb
import pandas as pd

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

file = test
filename = "ds1"

for i in range(len(file)):
    annotation = wfdb.rdann(directory + '/' + file[i], 'atr')
    record = wfdb.rdsamp(directory + '/' + file[i], sampfrom=0, channels=[0])
    features = [
        'amp',
        'prev1', 'prev2', 'prev3',
        'next1', 'next2', 'next3',
        'RRIR', '10RRIR',
        'loc_avg',
        'class'
    ]
    df = pd.DataFrame(index=list(range(0, annotation.sample.size)), columns=features)
    df = df.fillna(0)

    print(df)
