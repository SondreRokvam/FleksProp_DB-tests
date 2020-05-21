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
    def __init__(self, cae_file_path, input_file_path):
        self.cae_file_path = cae_file_path
        self.input_file_path = input_file_path
        self.r = 500
        self.r_val = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
        self.partition_set_names = []

    def openCAE(self):
        openMdb(self.cae_file_path)

    def all_over(self, bothSides=0):
        p = mdb.models['Model-1'].parts['HW']

        # --------------- Assignment ----------------------------------------
        if not bothSides:
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
            mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                orientationType=GLOBAL, axis=AXIS_1,
                additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='')

            # ----------------- Skin Mesh ----------------------------------------

            elemType1 = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
            elemType2 = mesh.ElemType(elemCode=STRI65, elemLibrary=STANDARD)
            a = mdb.models['Model-1'].rootAssembly
            f1 = a.instances['HW'].faces
            pickedRegions = regionToolset.Region(skinFaces=(('Skin-1', f1), ))
            a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

        else:
            cells = p.cells
            f = p.faces
            region = p.Set(cells=cells, name='Set-1')
            p.SectionAssignment(region=region, sectionName='Foam', offset=0.0,
                offsetType=MIDDLE_SURFACE, offsetField='',
                thicknessAssignment=FROM_SECTION)

            botFaces = f.findAt(((3.073776, -21.830757, 376.589579), ), ((-6.933196,
                    -65.248467, 149.969177), ))
            p.Skin(faces=botFaces, name='BotSkin')
            region = p.Set(skinFaces=(('BotSkin', botFaces), ), name='Set-2')
            p.SectionAssignment(region=region, sectionName='CF', offset=0.0,
                offsetType=MIDDLE_SURFACE, offsetField='',
                thicknessAssignment=FROM_SECTION)

            topFaces = f.findAt(((16.982367, -21.016115, 377.219167), ), ((-3.669506,
                        82.906904, 149.593831), ))
            p.Skin(faces=topFaces, name='TopSkin')
            region = p.Set(skinFaces=(('TopSkin', topFaces), ), name='Set-3')
            p.SectionAssignment(region=region, sectionName='CF2', offset=0.0,
                offsetType=MIDDLE_SURFACE, offsetField='',
                thicknessAssignment=FROM_SECTION)

            s = p.faces
            mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                        orientationType=GLOBAL, axis=AXIS_1,
                        additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='')

            elemType1 = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
            elemType2 = mesh.ElemType(elemCode=STRI65, elemLibrary=STANDARD)
            a = mdb.models['Model-1'].rootAssembly
            pickedRegions = regionToolset.Region(skinFaces=(('TopSkin', topFaces), ))
            a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
            pickedRegions = regionToolset.Region(skinFaces=(('BotSkin', botFaces), ))
            a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    def importAssembly(self):

        model = mdb.models['Model-1']
        p = model.parts['HW']
        a = model.rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        a.Instance(name='HW',
           part=p,
           dependent=OFF)
        e1 = a.instances['HW'].edges
        a.Set(name='prePartiti',
            edges=e1)

    def partitionRadii(self):
        file = 'HW'
        a = mdb.models['Model-1'].rootAssembly
        d = a.datums
        e1 = a.instances['HW'].edges
        f1 = a.instances['HW'].faces

        a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,
                             offset=200.0)
        edge1 = e1.getByBoundingBox(-6,82,100,100,83,149.5)
        t = a.MakeSketchTransform(sketchPlane=d.values()[1], sketchUpEdge=edge1[0],
            sketchPlaneSide=SIDE1, origin=(200.0, 0.0, 0.0))
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
            sheetSize=1520.48, gridSpacing=38.01, transform=t)
        g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        a.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.sketchOptions.setValues(gridOrigin=(0.0, 225.0))
        s.retrieveSketch(sketch=mdb.models['Model-1'].sketches['Sketch-1'])
        pickedFaces = f1

        a.PartitionFaceBySketchThruAll(sketchPlane=d.values()[1], sketchUpEdge=edge1[0],
                                       faces=pickedFaces, sketchPlaneSide=SIDE1, sketch=s)
        s.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']

    def partitionHorizontal(self,division,grid=0, angle=0):
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
        d1 = p.datums
        p.DatumPointByCoordinate((15,-50,306))
        p.DatumPointByCoordinate((14,-50,306))
        p.DatumAxisByTwoPoint(d1.values()[-2],d1.values()[-1])
        datumAxis = p.datums.values()[-1]
        datumPlanes = []

        if not grid:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=151)
            brimPlane = p.datums.values()[-1]

        for z in partitiondensity:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=z)
            if angle:
                p.DatumPlaneByRotation(plane=d1.values()[-1], axis=datumAxis, angle=angle)
            datumPlanes.append(p.datums.keys()[-1])

        if not grid:
            pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
            p.PartitionCellByDatumPlane(datumPlane=brimPlane, cells=pickedCells)
            brimCell = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, 151+tol)
            p.Set(cells=brimCell,name='Cell_Brim')

        for z in datumPlanes:
            pickedCells = cells.getByBoundingBox(-1000, -1000, 150-tol, 1000, 1000, Radius+tol)
            p.PartitionCellByDatumPlane(datumPlane=d1[z], cells=pickedCells)

        sortedIndeces = self.sortCells(angle)
        for i,cellIndex in enumerate(sortedIndeces):
            p.Set(cells=cells.findAt(cells[cellIndex].pointOn), name='Cell_'+str(i+1))
            self.sets.append('Cell_'+str(i+1))

    def sortCells(self,angle):
        p = mdb.models['Model-1'].parts['HW']
        distance = []
        pointA = np.array([-500,0])
        pointB = np.array([-500-np.cos(angle*180/np.pi),np.sin(angle*180/np.pi)])
        AB = pointB-pointA
        for cell in p.cells:
            pointC = np.array(cell.pointOn)[0]
            if pointC[2] > 151:
                xCoords, yCoords, zCoords = pointC
                AC = pointC[1:] - pointA
                distance.append(np.linalg.norm(np.cross(AC,AB))/np.linalg.norm(AB))
        sortedIndeces = sorted(range(len(distance)), key=lambda k: distance[k])
        return sortedIndeces

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
        p.Set(cells=pickedCells, name='Cell_brim')
        for z in datums.values()[1:]:
            pickedCells = cells.getByBoundingBox(-1000, ymin-tol, 150, 1000, ymax+tol,1000)
            p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
            if not grid:
                pickedCells = cells.getByBoundingBox(-1000, ymin+(i*splits)-tol, 150, 1000, ymin+((i+1)*splits)+tol,1000)
                p.Set(cells=pickedCells, name='Cell_'+str(i+1))
                self.sets.append('Cell_'+str(i+1))
            i += 1
        if not grid:
            pickedCells = cells.getByBoundingBox(-1000, ymin+(i*splits)-tol, 150, 1000, ymin+((i+1)*splits)+tol,1000)
            p.Set(cells=pickedCells, name='Cell_'+str(i+1))
            self.sets.append('Cell_'+str(i+1))

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
                    p.Set(cells=pickedCells, name='Cell_'+str(j+1)+str(i+1))
                    self.sets.append('Cell_'+str(j+1)+str(i+1))

    def assignSections(self,stiffSection,BronzeRatio=0):
        p = mdb.models['Model-1'].parts['HW']
        sets = p.sets
        self.createMaterials(BronzeRatio=BronzeRatio)
        for i in sets.keys():
            if i in stiffSection:
                if BronzeRatio < 1 and BronzeRatio > 0:
                    p.SectionAssignment(region=sets[i], sectionName='Foam', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)
                else:
                    p.SectionAssignment(region=sets[i], sectionName='Bronze', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)
            else:
                if i == 'Cell_Brim':
                    p.SectionAssignment(region=sets[i], sectionName='Foam', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)
                elif BronzeRatio < 1 and BronzeRatio > 0:
                    p.SectionAssignment(region=sets[i], sectionName='Bronze', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)
                else:
                    p.SectionAssignment(region=sets[i], sectionName='Foam', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)

    def removeSections(self):
        while mdb.models['Model-1'].parts['HW'].sectionAssignments:
            del mdb.models['Model-1'].parts['HW'].sectionAssignments[-1]

    def createMaterials(self,angle=0,angle2=0,CFratio=0,BronzeRatio=0):

        if CFratio >= 1:
            E1 = 130000
            E2 = E1/CFratio
        elif CFratio > 0:
            E2 = 130000
            E1 = E2/CFratio
        else:
            E1 = 130000
            E2 = 10000

        if BronzeRatio < 1 and BronzeRatio > 0:
                    ratio = 1/BronzeRatio
        else:
            ratio = BronzeRatio
        #-------------- Materials --------------------------------
        mdb.models['Model-1'].Material(name='CF')
        mdb.models['Model-1'].materials['CF'].Elastic(type=ENGINEERING_CONSTANTS,
        table=((E1, E2, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,3000.0), ))

        mdb.models['Model-1'].Material(name='CF2')
        mdb.models['Model-1'].materials['CF2'].Elastic(type=ENGINEERING_CONSTANTS,
        table=((E1, E2, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,3000.0), ))

        mdb.models['Model-1'].Material(name='Bronze')
        mdb.models['Model-1'].materials['Bronze'].Elastic(table=((115000.0, 0.34), ))

        if not BronzeRatio:
            mdb.models['Model-1'].Material(name='Foam')
            mdb.models['Model-1'].materials['Foam'].Elastic(table=((200.0, 0.3), ))

        else:
            mdb.models['Model-1'].Material(name='Foam')
            mdb.models['Model-1'].materials['Foam'].Elastic(table=((115000/ratio, 0.3), ))
        # -------------- Sections -----------------------------
        sectionLayer1 = section.SectionLayer(material='CF', thickness=1,
                                             orientAngle=angle, numIntPts=3, plyName='')
        mdb.models['Model-1'].CompositeShellSection(name='CF', preIntegrate=OFF,
                                                    idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                                                    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                                                    useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))


        sectionLayer1 = section.SectionLayer(material='CF2', thickness=1,
                                                 orientAngle=angle2, numIntPts=3, plyName='')
        mdb.models['Model-1'].CompositeShellSection(name='CF2', preIntegrate=OFF,
                                                        idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                                                        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                                                        useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

        mdb.models['Model-1'].HomogeneousSolidSection(name='Bronze', material='Bronze',
                                                      thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Foam', material='Foam',
                                                      thickness=None)

    def deleteMaterials(self):
        for material in mdb.models['Model-1'].materials.keys():
            del mdb.models['Model-1'].materials[material]
        for section in mdb.models['Model-1'].sections.keys():
            del mdb.models['Model-1'].sections[section]
        for skin in mdb.models['Model-1'].parts['HW'].skins.keys():
            del mdb.models['Model-1'].parts['HW'].skins[skin]
        while mdb.models['Model-1'].parts['HW'].sectionAssignments:
            del mdb.models['Model-1'].parts['HW'].sectionAssignments[-1]
        while mdb.models['Model-1'].parts['HW'].materialOrientations:
            del mdb.models['Model-1'].parts['HW'].materialOrientations[-1]

    def mesh(self,meshSize):
        r = self.r
        r_val = self.r_val
        tol = 0.01
        model = mdb.models['Model-1']
        a = model.rootAssembly
        partInstances =(a.instances['HW'], )

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

    def createSets(self):
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances['HW'].edges
        r_val = self.r_val
        r = self.r
        tol = 0.1

        a.Set(name='postPartiti',
            edges=e1)

        a.SetByBoolean(name='r_edges',
               sets=(a.sets['postPartiti'],
                     a.sets['prePartiti']),
               operation=DIFFERENCE)

        r_name = [] # Used throughout the script to name sets
        set_name = []
        for i in range(len(r_val)):
            r_name.append('R_'+str(r_val[i])[2:])
            set_name.append('PROFILE-'+r_name[i])

        for i in range(len(r_name)):
            edges = e1.getByBoundingBox(-1000, -1000, r_val[i]*r-tol, 1000, 1000, r_val[i]*r+tol)
            a.Set(edges=edges,
                  name='Area')
            a.SetByBoolean(name=set_name[i],
                           sets=(a.sets['Area'], a.sets['r_edges']),
                           operation=INTERSECTION)

            del a.sets['Area']
        del a.sets['r_edges']
        del a.sets['postPartiti']
        del a.sets['prePartiti']

    def applyLoad(self,field):
        model = mdb.models['Model-1']

        a = model.rootAssembly
        s1 = a.instances['HW'].faces
        region = a.Surface(side1Faces=s1, name='Surf-1')
        model.Pressure(name='Load-1',
                       createStepName='Step-1',
                       region=region,
                       distributionType=FIELD,
                       field=field,
                       magnitude=1.0,
                       amplitude=UNSET)

        d1 = a.datums
        a.AttachmentPoints(name='Attachment Points-1', points=(d1.values()[0].origin, ),
            setName='Attachment Points-1-Set-1')
        v1 = a.vertices
        verts1 = v1.getByBoundingBox(-1,-1,-1,1,1,1)
        region1=a.Set(vertices=verts1, name='m_Set-14')
        s1 = a.instances['HW'].faces
        side1Faces1 = s1.getByBoundingBox(-100, -150, 98, 100, 100, 102)
        region2=a.Surface(side1Faces=side1Faces1, name='BC_Surf-1')
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

    def writeInput(self,*args):
        name = 'HW_'
        for arg in args:
            name += str(arg) + '_'
        name = name[:-1]
        print(name)
        mdb.Job(name=name, model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numGPUs=0)
        mdb.jobs[name].writeInput(consistencyChecking=OFF)

    def createFolder(self,path=''):
        os.chdir(self.input_file_path)
        if not path:
            input_file_location = self.input_file_path
            input_folder_name = getInput('Enter name for folder containing input files: ')
            self.input_file_path += '/' + input_folder_name
            self.partitionName = input_folder_name
        else:
            input_folder_name = path
        if not os.path.exists(input_folder_name):
            os.mkdir(input_folder_name)
            print("Directory " , input_folder_name ,  " Created ")
            os.chdir(input_folder_name)
        else:
            print("Directory " , input_folder_name ,  " already exists")
            sys.exit()

    def createBatch(self):
        current=os.getcwd()
        print(current+'\\')
        # Hent
        odb_names = [f for f in os.listdir(current) if (f.endswith('.inp')) ]
        s=open(current+'\\'+'run_inputs.bat',"w+")
        for od in odb_names:
            s.write('call abq2017 job='+od[:-4]+ ' int\n')
        s.close()


caeFilePath = 'C:/Users/Jon/Documents/Abaqus/HW.cae'
inputFileLocation = 'C:/Users/Jon/OneDrive/FleksProp/InputFiles'


ratios = [1000., 100., 30., 10., 1.]
ratioNames = ['R1000','R100', 'R30', 'R10', 'R1']
angles = [0,30,45,60,90,120,135,150]

fields = ['Seven-','Seven+']

"""
# ------------- Grid, Vertical & Horizontal ----------------------
propeller = HydroWing(caeFilePath,inputFileLocation)

propeller.createFolder()
for field in fields:
    propeller.openCAE()
    propeller.partitionVertical(10)
    propeller.importAssembly()
    propeller.partitionRadii()
    propeller.createFolder(propeller.input_file_path+'/'+field)
    propeller.applyLoad(field)
    propeller.mesh(8)
    propeller.createSets()
    setList = []

    for angle in angles:
        propeller.createFolder(propeller.input_file_path+'/'+field+'/'+'Angle'+str(angle))
        for i,ratio in enumerate(ratios):
            propeller.createFolder(propeller.input_file_path+'/'+field+'/'+'Angle'+str(angle)+'/'+ratioNames[i])
            for set in propeller.sets:
                #setList.append(set)
                propeller.assignSections([set],BronzeRatio=ratio)
                propeller.writeInput(propeller.partitionName,field,'Angle'+str(angle),ratioNames[i],set)
                propeller.deleteMaterials()
            propeller.createBatch()
    mdb.close()
"""
"""
# -------------------- TopBot --------------------------
propeller = HydroWing(caeFilePath,inputFileLocation)
propeller.openCAE()
propeller.createFolder('TopBot-7+')
propeller.partitionName = 'TopBot-7+'
propeller.input_file_path += '/TopBot-7+/'
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad('Seven+')
propeller.mesh(8)
propeller.createSets()

for angle in np.linspace(-90,90,10):
    propeller.createFolder('TopDeg_'+str(int(angle)))
    for angle2 in np.linspace(-90,90,10):
        propeller.createMaterials(angle=angle,angle2=angle2)
        propeller.all_over(bothSides=1)
        propeller.writeInput(propeller.partitionName,'TopDeg',str(int(angle)),'BotDeg',str(int(angle2)))
        propeller.deleteMaterials()
propeller.createBatch()
"""
"""
# -------------------- AllOver --------------------------
propeller = HydroWing(caeFilePath,inputFileLocation)
propeller.openCAE()
propeller.createFolder('AllOver-7+')
propeller.partitionName = 'AllOver-7+'
propeller.input_file_path += '/AllOver-7+/'
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad('Seven+')
propeller.mesh(8)
propeller.createSets()

for angle in np.linspace(-90,90,10):
    propeller.createFolder('Angle_'+str(int(angle)))
    for i,ratio in enumerate(ratios):
        propeller.createMaterials(angle=angle, CFratio=ratio)
        propeller.all_over()
        propeller.writeInput(propeller.partitionName,'Angle',str(int(angle)),ratioNames[i])
        propeller.deleteMaterials()
propeller.createBatch()
"""
"""
# ----------------------- Mesh Convergence -------------------------------

meshList = [100,75,50,35,25,15,12,10,8,6]

propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.createFolder()
for meshSize in meshList:
    propeller.openCAE()
    propeller.importAssembly()
    propeller.partitionRadii()
    propeller.applyLoad()
    propeller.mesh(meshSize)
    propeller.createSets()
    propeller.createMaterials()
    p = mdb.models['Model-1'].parts['HW']
    p.Set(name='Set10', cells=p.cells)
    p.SectionAssignment(region=p.sets['Set10'], sectionName='Foam', offset=0.0,
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)
    propeller.writeInput(propeller.partitionName,meshSize)
    mdb.close()
propeller.createBatch()

"""

"""
# ------------- Centered Sweeps ----------------------
propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.openCAE()
propeller.createFolder()
propeller.partitionVertical(10)
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad()
propeller.mesh(8)
propeller.createSets()
setList = []
middle = len(propeller.sets)/2

for shift in range(5):
    setList.append(propeller.sets[middle+shift])
    setList.append(propeller.sets[middle-1-shift])
    propeller.assignSections(setList)
    propeller.writeInput(propeller.partitionName,'+-',shift)
    propeller.removeSections()
propeller.createBatch()
"""
