#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import numpy as np
import random
from trash.initial_files.Configure import configure
import os
import time
from trash.initial_files.read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light

config = configure()

file_dir_sce = os.getcwd() + '/scenarios_' + str(time.strftime("%Y_%m_%d"))
if not os.path.exists(file_dir_sce):
    os.mkdir(file_dir_sce)

file_dir_data = os.getcwd() + '/datalog_' + str(time.strftime("%Y_%m_%d"))
if not os.path.exists(file_dir_data):
    os.mkdir(file_dir_data)

file_dir_eval = os.getcwd() + '/results_' + str(time.strftime("%Y_%m_%d"))
if not os.path.exists(file_dir_eval):
    os.mkdir(file_dir_eval)

for num_sce in range(config.population):
    with open('SCENAR1.json', 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)

    for key in ret_dic:
        if key == "config":
            configList = ret_dic[key]
            # print(configList)
            configList["s0"] = random.uniform(50, 200)
            configList["l0"] = 1.75 + 3.5 * random.randint(0, 1)
            configList["v0"] = random.uniform(4, 16)
            configList["theta0"] = 1.57

        elif key == "dynamic_obs":
            obsList = ret_dic[key]
            ret_dic[key] = []
            num_obs = np.random.randint(1, 5)
            # print(num_obs)
            dir_list = [0, 3.14, -1.57, 1.57]
            for i in range(num_obs):
                dir_index = np.random.randint(0, 3)
                dir = dir_list[dir_index]
                if dir_index <= 2:
                    if dir_index == 0:
                        # [-120,-20]
                        x = - random.uniform(20, 120)
                        # [212,217]
                        y = random.uniform(212, 217)
                    elif dir_index == 1:
                        # [20,120]
                        x = random.uniform(20, 120)
                        ## [205,210]
                        y = random.uniform(205, 210)
                    elif dir_index == 2:
                        ## [1,6]
                        x = random.uniform(1, 6)
                        ## [150,250]
                        y = random.uniform(150, 250)
                    vel = random.uniform(4, 16)
                    acc = random.uniform(0, 3)
                    width = random.uniform(0.5, 3.5)
                    length = random.uniform(2, 5)
                    start = random.randint(0, 50)

                else:
                    x = -120 + random.uniform(0, 240)
                    y = random.uniform(50, 250)
                    vel = 0
                    acc = 0
                    width = random.uniform(1, 3)
                    length = random.uniform(2, 5)
                    start = 0
                obsDict = {"pos_x": x, "pos_y": y, "dir": dir, "width": width, "length": length, "velo": vel,
                           "acc": acc, "start_time": start}
                ret_dic[key].append(obsDict)
        elif key == "static_obs":
            obsList = ret_dic[key]
            ret_dic[key] = []
            # num_obs = random.randint(1, 3)
            # for i in range(num_obs):
            #     width = random.uniform(0, 3.5)
            #     length = random.uniform(0, 5)
            #     x = -120 + random.uniform(0, 240)
            #     y = random.uniform(50, 250)
            #     obsDict = {"pos_x": x, "pos_y": y, "width": width, "length": length, }
            #     ret_dic[key].append(obsDict)
            # num_obs = np.random.randint(0, 2)
            # for i in range(num_obs):
            #     obsDict = {"pos_s":20,"pos_l":213, "width": 1.8, "length": 4.8}
            #     ret_dic[key].append(obsDict)
        elif key == "traffic_signal":
            ret_dic[key] = []
            objDict = {"green_time": random.randint(10, 20), "yellow_time": random.randint(1, 3), "red_time": random.randint(4, 6), "start_s": 190, "end_s":220}
            ret_dic[key].append(objDict)

    scenario_name = file_dir_sce + "\scenario_" + str(num_sce) + ".json"
    print(scenario_name)
    with open(scenario_name, 'w', encoding='utf-8') as f:
        json.dump(ret_dic, f, ensure_ascii=False, indent=4)


    ## run the scenario
    duration = config.duration

    file_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    # print(file_path)
    scenario_name = file_dir_sce + "\scenario_" + str(num_sce) + ".json"
    log_name = file_dir_data + "\datalog_" + str(num_sce) + ".txt"
    cmd = file_path+"\dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (duration, scenario_name, log_name)

    # print(cmd)
    os.system(cmd)
    print(log_name)


    ## requirements evaluration
# for num_sce in range(config.population):
#     scenario_name = file_dir_sce + "\scenario_" + str(num_sce) + ".json"
#     log_name = file_dir_data + "\datalog_" + str(num_sce) + ".txt"
    # print(scenario_name)
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
    with open(log_name, 'r') as f:
        my_data = f.readlines()  # txt中所有字符串读入data，得到的是一个list
        # 对list中的数据做分隔和类型转换
        for line in my_data:
            line_data = line.split()
            numbers_float = map(float, line_data)  # 转化为浮点数

        for line in my_data:
            data = line.split()
            if data[0] == "EGO_STATUS":
                log = []
                for i in range(1, len(data)):
                    log.append(float(data[i]))
                ego_vehicle_state.append(log)



    dynamic_vehicle_state = np.zeros((num_dynamic_obs, len(ego_vehicle_state) ,8),float)
    # print(dynamic_vehicle_state.shape)
    static_vehicle_state = np.zeros((num_static_obs, len(ego_vehicle_state) ,8),float)
    width = config.ego_width
    length = config.ego_length

    with open(log_name, 'r') as f:
        my_data = f.readlines()  # txt中所有字符串读入data，得到的是一个list
        # 对list中的数据做分隔和类型转换
        for line in my_data:
            line_data = line.split()
            numbers_float = map(float, line_data)  # 转化为浮点数

        for i in range(num_dynamic_obs):
            time_step = 0
            for line in my_data:
                data = line.split()
                if data[0] == "DYNAMIC_OBS_INFO" and data[1] == str(i):
                    for j in range(2, len(data)):
                        # log.append(float(data[j]))
                        # print(i, time_step, j-2)
                        dynamic_vehicle_state[i][time_step][j-2] = float(data[j])
                    time_step = time_step + 1

                        # print(log, dynamic_vehicle_state[i])
                        # dynamic_vehicle_state[i].append(log)
        # print(dynamic_vehicle_state)

    # print(dynamic_vehicle_state.shape[0])

    comfort = evaluate_comfort(ego_vehicle_state)
    speed = evaluate_speed(ego_vehicle_state)
    min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state, dy_obsList)
    stable = evaluate_stability(ego_vehicle_state)
    traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

    result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]
    print(result)

    result_name = file_dir_eval + "\\result_" + str(num_sce) + ".txt"
    print(result_name)
    np.savetxt(result_name, result, fmt="%f", delimiter=" ")

