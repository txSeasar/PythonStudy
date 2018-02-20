# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:40:48 2018

@author: gaoyf
"""
import numpy as np
import pandas as pd

def computeSelfVarCorr(computeDf):
    computeResult = None
    
    if computeDf is not None:
        for var in computeDf.columns:
            oneCorrRet = computeDf.corrwith(computeDf[var])
            varArr = np.tile(['%s%s' % (var,'-')],oneCorrRet.size)
            indexArr = pd.Series(varArr).str.cat(oneCorrRet.index.values,sep='')
                        
            oneCorrRetDf = pd.DataFrame(np.array([indexArr,oneCorrRet]).T,columns=['name','corr'])
            
            if computeResult is None:
                computeResult = oneCorrRetDf
            else:
                computeResult = computeResult.append(oneCorrRetDf, ignore_index=True)
                #break;
    
    return computeResult

fileDataDf = pd.DataFrame(pd.read_csv('../data/out/OpenPric100.csv',sep=',',encoding='gbk'))
result = computeSelfVarCorr(fileDataDf.drop(['开始时间'],axis=1))
print(result.sort_values('corr',axis=0,ascending=False))

fileDataDf[['600000','600015','600064','600121']].plot()
        