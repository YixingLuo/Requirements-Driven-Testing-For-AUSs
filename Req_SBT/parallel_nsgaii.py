from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem.multiobjective.zdt import ZDT1Modified
# from jmetal.util.evaluator import MultiprocessEvaluator
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from MyAlgorithm.evaluator import SequentialEvaluator, MultiprocessEvaluator, MapEvaluator
from jmetal.util.comparator import DominanceComparator, Comparator, MultiComparator
from jmetal.operator import BinaryTournamentSelection

import numpy as np
import sys
import json
import random
from Configure import configure
import os
import time
import globalvar
import codecs
import multiprocessing as mp
from bestpop import BestPop
from MyProblem.OvertakeProblem import OvertakeProblem

config = configure()
bestpop = BestPop(config)

Goal_num = config.goal_num

file_dir_sce = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_scenarios_' + str(config.maxIterations)
if not os.path.exists(file_dir_sce):
    os.mkdir(file_dir_sce)

file_dir_data = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_datalog_' + str(config.maxIterations)
if not os.path.exists(file_dir_data):
    os.mkdir(file_dir_data)

file_dir_eval = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_results_' + str(config.maxIterations)
if not os.path.exists(file_dir_eval):
    os.mkdir(file_dir_eval)

globalvar._init()



if __name__ == '__main__':



    """===============================实例化问题对象============================"""
    problem = OvertakeProblem(Goal_num, file_dir_sce, file_dir_data, file_dir_eval, config)

    """=================================算法参数设置============================"""
    max_evaluations = config.maxIterations

    # algorithm = NSGAII(
    #     problem=problem,
    #     population_size=30,
    #     offspring_population_size=30,
    #     mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    #     crossover=SBXCrossover(probability=1.0, distribution_index=20),
    #     termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations),
    #     population_evaluator = SequentialEvaluator()
    # )

    algorithm = NSGAII(
        population_evaluator=MultiprocessEvaluator(8),
        problem=problem,
        population_size = config.population,
        offspring_population_size = config.population,
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
        termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations)
        # selection = BinaryTournamentSelection()
    )


    globalvar.set_value('Configure', config)
    globalvar.set_value('Problem', problem)
    globalvar.set_value('BestPop', bestpop)
    globalvar.set_value('Algorithm', algorithm)


# if __name__ == '__main__':

    # algorithm = NSGAII(
    #     population_evaluator=MultiprocessEvaluator(8),
    #     problem=problem,
    #     population_size=config.population,
    #     offspring_population_size=config.population,
    #     mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    #     crossover=SBXCrossover(probability=1.0, distribution_index=20),
    #     termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
    #     # selection = BinaryTournamentSelection()
    # )

    # globalvar.set_value('Algorithm', algorithm)

    # algorithm.population_evaluator = MultiprocessEvaluator(8)
    # algorithm.population_evaluator = MapEvaluator(8)
    # algorithm.population_evaluator = SequentialEvaluator()
    """==========================调用算法模板进行种群进化========================="""
    algorithm.run()
    front = algorithm.get_result()

    """==================================输出结果=============================="""
    # Save results to file
    print_function_values_to_file(front, 'FUN.' + algorithm.label)
    print_variables_to_file(front, 'VAR.'+ algorithm.label)

    print(f'Algorithm: ${algorithm.get_name()}')
    print(f'Problem: ${problem.get_name()}')
    print(f'Computing time: ${algorithm.total_computing_time}')

