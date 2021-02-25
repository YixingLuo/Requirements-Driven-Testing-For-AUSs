
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
# from MyAlgorithm.solution import FloatSolution
from MyScenario.CarBehindAndInFront import create_run_scenario_overtake
import numpy as np

# from scoop import futures

class CarBehindAndInFrontProblem(FloatProblem):
    """ Problem ZDT1Modified.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """
    def __init__(self,  M, configure):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(CarBehindAndInFrontProblem, self).__init__()
        self.number_of_variables = configure.num_variables
        self.number_of_objectives = configure.goal_num
        self.number_of_constraints = 0
        self.config = configure
        # self.problem_solved = 0
        # self.target_value_threshold = target_value_threshold

        self.obj_directions = []
        for i in range (len(configure.goal_selection_flag)):
            if configure.goal_selection_flag[i] == 1:
                self.obj_directions.append(self.MINIMIZE)
            else:
                self.obj_directions.append(self.MAXIMIZE)
        # self.obj_directions = [self.MINIMIZE] * M
        self.obj_labels = ['stable', 'acda', 'mini', 'speed', 'traffic_light', 'comfort']

        self.lower_bound = [self.config.ego_s0[0], self.config.ego_v0[0],
                            self.config.start_s[0], self.config.green_time[0], self.config.yellow_time[0], self.config.red_time[0],
                            self.config.pos_y_1[0], self.config.velo_1[0], self.config.acc_1[0],
                            self.config.pos_y_2[0], self.config.velo_2[0], self.config.acc_2[0],
                            self.config.pos_y_3[0], self.config.velo_3[0], self.config.acc_3[0]] # 决策变量下界
        self.upper_bound = [self.config.ego_s0[1], self.config.ego_v0[1],
                            self.config.start_s[1], self.config.green_time[1], self.config.yellow_time[1], self.config.red_time[1],
                            self.config.pos_y_1[1], self.config.velo_1[1], self.config.acc_1[1],
                            self.config.pos_y_2[1], self.config.velo_2[1], self.config.acc_2[1],
                            self.config.pos_y_3[1], self.config.velo_3[1], self.config.acc_3[1]]  # 决策变量上界



    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        Vars = solution.variables

        result = create_run_scenario_overtake(Vars, self.config)

        solution.objectives = result

        ## check if find such pattern
        # goal_flag = np.zeros((7), dtype=int)
        # for j in range(7):
        #     if result[j] < self.target_value_threshold[j]:
        #         goal_flag[j] = 1
        #     else:
        #         goal_flag[j] = 0
        # # print("problem, self.config.goal_selection_flag", self.target_value_threshold, self.problem_solved)
        # if (goal_flag == self.config.goal_selection_flag).all():
        #     self.problem_solved = 1
        #     print(self.config.goal_selection_flag, self.problem_solved)

        return solution


    def get_name(self):
        return 'CarBehindAndInFrontProblem'