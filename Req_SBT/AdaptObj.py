# -*- coding: utf-8 -*-
""" QuickStart """
import numpy as np
import geatpy as ea
import json
import random
from Configure import configure
import os
import time
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light
from MyScenario.overtake import create_run_scenario_overtake
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
# from scoop import futures
import globalvar as gl
from bestpop import BestPop



class AdaptObj(ea.Problem):  # 继承Problem父类
    def __init__(self, M, file_dir_sce, file_dir_data, file_dir_eval, configure):

        name = 'AdaptObj'  # 初始化name（函数名称，可以随意设置）
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）

        # Dim = 19  # 初始化Dim（决策变量维数）
        # varTypes = [  0,  0,   0,   0,  0, 0,   0,   0,  0, 0,  0,   0,  0, 0,   0,   0,  1, 1, 1] # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        # lb =       [150,  8,  20, 212,  4, 0,  20, 205,  4, 0,  1, 150,  4, 0,   0,  50, 10, 1, 4]  # 决策变量下界
        # ub =       [180, 16, 100, 217, 16, 3, 120, 210, 16, 3,  6, 250, 16, 3, 240, 250, 20, 3, 6] # 决策变量上界
        # lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        # ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）

        self.config = configure

        Dim = 16  # 初始化Dim（决策变量维数）
        # varTypes = [  0,  0,   0,   0,  0, 0,   0,   0,  0, 0,  0,   0,  0, 0,   0,   0,  1, 1, 1] # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb =       [self.config.ego_s0[0], self.config.ego_v0[0], self.config.start_s[0], self.config.end_s[0], self.config.green_time[0], self.config.yellow_time[0],
                    self.config.red_time[0], self.config.pos_s[0], self.config.pos_s[0], self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0],
                    self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0], self.config.start_time_2[0]]  # 决策变量下界
        ub =       [self.config.ego_s0[1], self.config.ego_v0[1], self.config.start_s[1], self.config.end_s[1], self.config.green_time[1], self.config.yellow_time[1],
                    self.config.red_time[1], self.config.pos_s[1], self.config.pos_s[1], self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1],
                    self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1], self.config.start_time_2[1]] # 决策变量上界
        Dim = len(lb)
        # print(Dim)
        varTypes = [0] * Dim
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）


        self.file_dir_sce = file_dir_sce
        self.file_dir_data = file_dir_data
        self.file_dir_eval = file_dir_eval
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

        # 设置用多线程还是多进程
        self.PoolType = configure.PoolType

        if self.PoolType == 'Thread':
            self.pool = ThreadPool(4)  # 设置池的大小
        elif self.PoolType == 'Process':
            num_cores = int(mp.cpu_count())  # 获得计算机的核心数
            self.pool = ProcessPool(num_cores)  # 设置池的大小


    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵

        result = create_run_scenario_overtake (Vars, self.file_dir_sce, self.file_dir_data, self.file_dir_eval)
        pop.ObjV = result
        bestpop = gl.get_value('BestPop')
        bestpop.update_weight()

        # args = list(zip(list(range(pop.sizes)), [Vars] * pop.sizes, [self.data] * pop.sizes, [
        #     self.dataTarget] * pop.sizes))  # pop.sizes就是种群的规模,args=[[种群大小],[决策变量*种群大小],[特征*种群大小],[分类target*种群大小]]，args含义见下面subAimFunc(args)函数

        # args = list(zip(list(range(pop.sizes)), [Vars] * pop.sizes,
                        # [self.file_dir_sce] * pop.sizes, [self.file_dir_data] * pop.sizes, [self.file_dir_eval] * pop.sizes))



        # if self.PoolType == 'Thread':
        #     pop.ObjV =  np.array(list(self.pool.map(subAimFunc, args)))
        # elif self.PoolType == 'Process':
        #     result = self.pool.map_async(subAimFunc, args)
        #     result.wait()
        #     pop.ObjV = np.array(result.get())

        # pop.ObjV = np.array(list(futures.map(subAimFunc, args)))

def subAimFunc(args):  # 单独计算单个个体的目标函数值
    i = args[0]
    Vars = args[1]
    file_dir_sce = args[2]
    file_dir_data = args[3]
    file_dir_eval = args[4]
    ObjV_i = create_run_scenario_overtake(Vars, file_dir_sce, file_dir_data, file_dir_eval)
    return ObjV_i