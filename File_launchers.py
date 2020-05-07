
from abaqus import *
from abaqusConstants import *
import __main__

import os

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


Desk='C:/Users/Sondre/Desktop/'
os.chdir(Desk+'MassTests/Mass_HW_7degs')
#os.chdir(Desk+'Single_Simulations/Mecanical aspects')
current=os.getcwd()
Bat_file = [b for b in os.listdir(current) if b.endswith('.bat') ]
for f in Bat_file:
     try:
        os.remove(os.path.join(current, f))
     except:
        pass
#Mass quantify - Parento tests
#Os walk to get files, roots and
BAtfiles=[]
for root, dirs, files in os.walk(current, topdown=False):
     for name in dirs:
          name = os.path.join(root, name)
          inplist= [a for a in os.listdir(name) if a.endswith('.inp')]
          if len(inplist)>0:
               BAtfiles.append([name,])
# -*- coding: mbcs -*-
# Do not delete the following import lines



a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.ModelFromInputFile(name='HW_AllOver_Seven+_Angle_-10_R_0_',
    inputFileName='C:/Users/Sondre/Desktop/MassTests/Mass_HW_7degs/AllOver/Seven+/-10.0/HW_AllOver_Seven+_Angle_-10_R_0_.inp')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
del mdb.models['Model-1']
a = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.ModelFromInputFile(name='HW_AllOver_Seven+_Angle_-10_R_0_01',
    inputFileName='C:/Users/Sondre/Desktop/MassTests/Mass_HW_7degs/AllOver/Seven+/-10.0/HW_AllOver_Seven+_Angle_-10_R_0_01.inp')
a = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_01'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_01'].parts['HW']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_01'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['HW_AllOver_Seven+_Angle_-10_R_0_'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.Job(name='HW_AllOver_+7_M-10_R_0',
    model='HW_AllOver_Seven+_Angle_-10_R_0_', description='',
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
    numGPUs=0)
mdb.jobs['HW_AllOver_+7_M-10_R_0'].writeInput(consistencyChecking=OFF)



