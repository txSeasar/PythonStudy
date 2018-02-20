# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:24:08 2018

@author: gaoyf
"""

import os
import numpy as np
import pandas as pd
#from pandas import Series,DataFrame

rootDir = '../data'
#analysisVars = ['股票代码','成交量','成交额','开盘价（前复权）','最低价（前复权）','最高价（前复权）','收盘价（前复权）']
analysisVars = ['股票代码','开始时间','开盘价（前复权）']


#dataFrameStock = pd.DataFrame(pd.read_csv('../data/600000.csv',sep=',',encoding='gbk')) 

#dataFrameStock[analysisVars]

def getFileNameList(dir):
    
    filePathArr = []
    
    dirFileNameList = os.listdir(rootDir)
    for fileName in dirFileNameList:
        filePathArr.append(os.path.join(rootDir,fileName))
        print(os.path.join(rootDir,fileName))
        
    return filePathArr

def readVarsFromFiles(filePathList,varArray):
    resultDf = None
    for filePath in filePathList:
        print('Else',filePath)
        if os.path.isdir(filePath) :
            continue
            
        fileDataDf = pd.DataFrame(pd.read_csv(filePath,sep=',',encoding='gbk'))
        fileDataDf = fileDataDf[varArray]
        stockCode = fileDataDf.pop('股票代码')
        fileDataDf.rename(columns={'开盘价（前复权）':stockCode[0]},inplace=True)
        
        if resultDf is None :
            resultDf =   fileDataDf
            print(fileDataDf)
        else:
            #resultDf = pd.concat([resultDf,fileDataDf[varArray]],axis=1)
            resultDf = pd.merge(resultDf,fileDataDf,left_on='开始时间',right_on='开始时间',how='left')
        
    return resultDf

filePathList = getFileNameList(rootDir)
data = readVarsFromFiles(filePathList,analysisVars)

if not os.path.exists('%s%s' % (rootDir,'/out')):
    os.makedirs('%s%s' % (rootDir,'/out'))

data.to_csv('%s%s' % (rootDir,'/out/OpenPric100.csv'),index=False)

data.plot()

print(data.describe())

        