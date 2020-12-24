import time
from typing import TypeVar, List
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool, Pool
import functools

from jmetal.config import store
from jmetal.core.algorithm import Algorithm
from jmetal.core.problem import Problem
from jmetal.util.archive import NonDominatedSolutionsArchive
from jmetal.util.termination_criterion import TerminationCriterion
from jmetal.util.evaluator import Evaluator

S = TypeVar('S')
R = TypeVar('R')

"""
.. module:: RamdomSearch
   :platform: Unix, Windows
   :synopsis: Simple random_search search algorithms.

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""


class RandomSearch(Algorithm[S, R]):

    def __init__(self,
                 problem: Problem[S],
                 termination_criterion: TerminationCriterion = store.default_termination_criteria,
                 population_evaluator: Evaluator = store.default_evaluator):
        super().__init__()
        self.problem = problem
        self.termination_criterion = termination_criterion
        self.observable.register(termination_criterion)
        self.evaluator = population_evaluator

        self.archive = NonDominatedSolutionsArchive()

    def get_observable_data(self) -> dict:
        ctime = time.time() - self.start_computing_time
        return {'PROBLEM': self.problem, 'EVALUATIONS': self.evaluations, 'SOLUTIONS': self.get_result(),
                'COMPUTING_TIME': ctime}

    def create_initial_solutions(self) -> List[S]:
        return [self.problem.create_solution()]

    # def evaluate(self, solution_list: List[S]) -> List[S]:
    #     return [self.problem.evaluate(solution_list[0])]

    def evaluate(self, solution_list: List[S]) -> List[S]:

        self.problem.bestpop.update_round()
        print("\033[1;31m new round \033[0m", self.problem.bestpop.round)
        self.problem.bestpop.clear()

        return self.evaluator.evaluate(solution_list,self.problem)

        # return self.pool.map(self.evaluator, solution_list[0])

    def init_progress(self) -> None:
        self.evaluations = 1

        observable_data = self.get_observable_data()
        self.observable.notify_all(**observable_data)

    def stopping_condition_is_met(self) -> bool:
        return self.termination_criterion.is_met

    def step(self) -> None:
        new_solution = self.problem.create_solution()
        self.problem.evaluate(new_solution)
        self.archive.add(new_solution)

    def update_progress(self) -> None:
        self.evaluations += 1

        observable_data = self.get_observable_data()
        self.observable.notify_all(**observable_data)

    def get_result(self) -> List[S]:
        return self.archive.solution_list

    def get_name(self) -> str:
        return 'Random Search'

    @property
    def label(self) -> str:
        return f'{self.get_name()}.{self.problem.get_name()}'