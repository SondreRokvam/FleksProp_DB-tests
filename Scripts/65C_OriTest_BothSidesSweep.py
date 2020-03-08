from abaqus import *
from abaqusConstants import *
from odbAccess import *
import sys
import visualization
import xyPlot
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
import math

#Controls
runnyJobb = 1
TheCae= ''
Mdb()
openMdb(pathName=TheCae)
resolution = 1
angels = np.linspace(0,180,resolution)
Joblist=[]
"""Sweep part _ Shell and Section"""

for ori in angels:
    jobbie = "HW_TopFace_"+str(int(ori))
    Joblist.append(jobbie)
    p = mdb.models['Model-1'].parts['HydroWingTopFace']
    region = p.sets['Set-1']
    p = mdb.models['Model-1'].parts['HydroWingTopFace']
    normalAxisRegion = p.surfaces['Surf-1']
    primaryAxisDatum=mdb.models['Model-1'].parts['HydroWingTopFace'].datums[3]
    mdb.models['Model-1'].parts['HydroWingTopFace'].MaterialOrientation(
        region=region, orientationType=DISCRETE, axis=AXIS_3,
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion,
        flipNormalDirection=False, normalAxisDirection=AXIS_3,
        primaryAxisDefinition=DATUM, primaryAxisDatum=primaryAxisDatum,
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False,
        additionalRotationType=ROTATION_ANGLE, additionalRotationField='',
        angle=ori)
    mdb.Job(name=jobbie, model='Model-1')
    if runnyJobb:
        mdb.jobs[jobbie].submit(consistencyChecking=OFF)
        mdb.jobs[jobbie].waitForCompletion()
    del mdb.models['Model-1'].parts['HydroWingTopFace'].materialOrientations[0]
print('Ferdig med Top-analysene')
for jobbo in Joblist:

"""BOTTOM"""


Mdb()
openMdb(pathName='C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/HydroWing/Face-Investigation/HW_BottomFaceTest.cae')
angels = np.linspace(0,180,resolution)
Joblist=[]
for ori in angels:
    jobbie = "HW_BottomFace_" + str(int(ori))
    Joblist.append(jobbie)
    p = mdb.models['Model-1'].parts['HydroWingBottomFace']
    region = p.sets['Set-1']
    p = mdb.models['Model-1'].parts['HydroWingBottomFace']
    normalAxisRegion = p.surfaces['Surf-1']
    primaryAxisDatum = mdb.models['Model-1'].parts['HydroWingBottomFace'].datums[2]
    mdb.models['Model-1'].parts['HydroWingBottomFace'].MaterialOrientation(
        region=region, orientationType=DISCRETE, axis=AXIS_3,
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion,
        flipNormalDirection=False, normalAxisDirection=AXIS_3,
        primaryAxisDefinition=DATUM, primaryAxisDatum=primaryAxisDatum,
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False,
        additionalRotationType=ROTATION_ANGLE, additionalRotationField='',
        angle=ori)
    mdb.Job(name=jobbie, model='Model-1')
    if runnyJobb:
        mdb.jobs[jobbie].submit(consistencyChecking=OFF)
        mdb.jobs[jobbie].waitForCompletion()

    del mdb.models['Model-1'].parts['HydroWingBottomFace'].materialOrientations[0]
print('Ferdig med Bunn-analysene')
for jobbo in Joblist:
    print(jobbo)
    o = session.openOdb(name='C:/temp/'+jobbo+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o)
    session.Path(name='Path_09', type=NODE_LIST, expression=(('HYDROWINGTOPFACE-1',
        (20, '1:19:1', 21, )), ))
    session.Path(name='Path_07', type=NODE_LIST, expression=(('HYDROWINGTOPFACE-1',
        ('22:40:1', 42, )), ))
    xyp = session.XYPlot('XYPlot-1')
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    pth = session.paths['Path_09']
    U09 = session.XYDataFromPath(name='XY_09',
                        variable=('U',NODAL,( (INVARIANT,'Magnitude'),),), path=pth, includeIntersections=False,
        projectOntoMesh=False, pathStyle=PATH_POINTS, numIntervals=10,
        projectionTolerance=0, shape=DEFORMED, labelType=TRUE_DISTANCE)
    pth = session.paths['Path_07']
    U07 = session.XYDataFromPath(name='XY_07', variable=('U',NODAL,( (INVARIANT,'Magnitude'),),), path=pth, includeIntersections=False,
        projectOntoMesh=False, pathStyle=PATH_POINTS, numIntervals=10,
        projectionTolerance=0, shape=DEFORMED, labelType=TRUE_DISTANCE)
    c1 = session.Curve(xyData=U09)
    c2 = session.Curve(xyData=U07)

    chart.setValues(curvesToPlot=(c1, c2, ), )
    session.viewports['Viewport: 1'].setValues(displayedObject=session.xyPlots['XYPlot-1'])
    session.xyPlots['XYPlot-1'].charts[chartName].axes2d[0].axisData.setValues(maxValue=45, maxAutoCompute=False, minValue=5,
                                                          minAutoCompute=False)
    session.printToFile(fileName='C:/Users/sondreor/Desktop/Sweeps/BottomFaceSweep/'+jobbo, format=TIFF, canvasObjects=(
        session.viewports['Viewport: 1'], ))

    del session.xyDataObjects['XY_07']
    del session.xyDataObjects['XY_09']
    del session.paths['Path_07']
    del session.paths['Path_09']
    del session.xyPlots['XYPlot-1']
    session.odbs['C:/temp/'+jobbo+'.odb'].close()

