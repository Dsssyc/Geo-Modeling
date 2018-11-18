from math import sqrt
import numpy as np
"""
本文件为数学算法的继承文件
"""
def Euclidean_Distance(array1, array2):
    # 判断两矩阵规模是否一致
    if array1.size != array2.size:
        return OSError

    size, count, _sum = array1.size, 0, 0
    while count < size:
        _sum += (array1[count] - array2[count]) ** 2
        count += 1
    result = sqrt(_sum)
    return result

def Normalization(array):
    _max = np.max(array)    # 选出欧式距离矩阵中的最大值
    result = 1 - array / _max   # 对矩阵进行归一化运算
    return result

def Cosine_Distance(array1, array2):
    # 判断两矩阵规模是否一致
    if array1.size != array2.size:
        return OSError

    size, count = array1.size, 0
    _sum, _sum1, _sum2 = 0, 0, 0

    while count < size:
        _sum += array1[count] * array2[count]
        _sum1 += array1[count] ** 2
        _sum2 += array2[count] ** 2
        count += 1

    result = _sum / sqrt(_sum1 * _sum2)
    return result
