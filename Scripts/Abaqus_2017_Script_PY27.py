from abaqus import *
from abaqusConstants import *
import __main__


def SetUpSimulations(op):
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
    import time
    start_time = (time.time())
    t= start_time- time.time()
    print t
    Mdb()
    step = mdb.openStep('C:/Users/sondreor/Desktop/NX_files/pyScriptmodel'+str(op)+'.stp',
                        scaleFromFile=OFF)
    mdb.models['Model-1'].PartFromGeometryFile(name='pyScriptmodel0-1',
                                               geometryFile=step, combine=False, dimensionality=THREE_D,
                                               type=DEFORMABLE_BODY)
    mdb.models['Model-1'].PartFromGeometryFile(name='pyScriptmodel0-2',
                                               geometryFile=step, bodyNum=2, combine=False, dimensionality=THREE_D,
                                               type=DEFORMABLE_BODY)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['pyScriptmodel0-1']
    a.Instance(name='pyScriptmodel0-1-1', part=p, dependent=OFF)
    p = mdb.models['Model-1'].parts['pyScriptmodel0-2']
    a.Instance(name='pyScriptmodel0-2-1', part=p, dependent=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.InstanceFromBooleanMerge(name='Part-1', instances=(
        a.instances['pyScriptmodel0-1-1'], a.instances['pyScriptmodel0-2-1'],
    ), keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)
    del mdb.models['Model-1'].parts['pyScriptmodel0-1']
    del mdb.models['Model-1'].parts['pyScriptmodel0-2']
    a.deleteFeatures(('pyScriptmodel0-1-1', 'pyScriptmodel0-2-1',))

    # Materials
    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'Epoxy', '2017',
                                 """{'name': 'Epoxy', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((2908.0, 0.3),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((1.19e-06,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'materialIdentifier': '', 'damping': {'composite': 0.0, 'alpha': 0.0, 'beta': 0.0001, 'structural': 0.0}, 'description': ''}""")

    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'CFPP', '2017',
                                 """{'name': 'CFPP', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((67000.0, 66000.0, 10000.0, 0.02, 0.3, 0.3, 3500.0, 3300.0, 3300.0),), 'type': ENGINEERING_CONSTANTS}, 'density': {'temperatureDependency': OFF, 'table': ((1.58e-06,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'materialIdentifier': '', 'damping': {'composite': 0.0, 'alpha': 0.0, 'beta': 0.001, 'structural': 0.0}, 'description': ''}""")

    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1',
                                                  material='Epoxy', thickness=None)
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2',
                                                  material='CFPP', thickness=None)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]',), )
    region = p.Set(cells=cells, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]',), )
    region = p.Set(cells=cells, name='Set-2')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['Part-1']
    region = p.sets['Set-2']
    p = mdb.models['Model-1'].parts['Part-1']
    surfaces = p.faces[5:6]
    normalAxis = p.Surface(side1Faces=surfaces, name='Mat-Dir-3')
    p = mdb.models['Model-1'].parts['Part-1']
    edges = p.edges[0:1]
    primaryAxis = p.Set(edges=edges, name='Mat-Dir-1')
    mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(region=region,
                                                              orientationType=DISCRETE, axis=AXIS_1,
                                                              normalAxisDefinition=SURFACE,
                                                              normalAxisRegion=normalAxis,
                                                              flipNormalDirection=False,
                                                              normalAxisDirection=AXIS_3, primaryAxisDefinition=EDGE,
                                                              primaryAxisRegion=primaryAxis,
                                                              primaryAxisDirection=AXIS_1,
                                                              flipPrimaryDirection=False,
                                                              additionalRotationType=ROTATION_NONE,
                                                              angle=0.0, additionalRotationField='',
                                                              stackDirection=STACK_3)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=2, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=C3D20R)
    elemType2 = mesh.ElemType(elemCode=C3D15)
    elemType3 = mesh.ElemType(elemCode=C3D10)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]',), )
    pickedRegions = (cells,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
                                                       elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#2 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=C3D20R)
    elemType2 = mesh.ElemType(elemCode=C3D15)
    elemType3 = mesh.ElemType(elemCode=C3D10)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]',), )
    pickedRegions = (cells,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
                                                       elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()


    print (time.time() - start_time)

    #Apply BC to inital step and make BC sets
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces[15:16]  # Specific number after investiation on assembly models in Abaqus

    region = a.Set(faces=f1, name='Bottom')
    mdb.models['Model-1'].XsymmBC(name='BC-1', createStepName='Initial',
                                  region=region, localCsys=None)

    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces[17:18]
    region = a.Set(faces=f1, name='Holding_Ring')
    mdb.models['Model-1'].EncastreBC(name='BC-2', createStepName='Initial',
                                     region=region, localCsys=None)

    #Make FSI Surface
    a = mdb.models['Model-1'].rootAssembly
    side1Faces1 = a.instances['Part-1-1'].faces[5:9] + a.instances['Part-1-1'].faces[18:21] + a.instances[
                                                                                                  'Part-1-1'].faces[
                                                                                              29:30]

    a.Surface(side1Faces=side1Faces1, name='PressureSurface')
    #Copy Model
    mdb.Model(name='Model-1-Copy', objectToCopy=mdb.models['Model-1'])

    # Make Dynamic and static step
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    mdb.models['Model-1-Copy'].ImplicitDynamicsStep(name='Step-1',
                                                    previous='Initial')
    # Import  loads to both
    #First, import field data
    f = open(
        'C:\\Users\\sondreor\\Dropbox\\!PhD!\\Propeller Design and Production\\Python NX_ Journal\\Pressure_Distribution.txt',
        'r+')
    text = f.read()
    lines = text.split('\n')
    tabell = []
    for line in lines:
        if not line == lines[-1]:
            data = line.split('\t')
            for i in range(0, len(data)):
                data[i] = float(data[i])
            tabell.append(data)
    mod = mdb.models['Model-1']
    mod.MappedField(name='Pressure_Field-1', description='',
                                      regionType=POINT, partLevelData=False, localCsys=None,
                                      pointDataFormat=XYZ, fieldDataType=SCALAR,
                                      xyzPointData=tabell)
    a = mod.rootAssembly
    region = a.surfaces['PressureSurface']
    mod.Pressure(name='Load-1', createStepName='Step-1',
                                   region=region, distributionType=FIELD, field='Pressure_Field-1',
                                   magnitude=1.0, amplitude=UNSET)

    mod = mdb.models['Model-1-Copy']
    mod.MappedField(name='Pressure_Field-1', description='',
                    regionType=POINT, partLevelData=False, localCsys=None,
                    pointDataFormat=XYZ, fieldDataType=SCALAR,
                    xyzPointData=tabell)
    a = mod.rootAssembly
    region = a.surfaces['PressureSurface']
    mod.Pressure(name='Load-1', createStepName='Step-1',
                 region=region, distributionType=FIELD, field='Pressure_Field-1',
                 magnitude=1.0, amplitude=UNSET)
    # Make Jobs
    mdb.Job(name='Job'+str(op)+'-1', model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN,
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT,
            numCpus=1, numGPUs=0)

    mdb.Job(name='Job'+str(op)+'-2', model='Model-1-Copy', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN,
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT,
            numCpus=1, numGPUs=0)

    mdb.jobs['Job'+str(op)+'-1'].submit(consistencyChecking=OFF)
    mdb.jobs['Job'+str(op)+'-1'].waitForCompletion()
files =50
for op in range(0,files):
    SetUpSimulations(op)
    print('Toerk opp')