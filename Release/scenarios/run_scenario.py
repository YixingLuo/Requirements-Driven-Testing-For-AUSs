#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import os
from threading import Thread

time = 10
num_sce = 1
file_path = r"C:\Users\lenovo\Documents\GitHub\mazda-path-planner-sbt_changes\mazda-path-planner-sbt_changes\ERATO_planning\\x64\Release\\"
scenario_name = file_path + "scenarios\scenario_" + str(num_sce) + ".json"
log_name = file_path + "datalog\datalog_" + str(num_sce) + ".txt"
cmd = file_path + "dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (time, scenario_name, log_name)

print(cmd)
os.system(cmd)
# output = os.popen(cmd)
# info = output.readlines()
# print(info)
# type(info)