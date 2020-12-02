from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII, UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem.multiobjective.zdt import ZDT1Modified
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from MyAlgorithm.evaluator import SequentialEvaluator, MultiprocessEvaluator, MapEvaluator
# from jmetal.util.evaluator import SequentialEvaluator,MultiprocessEvaluator
from jmetal.util.comparator import DominanceComparator, Comparator, MultiComparator
from jmetal.operator import BinaryTournamentSelection

import numpy as np
import sys
import json
import random
from Configure import configure
import os
import time
import globalvar as gl
import codecs
import multiprocessing as mp
from bestpop import BestPop
from MyProblem.OvertakeProblem import OvertakeProblem
from multiprocessing import Process, Value,freeze_support,Lock



def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path,  'w')
    return full_path



# global _global_dict
# _global_dict = {}
# _global_dict['Configure'] = Configuration
# _global_dict['BestPop'] =  BestPopulation

# gl._init()
# gl.set_value('Configure', Configuration)
# gl.set_value('Problem', problem)
# gl.set_value('BestPop', BestPopulation)

# config = Value('Configure', config)
# bestpop = Value('BestPop', bestpop)


if __name__ == '__main__':




    # freeze_support()

    # global Configuration
    Configuration = configure()
    # global BestPopulation
    BestPopulation = BestPop(Configuration)
    # config.createfolders()
    Goal_num = Configuration.goal_num

    file_name = text_create(Configuration )
    output = sys.stdout
    outputfile = codecs.open(file_name,  'w', 'utf-8')
    sys.stdout = outputfile

    """===============================实例化问题对象============================"""
    problem = OvertakeProblem(Goal_num, Configuration, BestPopulation)

    """=================================算法参数设置============================"""
    max_evaluations = Configuration.maxIterations

    if Configuration.algorithm == "NSGA_II":
        algorithm = NSGAII(
            population_evaluator=MultiprocessEvaluator(8),
            # population_evaluator=SequentialEvaluator(),
            problem=problem,
            population_size = Configuration.population,
            offspring_population_size = Configuration.population,
            mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
            crossover=SBXCrossover(probability=1.0, distribution_index=20),
            termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations)
            # selection = BinaryTournamentSelection()
        )
    elif Configuration.algorithm == "NSGA_III":
        algorithm = NSGAIII(
            population_evaluator=MultiprocessEvaluator(8),
            problem=problem,
            population_size = Configuration.population,
            reference_directions=UniformReferenceDirectionFactory(Configuration.goal_num, n_points= Configuration.population - 1),
            # offspring_population_size = Configuration.population,
            mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
            crossover=SBXCrossover(probability=1.0, distribution_index=20),
            termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations)
            # selection = BinaryTournamentSelection()
        )

    # globalvar.set_value('Algorithm', algorithm)

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

    outputfile.close()

