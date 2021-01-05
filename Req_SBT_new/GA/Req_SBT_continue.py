# -*- coding: utf-8 -*-

from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.multiobjective.random_search import RandomSearch
# from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII
from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import MultiprocessEvaluator, SequentialEvaluator
from MyAlgorithm.nsgaiii import NSGAIII
# from MyAlgorithm.nsgaii import NSGAII
# from MyAlgorithm.random_search import RandomSearch
# from MyAlgorithm.termination_criterion import StoppingByEvaluations
# from MyAlgorithm.evaluator import MultiprocessEvaluator
from Settings.CarBehindAndInFrontConfigureCon import CarBehindAndInFrontConfigureCon
import os
import time
from CarBehindAndInFrontProblem import CarBehindAndInFrontProblem
from jmetal.util.observer import ProgressBarObserver
import numpy as np


def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path,  'w')
    return full_path

data_folder = os.getcwd() + '/Overtake_Datalog_continue_' + str(time.strftime("%Y_%m_%d_%H"))
if not os.path.exists(data_folder):
    os.mkdir(data_folder)


if __name__ == '__main__':

    target_dir = data_folder
    search_round = 1000
    population = 50

    continue_flag = 0
    variables = []
    Configuration = CarBehindAndInFrontConfigureCon(target_dir, population, search_round)
    Goal_num = Configuration.goal_num

    if continue_flag == 1:
        vars_file_name = 'Overtake_Datalog_'
        fileList = os.listdir(vars_file_name)
        fileList.sort()
        total_length = len(fileList)
        for i in range(total_length-population, total_length):
            textname = vars_file_name + '/' + fileList[i]
            pop = np.loadtxt(textname)
            variables.append(pop)

    """===============================实例化问题对象============================"""
    problem = CarBehindAndInFrontProblem(Goal_num, Configuration)

    """=================================算法参数设置============================"""
    max_evaluations = Configuration.maxIterations

    algorithm = NSGAIII(initial_population=variables,
                        continue_flag=continue_flag,
                        population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
                        # population_evaluator=SequentialEvaluator(),
                        problem=problem,
                        population_size=Configuration.population,
                        reference_directions=UniformReferenceDirectionFactory(Configuration.goal_num,
                                                                              n_points=Configuration.population - 1),
                        # offspring_population_size = Configuration.population,
                        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables,
                                                    distribution_index=20),
                        crossover=SBXCrossover(probability=1.0, distribution_index=20),
                        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                        # termination_criterion = StoppingByQualityIndicator(quality_indicator=HyperVolume, expected_value=1,
                        #                                                  degree=0.9)
                        # selection = BinaryTournamentSelection()
                        )

    """==========================调用算法模板进行种群进化========================="""
    progress_bar = ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(progress_bar)
    algorithm.run()
    front = algorithm.get_result()

    """==================================输出结果=============================="""
    # Save results to file
    print_function_values_to_file(front, os.path.join(target_dir, '/FUN.' + algorithm.label))
    print_variables_to_file(front, os.path.join(target_dir, '/VAR.' + algorithm.label))

    print(f'Algorithm: ${algorithm.get_name()}')
    print(f'Problem: ${problem.get_name()}')
    print(f'Computing time: ${algorithm.total_computing_time}')