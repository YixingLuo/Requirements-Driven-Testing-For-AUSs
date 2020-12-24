
#!/usr/bin/python
# -*- coding:utf-8 -*-
# coding=gbk

import csv
import numpy as np
priority_list = []
with open("priority_list.csv") as csvfile:
    csv_file = csv.reader(csvfile)
    # birth_header = next(csv_reader)
    # csv_file=csv.reader(open("priority_list.csv",'r'))
    for row in csv_file:
        priority_list.append(row)


priority_list = [[float(x) for x in row] for row in priority_list]
# print(priority_list)

priority_list= np.array(priority_list)
# priority_list_header = np.array(priority_list)
print(priority_list.shape)
print(priority_list[0],priority_list[0][0])
goal_selection_flag = priority_list[0]
print(len(goal_selection_flag))
# print(priority_list.shape)

import random
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list

resultList=random.sample(range(1,5),4)
print(resultList)