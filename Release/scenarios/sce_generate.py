#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import numpy as np
import random

with open('SCENAR1.json', 'r', encoding='utf-8') as f:
    ret_dic = json.load(f)
    # print(ret_dic)

for key in ret_dic:
    if key == "config":
        configList = ret_dic[key]
        # print(configList)
        configList["s0"]= random.uniform (50,200)
        configList["l0"] = 1.5
        configList["v0"] = random.uniform(4,16)
        configList["theta0"] = 1.57

    elif key == "dynamic_obs":
        obsList = ret_dic[key]
        ret_dic[key] = []
        num_obs = np.random.randint(1, 4)
        # print(num_obs)
        dir_list = [0,3.14,-1.57]
        for i in range(num_obs):
            dir_index = np.random.randint(0, 3)
            dir = dir_list[dir_index]
            if dir_index == 0:
                # [-120,-20]
                x = - random.uniform (20,120)
                # [212,217]
                y = random.uniform(212,217)
            elif dir_index == 1:
                # [20,120]
                x = random.uniform(20,120)
                ## [205,210]
                y = random.uniform(205,210)
            else:
                ## [1,6]
                x = random.uniform(1,6)
                ## [150,250]
                y = random.uniform(150,250)

            vel = random.uniform(4,16)
            acc = random.uniform(0,3)
            width = 1.8
            length = 4.8
            obsDict = {"pos_x":x, "pos_y":y, "dir":dir, "width": width, "length": length, "velo": vel,"acc": acc}
            ret_dic[key].append(obsDict)
    elif key == "static_obs":
        obsList = ret_dic[key]
        ret_dic[key] = []
        # num_obs = np.random.randint(0, 2)
        # for i in range(num_obs):
        #     obsDict = {"pos_s":20,"pos_l":213, "width": 1.8, "length": 4.8}
        #     ret_dic[key].append(obsDict)
    elif key == "traffic_signal":
        ret_dic[key] = []
        # obsDict = {"green_time": 18, "yellow_time": 2, "red_time": 5, "start_s": 190, "end_s":220}
        # ret_dic[key].append(obsDict)

with open('scenario_1.json', 'w', encoding='utf-8') as f:
        json.dump(ret_dic, f, ensure_ascii=False, indent=4)
