from abaqus import *
from abaqusConstants import *
from odbAccess import *
import sys
import visualization
import xyPlot
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
import math
Parameters = np.load('Parameters_for_plots1.npz')
print Parameters.files

#f = open('C:/temp/dosradx.txt','w')
Jobbs= ['Hollow_Thick', 'Hollow_Thin', 'Pressure_Thick', 'Pressure_Thin', 'Pressure_Thin-w-Ridge', 'Suction_Thick','Suction_Thin','Suction_Thin-w-Ridge']
Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9',
 'PROFILE-R_95']
for i in range(0,len(Jobbs)):
    odb = session.openOdb(name='C:/Temp/'+Jobbs[i]+'.odb')
    for maal in Measurementes:

        #dots =[]
        #dotsm = []
        dots_cyl_langs_x = []
        dots_cyl_langs_xm =[]

        AllNodes = odb.rootAssembly.nodeSets[maal].nodes[0]
        Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region=odb.rootAssembly.nodeSets[maal]).values
        Acount= 0
        for nod in AllNodes:
            x = float(nod.coordinates[0])
            y = float(nod.coordinates[1])
            z = float(nod.coordinates[2])
            xm = float(Disp[Acount].data[0])
            ym= float(Disp[Acount].data[1])
            zm= float(Disp[Acount].data[2])
            Acount =Acount + 1
            #dots.append([x,y,z])
            #dotsm.append([x+xm,y+ym,z+zm])

            ang = math.atan2(y , z)
            angm = math.atan2((y+ym) , (z+zm))
            dots_cyl_langs_x.append([ang, ((y) ** 2 + (z) ** 2) ** 0.5, x ])
            dots_cyl_langs_xm.append([angm, ((y+ym)**2+(z+zm)**2)**0.5, x+xm])


            #f.write(str(math.tan(y/z))+'\t'+str((y**2+z**2)**0.5)+'\t'+str(x)+'\n')




        #np.savez('C:/temp/Profile_w'+maal+'_xyz', np.array(dots))
        #np.savez('C:/temp/Profile_w'+maal+'_xyz_def', np.array(dotsm))
        np.savez('C:/temp/Profile_w '+maal+Jobbs[i]+'_CylynderC_alongX', np.array(dots_cyl_langs_x))
        np.savez('C:/temp/Profile_w '+maal+Jobbs[i]+'_CylynderC_alongX_def', np.array(dots_cyl_langs_xm))
    print('worked')
    #f.close()
    odb.close()