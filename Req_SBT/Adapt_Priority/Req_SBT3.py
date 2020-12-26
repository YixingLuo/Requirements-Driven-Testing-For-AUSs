# -*- coding: utf-8 -*-

# from jmetal.algorithm.multiobjective.nsgaii import NSGAII
# from jmetal.algorithm.multiobjective.random_search import RandomSearch
# from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII
from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
# from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import SequentialEvaluator, MultiprocessEvaluator
from MyAlgorithm.nsgaiii import NSGAIII
from MyAlgorithm.nsgaii import NSGAII
from MyAlgorithm.random_search import RandomSearch
from MyAlgorithm.termination_criterion import StoppingByEvaluations
# from MyAlgorithm.evaluator import MultiprocessEvaluator
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
import os
import time
# from trash.initial_files.bestpop import BestPop
from CarBehindAndInFront import CarBehindAndInFront
from jmetal.util.observer import ProgressBarObserver
import csv
import numpy
from RankingRules.DistanceRanking import Distance_Ranking
from RankingRules.EnsembleRanking import Ensemble_Ranking, Ensemble_Ranking2
from RankingRules.RelationRanking import Relation_Ranking


def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(
        Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
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

    target_value_threshold = [1, 0, 1, 1, 1, 0.95, 0.99]

    priority_list = []
    with open("priority_list.csv") as csvfile:
        csv_file = csv.reader(csvfile)
        for row in csv_file:
            priority_list.append(row)
        priority_list = [[float(x) for x in row] for row in priority_list]
    priority_list = numpy.array(priority_list)

    violation_pattern_to_search = []
    pattern_count = numpy.zeros(priority_list.shape[0])

    total_search_round = 400
    # interation_round = 3
    round_index = 0
    while total_search_round > 0:

        ## read_files
        population = 50
        # search_round = 50
        evaluation = []
        variables = []
        sorted_pop = []
        searched_violation_pattern = []
        # vars_file_name = "2020_12_26_Adapt_Priority_variable_0"
        # results_file_name = "2020_12_26_Adapt_Priority_results_0"

        ## caculate goal_index
        if round_index == 0:
            goal_selection_flag = numpy.ones(7)
            searched_violation_pattern.append(goal_selection_flag)
            search_round = 10 * sum(goal_selection_flag)
            # search_round = 1
            if total_search_round < search_round:
                search_round = total_search_round
            total_search_round = total_search_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_selection_flag, population, search_round, round_index)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval
            # print(round_index, vars_file_name, results_file_name)


        else:
            print(round_index, sum(pattern_count))
            fileList = os.listdir(results_file_name)
            fileList.sort()

            for i in range(population * search_round):
                textname = results_file_name + '/' + fileList[i]
                # print(textname)
                result = numpy.loadtxt(textname)
                evaluation.append(result)
                goal_flag = numpy.zeros((7), dtype=int)
                for j in range(7):
                    if abs(result[j]) < target_value_threshold[j]:
                        goal_flag[j] = 1
                    else:
                        goal_flag[j] = 0
                for j in range(priority_list.shape[0]):
                    if (numpy.array(goal_flag) == priority_list[j]).all():
                        pattern_count[j] = pattern_count[j] + 1
                        break
            fileList = os.listdir(vars_file_name)
            fileList.sort()
            for i in range(population * search_round):
                textname = vars_file_name + '/' + fileList[i]
                pop = numpy.loadtxt(textname)
                variables.append(pop)

            violation_pattern_to_search = []
            for j in range(priority_list.shape[0]):
                if pattern_count[j] == 0:
                    violation_pattern_to_search.append(priority_list[j])
            # print(numpy.array(violation_pattern_to_search).shape[0])

            sorted_pattern_distance, sorted_pop = Distance_Ranking(violation_pattern_to_search, variables, evaluation)
            sorted_pattern_relation = Relation_Ranking (violation_pattern_to_search, searched_violation_pattern, priority_list)

            violation_pattern_ranking = Ensemble_Ranking(sorted_pattern_distance, sorted_pattern_relation, violation_pattern_to_search)
            # violation_pattern_ranking = Ensemble_Ranking2(sorted_pattern_distance, violation_pattern_to_search)
            # violation_pattern_ranking = sorted_pattern_distance

            if numpy.array(violation_pattern_ranking).shape[0] == 0:
                goal_selection_flag = numpy.ones(7)
            else:
                goal_selection_flag = violation_pattern_ranking[0]

            searched_violation_pattern.append(goal_selection_flag)
            search_round = 10 * sum(goal_selection_flag)
            # search_round = 1
            if total_search_round < search_round:
                search_round = total_search_round
            total_search_round = total_search_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_selection_flag, population, search_round, round_index)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval

        pattern_name = 'req_violation_pattern_' + str(round_index) + '.txt'
        numpy.savetxt(pattern_name, goal_selection_flag, fmt="%d")  # 保存为整数
        Goal_num = Configuration.goal_num

        """===============================实例化问题对象============================"""
        problem = CarBehindAndInFront(Goal_num, Configuration)

        """=================================算法参数设置============================"""
        max_evaluations = Configuration.maxIterations
        print(max_evaluations)

        if Configuration.algorithm == "NSGA_II":
            algorithm = NSGAII(
                population_evaluator=MultiprocessEvaluator(Configuration.ProcessNum),
                # population_evaluator=SequentialEvaluator(),
                problem=problem,
                population_size=Configuration.population,
                offspring_population_size=Configuration.population,
                mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
                crossover=SBXCrossover(probability=1.0, distribution_index=20),
                termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                # termination_criterion = StoppingByQualityIndicator(quality_indicator=FitnessValue, expected_value=1, degree=0.9)
                # selection = BinaryTournamentSelection()
            )
        elif Configuration.algorithm == "NSGA_III" or Configuration.algorithm == "Adapt_Priority":
            algorithm = NSGAIII(initial_population=sorted_pop,
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
        elif Configuration.algorithm == 'Random':
            algorithm = RandomSearch(
                problem=problem,
                termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
            )


        """==========================调用算法模板进行种群进化========================="""
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        front = algorithm.get_result()

        """==================================输出结果=============================="""
        # Save results to file
        print_function_values_to_file(front, 'FUN.' + str(round_index) + '_' + algorithm.label)
        print_variables_to_file(front, 'VAR.' + str(round_index) + '_' + algorithm.label)

        print(f'Algorithm: ${algorithm.get_name()}')
        print(f'Problem: ${problem.get_name()}')
        print(f'Computing time: ${algorithm.total_computing_time}')

        round_index = round_index + 1

