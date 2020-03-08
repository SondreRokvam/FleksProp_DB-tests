if True:
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
""" Test Parameters """
if True:
    stepOrCAEimport =['step','CAE']
    propellerTypes = ['HW', 'AzP65C']
    partitionMethods = ['Fan', 'Grid', 'Horizontal', 'Vertical']
    shellOrSolidTest = ['Shell','Solid']
    faceOrcellTest = ['face','cell']
    sides = ['P','S']

    filTyp = 1
    proptype = 1
    partMeth = 0
    shellOrSolid = 0
    faceOrcell = 0
    side= 0
    if 1:   #Bare skjules
        stepOrCAEimport = stepOrCAEimport[filTyp]
        propellerTypes = propellerTypes[proptype]
        partitionMethods = partitionMethods[partMeth]
        shellOrSolidTest = shellOrSolidTest[shellOrSolid]
        faceOrcellTest = faceOrcellTest[faceOrcell]
        sides = sides[side]
        if propellerTypes=='HW':
            r=500
            name= 'HW'
            if shellOrSolidTest=='Shell':
                name= name+'Shell'
            else:
                name = name + 'Solid'
        if propellerTypes=='AzP65C':
            r=650
            name = 'Azp65C-PB_no_Fillet_Shell'
            if shellOrSolidTest=='Shell':
                name= name+'Shell'
            else:
                name = name + 'Solid'
""" More Test Parameters """
Refinement = 5
plottedRadii = [0.5,0.6,0.7,0.8,0.9]


plyAngleLimits = [-180,180], # or nothing
plyAngleStep = 5


#Load module



""" Computer specific paths """

caeFilePath = 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Propeller_3D-files .prt .stp .iges/HydroWing_'
loadTxtFilePath = 'C:/Users/Jon/OneDrive/FleksProp/Scripts/load.txt'
inputLocation = 'C:/Temp'
#inputFileLocation += '/' + propellerType + '-' + partition + str(partitionRefinement) + '-' + shellOrSolid + '-' + cellOrFace + '-' side
GitHubLoc= r"C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests"

os.chdir(GitHubLoc)
try:
    os.remove('ClassTest.pyc')
except:
    pass

from ClassTest import FleksProp as MC

"""Running the scripts"""
propeller = MC(inputLocation+name+'.cae', 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Trykkfordelinger/P65C_25kn_561rpm__Aba.txt',
                 inputLocation, name, r, partitionMethods,
                 Refinement, shellOrSolidTest,
                 sides, plottedRadii, stepOrCAEimport)

os.chdir(r"C:/temp")
try:
    propeller = MC()#propellerType,plottedRadii,partition,partitionRefinement,shellOrSolid,cellOrFace,side,inputFileLocation, plyAngleLimits, plyAngleStep)
except:
    pass
propeller.SetUpAZP()
#propeller.partition()
#propeller.createInput()



"""Sondre Tweeaked variabler
Aba.Mdb()
part_name = 'AzP65C'
file_p = 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Basic_3D-files .prt .stp .iges/Azp65C-PB_no_Fillet_Solid.stp'
pressure_fi_path = "C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Trykkfordelinger/P65C_25kn_561rpm__Aba.txt"
inputFileLocation = 'C:/Users/Eivind/Documents/NTNU/FleksProp/Models'
r_val = 650
partition = 'Fan'
partitionRefinement = 10
shellOrSolid = 'solid'
sid = 'P'
ratio_li = [0.5,0.6,0.7,0.8,0.9]
step_CAEimp ='step'#'CAE'

p1 = FleksProp(file_p, 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/0_Trykkfordelinger/P65C_25kn_561rpm__Aba.txt',
                 inputLocation, name, r, partitionMethods,
                 Refinement, shellOrSolidTest,
                 sid, ratio_li, stepOrCAEimport)
p1.SetUpAZP()
p1.FullLaminateAZP()
"""





