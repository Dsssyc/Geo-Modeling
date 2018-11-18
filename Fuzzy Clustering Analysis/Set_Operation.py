from Math_Algorithm import Euclidean_Distance, Normalization, Cosine_Distance
import numpy as np

"""
本文件汇总了模糊聚类应用中需使用的集合运算操作
----------------------------------------
function:

Max_Min_Compound_Operation() 最大最小复合运算
Max_DotProduct_Compound_Operation() 最大点积符合运算
Similarity_Coefficient_Matrix() 相似系数矩阵求算
Passive_Closure_Algorithm() 遗传闭包算法
Binarization() 矩阵二值化
Row_Classificarion() 矩阵按行数据分类操作
"""
def Max_Min_Compound_Operation(array1, array2):
    # 判断两矩阵的共同边长度是否一致
    if array1.shape[1] != array2.shape[0]:
        return OSError
    
    x = 0
    max_com = np.empty([array1.shape[0], array2.shape[1]])  # 定义最大复合矩阵
    # 遍历两个矩阵并按规则进行最小复合运算
    while x < array1.shape[0]:
        z = 0
        while z < array2.shape[1]:
            y = 0
            min_com = []
            while y < array1.shape[1]:
                min_com.append(min(array1[x, y], array2[y, z]))     # 将较小值传入列表min_com
                y += 1
            max_com[x, z] = max(min_com)    # 将min_com中的最大值传入最大复合矩阵
            z += 1
        x += 1
    return max_com

def Max_DotProduct_Compound_Operation(array1, array2):
    # 判断两矩阵的共同边长度是否一致
    if array1.shape[1] != array2.shape[0]:
        return OSError
    
    x = 0
    max_com = np.empty([array1.shape[0], array2.shape[1]])  # 定义最大复合矩阵
    # 遍历两个矩阵并按规则做点击运算
    while x < array1.shape[0]:
        z = 0 
        while z < array2.shape[1]:
            y = 0
            dot_pro = []
            while y < array1.shape[1]:
                dot_pro.append(array1[x, y] * array2[y, z])     # 将乘积数组存入dot_Pro链表
                y += 1
            max_com[x, z] = max(dot_pro)    # 将dot_pro中的最大值传入最大复合矩阵
            z += 1
        x += 1
    return max_com

def Similarity_Coefficient_Matrix(array, _type='Eu_Dist'):
    # 定义集合A对应原矩阵行号set1， 距离矩阵dist
    set1, dist = 0, np.empty([array.shape[0], array.shape[0]])
    # 遍历矩阵并进行距离运算
    while set1 < array.shape[0]:
        set2 = 0
        while set2 < array.shape[0]:
            if _type == 'Eu_Dist' :
                dist[set1, set2] = Euclidean_Distance(array[set1, :], array[set2, :])
            if _type == 'Cos_Dist':
                dist[set1, set2] = Cosine_Distance(array[set1, :], array[set2, :])            
            set2 += 1
        set1 +=1
    # 如果距离类型为欧式距离，则对数据进行归一化操作
    if _type == 'Eu_Dist':
        result = Normalization(dist)
        return result  
    return dist

def Passive_Closure_Algorithm(array, method= 'MaxMinCom'):
    # 定义复合运算方法矩阵，key为运算名称，value为运算函数
    operation = {'MaxMinCom': Max_Min_Compound_Operation,
                 'MaxDotPro': Max_DotProduct_Compound_Operation}
    # 定义计数器、中间过程字典和元数据矩阵
    count, proSet, oArray= 2, {'1': array}, array
    rArray = operation[method](array, array)    # 定义结果矩阵
    # 若结果矩阵和元数据矩阵不等，则继续进行矩阵复合运算
    while  not (rArray == oArray).all():
        oArray = rArray
        proSet['{}'.format(str(count))] = oArray
        rArray = operation[method](oArray, oArray)
        count += 1
    return oArray, proSet

def Binarization(array, threshold):
    row = 0
    matrix = np.empty(array.shape)
    while row < array.shape[0]:
        col = 0
        while col < array.shape[1]:
            if array[row, col] >= threshold:
                matrix[row, col] = 1
            else:
                matrix[row, col] = 0
            col += 1
        row += 1
    return matrix

def Row_Classification(array):
    # 利用项头链表存储行数据， 建立字典存储分类结果
    # 字典格式为：key: 各类别的行数据，value: 对应行号构成的链表

    # 为降低消耗，分类循环中设置key值来判断待分类行数据是否已进行归类；
    # 若已归类, 即结果字典中已含有行号，则key为False，且不再做对比遍历；
    # 否则key为True，并进行遍历
    size = array.shape[0]   # 设置循环上限为矩阵行数
    count = 0
    _list = []      # 设置项头链表
    # 对项头链表进行赋值，赋值元素为待分类矩阵的行数据
    while count < size:
        _list.append(array[count, :])
        count += 1
    
    # 设置分类循环并定义结果字典
    i, result = 0, {}
    while True:
        # 判断是否进行遍历
        key = True
        for element in result.values():
            if i in element:
                key = False
        # 遍历并分类
        if key == True:
            result['{}'.format(str(_list[i]))] = []     # 在字典中添加key为当前行数据，value为链表结构的项
            result['{}'.format(str(_list[i]))].append(i)    # 将当前行号添加进该项

            # 利用当前行数据对之后行数据做循环比较
            j = i + 1   # 定义待比较行号
            while j < size:
                if (_list[i] == _list[j]).all():    # 判断两个一维数组是否完全一致
                    result['{}'.format(str(_list[i]))].append(j)      # 完全一致则添加进结果字典对应的分类
                j += 1
        i += 1

        if i >= size:
            break
    return result
