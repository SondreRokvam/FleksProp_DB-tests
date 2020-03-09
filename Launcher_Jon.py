from HydroWing import HydroWing
import numpy as np
caeFilePath = 'C:\Users\Jon\OneDrive\FleksProp\Scripts\HW.cae'
inputFileLocation = 'C:\Users\Jon\OneDrive\FleksProp\InputFiles'

partition = 'AllOver' # or partition = 'Fan', partition = 'Grid', partition = 'Horizontal', partition = 'Vertical', partition = AllOver
#partitionRefinement = 5
shellOrSolid = 'Solid' # or shellOrSolid = 'Solid'
#cellOrFace = 'Cell' # or cellOrFace = 'Face'
#side = 'P' # or side = 'S', side = 'PS'
plyAngleLimits = [-90,90] # or nothing
plyAngleNumber = 5 #
plyThickness = 0.2

propeller = HydroWing(caeFilePath)
print(plyAngleLimits[0])
print(plyAngleLimits[1])
propeller.all_over(np.linspace(plyAngleLimits[0],plyAngleLimits[1],3), plyThickness, inputFileLocation)




