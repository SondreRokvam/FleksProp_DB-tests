# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Partition():
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

    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    #mdb.models['Model-1'].sketches['__profile__']

    partitions = [250,300,350,400,450]

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(-26.25, 0.0), point2=(18.75, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.ConstructionLine(point1=(0.0, 17.5), point2=(0.0, -10.0))
    s.VerticalConstraint(entity=g[3], addUndoState=False)

    s.FixedConstraint(entity=g[3])
    s.FixedConstraint(entity=g[2])

    for line in range(len(partitions)):
        s.Line(point1=(-15.0, 15.0), point2=(13.75, 15.0))
        s.HorizontalConstraint(entity=g[line+4], addUndoState=False)
        s.ObliqueDimension(vertex1=v[2*line], vertex2=v[2*line+1], textPoint=(-4.73760223388672,
            9.81308364868164), value=1000)
        s.DistanceDimension(entity1=g[line+4], entity2=g[2], textPoint=(29.0790710449219,
            5.39719390869141), value=partitions[line])
        s.DistanceDimension(entity1=v[line*2+1], entity2=g[3], textPoint=(22.0712547302246,
            49.0563049316406), value=500)

    mdb.models['Model-1'].sketches.changeKey(fromName='__profile__',
        toName='Partition')
    s.unsetPrimaryObject()
    #del mdb.models['Model-1'].sketches['__profile__']

    p = mdb.models['Model-1'].parts['HydroWing_for_DB']
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=100.0)
    p = mdb.models['Model-1'].parts['HydroWing_for_DB']
    f, e, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=e[39],
        sketchPlaneSide=SIDE1, origin=(0, 0, 0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=1932.38, gridSpacing=48.3, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['HydroWing_for_DB']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.sketchOptions.setValues(gridOrigin=(0.0,0.0))
    s1.retrieveSketch(sketch=mdb.models['Model-1'].sketches['Partition'])

    p = mdb.models['Model-1'].parts['HydroWing_for_DB']
    f = p.faces
    pickedFaces = f
    f, e, d1 = p.faces, p.edges, p.datums
    p.PartitionFaceBySketchThruAll(sketchPlane=d1[2], sketchUpEdge=e[39],
        faces=pickedFaces, sketchPlaneSide=SIDE2, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    for i in range(0,len(partitions)):
        p.Set(edges=p.edges.getByBoundingBox(-100,-1000,partitions[i]-1,100,1000,partitions[i]+1), name='Radius'+str(partitions[i]))
Partition()