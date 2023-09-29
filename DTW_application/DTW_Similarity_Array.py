import os
import re

import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

#设置Excel文件夹的路径
filePath = r"D:\DTW_application\Rawdata"
#获取文件夹下的所有文件名称
nameList = os.listdir(filePath)
# print(nameList)

k=0
for i in nameList:
    #使用pandas中的read_excel函数读取文件
    temp = pd.read_excel(filePath + "//" + i, index_col=0)#, index_col=0(有时间就加这个)
    print("****************************************************")
    # print(temp)
    dataframe1 = temp
    # print(dataframe1)
    approach_list = re.findall(r'\w+',i)#寻找非均匀电阻的位置
    approach_list = approach_list[:len(approach_list)-1]#位置与方法清单
    print(approach_list)

    if k==0:
        dataframe2 = dataframe1
        dataframe2.columns=[i[:len(i)-5]]
        print("loading...")
        k += 1
    else:
        print(dataframe2)
        dataframe2.insert(loc=len(dataframe2.columns),column=i[:len(i)-5],value=dataframe1)
        print("loading...")
        k+=1
    print("****************************************************")

numpy = dataframe2.to_numpy()
print(numpy)

# print(list(dataframe2))#获取序号




# numpy1=numpy[:,3][:,np.newaxis]
# print(numpy1.shape)
# print(numpy1[~np.isnan(numpy1).any(axis=1)])

m=0
n=0
cost_table = np.zeros((numpy.shape[1],numpy.shape[1]), dtype=np.float)
while m < numpy.shape[1]:
    while n < numpy.shape[1]:
        numpy1=numpy[:,m][:,np.newaxis]#保持维度不丢失
        numpy2=numpy[:,n][:,np.newaxis]
        # print(numpy1[~np.isnan(numpy1).any(axis=1)].transpose())
        # print(numpy2[~np.isnan(numpy2).any(axis=1)].transpose())
        distance, path = fastdtw(numpy1[~np.isnan(numpy1).any(axis=1)], 
                                numpy2[~np.isnan(numpy2).any(axis=1)], dist=euclidean)

        cost_table[m,n] =distance
        n+=1
    m+=1
    n=0

# print(cost_table)
cost_table_df = pd.DataFrame(cost_table,index=list(dataframe2),columns=list(dataframe2))
print(cost_table_df)
cost_table_df.to_excel("Similarity.xlsx",sheet_name='sheet1')  # 此处修改EXCEL的名称和SHEET
print("***已使用dataframe更新excel***")
print("***完成***")
