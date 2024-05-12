import math

import numpy as np
from numpy.linalg import eig
import pandas as pd
from scipy.linalg import sqrtm
from sklearn.metrics import roc_curve, auc
from scipy.spatial.distance import cityblock, mahalanobis, euclidean
import matplotlib.pyplot as plt
# 置信区间
import scipy.stats as st

userId = 30
data = pd.read_csv("{}.csv".format(userId))
column_titles = data.columns.tolist()
# convert to microsecond from second
# if already second，no need
# data.iloc[:, 2:] = data.iloc[:, 2:].multiply(1.0e07)

subjects = data["UserID"].unique()


def is_nan(value):
    return math.isnan(float(value))


def filter_numbers(lst, threshold):
    return list(map(lambda x: threshold if is_nan(x) or x < threshold else x, lst))


def evaluateEER(user_scores, imposter_scores):
    labels = [0]*len(user_scores) + [1]*len(imposter_scores)
    fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    missrates = 1 - tpr
    farates = fpr
    dists = missrates - farates
    idx1 = np.argmin(dists[dists >= 0])
    idx2 = np.argmax(dists[dists < 0])
    x = [missrates[idx1], farates[idx1]]
    y = [missrates[idx2], farates[idx2]]
    a = ( x[0] - x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
    eer = x[0] + a * ( y[0] - x[0] )
    return eer


def evaluatefpr(user_scores, imposter_scores):
    labels = [0]*len(user_scores) + [1]*len(imposter_scores) # 分别计算两个集合的大小
    fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    return fpr


def evaluatetpr(user_scores, imposter_scores):
    labels = [0]*len(user_scores) + [1]*len(imposter_scores) # 分别计算两个集合的大小
    fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    return tpr


def ROCPlot(rst,algorithm_name):
    fpr1 = rst[2][1]
    tpr1 = rst[3][1]
    FT = np.array((fpr1, tpr1)).T
    data = pd.DataFrame(FT)
    roc_auc1 = auc(fpr1, tpr1)
    plt.plot(fpr1, tpr1, 'k--', label='Linux Command dataset (ROC area = {0:.2f})'.format(roc_auc1), lw=2)

    plt.xlim([-0.05, 1.05])  # 设置x、y轴的上下限，以免和边缘重合，更好的观察图像的整体
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')  # 可以使用中文，但需要导入一些库即字体
    plt.title(algorithm_name)
    plt.legend(loc="lower right")
    plt.show()


class ManhattanScaledDetector:

    def __init__(self, user_id):

        self.user_scores = []
        self.imposter_scores = []
        self.mean_vector = []
        self.mad_vector = []
        self.userID = user_id

    def training(self):
        self.mean_vector = self.train.mean().values
        # self.mad_vector = self.train.mad().values

        # Calculate the mean for each column
        this_df = pd.DataFrame(self.train)
        mean_values = this_df.mean()

        # Calculate the absolute deviations from the mean for each element in the DataFrame
        absolute_deviations = this_df.subtract(mean_values).abs()

        # Calculate the mean of these absolute deviations for each column, giving you the MAD
        self.mad_vector = absolute_deviations.mean()

    def testing(self):
        for i in range(self.test_genuine.shape[0]):
            cur_score = 0
            for j in range(len(self.mean_vector)):
                denominator = self.mad_vector[j]
                if is_nan(denominator) or abs(denominator) < 0.003:
                    # denominator = denominator/abs(denominator) # if denominator == 0 then trouble
                    denominator = 0.003
                cur_score = cur_score + \
                            abs(self.test_genuine.iloc[i].values[j] - \
                                self.mean_vector[j]) / denominator
            self.user_scores.append(cur_score)

        for i in range(self.test_imposter.shape[0]):
            cur_score = 0
            for j in range(len(self.mean_vector)):
                denominator = self.mad_vector[j]
                if is_nan(denominator) or abs(denominator) < 0.003:
                    # denominator = denominator/abs(denominator) # if denominator == 0 then trouble
                    denominator = 0.003
                cur_score = cur_score + \
                            abs(self.test_imposter.iloc[i].values[j] - \
                                self.mean_vector[j]) / denominator
            self.imposter_scores.append(cur_score)

    def evaluate(self):

        self.user_scores = []
        self.imposter_scores = []

        # Consider current subject as genuine and rest as imposters
        genuine_user_data = data.loc[data.UserID == self.userID, column_titles[2]:]
        imposter_data = data.loc[data.UserID != self.userID, :]

        # genuine user's first half vectors for training
        half_gud = len(genuine_user_data)//2
        self.train = genuine_user_data.iloc[0:half_gud]

        # True set (half records)
        self.test_genuine = genuine_user_data.iloc[half_gud:]

        # False set (first three records)
        self.test_imposter = imposter_data.groupby("UserID").head(3).loc[:, column_titles[2]:]

        self.training()
        self.testing()

        eer = evaluateEER(self.user_scores, self.imposter_scores)
        print(eer)
        fpr = evaluatefpr(self.user_scores, self.imposter_scores)
        tpr = evaluatetpr(self.user_scores, self.imposter_scores)

        return eer, fpr, tpr

for i in range(2000):
    print(i)
    result3 = ManhattanScaledDetector(userId).evaluate()
    # print(result3[0])

    data_eers = {'UserID': [str(userId)], 'eer': [result3[0]]}
    df = pd.DataFrame(data_eers)

    # 将DataFrame写入CSV文件
    file_path = "mht_eer_{}.csv".format(userId)  # 指定文件路径
    df.to_csv(file_path, index=False)  # 将DataFrame写入CSV文件

    print("mht user eer calculating and saving completed!")






