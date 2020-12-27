#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import os
import shutil
# import psutil

class CarBehindAndInFrontConfigure:
    def __init__(self):
        # self.auto_close_on_reach_the_objective= 1
        # self.auto_close_x_position = 10
        # self.auto_close_y_position = 0
        # self.mapt_no = 2
        # self.horizon = 80
        # self.speed_horizon_factor = 3.0
        # self.lon_interval = 10.0
        # self.lat_interval = 1.75
        # self.road_width = 3.5
        # self.infinity_cost = 100000000
        # self.sampling_step = 0.1
        self.k_thr = 0.172
        self.ego_width = 1.8
        self.ego_length = 4.8
        self.k_limit = 5.0
        # self.latg_max_soft = 2.94
        # self.curve_rate_limit = 1
        self.time_step = 0.1
        # self.lane_cost_factor = 1.5
        # self.map_type = 1
        # self.dynamic_obstacle_lethal_cost = 100000000
        # self.dynamic_obstacle_high_cost = 10000
        # self.minimum_horizon = 30
        # self.total_time_weight = 1.0
        # self.total_dist_weight = 1.0
        # self.max_eval_trajs = 200000
        # self.pena_low_speed = 100
        # self.auto_close_on_crash = 1
        # self.same_acc_bonus = -10

        ## requirement related
        self.assured_clear_distance_ahead = 1
        self.minimumseperation = 1.7
        self.a_max_soft = 0.98
        self.a_min_soft = -2.94
        self.speed_limit = 16.67
        self.speed_max = 33.3
        self.duration = 90
        self.population = 50
        self.goal_num = 7
        self.search_round = 50*8
        self.searchTimeout = 360000
        self.num_variables = 19
        self.PoolType = "Thread"
        # self.PoolType = "Process"
        # self.ProcessNum = psutil.cpu_count()
        self.ProcessNum = 32
        self.maxIterations = self.population * self.search_round

        ## ego
        self.ego_s0 = [10, 30]
        self.ego_v0 = [8, 16]

        ## traffic_signals
        self.start_s = [70, 75]
        self.end_s = [90, 95]
        self.green_time = [5, 10]
        self.yellow_time = [1, 2]
        self.red_time = [2, 4]

        ## static_obstacle
        # self.pos_s_1 = [60, 70]
        # self.pos_s_2 = [70, 80]

        ## dynamic_obstacle_1
        self.pos_y_1 = [40, 60]
        self.velo_1 = [4, 16]
        self.acc_1 = [0, 3]
        self.start_time_1 = [0, 0]


        ## dynamic_obstacle_2
        self.pos_y_2 = [5, 25]
        self.velo_2 = [4, 16]
        self.acc_2 = [0, 3]
        self.start_time_2 = [0, 2]

        ## dynamic_obstacle_3
        self.pos_y_3 = [30, 90]
        self.velo_3 = [4, 16]
        self.acc_3 = [0, 3]
        self.start_time_3 = [0, 2]

        ## algorithm
        ## "NSGA_II": NSGA_II, "NSGA_III": NSGA_III ,"NSGA_III_Adapt": NSGA_II_Goal_Adapt
        self.algorithm = "Random"

        self.file_dir_sce = os.getcwd() + '/Datalog_' + str(time.strftime("%Y_%m_%d_%H")) + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_scenarios_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_sce):
            os.mkdir(self.file_dir_sce)

        self.file_dir_data = os.getcwd() + '/Datalog_' + str(time.strftime("%Y_%m_%d_%H")) + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_datalog_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_data):
            os.mkdir(self.file_dir_data)

        self.file_dir_eval = os.getcwd() + '/Datalog_' + str(time.strftime("%Y_%m_%d_%H")) + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_results_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_eval):
            os.mkdir(self.file_dir_eval)

        self.file_dir_var = os.getcwd() + '/Datalog_' + str(time.strftime("%Y_%m_%d_%H")) + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_variable_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_var):
            os.mkdir(self.file_dir_var)







