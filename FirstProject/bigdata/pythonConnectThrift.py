# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:37:37 2018

@author: Zheng He
"""

#from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
#from hbase.ttypes import ColumnDescriptor, Mutation, BatchMutation, NotFound

#server端地址和端口
transport = TSocket.TSocket('172.16.33.11', 9090)
#可以设置超时
transport.setTimeout(5000)
#设置传输方式（TFramedTransport或TBufferedTransport）
trans = TTransport.TBufferedTransport(transport)
#设置传输协议
protocol = TBinaryProtocol.TBinaryProtocol(trans)
client = Hbase.Client(protocol)
#确定客户端
#client = Hbase.Client(protocol)
#打开连接
transport.open()
print(client.getTableNames())

