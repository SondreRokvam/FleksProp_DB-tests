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
from abaqus import *
from abaqus import getInput
from abaqus import getInputs
from abaqusConstants import *


openMdb(
        pathName='C:/Users/lmark/Documents/NTNU/TMM4960-Masters Thesis Project/FEA files/AZP65C/Abaqus/AZP65C/Azp65C_SolidVerticalPartition/Azp65C-PB_NFR_Solid.cae')
p = mdb.models['Model-1'].parts['Azp65C-PB_NFR_Solid']

tol = 5 # -- Tolerance value used throughout all functions. DO NOT DELETE
def SweepAssignSectionHorizontal(division):

    #---------- Specifying Partition Density Horizontal -----------------------------
    partitiondensity = []
    Radius = 650   # Later make this a user defined input
    #division = 3  # Later make this a user defined input.
    splits = (Radius-(Radius*0.1))/division
    startpart = (Radius*0.1)+splits
    for y in range(int(startpart),int(Radius-tol),int(splits)):
        partitiondensity.append(y)

    # ------------Creating Horizontal Partitions- -----------------------

    c1 = p.cells
    for x in partitiondensity:
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-x)
    d1 = p.datums
    #print(d1)
    for z in range(2,len(d1)+2,1):
        if z == 2:
            pickedCells = c1.getByBoundingBox(-1000,-int(Radius),-1000,1000,Radius,1000)
            p.PartitionCellByDatumPlane(datumPlane=d1[z], cells=pickedCells)
        elif z > 2:
            pickedCells = c1.getByBoundingBox(-1000, -Radius, -1000, 1000, 0+((z-2)*splits), 1000)
            p.PartitionCellByDatumPlane(datumPlane=d1[z], cells=pickedCells)


    # ----------------------Create Section --------------------------------------------

    # Create Material
    Materials = [1,2]
    Mat = ['Foam','Steel']
    Modulus = [3000.0,200000.0]

    for i in range(0,len(Materials),1):
        mdb.models['Model-1'].Material(name=Mat[i])
        mdb.models['Model-1'].materials[Mat[i]].Elastic(table=((Modulus[i], 0.3),))

    sectionnames = []
    #Create Section
    for m1 in range(0,len(Materials),1):
        mdb.models['Model-1'].HomogeneousSolidSection(name=Mat[m1], material=Mat[m1],
                                                  thickness=None)
        sectionnames.append(str(Mat[m1]))

    #----------------------Assign Section--------------------------------------------------
    # --- Create Sets----
    Setnames = []
    c = p.cells
    for s1 in range(0,len(d1)+1,1):
        s2 = s1-1
        Setnames.insert(0,'Set-'+str(s1))
        if s1 == 0:
            cells = c.getByBoundingBox(-1000, -startpart, -1000, 1000, s1*splits, 1000)
            p.Set(cells=cells, name='Set-'+str(s1))
        elif s1 > 0:
            cells = c.getByBoundingBox(-1000, -(startpart+(s1*splits)+tol), -1000, 1000, -(startpart+(s2*splits)-5), 1000)
            p.Set(cells=cells, name='Set-'+str(s1))

    session.viewports['Viewport: 1'].setValues(displayedObject=p)


def SweepAssignSectionVertical(division):
    p = mdb.models['Model-1'].parts['Azp65C-PB_NFR_Solid']

    # ---------- Specifying Partition Density Vertical -----------------------------

    partitiondensityv = []
    maxwidth = 300  # Later make this a user defined input
    minwidth = -125  # Later make this a user defined input
    rangev = maxwidth-minwidth
    #division = 3
    splitsv = rangev/division
    startpartv = minwidth + splitsv
    for y1 in range(int(startpartv), (maxwidth-splitsv), int(splitsv)):
        partitiondensityv.append(y1)

    # ------------Creating Vertical Partitions- -----------------------

    d2 = p.datums
    tol = 5
    c2 = p.cells
    for xv in partitiondensityv:
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=xv)
        print(d2)
    for yv in range(2, len(d2)+2, 1):
        z11 = yv-2
        if yv == 2:
            pickedCellsz = c2.getByBoundingBox(-1000, -1000, -1000, 1000, 0, 1000)
            p.PartitionCellByDatumPlane(datumPlane=d2[yv], cells=pickedCellsz)
        elif yv > 2:
            pickedCellsz = c2.getByBoundingBox(-1000, -1000, minwidth+(z11*splitsv)-20, 1000, 0, 1000)
            p.PartitionCellByDatumPlane(datumPlane=d2[yv], cells=pickedCellsz)

        # ----------------------Create Section Vertical --------------------------------------------

    # Create Material
    Materials = [1, 2]
    Mat = ['Foam', 'Steel']
    Modulus = [3000.0, 200000.0]

    for i in range(0, len(Materials), 1):
        mdb.models['Model-1'].Material(name=Mat[i])
        mdb.models['Model-1'].materials[Mat[i]].Elastic(table=((Modulus[i], 0.3),))

    sectionnames = []
    # Create Section
    for m1 in range(0, len(Materials), 1):
        mdb.models['Model-1'].HomogeneousSolidSection(name=Mat[m1], material=Mat[m1],
                                                      thickness=None)
        sectionnames.append(str(Mat[m1]))

    # ----------------------Assign Section Vertical --------------------------------------------------
    # --- Create Sets----
    Setnamesv = []
    c = p.cells
    for s1v in range(0, len(d2) + 1, 1):
        s2v = s1v - 1
        Setnamesv.insert(0, 'Set-' + str(s1v))
        if s1v == 0:
            cellsz = c2.getByBoundingBox(-1000, -1000, -1000, 1000, 1000, startpartv+tol)
            p.Set(cells=cellsz, name='Set-'+ str(s1v))
        elif s1v > 0:
            cellsz = c2.getByBoundingBox(-1000, -1000, startpartv+(s2v*splitsv)-tol, 1000, 0, startpartv+(s1v*splitsv)+tol)
            p.Set(cells=cellsz, name='Set-'+ str(s1v))
    session.viewports['Viewport: 1'].setValues(displayedObject=p)


def SweepAssignSectionFan():

    #------------------ Create Reference Planes ----------------------
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
    d = p.datums
    p.DatumAxisByTwoPlane(plane1=d[35], plane2=d[34]) # change the variables called from datum plane list
    d1 = p.datums
    p.DatumPlaneByRotation(plane=d1[34], axis=d1[36], angle=45.0) # change the variables calling from datum plane list
    p.DatumPlaneByRotation(plane=d1[38], axis=d1[36], angle=90.0)
    p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
    p.DatumAxisByTwoPlane(plane1=d1[41], plane2=d1[40])

    #------------ Setting Angle Limits ------------------------------
    alpha1 = -32
    alpha2 = 65
    rangeangles = alpha2 - alpha1
    numcells = 10
    dist = rangeangles/numcells

    #------------- Create Datum planes for fan partitions -----------------

    for alpha in range(alpha1, alpha2, int(dist)):
        p.DatumPlaneByRotation(plane=d2[40], axis=d2[42], angle=alpha)

    # ------- Partitioning Fan - ---------------------
    d3 = p.datums
    for a1 in range(2,10,1):
        c = p.cells
        for f in range(1,2,3):
            pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
            p.PartitionCellByDatumPlane(datumPlane=d3[43], cells=pickedCells)
    session.viewports['Viewport: 1'].setValues(displayedObject=p)


def SweepAssignSectionGrid(division):

    # -------- Using previous set of code to make a grid --------------
    #### ---------Horizontal Lines------------####
    ### ------ Partition Density ----------- ####

    partitiondensity = []
    tol = 5
    Radius = 650  # Later make this a user defined input
    #division = 5  # Later make this a user defined input.
    splits = (Radius - (Radius * 0.1)) / division
    startpart = (Radius * 0.1) + splits
    endpart = Radius - splits
    for y in range(int(startpart), int(Radius-tol), int(splits)):
        partitiondensity.append(y)

    # ------------Creating Horizontal Partitions- -----------------------

    c1 = p.cells
    for x in partitiondensity:
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-x)
    d1 = p.datums
    #print(d1)
    for z in range(2, len(d1) + 2, 1):
        if z == 2:
            pickedCells = c1.getByBoundingBox(-1000, -int(Radius), -1000, 1000, Radius, 1000)
            p.PartitionCellByDatumPlane(datumPlane=d1[z], cells=pickedCells)
        elif z > 2:
            pickedCells = c1.getByBoundingBox(-1000, -Radius, -1000, 1000, 0 + ((z - 2) * splits), 1000)
            p.PartitionCellByDatumPlane(datumPlane=d1[z], cells=pickedCells)

    # ###############--------------- Vertical Partitions-------------------------#################
    #### Assigning Density of Partitions Vertical #####

    partitiondensityv = []
    maxwidth = 300  # Later make this a user defined input
    minwidth = -125  # Later make this a user defined input
    rangev = maxwidth - minwidth
    splitsv = rangev / division
    startpartv = minwidth + splitsv
    for y1 in range(int(startpartv), int(maxwidth-tol), int(splitsv)):
        partitiondensityv.append(y1)

    # ------------Creating Vertical Partitions- -----------------------

    d2 = p.datums
    c2 = p.cells
    for xv in partitiondensityv:
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=xv)
        #print(d2)
        #print(len(d2))
        s11 = division-1
        startnumb = 1+(s11*2)+1  # Used to define the counting of the next Datum plane objects
        #print(startnumb)
        s22 = division-1
        endnumb = startnumb+(s22) # Used to define the number of the last Datum plane object
        #print(endnumb)
    for yv in range(startnumb, endnumb, 1):
        z11 = yv - startnumb-1
        if yv == startnumb:
            #print(yv)
            pickedCellsz = c2.getByBoundingBox(-1000, -1000, -1000, 1000, 0, 1000)
            p.PartitionCellByDatumPlane(datumPlane=d2[yv], cells=pickedCellsz)
        elif yv > startnumb:
            pickedCellsz = c2.getByBoundingBox(-1000, -1000, startpartv + (z11 * splitsv) - 20, 1000, 0, 1000)
            p.PartitionCellByDatumPlane(datumPlane=d2[yv], cells=pickedCellsz)

    #------------ Assign Materials ------#

        # Create Material
        Materials = [1, 2]
        Mat = ['Foam', 'Steel']
        Modulus = [3000.0, 200000.0]

        for i in range(0, len(Materials), 1):
            mdb.models['Model-1'].Material(name=Mat[i])
            mdb.models['Model-1'].materials[Mat[i]].Elastic(table=((Modulus[i], 0.3),))

    # ------------Assigning Sets to All Cells -------------##
session.viewports['Viewport: 1'].setValues(displayedObject=p)


def assignsectionsweep():   # --This code only works with vertical and horizontal partitioning
    Sections = sectionnames
    Sets = Setnames

    n = 0  # Loop counter
    d = []
    previousset = []

    for y in range(0, len(Sets), 1):
        currentset = Sets[y]
        for x in Sets:
            Jobb = ['Test' + str(n)]  # Job label maker
            d.insert(0, Jobb)
            region = p.sets[x]
            if x == currentset:
                section = Sections[1]
            elif x in previousset:
                section = Sections[1]
            else:
                section = Sections[0]
            region = p.sets[x]
            p.SectionAssignment(region=region, sectionName=section, offset=0.0,
                                offsetType=TOP_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)

        mdb.Job(name=Jobb[0], model='Model-1', description='', type=ANALYSIS,
                atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                numGPUs=0)
        mdb.jobs[Jobb[0]].writeInput(consistencyChecking=OFF)  # Creating job .inp file
        n = n + 1  # Loop Counter
        previousset.insert(y, Sets[y])
        print(previousset)
        for s in range(0, len(Sets), 1):  # Remove previous loop section assignments
            del mdb.models['Model-1'].parts['Azp65C-PB_NFR_Solid'].sectionAssignments[0]


#-----------Receive input from user on type of partition pattern ----------#

reply = getInput('SELECT PARTITION METHOD (HORIZONTAL, VERTICAL, FAN(UNDER CONST), GRID(CELLS NOT ASSIGNED)):')
if reply == 'HORIZONTAL':
    reply2 = getInput('Specify Partition Density (2,3...)')
    if reply2>1:
        SweepAssignSectionHorizontal(int(reply2))
    else:
        print('You are a moron')
elif reply == 'VERTICAL':
    reply2 = getInput('Specify Partition Density (2,3...)')
    if reply2 > 1:
        SweepAssignSectionVertical(int(reply2))
    else:
        print('You are a moron')
elif reply == FAN:
        print('You are a moron')
elif reply == 'GRID':
    reply2 = getInput('Specify Partition Density (2,3...)')
    if reply2 > 1:
        SweepAssignSectionGrid(int(reply2))
    else:
        print('You are a moron')
else:
    print(wrong)

