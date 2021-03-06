import abaqus as Aba
import abaqusConstants as AbaCon
from abaqus import  *
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

class FleksProp():
    def __init__(self, file_path, pressure_field_path,
                 inputFileLocation, part_name, r_val,
                 partition, partitionRefinement, shellOrSolid,
                 side, ratio_list, filtyp):
        self.model = mdb.models['Model-1']
        self.part_name = part_name
        self.file_path = file_path
        self.inputFileLocation = inputFileLocation
        self.pressure_field_path = pressure_field_path
        self.file = self.part_name + '-1'
        self.tol = 0.01
        self.r_val = r_val
        self.partition = partition
        self.partitionRefinement = partitionRefinement
        self.ratio_list = ratio_list
        if shellOrSolid == 'shell':
            self.reply = 'sel'
            #self.reply = AbaCon.YES
        elif shellOrSolid == 'solid':
            self.reply = 'sol'
        self.side = side

    def SetUpAZP(self):

        # --------------------Initial Variable Names and Settings--------------------
        #self.reply = Aba.getWarningReply(message='Press YES for sheet body \nPress NO for solid body',
        #                           buttons=(AbaCon.YES, AbaCon.NO))

        self.r = float(getInput('Enter the propeller radius(mm):'))

        # --------------------Prompt user for which radii to inspect--------------------
        fields = (('R= ', '0.5'), ('R= ', '0.6'), ('R= ', '0.7'), ('R= ', '0.8'), ('R= ', '0.9'),
                  ('R= ', ''), ('R= ', ''), ('R= ', ''),('R= ', ''), ('R= ', ''))
        self.r_input = getInputs(fields=fields,
                            label='Enter percentages of the propeller radius(0.5, 0.6,...etc.):',
                            dialogTitle='Inspected radii', )

        # filter out empty and duplicate inputs
        self.r_val = []
        for i in range(len(self.r_input)):
            duplicate = 0
            if self.r_input[i] != '':
                self.r_val.append(float(self.r_input[i]))
                for j in range(len(self.r_val) - 1):
                    if self.r_val[-1] == self.r_val[j]:
                        duplicate = 1
            if duplicate == 1:
                self.r_val.remove(self.r_val[-1])
        self.r_val.sort()

        # --------------------Save list of radii and set names to C:\temp--------------------
        self.r_name = []  # Used throughout the script to name sets
        self.set_name = []
        for i in range(len(self.r_val)):
            self.r_name.append('R_' + str(self.r_val[i])[2:])
            self.set_name.append('PROFILE-' + self.r_name[i])
        self.npz_name = 'parameters_for_plot.npz'
        np.savez(self.npz_name,
                 r_val=self.r_val,
                 set_name=self.set_name)
        npzfile = np.load(self.npz_name)

        # --------------------Import--------------------
        self.step = mdb.openStep(self.file_path,
                            scaleFromFile=OFF)
        self.model.PartFromGeometryFile(name=self.part_name,
                                   geometryFile=self.step,
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
        for i in range(len(self.r_val)):
            s.CircleByCenterPerimeter(center=(0.0, 0.0),
                                      point1=(self.r * self.r_val[i], 0.0))

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

        for i in range(len(self.r_name)):
            edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), self.r * self.r_val[i] + self.tol)
            a.Set(edges=edges,
                  name=self.r_name[i] + '+tol')
            edges = e1.getByBoundingCylinder((-1000, 0, 0), (1000, 0, 0), self.r * self.r_val[i] - self.tol)
            a.Set(edges=edges,
                  name=self.r_name[i] + '-tol')
            a.SetByBoolean(name='Area',
                           sets=(a.sets[self.r_name[i] + '+tol'], a.sets[self.r_name[i] + '-tol']),
                           operation=DIFFERENCE)
            a.SetByBoolean(name=self.set_name[i],
                           sets=(a.sets['Area'], a.sets['r_edges']),
                           operation=INTERSECTION)
            del a.sets['Area']
            del a.sets[self.r_name[i] + '+tol']
            del a.sets[self.r_name[i] + '-tol']
            n_labels = []
            for j in range(len(a.sets[self.set_name[i]].nodes)):
                node = a.sets[self.set_name[i]].nodes[j].label
                n_labels.append(node)
            n_labels = np.array(n_labels)
            a.SetFromNodeLabels(name='nodes_' + self.r_name[i],
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

    def SetUpHW(self):
        # --------------------Initial Variable Names and Settings--------------------
        self.reply = getWarningReply(message='Press YES for sheet body \nPress NO for solid body',
                                buttons=(YES, NO))

        self.r = float(getInput('Enter the propeller radius(mm):'))


        # --------------------Prompt user for which radii to inspect--------------------
        self.fields = (('R= ', '0.5'), ('R= ', '0.6'), ('R= ', '0.7'), ('R= ', '0.8'), ('R= ', '0.9'), ('R= ', ''), ('R= ', ''),
                  ('R= ', ''), ('R= ', ''), ('R= ', ''))
        self.r_input = getInputs(fields=self.fields,
                            label='Enter percentages of the propeller radius(0.5, 0.6,...etc.):',
                            dialogTitle='Inspected radii', )

        # filter out empty and duplicate inputs
        self.r_val = []
        for i in range(len(self.r_input)):
            duplicate = 0
            if self.r_input[i] != '':
                self.r_val.append(float(self.r_input[i]))
                for j in range(len(self.r_val) - 1):
                    if self.r_val[-1] == self.r_val[j]:
                        duplicate = 1
            if duplicate == 1:
                self.r_val.remove(self.r_val[-1])
        self.r_val.sort()

        # r_val = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95] #If all radii are predefined, uncomment this line, add the percentages to the list and comment out the previous 15 lines

        # --------------------Save list of radii and set names to C:\temp--------------------
        self.r_name = []  # Used throughout the script to name sets
        self.set_name = []
        for i in range(len(self.r_val)):
            self.r_name.append('R_' + str(self.r_val[i])[2:])
            self.set_name.append('PROFILE-' + self.r_name[i])
        npz_name = 'parameters_for_plot.npz'
        self.np.savez(npz_name,
                 r_val=self.r_val,
                 set_name=self.set_name)
        npzfile = self.np.load(npz_name)

        # --------------------Import--------------------
        self.step = mdb.openStep(file_path,
                            scaleFromFile=OFF)
        self.model.PartFromGeometryFile(name=self.part_name,
                                   geometryFile=self.step,
                                   combine=True,
                                   retainBoundary=True,
                                   mergeSolidRegions=True,
                                   dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
        p = self.model.parts[self.part_name]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)

        # --------------------Material--------------------
        # model.Material(name='CF-UD')
        # model.materials['CF-UD'].Elastic(type=ENGINEERING_CONSTANTS,
        #                                  table=((140000.0, 10000.0, 10000.0,      # E1, E2, E3
        #                                          0.28, 0.28, 0.5,                 # v12, v13, v23
        #                                          3300.0, 3300.0, 3500.0),))       # G12, G13, G23

        # --------------------Make instance--------------------
        a = self.model.rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        a.Instance(name=self.file,
                   part=p,
                   dependent=OFF)

        # --------------------Partition Settings--------------------
        a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,
                                     offset=200.0)
        d1 = a.datums
        e1 = a.instances[self.file].edges
        a.Set(name='prePartiti',
              edges=e1)
        t = a.MakeSketchTransform(sketchPlane=d1[4],
                                  sketchUpEdge=d1[1].axis3,
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

        s.ConstructionLine(point1=(-26.25, 0.0), point2=(18.75, 0.0))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        s.ConstructionLine(point1=(0.0, 17.5), point2=(0.0, -10.0))
        s.VerticalConstraint(entity=g[3], addUndoState=False)

        s.FixedConstraint(entity=g[3])
        s.FixedConstraint(entity=g[2])

        for line in range(len(self.r_val)):
            s.Line(point1=(-15.0, 15.0), point2=(13.75, 15.0))
            s.HorizontalConstraint(entity=g[line + 4], addUndoState=False)
            s.ObliqueDimension(vertex1=v[2 * line], vertex2=v[2 * line + 1], textPoint=(-4.73760223388672,
                                                                                        9.81308364868164), value=1000)
            s.DistanceDimension(entity1=g[line + 4], entity2=g[2], textPoint=(29.0790710449219,
                                                                              5.39719390869141), value=self.r_val[line] * self.r)
            s.DistanceDimension(entity1=v[2 * line], entity2=g[3], textPoint=(22.0712547302246,
                                                                              49.0563049316406), value=500)

        # --------------------Make Partition--------------------
        a = self.model.rootAssembly
        f1 = a.instances[self.file].faces
        d21 = a.datums
        e11 = a.instances[self.file].edges
        a.PartitionFaceBySketchThruAll(sketchPlane=d21[4],
                                       sketchUpEdge=d21[1].axis3,
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

        for i in range(len(self.r_name)):
            edges = e1.getByBoundingBox(-1000, -1000, self.r_val[i] * self.r - self.tol, 1000, 1000, self.r_val[i] * self.r + self.tol)
            a.Set(edges=edges,
                  name='Area')
            a.SetByBoolean(name=self.set_name[i],
                           sets=(a.sets['Area'], a.sets['r_edges']),
                           operation=INTERSECTION)
            del a.sets['Area']

            n_labels = []
            for j in range(len(a.sets[self.set_name[i]].nodes)):
                node = a.sets[self.set_name[i]].nodes[j].label
                n_labels.append(node)
            n_labels = np.array(n_labels)
            a.SetFromNodeLabels(name='nodes_' + self.r_name[i],
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

        readfile = open(pressure_field_path, "r")
        reading = readfile.read()
        pressuredist = reading.split('\n')
        len_s = len(pressuredist)

        for i in range(len_s):
            t = pressuredist[i].split('\t')
            for j in range(len(t)):
                t[j] = float(t[j])
            pressuredist[i] = t
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
        d1 = a.datums
        a.AttachmentPoints(name='Attachment Points-1', points=(d1[1].origin,),
                           setName='Attachment Points-1-Set-1')
        v1 = a.vertices
        verts1 = v1.getByBoundingBox(-1, -1, -1, 1, 1, 1)
        region1 = a.Set(vertices=verts1, name='m_Set-14')
        s1 = a.instances[self.file].faces
        side1Faces1 = s1.getByBoundingBox(-100, -150, 98, 100, 100, 102)
        region2 = a.Surface(side1Faces=side1Faces1, name='s_Surf-1')
        mdb.models['Model-1'].Coupling(name='Constraint-1', controlPoint=region1,
                                       surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
                                       localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

        self.model.DisplacementBC(name='BC-1', createStepName='Initial',
                             region=region1,
                             u1=0.0, u2=0.0, u3=0.0, ur1=0, ur2=0, ur3=0,
                             amplitude=UNSET,
                             fixed=OFF,
                             distributionType=UNIFORM,
                             fieldName='',
                             localCsys=None)

        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].setValues(displayedObject=a)

    def FullLaminateAZP(self):

        self.ratio_list = [100, 75, 50, 25, 10, 1, 10, 25, 50, 75, 100]
        for i in range(len(self.ratio_list)):
            if i > 0:
                self.model.parts[self.part_name].compositeLayups['Layup-' + material_name].suppress()
            # --------------------Material--------------------
            ratio = self.ratio_list[i]
            if i <= (len(self.ratio_list) - 1) / 2:
                E1 = 140000
                E2 = E1 / ratio
                material_name = 'CF-R-E1_E2_' + str(ratio)
            elif i > (len(self.ratio_list) - 1) / 2:
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
            mdb.jobs[job].writeInput(consistencyChecking=OFF)
            #mdb.jobs[job].submit(consistencyChecking=OFF)
            #mdb.jobs[job].waitForCompletion()

"""Sondre Tweeaked variabler"""
Aba.Mdb()
name = 'AzP65C'
r = 650
partitionMethods = 'Fan'
Refinement = 10
shellOrSolidTest = 'solid'
sid = 'P'
ratio_li = [0.5,0.6,0.7,0.8,0.9]
step_CAEimp ='step'#'CAE'

userP='C:/Users/sondreor/Dropbox/!PhD!/'
file_p = userP+'Propeller Design and Production/LargeScale/0_Basic_3D-files .prt .stp .iges/Azp65C-PB_no_Fillet_Shell.stp'
pressure_fi_path = userP+"Propeller Design and Production/LargeScale/0_Trykkfordelinger/P65C_25kn_561rpm__Aba.txt"
stepfil =userP+'/Propeller Design and Production/LargeScale/0_Trykkfordelinger/P65C_25kn_561rpm__Aba.txt'
inputLocation = 'C:/Temp'

p1 = FleksProp(file_p, stepfil,
                 inputLocation, name, r, partitionMethods,
                 Refinement, shellOrSolidTest,
                 sid, ratio_li, step_CAEimp)
p1.SetUpAZP()
p1.FullLaminateAZP()