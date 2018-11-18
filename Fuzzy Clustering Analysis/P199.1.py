import pandas as pd
import numpy as np
import Set_Operation as so

excel_path = 'Data.xlsx'
setData = pd.read_excel(excel_path, sheetname='因素集合', index_col=0)
teacherWeight = pd.read_excel(excel_path, sheetname='教师权重', index_col=0)

sData = setData.to_string()
sTeacherWeight = teacherWeight.to_string()

comment = setData.columns.values.tolist()
data = np.array(setData)
weight = np.array(teacherWeight)
result = so.Max_Min_Compound_Operation(weight, data)
where = np.where(np.max(result))[0][0]
# print('该教师讲课质量为：' + comment[where])

rString = '教师讲课因素与评语集合:\n{}\n\n某教师权重分配:\n{}\n\n该教师讲课质量综合评判结果：\n{}\n\n最终评价: {}'.format(sData, sTeacherWeight, result, comment[where])
print(rString)