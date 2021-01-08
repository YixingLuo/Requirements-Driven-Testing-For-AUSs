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
from Adapt_Priority.RankingRules.DistanceRanking import Distance_Ranking
from Adapt_Priority.RankingRules.EnsembleRanking import Ensemble_Ranking
from Adapt_Priority.RankingRules.RelationRanking import Relation_Ranking

target_value_threshold = [1, 0, 1, 1, 1, 0.9, 0.95]

priority_list = []
rank_list = []
with open("priority_list.csv") as csvfile:
    csv_file = csv.reader(csvfile)
    for row in csv_file:
        priority_list.append(row[:-1])
        rank_list.append(float(row[-1]))

    priority_list = [[float(x) for x in row] for row in priority_list]
    # rank_list = [[float(x) for x in row] for row in rank_list]
priority_list = np.array(priority_list)
rank_list = np.array(rank_list)

searched_violation_pattern = []
searched_violation_pattern.append(np.loadtxt("searched_violation_pattern_0.txt"))

pattern_count = np.zeros(priority_list.shape[0])

file_folder_orgin = os.path.abspath(os.path.join(os.getcwd())) + "/2021_01_07_Adapt_Priority_results_0"
evaluation = []
fileList = os.listdir(file_folder_orgin)
fileList.sort()
for i in range(len(fileList)):
# for i in range(20000):
    textname = file_folder_orgin + '/' + fileList[i]
    result = np.loadtxt(textname)
    evaluation.append(result)
    goal_flag = np.zeros((7), dtype=int)
    for j in range(7):
        if result[j] < target_value_threshold[j]:
            goal_flag[j] = 1
        else:
            goal_flag[j] = 0
    for j in range(priority_list.shape[0]):
        if (np.array(goal_flag) == priority_list[j]).all():
            pattern_count[j] = pattern_count[j] + 1
            break

variables = []
file_folder_orgin = os.path.abspath(os.path.join(os.getcwd())) + "/2021_01_07_Adapt_Priority_variable_0"
fileList = os.listdir(file_folder_orgin)
fileList.sort()
for i in range(len(fileList)):
    textname = file_folder_orgin + '/' + fileList[i]
    pop = np.loadtxt(textname)
    variables.append(pop)

violation_pattern_to_search = []
for j in range(priority_list.shape[0]):
    if pattern_count[j] == 0:
        violation_pattern_to_search.append(priority_list[j])
# print(np.array(violation_pattern_to_search).shape[0])

# print(variables, evaluation)

weight_dist, sorted_pattern_distance, sorted_pop, distance_ranking = Distance_Ranking(priority_list,
                                                                                      variables, evaluation,
                                                                                      target_value_threshold)
print(sorted_pattern_distance)
np.savetxt("sorted_pattern_distance_1.txt",sorted_pattern_distance, fmt="%d")
weight_relation, sorted_pattern_relation, relation_ranking = Relation_Ranking(violation_pattern_to_search,
                                                                              searched_violation_pattern,
                                                                              priority_list)

print(sorted_pattern_relation)
np.savetxt("sorted_pattern_relation_1.txt", sorted_pattern_relation, fmt="%d")
weights = [1, weight_dist, weight_relation]
violation_pattern_ranking, overall_rank_list = Ensemble_Ranking(distance_ranking, relation_ranking,
                                                                violation_pattern_to_search, weights)
print(violation_pattern_ranking)
np.savetxt("sorted_pattern_ranking_1.txt", violation_pattern_ranking, fmt="%d")
violation_pattern_ranking_removed = violation_pattern_ranking.copy()
for j in range(np.array(violation_pattern_ranking).shape[0]):
    for k in range(np.array(searched_violation_pattern).shape[0]):
        if (np.array(violation_pattern_ranking[j]) == np.array(searched_violation_pattern[k])).all():
            removed_item = violation_pattern_ranking[j]
            for ll in range(np.array(violation_pattern_ranking_removed).shape[0]):
                if (np.array(violation_pattern_ranking_removed[ll]) == np.array(removed_item)).all():
                    del violation_pattern_ranking_removed[ll]
                    break
            break

if np.array(violation_pattern_ranking_removed).shape[0] == 0:
    goal_selection_flag = np.ones(7)
else:
    goal_selection_flag = violation_pattern_ranking_removed[0]

searched_violation_pattern.append(goal_selection_flag)





target_pattern1 = sorted_pattern_distance[0]
target_pattern2 = sorted_pattern_relation[0]
target_pattern3 = violation_pattern_ranking[0]

# file_folder_orgin = os.path.abspath(os.path.join(os.getcwd())) + "/2021_01_08_Adapt_Priority_results_" + str(index)
# target_pattern = np.loadtxt("req_violation_pattern_" + str(index) + ".txt")

for k in range(priority_list.shape[0]):
    if (target_pattern1 == priority_list[k]).all():
        pattern_index1 = k
    if (target_pattern2 == priority_list[k]).all():
        pattern_index2 = k
    if (target_pattern3 == priority_list[k]).all():
        pattern_index3 = k

print(target_pattern1, target_pattern2, target_pattern3)

for i in range (9):
    pattern_count = np.loadtxt("pattern_count_" + str(i) + ".txt")
    print("distance", pattern_count[pattern_index1])

for i in range (9):
    pattern_count = np.loadtxt("pattern_count_" + str(i) + ".txt")
    print("relation", pattern_count[pattern_index2])

for i in range (9):
    pattern_count = np.loadtxt("pattern_count_" + str(i) + ".txt")
    print("overall", pattern_count[pattern_index3])

# result_list = []
# fileList = os.listdir(file_folder_orgin)
# fileList.sort()
# for i in range(len(fileList)):
# # for i in range(20000):
#     textname = file_folder_orgin + '/' + fileList[i]
#     result = np.loadtxt(textname)
#     violation_pattern = np.zeros((7), dtype = int)
#     result_list.append(result)
#     for j in range(len(violation_pattern)):
#         if result[j] < target_values[j]:
#             violation_pattern[j] = 1
#         else:
#             violation_pattern[j] = 0
#     if (target_pattern == violation_pattern).all():
#         print(textname)
