# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:27:58 2020

@author: Sondre
"""

"""Comparing Illustrations of deformation behaviour for AZP propeller
@author: Sondre feb-may.2020"""

from PlottingClass import plottts
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#Declare Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Mecanical aspects\\Periodic Force Variations'

#Hente folder directories
Inp_folders = plottts.FindInPFolders(Source)

#Plotting starte
KPItitles = ['Bending', 'Twisting', 'BendTwist, BT - (Twist per Bend)','Camber','Camber per Bend' ]
pli= ['\u0394 Deflection of center','\u0394 Alpha of coordline','\u0394 Alpha per deflection',
        '\u0394 Camber','\u0394 Camber per deflection']
#Comparisin plots
a = [([0.3,1]   , [-5, 140]),
     ([0.3,1]   , [-4, 2.5]),
     ([0.3,1]   , [-0.25, 0.3]),
     ([0.3,1]   , [-0.350, 0.5]),
     ([0.3,1]   , [-0.04, 0.07])]
#Forcevariations on isotropic blade
a = [([0.3,1]   , [-0, 5]),
     ([0.3,1]   , [-0, 0.075]),
     ([0.3,1]   , [-0, 0.1]),
     ([0.3,1]   , [-0, 0.0015]),
     ([0.3,1]   , [-0, 0.004])]
#Flow - Flags
ALL = 0

if ALL:
     #All Comparison
     a = [([0.3,1]   , [-5, 140]),
          ([0.3,1]   , [-5, 4]),
          ([0.3,1]   , [-0.4, 0.5]),
          ([0.3,1]   , [-0.50, 0.8]),
          ([0.3,1]   , [-0.07, 0.12])]
     print('All testing')
     fig, axs = plt.subplots(1, 5, figsize=(19, 10))
     fig.suptitle('Sim: '+'All '+ Source.split("\\")[-1]+' simulations', fontsize=16)
    

plottts.ScriptForSimuleringsSammenligningMasse(Source,Inp_folders,ALL,a)