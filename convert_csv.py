import wfdb
import pyscript.rr_features
import csv
from os.path import splitext
from os import walk


def save_csv(filename, rrs):
    save_file = filename + ".csv"

    with open(save_file, 'w') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        for rr in rrs:
            row = rr.feature
            # row.extend(rr.segment_250)
            # row.extend(rr.pca)
            row.extend(rr.label)
            # wr.writerow([rr.feature[0], rr.feature[1], rr.feature[2], rr.feature[3], rr.feature[4], rr.feature[5], rr.feature[6], rr.label])
            wr.writerow(row)


def save_arff(filename, rrs):
    save_file = filename + ".arff"
    with open(save_file, 'w') as csv_file:
        wr = csv.writer(csv_file)

        csv_file.write("@RELATION MITDB\n")
        # csv_file.write("@ATTRIBUTE prev\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE next\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE local_avg\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE rr2\tNUMERIC\n")     #avg
        # csv_file.write("@ATTRIBUTE rrir\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE 10rrir\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE peak_amp\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE rr2prev\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE rr3\tNUMERIC\n")
        # csv_file.write("@ATTRIBUTE rr3prev\tNUMERIC\n")

        for i in range(len(rrs[1].segment_250)):
            string = "@ATTRIBUTE s" + repr(i) + "\tNUMERIC\n"
            csv_file.write(string)

        # for i in range(len(rrs[1].pca)):
        #     string = "@ATTRIBUTE pca" + repr(i) + "\tNUMERIC\n"
        #     csv_file.write(string)

        csv_file.write("@ATTRIBUTE class\t{0, 1, 2, 3, 4}\n\n")

        csv_file.write("@DATA\n")

        wr = csv.writer(csv_file, delimiter=',')

        for rr in rrs:
            # row = rr.feature
            row = []
            row.extend(rr.segment_250)
            # row.extend(rr.pca)
            row.extend([rr.label])
            # wr.writerow([rr.feature[0], rr.feature[1], rr.feature[2], rr.feature[3], rr.feature[4], rr.feature[5], rr.feature[6], rr.label])
            wr.writerow(row)


rrs = []

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


# f = []
# for (dirpath, dirnames, filenames) in walk(directory):
#     f.extend(filenames)
#     break
#
# for i in range(len(f)):
#     f[i] = f[i][:-4]
#
# print(f)

file = test
filename = "ds1"

for i in range(len(file)):
    ann = wfdb.rdann(directory + '/' + file[i], 'atr')
    ecgrecord = wfdb.rdsamp(directory + '/' + file[i], sampfrom=0, channels=[0])

    rrf = pyscript.rr_features.RR_features(ann.sample, ecgrecord.adc(), 360)
    rrf.get_peak_amp()
    rrf.set_label(ann.subtype)
    rrf.remove_class([5])
    rrf.calc_features()
    # rrf.normalize()



    # rrf.print_features()

    print(i, ", ", len(rrf.rrs))

    for j in range(len(rrf.rrs)):
        rrs.append(rrf.rrs[j])
    # rrs.append(rrf.rrs)

    # save_arff(file[i], rrf.rrs)


# print("total ", len(rrs))


save_csv(filename,rrs)
# save_arff(filename, rrs)