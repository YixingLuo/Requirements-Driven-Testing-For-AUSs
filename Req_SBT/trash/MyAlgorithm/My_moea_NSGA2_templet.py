# -*- coding: utf-8 -*-
""" QuickStart """
import sys
sys.path.append("../../Random")
import numpy as np
import geatpy as ea


class My_moea_NSGA2_templet(ea.moea_NSGA2_templet):
    def terminated(self, pop):  # 判断是终止进化，pop为当代种群对象
        self.stat(pop)  # 进行统计分析，更新进化记录器

        if self.passTime >= self.MAXTIME:  # 增加时间限制
            return True
        if self.currentGen + 1 >= self.MAXGEN:
            return True
        else:
            self.currentGen += 1  # 进化代数+1
            return False

    # def logging(self, pop):
    #
    #     """
    #     描述:
    #         用于在进化过程中记录日志。该函数在stat()函数里面被调用。
    #         如果需要在日志中记录其他数据，需要在自定义算法模板类中重写该函数。
    #
    #     输入参数:
    #         pop : class <Population> - 种群对象。
    #
    #     输出参数:
    #         无输出参数。
    #
    #     """
    #
    #     self.passTime += time.time() - self.timeSlot  # 更新用时记录，不计算logging的耗时
    #     if len(self.log['gen']) == 0:  # 初始化log的各个键值
    #         if self.problem.ReferObjV is not None:
    #             self.log['gd'] = []
    #             self.log['igd'] = []
    #         self.log['hv'] = []
    #         self.log['spacing'] = []
    #     self.log['gen'].append(self.currentGen)
    #     self.log['eval'].append(self.evalsNum)  # 记录评价次数
    #     [levels, _] = ea.ndsortDED(pop.ObjV, needLevel=1, CV=pop.CV, maxormins=self.problem.maxormins)  # 非支配分层
    #     NDSet = pop[np.where(levels == 1)[0]]  # 只保留种群中的非支配个体，形成一个非支配种群
    #     if self.problem.ReferObjV is not None:
    #         self.log['gd'].append(ea.indicator.GD(NDSet.ObjV, self.problem.ReferObjV))  # 计算GD指标
    #         self.log['igd'].append(ea.indicator.IGD(NDSet.ObjV, self.problem.ReferObjV))  # 计算IGD指标
    #         self.log['hv'].append(ea.indicator.HV(NDSet.ObjV, self.problem.ReferObjV))  # 计算HV指标
    #     else:
    #         self.log['hv'].append(ea.indicator.HV(NDSet.ObjV))  # 计算HV指标
    #     self.log['spacing'].append(ea.indicator.Spacing(NDSet.ObjV))  # 计算Spacing指标
    #     self.timeSlot = time.time()  # 更新时间戳
    #
    # def display(self):
    #
    #     """
    #     描述:
    #         该函数打印日志log中每个键值的最后一条数据。假如log中只有一条数据或没有数据，则会打印表头。
    #         该函数将会在子类中被覆盖，以便进行更多其他的输出展示。
    #
    #     """
    #
    #     self.passTime += time.time() - self.timeSlot  # 更新用时记录，不计算display()的耗时
    #     headers = []
    #     widths = []
    #     values = []
    #     for key in self.log.keys():
    #         # 设置单元格宽度
    #         if key == 'gen':
    #             width = max(3, len(str(self.MAXGEN - 1)))  # 因为字符串'gen'长度为3，所以最小要设置长度为3
    #         elif key == 'eval':
    #             width = 8  # 因为字符串'eval'长度为4，所以最小要设置长度为4
    #         else:
    #             width = 13  # 预留13位显示长度，若数值过大，表格将无法对齐，此时若要让表格对齐，需要自定义算法模板重写该函数
    #         headers.append(key)
    #         widths.append(width)
    #         value = self.log[key][-1] if len(self.log[key]) != 0 else "-"
    #         if isinstance(value, float):
    #             values.append("%.5E" % value)  # 格式化浮点数，输出时只保留至小数点后5位
    #         else:
    #             values.append(value)
    #     if len(self.log['gen']) == 1:  # 打印表头
    #         header_regex = '|'.join(['{}'] * len(headers))
    #         header_str = header_regex.format(*[str(key).center(width) for key, width in zip(headers, widths)])
    #         print("=" * len(header_str))
    #         print(header_str)
    #         print("-" * len(header_str))
    #     if len(self.log['gen']) != 0:  # 打印表格最后一行
    #         value_regex = '|'.join(['{}'] * len(values))
    #         value_str = value_regex.format(*[str(value).center(width) for value, width in zip(values, widths)])
    #         print(value_str)
    #     self.timeSlot = time.time()  # 更新时间戳