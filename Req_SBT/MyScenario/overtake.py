import sys
sys.path.append("..")
import json
import numpy as np
import random
from Configure import configure
import os
import time
from read_log import evaluate_distance, evaluate_speed, evaluate_comfort, evaluate_stability, evaluate_traffic_light
import globalvar as gl
from bestpop import BestPop


# def create_run_scenario_overtake (Vars, config, file_dir_sce, file_dir_data, file_dir_eval):
def create_run_scenario_overtake(Vars, file_dir_sce, file_dir_data, file_dir_eval):
    alg = gl.get_value('Algorithm')
    bestpop = gl.get_value('BestPop')
    bestpop.call_iteration(alg)
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

    config = configure()
    population = config.population

    result = np.zeros((population, config.goal_num), float)

    for num_sce in range(population):

        # print(num_sce)

        with open('MyScenario/example.json', 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)

        for key in ret_dic:
            if key == "config":
                configList = ret_dic[key]

                configList["s0"] = Vars[num_sce][0]
                configList["v0"] = Vars[num_sce][1]

            elif key == "traffic_signal":
                ret_dic[key] = []
                objDict = {"start_s": Vars[num_sce][2], "end_s": Vars[num_sce][3], "green_time": Vars[num_sce][4], "yellow_time": Vars[num_sce][5],
                           "red_time": Vars[num_sce][6]}
                ret_dic[key].append(objDict)

            elif key == "static_obs":
                obsList = ret_dic[key]
                obsList[0]["pos_s"] = Vars[num_sce][7]
                obsList[1]["pos_s"] = Vars[num_sce][8]


            elif key == "dynamic_obs":
                obsList = ret_dic[key]
                obsList[0]["pos_y"] = Vars[num_sce][9]
                obsList[0]["velo"] = Vars[num_sce][10]
                obsList[0]["acc"] = Vars[num_sce][11]

                obsList[1]["pos_y"] = Vars[num_sce][12]
                obsList[1]["velo"] = Vars[num_sce][13]
                obsList[1]["acc"] = Vars[num_sce][14]
                obsList[1]["start_time"] = Vars[num_sce][15]



        scenario_name = file_dir_sce + "/scenario-" + str(alg.currentGen) +'-' + str(num_sce) + ".json"
        # print(scenario_name)
        with open(scenario_name, 'w', encoding='utf-8') as f:
            json.dump(ret_dic, f, ensure_ascii=False, indent=4)

        ## run the scenario
        duration = config.duration

        file_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        # print(file_path)
        # scenario_name = file_dir_sce + "\scenario_" + str(num_sce) + ".json"
        log_name = file_dir_data + "/datalog-" + str(alg.currentGen) +'-' + str(num_sce) + ".txt"
        cmd = "C:/Users/lenovo/Documents/GitHub/mazda-path-planner-sbt_changes/mazda-path-planner-sbt_changes/ERATO_planning/x64/Release/" \
              "dynamic_cost -c %d -v EGO_TESTER -a -i %s > %s" % (duration, scenario_name, log_name)


        # print(cmd)
        start = time.clock()

        os.system(cmd)
        elapsed = (time.clock() - start)
        print('totally cost', elapsed)


        print(log_name)

        with open(scenario_name, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
            for key in ret_dic:
                if key == "dynamic_obs":
                    dy_obsList = ret_dic[key]
                    num_dynamic_obs = len(dy_obsList)
                    # print(dy_obsList)
                    # print(dy_obsList[0]["width"])
                if key == "static_obs":
                    st_obsList = ret_dic[key]
                    num_static_obs = len(st_obsList)
                if key == "traffic_signal":
                    traffic_light = ret_dic[key]

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



        # print(dynamic_vehicle_state.shape[0])

        comfort = evaluate_comfort(ego_vehicle_state)
        speed = evaluate_speed(ego_vehicle_state)
        min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                        dy_obsList, static_vehicle_state, st_obsList)
        stable = evaluate_stability(ego_vehicle_state)
        traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

        # result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]


        result[num_sce][0] = stable
        # result[num_sce][1] = min_dis
        result[num_sce][1] = min_satisfaction
        result[num_sce][2] = avg_satisfaction
        result[num_sce][3] = speed
        result[num_sce][4] = traffic_light
        result[num_sce][5] = comfort

        bestpop.update_bestpop(result[num_sce])

        print("Scenario: %d %d, Result: %s" %(alg.currentGen, num_sce , str(result[num_sce])))
        print("Scenario: %d %d" %(alg.currentGen, num_sce))
        print("Variables:", Vars[num_sce])
        print("Results:", result[num_sce])
        print("Weights:", bestpop.weights)
        print("Round: %d, Iteration: %d" %(bestpop.round, bestpop.curiteration))

        result_name = file_dir_eval + "/result-" + str(alg.currentGen) +'-' + str(num_sce) + ".txt"
        # print(result_name)
        np.savetxt(result_name, result, fmt="%f", delimiter=" ")

        weights = bestpop.weights
        for i in range (config.goal_num):
            result[num_sce][i] = weights[i] *  result[num_sce][i]


    # print(result.shape)



    return result


if __name__=='__main__':

    file_dir_sce = os.getcwd() + '/2020_11_20_NSGAII_scenarios_2000'
    file_dir_data = os.getcwd() + '/2020_11_20_NSGAII_datalog_2000'
    scenario_name = file_dir_sce + "/scenario_" + str(0) + ".json"
    log_name = file_dir_data + "/datalog_" + str(0) + ".txt"

    with open(scenario_name, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        for key in ret_dic:
            if key == "dynamic_obs":
                dy_obsList = ret_dic[key]
                num_dynamic_obs = len(dy_obsList)
                # print(dy_obsList)
                # print(dy_obsList[0]["width"])
            if key == "static_obs":
                st_obsList = ret_dic[key]
                num_static_obs = len(st_obsList)
            if key == "traffic_signal":
                traffic_light = ret_dic[key]

    ego_vehicle_state = []
    dynamic_vehicle_state = [[] for i in range(num_dynamic_obs)]
    static_vehicle_state = [[] for i in range(num_static_obs)]
    print(ego_vehicle_state, dynamic_vehicle_state, static_vehicle_state)
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
                ego_vehicle_state.append(log)

            # dynamic_vehicle_state = np.zeros((num_dynamic_obs, len(ego_vehicle_state), 8), float)
            # print(dynamic_vehicle_state.shape)
            # static_vehicle_state = np.zeros((num_static_obs, len(ego_vehicle_state), 3), float)
            # width = config.ego_width
            # length = config.ego_length

            # for line in my_data:
            #     data = line.split()
            if data[0] == "DYNAMIC_OBS_INFO":
                log = []
                for i in range(2, len(data)):
                    log.append(float(data[i]))
                    # print(log)
                dynamic_vehicle_state[int(data[1])].append(log)
            elif data[0] == "STATIC_OBS_INFO":
                log = []
                for i in range(2, len(data)):
                    log.append(float(data[i]))
                    # print(log)
                static_vehicle_state[int(data[1])].append(log)

    # print(dynamic_vehicle_state.shape[0])

    comfort = evaluate_comfort(ego_vehicle_state)
    speed = evaluate_speed(ego_vehicle_state)
    min_dis, min_satisfaction, avg_satisfaction = evaluate_distance(ego_vehicle_state, dynamic_vehicle_state,
                                                                    dy_obsList, static_vehicle_state, st_obsList)
    stable = evaluate_stability(ego_vehicle_state)
    traffic_light = evaluate_traffic_light(ego_vehicle_state, traffic_light)

    result = [stable, min_satisfaction, avg_satisfaction, speed, traffic_light, comfort]
    # result[num_sce][0] = stable
    # result[num_sce][1] = min_dis
    # result[num_sce][2] = min_satisfaction
    # result[num_sce][3] = avg_satisfaction
    # result[num_sce][4] = speed
    # result[num_sce][5] = traffic_light
    # result[num_sce][6] = comfort

    print(result)