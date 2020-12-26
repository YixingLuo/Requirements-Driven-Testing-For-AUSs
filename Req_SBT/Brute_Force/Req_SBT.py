# -*- coding: utf-8 -*-

# from jmetal.algorithm.multiobjective.nsgaii import NSGAII
# from jmetal.algorithm.multiobjective.random_search import RandomSearch
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII
from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import SequentialEvaluator,MultiprocessEvaluator
# from MyAlgorithm.nsgaiii import NSGAIII
from MyAlgorithm.nsgaii import NSGAII
from MyAlgorithm.random_search import RandomSearch
# from MyAlgorithm.termination_criterion import StoppingByEvaluations
# from MyAlgorithm.evaluator import MultiprocessEvaluator
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
import os
import time
# from trash.initial_files.bestpop import BestPop
from CarBehindAndInFront import CarBehindAndInFront
from jmetal.util.observer import ProgressBarObserver
import random
import numpy


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

    goal_selection_index = random.sample(range(1,129),50)
    total_round = len(goal_selection_index)
    population = 20
    search_round = 20
    numpy.savetxt('goal_selection_index.txt', goal_selection_index, fmt="%d")  # 保存为整数

    # round_idx = 0
    for round_idx in range (total_round):

        # print(round_idx, goal_selection_index[round_idx])
        # global Configuration
        Configuration = CarBehindAndInFrontConfigure(goal_selection_index[round_idx],population,search_round)
        # global BestPopulation
        # BestPopulation = BestPop(Configuration)
        # config.createfolders()
        Goal_num = Configuration.goal_num

        # file_name = text_create(Configuration )
        # output = sys.stdout
        # outputfile = codecs.open(file_name,  'w', 'utf-8')
        # sys.stdout = outputfile

        """===============================实例化问题对象============================"""
        problem = CarBehindAndInFront(Goal_num, Configuration)

        """=================================算法参数设置============================"""
        max_evaluations = population * search_round
        # print(max_evaluations)

        if Configuration.algorithm == "NSGA_II":
            algorithm = NSGAII(
                population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
                # population_evaluator=SequentialEvaluator(),
                problem=problem,
                population_size = Configuration.population,
                offspring_population_size = Configuration.population,
                mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
                crossover=SBXCrossover(probability=1.0, distribution_index=20),
                termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations)
                # termination_criterion = StoppingByQualityIndicator(quality_indicator=FitnessValue, expected_value=1, degree=0.9)
                # selection = BinaryTournamentSelection()
            )
        elif Configuration.algorithm == "NSGA_III" or Configuration.algorithm == "Brute_Froce":
            algorithm = NSGAIII(
                population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
                # population_evaluator=SequentialEvaluator(),
                problem=problem,
                population_size = Configuration.population,
                reference_directions=UniformReferenceDirectionFactory(Configuration.goal_num, n_points= Configuration.population - 1),
                # offspring_population_size = Configuration.population,
                mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
                crossover=SBXCrossover(probability=1.0, distribution_index=20),
                termination_criterion = StoppingByEvaluations(max_evaluations=max_evaluations)
                # termination_criterion = StoppingByQualityIndicator(quality_indicator=HyperVolume, expected_value=1,
                #                                                  degree=0.9)
                # selection = BinaryTournamentSelection()
            )
        elif Configuration.algorithm == 'Random':
            algorithm = RandomSearch(
                problem=problem,
                termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
            )

        # globalvar.set_value('Algorithm', algorithm)

        """==========================调用算法模板进行种群进化========================="""
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        front = algorithm.get_result()

        """==================================输出结果=============================="""
        # Save results to file
        print_function_values_to_file(front, 'FUN.' + str(goal_selection_index[round_idx]) + '_' + algorithm.label)
        print_variables_to_file(front, 'VAR.' + str(goal_selection_index[round_idx]) + '_' + algorithm.label)

        print(f'Algorithm: ${algorithm.get_name()}')
        print(f'Problem: ${problem.get_name()}')
        print(f'Computing time: ${algorithm.total_computing_time}')

    # outputfile.close()

