import wfdb
import rr_features
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_scatter3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(x)):
        if (y[i] == 0):  #"N"):
            c = 'b'
        elif (y[i] == 1):  #"~"):
            c = 'y'
        elif (y[i] == 2):  #"V"):
            c = 'r'
        elif (y[i] == 3):  #"x"):
            c = 'm'
        elif (y[i] == 4):  #"A"):
            c = 'g'
        else:
            c = 'k'

        ax.scatter(rrf.rrs[i].feature[0], rrf.rrs[i].feature[1], rrf.rrs[i].feature[2], c=c)

    ax.set_xlabel('X = prev')
    ax.set_ylabel('Y = next')
    ax.set_zlabel('Z = local_avg')

    plt.show()


def plot_svm():
    h = .02  # step size in the mesh
    x_min = 0
    x_max = 1
    y_min = 0
    y_max = 1

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    for i, clf in enumerate((model, model2)):
        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        plt.subplot(2, 2, i + 1)
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)


        # Plot also the training points
        plt.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.coolwarm)
        plt.xlabel('Sepal length')
        plt.ylabel('Sepal width')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title("titles[i]")
    plt.show()



ann = wfdb.rdann('mitbih/200', 'atr')

rrf = rr_features.RR_features(ann.annsamp, 360)
rrf.set_label(ann.anntype)
rrf.calc_features()
rrf.calc_rrir()
rrf.calc_10rrir()
# rrf.print_features()
rrf.normalize()

x = np.empty(shape=(len(rrf.rrs), 5))
y = []

for i in range(len(x)):
    x[i] = [rrf.rrs[i].feature[0], rrf.rrs[i].feature[1], rrf.rrs[i].feature[2], rrf.rrs[i].feature[4], rrf.rrs[i].feature[5]] #rrf.rrs[i].feature #[rrf.rrs[i].feature[0], rrf.rrs[i].feature[1], rrf.rrs[i].feature[2]]
    y.append(rrf.rrs[i].label)
    # print("[" + repr(i) + "] " + repr(y[i]))

# model = SVC(decision_function_shape='ovo', C=100, gamma=1).fit(x, y)
# model2 = SVC(kernel='poly', degree=5, C=100).fit(x, y)
model3 = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0).fit(x, y)
# model4 = KNeighborsClassifier(20).fit(x, y)
model5 = GaussianNB().fit(x, y)
model6 = DecisionTreeClassifier().fit(x, y)
test = [x[0], x[1], x[2], x[2699], x[2788], x[2604], x[2579], x[2555], x[2556], x[2544]]

# print(test)
print("Tes  [" + repr(y[0]) + " " + repr(y[1]) + " " + repr(y[2]) + " " + repr(y[2699]) + " " + repr(y[2788]) + " " +
      repr(y[2604]) + " " + repr(y[2579]) + " " + repr(y[2555]) + " " + repr(y[2556]) + " " + repr(y[2544]) +"]")
# print("SVM " , model2.predict(test))
# print("SVM " , model.predict(test))
# print("KNN " , model4.predict(test))
print("NBC ", model5.predict(test))
print("RFC " , model3.predict(test))
start_time = time.time()
print("DTC ", model6.predict(test))
print("--- %s miliseconds ---" % ((time.time() - start_time) * 1000))


# print("x: " + repr(len(x)) + " - y: " + repr(len(y)))

# plot_scatter3D()

# plot_svm()