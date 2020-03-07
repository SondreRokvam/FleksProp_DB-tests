from abaqus import *
from abaqus import getInput
from abaqus import getInputs
from abaqusConstants import *
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

def SweepAssignSectionHorizontal():

    #Definitions
    Mdb()  # Clear all

    # ------------Import stp File - ----------------------------
    #step = mdb.openStep(
    #    'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Propeller_3D-files .prt .stp .iges/Azp65C-PB_no_Fillet_Solid.stp',
    #    scaleFromFile=OFF)
    #mdb.models['Model-1'].PartFromGeometryFile(name='Azp65C-PB_NFR_Solid',
    #                                           geometryFile=step, combine=False, retainBoundary=True,
    #                                           mergeSolidRegions=True, dimensionality=THREE_D, type=DEFORMABLE_BODY)

    openMdb(pathName='C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/Script-fra-masterstudentene/Lukas_DivideC/Azp65C-PB_NFR_Solid.cae')
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    p = mdb.models['Model-1'].parts['Azp65C-PB_NFR_Solid']
    #del koad #rand varible for stopping the code


    #---------- Specifying Partition Density -----------------------------

    partitiondensity = []
    Radius = 650   # Later make this a user defined input
    division = 10  # Later make this a user defined input.
    splits = (Radius-(Radius*0.1))/division
    startpart = (Radius*0.1)+splits
    for y in range(int(startpart),Radius,int(splits)):
        partitiondensity.append(y)

    # ------------Creating Horizontal Partitions- -----------------------

    c1 = p.cells
    for x in partitiondensity:
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-x)
    d1 = p.datums
    print(d1)
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
            cells = c.getByBoundingBox(-1000, -(startpart+(s1*splits)+5), -1000, 1000, -(startpart+(s2*splits)-5), 1000)
            p.Set(cells=cells, name='Set-'+str(s1))

    # ----------------Assign sweep of sections----------------------------------------
def assignsectionsweep():
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



SweepAssignSectionHorizontal()
assignsectionsweep()
