from abaqus import *
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
#import easygui

Mdb()
pressure_field_path = "C:\Users\Sondre\Dropbox\!PhD!\Propeller Design and Production\Azp65C\Trykkfordelinger\Pres.25kn_561rpm__Aba.txt"

file_path = 'C:\Users\Sondre\Dropbox\!PhD!\Propeller Design and Production\Azp65C\Propeller_3D-files .prt .stp .iges\Azp65C-PB_no_Fillet_Shell.stp'

#part_name = str(input('Write part name here: '))
part_name = 'AzpC65'

file = part_name + '-1'
model = mdb.models['Model-1']

#r = float(input('Propeller radius(mm): '))
r = 650

tol = 0.01

# r_name = []
# r_val = []
# while True:
#     r_temp = input('Radius to inspect(0.5, 0.6,...etc). Submit '' to advance: ')
#     if r_temp == '':
#         break
#     r_temp = float(r_temp)
#     r_val.append(r_temp)
#     r_name.append('R'+str(r_temp)[2:])

r_val = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
r_name = []
set_name = []
for i in range(len(r_val)):
    r_name.append('R_'+str(r_val[i])[2:])
    set_name.append('PROFILE-'+r_name[i])
#print(r_name)
npz_name = 'Parameters_for_plots1.npz'
np.savez(npz_name,r_val=r_val, set_name=set_name )
a = np.load(npz_name)
print (a['set_name'])
#------------Import--------------------

step = mdb.openStep(
    file_path,
    scaleFromFile=OFF)
model.PartFromGeometryFile(
    name=part_name, geometryFile=step, combine=True,
    retainBoundary=True, mergeSolidRegions=True, dimensionality=THREE_D,
    type=DEFORMABLE_BODY)
p = model.parts[part_name]
session.viewports['Viewport: 1'].setValues(displayedObject=p)


#-------------Make instance-------------
a = model.rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name=file, part=p, dependent=OFF)

#------------------Particion Settings--------------------------------
a = model.rootAssembly

a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=200.0)
d1 = a.datums
e1 = a.instances[file].edges
a.Set(name='prePartiti', edges=e1)
t = a.MakeSketchTransform(sketchPlane=d1[4], sketchUpEdge=e1[2],
                          sketchPlaneSide=SIDE1, origin=(200.0, 0.0, 0.0))
s = model.ConstrainedSketch(name='__profile__',
                            sheetSize=1926.91, gridSpacing=48.17, transform=t)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
a = model.rootAssembly
a.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)


#--------------Draw Radius circles----------------------------
for i in range(len(r_val)):
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(r*r_val[i], 0.0))


#--------------------Partition---------------------------------
a = model.rootAssembly
f1 = a.instances[file].faces
d21 = a.datums
e11 = a.instances[file].edges
a.PartitionFaceBySketchThruAll(sketchPlane=d21[4], sketchUpEdge=e11[2],
                               faces=f1, sketchPlaneSide=SIDE1, sketch=s)
s.unsetPrimaryObject()
del model.sketches['__profile__']


e1 = a.instances[file].edges
a.Set(name='postPartiti', edges=e1)
a.SetByBoolean(name='r_edges', sets=(a.sets['postPartiti'], a.sets['prePartiti']),
               operation=DIFFERENCE)
e1 = a.instances[file].edges

#---------------------MESH----------------------------
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
a = model.rootAssembly
f1 = a.instances[file].faces
a.setMeshControls(regions=f1, elemShape=TRI) #Choose between: QUAD, QUAD_DOMINATED, TRI
partInstances = (a.instances[file], )
a.seedPartInstance(regions=partInstances, size=15.0, deviationFactor=0.1,
                   minSizeFactor=0.1)
a = model.rootAssembly
partInstances = (a.instances[file], )
a.generateMesh(regions=partInstances)


#---------------------NodeSets----------------------------------

for i in range(len(r_name)):
    edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), r * r_val[i] + tol)
    a.Set(edges=edges, name=r_name[i]+'+tol')
    edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), r * r_val[i] - tol)
    a.Set(edges=edges, name=r_name[i] + '-tol')
    a.SetByBoolean(name='Area', sets=(a.sets[r_name[i]+'+tol'], a.sets[r_name[i] + '-tol']), operation=DIFFERENCE)
    a.SetByBoolean(name=set_name[i], sets=(a.sets['Area'], a.sets['r_edges']), operation=INTERSECTION)
    del a.sets['Area']
    del a.sets[r_name[i] + '+tol']
    del a.sets[r_name[i] + '-tol']
    n_labels = []
    #for j in range(len(a.sets[set_name[i]].nodes)):
        #node = a.sets[set_name[i]].nodes[j].label
        #n_labels.append(node)
    #n_labels = np.array(n_labels)
    #a.SetFromNodeLabels(name='nodes_' + r_name[i], nodeLabels=((file, n_labels),),)

#-------------------Step---------------------------------------
model.StaticStep(name='Step-1', previous='Initial', initialInc=0.001, maxInc=0.1)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
                                                        predefinedFields=ON, connectors=ON,
                                                        adaptiveMeshConstraints=OFF)

#-------------------Load-----------------------------------------
readfile = open(pressure_field_path,"r")
reading = readfile.read()
pressuredist = reading.split('\n')
len_s = len(pressuredist)


for i in range(len_s):
    t = pressuredist[i].split('\t')
    for j in range(len(t)):
        t[j] = float(t[j])
    pressuredist[i] = t
    #pressuredist[len_s-1] = [0,0,0,0]

model.MappedField(name='AnalyticalField-1', description='',
                                  regionType=POINT, partLevelData=False, localCsys=None,
                                  pointDataFormat=XYZ, fieldDataType=SCALAR,
                                  xyzPointData=pressuredist)
a = model.rootAssembly
s1 = a.instances[file].faces
#side1Faces1 = s1.getSequenceFromMask(mask=('[#fffff ]',), )
region = a.Surface(side1Faces=s1, name='Surf-1')
model.Pressure(name='Load-1', createStepName='Step-1',
                               region=region, distributionType=FIELD, field='AnalyticalField-1',
                               magnitude=1.0, amplitude=UNSET)


#-----------------------BC----------------------------
a = model.rootAssembly
e1 = a.instances[file].edges
edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), r * 0.408) #This must be changed if using other propeller than AzP65C
a.Set(edges=edges, name='BC_edges_extra')
edges = e1.getByBoundingCylinder((-254, -262, -20), (-254, -262, -7), 15)
a.Set(edges=edges, name='BC_edges_single')
region = a.SetByBoolean(name='BC-Edges', sets=(a.sets['BC_edges_extra'], a.sets['BC_edges_single']), operation=DIFFERENCE)
#edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), r * 0.41) #This must be changed if using other propeller than AzP65C
#region = a.Set(edges=edges, name='BC-edges')
model.DisplacementBC(name='BC-1', createStepName='Initial',
                                     region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
                                     amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',
                                     localCsys=None)