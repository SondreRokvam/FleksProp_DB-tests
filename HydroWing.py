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
<<<<<<< Updated upstream
    def __init__(self, cae_file_path,input_file_path,load_file_path):
        self.cae_file_path = cae_file_path
        self.input_file_path = input_file_path
        self.load_file_path = load_file_path
        self.r = 500
        self.r_val = [0.5, 0.6, 0.7, 0.8, 0.9]
=======
    def __init__(self, cae_file_path, input_file_path):
        self.cae_file_path = cae_file_path
        self.input_file_path = input_file_path
        self.r = 500
        self.r_val = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
>>>>>>> Stashed changes
        self.partition_set_names = []

    def openCAE(self):
        openMdb(self.cae_file_path)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def all_over(self, angles, thickness):
=======
    def all_over(self, thickness=0.2):
        try:
            p = mdb.models['Model-1'].parts['HW']

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

            # ----------------- Skin Mesh ----------------------------------------

            elemType1 = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
            elemType2 = mesh.ElemType(elemCode=STRI65, elemLibrary=STANDARD)
            a = mdb.models['Model-1'].rootAssembly
            f1 = a.instances['HW-1'].faces
            pickedRegions = regionToolset.Region(skinFaces=(('Skin-1', f1), ))
            a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))


        except:
            pass
=======
=======
>>>>>>> Stashed changes
    def all_over(self, thickness=0.2):
        p = mdb.models['Model-1'].parts['HW']

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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    def partitionHorizontal(self,division,grid=0):
=======
    def partitionHorizontal(self,division,grid=0, angle=0):
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
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
            p.Set(cells=pickedCells, name='Cell_Brim')
            for z in d1.values()[1:]:
                pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
                p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
                pickedCells = cells.getByBoundingBox(-1000, -1000 , 150+(i*splits)-tol, 1000, 1000 , 150+((i+1)*splits)+tol)
                p.Set(cells=pickedCells, name='Cell_'+str(i+1))
                self.sets.append('Cell_'+str(i+1))
                i += 1
            pickedCells = cells.getByBoundingBox(-1000, -1000 , 150+i*splits-tol, 1000, 1000 , Radius+tol)
            p.Set(cells=pickedCells, name='Cell_'+str(i+1))
            self.sets.append('Cell_'+str(i+1))
        else:
            for z in d1.values()[division:]:
                pickedCells = cells.getByBoundingBox(-1000, -1000, 0, 1000, 1000, Radius+tol)
                p.PartitionCellByDatumPlane(datumPlane=z, cells=pickedCells)
                i += 1
=======
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
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    def assignSections(self,stiffSection):
        p = mdb.models['Model-1'].parts['HW']
        sets = p.sets
        self.createMaterials()
        for i in sets.keys():
<<<<<<< Updated upstream
            if i == stiffSection:
=======
            if i in stiffSection:
>>>>>>> Stashed changes
                p.SectionAssignment(region=sets[i], sectionName='Steel', offset=0.0,
                                offsetType=TOP_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            else:
                p.SectionAssignment(region=sets[i], sectionName='Foam', offset=0.0,
=======
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
>>>>>>> Stashed changes
                                    offsetType=TOP_SURFACE, offsetField='',
                                    thicknessAssignment=FROM_SECTION)

    def removeSections(self):
        while mdb.models['Model-1'].parts['HW'].sectionAssignments:
            del mdb.models['Model-1'].parts['HW'].sectionAssignments[-1]

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def createMaterials(self,angle=0):
=======
    def createMaterials(self,angle=0,ratio=0):

        if ratio >= 1:
            E1 = 130000
            E2 = E1/ratio

        elif ratio > 0:
            E2 = 130000
            E1 = E2/ratio
        else:
            E1 = 130000
            E2 = 10000
>>>>>>> Stashed changes

        #-------------- Materials --------------------------------
        mdb.models['Model-1'].Material(name='CF')
        mdb.models['Model-1'].materials['CF'].Elastic(type=ENGINEERING_CONSTANTS,
<<<<<<< Updated upstream
        table=((130000.0, 10000.0, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,3000.0), ))
=======
        table=((E1, E2, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,3000.0), ))
>>>>>>> Stashed changes

        mdb.models['Model-1'].Material(name='Steel')
        mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000.0, 0.3), ))

        mdb.models['Model-1'].Material(name='Foam')
        mdb.models['Model-1'].materials['Foam'].Elastic(table=((200.0, 0.3), ))

=======
    def createMaterials(self,angle=0,CFratio=0,BronzeRatio=0):

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

        mdb.models['Model-1'].Material(name='Bronze')
        mdb.models['Model-1'].materials['Bronze'].Elastic(table=((115000.0, 0.34), ))

        if not BronzeRatio:
            mdb.models['Model-1'].Material(name='Foam')
            mdb.models['Model-1'].materials['Foam'].Elastic(table=((200.0, 0.3), ))

        else:
            mdb.models['Model-1'].Material(name='Foam')
            mdb.models['Model-1'].materials['Foam'].Elastic(table=((115000/ratio, 0.3), ))
>>>>>>> Stashed changes
        # -------------- Sections -----------------------------
        sectionLayer1 = section.SectionLayer(material='CF', thickness=0.2,
                                             orientAngle=angle, numIntPts=3, plyName='')
        mdb.models['Model-1'].CompositeShellSection(name='CF', preIntegrate=OFF,
                                                    idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                                                    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                                                    useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

<<<<<<< Updated upstream
        mdb.models['Model-1'].HomogeneousSolidSection(name='Steel', material='Steel',
=======
        mdb.models['Model-1'].HomogeneousSolidSection(name='Bronze', material='Bronze',
>>>>>>> Stashed changes
                                                      thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Foam', material='Foam',
                                                      thickness=None)

    def deleteMaterials(self):
        for material in mdb.models['Model-1'].materials.keys():
            del mdb.models['Model-1'].materials[material]
        for section in mdb.models['Model-1'].sections.keys():
            del mdb.models['Model-1'].sections[section]
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
        for skin in mdb.models['Model-1'].parts['HW'].skins.keys():
            del mdb.models['Model-1'].parts['HW'].skins[skin]
        while mdb.models['Model-1'].parts['HW'].sectionAssignments:
            del mdb.models['Model-1'].parts['HW'].sectionAssignments[-1]
        while mdb.models['Model-1'].parts['HW'].materialOrientations:
            del mdb.models['Model-1'].parts['HW'].materialOrientations[-1]
<<<<<<< Updated upstream
>>>>>>> Stashed changes

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
=======
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    def applyLoad(self):
=======
    def applyLoad(self,field):
>>>>>>> Stashed changes
        model = mdb.models['Model-1']

        a = model.rootAssembly
        s1 = a.instances['HW'].faces
        region = a.Surface(side1Faces=s1, name='Surf-1')
        model.Pressure(name='Load-1',
                       createStepName='Step-1',
                       region=region,
                       distributionType=FIELD,
<<<<<<< Updated upstream
                       field='AnalyticalField-1',
=======
                       field=field,
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        name = 'HW-'
        for arg in args:
            name += str(arg) + '-'
=======
        name = 'HW_'
        for arg in args:
            name += str(arg) + '_'
>>>>>>> Stashed changes
=======
        name = 'HW_'
        for arg in args:
            name += str(arg) + '_'
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    def createFolder(self):
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        input_file_location = self.input_file_path
        os.chdir(input_file_location)
        input_folder_name = getInput('Enter name for folder containing input files: ')
        self.input_file_path += '\\' + input_folder_name
=======
    def createFolder(self,name=''):
        os.chdir(self.input_file_path)
        if not name:
            input_file_location = self.input_file_path
            input_folder_name = getInput('Enter name for folder containing input files: ')
            self.input_file_path += '\\' + input_folder_name
            self.partitionName = input_folder_name
        else:
            input_folder_name = name
>>>>>>> Stashed changes
        if not os.path.exists(input_folder_name):
            os.mkdir(input_folder_name)
            print("Directory " , input_folder_name ,  " Created ")
            os.chdir(input_folder_name)
        else:
            print("Directory " , input_folder_name ,  " already exists")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
=======
            sys.exit()
        self.partitionName = getInput('Enter name for simulation series: ')

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

"""
# ------------- Grid, Vertical & Horizontal ----------------------
propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.openCAE()
propeller.createFolder()
propeller.partitionHorizontal(10)
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad()
propeller.mesh(8)
propeller.createSets()

for set in propeller.sets:
    propeller.assignSections(set)
    propeller.writeInput(propeller.partitionName,set)
    propeller.removeSections()
propeller.createBatch()
"""


# -------------------- All Over --------------------------
propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.openCAE()
propeller.createFolder()
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad()
propeller.mesh(8)
propeller.createSets()

for angle in np.linspace(-90,90,20):
    propeller.createMaterials(angle)
    propeller.all_over(thickness=0.2)
    propeller.writeInput(propeller.partitionName,int(angle))
    propeller.deleteMaterials()
    propeller.removeSections()
propeller.createBatch()
>>>>>>> Stashed changes
=======
            sys.exit()
        self.partitionName = getInput('Enter name for simulation series: ')

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

ratios = [100., 75., 50., 25., 10., 1., 1/10., 1/25., 1/50., 1/75., 1/100.]
ratios.reverse()
"""
sweep = 0
reverse = 0

# ------------- Grid, Vertical & Horizontal ----------------------
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
for set in propeller.sets:
    #setList = [set]
    #print(setList)
    #propeller.assignSections(setList)
    print(set)
    propeller.assignSections(set)
    propeller.writeInput(propeller.partitionName,set)
    propeller.removeSections()
propeller.createBatch()
"""


# -------------------- All Over --------------------------
propeller = HydroWing(caeFilePath,inputFileLocation,pressure_field_path)
propeller.openCAE()
propeller.createFolder()
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad()
propeller.mesh(8)
propeller.createSets()

for angle in np.linspace(-90,90,10):
    for ratio in ratios:
        if ratio < 1:
            ratioTxt = '0_'+str(ratio)[2:4]
        else:
            ratioTxt = int(ratio)
        propeller.createMaterials(angle,ratio)
        propeller.all_over(thickness=0.2)
        propeller.writeInput(propeller.partitionName,'Angle',str(int(angle)),'R',ratioTxt)
        propeller.deleteMaterials()
propeller.createBatch()


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
>>>>>>> Stashed changes
=======
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


caeFilePath = 'C:\Users\Jon\Documents\Abaqus\HW.cae'
inputFileLocation = 'C:\Users\Jon\OneDrive\FleksProp\InputFiles'


ratios = [1000, 100., 10., 1/10., 1/100., 1/1000]
ratioNames = ['1000', '100', '10', '0_1', '0_01', '0_001']
angles = [0,30,45,60,90,120,135,150]

fields = ['Seven-','Seven+']

"""
# ------------- Grid, Vertical & Horizontal ----------------------
propeller = HydroWing(caeFilePath,inputFileLocation)

propeller.createFolder()
for field in fields:
    propeller.openCAE()
    propeller.partitionHorizontal(10)
    propeller.importAssembly()
    propeller.partitionRadii()
    propeller.createFolder(field)
    propeller.applyLoad(field)
    propeller.mesh(8)
    propeller.createSets()
    setList = []

    for set in propeller.sets:
        setList.append(set)
        propeller.assignSections(setList)
        propeller.writeInput(propeller.partitionName,field,set)
        propeller.deleteMaterials()
    mdb.close()
    propeller.createBatch()
"""


# -------------------- All Over --------------------------
propeller = HydroWing(caeFilePath,inputFileLocation)
propeller.openCAE()
propeller.createFolder()
propeller.partitionName = 'AllOver'
propeller.importAssembly()
propeller.partitionRadii()
propeller.applyLoad('Seven-')
propeller.mesh(8)
propeller.createSets()

for angle in np.linspace(-90,90,10):
    propeller.createFolder(str(angle))
    for ratio in ratios:
        if ratio < 1:
            ratioTxt = '0_'+str(ratio)[2:4]
        else:
            ratioTxt = int(ratio)
        propeller.createMaterials(angle,ratio)
        propeller.all_over(thickness=0.2)
        propeller.writeInput(propeller.partitionName,'Seven-','Angle',str(int(angle)),'R',ratioTxt)
        propeller.deleteMaterials()
propeller.createBatch()


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
>>>>>>> Stashed changes
