import numpy as np

"""
本文件汇总了模糊聚类应用需使用的文件操作函数
----------------------------------------
function:

Read2Array() 读取文件并保存为numpy.array数据格式
Array2Str() 将numpy.array数据转换成字符串格式
Proset2Str() 将求算等价模糊矩阵时产生的中间过程转换为字符串格式
Classification2str() 将模糊聚类结果转换为字符串格式
"""

def Read2Array(filename, NameFiled = True):
    # 判断文件是否为.txt格式
    if '.txt' not in filename:
        return OSError
    # 按行读取文件内容，山区字符串中全部'\n'
    file = open(filename, 'r', encoding='utf-8')
    lines = [line.replace('\n', '') for line in file.readlines()]
    # 判断NameField是否为真，若是则提取数据首行内容
    rArray = []
    if NameFiled == True:
        nameFiled = []
        for element in lines[0].split('\t'):    # 按'\t'切分首行字符串
            nameFiled.append(element)
        nameFiled = np.array(nameFiled)     # 将保存为链表形式的首行数据转换为矩阵
        # 读取首行以外的其他行数据
        for line in lines[1:]:
            array = []
            for element in line.split('\t'):    # 按'\t'切分各行字符串
                array.append(float(element))    # 将切分的各字符串转换为float型数据
            rArray.append(array)
        rArray = np.array(rArray)   # 将保存为链表形式的结果矩阵数据转换为矩阵
        return rArray, nameFiled    # 返回除去首行的结果矩阵和名称字段(首行)矩阵
    # 如果NameFiled为假， 则不提取首行数据
    if NameFiled == False:
        for line in lines:
            array = []
            for element in line.split('\t'):
                array.append(element)
            rArray.append(array)
        rArray = np.array(rArray)
        return rArray, None

def Array2Str(array):
    string = ''
    for row in array:   # 遍历矩阵的各行
        for element in row:     # 遍历矩阵各行的各元素
            string += str(element) + '\t'   # 将各元素添加进结果字符串，并用'\t'做间隔
        string.rstrip('\t')
        string += '\n'  # 各行结尾用'\n'换行
    return string

def Proset2Str(proSet):
    string = ''
    for proArray in proSet:    # 遍历中间过程中的各矩阵的key
        count = 2 ** (int(proArray) - 1)    # 由于遗传闭包算法中使用的是平方法，因此复合次数要进行平方
        string += '第{}次复合运算:\n'.format(str(count)) + Array2Str(proSet[proArray]) + '\n\n'
    return string

def Classification2str(result):
    string = ''
    count = 1
    for element in result.values():
        string += '第{}类：\n'.format(str(count))
        for value in element:
            string += '{}'.format(str(value+1)) + '\t'
        string += '\n\n'
        count += 1
    return string

if __name__ == '__main__':
    y, z = Read2Array('test data.txt', True)
    print(y)
    