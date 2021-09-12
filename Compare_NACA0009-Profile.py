# -*- coding: utf-8 -*-
"""
@author: Sondre
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os
from PlottingClass import plottts

#Declare Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\NACA0009' 

#Hente folder directories
Inp_folders = plottts.FindInPFolders(Source)

#Plotting starte

a = [([0.3,1]   , [-0.01, 55]),
    ([0.3,1]   , [-4.5, 0.2]),
    ([0.3,1]   , [-0.15, 0.05]),
    ([0.3,1]   , [-.7, .7]),
    ([0.3,1]   , [-.7, .7])]

#Flow - Flags
ALL = 0


plottts.ScriptForSimuleringsSammenligningMasse(Source,Inp_folders,ALL,a)
