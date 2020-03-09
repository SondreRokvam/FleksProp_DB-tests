from HydroWing import HydroWing
import numpy as np
caeFilePath = 'C:\Users\Jon\OneDrive\FleksProp\Scripts\HW.cae'
inputFileLocation = 'C:\Users\Jon\OneDrive\FleksProp\InputFiles'

plyAngleLimits = [-90,90] # or nothing
plyAngleNumber = 3 #
plyThickness = 0.2

propeller = HydroWing(caeFilePath)

propeller.all_over(np.linspace(plyAngleLimits[0],plyAngleLimits[1],plyAngleNumber), plyThickness, inputFileLocation)




