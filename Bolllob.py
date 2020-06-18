
from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
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
#Reset Abaqus, find Githhub
Mdb()
step = mdb.openStep(
    'D:/PhD/Propeller Design and Production/LargeScale/3_Singles_Comparing_tests/Azp65C-PB-Shell-0.5mm.stp',
    scaleFromFile=OFF)
mdb.models['Model-1'].PartFromGeometryFile(name='Azp65C-PB-Shell-05mm',
                                           geometryFile=step, combine=False, dimensionality=THREE_D,
                                           type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Azp65C-PB-Shell-05mm']
p.seedPart(size=0.4, deviationFactor=0.2, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Azp65C-PB-Shell-05mm']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]',), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Azp65C-PB-Shell-05mm']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]',), )
pickedRegions = (cells,)
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
                                                   elemType3))
p = mdb.models['Model-1'].parts['Azp65C-PB-Shell-05mm']
p.seedPart(size=35.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Azp65C-PB-Shell-05mm']
p.generateMesh()