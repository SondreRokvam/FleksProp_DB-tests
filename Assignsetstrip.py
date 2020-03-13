
from abaqus import *
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
import time



def assignstrip():

    p = mdb.models['Model-1'].parts['Azp65C-Propeller-partitioned-ver']
    Sections = ['Foam', 'Aluminium']
    Sets = ['Set-1', 'Set-2', 'Set-3', 'Set-4', 'Set-5', 'Set-6', 'Set-7', 'Set-8', 'Set-9', 'Set-10', 'Set-11',
            'Set-12', 'Set-13', 'Set-14', 'Set-15', 'Set-16']

    for set in range(0, len(Sets)):
        Jobb = 'Job-' + str(set)
        for s in Sets:
            currentset = 'Set-'+str(set+1)
            if s == currentset:
                section = Sections[1]
            else:
                section = Sections[0]
            region = p.sets[s]
            p.SectionAssignment(region=region, sectionName=section, offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
        mdb.Job(name=Jobb, model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numGPUs=0)
        mdb.jobs[Jobb].writeInput(consistencyChecking=OFF)  # Creating job .inp file
        for s in range(0,len(Sets)):  # Remove previous loop section assignments
            del mdb.models['Model-1'].parts['Azp65C-Propeller-partitioned-ver'].sectionAssignments[0]


assignstrip()
