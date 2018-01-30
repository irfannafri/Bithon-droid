import numpy as np

class RR(object):


    """docstring for RR"""
    def __init__(self, label=""):
        super(RR, self).__init__()
        
        self.prev = 0
        self.next = 0
        self.local_avg = 0
        self.avg = 0

        self.label = label

        self.feature = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #np.empty(7)
        self.segment_250 = []
        self.pre_peak = []
        self.post_peak = []
        self.pca = []



    def get_flat_data(self):
        return([self.feature[0], self.feature[1], self.feature[2], self.feature[3], self.label])