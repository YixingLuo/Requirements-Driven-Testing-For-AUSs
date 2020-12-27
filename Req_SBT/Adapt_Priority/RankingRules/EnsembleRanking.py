# -*- coding: utf-8 -*-

import numpy as np

def Ensemble_Ranking(violation_pattern_distance, violation_pattern_relation, violation_pattern_to_search, weights):
    violation_pattern_distance = np.array(violation_pattern_distance)
    violation_pattern_relation = np.array(violation_pattern_relation)
    violation_pattern_to_search = np.array(violation_pattern_to_search)
    # weights = [1, 1, 1]
    violation_pattern_list = []
    sorted_violation_pattern_list = []
    ranking_list = []
    for i in range (violation_pattern_to_search.shape[0]):
        violation_pattern = violation_pattern_to_search[i]
        for j in range (violation_pattern_distance.shape[0]):
            if (np.array(violation_pattern_distance[j]) == np.array(violation_pattern)).all():
                for k in range (violation_pattern_relation.shape[0]):
                    if (np.array(violation_pattern_relation[k]) == np.array(violation_pattern)).all():
                        # print(i,j,k)
                        violation_pattern_list.append(violation_pattern)
                        rank = i*weights[0] + j*weights[1] + k*weights[2]
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