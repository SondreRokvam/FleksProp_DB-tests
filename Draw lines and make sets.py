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
modelName='NACA0009_Alu-Shell-and-Solid'
intanceName='Shell-1'
datum_label=9
refpoiunt=4
a = mdb.models[modelName].rootAssembly
a.Set(edges=a.instances[intanceName].edges, name='Original_Edges')

Measurementes = ['PROFILE-R_4','PROFILE-R_45',
                 'PROFILE-R_5','PROFILE-R_55',
                 'PROFILE-R_6','PROFILE-R_65',
                 'PROFILE-R_7','PROFILE-R_75',
                 'PROFILE-R_8','PROFILE-R_85',
                 'PROFILE-R_9','PROFILE-R_95',
                 'PROFILE-R1',]

s1 = mdb.models[modelName].ConstrainedSketch(
          name='__profile__', sheetSize=2.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
for line in range(40,100,5):
     s1.Line(point1=(float(line)/100.0, -1.0), point2=(float(line)/100.0, 1.0))
mdb.models[modelName].sketches.changeKey(
          fromName='__profile__', toName='PartitionSketch')
s1.unsetPrimaryObject()    
a = mdb.models[modelName].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[refpoiunt], )
for name in Measurementes:
     a.Set(referencePoints=refPoints1, name=name)
