# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 02:45:10 2021

@author: Sondre
"""
import csv
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

     
with open('C:/Users/Sondre/Desktop/20deg_r7_r9/dic-04-055-07-085.csv') as csv_file:
     spamreader = csv.reader(csv_file,delimiter =";")
     spamreader = np.array(list(spamreader))
     for i in range(0,len(spamreader)):
          spamreader[i]=np.array(spamreader[i])
     spamreader = np.array(spamreader)
     print(len(spamreader))
     Bilde0=spamreader[0:204]
     Bilde0=np.array(Bilde0[3:-1])
     
     Bilde1=spamreader[204:408]
     Bilde1=np.array(Bilde1[3:-1])
     Bilde2=spamreader[408:612]
     Bilde2=np.array(Bilde2[3:-1])
     Bilde3=spamreader[612:]
     Bilde3=np.array(Bilde3[3:-1])
     
     Bilder=np.array([Bilde0,Bilde1,Bilde2,Bilde3])
     Bilder=np.array([Bilde3])
     
     
     
     for a in range(0,len(Bilder)):
          for b in range(0, len(Bilder[0])):
               for c in range(0, len(Bilder[0][0])):
#                    print(len(Bilder),len(Bilder[0]),len(Bilder[0][0]))
#                    print(Bilder[a][b][c])
#                    print('\nHer : ',Bilder[a][b][c])
                    if Bilder[a][b][c]=="":
                         Bilder[a][b][c]=None
#                         print('np.nan')
                    else:
                         Bilder[a][b][c]=float(Bilder[a][b][c])
#                         print(Bilder[a][b][c])
                    
     for a in range(0,len(Bilder)):
          WorkingData=[]
          dispData=[]
          distData=[]
          for b in range(0, len(Bilder[0])):
               a = np.array(Bilder[0][b])[1:]
               Rad04=a[0:6]
               Rad055=a[6:12]
               Rad07=a[12:18]
               Rad085=a[18:24]
               WorkingData.append([Rad04,Rad055,Rad07,Rad085])
          #Fetching displacements
          DR04=[]
          DR055=[]
          DR07=[]
          DR085=[]
          DRs=[DR04,DR055,DR07,DR085]
          for WD in WorkingData:
               LineDat=[]
               for line in range(0,len(WD)):
#                    print('bob',line[0])
                    if not WD[line][0]=='None':
#                         print('bob',line[0])
                         DRs[line].append(np.round((float(WD[line][3])**2+float(WD[line][4])**2+float(WD[line][5])**2)**0.5,3))
#                         except:
#                              pass
#          print(dispData)
          R04=[]
          R055=[]
          R07=[]
          R085=[]
          Rs=[R04,R055,R07,R085]
          rrs=[]
          for WD in WorkingData:
               for line in range(0,len(WD)):
                    print('bib',WD[line][0])
                    if not WD[line][0]=='None':
                         print('bib',WD[line][0])
                         Rs[line].append(np.array([float(WD[line][0]),float(WD[line][1]),float(WD[line][2])]))

#          print(Rs[0])
          for Rrr in Rs:#For hver radlinje i bilde
               LastG=Rrr[0]
#               print(LastG)
               Distline=[]
               for dott in Rrr: #For hverdot i radlinje
                    if not dott[0]=='None':
                         Distline.append(((dott[0]-LastG[0])**2+
                                          (dott[1]-LastG[1])**2+
                                          (dott[2]-LastG[2])**2)**0.5)
                         LastG=dott
                    
#               print('a',Distline)
               
               
               cumsum2=pd.Series(list(Distline))
#               print('bob',np.array(cumsum2))
               cumsum2 =cumsum2.cumsum(axis=None, skipna=True)
               rrs.append(np.array(cumsum2))
            
          print(len(DRs[3]),len(rrs[3]))
          for r in range(0,len(rrs)):
               plt.plot(np.array(rrs[r]),np.array(DRs[r]),'x:', linewidth=4)
#"""  
#FEA
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
#          print('Here:',dat)
          if dat=="":
#               print('No dat')
               dat=np.nan
               dara.append(np.nan)
          else:     
               dara.append(float(dat))
     darra.append(dara)     
#print(darra)
darra=np.array(darra)
#print(darra[:,0:2])

#print ('wo',np.mean([list(darra[:,1])-[np.nan]]))
aa=plt.plot(darra[:,0],darra[:,1],'-', label='FEA - R = 0.4', linewidth=4)
ab=plt.plot(darra[:,2],darra[:,3],'-', label='FEA - R = 0.55', linewidth=4)
ac=plt.plot(darra[:,4],darra[:,5],'-', label='FEA - R = 0.7', linewidth=4)
ad=plt.plot(darra[:,6],darra[:,7],'-', label='FEA - R = 0.85', linewidth=4)
#"""
a=[]
for v in DRs[3]:
     if v>0.0:
          print(float(v), type(float(v)))
          a.append(float(v))
print(np.mean(a))
plt.xticks(np.arange(0,575,25),fontsize=20)
plt.yticks(np.arange(0,14,.5),fontsize=20)
plt.grid(linestyle = '--', linewidth = 0.5)
plt.legend(['DIC  r = 0.4',
            'DIC  r = 0.55',
            'DIC  r = 0.7',
            'DIC  r = 0.85',
            
            'FEA  r = 0.4',
            'FEA  r = 0.55',
            'FEA  r = 0.7',
            'FEA  r = 0.85'],fontsize=18)

plt.xlabel("Radius path length [mm]",fontsize=28)
plt.ylabel("Displacement [mm]",fontsize=26)
plt.xlim(0,530)
#plt.ylim(0.5,2)
#plt.ylim(2.5,4.5)
#plt.ylim(6,9)
#plt.ylim(10,13.5)
plt.show

