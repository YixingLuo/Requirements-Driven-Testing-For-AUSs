# -*- coding: utf-8 -*-

import threading
from abc import ABC, abstractmethod

from jmetal.core.observer import Observer
from jmetal.core.quality_indicator import QualityIndicator
from jmetal.core.problem import Problem, DynamicProblem

"""
.. module:: termination_criterion
   :platform: Unix, Windows
   :synopsis: Implementation of stopping conditions.

.. moduleauthor:: Antonio Benítez-Hidalgo <antonio.b@uma.es>
"""


class TerminationCriterion(Observer, ABC):

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def is_met(self):
        pass


class StoppingByEvaluations(TerminationCriterion):

    def __init__(self, max_evaluations: int, problem: Problem):
        super(StoppingByEvaluations, self).__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.problem = problem

    def update(self, *args, **kwargs):
        self.evaluations = kwargs['EVALUATIONS']
        # self.problem = kwargs['PROBLEM']

    @property
    def is_met(self):
        if self.problem.problem_solved:
            print("problem.solved", self.problem.problem_solved)
            return self.problem.problem_solved
        else:
            print("problem.solved", self.problem.problem_solved, self.evaluations)
            return self.evaluations >= self.max_evaluations

class MyStoppingByEvaluations(TerminationCriterion):

    evaluations = None

    def __init__(self, max_evaluations: int, problem: Problem):
        super(MyStoppingByEvaluations, self).__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.problem = problem

    def update(self, *args, **kwargs):
        self.evaluations = kwargs['EVALUATIONS']
        self.problem = kwargs['PROBLEM']

    @property
    def is_met(self):
        if self.problem.problem_solved:
            print("find that pattern!!")
            return self.problem.problem_solved
        else:
            print("reach the max evaluations!!")
            return self.evaluations >= self.max_evaluations



class StoppingByTime(TerminationCriterion):

    def __init__(self, max_seconds: int):
        super(StoppingByTime, self).__init__()
        self.max_seconds = max_seconds
        self.seconds = 0.0

    def update(self, *args, **kwargs):
        self.seconds = kwargs['COMPUTING_TIME']

    @property
    def is_met(self):
        return self.seconds >= self.max_seconds


def key_has_been_pressed(stopping_by_keyboard):
    input('PRESS ANY KEY + ENTER: ')
    stopping_by_keyboard.key_pressed = True


class StoppingByKeyboard(TerminationCriterion):

    def __init__(self):
        super(StoppingByKeyboard, self).__init__()
        self.key_pressed = False
        thread = threading.Thread(target=key_has_been_pressed, args=(self,))
        thread.start()

    def update(self, *args, **kwargs):
        pass

    @property
    def is_met(self):
        return self.key_pressed


class StoppingByQualityIndicator(TerminationCriterion):

    def __init__(self, quality_indicator: QualityIndicator, expected_value: float, degree: float):
        super(StoppingByQualityIndicator, self).__init__()
        self.quality_indicator = quality_indicator
        self.expected_value = expected_value
        self.degree = degree
        self.value = 0.0

    def update(self, *args, **kwargs):
        solutions = kwargs['SOLUTIONS']



        if solutions:
            self.value = self.quality_indicator.compute(solutions)
            print("hybervolume", self.value)
            for solution in solutions:
                print("Var", solution.variables)
                print("Fuc", solution.objectives)

    @property
    def is_met(self):
        if self.quality_indicator.is_minimization:
            met = self.value * self.degree < self.expected_value
        else:
            met = self.value * self.degree > self.expected_value

        return met
