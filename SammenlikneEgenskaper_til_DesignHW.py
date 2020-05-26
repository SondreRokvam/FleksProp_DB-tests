"""Comparing Illustrations of deformation behaviour for HW propeller
@author: Sondre feb-may.2020"""

from PlottingClass import plottts
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#Declare Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\HW' 

#Hente folder directories
Inp_folders = plottts.FindInPFolders(Source)

#Plotting starte

KPItitles = ['Bending', 'Twisting', 'BendTwist, BT - (Twist per Bend)','Camber','Camber per Bend' ]
pli= ['\u0394 Deflection of center','\u0394 Alpha of coordline','\u0394 Alpha per deflection',
        '\u0394 Camber','\u0394 Camber per deflection']

a = [([0.3,1]   , [-5, 150]),
     ([0.3,1]   , [-4, 6]),
     ([0.3,1]   , [-0.5, 0.5]),
     ([0.3,1]   , [-0.01, 0.5]),
     ([0.3,1]   , [-0, 0.07])]

#Flow - Flags
ALL = 1

if ALL:
     a = [([0.3,1]   , [-5, 140]),
          ([0.3,1]   , [-5, 9]),
          ([0.3,1]   , [-1.5, 1.5]),
          ([0.3,1]   , [-0.01, 0.6]),
          ([0.3,1]   , [-0, 0.007])]


plottts.ScriptForSimuleringsSammenligningMasse(Source,Inp_folders,ALL,a)