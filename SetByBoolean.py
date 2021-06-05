mdb.models['HW_23062020'].parts['FOAM-1'].sets
a=mdb.models['HW_23062020'].parts['FOAM-1'].sets['SET-1']
b=mdb.models['HW_23062020'].parts['FOAM-1'].sets['leadingBrim']
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
from abaqus import *
from abaqus import getInput
from abaqus import getInputs
from abaqusConstants import *
mdb.models['HW_23062020'].parts['FOAM-1'].SetByBoolean(name='Set-s-s', sets = (a,b), operation=DIFFERENCE)
mdb.models['HW_23062020'].parts['FOAM-1'].se	ts['Set-s-s']
