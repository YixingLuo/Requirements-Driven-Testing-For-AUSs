# -*- coding: utf-8 -*-

from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.operator.selection import RankingAndFitnessSelection,BestSolutionSelection, RouletteWheelSelection
# from MyAlgorithm.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import MultiprocessEvaluator, SequentialEvaluator
from MyAlgorithm.evaluator import MultiprocessEvaluator
from jmetal.util.observer import ProgressBarObserver
from MyAlgorithm.nsgaiii_2 import NSGAIII
from MyAlgorithm.nsgaii import NSGAII
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
import os
import time
from CarBehindAndInFrontProblem import CarBehindAndInFrontProblem
import csv
import numpy
import random

def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(
        Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    return full_path




# data_folder = os.getcwd() + '/Overtake_Datalog_Req1_2021_01_03_14'

if __name__ == '__main__':


    data_folder = os.getcwd() + '/Overtake_Datalog_Req3_nsgaii_' + str(time.strftime("%Y_%m_%d_%H"))
    # print(data_folder)
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    # search_round_list = [1, 10, 10, 10, 10, 20, 110, 110]
    # search_round_list = [1, 10, 20, 30, 40, 50, 60, 70]
    search_round_list = [100, 100, 100, 100, 100, 100, 100, 100]
    # goal_selection_index = random.sample(range(0,128),128)
    # goal_selection_index = [idx for idx in range(128)]

    total_round = 200
    round_index = 0
    population = 50
    search_round = 0

    target_dir = data_folder
    # file_name = os.path.join(target_dir, 'goal_selection_index.txt')
    # numpy.savetxt(file_name, goal_selection_index, fmt="%d")  # 保存为整数

    target_values = [-1 / 5.0, 0, -16.67, 1 - (1e-3), 0 - (1e-3), -0.075, -0.3]

    priority_list = []
    with open("priority_list.csv") as csvfile:
        csv_file = csv.reader(csvfile)
        for row in csv_file:
            priority_list.append(row)
        priority_list = [[float(x) for x in row] for row in priority_list]
    priority_list = numpy.array(priority_list)

    violation_pattern_to_search = []
    evaluation = []
    searched_violation_pattern = []
    pattern_count = numpy.zeros(priority_list.shape[0])
    # pattern_count = numpy.loadtxt("pattern_count_0.txt")
    # searched_violation_pattern = numpy.loadtxt("searched_violation_pattern_0.txt")

    while total_round > 0:

        # for round_index in range (total_round):

        if round_index == 0:
            goal_index = 91
            # goal_index = 110
            goal_selection_flag = priority_list[goal_index]
            print(goal_selection_flag)
            search_round = 100
            if total_round < search_round:
                search_round = total_round

            # total_round = total_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_index, population, target_dir, round_index, search_round)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval
            searched_violation_pattern.append(goal_index)
        else:
            # goal_index = 91
            goal_index = 110
            goal_selection_flag = priority_list[goal_index]
            print(goal_selection_flag)
            search_round = 100
            if total_round < search_round:
                search_round = total_round

            # total_round = total_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_index, population, target_dir, round_index, search_round)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval
            searched_violation_pattern.append(goal_index)

        # print(searched_violation_pattern)
        Goal_num = Configuration.goal_num

        """==================================输出结果=============================="""
        # Save results to file
        file_name = target_dir + '/searched_violation_pattern_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, searched_violation_pattern, fmt="%d")  # 保存为整数
        file_name = target_dir + '/violation_pattern_to_search_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, violation_pattern_to_search, fmt="%d")  # 保存为整数
        file_name = target_dir + '/pattern_count_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, pattern_count, fmt="%d")  # 保存为整数

        """===============================实例化问题对象============================"""
        problem = CarBehindAndInFrontProblem(Goal_num, Configuration)

        """=================================算法参数设置============================"""
        max_evaluations = Configuration.maxIterations
        # StoppingEvaluator = StoppingByEvaluations(max_evaluations=max_evaluations, problem=problem)
        StoppingEvaluator = StoppingByEvaluations(max_evaluations=max_evaluations)

        # algorithm = NSGAIII(target_pattern=goal_selection_flag,
        #                     target_value_threshold=target_values,
        #                     population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
        #                     # population_evaluator=SequentialEvaluator(),
        #                     problem=problem,
        #                     population_size=Configuration.population,
        #                     reference_directions=UniformReferenceDirectionFactory(Configuration.goal_num,
        #                                                                           n_points=Configuration.population - 1),
        #                     # offspring_population_size = Configuration.population,
        #                     mutation=PolynomialMutation(probability=0.01,
        #                                                 distribution_index=20),
        #                     crossover=SBXCrossover(probability=1, distribution_index=20),
        #                     # selection=RouletteWheelSelection(),
        #                     termination_criterion=StoppingEvaluator
        #                     # termination_criterion = StoppingByQualityIndicator(quality_indicator=HyperVolume, expected_value=1,
        #                     #                                                  degree=0.9)
        #                     # selection = BinaryTournamentSelection()
        #                     )

        algorithm = NSGAII(
            target_pattern=goal_selection_flag,
            target_value_threshold=target_values,
            problem=problem,
            population_size=Configuration.population,
            offspring_population_size=Configuration.population,
            population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
            # population_evaluator=SequentialEvaluator(),
            mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
            crossover=SBXCrossover(probability=1.0, distribution_index=20),
            termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
        )

        """==========================调用算法模板进行种群进化========================="""
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        front = algorithm.get_result()



        # Save results to file
        fun_name = 'FUN.' + str(round_index) + '_' + algorithm.label
        print_function_values_to_file(front, os.path.join(target_dir, fun_name))
        var_name = 'VAR.' + str(round_index) + '_' + algorithm.label
        print_variables_to_file(front, os.path.join(target_dir, var_name))

        print(f'Algorithm: ${algorithm.get_name()}')
        print(f'Problem: ${problem.get_name()}')
        print(f'Computing time: ${algorithm.total_computing_time}')

        search_round = int(StoppingEvaluator.evaluations / population)
        total_round = total_round - search_round
        print("real round: ", search_round, "idx: ", round_index, "left: ", total_round)
        round_index = round_index + 1
