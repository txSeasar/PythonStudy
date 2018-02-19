# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:24:08 2018

@author: gaoyf
"""

import pandas as pd
#from pandas import Series,DataFrame

dataFrameStock = pd.DataFrame(pd.read_csv('../data/600000.csv',sep=',',encoding='gbk')) 

dataFrameStock

