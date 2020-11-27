#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import os
from threading import Thread
from Configure import configure
import time
import json
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light

config = configure()

file_dir_sce = os.getcwd() + '/2020_11_26_NSGAII_scenarios_1000'
file_dir_data = os.getcwd() + '/2020_11_26_NSGAII_datalog_1000'
scenario_name = file_dir_sce + "/scenario-19-1.json"
log_name = file_dir_data + "/datalog-19-1.txt"

with open(scenario_name, 'r', encoding='utf-8') as f:
    ret_dic = json.load(f)
    for key in ret_dic:
        if key == "dynamic_obs":
            dy_obsList = ret_dic[key]
            num_dynamic_obs = len(dy_obsList)
            # print(dy_obsList)
            # print(dy_obsList[0]["width"])
        if key == "static_obs":
            st_obsList = ret_dic[key]
            num_static_obs = len(st_obsList)
        if key == "traffic_signal":
            traffic_light = ret_dic[key]

ego_vehicle_state = []
dynamic_vehicle_state = [[] for i in range(num_dynamic_obs)]
static_vehicle_state = [[] for i in range(num_static_obs)]
with open(log_name, 'r') as f:
    my_data = f.readlines()  # txt中所有字符串读入data，得到的是一个list
    # 对list中的数据做分隔和类型转换
    # for line in my_data:
    #     line_data = line.split()
    #     numbers_float = map(float, line_data)  # 转化为浮点数

    for line in my_data:
        data = line.split()
        if data[0] == "EGO_STATUS" and len(data) == 8:
            log = []
            for i in range(1, len(data)):
                log.append(float(data[i]))
            if len(log) == 7:
                ego_vehicle_state.append(log)

        if data[0] == "DYNAMIC_OBS_INFO"  and len(data) == 10:
            log = []
            for i in range(2, len(data)):
                log.append(float(data[i]))
                print(log)
            if len(log) == 8:
                dynamic_vehicle_state[int(data[1])].append(log)
        elif data[0] == "STATIC_OBS_INFO"  and len(data) == 5:
            log = []
            for i in range(2, len(data)):
                log.append(float(data[i]))
                # print(log)
            if len(log) == 3 :
                static_vehicle_state[int(data[1])].append(log)

# print(len(dynamic_vehicle_state[0]),len(static_vehicle_state[0]), np.array(static_vehicle_state).shape[0],len(ego_vehicle_state),static_vehicle_state[1][0][0])

comfort = evaluate_comfort(ego_vehicle_state)
speed = evaluate_speed(ego_vehicle_state)
min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                dy_obsList, static_vehicle_state, st_obsList)
stable = evaluate_stability(ego_vehicle_state)
traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]
print(result)