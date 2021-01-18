# -*- coding: utf-8 -*-

from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.multiobjective.random_search import RandomSearch
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII
from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import MultiprocessEvaluator, SequentialEvaluator
# from MyAlgorithm.evaluator import MultiprocessEvaluator
# from MyAlgorithm.nsgaiii import NSGAIII
# from MyAlgorithm.nsgaii import NSGAII
# from MyAlgorithm.random_search import RandomSearch
# from MyAlgorithm.termination_criterion import StoppingByEvaluations
# from MyAlgorithm.evaluator import MultiprocessEvaluator
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
import os
import time
# from trash.initial_files.bestpop import BestPop
from CarBehindAndInFrontProblem import CarBehindAndInFrontProblem
from jmetal.util.observer import ProgressBarObserver


def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path,  'w')
    return full_path




if __name__ == '__main__':

    for idx in range(10):

        data_folder = os.getcwd() + '/Overtake_Datalog_' + str(time.strftime("%Y_%m_%d_%H"))
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)

        target_dir = data_folder

        Configuration = CarBehindAndInFrontConfigure(target_dir)
        Goal_num = Configuration.goal_num


        """===============================实例化问题对象============================"""
        problem = CarBehindAndInFrontProblem(Goal_num, Configuration)

        """=================================算法参数设置============================"""
        max_evaluations = Configuration.maxIterations

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

        """==========================调用算法模板进行种群进化========================="""
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        front = algorithm.get_result()

        """==================================输出结果=============================="""
        # Save results to file
        # print_function_values_to_file(front, os.path.join(target_dir, '/FUN.' + algorithm.label))
        # print_variables_to_file(front, os.path.join(target_dir, '/VAR.' + algorithm.label))

        fun_name = 'FUN.' + algorithm.label
        print_function_values_to_file(front, os.path.join(target_dir, fun_name))
        var_name = 'VAR.' + algorithm.label
        print_variables_to_file(front, os.path.join(target_dir, var_name))

        print(f'Algorithm: ${algorithm.get_name()}')
        print(f'Problem: ${problem.get_name()}')
        print(f'Computing time: ${algorithm.total_computing_time}')


