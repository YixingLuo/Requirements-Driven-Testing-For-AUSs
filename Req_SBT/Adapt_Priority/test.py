import numpy
import csv

# violation_pattern_ranking = [[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0]]
# searched_violation_pattern = [[1, 1, 1], [1, 0, 1]]
#
# violation_pattern_ranking_removed = violation_pattern_ranking.copy()
# for j in range(numpy.array(violation_pattern_ranking).shape[0]):
#     for k in range(numpy.array(searched_violation_pattern).shape[0]):
#         if (numpy.array(violation_pattern_ranking[j]) == numpy.array(searched_violation_pattern[k])).all():
#             removed_item = violation_pattern_ranking[j]
#             for ll in range(numpy.array(violation_pattern_ranking_removed).shape[0]):
#                 if (numpy.array(violation_pattern_ranking_removed[ll]) == numpy.array(removed_item)).all():
#                     del violation_pattern_ranking_removed[ll]
#                     break
#             break
#
# print(violation_pattern_ranking_removed,violation_pattern_ranking)

priority_list = []
with open("priority_list.csv") as csvfile:
    csv_file = csv.reader(csvfile)
    for row in csv_file:
        priority_list.append(row)
    priority_list = [[float(x) for x in row] for row in priority_list]
priority_list = numpy.array(priority_list)

print(priority_list.shape[0])

