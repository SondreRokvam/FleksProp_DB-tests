
""" Computer specific paths """
stpFilePath = 'C:\Users\Jon\OneDrive\FleksProp\HW_2020_02\HydroWing.stp'
loadTxtFilePath = 'C:\Users\Jon\OneDrive\FleksProp\Scripts\load.txt'
inputFileLocation = 'C:\Users\Jon\Documents'
#inputFileLocation += '\' + propellerType + '-' + partition + str(partitionRefinement) + '-' + shellOrSolid + '-' + cellOrFace + '-' side


""" Parameters """
propellerTypes = ['HW', 'A65C']
partitionMethods = ['Fan', 'Grid', 'Horizontal', 'Vertical']
shellOrSolid = ['Solid','Shell']
sides = ['P','S']

proptype = 0
partMeth = 0

partitionRefinement = 5
shellOrSolid = 'Solid' # or 'Shell'
cellOrFace = 'Cell' # or cellOrFace = 'Face'
plottedRadii = [0.5,0.6,0.7,0.8,0.9]


plyAngleLimits = [-45,45], # or nothing
plyAngleStep = 5 #

os.chdir(r"C:\Users\sondreor\Documents\GitHub\FleksProp_DB-tests")
import ClassTest as MC
os.chdir(r"C:\temp")


propeller = MC(propellerType,plottedRadii,partition,partitionRefinement,shellOrSolid,cellOrFace,side,inputFileLocation, plyAngleLimits, plyAngleStep)

propeller.prep()
propeller.partition()
propeller.createInput()






