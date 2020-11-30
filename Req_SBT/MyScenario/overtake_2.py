import sys
sys.path.append("..")
import json
import numpy as np
import random
from Configure import configure
import os
import time
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light
import globalvar
# from bestpop import BestPop
import math
import uuid


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s_%03d" % (data_head, data_secs)
    return time_stamp


def create_run_scenario_overtake (Vars, BestPop, Configure):
# def create_run_scenario_overtake(Vars, num_sce, file_dir_sce, file_dir_data, file_dir_eval):

    # bestlog = globalvar.get_value('BestPop')
    # print(bestlog.round)



    # alg = globalvar.get_value('Algorithm')
    # global algorithm
    # alg = algorithm

    # bestpop = BestPop
    # bestpop.call_iteration(alg,num_sce)
    # print(args)
    # Vars = args[0]
    # config = args[1]
    # file_dir_sce = args[2]
    # file_dir_data = args[3]
    # file_dir_eval = args[4]
    #
    #
    # print(config.type)
    # population = config.population
    # population = Vars.shape[0]

    config = Configure
    # config =  globalvar.get_value('Configure')
    population = config.population

    result = np.zeros((population, config.goal_num), float)

    file_dir_sce = config.file_dir_sce
    file_dir_data = config.file_dir_data
    file_dir_eval = config.file_dir_eval

    # for num_sce in range(population):

    # print(num_sce)

    with open('MyScenario/example.json', 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)

    for key in ret_dic:
        if key == "config":
            configList = ret_dic[key]

            configList["s0"] = Vars[0]
            configList["v0"] = Vars[1]

        elif key == "traffic_signal":
            ret_dic[key] = []
            objDict = {"start_s": Vars[2], "end_s": Vars[3], "green_time": Vars[4], "yellow_time": Vars[5],
                       "red_time": Vars[6]}
            ret_dic[key].append(objDict)



        elif key == "static_obs":
            obsList = ret_dic[key]
            obsList[0]["pos_s"] = Vars[7]
            obsList[1]["pos_s"] = Vars[8]



        elif key == "dynamic_obs":
            obsList = ret_dic[key]
            obsList[0]["pos_y"] = Vars[9]
            obsList[0]["velo"] = Vars[10]
            obsList[0]["acc"] = Vars[11]

            obsList[1]["pos_y"] = Vars[12]
            obsList[1]["velo"] = Vars[13]
            obsList[1]["acc"] = Vars[14]
            obsList[1]["start_time"] = Vars[15]


    traffic_light = ret_dic["traffic_signal"]
    st_obsList = ret_dic["static_obs"]
    dy_obsList  = ret_dic["dynamic_obs"]
    # print(traffic_light, st_obsList, dy_obsList)

    # global bestpop
    # bestlog = globalvar.get_value('BestPop')
    # print("\033[1;32m scenario round: \033[0m", bestlog.round)
    now_time = get_time_stamp()
    uuid_str = uuid.uuid4().hex
    scenario_name = file_dir_sce + "/scenario_" + now_time + "_" + uuid_str + ".json"
    # scenario_name = file_dir_sce + "/scenario_" + str(bestlog.round) +'-' + str(num_sce) + ".json"
    # print(scenario_name)
    with open(scenario_name, 'w', encoding='utf-8') as f:
        json.dump(ret_dic, f, ensure_ascii=False, indent=4)

    ## run the scenario
    duration = config.duration

    file_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    # print(file_path)

    log_name = file_dir_data + "/datalog_" + now_time  + "_" + uuid_str + ".txt"
    cmd = "C:/Users/lenovo/Documents/GitHub/mazda-path-planner-sbt_changes/mazda-path-planner-sbt_changes/ERATO_planning/x64/Release/" \
          "dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (duration, scenario_name, log_name)


    # print(cmd)
    start = time.clock()

    os.system(cmd)
    elapsed = (time.clock() - start)
    # print('totally cost', elapsed)



    # with open(scenario_name, 'r', encoding='utf-8') as f:
    #     ret_dic = json.load(f)
    #     for key in ret_dic:
    #         if key == "dynamic_obs":
    #             dy_obsList = ret_dic[key]
    #             num_dynamic_obs = len(dy_obsList)
    #             # print(dy_obsList)
    #             # print(dy_obsList[0]["width"])
    #         if key == "static_obs":
    #             st_obsList = ret_dic[key]
    #             num_static_obs = len(st_obsList)
    #         if key == "traffic_signal":
    #             traffic_light = ret_dic[key]

    num_dynamic_obs = 2
    num_static_obs = 2

    ego_vehicle_state = []
    dynamic_vehicle_state = [[] for i in range(num_dynamic_obs)]
    static_vehicle_state = [[] for i in range(num_static_obs)]
    with open(log_name, 'r') as f:
        my_data = f.readlines()  # txt中所有字符串读入data，得到的是一个list
        # 对list中的数据做分隔和类型转换
        # for line in my_data:
        #     line_data = line.split()
        #     numbers_float = map(float, line_data)  # 转化为浮点数

        for line in my_data:
            data = line.split()
            if data[0] == "EGO_STATUS" and len(data) == 8:
                log = []
                for i in range(1, len(data)):
                    log.append(float(data[i]))
                if len(log) == 7:
                    ego_vehicle_state.append(log)

            if data[0] == "DYNAMIC_OBS_INFO" and len(data) == 10:
                log = []
                for i in range(2, len(data)):
                    log.append(float(data[i]))
                    # print(log)
                if len(log) == 8:
                    dynamic_vehicle_state[int(data[1])].append(log)
            elif data[0] == "STATIC_OBS_INFO" and len(data) == 5:
                log = []
                for i in range(2, len(data)):
                    log.append(float(data[i]))
                    # print(log)
                if len(log) == 3:
                    static_vehicle_state[int(data[1])].append(log)





    comfort = evaluate_comfort(ego_vehicle_state)
    speed = evaluate_speed(ego_vehicle_state)
    min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                    dy_obsList, static_vehicle_state, st_obsList)
    stable = evaluate_stability(ego_vehicle_state)
    traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

    result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]


    # result[0] = stable
    # # result[1] = min_dis
    # result[1] = min_satisfaction
    # result[2] = avg_satisfaction
    # result[3] = speed
    # result[4] = traffic_light
    # result[5] = comfort


    # global _global_dict
    # _global_dict
    # BestPopulation.round = 2
    # print(BestPopulation.round)
    # bestlog = globalvar.get_value('BestPop')
    # print("Scenario:", BestPopulation.round)
    # print("Variables:", Vars)
    print("Results:", result)
    # print("Weights:", bestlog.weights)
    # print("Round: %d" %(bestpop.round))

    result_name = file_dir_eval + "/result_" + now_time  + "_"  + uuid_str + ".txt"
    # print(result_name)
    np.savetxt(result_name, result, fmt="%f", delimiter=" ")

    weights = BestPop.weights
    for i in range (config.goal_num):
        result[i] = weights[i] *  result[i]

    print("Results after weight:", result)

    return result

