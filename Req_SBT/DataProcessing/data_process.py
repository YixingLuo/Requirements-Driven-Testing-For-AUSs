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

file_folder_orgin = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_12_10_NSGA_III_results_10000"
# file_folder_adapt = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_11_30_NSGAII_results_10000"

sum_list_orgin = []
result_list = []
fileList = os.listdir(file_folder_orgin)
fileList.sort()
for i in range(len(fileList)):
    textname = file_folder_orgin + '/' + fileList[i]
    # print(textname)
    result = np.loadtxt(textname)
    sum = 0
    # flag = 0
    # for j in range(len(result)):
    # 	if not (result[j] >=0 and result[j] <= 1):
    #         flag = 1
    # 		break
    # if not flag:
    # result_new = [result[0],result[1],result[2],result[3],result[5]]
    # if result[-3]<1:
        # print (textname)
    result_list.append(list(result))
    # for j in range(len(result)):
    if result[0] == -1:
        sum += np.power(2, 0)
    if result[1] < 1:
        sum += np.power(2, 1)
    if result[2] < 1:
        sum += np.power(2, 2)
    if result[3] < 1:
        sum += np.power(2, 3)
    if result[4] < 1:
        sum += np.power(2, 4)
    if result[5] < 0.95:
        sum += np.power(2, 5)
    if result[6] < 0.95:
        sum += np.power(2, 6)
    sum_list_orgin.append(sum)


##count the number

count_list = np.zeros(np.power(2, 7))
for i in range (np.power(2, 7)):
    count = sum_list_orgin.count(i)
    # print(i,count,count_list)
    count_list[i] = count
    print(count)


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

