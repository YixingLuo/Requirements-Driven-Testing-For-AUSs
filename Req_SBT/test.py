import uuid
import os
import time
from test2 import temp
import numpy as np

# def get_time_stamp():
#     ct = time.time()
#     local_time = time.localtime(ct)
#     data_head = time.strftime("%Y%m%d%H%M%S", local_time)
#     data_secs = (ct - int(ct)) * 1000
#     time_stamp = "%s_%02d" % (data_head, data_secs)
#     return time_stamp
#
# # 生成一个随机字符串
# uuid_str =  str(uuid.uuid4())
# # 构成完整文件存储路径
# tmp_file_name =  "scenario_" + get_time_stamp() + ".json"
# print(tmp_file_name)
# tmp_f_path = os.path.join(os.getcwd(),tmp_file_name)
# # 打开文件，完成数据写入
# tmp_f = open(tmp_f_path,'wb')

# foo = "ar"
#
#
#
# if __name__ == "__main__":
#
#     temp()
#     print(foo)


# pop = []
#
# fileList  = os.listdir('2020_11_29_NSGAII_results_10000')
# fileList.sort()
# print(fileList)
# for i in range (len(fileList)-20, len(fileList)):
#     textname = '2020_11_29_NSGAII_results_10000/' + fileList[i]
#     print(textname)
#     a = np.loadtxt(textname)
#     pop.append(list(a))
# print(pop, pop[0][1])
#
# print(min(pop))

a = [[1.0, 0.0, 0.973166, 1.0, 1.0, 0.983779], [1.0, 1.0, 1.0, 1.0, 1.0, 0.950004], [0.99792, 0.84416, 0.996558, 1.0, 1.0, 0.950422], [1.0, 1.0, 1.0, 1.0, 1.0, 0.959863], [1.0, 1.0, 1.0, 1.0, 1.0, 0.96099], [1.0, 1.0, 1.0, 1.0, 1.0, 0.962109], [1.0, 0.926184, 0.999432, 1.0, 1.0, 0.977814], [1.0, 0.882089, 0.999093, 1.0, 1.0, 0.972261], [1.0, 1.0, 1.0, 1.0, 1.0, 0.982591], [1.0, 1.0, 1.0, 1.0, 1.0, 0.984811], [1.0, 0.953279, 0.999493, 1.0, 1.0, 0.96406], [1.0, 0.895158, 0.999107, 1.0, 1.0, 0.987381], [0.999996, 0.298834, 0.986329, 1.0, 1.0, 0.96464], [1.0, 1.0, 1.0, 1.0, 1.0, 0.960513], [1.0, 0.918075, 0.999402, 1.0, 1.0, 0.974045], [1.0, 1.0, 1.0, 1.0, 1.0, 0.976589], [1.0, 0.573067, 0.993724, 1.0, 1.0, 0.961895], [1.0, 1.0, 1.0, 1.0, 1.0, 0.980566], [1.0, 1.0, 1.0, 1.0, 1.0, 0.974587], [1.0, 0.175311, 0.982698, 1.0, 1.0, 0.982706]]
print(min(a))

b = [[1.0, 0.953279, 0.999493, 1.0, 1.0, 0.96406], [1.0, 0.895158, 0.999107, 1.0, 1.0, 0.987381], [0.999996, 0.298834, 0.986329, 1.0, 1.0, 0.96464], [1.0, 1.0, 1.0, 1.0, 1.0, 0.960513], [1.0, 0.918075, 0.999402, 1.0, 1.0, 0.974045], [1.0, 1.0, 1.0, 1.0, 1.0, 0.976589], [1.0, 0.573067, 0.993724, 1.0, 1.0, 0.961895], [1.0, 1.0, 1.0, 1.0, 1.0, 0.980566], [1.0, 1.0, 1.0, 1.0, 1.0, 0.974587], [1.0, 0.175311, 0.982698, 1.0, 1.0, 0.982706]]
print(min(b))