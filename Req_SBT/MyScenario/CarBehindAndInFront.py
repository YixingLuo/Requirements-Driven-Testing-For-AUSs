import sys
sys.path.append("../Adapt_Priority")
sys.path.append("../Brute_Force")
sys.path.append("../GA")
sys.path.append("../Random")
import json
import numpy as np
import os
import time
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light, evaluate_cross_lane
# from bestpop import BestPop
import uuid


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s_%03d" % (data_head, data_secs)
    return time_stamp


def create_run_scenario_overtake (Vars, BestPop, Configure):

    config = Configure
    population = config.population

    result = np.zeros((population, config.goal_num), float)

    file_dir_sce = config.file_dir_sce
    file_dir_data = config.file_dir_data
    file_dir_eval = config.file_dir_eval
    file_dir_var = config.file_dir_var

    with open('Overtake.json', 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)

    for key in ret_dic:
        if key == "config":
            configList = ret_dic[key]

            configList["s0"] = Vars[0]
            configList["v0"] = Vars[1]

        elif key == "traffic_signal":
            ret_dic[key] = []
            objDict = {"start_s": Vars[2],
                       "end_s": Vars[3],
                       "green_time": Vars[4],
                       "yellow_time": Vars[5],
                       "red_time": Vars[6]}
            ret_dic[key].append(objDict)


        # elif key == "static_obs":
        #     obsList = ret_dic[key]
        #     obsList[0]["pos_s"] = Vars[7]
        #     obsList[1]["pos_s"] = Vars[8]

        elif key == "dynamic_obs":
            obsList = ret_dic[key]
            obsList[0]["pos_y"] = Vars[7]
            obsList[0]["velo"] = Vars[8]
            obsList[0]["acc"] = Vars[9]
            obsList[1]["start_time"] = Vars[10]

            obsList[1]["pos_y"] = Vars[11]
            obsList[1]["velo"] = Vars[12]
            obsList[1]["acc"] = Vars[13]
            obsList[1]["start_time"] = Vars[14]

            obsList[2]["pos_y"] = Vars[15]
            obsList[2]["velo"] = Vars[16]
            obsList[2]["acc"] = Vars[17]
            obsList[2]["start_time"] = Vars[18]

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


    var_name = file_dir_var + "/var_" + now_time + "_" + uuid_str + ".txt"

    with open(var_name, 'w', encoding='utf-8') as f:
        json.dump(Vars, f, ensure_ascii=False, indent=4)

    ## run the scenario
    duration = config.duration

    file_path = os.path.abspath(os.path.join(os.getcwd(), "../Random"))
    # print(file_path)

    log_name = file_dir_data + "/datalog_" + now_time  + "_" + uuid_str + ".txt"
    cmd = "C:/Users/lenovo/Documents/GitHub/mazda-path-planner-sbt_changes/mazda-path-planner-sbt_changes/ERATO_planning/x64/Release/dynamic_cost.exe -c %d -v EGO_TESTER -i %s > %s" % (duration, scenario_name, log_name)

    ## weiming
    # cmd = "wine /gpfs/share/home/1801111354/Release/dynamic_cost.exe -c %d -v EGO_TESTER -i %s > %s" % (duration, scenario_name, log_name)

    # print(cmd)
    start = time.clock()

    os.system(cmd)
    elapsed = (time.clock() - start)
    # print('totally cost', elapsed)

    num_dynamic_obs = 3
    num_static_obs = 0

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





    comfort1, comfort2 = evaluate_comfort(ego_vehicle_state, config)
    avg_speed, min_speed = evaluate_speed(ego_vehicle_state, config)
    min_dis, avg_dis_satisfaction, min_dis_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                    dy_obsList, static_vehicle_state, st_obsList, config)
    avg_stable, min_stable = evaluate_stability(ego_vehicle_state, config)
    traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)
    cross_lane = evaluate_cross_lane(ego_vehicle_state)

    # result = [avg_stable, min_stable, avg_dis_satisfaction, min_dis_satisfaction, avg_speed, min_speed, traffic_light, cross_lane, comfort1,
    #           comfort2]
    #
    #
    # result = [avg_stable, avg_dis_satisfaction, min_dis_satisfaction, avg_speed, min_speed, traffic_light,
    #       cross_lane, comfort1, comfort2]

    result = [min_stable, min_dis, min_speed, traffic_light, cross_lane, comfort1, comfort2]
    # result = [-min_dis, -min_stable, min_speed, traffic_light, -cross_lane, -comfort1, comfort2]

    # global _global_dict
    # _global_dict
    # BestPopulation.round = 2
    # print(BestPopulation.round)
    # bestlog = globalvar.get_value('BestPop')
    # print("Scenario:", BestPopulation.round)
    # print("Variables:", Vars)

    print("Results:", len(result), result)

    # print("Weights:", bestlog.weights)
    # print("Round: %d" %(bestpop.round))

    result_name = file_dir_eval + "/result_" + now_time  + "_"  + uuid_str + ".txt"
    # print(result_name)
    np.savetxt(result_name, result, fmt="%f", delimiter=" ")

    if Configure.algorithm == 'NSGA_III_Adapt':
        weights = BestPop.weights
        for i in range (config.goal_num):
            result[i] = weights[i] *  result[i]

        # print("Results after weight:", result)

    return result

