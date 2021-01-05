# -*- coding: utf-8 -*-

from jmetal.algorithm.multiobjective.nsgaiii import UniformReferenceDirectionFactory
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import MultiprocessEvaluator
from jmetal.util.observer import ProgressBarObserver
from MyAlgorithm.nsgaiii import NSGAIII
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
import os
import time
from CarBehindAndInFrontProblem import CarBehindAndInFrontProblem
import csv
import numpy
from RankingRules.DistanceRanking import Distance_Ranking
from RankingRules.EnsembleRanking import Ensemble_Ranking
from RankingRules.RelationRanking import Relation_Ranking



def text_create(Configuration):
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d_")) + str(Configuration.algorithm) + '_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path,  'w')
    return full_path



data_folder = os.getcwd() + '/Overtake_Datalog_Req2_' + str(time.strftime("%Y_%m_%d_%H"))
if not os.path.exists(data_folder):
    os.mkdir(data_folder)

if __name__ == '__main__':

    # search_round_list = [1, 10, 10, 10, 10, 20, 110, 110]
    search_round_list = [1, 10, 20, 30, 40, 50, 60, 70]
    target_value_threshold = [1, 0, 1, 1, 1, 0.95, 0.99]
    target_dir = data_folder

    priority_list = []
    with open("priority_list.csv") as csvfile:
        csv_file = csv.reader(csvfile)
        for row in csv_file:
            priority_list.append(row[0:-1])
        priority_list = [[float(x) for x in row] for row in priority_list]
    priority_list = numpy.array(priority_list)

    violation_pattern_to_search = []
    pattern_count = numpy.zeros(priority_list.shape[0])
    evaluation = []
    searched_violation_pattern = []
    violation_pattern_ranking_removed = []
    variables = []
    sorted_pop = []

    total_round = 400
    # interation_round = 3
    round_index = 0
    population = 50
    search_round = 0

    while total_round > 0:

    # for round_index in range (interation_round):
        ## read_files

        # search_round = 50

        # vars_file_name = "2020_12_26_Adapt_Priority_variable_0"
        # results_file_name = "2020_12_26_Adapt_Priority_results_0"

        ## caculate goal_index
        if round_index == 0:
            goal_selection_flag = numpy.ones(7)
            searched_violation_pattern.append(goal_selection_flag)

            search_round = search_round_list[int(sum(goal_selection_flag))]
            if total_round < search_round:
                search_round = total_round
            total_round = total_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_selection_flag, population, search_round, round_index, target_dir)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval

        else:
            # print(round_index, sum(pattern_count))
            fileList = os.listdir(results_file_name)
            fileList.sort()

            for i in range(population * search_round):
                textname = results_file_name + '/' + fileList[i]
                # print(textname)
                result = numpy.loadtxt(textname)
                evaluation.append(result)
                goal_flag = numpy.zeros((7), dtype=int)
                for j in range(7):
                    if result[j] < target_value_threshold[j]:
                        goal_flag[j] = 1
                    else:
                        goal_flag[j] = 0
                for j in range (priority_list.shape[0]):
                    if (numpy.array(goal_flag) == priority_list[j]).all():
                        pattern_count[j] = pattern_count[j] + 1
                        break
            fileList = os.listdir(vars_file_name)
            fileList.sort()
            for i in range (population * search_round):
                textname = vars_file_name + '/' + fileList[i]
                pop = numpy.loadtxt(textname)
                variables.append(pop)

            violation_pattern_to_search = []
            for j in range (priority_list.shape[0]):
                if pattern_count[j] == 0:
                    violation_pattern_to_search.append(priority_list[j])
            # print(numpy.array(violation_pattern_to_search).shape[0])

            weight_dist, sorted_pattern_distance, sorted_pop, distance_ranking = Distance_Ranking(priority_list,
                                                                                                  variables, evaluation)
            weight_relation, sorted_pattern_relation, relation_ranking = Relation_Ranking(violation_pattern_to_search,
                                                                                          searched_violation_pattern,
                                                                                          priority_list)
            weights = [1, weight_dist, weight_relation]
            violation_pattern_ranking, overall_rank_list = Ensemble_Ranking(distance_ranking, relation_ranking,
                                                                            violation_pattern_to_search, weights)

            violation_pattern_ranking_removed = violation_pattern_ranking.copy()
            for j in range(numpy.array(violation_pattern_ranking).shape[0]):
                for k in range(numpy.array(searched_violation_pattern).shape[0]):
                    if (numpy.array(violation_pattern_ranking[j]) == numpy.array(searched_violation_pattern[k])).all():
                        removed_item = violation_pattern_ranking[j]
                        for ll in range(numpy.array(violation_pattern_ranking_removed).shape[0]):
                            if (numpy.array(violation_pattern_ranking_removed[ll]) == numpy.array(removed_item)).all():
                                del violation_pattern_ranking_removed[ll]
                                break
                        break

            if numpy.array(violation_pattern_ranking_removed).shape[0] == 0:
                goal_selection_flag = numpy.ones(7)
            else:
                goal_selection_flag = violation_pattern_ranking_removed[0]

            searched_violation_pattern.append(goal_selection_flag)
            search_round = search_round_list[int(sum(goal_selection_flag))]
            if total_round < search_round:
                search_round = total_round
            total_round = total_round - search_round

            Configuration = CarBehindAndInFrontConfigure(goal_selection_flag, population, search_round, round_index, target_dir)
            vars_file_name = Configuration.file_dir_var
            results_file_name = Configuration.file_dir_eval

        print("round: ", search_round, "idx: ", round_index, "left: ", total_round)
        pattern_name = target_dir + '/req_violation_pattern_' + str(round_index) + '.txt'
        numpy.savetxt(pattern_name, goal_selection_flag, fmt="%d")  # 保存为整数
        # Save results to file
        file_name = target_dir + '/searched_violation_pattern_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, searched_violation_pattern, fmt="%d")  # 保存为整数
        file_name = target_dir + '/violation_pattern_to_search_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, violation_pattern_to_search, fmt="%d")  # 保存为整数
        file_name = target_dir + '/variables_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, variables, fmt="%d")  # 保存为整数
        file_name = target_dir + '/evaluations_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, evaluation, fmt="%d")  # 保存为整数
        file_name = target_dir + '/pattern_count_' + str(round_index) + '.txt'
        numpy.savetxt(file_name, pattern_count, fmt="%d")  # 保存为整数


        Goal_num = Configuration.goal_num



        """===============================实例化问题对象============================"""
        problem = CarBehindAndInFrontProblem(Goal_num, Configuration, target_value_threshold)

        """=================================算法参数设置============================"""
        max_evaluations = Configuration.maxIterations

        algorithm = NSGAIII(initial_population = sorted_pop,
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
        # progress_bar = ProgressBarObserver(max=max_evaluations)
        # algorithm.observable.register(progress_bar)
        algorithm.run()
        front = algorithm.get_result()

        """==================================输出结果=============================="""



        # Save results to file
        fun_name = 'FUN.' + str(round_index) + '_' + algorithm.label
        print_function_values_to_file(front, os.path.join(target_dir,fun_name))
        var_name = 'VAR.'+ str(round_index) + '_' + algorithm.label
        print_variables_to_file(front, os.path.join(target_dir, var_name))

        print(f'Algorithm: ${algorithm.get_name()}')
        print(f'Problem: ${problem.get_name()}')
        print(f'Computing time: ${algorithm.total_computing_time}')



        # print(search_round,round_index,total_search_round)
        round_index = round_index + 1
