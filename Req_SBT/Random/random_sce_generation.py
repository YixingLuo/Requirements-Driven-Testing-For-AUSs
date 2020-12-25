#coding: utf-8
from multiprocessing import Pool
from Settings.CarBehindAndInFrontConfigure import CarBehindAndInFrontConfigure
from MyScenario import create_run_scenario_overtake_random


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