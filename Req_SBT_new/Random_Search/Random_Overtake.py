#coding: utf-8
from multiprocessing import Pool
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
from MyScenario.CarBehindAndInFront import create_run_scenario_overtake_random
import os
import time

data_folder = os.getcwd() + '/Overtake_Datalog_' + str(time.strftime("%Y_%m_%d_%H"))
if not os.path.exists(data_folder):
    os.mkdir(data_folder)

if __name__ == "__main__":

    target_dir = data_folder
    Configuration = CarBehindAndInFrontConfigure(target_dir)

    pool = Pool(processes=Configuration.ProcessNum)
    res_l=[]
    for i in range(Configuration.maxIterations):
        res=pool.apply_async(create_run_scenario_overtake_random, (Configuration, ))
        res_l.append(res)

    pool.close()
    pool.join()

    # for i in range(Configuration.maxIterations):
    #     create_run_scenario_overtake_random (Configuration)