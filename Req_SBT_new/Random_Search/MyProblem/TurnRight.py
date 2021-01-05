import sys
# sys.path.append("../Adapt_Priority")
# sys.path.append("../Brute_Force")
# sys.path.append("../GA")
# sys.path.append("../Random")
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
# from MyAlgorithm.solution import FloatSolution
from MyScenario.TurnRight import create_run_scenario_overtake_random


# from scoop import futures

class TurnRight(FloatProblem):
    """ Problem ZDT1Modified.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """
    def __init__(self,  M, configure):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(TurnRight, self).__init__()
        self.number_of_variables = configure.num_variables
        self.number_of_objectives =  configure.goal_num
        self.number_of_constraints = 0
        self.config = configure

        self.obj_directions = [self.MINIMIZE] * M
        self.obj_labels = ['stable', 'acda', 'mini', 'speed', 'traffic_light', 'comfort']

        self.lower_bound = [self.config.ego_s0[0], self.config.ego_v0[0],
                            self.config.green_time[0], self.config.yellow_time[0], self.config.red_time[0],
                            self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0], self.config.start_time_1[0],
                            self.config.pos_x_2[0], self.config.velo_2[0], self.config.acc_2[0], self.config.start_time_2[0],
                            self.config.pos_x_3[0], self.config.velo_3[0], self.config.acc_3[0], self.config.start_time_3[0]]  # 决策变量下界
        self.upper_bound = [self.config.ego_s0[1], self.config.ego_v0[1],
                            self.config.green_time[1], self.config.yellow_time[1], self.config.red_time[1],
                            self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1], self.config.start_time_1[1],
                            self.config.pos_x_2[1], self.config.velo_2[1], self.config.acc_2[1], self.config.start_time_2[1],
                            self.config.pos_x_3[1], self.config.velo_3[1], self.config.acc_3[1], self.config.start_time_3[1]]  # 决策变量上界



    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        Vars = solution.variables

        result = create_run_scenario_overtake_random(Vars, self.config)

        solution.objectives = result

        return solution


    def get_name(self):
        return 'TurnRight'