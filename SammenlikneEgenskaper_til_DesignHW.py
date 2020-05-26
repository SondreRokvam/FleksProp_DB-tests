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


a = [([0.3,1]   , [-5, 140]),
     ([0.3,1]   , [-4, 6]),
     ([0.3,1]   , [-0.5, 0.5]),
     ([0.3,1]   , [-0.04, 0.01]),
     ([0.3,1]   , [-0.5, 0.5])]

#Flow - Flags
ALL = 1


plottts.ScriptForSimuleringsSammenligningMasse(Source,Inp_folders,ALL,a)