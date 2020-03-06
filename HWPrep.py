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
#import easygui

Mdb()
#--------------------File paths--------------------
#file_path = 'C:\Users\Eivind\Documents\NTNU\FleksProp\Models\Azp65C-PB_no_Fillet_Shell.stp'
file_path = 'C:/Users/Jon/OneDrive/FleksProp/HW_2020_02/HydroWing.stp'
pressure_field_path = "C:\Users\Jon\OneDrive\FleksProp\Scripts\load.txt"



#--------------------Initial Variable Names and Settings--------------------
reply = getWarningReply(message='Press YES for sheet body \nPress NO for solid body',
                        buttons=(YES, NO))
if reply == YES:
    part_type = 0
elif reply == NO:
    part_type = 1

#part_name = str(getInput('Write part name here: '))
part_name = 'HW'
file = part_name + '-1'
model = mdb.models['Model-1']
tol = 0.01
r = float(getInput('Enter the propeller radius(mm):'))
#r = 650

#--------------------Prompt user for which radii to inspect--------------------
fields = (('R= ','0.5'),('R= ','0.6'),('R= ','0.7'),('R= ','0.8'),('R= ','0.9'),('R= ',''),('R= ',''),('R= ',''),('R= ',''),('R= ',''))
r_input = getInputs(fields=fields,
                    label='Enter percentages of the propeller radius(0.5, 0.6,...etc.):',
                    dialogTitle='Inspected radii',)

#filter out empty and duplicate inputs
r_val = []
for i in range(len(r_input)):
    duplicate = 0
    if r_input[i] !='':
        r_val.append(float(r_input[i]))
        for j in range(len(r_val)-1):
            if r_val[-1] == r_val[j]:
                duplicate = 1
    if duplicate == 1:
        r_val.remove(r_val[-1])
r_val.sort()

#r_val = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95] #If all radii are predefined, uncomment this line, add the percentages to the list and comment out the previous 15 lines


#--------------------Save list of radii and set names to C:\temp--------------------
r_name = [] # Used throughout the script to name sets
set_name = []
for i in range(len(r_val)):
    r_name.append('R_'+str(r_val[i])[2:])
    set_name.append('PROFILE-'+r_name[i])
npz_name = 'parameters_for_plot.npz'
np.savez(npz_name,
         r_val=r_val,
         set_name=set_name )
npzfile = np.load(npz_name)


#--------------------Import--------------------
step = mdb.openStep(file_path,
                    scaleFromFile=OFF)
model.PartFromGeometryFile(name=part_name,
                           geometryFile=step,
                           combine=True,
                           retainBoundary=True,
                           mergeSolidRegions=True,
                           dimensionality=THREE_D,
                           type=DEFORMABLE_BODY)
p = model.parts[part_name]
session.viewports['Viewport: 1'].setValues(displayedObject=p)


 #--------------------Material--------------------
# model.Material(name='CF-UD')
# model.materials['CF-UD'].Elastic(type=ENGINEERING_CONSTANTS,
#                                  table=((140000.0, 10000.0, 10000.0,      # E1, E2, E3
#                                          0.28, 0.28, 0.5,                 # v12, v13, v23
#                                          3300.0, 3300.0, 3500.0),))       # G12, G13, G23


#--------------------Make instance--------------------
a = model.rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name=file,
           part=p,
           dependent=OFF)


#--------------------Partition Settings--------------------
a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,
                             offset=200.0)
d1 = a.datums
e1 = a.instances[file].edges
a.Set(name='prePartiti',
      edges=e1)
t = a.MakeSketchTransform(sketchPlane=d1[4],
                          sketchUpEdge=d1[1].axis3,
                          sketchPlaneSide=SIDE1,
                          origin=(200.0, 0.0, 0.0))
s = model.ConstrainedSketch(name='__profile__',
                            sheetSize=1926.91,
                            gridSpacing=48.17,
                            transform=t)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
a = model.rootAssembly
a.projectReferencesOntoSketch(sketch=s,
                              filter=COPLANAR_EDGES)


#--------------------Draw Radius circles--------------------

s.ConstructionLine(point1=(-26.25, 0.0), point2=(18.75, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.ConstructionLine(point1=(0.0, 17.5), point2=(0.0, -10.0))
s.VerticalConstraint(entity=g[3], addUndoState=False)

s.FixedConstraint(entity=g[3])
s.FixedConstraint(entity=g[2])

for line in range(len(r_val)):
    s.Line(point1=(-15.0, 15.0), point2=(13.75, 15.0))
    s.HorizontalConstraint(entity=g[line+4], addUndoState=False)
    s.ObliqueDimension(vertex1=v[2*line], vertex2=v[2*line+1], textPoint=(-4.73760223388672,
                                                                          9.81308364868164), value=1000)
    s.DistanceDimension(entity1=g[line+4], entity2=g[2], textPoint=(29.0790710449219,
                                                                    5.39719390869141), value=r_val[line]*r)
    s.DistanceDimension(entity1=v[2*line], entity2=g[3], textPoint=(22.0712547302246,
                                                                      49.0563049316406), value=500)

#--------------------Make Partition--------------------
a = model.rootAssembly
f1 = a.instances[file].faces
d21 = a.datums
e11 = a.instances[file].edges
a.PartitionFaceBySketchThruAll(sketchPlane=d21[4],
                               sketchUpEdge=d21[1].axis3,
                               faces=f1,
                               sketchPlaneSide=SIDE1,
                               sketch=s)
s.unsetPrimaryObject()
del model.sketches['__profile__']
e1 = a.instances[file].edges
a.Set(name='postPartiti',
      edges=e1)
a.SetByBoolean(name='r_edges',
               sets=(a.sets['postPartiti'],
                     a.sets['prePartiti']),
               operation=DIFFERENCE)
e1 = a.instances[file].edges


#--------------------MESH--------------------
# Sheet mesh
if reply == YES:
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
    a = model.rootAssembly
    f1 = a.instances[file].faces
    a.setMeshControls(regions=f1,
                      elemShape=TRI)  # Choose between: QUAD, QUAD_DOMINATED, TRI
    partInstances = (a.instances[file],)
    a.seedPartInstance(regions=partInstances,
                       size=10.0,
                       deviationFactor=0.1,
                       minSizeFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=S8R,
                              elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=STRI65,
                              elemLibrary=STANDARD)
    pickedRegions = (f1,)
    a.setElementType(regions=pickedRegions,
                     elemTypes=(elemType1, elemType2))
    partInstances = (a.instances[file],)
    a.generateMesh(regions=partInstances)

# Solid mesh
if reply == NO:
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
    a = model.rootAssembly
    partInstances =(a.instances[file], )
    a.seedPartInstance(regions=partInstances,
                       size=10.0,
                       deviationFactor=0.1,
                       minSizeFactor=0.1)
    c1 = a.instances[file].cells
    a.setMeshControls(regions=c1,
                      elemShape=TET,
                      technique=FREE)
    elemType1 = mesh.ElemType(elemCode=C3D20R,
                              elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15,
                              elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10,
                              elemLibrary=STANDARD)
    pickedRegions =(c1, )
    a.setElementType(regions=pickedRegions,
                     elemTypes=(elemType1, elemType2, elemType3))
    a.generateMesh(regions=partInstances)


#--------------------NodeSets--------------------

for i in range(len(r_name)):
    edges = e1.getByBoundingBox(-1000, -1000, r_val[i]*r-tol, 1000, 1000, r_val[i]*r+tol)
    a.Set(edges=edges,
          name='Area')
    a.SetByBoolean(name=set_name[i],
                   sets=(a.sets['Area'], a.sets['r_edges']),
                   operation=INTERSECTION)
    del a.sets['Area']
  
    n_labels = []
    for j in range(len(a.sets[set_name[i]].nodes)):
        node = a.sets[set_name[i]].nodes[j].label
        n_labels.append(node)
    n_labels = np.array(n_labels)
    a.SetFromNodeLabels(name='nodes_' + r_name[i],
                        nodeLabels=((file, n_labels),),)


#--------------------Step--------------------
model.StaticStep(name='Step-1',
                 previous='Initial',
                 initialInc=0.001,
                 maxInc=0.1)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON,
                                                           bcs=ON,
                                                           predefinedFields=ON,
                                                           connectors=ON,
                                                           adaptiveMeshConstraints=OFF)

#--------------------Load--------------------

readfile = open(pressure_field_path,"r")
reading = readfile.read()
pressuredist = reading.split('\n')
len_s = len(pressuredist)

for i in range(len_s):
    t = pressuredist[i].split('\t')
    for j in range(len(t)):
        t[j] = float(t[j])
    pressuredist[i] = t
model.MappedField(name='AnalyticalField-1',
                  description='',
                  regionType=POINT,
                  partLevelData=False,
                  localCsys=None,
                  pointDataFormat=XYZ,
                  fieldDataType=SCALAR,
                  xyzPointData=pressuredist)
a = model.rootAssembly
s1 = a.instances[file].faces
region = a.Surface(side1Faces=s1,
                   name='Surf-1')
model.Pressure(name='Load-1',
               createStepName='Step-1',
               region=region,
               distributionType=FIELD,
               field='AnalyticalField-1',
               magnitude=1.0,
               amplitude=UNSET)


#--------------------BC--------------------
a = model.rootAssembly
d1 = a.datums
a.AttachmentPoints(name='Attachment Points-1', points=(d1[1].origin, ),
    setName='Attachment Points-1-Set-1')
v1 = a.vertices
verts1 = v1.getByBoundingBox(-1,-1,-1,1,1,1)
region1=a.Set(vertices=verts1, name='m_Set-14')
s1 = a.instances[file].faces
side1Faces1 = s1.getByBoundingBox(-100, -150, 98, 100, 100, 102)
region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-1')
mdb.models['Model-1'].Coupling(name='Constraint-1', controlPoint=region1,
    surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
    localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

model.DisplacementBC(name='BC-1', createStepName='Initial',
                     region=region1,
                     u1=0.0, u2=0.0, u3=0.0, ur1=0, ur2=0, ur3=0,
                     amplitude=UNSET,
                     fixed=OFF,
                     distributionType=UNIFORM,
                     fieldName='',
                     localCsys=None)

session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].setValues(displayedObject=a)
