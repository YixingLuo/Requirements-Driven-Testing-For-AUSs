#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import math
# from TurnRightConfigure import TurnRightConfigure
import os
import time
import json
import shapely
from shapely.geometry import Point, Polygon
from shapely import affinity

"""
ego_state: X, Y, Time, Direction, Velocity, Acceleration Profile (aidx), Acceleration
dynamic_obstacle_state: dyn_obs->start_pos()[0], dyn_obs->start_pos()[1], dyn_obs->start_dir(),euclidean_distance(ego_x, ego_y, dynamic_obs_x, dynamic_obs_y), 
dynamic_obs_x, dynamic_obs_y, dyn_obs->velo(), dyn_obs->acc());
static_vehicle_state
static_vehicle_state: x,y, euclidean_distance
"""

# config = configure()


def evaluate_collision (ego_vehicle_state, dynamic_vehicle_state,dy_obsList, static_vehicle_state,st_obsList, config):
    dis_list = []
    dis_satisfaction = []

    ## in case that the size are not same
    num_dynamic_obs = len(dy_obsList)
    num_static_obs = len(st_obsList)

    if num_dynamic_obs:
        range_list_dy = len(dynamic_vehicle_state[0])
    else:
        range_list_dy = 0
    for obs in range (1,num_dynamic_obs):
        range_list_dy = min(range_list_dy,len(dynamic_vehicle_state[obs]))

    if num_static_obs:
        range_list_st = len(static_vehicle_state[0])
    else:
        range_list_st = 0
    for obs in range (1,num_static_obs):
        range_list_st = min(range_list_st,len(static_vehicle_state[obs]))

    if num_dynamic_obs and num_static_obs:
        if range_list_dy < range_list_st:
            range_list = min(len(ego_vehicle_state),range_list_dy)
        else:
            range_list = min(len(ego_vehicle_state), range_list_st)
    elif num_dynamic_obs:
        range_list = min(len(ego_vehicle_state), range_list_dy)
    elif num_static_obs:
        range_list = min(len(ego_vehicle_state), range_list_st)

    for i in range (range_list):
        min_dist = 1000
        flag = 0
        ego_direction = ego_vehicle_state[i][3]
        x = ego_vehicle_state[i][0]
        y = ego_vehicle_state[i][1]
        ego_vehicle_center = Point(x, y)
        point1 = Point(x - config.ego_length / 2, y - config.ego_width / 2)
        point2 = Point(x + config.ego_length / 2, y - config.ego_width / 2)
        point3 = Point(x + config.ego_length / 2, y + config.ego_width / 2)
        point4 = Point(x - config.ego_length / 2, y + config.ego_width / 2)
        ego_rect = Polygon([point1, point2, point3, point4])
        angle = ego_direction * (180.0 / math.pi)


        rect_ego = affinity.rotate(ego_rect, angle)


        for num in range (len(dynamic_vehicle_state)):
            vehicle_width = float(dy_obsList[num]["width"])
            vehicle_length = float(dy_obsList[num]["length"])

            veh_x = dynamic_vehicle_state[num][i][4]
            veh_y = dynamic_vehicle_state[num][i][5]
            other_vehicle_center = Point(veh_x, veh_y)
            point1 = Point(veh_x - vehicle_length / 2, veh_y - vehicle_width / 2)
            point2 = Point(veh_x + vehicle_length / 2, veh_y - vehicle_width / 2)
            point3 = Point(veh_x + vehicle_length / 2, veh_y + vehicle_width / 2)
            point4 = Point(veh_x - vehicle_length / 2, veh_y + vehicle_width / 2)
            other_rect = Polygon([point1, point2, point3, point4])
            angle = dynamic_vehicle_state[num][i][2] * (180.0 / math.pi)
            rect_other = affinity.rotate(other_rect, angle)

            intersection = rect_ego.intersection(rect_other)
            if not intersection.is_empty:
                # print("rect_ego", rect_ego)
                # print("ego_state", ego_vehicle_state[i][0], ego_vehicle_state[i][1])
                # print("other rect:", other_rect)
                # print("other vehicle state:", dynamic_vehicle_state[num][i][4], dynamic_vehicle_state[num][i][5])
                flag = -1
                min_dist = -1
                break
            else:
                dist = ego_vehicle_center.distance(other_vehicle_center)
                if dist < min_dist:
                    # print("rect_ego", rect_ego)
                    # print("ego_state", ego_vehicle_state[i][0], ego_vehicle_state[i][1])
                    # print("other rect:", rect_other)
                    # print("other vehicle state:", dynamic_vehicle_state[num][i][4], dynamic_vehicle_state[num][i][5])
                    min_dist = dist


        for num in range (len(static_vehicle_state)):
            vehicle_width = float(st_obsList[num]["width"])
            vehicle_length = float(st_obsList[num]["length"])

            veh_x = dynamic_vehicle_state[num][i][4]
            veh_y = dynamic_vehicle_state[num][i][5]
            other_vehicle_center = Point(veh_x, veh_y)
            point1 = Point(veh_x - vehicle_width / 2, veh_y - vehicle_length / 2)
            point2 = Point(veh_x + vehicle_width / 2, veh_y - vehicle_length / 2)
            point3 = Point(veh_x + vehicle_width / 2, veh_y + vehicle_length / 2)
            point4 = Point(veh_x - vehicle_width / 2, veh_y + vehicle_length / 2)
            other_rect = Polygon([point1, point2, point3, point4])

            intersection = rect_ego.intersection(other_rect)
            if not intersection.is_empty:
                flag = -1
                min_dist = -1
                break
            else:
                dist = ego_vehicle_center.distance(other_vehicle_center)
                if dist < min_dist:
                    min_dist = dist



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

    return min_dis, avg_satisfaction, min_satisfaction


def evaluate_distance (ego_vehicle_state, dynamic_vehicle_state,dy_obsList, static_vehicle_state,st_obsList, config):

    # print(dynamic_vehicle_state,dy_obsList)

    dis_list = []
    dis_satisfaction = []


    # if len(ego_vehicle_state) == len(dynamic_vehicle_state[0]):
    #     range_list = len(ego_vehicle_state)
    # else:
    #     range_list = min(len(ego_vehicle_state),len(dynamic_vehicle_state[0]))

    ## in case that the size are not same
    num_dynamic_obs = len(dy_obsList)
    num_static_obs = len(st_obsList)

    if num_dynamic_obs:
        range_list_dy = len(dynamic_vehicle_state[0])
    else:
        range_list_dy = 0
    # print(range_list_dy)
    for obs in range (1,num_dynamic_obs):
        range_list_dy = min(range_list_dy,len(dynamic_vehicle_state[obs]))
    # print(range_list_dy)

    if num_static_obs:
        range_list_st = len(static_vehicle_state[0])
    else:
        range_list_st = 0
    # print(range_list_st)
    for obs in range (1,num_static_obs):
        range_list_st = min(range_list_st,len(static_vehicle_state[obs]))
    # print(range_list_st)

    if num_dynamic_obs and num_static_obs:
        if range_list_dy < range_list_st:
            range_list = min(len(ego_vehicle_state),range_list_dy)
        else:
            range_list = min(len(ego_vehicle_state), range_list_st)
    elif num_dynamic_obs:
        range_list = min(len(ego_vehicle_state), range_list_dy)
    elif num_static_obs:
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

    return min_dis, avg_satisfaction, min_satisfaction


def evaluate_speed (ego_vehicle_state, config):
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
    if len(speed_list):
        for i in range(len(speed_list)):
            if speed_list[i] <= config.speed_limit:
                ds = 1
            elif  speed_list[i] > config.speed_max:
                ds = 0
            else:
                ds = (config.speed_max - speed_list[i])/(config.speed_max - config.speed_limit)
            satisfaction_list.append(ds)
    else:
        satisfaction_list.append(0)
    # print(satisfaction_list)
    # satisfaction  = 1/(len(satisfaction_list))*sum(satisfaction_list)

    return np.mean(satisfaction_list), min(satisfaction_list)

def evaluate_comfort (ego_vehicle_state, config):
    comfort_list_1 = []
    comfort_list_2 = []

    for i in range(len(ego_vehicle_state)-1):
        a_pre = [ego_vehicle_state[i][6]*math.cos(ego_vehicle_state[i][3]), ego_vehicle_state[i][6]*math.sin(ego_vehicle_state[i][3])]
        a_next = [ego_vehicle_state[i+1][6]*math.cos(ego_vehicle_state[i+1][3]), ego_vehicle_state[i+1][6]*math.sin(ego_vehicle_state[i+1][3])]
        v_pre = [ego_vehicle_state[i][4]*math.cos(ego_vehicle_state[i][3]), ego_vehicle_state[i][4]*math.sin(ego_vehicle_state[i][3])]
        v_next = [ego_vehicle_state[i+1][4]*math.cos(ego_vehicle_state[i+1][3]), ego_vehicle_state[i+1][4]*math.sin(ego_vehicle_state[i+1][3])]
        delta_a = np.sqrt(np.sum(np.square(np.array(a_pre)-np.array(a_next))))/ np.sqrt(np.sum(np.square(config.a_max_soft-config.a_min_soft)))
        delta_v = np.sqrt(np.sum(np.square(np.array(v_pre)-np.array(v_next))))/ config.speed_max
        comfort_now_1 = math.exp(- delta_a)
        comfort_now_2 = math.exp(- delta_v)

        comfort_list_1.append (comfort_now_1)
        comfort_list_2.append (comfort_now_2)
        # print(a_pre, a_next, np.sqrt(np.sum(np.square(np.array(a_pre)-np.array(a_next)))), comfort_now)

    if len(comfort_list_1) == 0:
        satisfaction_comfort_1 = 1
        satisfaction_comfort_2 = 1
    else:
        # satisfaction_comfort_1 = 1 / (len(comfort_list_1)) * sum(comfort_list_1)
        # satisfaction_comfort_2 = 1 / (len(comfort_list_2)) * sum(comfort_list_2)

        satisfaction_comfort_1 = 1 - sum(comfort_list_1) / 1000
        satisfaction_comfort_2 = 1 - sum(comfort_list_2) / 1000

    return satisfaction_comfort_1,satisfaction_comfort_2

def evaluate_stability (ego_vehicle_state, config):
    curvature_list = []

    for i in range(len(ego_vehicle_state) - 1):
        pre = [ego_vehicle_state[i][0], ego_vehicle_state[i][1]]
        next = [ego_vehicle_state[i+1][0], ego_vehicle_state[i+1][1]]
        theta = abs (ego_vehicle_state[i+1][3] -ego_vehicle_state[i][3])
        delta_l = np.sqrt(np.sum(np.square(np.array(pre) - np.array(next))))
        if delta_l == 0:
            cur = 0
        else:
            cur = theta/delta_l
            # cur = theta/math.pi*180/delta_l
            # print(cur)
        if cur <= 1/config.k_limit:
            satisfaction = 1
        elif cur > 1/config.k_limit:
            # print(cur, theta, delta_l, pre, next, ego_vehicle_state[i+1][2], ego_vehicle_state[i][2])
            satisfaction = 0
        # else:
        #     satisfaction = 1 - (cur - config.k_thr)/(config.k_limit - config.k_thr)
        curvature_list.append(satisfaction)

    if len(curvature_list) == 0:
        satisfaction_curvature = 0
        least_satisfaction_curvature = 0
    else:
        satisfaction_curvature = 1/(len(curvature_list))*sum(curvature_list)
        least_satisfaction_curvature = min(curvature_list)
    # print(curvature_list)
    return satisfaction_curvature, least_satisfaction_curvature

def evaluate_traffic_light (ego_vehicle_state, traffic_light):
    t_green = float(traffic_light[0]["green_time"])
    t_yellow = float(traffic_light[0]["yellow_time"])
    t_red = float(traffic_light[0]["red_time"])
    t_start = float(traffic_light[0]["start_s"])
    # print(t_green, t_yellow, t_red)
    ego_velocity = []
    for i in range(len(ego_vehicle_state)):
        if (ego_vehicle_state[i][2] >= t_green + t_yellow) and (ego_vehicle_state[i][2] <= t_green + t_yellow + t_red):
            # print(ego_vehicle_state[i][4])
            if abs(ego_vehicle_state[i][4]) < 1:
                ego_velocity.append(ego_vehicle_state[i][4])
    stop_time = 0.1 * len(ego_velocity)
    if stop_time <= 0:
        # print(1)
        satisfaction = 0
    else:
        satisfaction = stop_time/t_red

    ## pass the traffic light
    red_start = t_green + t_yellow
    red_end = t_green + t_yellow + t_red
    index = int(red_start/0.1)
    index_2 = int(red_end/0.1)
    # print(red_start,index,  ego_vehicle_state[index][2], len(ego_vehicle_state), ego_vehicle_state[index][1])
    # for i in range(len(ego_vehicle_state)):
    #     if (ego_vehicle_state[i][2] == red_start):
    #         print(ego_vehicle_state[i])
    #     elif (ego_vehicle_state[i][2]· == red_start) and (ego_vehicle_state[i][1]>200):
    #         satisfaction = 1

    # print(ego_velocity)
    # print(satisfaction,len(ego_vehicle_state))
    if len(ego_vehicle_state) <= index:
        satisfaction = 1
    elif len(ego_vehicle_state) > index:
        if ego_vehicle_state[index][1] > t_start + 1: ## not start y >= 200.8
            satisfaction = 1
    elif len(ego_vehicle_state) > index_2:
        if ego_vehicle_state[index_2][1] <= t_start - 4 : ## t_start = 200 ego vehicle reach the destination before 196 y<=196
            # print(ego_vehicle_state[index], index)
            # print(2)
            satisfaction = 1
        # elif ego_vehicle_state[index][1] > t_start+ 5: ## red light behind 200.8
        #     print(3)
        #     satisfaction = 1
    return satisfaction

def evaluate_cross_lane (ego_vehicle_state):
    satisfaction = 1
    total_time = 0
    # print(ego_vehicle_state)
    for i in range (len(ego_vehicle_state)):
        if ego_vehicle_state[i][0] >=10 and  ego_vehicle_state[i][1] <= 211.5:
            total_time += 1
    # print(total_time, len(ego_vehicle_state))
    if not total_time:
        return satisfaction
    else:
        return total_time/len(ego_vehicle_state)



if __name__=='__main__':

    file_dir_sce = os.getcwd() + '/2021_01_07_Brute_Froce_scenarios_2'
    file_dir_data = os.getcwd() + '/2021_01_07_Brute_Froce_datalog_2'

    fileList = os.listdir(file_dir_sce)
    fileList.sort()

    for i in range(len(fileList)):
        scenario_name = file_dir_sce  + '/' + fileList[i]
        uuixcode = fileList[i].split('.', 1)[0]
        # print(uuixcode)
        code = uuixcode.split("_",1)[1]
        log_name = file_dir_data + '/' + 'datalog_' + code + '.txt'
        # if code == "20210107171223_353_0d446fad65e94945bfe94cc342e6a0cf":
        #     continue


        print(log_name)


    # scenario_name = 'scenario_20210107171223_353_0d446fad65e94945bfe94cc342e6a0cf.json'
    # log_name = 'datalog_20210107171223_353_0d446fad65e94945bfe94cc342e6a0cf.txt'

        config = TurnRightConfigure()

        with open(scenario_name, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)

        traffic_light = ret_dic["traffic_signal"]
        st_obsList = ret_dic["static_obs"]
        dy_obsList  = ret_dic["dynamic_obs"]

        num_dynamic_obs = 3
        num_static_obs = 0

        ego_vehicle_state = []
        dynamic_vehicle_state = [[] for i in range(num_dynamic_obs)]
        static_vehicle_state = [[] for i in range(num_static_obs)]
        with open(log_name, 'r') as f:
            my_data = f.readlines()

            for line in my_data:
                data = line.split()
                if data[0] == "CRASH" or data[0] == "Register" or data[0] == "TIMEOUT":
                    break
                if len(data) == 8 and data[0] == "EGO_STATUS":
                    log = []
                    for i in range(1, len(data)):
                        log.append(float(data[i]))
                    if len(log) == 7:
                        ego_vehicle_state.append(log)

                elif len(data) == 10 and data[0] == "DYNAMIC_OBS_INFO":
                    log = []
                    # print(data)
                    if data[1] == '0' or data[1] == '1' or data[1] == '2':
                        for i in range(2, len(data)):
                            log.append(float(data[i]))
                            # print(log)
                        if len(log) == 8:
                            dynamic_vehicle_state[int(data[1])].append(log)
                    else:
                        break
                elif len(data) == 5 and data[0] == "STATIC_OBS_INFO":
                    log = []
                    for i in range(2, len(data)):
                        log.append(float(data[i]))
                        # print(log)
                    if len(log) == 3:
                        static_vehicle_state[int(data[1])].append(log)





        comfort1, comfort2 = evaluate_comfort(ego_vehicle_state, config)
        avg_speed, min_speed = evaluate_speed(ego_vehicle_state, config)
        # min_dis, avg_dis_satisfaction, min_dis_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
        #                                                                 dy_obsList, static_vehicle_state, st_obsList, config)
        min_dis, avg_dis_satisfaction, min_dis_satisfaction = evaluate_collision (ego_vehicle_state, dynamic_vehicle_state, dy_obsList, static_vehicle_state, st_obsList, config)
        print(min_dis, avg_dis_satisfaction, min_dis_satisfaction)
        avg_stable, min_stable = evaluate_stability(ego_vehicle_state, config)
        traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)
        cross_lane = evaluate_cross_lane(ego_vehicle_state)

        # result = [avg_stable, min_stable, avg_dis_satisfaction, min_dis_satisfaction, avg_speed, min_speed, traffic_light, cross_lane, comfort1,
        #           comfort2]
        #
        #
        # result = [avg_stable, avg_dis_satisfaction, min_dis_satisfaction, avg_speed, min_speed, traffic_light,
        #       cross_lane, comfort1, comfort2]

        result = [min_stable, min_dis, min_speed, traffic_light, cross_lane, comfort1, comfort2]
        print(result)