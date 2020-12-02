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

file_folder_orgin = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_12_01_NSGA_II_results_10000"
file_folder_adapt = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/2020_11_30_NSGAII_results_10000"

sum_list_orgin = []
fileList = os.listdir(file_folder_orgin)
fileList.sort()
for i in range(len(fileList)):
    textname = file_folder_orgin + '/' + fileList[i]
    # print(textname)
    result = np.loadtxt(textname)
    sum = 0
    for j in range(len(result)):
        if result[j] == 1:
            sum += result[j] * np.power(2, j)
    sum_list_orgin.append(sum)


sum_list_adapt = []
fileList = os.listdir(file_folder_adapt)
fileList.sort()
for i in range(len(fileList)):
    textname = file_folder_adapt + '/' + fileList[i]
    # print(textname)
    result = np.loadtxt(textname)
    sum = 0
    for j in range(len(result)):
        if result[j] == 1:
            sum += result[j] * np.power(2, j)
    sum_list_adapt.append(sum)

# num_files = 0

# for fn in os.listdir(file_folder):
#     num_files += 1

# print(num_files)
# num_files = 70
# my_data = np.zeros((num_files,50,7))
# req_flag = np.zeros((num_files,50,6))
# for fn in range(num_files):
#     file_name = file_folder + "/result-" + str(fn) + '-49.txt'
#     my_data[fn] = np.loadtxt(file_name)




# print(my_data.shape)
# for i in range(num_files):
#     for j in range(50):
#         for k in range (7):
#             if k == 1:
#                 continue
#             else:
#                 if my_data[i][j][k]<1:
#                     req_flag[i][j][max(0,k-1)] = 0
#                 else:
#                     req_flag[i][j][max(0,k-1)] = 1
#         # temp = np.array([0,0,0,0,0,0])
#         # print(req_flag[i][j])
#         if req_flag[i][j].any() == 0:
#             print("$$$")


#
# for i in range(num_files):
#     for j in range(50):
#         sum = 0
#         for k in range (6):
#             sum += req_flag[i][j][k]*np.power(2,k)
#         sum_list.append(sum)
#
# print(len(sum_list))


sns.set_style("darkgrid")
fig,axes = plt.subplots(1,2)
sns.displot(sum_list_orgin, kde = False, ax = axes[0])
sns.displot(sum_list_adapt, kde = False, ax = axes[1])

# sns.displot(sum_list)
# sns.histplot(sum_list)
# plt.show()
# current_palette = sns.color_palette("hls",12)
# sns.boxplot(data=sum_list,palette=current_palette) #使用颜色就是传递参数给palette
plt.show()


##count the number
se = pd.Series(sum_list_orgin)
countDict = dict(se.value_counts())
proportitionDict = dict(se.value_counts(normalize=True))
print(countDict)
print(proportitionDict)
se = pd.Series(sum_list_adapt)
countDict = dict(se.value_counts())
proportitionDict = dict(se.value_counts(normalize=True))
print(countDict)