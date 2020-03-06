class FleksProp():

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

    def __init__(self, model, part_name, file_path, pressure_field_path):
        self.model = model
        self.part_name = part_name
        self.file_path = file_path
        self.pressure_field_path = pressure_field_path
        self.file = self.part_name + '-1'

    def SetUp(self):
        Mdb()
        # --------------------Initial Variable Names and Settings--------------------
        self.reply = getWarningReply(message='Press YES for sheet body \nPress NO for solid body',
                                    buttons=(YES, NO))
        if self.reply == YES:
            part_type = 0
        elif self.reply == NO:
            part_type = 1

        self.tol = 0.01
        self.r = float(getInput('Enter the propeller radius(mm):'))

        print('hei')
        # --------------------Prompt user for which radii to inspect--------------------
        fields = (('R= ', '0.5'), ('R= ', ''), ('R= ', ''), ('R= ', ''), ('R= ', ''), ('R= ', ''), ('R= ', ''), ('R= ', ''),
                  ('R= ', ''), ('R= ', ''))
        r_input = getInputs(fields=fields,
                            label='Enter percentages of the propeller radius(0.5, 0.6,...etc.):',
                            dialogTitle='Inspected radii', )

        # filter out empty and duplicate inputs
        r_val = []
        for i in range(len(r_input)):
            duplicate = 0
            if r_input[i] != '':
                r_val.append(float(r_input[i]))
                for j in range(len(r_val) - 1):
                    if r_val[-1] == r_val[j]:
                        duplicate = 1
            if duplicate == 1:
                r_val.remove(r_val[-1])
        r_val.sort()
        # r_val = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]  # If all radii are predefined, uncomment this line, add the percentages to the list and comment out the previous 15 lines

        # --------------------Save list of radii and set names to C:\temp--------------------
        r_name = []  # Used throughout the script to name sets
        set_name = []
        for i in range(len(r_val)):
            r_name.append('R_' + str(r_val[i])[2:])
            set_name.append('PROFILE-' + r_name[i])
        npz_name = 'parameters_for_plot.npz'
        self.np.savez(npz_name,
                 r_val=r_val,
                 set_name=set_name)
        npzfile = self.np.load(npz_name)

        # --------------------Import--------------------
        step = mdb.openStep(self.file_path,
                            scaleFromFile=OFF)
        self.model.PartFromGeometryFile(name=self.part_name,
                                   geometryFile=step,
                                   combine=True,
                                   retainBoundary=True,
                                   mergeSolidRegions=True,
                                   dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
        p = self.model.parts[self.part_name]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)

        # --------------------Make instance--------------------
        a = self.model.rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        a.Instance(name=self.file,
                   part=p,
                   dependent=OFF)

        # --------------------Particion Settings--------------------
        a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,
                                     offset=200.0)
        d1 = a.datums
        e1 = a.instances[self.file].edges
        a.Set(name='prePartiti',
              edges=e1)
        t = a.MakeSketchTransform(sketchPlane=d1[4],
                                  sketchUpEdge=e1[2],
                                  sketchPlaneSide=SIDE1,
                                  origin=(200.0, 0.0, 0.0))
        s = self.model.ConstrainedSketch(name='__profile__',
                                    sheetSize=1926.91,
                                    gridSpacing=48.17,
                                    transform=t)
        g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        a = self.model.rootAssembly
        a.projectReferencesOntoSketch(sketch=s,
                                      filter=COPLANAR_EDGES)

        # --------------------Draw Radius circles--------------------
        for i in range(len(r_val)):
            s.CircleByCenterPerimeter(center=(0.0, 0.0),
                                      point1=(self.r * r_val[i], 0.0))

        # --------------------Make Partition--------------------
        a = self.model.rootAssembly
        f1 = a.instances[self.file].faces
        d21 = a.datums
        e11 = a.instances[self.file].edges
        a.PartitionFaceBySketchThruAll(sketchPlane=d21[4],
                                       sketchUpEdge=e11[2],
                                       faces=f1,
                                       sketchPlaneSide=SIDE1,
                                       sketch=s)
        s.unsetPrimaryObject()
        del self.model.sketches['__profile__']
        e1 = a.instances[self.file].edges
        a.Set(name='postPartiti',
              edges=e1)
        a.SetByBoolean(name='r_edges',
                       sets=(a.sets['postPartiti'],
                             a.sets['prePartiti']),
                       operation=DIFFERENCE)
        e1 = a.instances[self.file].edges

        # --------------------MESH--------------------
        # Sheet mesh
        if self.reply == YES:
            session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
            session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
            a = self.model.rootAssembly
            f1 = a.instances[self.file].faces
            a.setMeshControls(regions=f1,
                              elemShape=TRI)  # Choose between: QUAD, QUAD_DOMINATED, TRI
            partInstances = (a.instances[self.file],)
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
            partInstances = (a.instances[self.file],)
            a.generateMesh(regions=partInstances)

        # Solid mesh
        if self.reply == NO:
            session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
            session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
            a = self.model.rootAssembly
            partInstances = (a.instances[self.file],)
            a.seedPartInstance(regions=partInstances,
                               size=10.0,
                               deviationFactor=0.1,
                               minSizeFactor=0.1)
            c1 = a.instances[self.file].cells
            a.setMeshControls(regions=c1,
                              elemShape=TET,
                              technique=FREE)
            elemType1 = mesh.ElemType(elemCode=C3D20R,
                                      elemLibrary=STANDARD)
            elemType2 = mesh.ElemType(elemCode=C3D15,
                                      elemLibrary=STANDARD)
            elemType3 = mesh.ElemType(elemCode=C3D10,
                                      elemLibrary=STANDARD)
            pickedRegions = (c1,)
            a.setElementType(regions=pickedRegions,
                             elemTypes=(elemType1, elemType2, elemType3))
            a.generateMesh(regions=partInstances)

        # --------------------NodeSets--------------------

        for i in range(len(r_name)):
            edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), self.r * r_val[i] + self.tol)
            a.Set(edges=edges,
                  name=r_name[i] + '+tol')
            edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), self.r * r_val[i] - self.tol)
            a.Set(edges=edges,
                  name=r_name[i] + '-tol')
            a.SetByBoolean(name='Area',
                           sets=(a.sets[r_name[i] + '+tol'], a.sets[r_name[i] + '-tol']),
                           operation=DIFFERENCE)
            a.SetByBoolean(name=set_name[i],
                           sets=(a.sets['Area'], a.sets['r_edges']),
                           operation=INTERSECTION)
            del a.sets['Area']
            del a.sets[r_name[i] + '+tol']
            del a.sets[r_name[i] + '-tol']
            n_labels = []
            for j in range(len(a.sets[set_name[i]].nodes)):
                node = a.sets[set_name[i]].nodes[j].label
                n_labels.append(node)
            n_labels = np.array(n_labels)
            a.SetFromNodeLabels(name='nodes_' + r_name[i],
                                nodeLabels=((self.file, n_labels),), )

        # --------------------Step--------------------
        self.model.StaticStep(name='Step-1',
                         previous='Initial',
                         initialInc=0.001,
                         maxInc=0.1)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON,
                                                                   bcs=ON,
                                                                   predefinedFields=ON,
                                                                   connectors=ON,
                                                                   adaptiveMeshConstraints=OFF)

        # --------------------Load--------------------
        readfile = open(self.pressure_field_path, "r")
        reading = readfile.read()
        pressuredist = reading.split('\n')
        len_s = len(pressuredist)
        empty_rows = []
        for i in range(len_s):
            if len(pressuredist[i]) == 0:
                empty_rows.append(i)
            t = pressuredist[i].split('\t')
            for j in range(len(t)):
                t[j] = float(t[j])
            pressuredist[i] = t
        if len(empty_rows) > 0:
            for i in range(len(empty_rows)):
                del pressuredist[empty_rows[i]]
        self.model.MappedField(name='AnalyticalField-1',
                          description='',
                          regionType=POINT,
                          partLevelData=False,
                          localCsys=None,
                          pointDataFormat=XYZ,
                          fieldDataType=SCALAR,
                          xyzPointData=pressuredist)
        a = self.model.rootAssembly
        s1 = a.instances[self.file].faces
        region = a.Surface(side1Faces=s1,
                           name='Surf-1')
        self.model.Pressure(name='Load-1',
                       createStepName='Step-1',
                       region=region,
                       distributionType=FIELD,
                       field='AnalyticalField-1',
                       magnitude=1.0,
                       amplitude=UNSET)

        # --------------------BC--------------------
        a = self.model.rootAssembly
        e1 = a.instances[self.file].edges
        edges = e1.getByBoundingCylinder((1000, 0, 0),  # Top        #This is only correct for AzP65C
                                         (-1000, 0, 0),  # Bottom
                                         self.r * 0.408)  # Radius
        a.Set(edges=edges,
              name='BC_edges_extra')
        edges = e1.getByBoundingCylinder((-254, -262, -7),  # Top        #This is only correct for AzP65C
                                         (-254, -262, -20),  # Bottom
                                         15)  # Radius
        a.Set(edges=edges,
              name='BC_edges_single')
        region = a.SetByBoolean(name='BC-Edges',
                                sets=(a.sets['BC_edges_extra'],
                                      a.sets['BC_edges_single']),
                                operation=DIFFERENCE)
        self.model.DisplacementBC(name='BC-1',
                             createStepName='Initial',
                             region=region,
                             u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
                             amplitude=UNSET,
                             fixed=OFF,
                             distributionType=UNIFORM,
                             fieldName='',
                             localCsys=None)

        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].setValues(displayedObject=a)






    def FullLaminate(self):

        ratio_list = [100, 75, 50, 25, 10, 1, 10, 25, 50, 75, 100]
        for i in range(len(ratio_list)):
            if i > 0:
                self.model.parts[self.part_name].compositeLayups['Layup-' + material_name].suppress()
            # --------------------Material--------------------
            ratio = ratio_list[i]
            if i <= (len(ratio_list) - 1) / 2:
                E1 = 140000
                E2 = E1 / ratio
                material_name = 'CF-R-E1_E2_' + str(ratio)
            elif i > (len(ratio_list) - 1) / 2:
                E2 = 140000
                E1 = E2 / ratio

                material_name = 'CF-R-E2_E1_' + str(ratio)

            self.model.Material(name=material_name)
            self.model.materials[material_name].Elastic(type=ENGINEERING_CONSTANTS,
                                                   table=((E1, E2, 10000,  # E1, E2, E3
                                                           0.02, 0.3, 0.3,  # v12, v13, v23
                                                           3500, 3300, 3300),))  # G12, G13, G23

            # -------------------------------LAYUP------------------------------------------------

            # ---------------------Layup-------------------------
            layupOrientation = None
            p = self.model.parts[self.part_name]
            f = p.faces
            region1 = regionToolset.Region(faces=f)

            p = self.model.parts[self.part_name]
            s = p.faces
            normalAxisRegion = p.Surface(side1Faces=s, name='Normal_Axis_Region')
            p = self.model.parts[self.part_name]
            e = p.edges
            edges = e.getSequenceFromMask(mask=('[#20 ]',), )
            primaryAxisRegion = p.Set(edges=edges, name='Primary_Axis_Region')
            compositeLayup = self.model.parts[self.part_name].CompositeLayup(name='Layup-' + material_name,
                                                                   description='',
                                                                   elementType=SHELL,
                                                                   offsetType=TOP_SURFACE,
                                                                   symmetric=False,
                                                                   thicknessAssignment=FROM_SECTION)
            compositeLayup.Section(preIntegrate=OFF,
                                   integrationRule=SIMPSON,
                                   thicknessType=UNIFORM,
                                   poissonDefinition=DEFAULT,
                                   temperature=GRADIENT,
                                   useDensity=OFF)

            compositeLayup.CompositePly(suppressed=False,
                                        plyName='Ply-1',
                                        region=region1,
                                        material=material_name,
                                        thicknessType=SPECIFY_THICKNESS,
                                        thickness=5.0,
                                        orientationType=SPECIFY_ORIENT,
                                        orientationValue=0.0,
                                        additionalRotationType=ROTATION_NONE,
                                        additionalRotationField='',
                                        axis=AXIS_3,
                                        angle=0.0,
                                        numIntPoints=3)
            compositeLayup.ReferenceOrientation(orientationType=DISCRETE,
                                                localCsys=None,
                                                additionalRotationType=ROTATION_NONE,
                                                angle=0.0,
                                                additionalRotationField='',
                                                axis=AXIS_3,
                                                stackDirection=STACK_3,
                                                normalAxisDefinition=SURFACE,
                                                normalAxisRegion=normalAxisRegion,
                                                normalAxisDirection=AXIS_3,
                                                flipNormalDirection=False,
                                                primaryAxisDefinition=EDGE,
                                                primaryAxisRegion=primaryAxisRegion,
                                                primaryAxisDirection=AXIS_1,
                                                flipPrimaryDirection=True)

            p = self.model.parts[self.part_name]
            session.viewports['Viewport: 1'].setValues(displayedObject=p)

            # -----------------Load--------------------------------------
            self.model.loads['Load-1'].setValues(distributionType=FIELD)

            # ------------------JOB------------------------------------
            job = 'Job-' + material_name
            session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
            session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
                meshTechnique=OFF)

            mdb.Job(name=job,
                    model='Model-1',
                    description='',
                    type=ANALYSIS,
                    atTime=None,
                    waitMinutes=0,
                    waitHours=0,
                    queue=None,
                    memory=90,
                    memoryUnits=PERCENTAGE,
                    getMemoryFromAnalysis=True,
                    explicitPrecision=SINGLE,
                    nodalOutputPrecision=SINGLE,
                    echoPrint=OFF,
                    modelPrint=OFF,
                    contactPrint=OFF,
                    historyPrint=OFF,
                    userSubroutine='',
                    scratch='',
                    resultsFormat=ODB,
                    multiprocessingMode=DEFAULT,
                    numCpus=1,
                    numGPUs=0)
            mdb.jobs[job].submit(consistencyChecking=OFF)
            mdb.jobs[job].waitForCompletion()

model = mdb.models['Model-1']
part_name = 'AzP65C'
file_path = 'C:\Users\Eivind\Documents\NTNU\FleksProp\Models\Azp65C-PB_no_Fillet_Shell.stp'
pressure_field_path = "C:\Users\Eivind\Pres.25kn_561rpm__Aba.txt"


p1 = FleksProp(model, part_name, file_path, pressure_field_path)
p1.SetUp()
p1.FullLaminate()