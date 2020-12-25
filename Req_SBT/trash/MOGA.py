# -*- coding: utf-8 -*-
""" QuickStart """
import sys
import geatpy as ea
from trash.initial_files.Configure import configure
import os
import time
from trash.initial_files.AdaptObj import AdaptObj
from trash.MyAlgorithm.My_moea_NSGA2_templet import My_moea_NSGA2_templet
import globalvar as gl
import codecs
from trash.initial_files.bestpop import BestPop




def text_create():
    desktop_path = os.getcwd() + '/'
    # 新创建的txt文件的存放路径
    full_path = desktop_path + str(time.strftime("%Y_%m_%d")) + '_NSGAII_iteration.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path,  'w')
    return full_path

# iteration_list = [10,20,30,40,50]

# for iteration in iteration_list:

if __name__ == '__main__':

    file_name = text_create()
    output = sys.stdout
    outputfile = codecs.open(file_name,  'w', 'utf-8')
    sys.stdout = outputfile


    config = configure()

    Goal_num = config.goal_num

    file_dir_sce = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_scenarios_' + str(config.maxIterations)
    if not os.path.exists(file_dir_sce):
        os.mkdir(file_dir_sce)

    file_dir_data = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_datalog_' + str(config.maxIterations)
    if not os.path.exists(file_dir_data):
        os.mkdir(file_dir_data)

    file_dir_eval = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAII_results_' + str(config.maxIterations)
    if not os.path.exists(file_dir_eval):
        os.mkdir(file_dir_eval)


    # file_dir_sce = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAIII_scenarios_' + str(iteration)
    # if not os.path.exists(file_dir_sce):
    #     os.mkdir(file_dir_sce)
    #
    # file_dir_data = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAIII_datalog_' + str(iteration)
    # if not os.path.exists(file_dir_data):
    #     os.mkdir(file_dir_data)
    #
    # file_dir_eval = os.getcwd() + '/' + str(time.strftime("%Y_%m_%d")) + '_NSGAIII_results_' + str(iteration)
    # if not os.path.exists(file_dir_eval):
    #     os.mkdir(file_dir_eval)

    """===============================实例化问题对象============================"""
    # problem = MyProblem(Goal_num, file_dir_sce, file_dir_data, file_dir_eval, config)  # 生成问题对象
    problem = AdaptObj(Goal_num, file_dir_sce, file_dir_data, file_dir_eval, config)  # 生成问题对象

    """==================================种群设置==============================="""
    Encoding = 'RI'  # 编码方式
    NIND = config.population  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）


    """=================================算法参数设置============================"""
    # myAlgorithm = My_moea_NSGA3_templet(problem, population)
    myAlgorithm = My_moea_NSGA2_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXTIME = config.searchTimeout  # 0.2限时0.2秒
    myAlgorithm.MAXGEN = config.maxIterations  # 最大进化代数
    myAlgorithm.logTras = 1  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    bestpop = BestPop (config)

    gl._init()
    gl.set_value('Configure', config)
    gl.set_value('Problem', problem)
    gl.set_value('Algorithm', myAlgorithm)
    gl.set_value('BestPop', bestpop)

    """==========================调用算法模板进行种群进化=========================
    调用run执行算法模板，得到帕累托最优解集NDSet以及最后一代种群。NDSet是一个种群类Population的对象。
    NDSet.ObjV为最优解个体的目标函数值；NDSet.Phen为对应的决策变量值。
    详见Population.py中关于种群类的定义。
    """
    [NDSet, population] = myAlgorithm.run()  # 执行算法模板，得到非支配种群以及最后一代种群
    NDSet.save()  # 把非支配种群的信息保存到文件中
    # problem.pool.close()  # 及时关闭问题类中的池，否则在采用多进程运算后内存得不到释放

    """==================================输出结果=============================="""
    print('Time: %f'%(myAlgorithm.passTime))
    print('Eval: %d'%(myAlgorithm.evalsNum))
    print('Non-dominated: %d'%(NDSet.sizes))
    print('PFnumber per time unit: %d'%(int(NDSet.sizes //
    myAlgorithm.passTime)))
    # 计算指标
    PF = problem.getReferObjV() # 获取真实前沿
    if PF is not None and NDSet.sizes != 0:
        GD = myAlgorithm.indicator.GD(NDSet.ObjV, PF) # 计算GD指标
        IGD = myAlgorithm.indicator.IGD(NDSet.ObjV, PF) # 计算IGD指标
        HV = myAlgorithm.indicator.HV(NDSet.ObjV, PF) # 计算HV指标
        Spacing = myAlgorithm.indicator.Spacing(NDSet.ObjV) # 计算Spacing指标
        print('GD: %f'%GD)
        print('IGD: %f'%IGD)
        print('HV: %f'%HV)
        print('Spacing: %f'%Spacing)

    """=============================进化过程指标追踪分析========================"""
    if PF is not None:
        metricName = [['IGD'], ['HV']]
        [NDSet_trace, Metrics] = myAlgorithm.indicator.moea_tracking(myAlgorithm.pop_trace, PF, metricName, problem.maxormins)
        # 绘制指标追踪分析图
        myAlgorithm.trcplot(Metrics, labels = metricName, titles = metricName)

    outputfile.close()

    # with open(file_name,'w') as f:
    #     for line in f:
    #         line = line.encode('utf-8')
    #         f.write(line)

