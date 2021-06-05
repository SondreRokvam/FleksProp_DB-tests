"""Comparing Illustrations of deformation behaviour for AZP propeller
@author: Sondre feb-may.2020"""

from PlottingClass import plottts
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#Declare Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp_Particular' 
 

#Source = 'D:\\PhD\\Simuleringer\\Mecanical aspects\\Periodic Force Variations'
     
#Hente folder directories
Inp_folders = plottts.FindInPFolders(Source)

#Plotting starte



a = [([0.3,1]   , [-5, 65]),
    ([0.3,1]   , [-3, 0.5]),
    ([0.3,1]   , [-0.075, 0]),
    ([0.3,1]   , [-1/4, 1/2]),
    ([0.3,1]   , [-.5, .5])]

#Flow - Flags
ALL = 0


plottts.ScriptForSimuleringsSammenligningMasse(Source,Inp_folders,ALL,a)
