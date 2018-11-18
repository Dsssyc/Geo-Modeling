import Math_Algorithm as ma
import Set_Operation  as so
import numpy as np

"""
本文件为定义Fuzzy Clustering类，继承了数学算法和集合操作内容，以供其它需要利用模糊矩阵与模糊聚类的文件使用
----------------------------------------
class Fuzzy_Clustering:

该类继承了求算等价模糊矩阵在内的多种运算函数；
通过建立一个模糊矩阵对象可以连接其他相关运算

<----函数介绍---->

__init__() 载入基本参数以初始化对象，参数包括原数据矩阵、距离类型(默认欧式距离)、复合类型(默认最大最小复合)
Classification() 载入分类阈值得到对应的模糊分类情况
CutSet_Itrtation() 以默认间隔0.1迭代计算不同分类阈值对应的分类情况
"""

class Fuzzy_Clustering:
    def __init__(self, array, disType = 'Eu_Dist', co_method= 'MaxMinCom'):
        self.array = array  # 对元数组变量赋值
        self._type = disType    # 设置距离类型
        self.scMatrix = so.Similarity_Coefficient_Matrix(array, self._type)     # 获取相似系数矩阵
        self.efMatrix, self.proSet = so.Passive_Closure_Algorithm(self.scMatrix, co_method)     # 获取等价模糊矩阵和中间过程
    
    def Classification(self, threshold):
        bMatrix = so.Binarization(self.efMatrix, threshold)     # 利用分类阈值获得二值化矩阵
        result = so.Row_Classification(bMatrix)     # 对二值化矩阵按行分类
        return result

    def CutSet_Iteration(self, step= 0.1):
        result = {}
        threshold = 1.0     # 设置分类阈值上限
        # 以step为间隔循环分类操作
        while threshold >= 0:
            bMatrix = so.Binarization(self.efMatrix, threshold)
            rDict = so.Row_Classification(bMatrix)  # 将分类结果赋值给rDict
            result['%0.1f'%threshold] = rDict   # 对结果变量添加(分类阈值：rDict)字典元素
            threshold -= step
        return result

if __name__ == '__main__':
    # 测试
    a = np.array([[1,1016,2359,1.04],
                  [2,928,2087,1.01],
                  [3,650,1959,.83],
                  [4,576,1691,.65],
                  [5,540,1532,.74],
                  [6,829,1987,.70],
                  [7,638,1641,.73],
                  [8,621,1611,.77],
                  [9,1234,2925,.98],
                  [10,852,2101,.72]])

    test = Fuzzy_Clustering(a, co_method='MaxMinCom')
    r = test.CutSet_Iteration()
    print(test.efMatrix)
        