#coding: utf-8
from multiprocessing import Pool
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
from MyScenario.CarBehindAndInFront import create_run_scenario_overtake_random
import os
import time

data_folder = os.getcwd() + '/Datalog_' + str(time.strftime("%Y_%m_%d_%H"))
if not os.path.exists(data_folder):
    os.mkdir(data_folder)

if __name__ == "__main__":

    Configuration = CarBehindAndInFrontConfigure()

    pool = Pool(processes = Configuration.ProcessNum)
    res_l=[]
    for i in range(Configuration.maxIterations):
        res=pool.apply_async(create_run_scenario_overtake_random, (Configuration, ))
        res_l.append(res)
    # print("==============================>")

    pool.close()
    pool.join()

    # print(res_l)
    # for i in res_l:
    #     print(i.get())