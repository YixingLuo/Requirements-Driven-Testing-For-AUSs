import sys
sys.path.append("..")
import json
import numpy as np
import random
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
import csv

target_value_threshold = [1, 0, 1, 1, 1, 0.95, 0.99]

priority_list = []
with open("priority_list.csv") as csvfile:
    csv_file = csv.reader(csvfile)
    for row in csv_file:
        priority_list.append(row)
    priority_list = [[float(x) for x in row] for row in priority_list]
priority_list = np.array(priority_list)

result_list = []
pattern_count = np.zeros(priority_list.shape[0])
goal_selection_index = np.loadtxt("goal_selection_index.txt")
for i in range (1):
    # file_folder_orgin = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_12_27_Brute_Froce_results_" + str(int(goal_selection_index[i]))
    file_folder_orgin = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_12_27_Brute_Froce_results_" + str(0)
    fileList = os.listdir(file_folder_orgin)
    fileList.sort()
    for k in range(len(fileList)):
        textname = file_folder_orgin + '/' + fileList[i]
        result = np.loadtxt(textname)
        result_list.append(list(result))
        goal_flag = np.zeros((7), dtype=int)
        for j in range(7):
            if abs(result[j]) < target_value_threshold[j]:
                goal_flag[j] = 1
            else:
                goal_flag[j] = 0
        for j in range(priority_list.shape[0]):
            if (np.array(goal_flag) == priority_list[j]).all():
                pattern_count[j] = pattern_count[j] + 1
                break

print(pattern_count, sum(pattern_count))
criticality = 0
for i in range(priority_list.shape[0]):
    criticality = criticality + (priority_list.shape[0]-1-i)/(priority_list.shape[0]-1) * pattern_count[i]

print(criticality/sum(pattern_count))

# print(count_list)

## plot
# print(result_list)
# sns.set_style("darkgrid")
# data = DataFrame(result_list)
# # data.rename(columns={0:'a',1:'b',2:'c',3:'d',4:'e'},inplace=True)#注意这里0和1都不是字符串
# data.dropna(axis=0,how='any')
# print(data)
# sns.distplot(data['a'])
# plt.show()
# print(data.corr())
# sns.pairplot(data)
# # sns.pairplot(data , markers=["o", "s"])
# sns.heatmap(data.corr())
# plt.show()
# sns.clustermap(data.corr())
# g = sns.PairGrid(data)
# g.map_diag(sns.distplot)
# g.map_upper(plt.scatter)
# g.map_lower(sns.kdeplot)
# # sns.distplot(data['0'])
# plt.show()



# sns.set_style("darkgrid")
# fig,axes = plt.subplots(1,2)
# sns.displot(sum_list_orgin, kde = False, ax = axes[0])
# sns.displot(sum_list_adapt, kde = False, ax = axes[1])

# sns.displot(sum_list)
# sns.histplot(sum_list)
# plt.show()
# current_palette = sns.color_palette("hls",12)
# sns.boxplot(data=sum_list,palette=current_palette) #使用颜色就是传递参数给palette
# plt.show()


##count the number
# se = pd.Series(sum_list_orgin)
# countDict = dict(se.value_counts())
# proportitionDict = dict(se.value_counts(normalize=True))
# print(countDict)
# print(proportitionDict)
# se = pd.Series(sum_list_adapt)
# countDict = dict(se.value_counts())
# proportitionDict = dict(se.value_counts(normalize=True))
# print(countDict)

