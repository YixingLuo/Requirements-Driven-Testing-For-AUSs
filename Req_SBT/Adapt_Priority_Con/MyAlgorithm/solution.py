from abc import ABC
from typing import List, Generic, TypeVar

from jmetal.util.ckecking import Check

BitSet = List[bool]
S = TypeVar('S')


class Solution(Generic[S], ABC):
    """ Class representing solutions """

    def __init__(self, number_of_variables: int, number_of_objectives: int, number_of_constraints: int = 0, index: int):
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = number_of_constraints
        self.variables = [[] for _ in range(self.number_of_variables)]
        self.objectives = [0.0 for _ in range(self.number_of_objectives)]
        self.constraints = [0.0 for _ in range(self.number_of_constraints)]
        self.attributes = {}
        self.index = index

    def __eq__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.variables == solution.variables
        return False

    def __str__(self) -> str:
        return 'Solution(variables={},objectives={},constraints={})'.format(self.variables, self.objectives,
                                                                            self.constraints)


class FloatSolution(Solution[float]):
    """ Class representing float solutions """

    def __init__(self, lower_bound: List[float], upper_bound: List[float], number_of_objectives: int,
                 number_of_constraints: int = 0):
        super(FloatSolution, self).__init__(len(lower_bound), number_of_objectives, number_of_constraints)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __copy__(self):
        new_solution = FloatSolution(
            self.lower_bound,
            self.upper_bound,
            self.number_of_objectives,
            self.number_of_constraints)
        new_solution.objectives = self.objectives[:]
        new_solution.variables = self.variables[:]
        new_solution.constraints = self.constraints[:]

        new_solution.attributes = self.attributes.copy()

        return new_solution