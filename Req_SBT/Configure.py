#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import os
import shutil

class configure:
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
        self.duration = 60
        self.population = 50
        self.goal_num = 6
        self.maxIterations = 10000
        self.searchTimeout = 360000
        self.interval = 20
        self.num_variables = 16
        self.PoolType = "Thread"
        # self.PoolType = "Process"

        ## ego
        self.ego_s0 = [10, 20]
        self.ego_v0 = [10, 16]

        ## traffic_signals
        self.start_s = [80, 85]
        self.end_s = [90, 95]
        self.green_time = [10, 15]
        self.yellow_time = [1, 2]
        self.red_time = [2, 3]

        ## static_obstacle
        self.pos_s = [60, 80]

        ## dynamic_obstacle_1
        self.pos_y_1 = [30, 60]
        self.velo_1 = [4, 16]
        self.acc_1 = [0, 3]


        ## dynamic_obstacle_2
        self.pos_y_2 = [5, 30]
        self.velo_2 = [4, 16]
        self.acc_2 = [0, 3]
        self.start_time_2 = [0,2]

        ## algorithm
        self.algorithm = "NSGA_II" ## "NSGA_II": NSGA_II, "Adapt": NSGA_II_Goal_Adapt

        self.file_dir_sce = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_scenarios_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_sce):
            os.mkdir(self.file_dir_sce)

        self.file_dir_data = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_datalog_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_data):
            os.mkdir(self.file_dir_data)

        self.file_dir_eval = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_' + str(self.algorithm) + '_results_' + str(
            self.maxIterations)
        if not os.path.exists(self.file_dir_eval):
            os.mkdir(self.file_dir_eval)



    # def createfolders (self,):
    #     self.file_dir_sce = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_scenarios_' + str(self.maxIterations)
    #     if os.path.exists(self.file_dir_sce):
    #         shutil.rmtree(self.file_dir_sce)
    #         os.mkdir(self.file_dir_sce)
    #     else:
    #         os.mkdir(self.file_dir_sce)
    #
    #     self.file_dir_data = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_datalog_' + str(self.maxIterations)
    #     if os.path.exists(self.file_dir_data):
    #         shutil.rmtree(self.file_dir_data)
    #         os.mkdir(self.file_dir_data)
    #     else:
    #         os.mkdir(self.file_dir_data)
    #
    #     self.file_dir_eval = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_results_' + str(self.maxIterations)
    #     if os.path.exists(self.file_dir_eval):
    #         shutil.rmtree(self.file_dir_eval)
    #         os.mkdir(self.file_dir_eval)
    #     else:
    #         os.mkdir(self.file_dir_eval)







