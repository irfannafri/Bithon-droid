import numpy as np
import pyscript.rr as rr

class RR_features(object):

    """docstring for RR"""
    def __init__(self, peaks, signals, sampling_rate): #signals
        super(RR_features, self).__init__()

        self.sampling_rate = sampling_rate
        self.signals = signals
        self.segmented_signals = []

        width = int(round(.25 * sampling_rate))
        side_width = int(round(width / 2))

        # print("side width: ", side_width)

        for p in peaks:
            # self.segmented_signals.append(self.signals[p])
            sgnl = []
            # print(signals[p][0])
            # if (p < side_width):
            #     for i in range(0, side_width - p):
            #         sgnl.append(0)
            #     for i in range(0, (p + side_width)):
            #         sgnl.append(signals[i][0])
            # elif (p + side_width > len(signals)):
            #     for i in range(p-side_width, len(signals)):
            #         sgnl.append(signals[i][0])
            #     for i in range(len(signals), p + side_width):
            #         sgnl.append(0)
            # else:
            #     for i in range(p-side_width, p+side_width):
            #         sgnl.append(signals[i][0])
            #
            #     for i in range(p + side_width - len(signals)):
            #         sgnl.append(0)


            # print(sgnl)
            self.segmented_signals.append(sgnl)
            # print(p, ", ", len(sgnl))


        self.peaks = peaks
        self.rrs = []
        # print(len(peaks))
        for r in peaks:
            self.rrs.append()


        # print(peaks)
        # print(self.segmented_signals)

        # print(len(peaks), ", " ,len(self.segmented_signals))



    def calc_features(self):
        # self.get_peak_amp()
        self.calc_rr_prev_next()
        # self.calc_rr_avg()
        self.calc_rr_local_avg(10)
        self.calc_rrir()
        self.calc_10rrir()
        # self.do_pca()
        self.calc_rrn()


    def calc_rrn(self):
        for i in range(len(self.rrs)):
            if (i > 1):
                self.rrs[i].feature[7] = self.peaks[i] - self.peaks[i - 2]
                if (i > 2):
                    self.rrs[i].feature[9] = self.peaks[i] - self.peaks[i - 3]

            if (i < len(self.rrs) - 3):
                self.rrs[i].feature[3] = self.peaks[i + 3] - self.peaks[i]
                if (i < len(self.rrs) - 2):
                    self.rrs[i].feature[8] = self.peaks[i + 2] - self.peaks[i]





    def get_peak_amp(self):
        for i in range(len(self.rrs)):
            self.rrs[i].feature[6] = self.signals[self.peaks[i]][0]
            self.rrs[i].segment_250 = self.segmented_signals[i]

            # print("(", i, ") ", self.rrs[i].feature[6], len(self.rrs[i].segment_250))

    # def do_pca(self):
    #     for i in self.rrs:
    #         X = np.array(i.segment_250).reshape(-1, 1)
            # pca = PCA()
            # pca.fit(X)
            # i.pca = pca.components_[0]
            # i.pca = pca.transform(X)
            # print(len(i.pca))


    def set_label(self, label):
        # print(label[1])
        for i in range(len(label)):
            # print(label[i])
            self.rrs[i].label = label[i]

            # R   : RBBB = N
            # L   : LBBB = N
            # N   : NOR  = N
            # e   : AE   = N
            # j   : NE   = N
            # V   : PVC  = V
            # E   : VE   = V
            # A   : AP   = S
            # J   : NP   = S
            # a   : aAP  = S
            # S   : SP   = S
            # F   : fVN  = F
            # Q   : U    = Q
            # f   : fPN  = Q
            # /   : P    = Q

            # N = 0
            # V = 1
            # S = 2
            # F = 3
            # Q = 4
            # else = 5

            # if ((label[i] == "N")):
            #     self.rrs[i].label = "N"
            # elif ((label[i] == "R")):
            #     self.rrs[i].label = "R"
            # elif ((label[i] == "L")):
            #     self.rrs[i] == "L"

            if ((label[i] == "N") or (label[i] == "R")
                or (label[i] == "L") or (label[i] == "e")
                or (label[i] == "j")):
                self.rrs[i].label = 0 #"N" #
            elif ((label[i] == "V") or (label[i] == "E")):
                self.rrs[i].label = 1 #"V" #
            elif ((label[i] == "A") or (label[i] == "J")
                  or (label[i] == "a") or (label[i] == "S")):
                self.rrs[i].label = 2 #"S" #
            elif (label[i] == "F"):
                self.rrs[i].label = 3 #"F" #
            elif ((label[i] == "Q") or (label[i] == "f")
                  or (label[i] == "/")):
                self.rrs[i].label = 4 # "Q" #
            else:
                self.rrs[i].label = 5 # "else"

    def remove_class(self, label):
        for i in range(len(label)):
            self.rrs = [rr for rr in self.rrs if rr.label != label[i]]

    def print_features(self):
        print(self.rrs[1].label)
        for i in range(len(self.rrs)):
            # print("["+repr(i)+"] "+self.rrs[i].label)
            print("[",repr(i)+"] ", "{0:.2f}".format(self.peaks[i]), " - ", self.rrs[i].label , " - (" , "{0:.2f}".format(self.rrs[i].feature[0]) , ", "
                  , "{0:.8f}".format(self.rrs[i].feature[1]) , ", " , "{0:.2f}".format(self.rrs[i].feature[3]) , ", " , "{0:.2f}".format(self.rrs[i].feature[2]) , ", "
                  , "{0:.2f}".format(self.rrs[i].feature[4]), ", ", "{0:.2f}".format(self.rrs[i].feature[5]) , ")")

    def normalize(self):
        min_prev    = 99999
        min_next    = 99999
        min_local_avg = 99999

        max_prev    = -1
        max_next    = -1
        max_local_avg = -1

        for i in range(len(self.rrs)):
            if (self.rrs[i].feature[0] < min_prev):
                min_prev = self.rrs[i].feature[0]

            if (self.rrs[i].feature[1] < min_next):
                min_next = self.rrs[i].feature[1]

            if (self.rrs[i].feature[2] < min_local_avg):
                min_local_avg = self.rrs[i].feature[2]

            if (self.rrs[i].feature[0] > max_prev):
                max_prev = self.rrs[i].feature[0]

            if (self.rrs[i].feature[1] > max_next):
                max_next = self.rrs[i].feature[1]

            if (self.rrs[i].feature[2] > max_local_avg):
                max_local_avg = self.rrs[i].feature[2]


        for i in range(len(self.rrs)):
            self.rrs[i].feature[0] = (self.rrs[i].feature[0] - min_prev) / (max_prev - min_prev)
            self.rrs[i].feature[1] = (self.rrs[i].feature[1] - min_next) / (max_next - min_next)
            self.rrs[i].feature[2] = (self.rrs[i].feature[2] - min_local_avg) / (max_local_avg - min_local_avg)


    def calc_rr_prev_next(self):
        self.peaks = self.peaks / self.sampling_rate
        for i in range(len(self.rrs)):
            if i < len(self.rrs) - 1:
                self.rrs[i].feature[1] = self.peaks[i+1] - self.peaks[i]

                if i == 0:
                    self.rrs[i].feature[0] = 0 # -1
                else:
                    self.rrs[i].feature[0] = self.rrs[i-1].feature[1]
                
            else:
                self.rrs[i].feature[1] = 0 # -1
                self.rrs[i].feature[0] = self.rrs[i-1].feature[1]


    def calc_rrir(self):

        for i in range(len(self.rrs) - 2):
            self.rrs[i].feature[4] = self.rrs[i].feature[1] / self.rrs[i+1].feature[1]

            # if i == len(self.rrs) - 2:
            #     print("2nd last")

        # TODO : handle the last rr
        self.rrs[len(self.rrs) - 2].feature[4] = 1
        self.rrs[len(self.rrs) - 1].feature[4] = 1


    def calc_10rrir(self):
        width = 10

        for i in range(1, len(self.rrs)):
            count = 0
            tempval = 0

            if (i == 0):
                tempval = 1
                count = 1
            elif (i < width):
                for j in range(1, i + 1):
                    tempval += self.rrs[i - j].feature[1]
                    count += 1
            else:
                for j in range(1, width + 1):
                    tempval += self.rrs[i - j].feature[1]
                    count += 1

            self.rrs[i].feature[5] = self.rrs[i].feature[1] / (tempval / count)



    def calc_rr_avg(self):
        tempval = 0

        for i in range(len(self.rrs) - 1):
            tempval = tempval + self.rrs[i].feature[1]

        tempval = tempval / (len(self.rrs) - 1)

        for i in range(len(self.rrs)):
            self.rrs[i].feature[3] = tempval



    def calc_rr_local_avg(self, width):
        side_width = int(width / 2)
        # print("s_width " + repr(side_width))

        for i in range(len(self.rrs)):
            tempval = self.rrs[i].feature[1]
            # tempval = 0

            if (i < side_width):
                
                for j in range(1, i + 1):
                    tempval += self.rrs[i-j].feature[1]

                for j in range(1, side_width):
                    tempval += self.rrs[i+j].feature[1]

                self.rrs[i].feature[2] = tempval / (i + side_width)

            elif (i > len(self.rrs) - side_width - 1):
                
                for j in range(1, side_width + 1):
                    tempval += self.rrs[i-j].feature[1]

                for j in range(1, len(self.rrs) - i):
                    tempval += self.rrs[i+j].feature[1]

                self.rrs[i].feature[2] = tempval / (len(self.rrs) - i + side_width)


            else:
                for j in range(1, side_width + 1):
                    tempval += self.rrs[i-j].feature[1]

                for j in range(1, side_width):
                    tempval += self.rrs[i+j].feature[1]

                    # if (i == 5):
                    #     print(repr(j) + ". temp " + repr(tempval))

                self.rrs[i].feature[2] = tempval / (width)
            
        