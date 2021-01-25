# -*- coding: utf-8 -*-

import numpy as np
import math
import os
import csv

# target_value_threshold = [1, 0, 1, 1, 1, 0.95, 0.99]


# def Distance_Ranking (violation_pattern_to_search, population, scores):
#     sorted_violation_pattern_list = []
#     sorted_pop = np.zeros((np.array(violation_pattern_to_search).shape[0], np.array(population).shape[0], np.array(population).shape[1]),dtype=float)
#     distance = np.zeros((np.array(violation_pattern_to_search).shape[0], np.array(population).shape[0]),dtype=float)
#
#
#     for i in range (np.array(violation_pattern_to_search).shape[0]):
#
#         for j in range (np.array(population).shape[0]):
#             violation_pattern = violation_pattern_to_search[i]
#             dist = np.zeros((np.array(violation_pattern).shape[0]),dtype=float)
#             sum_dist = 0
#
#             for k in range (np.array(violation_pattern).shape[0]):
#                 if violation_pattern[k] == 0: ## satisfied
#                     if scores[j][k] >= target_value_threshold[k]:
#                         dist[k] = 0
#                     else:
#                         dist[k] = max(target_value_threshold[k] - scores[j][k], 0)
#                 else: ## violated
#                     if scores[j][k] < target_value_threshold[k]:
#                         dist[k] = 0
#                     else:
#                         dist[k] = max(scores[j][k] - target_value_threshold[k], 0)
#
#                 sum_dist += dist[k]*dist[k]
#
#             distance[i][j] = math.sqrt(sum_dist)
#
#     dist_mean = distance.mean(axis=1)
#     sorted_dist_mean = np.argsort(dist_mean)
#     for i in range (np.array(sorted_dist_mean).shape[0]):
#         index = sorted_dist_mean[i]
#         sorted_violation_pattern_list.append(violation_pattern_to_search[index])
#
#     # distance = distance.T
#     for i in range (np.array(violation_pattern_to_search).shape[0]):
#         sorted_pop_index = np.argsort(distance[i])
#         for j in range (np.array(sorted_pop_index).shape[0]):
#             sorted_pop[i][j] = population[sorted_pop_index[j]]
#
#     weight_dist = 1
#
#     return weight_dist, sorted_violation_pattern_list, sorted_pop


def Distance_Ranking (priority_list, population, scores, target_value_threshold):
    sorted_violation_pattern_list = []
    # print(np.array(population).shape[0], np.array(population).shape[1])
    # print(np.array(scores).shape[0], np.array(scores).shape[1])
    sorted_pop = np.zeros((np.array(priority_list).shape[0], np.array(population).shape[0], np.array(population).shape[1]),dtype=float)
    distance = np.zeros((np.array(priority_list).shape[0], np.array(population).shape[0]),dtype=float)


    for i in range (np.array(priority_list).shape[0]):

        for j in range (np.array(population).shape[0]):
            violation_pattern = priority_list[i]
            dist = np.zeros((np.array(violation_pattern).shape[0]),dtype=float)
            sum_dist = 0

            for k in range (np.array(violation_pattern).shape[0]):
                if violation_pattern[k] == 0: ## satisfied
                    if scores[j][k] >= target_value_threshold[k]:
                        dist[k] = 0
                    else:
                        dist[k] = abs(target_value_threshold[k] - scores[j][k])
                        dist[k] = dist[k] / (dist[k] + 1)
                else: ## violated
                    if scores[j][k] < target_value_threshold[k]:
                        dist[k] = 0
                    else:
                        dist[k] = abs(target_value_threshold[k] - scores[j][k])
                        dist[k] = dist[k] / (dist[k] + 1)

                sum_dist += dist[k]*dist[k]

            distance[i][j] = math.sqrt(sum_dist)


    ## top 2500
    dist_mean = np.zeros(np.array(priority_list).shape[0])

    for i in range(np.array(priority_list).shape[0]):
        sorted_pop_index = np.argsort(distance[i])
        for j in range(np.array(sorted_pop_index).shape[0]):
            sorted_pop[i][j] = population[sorted_pop_index[j]]
        sum_dist = 0
        for j in range(2500):
            sum_dist += distance[i][sorted_pop_index[j]]
        dist_mean[i] = sum_dist/2500
    sorted_dist_mean = np.sort(list(set(dist_mean)))
    distance_ranking = np.zeros((np.array(priority_list).shape[0]), dtype=int)
    count = 1
    for i in range(len(sorted_dist_mean)):
        same_number = 0
        for j in range(len(dist_mean)):
            if dist_mean[j] == sorted_dist_mean[i]:
                sorted_violation_pattern_list.append(priority_list[j])
                distance_ranking[j] = count
                same_number = same_number + 1
        count = count + same_number

    weight_dist = 1

    # dist_mean = distance.mean(axis=1)
    # sorted_dist_mean = np.sort(list(set(dist_mean)))
    # distance_ranking = np.zeros((np.array(priority_list).shape[0]), dtype= int)
    # count = 1
    # for i in range (len(sorted_dist_mean)):
    #     same_number = 0
    #     for j in range (len(dist_mean)):
    #         if dist_mean[j] == sorted_dist_mean[i]:
    #             sorted_violation_pattern_list.append(priority_list[j])
    #             distance_ranking[j] = count
    #             same_number = same_number + 1
    #     count = count + same_number
    #
    # for i in range (np.array(priority_list).shape[0]):
    #     sorted_pop_index = np.argsort(distance[i])
    #     for j in range (np.array(sorted_pop_index).shape[0]):
    #         sorted_pop[i][j] = population[sorted_pop_index[j]]
    #
    # weight_dist = 1

    return weight_dist, sorted_violation_pattern_list, sorted_pop, distance_ranking, dist_mean

if __name__ == '__main__':
    # violation_pattern = np.array([[1,1,1],[2,2,2]])
    # print(violation_pattern, violation_pattern.mean(axis=1))

    target_value_threshold = [1, 1, 1, 1, 1, 1, 1]
    priority_list = []
    with open("../priority_list.csv") as csvfile:
        csv_file = csv.reader(csvfile)
        for row in csv_file:
            priority_list.append(row[0:-1])
        priority_list = [[float(x) for x in row] for row in priority_list]
    priority_list = np.array(priority_list)

    violation_pattern_to_search = []
    # print(priority_list.shape[0])
    len_priority_list = priority_list.shape[0]
    pattern_count = np.zeros((priority_list.shape[0]), dtype=int)

    evaluation = []
    variables = []

    vars_file_name = "../2020_12_24_NSGA_III_variable_20000"
    results_file_name = "../2020_12_24_NSGA_III_results_20000"
    fileList = os.listdir(results_file_name)
    fileList.sort()
    for i in range(3):
        textname = results_file_name + '/' + fileList[i]
        # print(textname)
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
                pattern_count[j] += pattern_count[j] + 1
                break
    # print(pattern_count,evaluation)
    fileList = os.listdir(vars_file_name)
    fileList.sort()
    for i in range(3):
        textname = vars_file_name + '/' + fileList[i]
        pop = np.loadtxt(textname)
        variables.append(pop)

    violation_pattern_to_search = []
    for j in range(priority_list.shape[0]):
        if pattern_count[j] == 0:
            violation_pattern_to_search.append(priority_list[j])

    # print(violation_pattern_to_search,pattern_count)

    [sorted_violation_pattern_list, sorted_pop] = Distance_Ranking(violation_pattern_to_search,
                                                                                          variables, evaluation, target_value_threshold)
    print(np.array(sorted_violation_pattern_list).shape, sorted_pop.shape)