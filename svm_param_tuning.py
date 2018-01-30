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
file = ds1
# filename = "ds3__250"

# def __init__(self):
#     super(self).__init__()

def load_data(valid_portion=0.2):

    xsize = 0
    xidx = 0

    # for i in range(len(file)):
    #     ann = wfdb.rdann(directory + '/' + file[i], 'atr')
    #     for j in range (len(ann.annsamp)):
    #         xsize = xsize + 1

    train_set_x = [] #numpy.empty([xsize, 90])
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
            x = rrf.rrs[j].feature
            train_set_x.append(x)
            train_set_y.append(rrf.rrs[j].label)
            # print("j: ", len(train_set_x))
        #     if (j == 0):
        #         print("j=> ", train_set_x)
        #
        # print("i: ", len(train_set_x))


    n_samples = len(train_set_x)
    sidx = numpy.random.permutation(n_samples)
    n_train = int(numpy.round(n_samples * (1. - valid_portion)))

    print("n_samp:", n_samples, " sidx: ", sidx, " n_train: ", n_train)

    valid_set_x = [train_set_x[s] for s in sidx[n_train:]]
    valid_set_y = [train_set_y[s] for s in sidx[n_train:]]
    train_set_x = [train_set_x[s] for s in sidx[:n_train]]
    train_set_y = [train_set_y[s] for s in sidx[:n_train]]
    #
    # train_x = numpy.array(train_set_x)
    # valid_x = numpy.array(valid_set_x)
    # # print(train_x.shape)
    #
    train = (train_set_x, train_set_y)
    valid = (valid_set_x, valid_set_y)
    # test = (test_set_x, test_set_y)

    return train, valid #, test


import gp
import plotters
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import svm
train, valid = load_data(0)
data, target = train

from sklearn.preprocessing import label_binarize
y = label_binarize(target, classes=[0, 1, 2, 3, 4])

print(len(data), len(target), len(valid))

from sklearn.metrics import cohen_kappa_score, make_scorer
kappa_scorer = make_scorer(cohen_kappa_score)

def sample_loss(params):
    clf = svm.SVC(C=10 ** params[0], gamma=10 ** params[1], random_state=12345)
    return cross_val_score(clf, X=data, y=target, scoring=kappa_scorer, cv=8).mean()


lambdas = np.linspace(1, -4, 25)
gammas = np.linspace(1, -4, 20)

# print(lambdas)
# print(gammas)

# We need the cartesian combination of these two vectors
# param_grid = np.array([[C, gamma] for gamma in gammas for C in lambdas])
#
# print(param_grid)
# real_loss = [sample_loss(params) for params in param_grid]
#
# # The maximum is at:
# # print(param_grid[np.array(real_loss).argmax(), :])
#
# from matplotlib import rc
# import matplotlib.pyplot as plt
# rc('text', usetex=True)
#
# C, G = np.meshgrid(lambdas, gammas)
# plt.figure()
# cp = plt.contourf(C, G, np.array(real_loss).reshape(C.shape))
# plt.colorbar(cp)
# plt.title('Filled contours plot of loss function $\mathcal{L}$($\gamma$, $C$)')
# plt.xlabel('$C$')
# plt.ylabel('$\gamma')
# plt.savefig('/Users/ilham/Documents/gp-optimisation/figures/real_loss_contour.png', bbox_inches='tight')
# plt.show()

from matplotlib import rc
bounds = np.array([[-4, 1], [-4, 1]])

xp, yp = gp.bayesian_optimisation(n_iters=30,
                               sample_loss=sample_loss,
                               bounds=bounds,
                               n_pre_samples=3,
                               random_search=100000)


print(xp)
print(yp)
rc('text', usetex=False)
plotters.plot_iteration(lambdas, xp, yp, first_iter=3, second_param_grid=gammas, optimum=[0.58333333, -2.15789474])



