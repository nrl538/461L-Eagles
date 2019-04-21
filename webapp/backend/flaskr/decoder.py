# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:17:15 2019

@author: Doly
"""
import pandas as pd
import re
dataframe=pd.read_csv('C:\\Users\\Doly\\Desktop/RedditResults.csv')

df=dataframe.values.tolist()
for i in range(len(df)):
    row = df[i]
    for j in range(len(row)):
        '''
        if type(row[j])==str:
            df[i][j]=row[j].replace('（','(').replace('）',')').replace('，',',').replace('；',';').replace('：',':').replace('”','"').replace('“','"').replace('。','.').replace('、','/').replace('？','?').replace('’',"'").replace('‘',"'").replace('…','...')
        '''
        if type(df[i][j])==str:
            df[i][j]=re.sub("[^A-Za-z0-9\.\,\?\!\(\)\;\:\'\"\\n\ \/\=\+\-\_\*\#\%_]+", '', df[i][j])
writerCSV=pd.DataFrame(data=df)   
writerCSV.to_csv('C:\\Users\\Doly\\Desktop/fixedReddit.csv',encoding='utf-8')    