# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:13:46 2018

@author: gaoyf
"""
#

import tensorflow as tf
import numpy as np

#use numpy create sample Data ,amount 100 data
x_data = np.float32(np.random.rand(2,100)) #random input
y_data = np.dot([0.1,0.2],x_data) + 0.3

#construct linear model
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1,2],-1.0,1.0)) #like matrix[[ 0.54,  0.19 ]]
y = tf.matmul(W,x_data) + b

#minimize the variance(方差)
loss = tf.reduce_mean(tf.square(y-y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#initial all variable
init = tf.initialize_all_variables()

#start graph
sess = tf.Session()
sess.run(init)

#fit panel
for step in range(0,201):
    sess.run(train)
    if step%20 ==0:
        print(step,sess.run(W),sess.run(b))

#destroy resource
sess.close()