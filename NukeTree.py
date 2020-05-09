# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:42:26 2020

@author: Sondre
"""
import os

def nukemappe(loca, avoid1): 
     filelist = [f for f in os.listdir(loca) if (not avoid1 in f )]  # if not f.endswith('.inp')]
     for f in filelist:
         try:
             os.remove(os.path.join(loca, f))
         except:
             pass
        
#nukeloc= 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp'
#nukeloc= 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\HW'
affectedFolds=[['D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp']]
for root, dirs, files in os.walk(nukeloc, topdown=False):
     for name in dirs:
          name = os.path.join(root, name)
          affectedFolds.append(name.split('\n'))
          

for fold in affectedFolds:
     print('FOLDA',fold)
     nukemappe(fold[0],'.inp')