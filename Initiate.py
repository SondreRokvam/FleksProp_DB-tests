
print '\n\n\n'
from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
import time

#Reset Abaqus, find Githhub
Mdb()
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
