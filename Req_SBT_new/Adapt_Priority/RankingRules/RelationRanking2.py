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

def check_relation (pattern1, pattern2):
    large_flag = 0
    for k in range(len(pattern1)):
        if pattern1[k] < pattern2[k]:
            large_flag = 1
            break
    if large_flag == 1:
        return False
    else:
        return True


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

    reward = np.ones((pattern_num), dtype=float)
    pattern_class = np.sum(priority_list, axis=1)
    found_index = []
    unfound_index = []
    searched_unfound_index = []
    unsearch_unfound_index = []

    for i in range (np.array(violation_pattern_to_search).shape[0]):
        for j in range(np.array(priority_list).shape[0]):
            if (np.array(violation_pattern_to_search[i]) == np.array(priority_list[j])).all():
                my_index = j ## not found
                break
        unfound_index.append(my_index)
        reward[my_index] = 0

    for i in range (pattern_num):
        if i in unfound_index:
            pass
        else:
            found_index.append(i)

    for i in range (np.array(searched_violation_pattern).shape[0]):
        for j in range (np.array(violation_pattern_to_search).shape[0]):
            if (np.array(searched_violation_pattern[i]) == np.array(violation_pattern_to_search[j])).all():
                my_index = j  ## searched and not found
                break
        searched_unfound_index.append(my_index)
        reward[my_index] = -1

    for i in range(len(unfound_index)):
        if unfound_index[i] in searched_unfound_index:
            pass
        else:
            unsearch_unfound_index.append(unfound_index[i])

    # print("found_index:", found_index, len(found_index))
    # print("unfound_index:", unfound_index, len(unfound_index))
    # print("searched_unfound_index:", searched_unfound_index, len(searched_unfound_index))
    # print("unsearch_unfound_index:", unsearch_unfound_index, len(unsearch_unfound_index))


    for i in range(len(found_index)):
        father_index = found_index[i]
        initial_class = sum(priority_list[my_index])
        for j in range (len(unsearch_unfound_index)):
            child_index =unsearch_unfound_index[j]
            if check_relation(priority_list[father_index], priority_list[child_index]):
                # print("father and child", priority_list[father_index], priority_list[child_index])
                reward[child_index] = reward[child_index] + reward[father_index] * np.power(gamma, (pattern_class[father_index] - pattern_class[child_index]))



    for i in range (len(searched_unfound_index)):
        father_index = searched_unfound_index[i]
        initial_class = sum (priority_list[my_index])
        for j in range (len(unsearch_unfound_index)):
            child_index = unsearch_unfound_index[j]
            if check_relation(priority_list[father_index], priority_list[child_index]):
                reward[child_index] = reward[child_index] + reward[father_index] * np.power(gamma, (pattern_class[father_index] - pattern_class[child_index]))


    reward_threshold = 0

    reward_list = list(set(reward))
    sorted_reward = sorted(reward_list, reverse=True)

    relation_ranking = np.zeros((np.array(priority_list).shape[0]), dtype= int)
    count = 1
    for i in range (len(sorted_reward)):
        same_number = 0
        for j in range (len(reward)):
            if reward[j] == sorted_reward[i]:
                sorted_violation_pattern_list.append(priority_list[j])
                if reward[j] <= reward_threshold:
                    relation_ranking[j] = 1000
                else:
                    relation_ranking[j] = count
                # relation_ranking[j] = count
                same_number = same_number + 1
        count = count + same_number

    weight_relation = 1

    return weight_relation, sorted_violation_pattern_list, relation_ranking, reward

def Relation_Ranking2 (violation_pattern_to_search, searched_violation_pattern, priority_list):
    parent_list, child_list = Relation (priority_list)
    sorted_violation_pattern_list = []
    gamma = 0.5
    pattern_num = np.array(priority_list).shape[0]
    goal_num = np.array(priority_list).shape[1]

    reward = np.ones((pattern_num), dtype=float)
    count_violation = np.sum(priority_list, axis=1)

    for i in range (np.array(violation_pattern_to_search).shape[0]):
        ## 0126
        for j in range(np.array(priority_list).shape[0]):
            if (np.array(violation_pattern_to_search[i]) == np.array(priority_list[j])).all():
                my_index = j
                break

        ancessor_list = []
        father_index = []
        for j in range (pattern_num):
            if parent_list[my_index][j] == 1:
                father_index.append(j)
                ancessor_list.append(priority_list[j])

        if len(father_index) > 0:
            not_found_pattern = 0
            for j in range (len(father_index)):
                for k in range (np.array(violation_pattern_to_search).shape[0]):
                    if (np.array(ancessor_list[j]) == np.array(violation_pattern_to_search[k])).all():
                        # print("we have this")
                        not_found_pattern = not_found_pattern + 1
                        break
            reward[my_index] = (len(father_index) - not_found_pattern)/len(father_index)

    for i in range (np.array(searched_violation_pattern).shape[0]):
        reward_0 = 1 ## searched and found
        for j in range (np.array(violation_pattern_to_search).shape[0]):
            if (np.array(searched_violation_pattern[i]) == np.array(violation_pattern_to_search[j])).all():
                reward_0 = -1  ## searched and not found
                break

        for j in range (pattern_num):
            if (np.array(searched_violation_pattern[i]) == np.array(priority_list[j])).all():
                goal_selection_flag_index = j
                # reward[goal_selection_flag_index] = reward[goal_selection_flag_index] + reward_0
                reward[goal_selection_flag_index] = reward_0
                break

        if reward_0 == -1:
            initial_class = sum(searched_violation_pattern[i])
            for j in range (pattern_num):
                if count_violation[j] < initial_class:
                    for k in range(np.array(violation_pattern_to_search).shape[0]):
                        if (np.array(violation_pattern_to_search[k]) == np.array(priority_list[j])).all():
                            reward[j] = reward[j] + reward_0 * np.power(gamma, (initial_class - count_violation[j]))
                            break


        # initial_class = sum(searched_violation_pattern[i])
        # for j in range (pattern_num):
        #     if count_violation[j] < initial_class:
        #         reward[j] = reward[j] + reward_0 * np.power(gamma, (initial_class - count_violation[j]))

    # sorted_reward = np.sort(list(set(reward)))
    reward_list = list(set(reward))
    # print(reward_list)
    sorted_reward = sorted(reward_list, reverse=True)
    # print(sorted_reward)
    # sorted_reward = np.array(sorted_reward)

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

    return weight_relation, sorted_violation_pattern_list, relation_ranking, reward

if __name__ == '__main__':


    searched_violation_pattern = [[1, 1, 1], [1, 0, 1]]
    priority_list = [[1, 1, 1], [0, 1, 1], [1, 0, 1], [0, 0, 1], [1, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0]]
    violation_pattern_to_search = [[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0]]
    sorted_violation_pattern_relation = Relation_Ranking (violation_pattern_to_search, searched_violation_pattern, priority_list)
    print(sorted_violation_pattern_relation )