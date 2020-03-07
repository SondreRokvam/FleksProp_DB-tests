import ModelClass as MC

stpFilePath = 'C:\Users\Jon\OneDrive\FleksProp\HW_2020_02\HydroWing.stp'
loadTxtFilePath = 'C:\Users\Jon\OneDrive\FleksProp\Scripts\load.txt'
inputFileLocation = 'C:\Users\Jon\Documents'

propellerType = 'HW' # or propeller = 'A65C'
plottedRadii = [0.5,0.6,0.7,0.8,0.9]
partition = 'Fan' # or partition = 'Grid', partition = 'Horizontal', partition = 'Vertical'
partitionRefinement = 5
shellOrSolid = 'Solid' # or shellOrSolid = 'Solid'
cellOrFace = 'Cell' # or cellOrFace = 'Face'
side = 'P' # or side = 'S', side = 'PS'
plyAngleLimits = [-45,45], # or nothing
plyAngleStep = 5 #

inputFileLocation += '\' + propellerType + '-' + partition + str(partitionRefinement) + '-' + shellOrSolid + '-' + cellOrFace + '-' side

propeller = MC(propellerType,plottedRadii,partition,partitionRefinement,shellOrSolid,cellOrFace,side,inputFileLocation, plyAngleLimits, plyAngleStep)

propeller.prep()
propeller.partition()
propeller.createInput()






