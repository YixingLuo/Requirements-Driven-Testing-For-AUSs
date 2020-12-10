#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import numpy as np
import shutil

class BestPop:
    def __init__(self, configure):
        self.goal_num = configure.goal_num
        self.weights = [1] * configure.goal_num
        self.best = []
        self.pop = []
        self.configure = configure
        self.round = 0
        self.generation = configure.population
        # self.curiteration = 0
        self.interval = configure.interval

    # def call_iteration (self, algorithm, idx):
    #     # print("evaluations: ", algorithm.termination_criterion.evaluations)
    #     # self.round = math.ceil(algorithm.termination_criterion.evaluations/self.generation)
    #     # self.curiteration = algorithm.termination_criterion.evaluations - self.round * self.generation
    #     self.curiteration = idx
    #     if  (self.curiteration + 1) % self.generation == 0:
    #         print("\033[1;31m new round \033[0m")
    #         self.round += 1
    #         print(self.round, self.curiteration)

    # def update_bestpop (self,):
    #     total_num = self.round * self.generation
    #     fileList = os.listdir(self.configure.file_dir_eval)
    #     fileList.sort()
    #     for i in range (1, self.generation+1):
    #         textname = self.configure.file_dir_eval + '/' + fileList[(self.round-2) * self.generation + i]
    #         result = np.loadtxt(textname)
    #         self.pop.append(result)
    #         if (self.round - 1) % self.interval == 0:
    #             self.best.append(result)


        # for i in range (len(result)):
        #     # print(result)
        #     if result[i] < self.pop[i] :
        #         self.pop[i] = result[i]
        # print("self.pop:", self.pop)
        # if (self.round - 1) % self.interval == 0: ## select the best every interval
        #     for i in range(len(result)):
        #         if result[i] < self.best[i]:
        #             self.best[i] = result[i]

    def add_results (self,):
        total_num = self.round * self.generation
        fileList = os.listdir(self.configure.file_dir_eval)
        fileList.sort()
        for i in range (self.generation):
            textname = self.configure.file_dir_eval + '/' + fileList[(self.round-2) * self.generation + i]
            print(textname)
            result = np.loadtxt(textname)
            self.pop.append(list(result))
            if (self.round - 1) % self.interval == 0:
                self.best.append(list(result))

    def clear(self,):
        filefolder = self.configure.file_dir_data
        shutil.rmtree(filefolder)
        os.mkdir(filefolder)

    # def update_weight (self,idx):
    #     if (idx + 1) % self.generation == 0 and self.round % self.interval==0:
    #         for i in range (len(self.weights)):
    #             if self.pop[i] < 1:
    #                 self.weights[i] = (self.pop[i]-self.pop[i])/(1-self.pop[i])
    #             else:
    #                 self.weights[i] = 1
    #
    # def update_round (self, idx):
    #     if (idx + 1) % self.generation == 0:
    #         self.round += 1

    def update_weight (self,):
        # if self.round == 2:
        #     for i in range(len(self.weights)):
        #         self.weights[i] = 0.5

        if (self.round - 1) % self.interval == 0:
            min_best = np.min(self.best, axis=0) # computes minimum in each column
            min_pop = np.min(self.pop, axis=0)
            # print(self.best, len(self.best),min_best)
            # print(self.pop, len(self.pop), min_pop)
            for i in range (len(self.weights)):
                if min_pop[i] < 1:
                    self.weights[i] = (min_best[i]-min_pop[i])/(1-min_pop[i])
                else:
                    self.weights[i] = 1
        print ("\033[1;32m New weights \033[0m", self.weights)

    def update_round (self,):
        # print("\033[1;31m new round \033[0m")
        self.round = self.round + 1



