import wfdb
import rr_features
import numpy
import csv
from os.path import splitext
from os import walk

# class load_mitdb(object):
full  = ["100" , "101", "103", "105", "106", "108",
         "109", "111", "112", "113", "114", "115", "116", "117",
         "118", "119", "121", "122", "123", "124", "200", "201",
         "202", "203", "205", "207", "208", "209", "210", "212",
         "213", "214", "215", "219", "220", "221", "222",
         "223", "228", "230", "231", "232", "233", "234",
         "102", "104", "107", "217" ] # PACED BEAT

test  = ["100"]

ds1   = ["101", "106", "108", "109", "112", "114", "115", "116",
         "118", "119", "122", "124", "201", "203", "205", "207",
         "208", "209", "215", "220", "223", "230"]

ds2   = ["100", "103", "105", "111", "113", "117", "121", "123",
         "200", "202", "210", "212", "213", "214", "219", "221",
         "222", "228", "231", "232", "233", "234"]

ds3   = ["101", "106", "108", "109", "112", "114", "115", "116",
         "118", "119", "122", "124", "201", "203", "205", "207",
         "208", "209", "215", "220", "223", "230", "100", "105",
         "113", "121", "200", "210", "213", "219", "222", "231", "233"]

ds4   = ["103", "111", "117", "123", "202", "212", "214", "221",
         "228", "232", "234"]

paced = ["102", "104", "107", "217" ] # PACED BEAT


directory = "mitbih"
file = ds3
filename = "ds3__250"

# def __init__(self):
#     super(self).__init__()

def load_data(valid_portion=0.2):

    xsize = 0
    xidx = 0

    for i in range(len(file)):
        ann = wfdb.rdann(directory + '/' + file[i], 'atr')
        for j in range (len(ann.annsamp)):
            xsize = xsize + 1

    train_set_x = numpy.empty([xsize, 90])
    train_set_y = []
    for i in range(len(file)):
        ann = wfdb.rdann(directory + '/' + file[i], 'atr')
        ecgrecord = wfdb.rdsamp(directory + '/' + file[i], sampfrom=0, channels=[0])

        rrf = rr_features.RR_features(ann.annsamp, ecgrecord.p_signals, 360)
        rrf.get_peak_amp()
        rrf.set_label(ann.anntype)
        rrf.remove_class(["else"])
        rrf.calc_features()
        # rrf.normalize()
        # rrf.print_features()

        # print(i, ", ", len(rrf.rrs))

        for j in range(len(rrf.rrs)):
            # x = rrf.rrs[j].feature
            # x.extend(rrf.rrs[j].segment_250)
            # train_set_x.append(x)
            if len(rrf.rrs[j].segment_250)< 90:
                print(file[i], ", ", j)
            train_set_x[xidx] = numpy.array(rrf.rrs[j].segment_250)
            train_set_y.append(rrf.rrs[j].label)
            # print(len(x), ", ", len(train_set_x))
            xidx = xidx + 1

    n_samples = len(train_set_x)
    sidx = numpy.random.permutation(n_samples)
    n_train = int(numpy.round(n_samples * (1. - valid_portion)))
    valid_set_x = [train_set_x[s] for s in sidx[n_train:]]
    valid_set_y = [train_set_y[s] for s in sidx[n_train:]]
    train_set_x = [train_set_x[s] for s in sidx[:n_train]]
    train_set_y = [train_set_y[s] for s in sidx[:n_train]]

    train_x = numpy.array(train_set_x)
    valid_x = numpy.array(valid_set_x)
    # print(train_x.shape)

    train = (train_x, train_set_y)
    valid = (valid_x, valid_set_y)
    # test = (test_set_x, test_set_y)

    return train, valid #, test



