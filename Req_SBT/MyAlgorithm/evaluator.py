import functools
from abc import ABC, abstractmethod
import itertools
from multiprocessing.pool import ThreadPool, Pool
from typing import TypeVar, List, Generic
# from pathos.multiprocessing import ProcessingPoll as Pool
import pathos
import globalvar

try:
    import dask
except ImportError:
    pass

try:
    from pyspark import SparkConf, SparkContext
except ImportError:
    pass

from jmetal.core.problem import Problem

S = TypeVar('S')


class Evaluator(Generic[S], ABC):

    @abstractmethod
    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        pass

    @staticmethod
    def evaluate_solution(idx, solution: S, problem: Problem) -> None:
        problem.evaluate(idx, solution)


class SequentialEvaluator(Evaluator[S]):

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        for idx, solution in enumerate(solution_list):
            Evaluator.evaluate_solution(idx, solution, problem)

        return solution_list

class MultiprocessEvaluator(Evaluator[S]):
    def __init__(self, processes: int = None):
        super().__init__()
        # self.pool = Pool(processes)
        self.pool = pathos.multiprocessing.ProcessingPool(processes)

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        x = [solution_list.index(x) for x in solution_list]
        #
        # for solution in solution_list :
        #     result = solution.objectives
        #     print(result)
        # x_y = zip(x, y)
        # return self.pool.map(functools.partial(Evaluator.evaluate_solution, problem=problem), x_y)
        # return self.pool.map(Evaluator.evaluate_solution, zip(x, solution_list, itertools.repeat(problem)))

        # return self.pool.map(Evaluator.evaluate_solution, x, y, itertools.repeat(problem))

        self.pool.map(Evaluator.evaluate_solution, x, solution_list, itertools.repeat(problem))

        print(type(reee))

        bestlog = globalvar.get_value('BestPop')

        for solution in solution_list:
            result = solution.objectives
            print("final result", result)
            # print("final result", reee[solution].objectives)
            bestlog.update_bestpop(result)
            globalvar.set_value('BestPop', bestlog)
            print("\033[1;32m bestlog.pop \033[0m", bestlog.pop)

        # global bestpop
        # bestlog = globalvar.get_value('BestPop')
        bestlog.update_weight()
        bestlog.update_round()
        print("\033[1;31m new round \033[0m", bestlog.round)
        globalvar.set_value('BestPop', bestlog)
        bestpop2 = globalvar.get_value('BestPop')
        print("\033[1;31m new round \033[0m", bestpop2.round, bestpop2.pop)


        return solution_list

class MapEvaluator(Evaluator[S]):

    def __init__(self, processes: int = None):
        self.pool = ThreadPool(processes)

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        x = [solution_list.index(x) for x in solution_list]
        y = solution_list
        # z = problem * len(x)
        x_y = zip(x, y)
        solution_list_out = self.pool.map(Evaluator.evaluate_solution, x, y, itertools.repeat(problem))

        return solution_list_out