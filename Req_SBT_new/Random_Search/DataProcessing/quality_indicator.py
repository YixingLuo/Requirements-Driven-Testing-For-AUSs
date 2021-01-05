from jmetal.core.quality_indicator import GenerationalDistance, InvertedGenerationalDistance, HyperVolume
import numpy as np
import os

file_folder_orgin = os.path.abspath(os.path.join(os.getcwd(), "../../Random"))
var_file = file_folder_orgin + "/FUN.NSGAII.OvertakeProblem"
solution_file = file_folder_orgin + "/VAR.NSGAII.OvertakeProblem"

var = np.loadtxt(var_file)
solution = np.loadtxt(solution_file)

# print(var, solution)

indicator1 = GenerationalDistance(solution)
GD = indicator1.compute(solution)
print(GD)
indicator1 = InvertedGenerationalDistance(solution)
GD = indicator1.compute(solution)
print(GD)