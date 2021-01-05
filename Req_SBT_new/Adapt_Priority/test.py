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

pattern_list = []
pattern = numpy.zeros((7), dtype=int)
for a in range(2):
    pattern[0] = a
    for b in range(2):
        pattern[1] = b
        for c in range(2):
            pattern[2] = c
            for d in range(2):
                pattern[3] = d
                for e in range(2):
                    pattern[4] = e
                    for f in range(2):
                        pattern[5] = f
                        for g in range(2):
                            pattern[6] = g
                            cc = pattern.copy()
                            # print(pattern)
                            pattern_list.append(cc)
                            # print(pattern_list)

pattern_list = numpy.array(pattern_list)
# print(pattern_list.shape)
# print(pattern_list)

count = numpy.zeros((128), dtype=int)

for i in range (priority_list.shape[0]):
    for j in range (pattern_list.shape[0]):
        if (priority_list[i] == pattern_list[j]).all():
            # print(priority_list[i], pattern_list[j])
            count[j] = count[j] + 1
            print(count[j])
            break
print(count, count.sum())
for i in range(len(count)):
    if count[i] == 0:
        print("less than", pattern_list[i])
    elif count[i] > 1:
        print("more than: ", pattern_list[i])

find_pattern = [0,1,0,0,1,1,0]
for i in range(priority_list.shape[0]):
    if (priority_list[i] == numpy.array(find_pattern)).all():
        print(i, priority_list[i])
for i in range(pattern_list.shape[0]):
    if (pattern_list[i] == numpy.array(find_pattern)).all():
        print(i, pattern_list[i])