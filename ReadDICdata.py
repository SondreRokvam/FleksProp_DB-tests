# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 15:06:13 2021

DIC  treatment

@author: Sondre
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as  py


def getRef(line0):
     bob= line0.split(';')
     #print (bob[1:4])
     #print (bob[8:11])
     #print (bob[19:22])
     Ref1=bob[1:4]
     Ref2=bob[7:10]
     Ref3=bob[13:16]
     Ref4=bob[19:22]
     return [Ref1,Ref2,Ref3,Ref4]

def getValues(aa):
     a=[]
     for line in aa:
          bob=line[0].split(';')
          a.append(bob)
     a=np.array(a)
     return a

def sortValues(b):
     L1,L2,L3,L4=[],[],[],[]
     for lin in Xss:  
          L1.append(lin[1:7])
          L2.append(lin[7:13])
          L3.append(lin[13:19])
          L4.append(lin[19:25])
     b=np.array([L1,L2,L3,L4])
     return b


def dist_to_Ref(d,org):
     Li=[]
     for nr in range(0,len(d)):
#          print (len(d[nr]))
          La=[]
          
          for subs in range(0,len(d[nr])):
#               print(d[nr][subs][0:3])
#               print(org[nr])
#              Skrive ned avstanden fra origin i hver retning
               dis=[]
               for ent in range(0,3):
                    coordinat=d[nr][subs][0:3][ent]
                    if not coordinat=="":
#                         print(d[nr][subs][0:3][ent],org[nr][ent])
                         if subs==0:
                              distan=float(d[nr][subs][0:3][ent])-float(org[nr][ent])
                         else:
                              if d[nr][subs-1][0:3][ent]==0:
                                   distan=None
                              else:
                                   distan=float(d[nr][subs][0:3][ent])-float(d[nr][subs-1][0:3][ent])
                    else:
                         distan=None
                    dis.append(distan)
#              calc distance
               if not (dis[0]==0) :
                    La.append((float(dis[0])**2+float(dis[1])**2+float(dis[2])**2)**0.5)
               else:
                    La.append(None)
          La= FromSteps_to_total(La)
          Li.append(La)
     return Li
     
def FromSteps_to_total(Lo):
     Lp=[]
     Lp.append(0.0)
     for i in range(1,len(Lo)):
          try:
               Lp.append(Lp[i-1]+Lo[i])
          except:
               Lp.append(None)          
     return Lp
          

def gettoal_def(c):
#     print(len(c))
     Rrs=[]
     for tit in c:
          U=tit[:,3]
          V=tit[:,4]
          W=tit[:,5]
          r=np.zeros(200)
          print(tit)
          for ui in range(0,len(U)):
#               print (ui,r[ui])
#               print (len(U[ui]),len(V[ui]),len(W[ui]))
               if not len(U[ui])==0:
                    r[ui]=(float(U[ui])**2+float(V[ui])**2+float(W[ui])**2)**0.5
               else:
                    print(np.where(c==tit),ui)
                    r[ui]=None
          Rrs.append(r)
     return np.array(Rrs)

"""Meta"""
#Hente verdier fra CSV med fire linjer
df = pd.read_csv (r'C:\Users\Sondre\Desktop\20deg_r7_Test3\0_0-5_0.6_0.85.csv', header=[2])
#Hente tail ref data
Ref1234 = getRef(df.values[0][0])
#print (Ref1234)

#Hente data
Xss=getValues(df.values)
#Sortere data i #[lines[X,Y,Z,U,V,W] format]
Xsss=sortValues(Xss)
print (Xsss[0][:])
#Finn total deformasjon
Defs, errors= gettoal_def(Xsss),1
#Finn distance from ref for plotting
dist= dist_to_Ref(Xsss,Ref1234)
for j in range (0,4):
     py.plot(dist[j],Defs[j])
