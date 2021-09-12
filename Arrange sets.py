# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 12:03:48 2021
@author: Sondre
"""
from abaqus import *
from abaqus import getInput
from abaqus import getInputs
from abaqusConstants import *
import __main__
import time
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import numpy as np
modelName='NACA0009-AnisotropicShell'
intanceName='Shell-1'
datum_label=52
a = mdb.models[modelName].rootAssembly
a.Set(edges=a.instances[intanceName].edges, name='New_Edges')
a.SetByBoolean(name='Radlines', sets = (a.sets['New_Edges'],a.sets['Original_Edges']), operation=DIFFERENCE)
tol=0.01
for name, numb in zip(Measurementes,range(-40,-105,-5)):
     bob= a.sets['Radlines'].edges.getBoundingBox(-10.0,float(numb)-tol,-10.0,10.0,float(numb)+tol,10.0)
     a.Set(edges=bob, name=name)