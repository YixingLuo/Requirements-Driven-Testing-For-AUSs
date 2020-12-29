#coding: utf-8
from multiprocessing import Pool
from Settings.TurnRightConfigure import TurnRightConfigure
from MyScenario.TurnRight import create_run_scenario_turnright_random
import os
import time

data_folder = os.getcwd() + '/TurnRight_Datalog_' + str(time.strftime("%Y_%m_%d_%H"))
if not os.path.exists(data_folder):
    os.mkdir(data_folder)

if __name__ == "__main__":

    target_dir = data_folder
    Configuration = TurnRightConfigure(target_dir)

    pool = Pool(processes = Configuration.ProcessNum)
    res_l=[]
    for i in range(Configuration.maxIterations):
        res=pool.apply_async(create_run_scenario_turnright_random, (Configuration, ))
        res_l.append(res)
    # print("==============================>")

    pool.close()
    pool.join()
