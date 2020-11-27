#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import math
from Configure import configure
import os
import time
import json


"""
ego_state: X, Y, Time, Direction, Velocity, Acceleration Profile (aidx), Acceleration
dynamic_obstacle_state: dyn_obs->start_pos()[0], dyn_obs->start_pos()[1], dyn_obs->start_dir(),euclidean_distance(ego_x, ego_y, dynamic_obs_x, dynamic_obs_y), 
dynamic_obs_x, dynamic_obs_y, dyn_obs->velo(), dyn_obs->acc());
static_vehicle_state
static_vehicle_state: x,y, euclidean_distance
"""

config = configure()


def evaluate_distance (ego_vehicle_state, dynamic_vehicle_state,dy_obsList, static_vehicle_state,st_obsList):

    # print(len(static_vehicle_state[0][0]), len(dynamic_vehicle_state[0]))

    dis_list = []
    dis_satisfaction = []


    # if len(ego_vehicle_state) == len(dynamic_vehicle_state[0]):
    #     range_list = len(ego_vehicle_state)
    # else:
    #     range_list = min(len(ego_vehicle_state),len(dynamic_vehicle_state[0]))

    ## in case that the size are not same
    num_dynamic_obs = len(dy_obsList)
    num_static_obs = len(st_obsList)

    range_list_dy = len(dynamic_vehicle_state[0])
    # print(range_list_dy)
    for obs in range (1,num_dynamic_obs):
        range_list_dy = min(range_list_dy,len(dynamic_vehicle_state[obs]))
    # print(range_list_dy)

    range_list_st = len(static_vehicle_state[0])
    # print(range_list_st)
    for obs in range (1,num_static_obs):
        range_list_st = min(range_list_st,len(static_vehicle_state[obs]))
    # print(range_list_st)

    if range_list_dy < range_list_st:
        range_list = min(len(ego_vehicle_state),range_list_dy)
    else:
        range_list = min(len(ego_vehicle_state), range_list_st)

    # print(range_list)

    for i in range (range_list):
        min_dist = 1000
        flag = 0
        ego_x_min = ego_vehicle_state[i][0] - config.ego_width / 2
        ego_x_max = ego_vehicle_state[i][0] + config.ego_width / 2
        ego_y_min = ego_vehicle_state[i][1] - config.ego_length / 2
        ego_y_max = ego_vehicle_state[i][1] + config.ego_length / 2

        ego_position = [[ego_x_min, ego_y_min], [ego_x_min, ego_y_max], [ego_x_max, ego_y_min],
                        [ego_x_max, ego_y_max]]

        for num in range (len(dynamic_vehicle_state)):
            vehicle_width = float(dy_obsList[num]["width"])
            vehicle_length = float(dy_obsList[num]["length"])
            veh_x_min = dynamic_vehicle_state[num][i][4] - vehicle_width / 2
            veh_x_max = dynamic_vehicle_state[num][i][4] + vehicle_width / 2
            veh_y_min = dynamic_vehicle_state[num][i][5] - vehicle_length / 2
            veh_y_max = dynamic_vehicle_state[num][i][5] + vehicle_length / 2

            veh_position = [[veh_x_min, veh_y_min], [veh_x_min, veh_y_max], [veh_x_max, veh_y_min],
                            [veh_x_max, veh_y_max]]

            # 分别计算两矩形中心点在X轴和Y轴方向的距离
            Dx = abs (ego_vehicle_state[i][0] - dynamic_vehicle_state[num][i][4])
            Dy = abs (ego_vehicle_state[i][1] - dynamic_vehicle_state[num][i][5])

            # 两矩形不相交，在X轴方向有部分重合的两个矩形，最小距离是上矩形的下边线与下矩形的上边线之间的距离
            if ((Dx < ((config.ego_width + vehicle_width)/2)) and (Dy >= ((config.ego_length + vehicle_length) / 2))):
                dist = Dy - ((config.ego_length + vehicle_length) / 2)
                if dist < min_dist:
                    flag = 1
                    min_dist = dist
            # 两矩形不相交，在Y轴方向有部分重合的两个矩形，最小距离是左矩形的右边线与右矩形的左边线之间的距离
            elif ((Dx >= ((config.ego_width + vehicle_width)/ 2)) and (Dy < ((config.ego_length + vehicle_length) / 2))):
                dist = Dx - ((config.ego_width + vehicle_width) / 2)
                if dist < min_dist:
                    flag = 2
                    min_dist = dist
            # 两矩形不相交，在X轴和Y轴方向无重合的两个矩形，最小距离是距离最近的两个顶点之间的距离
            elif ((Dx >= ((config.ego_width + vehicle_width)/ 2)) and (Dy >= ((config.ego_length + vehicle_length) / 2))):
                delta_x = Dx - ((config.ego_width + vehicle_width)/ 2)
                delta_y = Dy - ((config.ego_length + vehicle_length) / 2)
                dist = math.sqrt(delta_x * delta_x + delta_y * delta_y)
                if dist < min_dist:
                    flag = 3
                    min_dist = dist

            # 两矩形相交，最小距离为负值，返回-1
            else:
                flag = 4
                min_dist = -1
                break

        for num in range (len(static_vehicle_state)):
            vehicle_width = config.ego_width
            vehicle_length = config.ego_length
            veh_x_min = static_vehicle_state[num][i][0] - vehicle_width / 2
            veh_x_max = static_vehicle_state[num][i][0] + vehicle_width / 2
            veh_y_min = static_vehicle_state[num][i][1] - vehicle_length / 2
            veh_y_max = static_vehicle_state[num][i][1] + vehicle_length / 2

            veh_position = [[veh_x_min, veh_y_min], [veh_x_min, veh_y_max], [veh_x_max, veh_y_min],
                            [veh_x_max, veh_y_max]]

            # 分别计算两矩形中心点在X轴和Y轴方向的距离
            Dx = abs (ego_vehicle_state[i][0] - static_vehicle_state[num][i][0])
            Dy = abs (ego_vehicle_state[i][1] - static_vehicle_state[num][i][1])

            # 两矩形不相交，在X轴方向有部分重合的两个矩形，最小距离是上矩形的下边线与下矩形的上边线之间的距离
            if ((Dx < ((config.ego_width + vehicle_width)/2)) and (Dy >= ((config.ego_length + vehicle_length) / 2))):
                dist = Dy - ((config.ego_length + vehicle_length) / 2)
                if dist < min_dist:
                    flag = 1
                    min_dist = dist
            # 两矩形不相交，在Y轴方向有部分重合的两个矩形，最小距离是左矩形的右边线与右矩形的左边线之间的距离
            elif ((Dx >= ((config.ego_width + vehicle_width)/ 2)) and (Dy < ((config.ego_length + vehicle_length) / 2))):
                dist = Dx - ((config.ego_width + vehicle_width) / 2)
                if dist < min_dist:
                    flag = 2
                    min_dist = dist
            # 两矩形不相交，在X轴和Y轴方向无重合的两个矩形，最小距离是距离最近的两个顶点之间的距离
            elif ((Dx >= ((config.ego_width + vehicle_width)/ 2)) and (Dy >= ((config.ego_length + vehicle_length) / 2))):
                delta_x = Dx - ((config.ego_width + vehicle_width)/ 2)
                delta_y = Dy - ((config.ego_length + vehicle_length) / 2)
                dist = math.sqrt(delta_x * delta_x + delta_y * delta_y)
                if dist < min_dist:
                    flag = 3
                    min_dist = dist

            # 两矩形相交，最小距离为负值，返回-1
            else:
                flag = 4
                min_dist = -1
                break




        dis_list.append(min_dist)
        # print(min_dist)
        if min_dist >= config.minimumseperation:
            satisfaction = 1
        elif min_dist < config.assured_clear_distance_ahead:
            satisfaction = 0
        else:
            satisfaction =(min_dist- config.assured_clear_distance_ahead)/(config.minimumseperation - config.assured_clear_distance_ahead)

        dis_satisfaction.append(satisfaction)

    # print(dis_list, dis_satisfaction, dis_satisfaction)

    if len(dis_list) and len(dis_satisfaction):
        min_dis = min(dis_list)
        min_satisfaction = min(dis_satisfaction)
        avg_satisfaction = np.mean(dis_satisfaction)
    else:
        min_dis = -1
        min_satisfaction = -1
        avg_satisfaction = -1

    return min_dis, min_satisfaction, avg_satisfaction


def evaluate_speed (ego_vehicle_state):
    speed_list = []
    for i in range(len(ego_vehicle_state)):
        speed_list.append(ego_vehicle_state[i][4])

    ## type 1
    # maxspeed = max(speed_list)
    # if  maxspeed > config.speed_limit:
    #     satisfaction = 0
    # else:
    #     satisfaction  = 1

    ## type 2
    satisfaction_list = []
    for i in range(len(speed_list)):
        if speed_list[i]<= config.speed_limit:
            ds = 1
        elif  speed_list[i] > config.speed_max:
            ds = 0
        else:
            ds = (config.speed_max - speed_list[i])/(config.speed_max - config.speed_limit)
        satisfaction_list.append(ds)
    # print(satisfaction_list)
    # satisfaction  = 1/(len(satisfaction_list))*sum(satisfaction_list)


    return np.mean(satisfaction_list)

def evaluate_comfort (ego_vehicle_state):
    comfort_list = []

    for i in range(len(ego_vehicle_state)-1):
        a_pre = [ego_vehicle_state[i][6]*math.cos(ego_vehicle_state[i][3]), ego_vehicle_state[i][6]*math.sin(ego_vehicle_state[i][3])]
        a_next = [ego_vehicle_state[i+1][6]*math.cos(ego_vehicle_state[i+1][3]), ego_vehicle_state[i+1][6]*math.sin(ego_vehicle_state[i+1][3])]
        v_pre = [ego_vehicle_state[i][4]*math.cos(ego_vehicle_state[i][3]), ego_vehicle_state[i][4]*math.sin(ego_vehicle_state[i][3])]
        v_next = [ego_vehicle_state[i+1][4]*math.cos(ego_vehicle_state[i+1][3]), ego_vehicle_state[i+1][4]*math.sin(ego_vehicle_state[i+1][3])]
        delta_a = np.sqrt(np.sum(np.square(np.array(a_pre)-np.array(a_next))))/ np.sqrt(np.sum(np.square(config.a_max_soft-config.a_min_soft)))
        delta_v = np.sqrt(np.sum(np.square(np.array(v_pre)-np.array(v_next))))/ config.speed_max
        comfort_now = math.exp(-(delta_a + delta_v))

        comfort_list.append (comfort_now)
        # print(a_pre, a_next, np.sqrt(np.sum(np.square(np.array(a_pre)-np.array(a_next)))), comfort_now)

    if len(comfort_list) == 0:
        satisfaction_comfort = 1
    else:
        satisfaction_comfort = 1/(len(comfort_list))*sum(comfort_list)

    return satisfaction_comfort

def evaluate_stability (ego_vehicle_state):
    curvature_list = []

    for i in range(len(ego_vehicle_state) - 1):
        pre = [ego_vehicle_state[i][0], ego_vehicle_state[i][1]]
        next = [ego_vehicle_state[i+1][0], ego_vehicle_state[i+1][1]]
        theta = abs (ego_vehicle_state[i+1][2] -ego_vehicle_state[i][2])
        delta_l = np.sqrt(np.sum(np.square(np.array(pre) - np.array(next))))
        if delta_l == 0:
            cur = 0
        else:
            cur = theta/delta_l
        if cur <= config.k_thr:
            satisfaction = 1
        elif cur > config.k_limit:
            satisfaction = 0
        else:
            satisfaction = 1 - (cur - config.k_thr)/(config.k_limit - config.k_thr)
        curvature_list.append(satisfaction)

    if len(curvature_list) == 0:
        satisfaction_curvature = 0
    else:
        satisfaction_curvature = 1/(len(curvature_list))*sum(curvature_list)
    return satisfaction_curvature

def evaluate_traffic_light (ego_vehicle_state, traffic_light):
    t_green = traffic_light[0]["green_time"]
    t_yellow = traffic_light[0]["yellow_time"]
    t_red = traffic_light[0]["red_time"]
    # print(t_green, t_yellow, t_red)
    ego_velocity = []
    for i in range(len(ego_vehicle_state)):
        if (ego_vehicle_state[i][2] >= t_green + t_yellow) and (ego_vehicle_state[i][2] <= t_green + t_yellow + t_red):
            # print(ego_vehicle_state[i][4])
            if abs(ego_vehicle_state[i][4]) < 0.1:
                ego_velocity.append(ego_vehicle_state[i][4])
    stop_time = 0.1 * len(ego_velocity)
    if stop_time < 0:
        satisfaction = 0
    else:
        satisfaction = stop_time/t_red

    ## pass the traffic light
    red_start = t_green + t_yellow
    red_end = t_green + t_yellow + t_red
    index = int(red_start/0.1)
    index_2 = int(red_start/0.1)
    # print(red_start,index,  ego_vehicle_state[index][2], len(ego_vehicle_state), ego_vehicle_state[index][1])
    # for i in range(len(ego_vehicle_state)):
    #     if (ego_vehicle_state[i][2] == red_start):
    #         print(ego_vehicle_state[i])
    #     elif (ego_vehicle_state[i][2] == red_start) and (ego_vehicle_state[i][1]>200):
    #         satisfaction = 1

    if ego_vehicle_state[-1][2] < red_start: ## not start
        satisfaction = 1
    elif ego_vehicle_state[index][1] < 196 : ## red light previous
        satisfaction = 1
    elif ego_vehicle_state[index][1] > 200.8: ## red light behind
        satisfaction = 1
    return satisfaction




if __name__=='__main__':

    file_dir_sce = os.getcwd() + '/scenarios_' + str(time.strftime("%Y_%m_%d"))
    file_dir_data = os.getcwd() + '/datalog_' + str(time.strftime("%Y_%m_%d"))

    file_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    scenario_name = file_dir_sce + "\scenario_" + str(0) + ".json"
    log_name = file_dir_data + "\datalog_" + str(0) + ".txt"

    cmd = file_path+"\dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (100, scenario_name, log_name)

    # print(cmd)
    os.system(cmd)
    print(log_name)


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

    dynamic_vehicle_state = np.zeros((num_dynamic_obs, len(ego_vehicle_state), 8), float)
    # print(dynamic_vehicle_state.shape)
    static_vehicle_state = np.zeros((num_static_obs, len(ego_vehicle_state), 8), float)
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
                        dynamic_vehicle_state[i][time_step][j - 2] = float(data[j])
                    time_step = time_step + 1

                    # print(log, dynamic_vehicle_state[i])
                    # dynamic_vehicle_state[i].append(log)
        # print(dynamic_vehicle_state)

    # print(dynamic_vehicle_state.shape[0])

    comfort = evaluate_comfort(ego_vehicle_state)
    speed = evaluate_speed(ego_vehicle_state)
    min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                    dy_obsList)
    stable = evaluate_stability(ego_vehicle_state)
    traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

    result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]
    print(result)