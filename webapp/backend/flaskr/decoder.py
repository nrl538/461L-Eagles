# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:17:15 2019

@author: Doly
"""
import pandas as pd
df=pd.read_csv('C:\\Users\\Doly\\Desktop/bookdata1.csv')
'''
df=df.values.tolist()
for i in range(len(df)):
    row = df[i]
    for j in range(len(row)):
        if type(row[j])==str:
            df[i][j]=row[j].replace('（','(').replace('）',')').replace('，',',').replace('；',';').replace('：',':').replace('”','"').replace('“','"').replace('。','.').replace('、','/').replace('？','?').replace('’',"'").replace('‘',"'").replace('…','...')
writerCSV=pd.DataFrame(data=df)   
'''
df.to_csv('C:\\Users\\Doly\\Desktop/fixedbookdata.csv',encoding='utf-8')    