# -*- coding: utf-8 -*-

from jmetal.algorithm.multiobjective.random_search import RandomSearch
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations

from Configure import configure
from bestpop import BestPop
from MyProblem.OvertakeProblem import OvertakeProblem

if __name__ == '__main__':

    # freeze_support()

    # global Configuration
    Configuration = configure()
    # global BestPopulation
    BestPopulation = BestPop(Configuration)
    # config.createfolders()
    Goal_num = Configuration.goal_num

    # file_name = text_create(Configuration )
    # output = sys.stdout
    # outputfile = codecs.open(file_name,  'w', 'utf-8')
    # sys.stdout = outputfile

    """===============================实例化问题对象============================"""
    problem = OvertakeProblem(Goal_num, Configuration, BestPopulation)

    """=================================算法参数设置============================"""
    max_evaluations = Configuration.maxIterations
    algorithm = RandomSearch(
        problem=problem,
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
    )

    algorithm.run()
    front = algorithm.get_result()

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + Configuration.file_dir_eval + algorithm.label)
    print_variables_to_file(front, 'VAR.'+ Configuration.file_dir_var + algorithm.label)

    print(f'Algorithm: ${algorithm.get_name()}')
    print(f'Problem: ${problem.get_name()}')
    print(f'Computing time: ${algorithm.total_computing_time}')
