#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np

"""
ego_state: X, Y, Time, Direction, Velocity, Acceleration Profile (aidx), Acceleration
dynamic_obstacle_state: dyn_obs->start_pos()[0], dyn_obs->start_pos()[1], dyn_obs->start_dir(),euclidean_distance(ego_x, ego_y, dynamic_obs_x, dynamic_obs_y), dynamic_obs_x,
dynamic_obs_y, dyn_obs->velo(), dyn_obs->acc());
"""


ego_vehicle_state = []
dynamic_vehicle_state0 = []
dynamic_vehicle_state1 = []
dynamic_vehicle_state2 = []
width = 1.8
length = 4.8


def evaluate_assured_clear_distance_ahead (ego_vehicle_state, dynamic_vehicle_state0,dynamic_vehicle_state1,dynamic_vehicle_state2):
    least_dis = 100
    if len(dynamic_vehicle_state0) > 0:
        for i in range(len(ego_vehicle_state)):
            ego_x_min = ego_vehicle_state[i][0] - width / 2
            ego_x_max = ego_vehicle_state[i][0] + width / 2
            ego_y_min = ego_vehicle_state[i][1] - length / 2
            ego_y_max = ego_vehicle_state[i][1] + length / 2

            ego_position = [[ego_x_min, ego_y_min],[ego_x_min, ego_y_max],[ego_x_max, ego_y_min],[ego_x_max, ego_y_max]]

            veh_x_min = dynamic_vehicle_state0[i][4] - width / 2
            veh_x_max = dynamic_vehicle_state0[i][4] + width / 2
            veh_y_min = dynamic_vehicle_state0[i][5] - length / 2
            veh_y_max = dynamic_vehicle_state0[i][5] + length / 2

            veh_position = [[veh_x_min, veh_y_min],[veh_x_min, veh_y_max],[veh_x_max, veh_y_min],[veh_x_max, veh_y_max]]

            for i in range(4):
                for j in range (4):
                    x = np.array(ego_position[i])
                    y = np.array(veh_position[j])
                    dis = np.sqrt(np.sum(np.square(x-y)))
                    if dis < least_dis:
                        least_dis = dis

            dis = dynamic_vehicle_state0[i][3]
            if dis < least_dis:
                least_dis = dis

    if len(dynamic_vehicle_state1) > 0:
        for i in range(len(ego_vehicle_state)):
            ego_x_min = ego_vehicle_state[i][0] - width / 2
            ego_x_max = ego_vehicle_state[i][0] + width / 2
            ego_y_min = ego_vehicle_state[i][1] - length / 2
            ego_y_max = ego_vehicle_state[i][1] + length / 2

            ego_position = [[ego_x_min, ego_y_min],[ego_x_min, ego_y_max],[ego_x_max, ego_y_min],[ego_x_max, ego_y_max]]

            veh_x_min = dynamic_vehicle_state1[i][4] - width / 2
            veh_x_max = dynamic_vehicle_state1[i][4] + width / 2
            veh_y_min = dynamic_vehicle_state1[i][5] - length / 2
            veh_y_max = dynamic_vehicle_state1[i][5] + length / 2

            veh_position = [[veh_x_min, veh_y_min],[veh_x_min, veh_y_max],[veh_x_max, veh_y_min],[veh_x_max, veh_y_max]]

            for i in range(4):
                for j in range (4):
                    x = np.array(ego_position[i])
                    y = np.array(veh_position[j])
                    dis = np.sqrt(np.sum(np.square(x-y)))
                    if dis < least_dis:
                        least_dis = dis

            dis = dynamic_vehicle_state1[i][3]
            if dis < least_dis:
                least_dis = dis
    if len(dynamic_vehicle_state2) > 0:
        for i in range(len(ego_vehicle_state)):
            ego_x_min = ego_vehicle_state[i][0] - width / 2
            ego_x_max = ego_vehicle_state[i][0] + width / 2
            ego_y_min = ego_vehicle_state[i][1] - length / 2
            ego_y_max = ego_vehicle_state[i][1] + length / 2

            ego_position = [[ego_x_min, ego_y_min],[ego_x_min, ego_y_max],[ego_x_max, ego_y_min],[ego_x_max, ego_y_max]]

            veh_x_min = dynamic_vehicle_state2[i][4] - width / 2
            veh_x_max = dynamic_vehicle_state2[i][4] + width / 2
            veh_y_min = dynamic_vehicle_state2[i][5] - length / 2
            veh_y_max = dynamic_vehicle_state2[i][5] + length / 2

            veh_position = [[veh_x_min, veh_y_min],[veh_x_min, veh_y_max],[veh_x_max, veh_y_min],[veh_x_max, veh_y_max]]

            for i in range(4):
                for j in range (4):
                    x = np.array(ego_position[i])
                    y = np.array(veh_position[j])
                    dis = np.sqrt(np.sum(np.square(x-y)))
                    if dis < least_dis:
                        least_dis = dis
            dis = dynamic_vehicle_state2[i][3]
            if dis < least_dis:
                least_dis = dis

    return least_dis

def evaluate_conformt (ego_vehicle_state)
    comfort = 0

    for i in range()

    return comfort


with open('datalog_1.txt', 'r') as f:
    my_data = f.readlines() #txt中所有字符串读入data，得到的是一个list
    # 对list中的数据做分隔和类型转换
    for line in my_data:
       line_data = line.split()
       numbers_float = map(float, line_data) #转化为浮点数

    for line in my_data:
        data = line.split()
        if data[0] == "EGO_STATUS":
            log = []
            for i in range (1, len(data)):
                log.append(float(data[i]))
            ego_vehicle_state.append(log)
    # print(ego_vehicle_state)

    for line in my_data:
        data = line.split()
        if data[0] == "DYNAMIC_OBS_INFO":
            log = []
            if data[1] == "0":
                for i in range (2, len(data)):
                    log.append(float(data[i]))
                dynamic_vehicle_state0.append(log)
            if data[1] == "1":
                for i in range (2, len(data)):
                    log.append(float(data[i]))
                dynamic_vehicle_state1.append(log)
            if data[1] == "2":
                for i in range (2, len(data)):
                    log.append(float(data[i]))
                dynamic_vehicle_state2.append(log)

# print(dynamic_vehicle_state0)
value = evaluate_assured_clear_distance_ahead(ego_vehicle_state, dynamic_vehicle_state0, dynamic_vehicle_state1, dynamic_vehicle_state2)
print(value)


