# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 12:37:00 2021

@author: Sondre
"""
import numpy as np
import matplotlib.pyplot as plt
data = list()   #Same hvilken

f = open('C:/Users/Sondre/Desktop/FEA.txt', "r") #r for read, w for write og a for append

tekstFEA = f.read()
f.close()

lines = tekstFEA.split('\n')
darra=[]
for line in lines:
     data= line.split('\t')
     dara=[]
     for dat in data:
          print('Here:',dat)
          if dat=="":
               print('No dat')
               dat=None
               dara.append(None)
          else:     
               dara.append(float(dat))
     darra.append(dara)     
print(darra)
darra=np.array(darra)
print(darra[:,0:2])
plt.plot(darra[:,0],darra[:,1],'--')
plt.plot(darra[:,2],darra[:,3],'--')
plt.plot(darra[:,4],darra[:,5],'--')
plt.plot(darra[:,6],darra[:,7],'--')


#plt.plot(FEx2)

