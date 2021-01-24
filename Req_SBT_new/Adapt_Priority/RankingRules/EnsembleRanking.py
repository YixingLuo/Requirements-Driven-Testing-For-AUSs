# -*- coding: utf-8 -*-

import numpy as np
import csv
# def Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search, weights):
#     violation_pattern_distance = np.array(violation_pattern_distance)
#     violation_pattern_relation = np.array(violation_pattern_relation)
#     violation_pattern_to_search = np.array(violation_pattern_to_search)
#     # weights = [1, 1, 1]
#     violation_pattern_list = []
#     sorted_violation_pattern_list = []
#     ranking_list = []
#     for i in range (violation_pattern_to_search.shape[0]):
#         violation_pattern = violation_pattern_to_search[i]
#         for j in range (violation_pattern_distance.shape[0]):
#             if (np.array(violation_pattern_distance[j]) == np.array(violation_pattern)).all():
#                 for k in range (violation_pattern_relation.shape[0]):
#                     if (np.array(violation_pattern_relation[k]) == np.array(violation_pattern)).all():
#                         # print(i,j,k)
#                         violation_pattern_list.append(violation_pattern)
#                         rank = i*weights[0] + j*weights[1] + k*weights[2]
#                         ranking_list.append(rank)
#
#     sorted_ranking_list = np.argsort(ranking_list)
#     for i in range (np.array(sorted_ranking_list).shape[0]):
#         index = sorted_ranking_list[i]
#         sorted_violation_pattern_list.append(violation_pattern_list[index])
#
#     return sorted_violation_pattern_list

def Ensemble_Ranking(distance_rank, relation_rank, violation_pattern_to_search, weights):
    priority_list = []
    rank_list = []
    with open("priority_list.csv") as csvfile:
        csv_file = csv.reader(csvfile)
        for row in csv_file:
            priority_list.append(row[0:-1])
            rank_list.append(float(row[-1]))
        priority_list = [[float(x) for x in row] for row in priority_list]
    priority_list = np.array(priority_list)
    # weights = [1, 1, 1]

    overall_rank = np.zeros(len(distance_rank), dtype=float)
    overall_rank_list_new = []

    for i in range (len(distance_rank)):
        overall_rank[i] = distance_rank[i] * weights[0] + relation_rank[i] * weights[1] + rank_list[i] * weights[2]

    sorted_overall_rank = np.sort(list(set(overall_rank)))

    sorted_violation_pattern_list = []

    for i in range(len(sorted_overall_rank)):
        for j in range(np.array(priority_list).shape[0]):
            if overall_rank[j] == sorted_overall_rank[i]:
                for k in range(len(violation_pattern_to_search)):
                    if (np.array(priority_list[j]) == violation_pattern_to_search[k]).all():
                        sorted_violation_pattern_list.append(violation_pattern_to_search[k])
                        overall_rank_list_new.append([distance_rank[j], relation_rank[j], rank_list[j], overall_rank[j]])

    return sorted_violation_pattern_list, overall_rank_list_new


def Ensemble_Ranking2(violation_pattern_distance, violation_pattern_to_search):
    violation_pattern_distance = np.array(violation_pattern_distance)
    violation_pattern_to_search = np.array(violation_pattern_to_search)
    weights = [1, 1]
    violation_pattern_list = []
    sorted_violation_pattern_list = []
    ranking_list = []
    for i in range (violation_pattern_to_search.shape[0]):
        violation_pattern = violation_pattern_to_search[i]
        for j in range (violation_pattern_distance.shape[0]):
            if (np.array(violation_pattern_distance[j]) == np.array(violation_pattern)).all():
                        # print(i,j,k)
                    violation_pattern_list.append(violation_pattern)
                    rank = i*weights[0] + j*weights[1]
                    ranking_list.append(rank)

    sorted_ranking_list = np.argsort(ranking_list)
    # print(sorted_ranking_list,np.array(sorted_ranking_list).shape[0])
    for i in range (np.array(sorted_ranking_list).shape[0]):
        index = sorted_ranking_list[i]
        sorted_violation_pattern_list.append(violation_pattern_list[index])

    # sorted_ranking_list = [np.lexsort(np.array(ranking_list).T)]## sort as the last column
    # for i in range (np.array(sorted_ranking_list).shape[0]):
    #     index = sorted_ranking_list [i][0]
    #     sorted_violation_pattern_list.append(violation_pattern_list[index])



    return sorted_violation_pattern_list

if __name__ == '__main__':

    violation_pattern_to_search = [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
    violation_pattern_distance = [[1, 0, 1], [0, 1, 1], [1, 1, 1]]
    violation_pattern_relation = [[0, 1, 1], [1, 0, 1], [1, 1, 1]]

    sorted_violation_pattern_list = Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search)
    print(sorted_violation_pattern_list)