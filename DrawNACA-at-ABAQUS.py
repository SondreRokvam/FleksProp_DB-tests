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
Mdb()
mdb.models.changeKey(fromName='Model-1', toName='NACA0009')
s = mdb.models['NACA0009'].ConstrainedSketch(name='__profile__', 
    sheetSize=1000.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
txt= open('C:/Users/Sondre/Desktop/NACA0009.txt','r')
tekst = txt.read()
#print(tekst)
tekst=tekst.split('\n')
alldata=[]
for line in tekst:
     data=line[2:].split('  ')
#     print data
     alldata.append([[float(data[0])],[float(data[1])]])
print(alldata[dat-1][0])
for dat in range(1,len(alldata)):
     print(alldata[dat][1])
     s.Line(point1=(alldata[dat-1][0][0],alldata[dat-1][1][0]), point2=(alldata[dat][0][0],alldata[dat][1][0]))
p = mdb.models['NACA0009'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
p = mdb.models['NACA0009'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=1.0)
s.unsetPrimaryObject()
p = mdb.models['NACA0009'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['NACA0009'].sketches['__profile__']