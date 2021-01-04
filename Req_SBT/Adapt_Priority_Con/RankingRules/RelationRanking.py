# -*- coding: utf-8 -*-

import numpy as np
import math
import os
import csv

# priority_list = []
# with open("priority_list.csv") as csvfile:
#     csv_file = csv.reader(csvfile)
#     for row in csv_file:
#         priority_list.append(row)
#     priority_list = [[float(x) for x in row] for row in priority_list]
# priority_list = np.array(priority_list)

def Relation (priority_list):
    pattern_num = np.array(priority_list).shape[0]
    goal_num = np.array(priority_list).shape[1]
    parent_list = np.zeros((pattern_num, pattern_num), dtype=int)
    child_list = np.zeros((pattern_num, pattern_num), dtype=int)

    for i in range (pattern_num):
        father = priority_list[i]
        for j in range (pattern_num):
            child = priority_list[j]
            count_same = 0
            large_flag = 0
            for k in range (goal_num):
                if father[k] == child[k]:
                    count_same = count_same + 1
                elif father[k] > child[k]:
                    large_flag = 1

            if (count_same == goal_num - 1) and large_flag == 1:
                parent_list[j][i] = 1
                child_list[i][j] = 1

    return parent_list, child_list


# def Relation_Ranking (violation_pattern_to_search, searched_violation_pattern, priority_list):
#     parent_list, child_list = Relation (priority_list)
#     sorted_violation_pattern_list = []
#     gamma = 0.5
#     pattern_num = np.array(priority_list).shape[0]
#     goal_num = np.array(priority_list).shape[1]
#
#     reward = np.zeros((pattern_num), dtype=float)
#     count_violation = np.sum(priority_list, axis=1)
#
#
#     for i in range (pattern_num):
#         ancessor_list = []
#         father_index = []
#         for j in range (pattern_num):
#             if parent_list[i][j] == 1:
#                 father_index.append(j)
#                 ancessor_list.append(priority_list[j])
#
#         if len(father_index) > 0:
#             existing_pattern = 0
#             for j in range (len(father_index)):
#                 for k in range (np.array(violation_pattern_to_search).shape[0]):
#                     if (np.array(ancessor_list[j]) == np.array(violation_pattern_to_search[k])).all():
#                         existing_pattern = existing_pattern + 1
#                         break
#             reward[i] = (len(father_index) - existing_pattern)/len(father_index)
#
#
#     for i in range (np.array(searched_violation_pattern).shape[0]):
#         reward_0 = 1 ## have been searched patterns
#         for j in range (np.array(violation_pattern_to_search).shape[0]):
#             if (np.array(searched_violation_pattern[i]) == np.array(violation_pattern_to_search[j])).all():
#                 reward_0 = -1
#                 break
#
#         for j in range (pattern_num):
#             if (np.array(searched_violation_pattern[i]) == np.array(priority_list[j])).all():
#                 goal_selection_flag_index = j
#                 reward[goal_selection_flag_index] = reward[goal_selection_flag_index] + reward_0
#                 break
#
#         if reward_0 == -1:
#             initial_class = sum(searched_violation_pattern[i])
#             for j in range (pattern_num):
#                 if count_violation[j] < initial_class:
#                     reward[j] = reward[j] + reward_0 * np.power(gamma, (initial_class - count_violation[j]))
#
#     sorted_reward = np.argsort(reward)
#     # print(reward, sorted_reward)
#     for i in range (np.array(sorted_reward).shape[0]):
#         index = sorted_reward[np.array(sorted_reward).shape[0]-1-i]
#         for j in range (np.array(violation_pattern_to_search).shape[0]):
#             if (np.array(priority_list[index]) == np.array(violation_pattern_to_search[j])).all():
#                 sorted_violation_pattern_list.append(violation_pattern_to_search[j])
#                 break
#
#     weight_relation = 1
#
#     return weight_relation, sorted_violation_pattern_list


def Relation_Ranking (violation_pattern_to_search, searched_violation_pattern, priority_list):
    parent_list, child_list = Relation (priority_list)
    sorted_violation_pattern_list = []
    gamma = 0.5
    pattern_num = np.array(priority_list).shape[0]
    goal_num = np.array(priority_list).shape[1]

    reward = np.zeros((pattern_num), dtype=float)
    count_violation = np.sum(priority_list, axis=1)


    for i in range (pattern_num):
        ancessor_list = []
        father_index = []
        for j in range (pattern_num):
            if parent_list[i][j] == 1:
                father_index.append(j)
                ancessor_list.append(priority_list[j])

        if len(father_index) > 0:
            existing_pattern = 0
            for j in range (len(father_index)):
                for k in range (np.array(violation_pattern_to_search).shape[0]):
                    if (np.array(ancessor_list[j]) == np.array(violation_pattern_to_search[k])).all():
                        existing_pattern = existing_pattern + 1
                        break
            reward[i] = (len(father_index) - existing_pattern)/len(father_index)


    for i in range (np.array(searched_violation_pattern).shape[0]):
        reward_0 = 1 ## have been searched patterns
        for j in range (np.array(violation_pattern_to_search).shape[0]):
            if (np.array(searched_violation_pattern[i]) == np.array(violation_pattern_to_search[j])).all():
                reward_0 = -1
                break

        for j in range (pattern_num):
            if (np.array(searched_violation_pattern[i]) == np.array(priority_list[j])).all():
                goal_selection_flag_index = j
                reward[goal_selection_flag_index] = reward[goal_selection_flag_index] + reward_0
                break

        if reward_0 == -1:
            initial_class = sum(searched_violation_pattern[i])
            for j in range (pattern_num):
                if count_violation[j] < initial_class:
                    reward[j] = reward[j] + reward_0 * np.power(gamma, (initial_class - count_violation[j]))

    sorted_reward = np.sort(list(set(reward)))

    relation_ranking = np.zeros((np.array(priority_list).shape[0]), dtype= int)
    count = 1
    for i in range (len(sorted_reward)):
        same_number = 0
        for j in range (len(reward)):
            if reward[j] == sorted_reward[i]:
                sorted_violation_pattern_list.append(priority_list[j])
                relation_ranking[j] = count
                same_number = same_number + 1
        count = count + same_number

    weight_relation = 1

    return weight_relation, sorted_violation_pattern_list, relation_ranking

if __name__ == '__main__':


    searched_violation_pattern = [[1, 1, 1], [1, 0, 1]]
    priority_list = [[1, 1, 1], [0, 1, 1], [1, 0, 1], [0, 0, 1], [1, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0]]
    violation_pattern_to_search = [[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0]]
    sorted_violation_pattern_relation = Relation_Ranking (violation_pattern_to_search, searched_violation_pattern, priority_list)
    print(sorted_violation_pattern_relation )