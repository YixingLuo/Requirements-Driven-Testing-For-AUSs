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
import globalvar as gl
from bestpop import BestPop
from multiprocessing import freeze_support,Lock, Value

class OvertakeProblem(FloatProblem):
    """ Problem ZDT1Modified.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """
    def __init__(self,  M, configure, bestpop):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(OvertakeProblem, self).__init__()
        self.number_of_variables = configure.num_variables
        self.number_of_objectives =  configure.goal_num
        self.number_of_constraints = 0
        self.config = configure
        self.bestpop = bestpop
        # self.mutux = Value('i', 0 )
        # self.manager = multiprocessing.Manager()

        self.obj_directions = [self.MINIMIZE] * M
        self.obj_labels = ['stable', 'acda', 'mini', 'speed', 'traffic_light', 'comfort']

        self.lower_bound = [self.config.ego_s0[0], self.config.ego_v0[0], self.config.start_s[0], self.config.end_s[0], self.config.green_time[0], self.config.yellow_time[0],
                    self.config.red_time[0], self.config.pos_s[0], self.config.pos_s[0], self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0],
                    self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0], self.config.start_time_2[0]]  # 决策变量下界
        self.upper_bound = [self.config.ego_s0[1], self.config.ego_v0[1], self.config.start_s[1], self.config.end_s[1], self.config.green_time[1], self.config.yellow_time[1],
                    self.config.red_time[1], self.config.pos_s[1], self.config.pos_s[1], self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1],
                    self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1], self.config.start_time_2[1]] # 决策变量上界

        # self.file_dir_sce = file_dir_sce
        # self.file_dir_data = file_dir_data
        # self.file_dir_eval = file_dir_eval

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        # print(solution.__str__)
        Vars = solution.variables

        # L = np.array(solution.variables)
        # print(L.shape)

        # bestlog = gl.get_value('BestPop')
        # print("\033[1;32m round: \033[0m",bestlog.round)

        result = create_run_scenario_overtake(Vars, self.bestpop, self.config)

        solution.objectives = result

        # lock = Lock()
        # with lock:
        #     time.sleep(1)
        # lock.acquire()
        # self.bestpop.add_results(result)
        # print(self.bestpop.pop)
        # lock.release()

        # Lock = threading.Lock()
        # Lock.acquire()
        # print("\033[1;32m round: \033[0m", self.bestpop.round)
        # print("\033[1;32m before: bestlog.pop \033[0m", self.bestpop.pop)
        # self.bestpop.update_bestpop(result)
        # print("\033[1;32m after: bestlog.pop \033[0m", self.bestpop.pop)
        # Lock.release()

        # global BestPopulation
        # Lock = threading.Lock()
        # Lock.acquire()
        # BestPopulation = gl.get_value('BestPop')
        # print("\033[1;32m round: \033[0m",BestPopulation.round)
        # print("\033[1;32m before: bestlog.pop \033[0m", BestPopulation.pop)
        # BestPopulation.update_bestpop(result)
        # gl.set_value('BestPop', BestPopulation)
        # print("\033[1;32m after: bestlog.pop \033[0m", BestPopulation.pop)
        # Lock.release()

        # with bestpop.get_lock():  # 直接调用get_lock()函数获取锁
        #
        # # bestlog = globalvar.get_value('BestPop')
        #     bestpop.update_bestpop(result)
        #
        # # globalvar.set_value('BestPop', bestlog)
        #     print("\033[1;32m bestlog.pop \033[0m", bestpop.pop)

        return solution


    def get_name(self):
        return 'OvertakeProblem'