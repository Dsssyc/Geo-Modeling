import sys
from Fuzzy_GUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import File_Operation as fo
import Fuzzy_Clustering as fc
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QFileDialog, QGridLayout

"""
本文件为模糊聚类程序的主文件，运行该文件可以得到模糊聚类的窗体应用程序
----------------------------------------
class Myfigure:

该类以matplotlib库中的FigureCanvas类做父类，用于创建散点图显示部件；
运用该类可以对窗体程序中的显示部件（Matplot）做覆盖，使分类散点图嵌入窗体中；
散点图为显示不同分类阈值下(以0.1为间隔)数据分类的变化情况

<----函数介绍---->

__init__() 对MyFigure类对象初始化，将其定义为兼具FigureCanvas和QWidgets身份的对象
plotScatter() 为散点图绘制函数，利用该函数完成对子画布的更新，绘制操作
----------------------------------------
class Fuzzy_Clustering_Tool:

该类以PyQT5库中的QMainWindow类和designer生成的窗体基类Ui_MainWindow为父类；
注：designer为窗体应用绘制工具，使用方法类似C#的窗口拖动绘制功能

<----函数介绍---->

__init__() 对模糊聚类工具窗体对象进行激活、初始化，并显示应用窗体
initUI() 实现具体的窗体对象初始化方法，其中包含各窗体部件和功能实现的细节
Open_File() 执行打开文件命令
Choose_Dist(), Choose_Operation() 用于选择距离公式和集合复合运算方法
Martrix_Operation() 求算等价模糊矩阵并获取不同分类阈值下的分类情况
Fuzzy_Classification() 利用输入的阈值进行分类
Save_File() 执行保存结果文件命令
"""

class MyFigure(FigureCanvas):
    def __init__(self, width = 5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)     # 继承Figure类
        super(MyFigure, self).__init__(self.fig)    # 继承QWidgets类并激活
        self.axes = self.fig.add_subplot(111)   # 创建子画布，命名为'111'

    def plotScatter(self, cutSet):
        # 确定散点图的x, y轴分别对应的内容
        x, y =[], []
        for key in cutSet:
            x.append(float(key))    # x轴对应的是每类截集的分类阈值
            y.append(len(cutSet[key]))  # y轴为每类截集对应的个数 

        # 绘制散点图
        self.axes.cla()     # 更新子画布
        self.axes.plot(x, y, 'o--')     # 绘制画布，设置绘制格式为'点-虚线'
        self.draw()     # 动态绘制画布

class Fuzzy_Clustering_Tool(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()  # 激活对象
        self.setupUi(self)  # 创建窗体
        self.initUI()   # 调用UI定义函数
        self.show()     # 绘制窗体

    def initUI(self):
        # 初始化矩阵数据，待处理数据，等价模糊矩阵数据，分类结果数据
        self.data, self.pendingData, self.efMatrix, self.classfication  = None, '', '', ''  
        self.Euclidean.setChecked(True)     # 默认选择欧式距离
        self.MaxMinCom.setChecked(True)     # 默认选择最大最小复合
        self.figure = MyFigure()    # 定义散点图显示部件
        self.actionOpen_File.triggered.connect(self.Open_File)  # 点击菜单栏-Open File命令时连接Open_File函数
        self.actionSave_As.triggered.connect(self.Save_File)    # 点击菜单栏-Save As命令时连接Save_File函数
        self.Operation_Button.clicked.connect(self.Martix_Operation)    # 点击运算按键时连接Matrix_Operation函数
        self.Classification_Button.clicked.connect(self.Fuzzy_Classification)   # 点击分类按键时连接Fuzzy_Classification函数
    
    def Open_File(self):
        # 打开文件对话框并获取文件名， 只允许打开.txt文件
        filename = QFileDialog.getOpenFileName(self, '选取文本文件', "./", "Text Files (*.txt)")[0]     
        if filename != '':      # 若获取的文件名不为空则执行读取操作
            data = fo.Read2Array(filename, False)[0]    # 将数据文件中内容以保留第一行的形式读取为矩阵
            self.data= fo.Read2Array(filename, True)[0]     # 将数据文件中内容以不保留第一行的形式读取为全局数据矩阵
            self.pendingData = fo.Array2Str(data)   # 将转换为字符串格式的矩阵数据保存进预处理变量
            data = fo.Array2Str(data)   # 将矩阵转换为字符串格式
            self.Data.setPlainText(data)   # 显示矩阵

    def Choose_Dist(self):
        # dist为待传入fc.Fuzzy_Clustering对象的参数
        if self.Euclidean.isChecked():
            dist = 'Eu_Dist'
        if self.Cosine.isChecked():
            dist = 'Cos_Dist'
        return dist
    
    def Choose_Operation(self):
        # operation为待传入fc.Fuzzy_Clustering对象的参数
        if self.MaxMinCom.isChecked():
            operation = 'MaxMinCom'
        if self.MaxDotPro.isChecked():
            operation = 'MaxDotPro'
        return operation

    def Martix_Operation(self):
        # 执行矩阵运算前判断是否已读入数据文件
        if self.data is None:
            self.Data.setText('请先导入文件')
            return False
        
        result = '' # 定义结果变量
        # 建立模糊聚类矩阵对象
        dist = self.Choose_Dist()
        operation = self.Choose_Operation()
        self.fcm = fc.Fuzzy_Clustering(self.data, dist, operation)
        # 判断是否显示并保存中间过程
        if self.Process.isChecked():
            result += fo.Proset2Str(self.fcm.proSet)
        # 对结果变量赋值并显示
        result += '等价模糊矩阵:\n' + fo.Array2Str(self.fcm.efMatrix)
        self.Fmatrix.setPlainText(result)
        self.efMatrix = result  # 将结果写进全局等价模糊矩阵变量
        # 绘制散点图
        self.figure.plotScatter(self.fcm.CutSet_Iteration())    # 执行散点图绘制函数
        self.gridlayout = QGridLayout(self.MatPlot)     # 重定义MatPlot部件所在位置
        self.gridlayout.addWidget(self.figure, 0, 1)    # 将重定义的位置替换为散点图

    def Fuzzy_Classification(self):
        threshold = self.Threshold.toPlainText()    # 获取输入的分类阈值
        # 判断分类阈值是否为空
        if threshold == '':
            self.Threshold.setText('请输入分类阈值')
            return False
        
        result = self.fcm.Classification(float(threshold))      # 将模糊聚类矩阵对象的分类结果写入结果变量
        result = fo.Classification2str(result)      # 将分类结果转换为字符串格式
        self.Result.setPlainText(result)    # 显示分类结果
        self.classfication = result     # 将分类结果写入全局分类结果变量

    def Save_File(self):
        # 打开保存文件对话框并获取文件名， 只允许保存为.txt文件
        filename = QFileDialog.getSaveFileName(self, '保存文本文件', "./", "Text Files (*.txt)")[0]
        # 判断获取的文件名是否为空，不是则写入并保存结果文件
        if filename != '':
            file = open(filename, 'w', encoding='utf-8')
            result = '数据：\n' + self.pendingData + '\n\n\n' + self.efMatrix + '\n\n\n' + '分类结果：\n' + self.classfication 
            file.write(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)    # 启动应用线程
    ex = Fuzzy_Clustering_Tool()    # 绘制应用
    sys.exit(app.exec_())   # 关闭线程