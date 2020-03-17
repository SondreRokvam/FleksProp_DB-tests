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
import os
import numpy as np
import sys

class HydroWing:
    def __init__(self, cae_file_path,input_file_path,load_file_path):
        self.cae_file_path = cae_file_path
        self.input_file_path = input_file_path
        self.load_file_path = load_file_path
        self.r = 500
        self.r_val = [0.5, 0.6, 0.7, 0.8, 0.9]
        self.partition_set_names = []

    def openCAE(self):
        openMdb(self.cae_file_path)

    def all_over(self, angles, thickness):
        input_file_location = self.input_file_path
        os.chdir(input_file_location)
        input_folder_name = getInput('Enter name for folder containing input files: ')
        if not os.path.exists(input_folder_name):
            os.mkdir(input_folder_name)
            print("Directory " , input_folder_name ,  " Created ")
            os.chdir(input_folder_name)
        else:
            print("Directory " , input_folder_name ,  " already exists")
            os.chdir(input_folder_name)
            return

        for angle in angles:
            try:
                self.openCAE()
                p = mdb.models['Model-1'].parts['HW']

                #--------------- Materials -------------------------------------
                mdb.models['Model-1'].Material(name='CF')
                mdb.models['Model-1'].Material(name='Foam')
                mdb.models['Model-1'].materials['CF'].Elastic(type=ENGINEERING_CONSTANTS,
                        table=((130000.0, 10000.0, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,
                        3000.0), ))
                mdb.models['Model-1'].materials['Foam'].Elastic(type=ISOTROPIC,
                        table=((300,0.3), ))


                #---------------- Section ----------------------------------------
                sectionLayer1 = section.SectionLayer(material='CF', thickness=thickness,
                    orientAngle=angle, numIntPts=3, plyName='')
                mdb.models['Model-1'].CompositeShellSection(name='CF', preIntegrate=OFF,
                    idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                    useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

                mdb.models['Model-1'].HomogeneousSolidSection(name='Foam',
                    material='Foam', thickness=None)

                # --------------- Assignment ----------------------------------------
                cells = p.cells
                region = p.Set(cells=cells, name='Set-1')
                p.SectionAssignment(region=region, sectionName='Foam', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
                faces = p.faces
                p.Skin(faces=faces, name='Skin-1')
                region = p.Set(skinFaces=(('Skin-1', faces), ), name='Set-4')
                p.SectionAssignment(region=region, sectionName='CF', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)


                # ----------------- Orientation -------------------------------------
                s = p.faces
                edge = p.edges.getByBoundingBox(-1000,-1000,249,1000,1000,251)
                normalAxisRegion = p.Surface(side1Faces=s, name='Normal_Axis_Region')
                primaryAxisRegion = p.Set(edges=edge, name='Primary_Axis_Region')
                mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                    orientationType=GLOBAL, axis=AXIS_1,
                    additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='')

                """
                mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                    orientationType=DISCRETE, axis=AXIS_3, normalAxisDefinition=SURFACE,
                    normalAxisRegion=normalAxisRegion, flipNormalDirection=False,
                    normalAxisDirection=AXIS_3, primaryAxisDefinition=EDGE,
                    primaryAxisRegion=primaryAxisRegion, primaryAxisDirection=AXIS_2,
                    flipPrimaryDirection=False, additionalRotationType=ROTATION_NONE,
                    angle=0.0, additionalRotationField='')
                """

                # ----------------- Skin Mesh ----------------------------------------

                elemType1 = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
                elemType2 = mesh.ElemType(elemCode=STRI65, elemLibrary=STANDARD)
                a = mdb.models['Model-1'].rootAssembly
                f1 = a.instances['HW-1'].faces
                pickedRegions = regionToolset.Region(skinFaces=(('Skin-1', f1), ))
                a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

                # ------------------ Job ----------------------------------------------
                name = 'HWAllOver_' + str(int(angle))
                print(name)
                mdb.Job(name=name, model='Model-1', description='', type=ANALYSIS,
                    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                    numGPUs=0)
                mdb.jobs[name].writeInput(consistencyChecking=OFF)
                mdb.close()
            except:
                pass

    def partitionHorizontal(self,division,grid=0):
        if not grid:
            self.sets = []
        p = mdb.models['Model-1'].parts['HW']
        tol = 5

        #---------- Specifying Partition Density Horizontal -----------------------------
        partitiondensity = []
        Radius = 500   # Later make this a user defined input
        #division = 3  # Later make this a user defined input.
        splits = (Radius-150)/division
        startpart = 150+splits
        for y in range(int(startpart),int(Radius-tol),int(splits)):
            partitiondensity.append(y)

        # ------------Creating Horizontal Partitions- -----------------------

        cells = p.cells
        if not grid:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=151)
        for z in partitiondensity:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=z)
        d1 = p.datums

        i = 0
        if not grid:
            z = d1.values()[0]
            pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
            p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
            pickedCells = cells.getByBoundingBox(-1000, -1000 , 0, 1000, 1000 , 150+tol)
            p.Set(cells=pickedCells, name='Cell-Brim')
            for z in d1.values()[1:]:
                pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
                p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
                pickedCells = cells.getByBoundingBox(-1000, -1000 , 150+(i*splits)-tol, 1000, 1000 , 150+((i+1)*splits)+tol)
                p.Set(cells=pickedCells, name='Cell-'+str(i+1))
                i += 1
            pickedCells = cells.getByBoundingBox(-1000, -1000 , 150+i*splits-tol, 1000, 1000 , Radius+tol)
            p.Set(cells=pickedCells, name='Cell-'+str(i+1))
            self.sets.append('Cell-'+str(i+1))
        else:
            for z in d1.values()[division:]:
                pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
                p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
                i += 1

    def partitionVertical(self,division,grid=0):
        if not grid:
            self.sets = []
        p = mdb.models['Model-1'].parts['HW']
        tol = 5
        #---------- Specifying Partition Density Horizontal -----------------------------
        partitiondensity = []
        boundingBox = p.cells.getBoundingBox()
        ymin = boundingBox['low'][1]

        ymax = boundingBox['high'][1]

        splits = (ymax-ymin)/division
        startpart = ymin+splits
        for y in range(int(startpart),int(ymax-tol),int(splits)):
            partitiondensity.append(y)

        # ------------Creating Vertical Partitions- -----------------------

        datums = p.datums
        tol = 5
        cells = p.cells
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=151)
        for y in partitiondensity:
            p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=y)

        i=0
        pickedCells=cells.getByBoundingBox(-1000,-1000,-1000,1000,1000,1000)
        p.PartitionCellByDatumPlane(datumPlane=datums.values()[0], cells=pickedCells)
        pickedCells = cells.getByBoundingBox(-1000,-1000,0,1000,1000,150+tol)
        p.Set(cells=pickedCells, name='Cell-brim')
        for z in datums.values()[1:]:
            pickedCells = cells.getByBoundingBox(-1000, ymin-tol, 150, 1000, ymax+tol,1000)
            p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
            if not grid:
                pickedCells = cells.getByBoundingBox(-1000, ymin+(i*splits)-tol, 150, 1000, ymin+((i+1)*splits)+tol,1000)
                p.Set(cells=pickedCells, name='Cell-'+str(i+1))
                self.sets.append('Cell-'+str(i+1))
            i += 1
        if not grid:
            pickedCells = cells.getByBoundingBox(-1000, ymin+(i*splits)-tol, 150, 1000, ymin+((i+1)*splits)+tol,1000)
            p.Set(cells=pickedCells, name='Cell-'+str(i+1))

    def partitionGrid(self,division):
        p = mdb.models['Model-1'].parts['HW']
        partitiondensity = []
        tol = 30/division
        Radius = 500
        brim = 150
        boundingBox = p.cells.getBoundingBox()
        xmin, ymin, zmin = boundingBox['low']
        xmax, ymax, zmax = boundingBox['high']

        self.partitionVertical(division,grid=1)
        self.partitionHorizontal(division,grid=1)

        splity = (ymax-ymin)/division
        splitz = (zmax-151)/division
        cells = p.cells

        self.sets = []
        for j in range(division):
            for i in range(division):
                pickedCells = cells.getByBoundingBox(-1000,ymin-tol+i*splity,150-tol+j*splitz,1000,ymin+tol+(i+1)*splity,150+tol+(j+1)*splitz)
                if pickedCells:
                    p.Set(cells=pickedCells, name='Cell-'+str(j+1)+str(i+1))
                    self.sets.append('Cell-'+str(j+1)+str(i+1))

    def assignSections(self,stiffSection):
        p = mdb.models['Model-1'].parts['HW']
        sets = p.sets
        self.createMaterials()
        for i in sets.keys():
            if i == stiffSection:
                p.SectionAssignment(region=sets[i], sectionName='Steel', offset=0.0,
                                offsetType=TOP_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            else:
                p.SectionAssignment(region=sets[i], sectionName='Foam', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)

    def removeSections(self):
        for section in mdb.models['Model-1'].parts['HW'].sectionAssignments:
            del section

    def createMaterials(self,angle=0):

        #-------------- Materials --------------------------------
        mdb.models['Model-1'].Material(name='CF')
        mdb.models['Model-1'].materials['CF'].Elastic(type=ENGINEERING_CONSTANTS,
        table=((130000.0, 10000.0, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,3000.0), ))

        mdb.models['Model-1'].Material(name='Steel')
        mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000.0, 0.3), ))

        mdb.models['Model-1'].Material(name='Foam')
        mdb.models['Model-1'].materials['Foam'].Elastic(table=((200.0, 0.3), ))

        # -------------- Sections -----------------------------
        sectionLayer1 = section.SectionLayer(material='CF', thickness=0.2,
                                             orientAngle=angle, numIntPts=3, plyName='')
        mdb.models['Model-1'].CompositeShellSection(name='CF', preIntegrate=OFF,
                                                    idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                                                    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                                                    useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

        mdb.models['Model-1'].HomogeneousSolidSection(name='Steel', material='Steel',
                                                      thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Foam', material='Foam',
                                                      thickness=None)

    def prep(self):

        pressure_field_path = self.load_file_path
        r = self.r
        r_val = self.r_val
        model = mdb.models['Model-1']
        p = model.parts['HW']

        #--------------------- Make assembly -------------------
        a = model.rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        a.Instance(name='HW',
           part=p,
           dependent=OFF)


        #--------------------Partition Settings--------------------
        a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,
                             offset=200.0)
        d1 = a.datums
        e1 = a.instances['HW'].edges
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
        a.projectReferencesOntoSketch(sketch=s,
                                      filter=COPLANAR_EDGES)


        #--------------------Draw Radius lines--------------------

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
        f1 = a.instances['HW'].faces
        d21 = a.datums
        e11 = a.instances['HW'].edges
        a.PartitionFaceBySketchThruAll(sketchPlane=d21[4],
                                       sketchUpEdge=d21[1].axis3,
                                       faces=f1,
                                       sketchPlaneSide=SIDE1,
                                       sketch=s)
        s.unsetPrimaryObject()
        del model.sketches['__profile__']
        e1 = a.instances['HW'].edges
        a.Set(name='postPartiti',
              edges=e1)
        a.SetByBoolean(name='r_edges',
                       sets=(a.sets['postPartiti'],
                             a.sets['prePartiti']),
                       operation=DIFFERENCE)
        e1 = a.instances['HW'].edges
        del a.sets['postPartiti']
        del a.sets['prePartiti']

        #--------------------Step--------------------
        model.StaticStep(name='Step-1',
                         previous='Initial',
                         initialInc=0.001,
                         maxInc=0.1)

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
        s1 = a.instances['HW'].faces
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
        s1 = a.instances['HW'].faces
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

    def mesh(self,meshSize):
        r = self.r
        r_val = self.r_val
        tol = 0.01
        model = mdb.models['Model-1']
        a = model.rootAssembly
        partInstances =(a.instances['HW'], )

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

        a.seedPartInstance(regions=partInstances,
                           size=meshSize,
                           deviationFactor=0.1,
                           minSizeFactor=0.1)
        c1 = a.instances['HW'].cells
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
        e1 = a.instances['HW'].edges

    def applyLoad(self):
        model = mdb.models['Model-1']
        readfile = open(self.load_file_path,"r")
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
        s1 = a.instances['HW'].faces.getByBoundingBox(-1000,-1000,-1000,1000,1000,1000)
        region = a.Surface(side1Faces=s1, name='Surf-1')
        model.Pressure(name='Load-1',
                       createStepName='Step-1',
                       region=region,
                       distributionType=FIELD,
                       field='AnalyticalField-1',
                       magnitude=1.0,
                       amplitude=UNSET)

    def writeInput(self,partition,stiffSection):

        name = 'HW' + partition + stiffSection
        print(name)
        mdb.Job(name=name, model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numGPUs=0)
        mdb.jobs[name].writeInput(consistencyChecking=OFF)

    def createFolder(self):
        input_file_location = self.input_file_path
        os.chdir(input_file_location)
        input_folder_name = getInput('Enter name for folder containing input files: ')
        self.input_file_path += '\\' + input_folder_name
        if not os.path.exists(input_folder_name):
            os.mkdir(input_folder_name)
            print("Directory " , input_folder_name ,  " Created ")
            os.chdir(input_folder_name)
        else:
            print("Directory " , input_folder_name ,  " already exists")
            os.chdir(input_folder_name)
            return

    def createBatch(self):
        os.chdir(self.input_file_path)
        current=os.getcwd()
        print(current+'\\')
        # Hent
        odb_names = [f for f in os.listdir(current) if (f.endswith('.inp')) ]
        s=open(current+'\\'+'run_inputs.bat',"w+")
        for od in odb_names:
            s.write('call abq2017 job='+od[:-4]+ ' int\n')
        s.close()

caeFilePath = 'C:\Users\Jon\OneDrive\FleksProp\Scripts\HW.cae'
inputFileLocation = 'C:\Users\Jon\OneDrive\FleksProp\InputFiles'
pressure_field_path = "C:\Users\Jon\OneDrive\FleksProp\Scripts\load.txt"


partition = 'Grid' # 'AllOver' , 'Vertical' , 'Horizontal' , 'Grid'
partitionRefinement = 5
cellOrFace = 'Cell' # 'Cell' , 'Face'
#side = 'P' # 'S'
plyAngleLimits = [-90,90] # or nothing
plyAngleNumber = 20 #
plyThickness = 0.2
stiffSection='Cell-15'


propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.openCAE()
#propeller.createFolder()
propeller.partitionGrid(partitionRefinement)
propeller.applyLoad()
propeller.mesh(10)
"""
for sets in propeller.sets:
    propeller.assignSections(sets)
    propeller.writeInput(partition,sets)
    propeller.removeSections()
propeller.createBatch()

"""
