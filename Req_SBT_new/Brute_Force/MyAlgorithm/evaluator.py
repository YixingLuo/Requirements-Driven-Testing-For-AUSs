import functools
from abc import ABC, abstractmethod
from multiprocessing.pool import ThreadPool, Pool
from typing import TypeVar, List, Generic
from multiprocessing import Pool

try:
    import dask
except ImportError:
    pass

try:
    from pyspark import SparkConf, SparkContext
except ImportError:
    pass

from jmetal.core.problem import Problem


# def init(l):
# 	global lock
# 	lock = l

S = TypeVar('S')


class Evaluator(Generic[S], ABC):

    @abstractmethod
    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        pass

    @staticmethod
    def evaluate_solution(solution: S, problem: Problem) -> None:
        problem.evaluate(solution)


class SequentialEvaluator(Evaluator[S]):

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        for solution in solution_list:
            Evaluator.evaluate_solution(solution, problem)

        return solution_list


class MapEvaluator(Evaluator[S]):

    def __init__(self, processes: int = None):
        self.pool = ThreadPool(processes)

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        self.pool.map(lambda solution: Evaluator.evaluate_solution(solution, problem), solution_list)

        return solution_list


class MultiprocessEvaluator(Evaluator[S]):
    def __init__(self, processes: int = None):
        super().__init__()
        # lock = Lock()
        self.pool = Pool(processes)
        # self.pool = Pool(processes, initializer = init, initargs = (lock,))

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:


        # problem.bestpop.clear()

        # if problem.bestpop.configure.algorithm == "Adapt_Priority":
        #     if problem.bestpop.round > 0:
        #         # print(problem.bestpop.pop)
        #         problem.bestpop.add_results()
        #         if problem.bestpop.round % problem.bestpop.configure.interval == 0:
        #         # problem.bestpop.update_weight()
        #         # print("\033[1;31m new weight \033[0m", problem.bestpop.weights)

        problem.bestpop.update_round()
        print("\033[1;31m new round \033[0m", problem.bestpop.round)


        # gl.set_value('BestPop', bestlog)
        # bestpop2 = gl.get_value('BestPop')
        # print("\033[1;31m new round \033[0m", bestpop2.round, bestpop2.pop)

        # results_list = self.pool.map(functools.partial(evaluate_solution, problem=problem), solution_list)
        #
        # self.pool.close()
        # self.pool.join()
        # manager = Manager()
        # lock = manager.Lock()
        # func = functools.partial(evaluate_solution, problem=problem, lock = lock)

        # return self.pool.map(func, solution_list)
        return self.pool.map(functools.partial(evaluate_solution, problem=problem), solution_list)

# class MultiprocessEvaluator(Evaluator[S]):
#     def __init__(self, processes: int = None):
#         super().__init__()
#         self.pool = Pool(processes)
#
#     def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
#         return self.pool.map(functools.partial(evaluate_solution, problem=problem), solution_list)


class SparkEvaluator(Evaluator[S]):
    def __init__(self, processes: int = 8):
        self.spark_conf = SparkConf().setAppName("jmetalpy").setMaster(f"local[{processes}]")
        self.spark_context = SparkContext(conf=self.spark_conf)

        logger = self.spark_context._jvm.org.apache.log4j
        logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        solutions_to_evaluate = self.spark_context.parallelize(solution_list)

        return solutions_to_evaluate \
            .map(lambda s: problem.evaluate(s)) \
            .collect()


def evaluate_solution(solution, problem):
    Evaluator[S].evaluate_solution(solution, problem)
    return solution


class DaskEvaluator(Evaluator[S]):
    def __init__(self, scheduler='processes'):
        self.scheduler = scheduler

    def evaluate(self, solution_list: List[S], problem: Problem) -> List[S]:
        with dask.config.set(scheduler=self.scheduler):
            return list(dask.compute(*[
                dask.delayed(evaluate_solution)(solution=solution, problem=problem) for solution in solution_list
            ]))