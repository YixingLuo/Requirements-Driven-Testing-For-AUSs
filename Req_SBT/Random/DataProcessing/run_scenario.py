#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from trash.initial_files.Configure import configure
import json
from trash.initial_files.read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light, evaluate_cross_lane

config = configure()

file_dir_sce = 'C:/Users/lenovo/Documents/GitHub/Requirements-Driven-Testing-For-AUSs/Req_SBT/2020_12_03_NSGA_III_scenarios_5000'
# file_dir_data = os.getcwd() + '/2020_12_02_NSGA_III_scenarios_10000'
scenario_name = file_dir_sce + "/scenario_20201203215357_995_0dfc64c77d4843a7ad060b8fe53afb69.json"
log_name = "datalog_example.txt"

# log_name = file_dir_data + "/datalog_" + now_time + "_" + uuid_str + ".txt"
cmd = "C:/Users/lenovo/Documents/GitHub/mazda-path-planner-sbt_changes/mazda-path-planner-sbt_changes/ERATO_planning/x64/Release/" \
      "dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (config.duration, scenario_name, log_name)


os.system(cmd)

num_dynamic_obs = 2
num_static_obs = 2

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

        if data[0] == "DYNAMIC_OBS_INFO" and len(data) == 10:
            log = []
            for i in range(2, len(data)):
                log.append(float(data[i]))
                # print(log)
            if len(log) == 8:
                dynamic_vehicle_state[int(data[1])].append(log)
        elif data[0] == "STATIC_OBS_INFO" and len(data) == 5:
            log = []
            for i in range(2, len(data)):
                log.append(float(data[i]))
                # print(log)
            if len(log) == 3:
                static_vehicle_state[int(data[1])].append(log)

comfort1, comfort2 = evaluate_comfort(ego_vehicle_state)
avg_speed, min_speed = evaluate_speed(ego_vehicle_state)
min_dis, avg_dis_satisfaction, min_dis_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                        dy_obsList, static_vehicle_state, st_obsList)
avg_stable, min_stable = evaluate_stability(ego_vehicle_state)
traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)
cross_lane = evaluate_cross_lane(ego_vehicle_state)

result = [avg_stable, min_stable, avg_dis_satisfaction, min_dis_satisfaction, avg_speed, min_speed, traffic_light, cross_lane,
          comfort1, comfort2]
print(result)