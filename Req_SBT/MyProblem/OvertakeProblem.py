import random
from math import sqrt, exp, pow, sin

from jmetal.core.problem import FloatProblem, BinaryProblem, Problem
from jmetal.core.solution import FloatSolution, BinarySolution, CompositeSolution, IntegerSolution
# from MyAlgorithm.solution import FloatSolution
import numpy as np
import json
import random
from Configure import configure
import os
import time
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light
from MyScenario.overtake_2 import create_run_scenario_overtake
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
# from scoop import futures
import globalvar
from bestpop import BestPop

class OvertakeProblem(FloatProblem):
    """ Problem ZDT1Modified.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """
    def __init__(self,  M, file_dir_sce, file_dir_data, file_dir_eval, configure):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(OvertakeProblem, self).__init__()
        self.number_of_variables = 16
        self.number_of_objectives =  M
        self.number_of_constraints = 0
        self.config = configure
        # self.bestpop = pop

        self.obj_directions = [self.MINIMIZE] * M
        self.obj_labels = ['stable', 'acda', 'mini', 'speed', 'traffic_light', 'comfort']

        self.lower_bound = [self.config.ego_s0[0], self.config.ego_v0[0], self.config.start_s[0], self.config.end_s[0], self.config.green_time[0], self.config.yellow_time[0],
                    self.config.red_time[0], self.config.pos_s[0], self.config.pos_s[0], self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0],
                    self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0], self.config.start_time_2[0]]  # 决策变量下界
        self.upper_bound = [self.config.ego_s0[1], self.config.ego_v0[1], self.config.start_s[1], self.config.end_s[1], self.config.green_time[1], self.config.yellow_time[1],
                    self.config.red_time[1], self.config.pos_s[1], self.config.pos_s[1], self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1],
                    self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1], self.config.start_time_2[1]] # 决策变量上界

        self.file_dir_sce = file_dir_sce
        self.file_dir_data = file_dir_data
        self.file_dir_eval = file_dir_eval

    def evaluate(self, idx,  solution: FloatSolution) -> FloatSolution:
        # print(solution.__str__)
        Vars = solution.variables

        # L = np.array(solution.variables)
        # print(L.shape)

        result = create_run_scenario_overtake(Vars,idx, self.file_dir_sce, self.file_dir_data,
                                              self.file_dir_eval)

        solution.objectives = result

        print(solution.objectives)

        return solution


    def get_name(self):
        return 'OvertakeProblem'