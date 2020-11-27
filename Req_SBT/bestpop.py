#!/usr/bin/python
# -*- coding:utf-8 -*-
from Configure import configure
import math
import globalvar

class BestPop:
    def __init__(self, configure):
        self.goal_num = configure.goal_num
        self.weights = [1] * configure.goal_num
        self.best = [1] * configure.goal_num
        self.pop = [1] * configure.goal_num
        self.round = 1
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

    def update_bestpop (self,result):
        for i in range (len(result)):
            # print(result)
            if result[i] < self.pop[i] :
                self.pop[i] = result[i]
        print("self.pop:", self.pop)
        if self.round % self.interval == 0: ## select the best every interval
            for i in range(len(result)):
                if result[i] < self.best[i]:
                    self.best[i] = result[i]

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
        if self.round % self.interval==0:
            for i in range (len(self.weights)):
                if self.pop[i] < 1:
                    self.weights[i] = (self.pop[i]-self.pop[i])/(1-self.pop[i])
                else:
                    self.weights[i] = 1

    def update_round (self,):
        print("\033[1;31m new round \033[0m")
        self.round = self.round + 1



